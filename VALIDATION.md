# Validation gates

The production source is checked out at the immutable commit recorded in production.ref. This repository does not duplicate its solver.

## Gate 1: executable toolchain
Compile and execute C# checks on a hosted runner. A workflow file existing is not a passing test.

## Gate 2: numerical mechanics
Positive tetrahedra; density-derived masses; elastic rest stability; rigid-motion invariance; near-volume-preservation; force/gradient finite differences; attachment response; plane and capsule contact; recovery and finite state; invalid input rejection. Test timestep sensitivity rather than claiming timestep independence.

## Gate 3: engine integration
Compile with the pinned Godot .NET SDK, import in the matching engine, run the C# scene headlessly, then capture rendered frames using software rendering where available. Headless checks are not image validation and software rendering does not establish GTX 1080 performance.

## Gate 4: character deformation
Original illustration is authoritative for proportions, outfit, and colors. Require complete animation/deformation tests before claiming game readiness. Initial generated geometry is a development blockout, not a final likeness.

## Results
No numerical solver, engine, or character validation results recorded yet. Inspect the actual workflow run and its source SHA; do not infer success from this checklist.
