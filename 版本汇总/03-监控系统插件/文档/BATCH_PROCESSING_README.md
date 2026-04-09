# 分批次处理系统使用说明

## 概述

本系统提供了一套完整的影视示例数据分批次处理解决方案，支持10%/30%/60%/100%分批次处理，包含数据处理、质量验证和报告生成功能。

## 文件结构

```
.
├── phase_C_examples.json          # 标准化的示例数据（7个示例）
├── batch_processor.py            # 分批次处理脚本
├── batch_validation.py           # 批次验证脚本
├── test_batch_processing.py      # 系统测试脚本
└── BATCH_PROCESSING_README.md    # 本使用说明
```

## 示例数据格式

`phase_C_examples.json` 包含7个标准化的影视示例，每个示例包含以下字段：

```json
{
  "id": "example_01",
  "title": "温馨回忆（剧情片）",
  "original_content": "完整的示例内容...",
  "creative_density": 0.85,      # 创意密度评分（0-1）
  "p1_count": 3,                 # P1元素数量
  "p2_count": -1,                # P2元素数量（-1表示需要计算）
  "category": "emotional_closeup", # 示例类别
  "keywords": ["温馨", "回忆", "特写", "情感表达"],
  "character_count": 120,        # 字符数
  "word_count": -1               # 单词数（-1表示需要计算）
}
```

## 使用方法

### 1. 运行测试

```bash
# 运行完整测试套件
python test_batch_processing.py
```

### 2. 处理单个批次

```bash
# 处理10%的批次
python batch_processor.py --single 10

# 处理30%的批次，使用分层抽样策略
python batch_processor.py --single 30 --strategy stratified
```

### 3. 处理多个批次

```bash
# 处理10%/30%/60%/100%批次（默认）
python batch_processor.py

# 自定义批次百分比
python batch_processor.py --batch 20 50 80
```

### 4. 验证批次结果

```bash
# 验证单个批次报告
python batch_validation.py batch_report_*.json

# 验证多个批次报告，保存到指定目录
python batch_validation.py batch_report_*.json --output-dir validation_results

# 只显示摘要，不保存详细结果
python batch_validation.py batch_report_*.json --summary-only
```

## 命令行参数

### batch_processor.py

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--examples` | 示例数据文件路径 | `phase_C_examples.json` |
| `--batch` | 批次百分比列表 | `10 30 60 100` |
| `--strategy` | 示例选择策略（random/stratified/sequential） | `random` |
| `--single` | 运行单个批次（指定百分比） | 无 |

### batch_validation.py

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `report_files` | 批次报告文件路径（支持通配符） | 必需 |
| `--output-dir` | 输出目录 | `validation_results` |
| `--summary-only` | 只显示摘要，不保存详细结果 | 否 |

## 输出文件

### 批次处理器输出

- `batch_report_{batch_id}.json` - 批次处理报告
- `batch_processing.log` - 处理日志
- `overall_batch_report_{timestamp}.json` - 总体报告（多批次时）

### 批次验证器输出

- `validation_result_{batch_id}.json` - 验证结果
- `batch_validation.log` - 验证日志
- `overall_validation_report.json` - 总体验证报告（多批次时）

## 验证标准

系统使用以下标准验证批次处理质量：

### 必须满足（Must Have）
- 平均质量评分 ≥ 0.6
- P1元素保留率 ≥ 70%
- 错误率 ≤ 10%
- 平均处理时间 ≤ 5秒/示例

### 应该满足（Should Have）
- 平均质量评分 ≥ 0.8
- P2元素保留率 ≥ 50%
- 错误率 ≤ 5%
- 长度保留率在 0.5-2.0 之间

### 最好满足（Nice to Have）
- 平均质量评分 ≥ 0.9
- 所有示例无错误
- 处理时间稳定且可预测
- 良好的长度保留一致性

## 扩展和自定义

### 1. 添加新的示例数据

编辑 `phase_C_examples.json`，在 `examples` 数组中添加新的示例对象。

### 2. 修改处理逻辑

在 `batch_processor.py` 中修改 `process_example()` 和 `simulate_processing()` 方法，实现实际的处理逻辑。

### 3. 调整验证规则

在 `batch_validation.py` 中修改 `load_validation_rules()` 方法，调整验证阈值和标准。

### 4. 添加新的验证检查

在 `BatchValidator` 类中添加新的检查方法，并在 `validate_batch_report()` 中调用。

## 故障排除

### 常见问题

1. **示例数据加载失败**
   - 检查 `phase_C_examples.json` 格式是否正确
   - 确保文件编码为 UTF-8

2. **批次处理失败**
   - 检查日志文件 `batch_processing.log`
   - 确保有足够的示例数据

3. **验证失败**
   - 检查批次报告文件是否存在且格式正确
   - 查看 `batch_validation.log` 获取详细信息

### 日志文件

系统生成两个日志文件：
- `batch_processing.log` - 批次处理日志
- `batch_validation.log` - 批次验证日志

查看日志文件可以帮助诊断问题：
```bash
tail -f batch_processing.log  # 实时查看处理日志
cat batch_validation.log      # 查看验证日志
```

## 性能优化建议

1. **大数据集处理**
   - 考虑使用多进程/多线程处理
   - 实现增量处理，避免内存溢出

2. **实时监控**
   - 添加进度条显示
   - 实现实时质量监控

3. **结果缓存**
   - 缓存处理结果，避免重复处理
   - 实现断点续传功能

## 版本历史

- v1.0.0 (2026-01-30): 初始版本
  - 支持10%/30%/60%/100%分批次处理
  - 包含完整的验证系统
  - 提供7个标准化影视示例

## 技术支持

如有问题或建议，请：
1. 查看日志文件获取详细信息
2. 运行测试脚本验证系统功能
3. 检查示例数据格式是否正确

## 许可证

本系统为开源项目，遵循 MIT 许可证。