# 项目地图生成器 - 可移植版

> **Description:** 单文件项目地图生成器，支持Git集成、学习机制、YAML描述提取

## 快速开始

### 方法1：一键安装（推荐）

```bash
curl -fsSL https://raw.githubusercontent.com/JEREMY30312/cc-verify/main/portable/install.sh | bash
```

### 方法2：手动安装

将 `standalone.py` 复制到你的项目根目录：

```bash
# 方法1：从本目录复制
cp standalone.py /path/to/your/project/

# 方法2：直接下载
curl -o generate_map.py https://raw.githubusercontent.com/JEREMY30312/cc-verify/main/portable/standalone.py
```

### 2. 运行

```bash
cd /path/to/your/project
python3 standalone.py
```

运行后会自动生成：
- `PROJECT_MAP.md` - 项目地图文件
- `PROJECT_FINGERPRINT.json` - 项目指纹（AI学习用）

### 3. 安装Git钩子（可选）

```bash
python3 standalone.py --install-hooks
```

安装后，每次 Git 操作会自动更新项目地图。

---

## 配置说明

### 配置文件

在项目根目录创建 `.project-map-config.json` 文件：

```json
{
  "time_range_hours": 168,
  "max_description_length": 20,
  "ignore_list": [".git", "node_modules", "__pycache__"],
  "collapse_folders": ["backups", "版本汇总"],
  "hooks": {
    "post_commit_update": true,
    "post_merge_update": true,
    "post_checkout_update": true,
    "auto_add_to_git": true
  },
  "output": {
    "map_file": "PROJECT_MAP.md",
    "fingerprint_file": "PROJECT_FINGERPRINT.json"
  }
}
```

### 配置项说明

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `time_range_hours` | 数字 | 168 | 显示最近多少小时的变化（168=7天） |
| `max_description_length` | 数字 | 20 | 文件描述最多多少字 |
| `max_tree_depth` | 数字 | 3 | 目录树最大显示深度 |
| `shallow_folders` | 数组 | 见示例 | 浅层显示文件夹（只显示第一层） |
| `ignore_list` | 数组 | 见上表 | 扫描时忽略的文件夹列表 |
| `collapse_folders` | 数组 | 见上表 | 在目录树中折叠显示的文件夹 |
| `hooks.post_commit_update` | 布尔 | true | git commit 后是否自动更新 |
| `hooks.post_merge_update` | 布尔 | true | git merge/pull 后是否自动更新 |
| `hooks.post_checkout_update` | 布尔 | true | git checkout 切换分支后是否自动更新 |
| `hooks.auto_add_to_git` | 布尔 | true | 更新后是否自动 git add 地图文件 |
| `output.map_file` | 字符串 | "PROJECT_MAP.md" | 项目地图文件名 |
| `output.fingerprint_file` | 字符串 | "PROJECT_FINGERPRINT.json" | 项目指纹文件名 |

**注意**：如果不创建配置文件，程序会使用内置默认配置运行。

---

## 钩子说明

### 钩子类型

| 钩子 | 触发时机 | 目的 |
|------|---------|------|
| post-commit | 每次 `git commit` 后 | 保持地图实时性 |
| post-merge | 每次 `git merge` 或 `git pull` 后 | 合并后同步地图 |
| post-checkout | 每次 `git checkout` 后 | 切换分支后同步地图 |

### 钩子工作原理

1. 钩子触发后，读取配置文件 `.project-map-config.json`
2. 检查对应钩子开关是否开启
3. 运行 `generate_map.py` 更新地图
4. 如果 `auto_add_to_git` 为 true，自动 `git add` 地图文件

### 手动安装钩子

```bash
cd hooks
bash install.sh
```

### 手动卸载钩子

```bash
rm .git/hooks/post-commit
rm .git/hooks/post-merge
rm .git/hooks/post-checkout
```

---

## 文件描述格式

程序会自动提取以下两种格式的文件描述：

### YAML front matter（推荐）

```markdown
---
description: "项目地图生成器主程序"
---

# 文件内容...
```

### Markdown 引用块（兼容旧格式）

```markdown
> **Description:** 项目地图生成器主程序

# 文件内容...
```

**注意**：描述最多20字（可在配置中修改）。

---

## 输出文件

### PROJECT_MAP.md

项目地图文件，包含：
- 最近7天的变更记录
- 完整目录树结构
- 文件描述信息

### PROJECT_FINGERPRINT.json

项目指纹文件，包含：
- 项目领域分析
- 架构模式检测
- 关键特征识别
- AI优化索引

---

## 故障排除

查看 [TROUBLESHOOTING.md](TROUBLESHOOTING.md) 获取详细故障排除指南。

### 常见问题速查

| 问题 | 解决 |
|------|------|
| 运行后没有生成文件 | 检查Python版本 >= 3.6 |
| 钩子不工作 | 检查钩子是否可执行：`ls -la .git/hooks/` |
| 描述提取不正确 | 检查文件格式是否正确 |

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 2.1 | 2026-04-03 | 智能层级控制、关键文件类型识别、curl一键安装 |
| 2.0 | 2025-02-04 | 支持Git集成、学习机制、YAML描述 |
| 1.0 | 2025-01-20 | 初始版本，基本地图生成 |

## V2.1 新功能

### 智能层级控制

自动识别非功能性文件夹（备份/缓存/日志/测试等），只显示第一层，避免目录树过深。

```json
{
  "max_tree_depth": 3,
  "shallow_folders": ["backups", "版本汇总", "logs", "tests", "dist"]
}
```

### 关键文件类型识别

基于类型而非具体文件名识别关键文件，适配任何项目类型：
- 入口文档：README, CLAUDE, AGENTS, HANDOFF
- 核心配置：package.json, tsconfig, config, .env
- 产品规格：Product-Spec, spec, 规格
- 工作流：workflow, 流程, pipeline, persona, skill
- 设计/计划：design, plan, 设计, 计划
- 验证/审计：audit, verify, 验收, test_report

### 描述显示优化

- 前两层：显示所有.md文件描述
- 深层：只显示关键文件描述
- 减少50%注释噪音

### curl一键安装

```bash
curl -fsSL https://raw.githubusercontent.com/JEREMY30312/cc-verify/main/portable/install.sh | bash
```

自动完成：下载程序 → 创建配置 → 首次运行 → 安装钩子

---

## 许可证

MIT License
