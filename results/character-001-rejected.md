# First character prototype: rejected deformation baseline

Production checkpoint `0a85f344a94c1a1db87505bb54314cac8dbc460b`, Actions run 42964482725. The authoring/export workflow completed and actual renders were inspected. This was not a successful rig-quality result.

GLB SHA256: `41a37aa1d5e093d226cce795daae39189827d5949bb0387602a6ff304aed973c`.

The body was manifold with normalized four-influence weights and 72 exported joints. However, abrupt anatomical candidate boundaries assigned outer chest vertices to arms. The overhead render showed severe stretching. The independent NumPy GLB sampler measured a 99.9th-percentile edge stretch of 111.08x and maximum 332.96x for edges longer than 2 mm. High-kick and crouch showed related transition problems. Structural checks alone would not catch this.

The next authoring pass uses smooth anatomical support masks, explicit chest support, a continuous leg form, and a smaller mesh. A follow-up build caught more than four influences on auxiliary hair/tail meshes; that was fixed by normalizing the final four influences consistently across all meshes. No failure threshold was weakened.

The companion `tools/inspect_character_glb.py` reconstructs actual exported skinning and morph animation, rather than trusting that named clips exist. It reports stretch diagnostics separately from its structural pass. Results are not a claim of anatomical realism or collision quality.
