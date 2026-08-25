---
description: 审核论文表述是否由当前实验和产物直接支持
argument-hint: "[章节、表格、图或 claim]"
---
# 论文证据审核

审核 ${@:-当前论文改动} 的证据链。以当前代码、冻结协议、per-plant 结果和可追溯表格/图脚本为准；逐条标记 SUPPORTED、OVERSTATED、STALE、MISSING EVIDENCE。检查数据划分、统计单位、置信区间、多重比较、baseline 公平性、deterministic bootstrap 与真实 gsplat 优化的区别，以及 sequence-aware 与 4D 的边界。没有 canonical TeX 构建命令时不得声称 PDF 已重建。
