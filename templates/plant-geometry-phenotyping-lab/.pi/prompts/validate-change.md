---
description: 按植物表型仓库的分层验证合同检查当前改动
argument-hint: "[文件、模块或改动范围]"
---
# 植物表型改动验证

验证 ${@:-当前改动}。先检查现有工作树并只评估目标范围：文档改动检查引用和事实；Python 改动运行定向 pytest 与 `make lint`；共享契约改动再运行 `make test`；pipeline/config 改动增加安全数据集的 `make dry-run`；科学评估改动检查 plant-disjoint、冻结配置、输入哈希、直接身份指标和 quality gate。不得启动完整 `make run`、访问 sealed test 或重新生成大型产物，除非用户明确授权。报告每条命令、退出状态和未验证环境。
