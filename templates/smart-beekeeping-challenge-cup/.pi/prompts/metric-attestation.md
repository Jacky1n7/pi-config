---
description: 为检测、跟踪或行为量化指标生成可追溯证明
argument-hint: "<指标文件、run 或结论>"
---
# 指标证明

为 $@ 建立指标证明。记录 modality、source video/clip、split、GT policy（例如 clean46/orig196/kfign196）、annotation/export revision、model checksum、runtime config checksum、evaluator revision、seed、hardware、PT/ONNX 路径和调参/报告序列边界。检查相邻帧泄漏和测试序列调参；无法从保存预测重算的指标标为 UNATTESTED。不要把 structural validator 通过描述成完整竞赛验收。
