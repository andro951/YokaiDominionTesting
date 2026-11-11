# YokaiDominionTesting

Companion validation repository for the C# character/soft-tissue project in `andro951/YokaiDominion`. The immutable production revision is in `production.ref`; do not maintain another solver here.

## Current checkpoint: milestone 002 character prototype

An actual rigged character, localized volumetric tissue regions, visible surface-deformation integration and native skinned fallback are implemented. The asset and runtime were executed and rendered, not merely written. **Final artistic likeness, high-quality deformation and anatomical physics are not accepted yet.**

Asset source: `95af2eb3f902dac56705f4b6d51f16589a8d8787`, workflow 42971187686.
Validated runtime/renderer: `409ae5f39de720bb12e36cb82050825975f596a9`, workflow 42973867993.
The production pin includes that implementation plus final evidence/run documentation.

The main workflow reruns the production 27 numerical checks and material sweep against the pin, then archives the exact pair of repositories. Character-specific asset and rendered reports are recorded separately: a generic numerical pass does not establish character quality.

See `results/milestone-002.json`, `results/character-002-review.md`, and `CHARACTER_VALIDATION.md`. The independent `tools/inspect_character_glb.py` decodes actual skin/morph animation and reports extreme edge stretching separately from structural integrity. It requires Python and NumPy.

The original character illustration remains authoritative for body proportions, outfit and colours. Neither the secondary sheet nor the current prototype overrides it. Preserve observed failures; do not turn a successful import, a high joint count or a bounded numerical fixture into a claim of final quality.
