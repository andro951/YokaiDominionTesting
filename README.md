# YokaiDominionTesting

Companion validation workspace for [YokaiDominion](https://github.com/andro951/YokaiDominion), a C#-first 3D game and reusable character/soft-tissue simulation package.

## Current status

Repository initialized for planning and write-access verification only. No test suite, engine demo, character, benchmark, or simulator has been implemented or executed yet. Planned checks below are requirements, not passing results.

## Purpose

Provide reproducible numerical tests, engine-integration checks, character deformation scenes, visual captures, and performance measurements. Test the production implementation from a recorded YokaiDominion commit or package version; do not fork the solver into an independent copy here.

The initial engine recommendation under evaluation is Godot 4 .NET. The numerical core should remain portable C# and runnable without an engine or graphics device. Renderer and engine versions must be recorded with each integration result.

## Reference authority

The original single character illustration controls proportions, silhouette, breast size, hip shape, outfit, and colors. The generated turnaround is secondary for details such as hair, horns, face, and missing viewpoints; it must not override conflicting original-image features.

Validate the approved stylized design, not normalized human proportions. Focus advanced tissue response on the breasts and buttocks while preserving the muscular structure elsewhere.

## Planned validation coverage

### Numerical and asset checks

- Mesh, attachment, coordinate-system, unit-scale, and deformation-binding validity.
- Elastic response, volume change, damping, supported equilibrium, and timestep/substep sensitivity.
- Finite-state checks, excessive distortion/inversion handling, collision penetration, and recovery after impacts or discontinuities such as teleports.
- Stable, repeatable fixtures with explicit tolerances; do not assume cross-platform bitwise determinism.

### Movement and contact scenes

- Idle and gravity settling.
- Running, abrupt stops, turns, jumping, running jumps, and hard landings.
- Ground slams, knockdowns, lying on the ground, and getting up.
- Deep squats, arm raises, torso twists, high kicks, and martial-arts poses.
- Arms/body, tissue/body, tissue/ground, and garment contact; hair and tail interactions where implemented.

### Visual and performance checks

- Original-reference silhouette and color checks in controlled lighting.
- Deformation viewed at normal speed and in slow motion from several angles.
- Stable attachment transitions, realistic settling, and absence of obvious clipping or rubber-like behavior.
- Simulation-disabled fallback, distance/detail settings, and multiple-character load tests.
- CPU/GPU timings measured on named hardware, not inferred from headless test success.

## Recording results

Every result should identify the production commit, test revision, toolchain, engine/renderer, platform, settings, and relevant hardware. Separate numerical passes, import/build passes, rendered inspection, and interactive GPU performance validation. An unexecuted test must be labeled untested; a rendered still does not prove animation quality.

## Checkpoint policy

During active work, push small, coherent checkpoints and preserve reproduction steps, known failures, untested work, and the next action. Do not leave the only copy of progress in a temporary session. Keep large generated reports and captures out of ordinary Git history when an artifact store or Git LFS is more appropriate.
