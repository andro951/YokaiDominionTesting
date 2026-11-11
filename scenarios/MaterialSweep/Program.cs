using System.Diagnostics;
using System.Text.Json;
using Yokai.Tissue;

// Change only Poisson ratio; retain shear/Young-scale intent, mesh, drive and integration settings.
// This is a numerical characterization experiment, not a biological material fit.
var results=new List<object>(); bool failed=false;
foreach(double nu in new[] {0.48,0.49,0.495,0.499})
{
    var mesh=TetMesh.Block(3,3,3,new(0.5,0.3,0.35),new(-0.25,1,-0.175));
    var body=new TissueBody(mesh,new TissueMaterial(6500,nu),new SolverSettings {Substeps=4,Iterations=5,VelocityDrag=1});
    for(int i=0;i<mesh.VertexCount;i++) if(mesh.RestPositions[i].Y>1.299) body.Attach(i);
    body.Contacts.Add(new ContactPlane(V3.UnitY,0));
    double maxError=0,minJ=double.PositiveInfinity; int inverted=0; bool finite=true;
    var watch=Stopwatch.StartNew();
    for(int frame=0;frame<600;frame++)
    {
        double time=(frame+1)/120.0,u=(time-1)/0.75;
        double elevation=u>=0&&u<=1 ? 0.3*Math.Pow(Math.Sin(Math.PI*u),2):0;
        body.Step(1.0/120,new V3(0.025*Math.Sin(time*2),elevation,0));
        var d=body.Inspect();
        maxError=Math.Max(maxError,d.MaxVolumeError); minJ=Math.Min(minJ,d.MinJacobian); inverted+=d.InvertedElements; finite&=d.Finite;
    }
    watch.Stop(); var final=body.Inspect();
    bool passed=finite&&inverted==0;
    failed|=!passed;
    Console.WriteLine($"nu={nu:F3} peak volume error={maxError:P3}, final={final.MaxVolumeError:P3}, minimum J={minJ:F6}, inversions={inverted}, finite={finite}, ms/tick={watch.Elapsed.TotalMilliseconds/600:F3}");
    results.Add(new {poissonRatio=nu,youngModulusPa=6500,peakRelativeVolumeError=maxError,finalRelativeVolumeError=final.MaxVolumeError,minJacobian=minJ,invertedElementSamples=inverted,finite,passed,millisecondsPerTick=watch.Elapsed.TotalMilliseconds/600});
}
Directory.CreateDirectory("artifacts");
File.WriteAllText("artifacts/material-sweep.json",JsonSerializer.Serialize(new {
    schemaVersion=1,productionCommit=File.ReadAllText("production.ref").Trim(),testCommit=Environment.GetEnvironmentVariable("GITHUB_SHA")??"local",
    runtime=System.Runtime.InteropServices.RuntimeInformation.FrameworkDescription,os=System.Runtime.InteropServices.RuntimeInformation.OSDescription,
    warning="Hosted-runner timing is not target-PC performance. Material values are illustrative, not biological measurements.",results
},new JsonSerializerOptions {WriteIndented=true}));
return failed?1:0;
