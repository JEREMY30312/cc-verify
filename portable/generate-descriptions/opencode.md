---
description: 自动检测并处理文件描述任务，为项目地图生成智能描述
---

# 生成文件描述

**目的**：自动检测 `.llm-tasks.json`，为每个文件生成简短描述，输出到 `.file-descriptions.json`

**触发条件**：
- 检测到 `.llm-tasks.json` 文件存在
- 文件内容包含待处理的任务列表

**使用方式**：
```bash
# 自动触发（无需手动执行）
# 当 .llm-tasks.json 存在时，OpenCode 会自动执行此命令
```

**工作流程**：

1. **读取任务清单**
   - 路径：`.llm-tasks.json`
   - 解析任务列表（包含文件路径、内容预览、最大长度）

2. **生成描述**
   - 为每个文件生成简短描述（≤20字）
   - 基于文件内容和文件名智能生成

3. **输出结果**
   - 路径：`.file-descriptions.json`
   - 格式：
     ```json
     {
       "文件路径.md": {
         "description": "简短描述",
         "mtime": 1234567890.0,
         "generated_at": "2026-04-09 12:00:00"
       }
     }
     ```

4. **清理任务文件**
   - 处理完成后删除 `.llm-tasks.json`

**示例**：

输入任务：
```json
{
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

输出描述：
```json
{
  "AGENTS.md": {
    "description": "ANINEO制片人Agent配置",
    "mtime": 1234567890.0,
    "generated_at": "2026-04-09 12:00:00"
  }
}
```

**注意事项**：
- 描述长度限制：20字（可在配置中修改）
- 只处理 `.md` 文件
- 自动缓存，避免重复生成
