---
name: plant-scientific-workflow
description: Apply the plant-geometry-phenotyping-lab scientific contract when changing pipeline stages, cross-view identity matching, Gaussian artifacts, calibrated traits, evaluation, experiments, or manuscript claims.
---

# Plant Scientific Workflow

1. Read root `AGENTS.md`, `Makefile`, `configs/pipeline.toml`, the target dataset TOML and `.planning/REVISION_ACTION_CHARTER.md`.
2. Preserve the live dirty worktree; never clean, reset, bulk-stage or overwrite existing experiment records.
3. Treat plant as the independent unit. Keep splits plant-disjoint and frozen; never tune on final holdout data.
4. Evaluate cross-view identity directly. Downstream point-cloud or trait metrics cannot replace matcher evaluation.
5. Do not use manual dimensions to select predicted organs in primary evaluation.
6. Record code/data/config/seed/environment/hardware/artifact hashes. Distinguish deterministic bootstrap from real optimized 3DGS.
7. Validate by scope: targeted pytest; `make lint`; full `make test` for shared contracts; safe `make dry-run` for pipeline/config. Full runs require explicit authorization.
8. A failed `quality_gate.status` or scientific gate blocks promotion. Report limitations and the strongest supportable claim.
