# Testing progress

The production numerical suite at 9437302ce6353d6a3006d73e4ad0c9feaa473e59 passed on Windows and Linux (production Actions run 42955998709).

The initial Godot fixture at 8a97326999b7ad1de1a1d6c3719a13962bd114a9 compiled, ran headlessly, and rendered a real screenshot (production run 42956320270). Inspection found roughly 11-13% maximum local volume change at the end/capture of its trajectory. This is too compressible for the intended flesh target, despite the integration test passing.

Added MaterialSweep: same mesh, Young modulus, density, drive trajectory and integration settings; vary only Poisson ratio 0.48/0.49/0.495/0.499. Record peak/final volume change, minimum Jacobian, inverted element samples, finite-state checks, and hosted-runner timing. Do not adjust acceptance thresholds silently or call the illustrative material biologically calibrated.

At this checkpoint the sweep has been submitted but its result has not yet been observed. Keep the exact production SHA pinned in production.ref.
