---
name: beekeeping-competition-workflow
description: Apply the smart-beekeeping Challenge Cup competition contract for dataset annotation, YOLO detection, BeeTracker tracking, behavior quantification, metric reporting, CVAT workflows, GPU training, and Windows delivery.
---

# Beekeeping Competition Workflow

1. Read root `AGENTS.md`, `CLAUDE.md`, the competition PDF/Markdown spec and the relevant `赛事部署包/*/README.md`.
2. Preserve the very dirty worktree. Never clean/reset/bulk-stage or delete ignored data, videos, labels, weights, results or deliveries.
3. Treat raw competition videos as read-only; never inspect hidden-test content or use leaderboard/holdout feedback for tuning.
4. Keep the primary class `bee` with `class_id=0`. Split by source video/clip, never adjacent random frames.
5. Bind metrics to modality, GT policy, split, annotation revision, model/runtime/evaluator hashes and tuning/reporting sequence roles.
6. Local Mac validation is dependency-light only. GPU training runs on the AutoDL data disk; Windows delivery requires real x86_64 NVIDIA black-box validation.
7. External data, CVAT/network actions, training, packaging, upload and submission require explicit authorization. Never expose credentials or infrastructure details.
8. Report what was locally validated, remotely validated, skipped, or unattested; structural validation is not full competition acceptance.
