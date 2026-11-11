# Testing progress

## Observed results
- Production baseline 9437302ce6353d6a3006d73e4ad0c9feaa473e59 passed 18 checks on Windows and Linux (run 42955998709).
- Production initial Godot fixture 8a97326999b7ad1de1a1d6c3719a13962bd114a9 compiled, ran headlessly and produced an inspected engine screenshot (run 42956320270).
- The first material was visibly too compressible. Testing commit 20ada9ecae58144b6b9b974a196f7b2aca588140 ran the one-variable study against production ec943fc6301626a424d5d198736b5032710afdc1 (run 42957245209). Selected measured results are retained in results/material-sweep-initial.json.
- Production 146f48c2089630680656009fb8f16634e0653f16 passed the full 27-check suite (18 core + 9 advanced) on Windows and Linux in run 42957968022, after correcting two target-typed argument ambiguities. Assertions were not loosened.

## Current checkpoint
Pinned production now includes the native asset-import fix that merges bone and morph animation into a single exported clip. This testing workflow runs all 27 production checks plus the material sweep and archives both exact source trees. Its own result must still be observed after submission.

## Still not established
No final character geometry or anatomical calibration; no end-to-end full-body animation/tissue interaction; no triangle self-contact or CCD; no clothing restraint; no target-PC GPU measurement. The numerical material experiment is not a biological validation study.
