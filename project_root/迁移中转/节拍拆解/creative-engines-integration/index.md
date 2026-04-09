---
name: creative-engines-integration-index
description: 创意引擎系统集成指南入口文件。规范视觉叙事与蒙太奇逻辑引擎、影视联想与融合引擎、通感视觉化引擎的调用时机、输入输出格式和冲突解决规则。
---

# 创意引擎集成指南（Creative Engines Integration）

## 文档索引

本文档已被拆分为多个子模块。

### 核心规格
- [01-engine-specs.md](./01-engine-specs.md) - 三个引擎的技术规格
- [02-call-sequence.md](./02-call-sequence.md) - 引擎调用时序规范

### 融合规则
- [03-output-fusion.md](./03-output-fusion.md) - 引擎输出融合与冲突解决
- [04-output-mapping.md](./04-output-mapping.md) - 引擎输出到分镜的映射规则

### 质量与性能
- [05-quality-assurance.md](./05-quality-assurance.md) - 质量保证与验证
- [06-performance.md](./06-performance.md) - 性能指标与优化

### 测试与维护
- [07-test-cases.md](./07-test-cases.md) - 集成测试用例
- [08-maintenance.md](./08-maintenance.md) - 更新与维护

---

## 核心引擎

| 引擎 | 功能 | 调用频率 |
|------|------|----------|
| 视觉叙事与蒙太奇逻辑 | 镜头资源分配 | 每关键帧1次 |
| 影视联想与融合 | 视觉风格参考 | 每场景1次 |
| 通感视觉化 | 感官转化视觉 | 每感官事件1次 |

## 版本信息
- 版本：拆分后 v2.0
- 原始文件：creative-engines-integration/ (773行)
- 拆分日期：2026-01-19
