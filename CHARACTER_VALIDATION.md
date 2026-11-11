# Character validation

Use the exact production revision in production.ref; the production repository contains the only solver implementation.

## Current anatomical authoring path

Run production `tools/blender/build_character_anatomy.py` in Blender 4.5.3 LTS with `--base-data` pointing to the selected CC0 data and `--out` pointing to an artifact directory. The immutable upstream revision and graphical-data-only licensing are in production THIRD_PARTY_ASSETS.md. The older refined/primitive scripts reproduce rejected baselines, not the current asset.

## Independent checks

Run `dotnet run --project production/tests/Yokai.Character.Checks -c Release -- PATH/tissue-regions.json results/character-numerical.json` for the authored cages.

With Python and NumPy, run `python tools/inspect_character_glb.py PATH/character-blockout.glb --report results/character-glb-audit.json`. It decodes sparse morph accessors, sampled skinning and animation transforms and reports stretching on edges longer than 2 mm. Structural success is not deformation-quality acceptance.

Godot CharacterLab tests imported pose changes relative to neutral, support coordinate transforms, visible tissue displacement, finite states, inversions and the native-skin fallback. Its render mode captures actual poses and a controlled four-second motion fixture. ColorCalibration compares rendered vertex-colour swatches to reference material swatches. Check images and recorded numerical values as well as workflow status.

The full authoring workflow regenerates assets. The fast renderer regression reuses an exact artifact and SHA-256; after that artifact expires it must be regenerated and repinned explicitly. Never silently substitute latest assets.

The existing main validation workflow runs 27 general numerical checks plus the material sweep against the production pin. It does not rerun expensive character authoring/rendering; those run IDs and results are recorded separately.
