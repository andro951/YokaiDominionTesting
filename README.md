# YokaiDominionTesting

Independent, pinned validation workspace for [YokaiDominion](https://github.com/andro951/YokaiDominion). The production solver is not copied here: `production.ref` identifies an immutable production commit, and CI checks out exactly that revision into `production/`.

## Current checks
- Run the production core numerical suite (18 checks).
- Run its rotational-support and volume-regression suite (9 checks).
- Run a one-variable material experiment comparing Poisson ratios 0.48, 0.49, 0.495 and 0.499 at otherwise identical inputs.
- Upload machine-readable reports carrying the source revision, test revision and runtime details.

Production additionally has its own Windows/Linux checks and actual Godot/Blender integration workflows. See [VALIDATION.md](VALIDATION.md) for the acceptance gates and [PROGRESS.md](PROGRESS.md) for observed results and limitations.

## Reproduce locally
Install .NET 10 SDK. From this repository root, clone `https://github.com/andro951/YokaiDominion.git` into `production`, then check out the SHA in `production.ref`. Run `dotnet run --project production/tests/Yokai.Tissue.Checks -c Release`, then `dotnet run --project production/tests/Yokai.Tissue.AdvancedChecks -c Release`, and `dotnet run --project scenarios/MaterialSweep -c Release`.

The production directory and generated reports are ignored by Git. They are not a second source tree to maintain.

## Checkpoint policy
Commit the pin and testing changes together. Distinguish submitted tests from observed passes. Preserve failures and their fixes in history; never weaken assertions merely to make a workflow green. Raw workflow artifacts expire after their configured retention period; durable result summaries and the code needed to regenerate them remain in Git.

This repository does not establish anatomical realism, a finished character, or target-GPU performance merely by reporting passing tests.
