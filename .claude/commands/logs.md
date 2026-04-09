> **Description:** 日志查询命令处理器

# 日志查询系统

## 命令列表

| 命令 | 功能 | 示例 |
|------|------|------|
| `/logs` | 显示最近3次执行摘要 | `/logs` |
| `/logs last` | 显示最近1次执行详情 | `/logs last` |
| `/logs <exec-id>` | 显示特定执行详情 | `/logs exec-003` |
| `/logs files` | 显示文件操作统计 | `/logs files` |
| `/logs deps <file>` | 查看文件依赖图 | `/logs deps beat-analyzer.md` |
| `/logs timeline` | 显示执行时间线 | `/logs timeline` |
| `/logs modules` | 显示模块使用统计 | `/logs modules` |
| `/logs debug` | 显示调试信息 | `/logs debug` |
| `/logs search <keyword>` | 搜索日志记录 | `/logs search 节拍拆解` |

## 执行流程

1. **解析命令参数**
   - 提取子命令和参数
   - 确定查询类型

2. **读取日志文件**
   - 路径：`.claude/.execution-log.json`
   - 解析 JSON 结构

3. **格式化输出**
   - 根据子命令选择输出格式
   - 生成格式化报告

## 日志文件结构

```json
{
  "version": "1.0",
  "created_at": "2025-02-04T14:30:00Z",
  "executions": {
    "exec-001": {
      "timestamp": "2025-02-04T14:30:22.000Z",
      "command": "/breakdown ep01",
      "duration_ms": 15200,
      "status": "success",
      "steps": [
        {
          "name": "步骤1: 读取剧本",
          "duration_ms": 580,
          "files_read": ["script/猪打镇关西_v2.0.md"],
          "modules_used": ["character-loader.py"],
          "output": "character_settings"
        }
      ]
    }
  },
  "last_execution_id": "exec-001",
  "statistics": {
    "total_executions": 1,
    "successful_executions": 1,
    "failed_executions": 0
  }
}
```

## 输出格式

### 执行摘要
```
📊 最近执行摘要

exec-003 [/breakdown ep01] - 15.2s - ✅ 成功
exec-002 [/beatboard ep01] - 23.5s - ✅ 成功
exec-001 [/sequence ep01] - 18.7s - ✅ 成功
```

### 执行详情
```
📋 执行详情 (exec-003: /breakdown ep01)

执行时间: 2025-02-04 14:30:22
总耗时: 15.2s
状态: ✅ 成功

步骤详情:
[步骤1] 读取剧本 + 提取角色设定 (580ms)
  📖 读取: script/猪打镇关西_v2.0.md (行1-245)
  🧩 模块: character-loader.py
  📝 输出: character_settings

[步骤2] 执行节拍拆解 (3200ms) ⚠️ 最耗时
  📖 读取: .claude/common/beat-analyzer.md (行1-1152)
  🔬 算法: beat_analysis, drama_weight_v4.1
```

### 时间线
```
⏱️ 执行时间线 (exec-003)

[14:30:22.000] 开始执行 /breakdown ep01
[14:30:22.581] ✓ 步骤1: 读取剧本 (580ms)
[14:30:25.781] ✓ 步骤2: 节拍拆解 (3200ms) ← 最耗时
[14:30:31.181] ✓ 完成 (15200ms)
```

### 文件统计
```
📁 文件操作统计

最常读取:
1. beat-analyzer.md (8次)
2. coherence-checker.md (5次)
3. quality-check.md (4次)

最近写入:
1. outputs/beat-breakdown-ep01.md
2. outputs/scene-breakdown-ep01.json
```

### 调试信息
```
🐛 调试信息

最近的错误:
exec-002 - 步骤4: 执行连贯性检查
  ⚠️ 警告: 角色一致性检查失败
  📖 读取的文件: coherence-checker.md (行1-full)
  🔬 使用的算法: continuity_check_v4.0
```

## 错误处理

| 错误类型 | 处理方式 |
|---------|---------|
| 日志文件不存在 | 显示空状态提示 |
| exec-id 不存在 | 显示 "未找到执行记录" |
| 无执行记录 | 显示 "暂无执行记录" |
| 参数无效 | 显示命令使用帮助 |
