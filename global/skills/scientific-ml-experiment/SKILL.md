---
name: scientific-ml-experiment
description: Plan, execute, validate, and report reproducible scientific machine-learning or computer-vision experiments with data-lineage, leakage, metric-attestation, and artifact safeguards. Use for model training, evaluation, ablations, dataset changes, scientific figures, or claims based on experiment results.
---

# Scientific ML Experiment

## When to Use

Use for training, evaluation, ablations, dataset/split changes, model comparisons, paper tables/figures, or any claim derived from ML/CV results. Do not use for ordinary code-only changes with no experimental evidence.

## Procedure

1. Read the project `AGENTS.md`, authoritative evaluation specification, current Git status, and existing experiment conventions.
2. State the hypothesis, independent statistical unit, primary metric, comparison baseline, acceptance threshold, non-goals, and compute budget before running.
3. Freeze and identify inputs: data/split manifest, annotation revision, preprocessing, config, seeds, code revision, environment and hardware.
4. Prove leakage controls appropriate to the domain: group by plant/specimen/video/clip/hive/site/time as required; never tune on hidden or final holdout data.
5. Start with the cheapest representative validation. Escalate from schema/unit checks to tiny integration, smoke training, full training, and blind evaluation only when earlier gates pass.
6. Record each run with command, exit status, resolved config, hashes, metrics, predictions, logs, runtime, environment and artifact paths.
7. Compare like with like. Every reported metric must name its split/ground-truth policy, evaluator revision and model/config identity.
8. Generate tables and figures from recorded artifacts; do not manually edit values.
9. Report failures and uncertainty explicitly. Do not convert a failed scientific gate into a prose warning.

## Approval and Stop Conditions

Stop and ask before accessing sealed/hidden test data, uploading submissions, using new external datasets, changing the primary metric/split after results are visible, spending material paid compute, deleting artifacts, or publishing claims.

## Verification

- Confirm the repository did not gain raw data, secrets, weights or unintended large files.
- Run project-declared schema/leakage tests and focused code tests.
- Verify run metadata and checksums are complete.
- Recompute the primary metric from saved predictions when practical.
- State what was not reproduced across machines, frameworks or GPU versions.

## Output

Return: hypothesis; run ID; code/data/config identities; environment; commands; validation results; metric table with exact protocol; artifact paths/hashes; limitations; promotion decision; next experiment.
