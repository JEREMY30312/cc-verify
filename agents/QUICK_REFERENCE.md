# ANINEO Agent 快速调用指南

## 🔧 问题回顾

### 原始问题

```
Error: Unknown agent type: storyboard-artist is not a valid agent type
```

OpenCode 平台的 `task` 工具只支持**内置 Agent 类型**，不支持直接调用自定义 Agent。

### 原因

| 平台机制 | 说明 |
|----------|------|
| 内置 Agent | `explore`, `librarian`, `oracle`, `general` 等 |
| 自定义 Agent | `storyboard-artist`, `director`, `animator` (AGENTS.md 定义) |
| 调用差异 | 内置 Agent 可直接调用，自定义 Agent 需要通过 `general` 间接调用 |

---

## ✅ 解决方案

### 方案1：使用快捷命令（推荐）

```bash
# 生成节拍拆解
./agents/storyboard-artist breakdown -s script/"猪"打镇关西_v2.0"

# 审核节拍拆解表
./agents/director review -f outputs/beat-breakdown-ep01.md

# 生成九宫格提示词
./agents/storyboard-artist beatboard

# 生成动态提示词
./agents/animator motion
```

### 方案2：在 OpenCode 中使用 general agent

```javascript
// 构建 prompt
const prompt = `
// 从 caller.js 生成的完整 prompt
[角色设定]
你是 storyboard-artist...
...

[任务]
生成节拍拆解表
...

[项目配置]
- 视觉风格：国潮动漫风格
...
`;

// 调用 general agent
task(
    subagent_type="general",
    prompt=prompt
);
```

### 方案3：使用 slash command

```bash
# OpenCode 内置的 slash command
/breakdown      # 节拍拆解
/beatboard      # 九宫格提示词
/sequence       # 四宫格提示词
/motion         # 动态提示词
```

---

## 📋 未来调用规范

### 应该怎么做

| ✅ 正确方式 | ❌ 错误方式 |
|-------------|-------------|
| `task(subagent_type="general", prompt=完整prompt)` | `task(subagent_type="storyboard-artist")` |
| `./agents/storyboard-artist breakdown` | (无脚本时的直接调用) |
| `/breakdown` slash command | (假设可以调用自定义 agent) |

### Agent 调用流程图

```
用户请求
    │
    ▼
┌─────────────────┐
│ 检查 Agent 类型 │
└─────────────────┘
    │
    ├─→ 内置 Agent (explore/librarian/oracle)
    │       │
    │       ▼
    │   直接调用
    │   task(..., subagent_type="explore")
    │
    └─→ 自定义 Agent (storyboard-artist/director/animator)
            │
            ▼
        方案A: 使用 caller.js
        node agents/caller.js storyboard-artist --task breakdown
            │
            ▼
        方案B: 使用快捷脚本
        ./agents/storyboard-artist breakdown
            │
            ▼
        方案C: 使用 general agent + 构建的 prompt
        task(subagent_type="general", prompt=完整prompt)
```

---

## 🎯 快速参考

### 命令速查表

| 任务 | 快捷命令 | Slash Command | Agent 类型 |
|------|----------|---------------|------------|
| 节拍拆解 | `./agents/storyboard-artist breakdown` | `/breakdown` | storyboard-artist |
| 九宫格提示词 | `./agents/storyboard-artist beatboard` | `/beatboard` | storyboard-artist |
| 四宫格提示词 | `./agents/storyboard-artist sequence` | `/sequence` | storyboard-artist |
| 动态提示词 | `./agents/animator motion` | `/motion` | animator |
| 审核 | `./agents/director review -f <文件>` | - | director |

### 参数速查

| 参数 | 说明 | 示例 |
|------|------|------|
| `-s, --script` | 剧本文件 | `-s script/剧本.md` |
| `-f, --file` | 待审核文件 | `-f outputs/xxx.md` |
| `-o, --output` | 输出文件 | `-o outputs/xxx.md` |
| `-t, --task` | 任务类型 | `-t breakdown` |
| `-v, --verbose` | 详细输出 | `-v` |
| `-h, --help` | 帮助 | `-h` |

---

## 📁 文件清单

```
agents/
├── caller.js              # ✅ 核心调用器
├── storyboard-artist      # ✅ 分镜师快捷脚本
├── director               # ✅ 导演快捷脚本
├── animator               # ✅ 动画师快捷脚本
└── README.md              # ✅ 使用文档

.claude/
├── AGENTS.md              # 主配置
├── agents/
│   ├── storyboard-artist.md    # Agent 定义
│   ├── director.md             # Agent 定义
│   └── animator.md             # Agent 定义
└── skills/
    ├── film-storyboard-skill/
    ├── storyboard-review-skill/
    └── animator-skill/
```

---

## 🔑 关键要点

1. **OpenCode 限制**: `task` 工具只支持内置 Agent 类型
2. **解决方案**: 使用 `general` agent + 自动构建的 prompt
3. **推荐方式**: 使用快捷脚本（`./agents/xxx`）
4. **备选方式**: 使用 slash command（`/breakdown`）
5. **禁止方式**: 直接调用不存在的 Agent 类型

---

## ❓ 常见问题

**Q: 为什么不能像 `explore` 一样直接调用 `storyboard-artist`？**

A: 因为 `storyboard-artist` 不是 OpenCode 平台的内置 Agent，需要通过 `general` agent 间接调用。

**Q: 如何确认一个 Agent 是否可以直接调用？**

A: 检查 OpenCode 文档中 `task` 工具支持的 `subagent_type` 参数。

**Q: 快捷脚本和 slash command 哪个更好？**

A: 快捷脚本更灵活，支持更多参数；slash command 更简洁，适合固定流程。

**Q: 我可以添加新的自定义 Agent 吗？**

A: 可以。按照 `agents/*.md` 的格式创建配置文件，然后创建对应的快捷脚本即可。
