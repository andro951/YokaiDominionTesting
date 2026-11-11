# Testing progress - engineering milestone 001

## Observed evidence
- Production current numerical core at e9705b8bb049975cf3e4fe2b4b019938ebbe232e passed 18 core plus 9 advanced checks on Windows and Linux (production run 42958865072).
- Godot lab at adaaf334b7a0d623857fd3dac4a4ae2db35c1fa7 compiled, ran headlessly, and produced an inspected software-rendered frame (run 42958219773). Its jump fixture had about 2.91% peak local volume change, 1.16% at the endpoint, and no inverted elements.
- Blender-to-native-Godot asset path at e9705b8bb049975cf3e4fe2b4b019938ebbe232e passed structural export checks and imported animation sampling in headless/rendered modes (run 42958864946). The rendered bent limb was inspected. This is a calibration asset, not the character.
- Independent testing revision b1d86c4ac241ba50b2a2ba2910e3d94689369084 passed all 27 production checks and the material sweep against its pinned production revision (testing run 42958498338).

## Retained experiment
results/material-sweep-initial.json records exact selected measurements from testing run 42957245209. Varying only Poisson ratio reduced peak local volume error from roughly 30.72% at 0.48 to 2.91% at 0.499. No inverted or non-finite samples occurred. This is fixture characterization, not biological material fitting.

## Current pin
production.ref now points to bb049bc1a7ea63b6424380db25cd76cbd9cd8156, the production documentation/evidence handoff after verified code revision e9705b8. The current testing run is submitted by this commit and must be observed rather than assumed successful. Its artifacts include both exact source trees and all current numerical reports.

## Next work and limitations
Original-reference body proportions, early full-body deformation rig, character-specific tissue regions and graded attachments are next. Final anatomy, skin layers, cloth support, hair/tail physics, full-body animations/ragdoll, robust self/continuous contact and target-GPU performance are not established. Full reference images are identified by exact hashes in production; bytes are preserved in the conversation/handoff archive rather than committed via the text connector.
