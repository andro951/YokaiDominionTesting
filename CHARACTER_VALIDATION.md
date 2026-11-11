# Character validation

Use the exact production revision in production.ref. The main repository contains the only solver implementation.

Run the production authoring entrypoint `tools/blender/build_character_refined.py` in Blender 4.5.3 LTS. It writes the editable .blend, GLB, tissue-regions.json, manifests and rendered pose studies.

Run `dotnet run --project production/tests/Yokai.Character.Checks -c Release -- PATH/tissue-regions.json results/character-numerical.json` to check the authored cages against the pinned production solver.

With Python and NumPy, run `python tools/inspect_character_glb.py PATH/character-blockout.glb --report results/character-glb-audit.json` to independently decode and sample the exported asset. Sparse morph accessors and constant/linear rotation channels are handled. Inspect stretch metrics and actual images: a structural pass does not mean rig-quality acceptance.

Godot's CharacterLab scene checks imported poses, support coordinate transforms, transfer of simulated motion to the visible body, finite states, element inversions, and the physics-disabled fallback. Its rendered mode also captures a motion sequence. These are engineering gates, not artistic approval or production physics certification.
