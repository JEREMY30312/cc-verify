# ANINEO 自定义 Agent 快速调用工具

## 问题背景

OpenCode 平台的 `task` 工具只支持内置的 Agent 类型（如 `explore`、`librarian`、`general` 等），不支持直接调用自定义的 Agent（如 `storyboard-artist`、`director`、`animator`）。

**报错示例**：
```
Error: Unknown agent type: storyboard-artist is not a valid agent type
```

## 解决方案

创建了一套快速调用工具，通过以下方式实现自定义 Agent 的便捷调用：

1. **caller.js** - 通用 Agent 调用器
2. **快捷脚本** - 一键调用特定 Agent
3. **集成方案** - 在 OpenCode 中无缝使用

## 文件结构

```
agents/
├── caller.js              # 通用调用器（核心）
├── storyboard-artist      # 分镜师快捷脚本
├── director               # 导演快捷脚本
├── animator               # 动画师快捷脚本
└── README.md              # 本文档
```

## 使用方式

### 方式1：使用快捷脚本（推荐）

```bash
# 生成节拍拆解
./agents/storyboard-artist breakdown --script script/"猪"打镇关西_v2.0"

# 审核节拍拆解表
./agents/director review --file outputs/beat-breakdown-ep01.md

# 生成九宫格提示词
./agents/storyboard-artist beatboard --output beat-board-prompt.md

# 生成动态提示词
./agents/animator motion --output motion-prompt.md
```

### 方式2：使用 caller.js 直接调用

```bash
# 调用 storyboard-artist
node agents/caller.js storyboard-artist \
    --task breakdown \
    --script script/"猪"打镇关西_v2.0" \
    --verbose

# 调用 director
node agents/caller.js director \
    --task review \
    --file outputs/beat-breakdown-ep01.md

# 调用 animator
node agents/caller.js animator \
    --task motion \
    --output motion-prompt.md
```

### 方式3：在 OpenCode 中使用

在 OpenCode 中，使用 `general` agent + 构建好的 prompt：

```javascript
// 步骤1：加载 Agent 配置
const agentConfig = loadAgentConfig('storyboard-artist');

// 步骤2：构建完整 prompt
const prompt = buildPrompt(agentConfig, 'breakdown', {
    contextFiles: ['outputs/beat-breakdown-ep01.md'],
    projectConfig: {...},
    userPreferences: {...},
    taskSpecificData: scriptContent
});

// 步骤3：使用 task 工具调用
task(
    subagent_type="general",
    prompt=prompt
);
```

## 工具功能

### caller.js 功能

| 功能 | 说明 |
|------|------|
| 读取 Agent 配置 | 自动解析 agent/*.md 文件 |
| 构建完整 Prompt | 整合角色设定、任务、数据 |
| 加载 Context | 读取前置产物文件 |
| 保存输出 | 支持输出到文件 |

### 支持的参数

| 参数 | 简写 | 说明 |
|------|------|------|
| --task | -t | 任务类型 |
| --script | -s | 剧本文件路径 |
| --file | -f | 待审核文件路径 |
| --output | -o | 输出文件路径 |
| --verbose | -v | 详细输出 |
| --help | -h | 显示帮助 |

## Agent 配置格式

自定义 Agent 需要按照以下格式编写配置文件（`agents/*.md`）：

```markdown
---
name: agent-name           # Agent 名称
description: 描述          # Agent 功能描述
skills: skill-name         # 使用的技能包
model: opus                # 使用的模型
color: red                 # 标识颜色
---

[角色]
你是专业的...

[任务]
- 任务1
- 任务2

[输出规范]
- 规范1
- 规范2

[协作模式]
协作流程说明...
```

## 集成到工作流

### 在 AGENTS.md 中使用

可以在 AGENTS.md 的工作流程中集成这些工具：

```markdown
第三步：调用 storyboard-artist 生成并写入
    1. 检查 .agent-state.json 是否有 context_files
    2. 如有：读取 context_files 中的前置产物
    3. 调用 agents/caller.js 构建 prompt：
       node agents/caller.js storyboard-artist \
           --task breakdown \
           --script script/xxx.md \
           --output outputs/beat-breakdown-xxx.md
    4. 使用 task 工具执行生成的 prompt
```

## 常见问题

### Q1: 为什么不能直接调用 storyboard-artist？

OpenCode 平台的 `task` 工具只支持内置 Agent 类型，无法直接识别自定义 Agent。

### Q2: 解决方案是什么？

通过 `general` agent + 自动构建的 prompt 来实现。`caller.js` 负责读取 Agent 配置并构建完整的 prompt。

### Q3: 快捷脚本如何工作？

快捷脚本（`storyboard-artist`、`director` 等）是 bash 封装，简化命令行调用，本质上还是调用 `caller.js`。

### Q4: 如何添加新的自定义 Agent？

1. 在 `agents/` 目录创建 `<agent-name>.md` 配置文件
2. 创建对应的快捷脚本 `<agent-name>`
3. 更新 `caller.js` 的 Agent 列表（如需要）

## 注意事项

1. **Node.js 依赖**: 需要安装 Node.js (v14+)
2. **路径处理**: 脚本使用相对路径，确保在项目根目录运行
3. **文件权限**: 给快捷脚本添加执行权限：`chmod +x agents/*`
4. **OpenCode 环境**: 在 OpenCode 中使用时，需要确保文件路径正确

## 下一步优化

- [ ] 集成到 OpenCode 作为自定义 tool
- [ ] 添加进度显示
- [ ] 支持并行调用多个 Agent
- [ ] 添加错误重试机制
