# Validation gates

The production source is checked out at the immutable commit recorded in production.ref. This repository does not duplicate its solver.

## Gate 1: executable toolchain - established
C# core checks compile and execute on Windows and Linux in the production workflow. A workflow file existing is not itself a pass; exact observed runs are recorded in PROGRESS.md and production docs/evidence/milestone-001.json.

## Gate 2: numerical baseline - established for named tests
18 core and 9 advanced checks cover tetrahedron orientation, mass, energy/stress gradients, rest and rigid-motion invariance, attachments, analytic contact, embedding, pose conventions and a specific jump-volume envelope. A material sweep varies Poisson ratio while keeping other fixture inputs fixed. These tests do not prove arbitrary-motion stability, convergence or anatomical accuracy.

## Gate 3: engine/asset path - established for calibration fixtures
Godot .NET builds, imports and executes the tissue lab headlessly and through software rendering. Blender creates an editable test rig, morph and animation; GLB structural validation and native Godot sampling check the imported bone motion and corrective together. Actual rendered images were downloaded and inspected. Software rendering does not establish target-PC performance.

## Gate 4: character deformation - not established
No finished character mesh or full-body rig exists yet. Preserve the original illustration's proportions, outfit and palette. Establish an early full-body deformation setup, localized simulation regions and difficult-pose tests before cosmetic polish. The generic block and limb are not the character.

## Gate 5: realistic contact and production readiness - not established
Require anatomical support/skin behavior, motion-dependent damping, robust surface/self/continuous contact, clothing restraint, hair/tail interaction, falls and get-up tests, and measured runtime/performance on the intended machine. Passing the numerical baseline does not imply these features exist.

## Reporting
Keep source and test revisions in reports. Retain measured summaries in Git because binary workflow artifacts expire. Archive the exact source pair for reproducibility. Do not weaken assertions to conceal failures, present pending runs as complete, or report hosted-runner timings as user hardware benchmarks.
