"""Independent GLB structural and sampled-skin deformation audit (Python + NumPy).
A structural pass is NOT an artistic/deformation-quality pass. Requires NumPy.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import struct
import numpy as np

TYPES={5120:'i1',5121:'u1',5122:'<i2',5123:'<u2',5125:'<u4',5126:'<f4'}
WIDTH={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4,'MAT4':16}
class GLB:
    def __init__(self,path):
        raw=Path(path).read_bytes()
        magic,version,length=struct.unpack_from('<III',raw)
        if magic!=0x46546c67 or version!=2 or length!=len(raw):raise ValueError('Invalid GLB header')
        offset=12;self.doc=None;self.binary=None
        while offset<len(raw):
            count,kind=struct.unpack_from('<II',raw,offset);data=raw[offset+8:offset+8+count];offset+=count+8
            if kind==0x4e4f534a:self.doc=json.loads(data)
            elif kind==0x004e4942:self.binary=data
        if self.doc is None or self.binary is None:raise ValueError('Missing GLB chunks')
    def accessor(self,index):
        a=self.doc['accessors'][index];dt=np.dtype(TYPES[a['componentType']]);w=WIDTH[a['type']]
        def read(view,offset,count,width,dtype):
            v=self.doc['bufferViews'][view];stride=v.get('byteStride',width*dtype.itemsize)
            return np.ndarray((count,width),dtype=dtype,buffer=self.binary,offset=v.get('byteOffset',0)+offset,strides=(stride,dtype.itemsize)).copy()
        result=read(a['bufferView'],a.get('byteOffset',0),a['count'],w,dt) if 'bufferView' in a else np.zeros((a['count'],w),dtype=dt)
        if 'sparse' in a:
            sp=a['sparse'];idx=sp['indices'];val=sp['values']
            indices=read(idx['bufferView'],idx.get('byteOffset',0),sp['count'],1,np.dtype(TYPES[idx['componentType']])).ravel()
            result[indices]=read(val['bufferView'],val.get('byteOffset',0),sp['count'],w,dt)
        if a.get('normalized',False) and dt.kind in 'iu':result=result.astype(float)/np.iinfo(dt).max
        return result

def matrix(translation,rotation,scale):
    x,y,z,w=np.asarray(rotation,dtype=float)/np.linalg.norm(rotation)
    r=np.array([[1-2*(y*y+z*z),2*(x*y-z*w),2*(x*z+y*w)],[2*(x*y+z*w),1-2*(x*x+z*z),2*(y*z-x*w)],[2*(x*z-y*w),2*(y*z+x*w),1-2*(x*x+y*y)]])
    m=np.eye(4);m[:3,:3]=r@np.diag(scale);m[:3,3]=translation;return m

def sample(g,time):
    nodes=g.doc['nodes'];trs=[{'translation':n.get('translation',[0,0,0]),'rotation':n.get('rotation',[0,0,0,1]),'scale':n.get('scale',[1,1,1])} for n in nodes];morph={}
    anim=g.doc['animations'][0]
    for channel in anim['channels']:
        s=anim['samplers'][channel['sampler']];times=g.accessor(s['input']).ravel();values=g.accessor(s['output'])
        target=channel['target'];path=target['path'];node=target['node']
        if s.get('interpolation','LINEAR') not in ('LINEAR','STEP'):raise ValueError('Unsupported animation interpolation')
        values=values.reshape(len(times),-1)
        hi=min(len(times)-1,int(np.searchsorted(times,time,side='right')));lo=max(0,hi-1)
        alpha=float(np.clip((time-times[lo])/(times[hi]-times[lo]),0,1)) if hi!=lo else 0.0
        if s.get('interpolation')=='STEP':alpha=0
        a,b=values[lo],values[hi]
        if path=='rotation':
            dot=float(np.dot(a,b))
            if dot<0:b=-b;dot=-dot
            if dot<.9995:
                theta=np.arccos(np.clip(dot,-1,1));value=(np.sin((1-alpha)*theta)*a+np.sin(alpha*theta)*b)/np.sin(theta)
            else:value=a*(1-alpha)+b*alpha
            value=value/np.linalg.norm(value)
        else:value=a*(1-alpha)+b*alpha
        if path=='weights':morph[node]=value
        else:trs[node][path]=value
    local=[np.array(n['matrix']).reshape(4,4).T if 'matrix'in n else matrix(**t) for n,t in zip(nodes,trs)]
    parent={c:i for i,n in enumerate(nodes) for c in n.get('children',[])};world={}
    def transform(i):
        if i not in world:world[i]=transform(parent[i])@local[i] if i in parent else local[i]
        return world[i]
    for i in range(len(nodes)):transform(i)
    return world,morph

def inspect(path):
    g=GLB(path);d=g.doc;node=next(i for i,n in enumerate(d['nodes']) if n.get('name')=='Body' and 'mesh'in n)
    nd=d['nodes'][node];mesh=d['meshes'][nd['mesh']];skin=d['skins'][nd['skin']]
    ib=g.accessor(skin['inverseBindMatrices']).reshape(-1,4,4).transpose(0,2,1)
    names={d['nodes'][i].get('name') for i in skin['joints']}
    required={'Pelvis','Chest','Head','Clavicle.L','ForearmTwist.R','Thigh.L','Hand.R','Index3.L','Foot.R','Tail05'}
    if not required.issubset(names):raise ValueError('Missing required named joints '+str(required-names))
    total=0;triangles=0;results=[];primitives=[]
    for p in mesh['primitives']:
        a=p['attributes'];v=g.accessor(a['POSITION']);weights=g.accessor(a['WEIGHTS_0']);joints=g.accessor(a['JOINTS_0']).astype(int)
        if not np.isfinite(v).all() or not np.isfinite(weights).all():raise ValueError('Nonfinite vertex data')
        if np.max(abs(weights.sum(axis=1)-1))>.001 or np.min(weights)<0:raise ValueError('Non-normalized or negative skin weights')
        if joints.max()>=len(skin['joints']):raise ValueError('Invalid skin joint index')
        ids=g.accessor(p['indices']).ravel().astype(int).reshape(-1,3)
        if ids.max()>=len(v):raise ValueError('Invalid triangle index')
        targets=[g.accessor(t['POSITION']) for t in p.get('targets',[])]
        edges=np.concatenate([ids[:,[0,1]],ids[:,[1,2]],ids[:,[2,0]]]);length=np.linalg.norm(v[edges[:,0]]-v[edges[:,1]],axis=1);ok=length>.002
        primitives.append((v,weights,joints,targets,edges[ok],length[ok]));total+=len(v);triangles+=len(ids)
    for name,time in [('neutral',0),('overhead',1),('crouch',2),('high-kick',3),('twist',4),('jump',5),('knockdown',6),('recover',7)]:
        world,morph=sample(g,time);bones=np.stack([world[j]@bind for j,bind in zip(skin['joints'],ib)]);ratios=[];allpos=[]
        for v,weights,joints,targets,edges,length in primitives:
            source=v.copy()
            for target,w in zip(targets,morph.get(node,[])):source+=target*w
            hom=np.column_stack([source,np.ones(len(source))]);position=np.zeros((len(v),3))
            for slot in range(4):position+=np.einsum('nij,nj->ni',bones[joints[:,slot]],hom)[:,:3]*weights[:,slot,None]
            if not np.isfinite(position).all():raise ValueError('Nonfinite posed surface')
            ratios.extend(np.linalg.norm(position[edges[:,0]]-position[edges[:,1]],axis=1)/length);allpos.append(position)
        ratios=np.asarray(ratios);pos=np.concatenate(allpos)
        results.append({'pose':name,'edgeStretchP99':float(np.quantile(ratios,.99)),'edgeStretchP999':float(np.quantile(ratios,.999)),'maxEdgeStretch':float(max(ratios)),'edgesOver4x':int(sum(ratios>4)),'boundsMin':pos.min(axis=0).tolist(),'boundsMax':pos.max(axis=0).tolist()})
    return {'fileSha256':hashlib.sha256(Path(path).read_bytes()).hexdigest(),'structuralChecksPassed':True,'bodyExportVertices':total,'bodyTriangles':triangles,'skinJointCount':len(skin['joints']),'poseDeformation':results,'limitation':'Structural integrity and large-stretch diagnostics only. Self intersection, contacts, silhouette fidelity and artistic quality require separate review.'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('glb',type=Path);p.add_argument('--report',type=Path,required=True);a=p.parse_args();result=inspect(a.glb);a.report.parent.mkdir(parents=True,exist_ok=True);a.report.write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
