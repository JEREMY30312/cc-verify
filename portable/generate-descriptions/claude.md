> **Description:** 自动检测并处理文件描述任务，为项目地图生成智能描述

# 生成文件描述

## 命令列表

| 命令 | 功能 | 示例 |
|------|------|------|
| `/generate-descriptions` | 自动处理文件描述任务 | `/generate-descriptions` |

## 执行流程

### 1. 检测任务文件

**路径**：`.llm-tasks.json`

**触发条件**：
- 文件存在
- 包含待处理的任务列表

### 2. 读取任务清单

**文件格式**：
```json
{
  "version": "2.2",
  "generated_at": "2026-04-09 12:00:00",
  "task_count": 10,
  "tasks": [
    {
      "type": "generate_description",
      "file": "AGENTS.md",
      "content_preview": "# ANINEO 制片人 Agent 配置...",
      "max_length": 20
    }
  ]
}
```

### 3. 生成描述

**规则**：
- 描述长度：≤20字
- 基于文件内容和文件名智能生成
- 只处理 `.md` 文件

### 4. 输出结果

**路径**：`.file-descriptions.json`

**格式**：
```json
{
  "AGENTS.md": {
    "description": "ANINEO制片人Agent配置",
    "mtime": 1234567890.0,
    "generated_at": "2026-04-09 12:00:00"
  }
}
```

### 5. 清理任务文件

处理完成后删除 `.llm-tasks.json`

## 使用方式

```bash
# 自动触发（无需手动执行）
# 当 .llm-tasks.json 存在时，Claude Code 会自动执行此命令
```

## 示例

### 输入任务

```json
{
  "tasks": [
    {
      "type": "generate_description",
      "file": "AGENTS.md",
      "content_preview": "# ANINEO 制片人 Agent 配置（V4.0）...",
      "max_length": 20
    },
    {
      "type": "generate_description",
      "file": "README.md",
      "content_preview": "# 项目地图生成器 - 可移植版...",
      "max_length": 20
    }
  ]
}
```

### 输出描述

```json
{
  "AGENTS.md": {
    "description": "ANINEO制片人Agent配置",
    "mtime": 1234567890.0,
    "generated_at": "2026-04-09 12:00:00"
  },
  "README.md": {
    "description": "项目地图生成器说明",
    "mtime": 1234567890.0,
    "generated_at": "2026-04-09 12:00:00"
  }
}
```

## 注意事项

- 描述长度限制：20字（可在配置中修改）
- 只处理 `.md` 文件
- 自动缓存，避免重复生成
- 处理完成后自动清理任务文件
