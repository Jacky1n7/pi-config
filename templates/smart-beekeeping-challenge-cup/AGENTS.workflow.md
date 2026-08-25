<!-- markdownlint-disable MD041 -->

## Pi 工作流补充

- 当前仓库包含大量未提交/未跟踪数据与产物。任何任务先检查目标路径；禁止 `git clean`、force reset/checkout、`git add .`、批量格式化或删除忽略目录。
- 工作流按成本分层：本地 dependency-light unittest/结构校验 → manifest/泄漏/指标证明 → AutoDL 5090 训练与评测 → Windows NVIDIA 黑盒交付。不同层级不得相互冒充。
- 多代理默认只并行审计规范、代码、指标和文档；同一工作树只允许一个写入者。训练、CVAT、远端、打包、上传、提交比赛均需明确授权。
- 代码审查优先检查：相邻帧泄漏、hidden-test 接触、`bee/class_id=0` 漂移、YOLO/COCO/MOT 格式、GT 口径混用、指标缺少哈希/运行配置、CPU 静默回退、交付 stdout/错误码/时延/VRAM 违约。
- 项目级 Skill：`beekeeping-competition-workflow`；Prompt：`/competition-review`、`/metric-attestation`、`/delivery-check`。
