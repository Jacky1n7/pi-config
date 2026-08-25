---
description: 按赛题原始规范审核数据、代码、指标和交付改动
argument-hint: "[目标文件、实验或交付物]"
---
# 竞赛合同审核

审核 ${@:-当前改动}。以 `数据集及评测机制说明20260527.pdf` 及其版本化 Markdown 转录为硬约束，检查 `bee/class_id=0`、YOLO/COCO/MOT 格式、按视频/片段切分、hidden-test 隔离、外部数据披露、ONNX/Windows onedir/单行 JSON stdout、错误码、时延和 VRAM。每个指标必须绑定 GT 口径、split、模型/配置/评测脚本哈希。不要打开或遍历原始视频和大型训练产物；输出 BLOCK/READY WITH NOTES/READY。
