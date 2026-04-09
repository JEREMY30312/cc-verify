# ANINEO 智能文件自动整理器 (V1.0)

> **聪明且轻量**的自动化文件管理解决方案

---

## 🎯 核心特性

### ✨ 自动化
- **实时监控**：新文件创建时立即自动整理
- **零手动操作**：无需手动分类，智能判断文件位置
- **预防性管理**：从源头防止文件混乱，而不是事后补救

### 🧠 智能分类

支持多种智能分类规则：

| 文件类型 | 自动分类到 | 示例 |
|---------|-----------|------|
| Phase C 相关 | `07-PhaseC部署插件/` | `phase_C_*.py`, `deploy_phase_c.sh` |
| 部署相关 | `05-临时文件归档/部署记录/` | `deploy_*.md`, `deployment_*.json` |
| 分析/报告 | `01-版本历史/项目报告/` | `*_report.md`, `*_summary.md` |
| 测试文件 | `02-测试验证/` | `test_*.py`, `*_verification.json` |
| 备份/回滚 | `05-临时文件归档/备份文件/` | `backup_*.py`, `rollback_*.sh` |
| Python 脚本 | `临时池/暂存脚本/` | `*.py` |
| Shell 脚本 | `临时池/暂存脚本/` | `*.sh` |
| Markdown 文档 | `临时池/暂存文档/` | `*.md` |
| JSON 数据 | `临时池/暂存数据/` | `*.json` |
| 日志文件 | `临时池/暂存文档/` | `*.log` |
| 其他未知 | `临时池/不确定文件/` | 其他 |

### 🎨 轻量级
- **一键启动**：`./start_organizer.sh`
- **零配置**：开箱即用，无需复杂配置
- **低资源占用**：轻量级监控，不影响开发效率

---

## 🚀 快速开始

### 1. 安装依赖（首次使用）

```bash
pip3 install watchdog
```

### 2. 启动整理器

**方式A：实时监控模式（推荐）**

```bash
./start_organizer.sh
```

- 持续监控根目录
- 新文件创建时自动整理
- 按 Ctrl+C 停止监控

**方式B：单次扫描模式**

```bash
./start_organizer.sh --once
```

- 扫描当前根目录的所有文件
- 自动整理一次后退出
- 不持续监控

**方式C：试运行模式（测试用）**

```bash
./start_organizer.sh --dry-run
```

或

```bash
python3 smart_file_organizer.py --dry-run
```

- 不实际移动文件
- 仅显示将会执行的操作
- 用于测试规则是否正确

---

## 📖 工作原理

### 1. 文件监控流程

```
新文件创建
    ↓
等待文件写入完成（避免移动未完成的文件）
    ↓
智能分类分析
    ├─ 是核心系统文件？ → 保留在根目录
    ├─ 是 Phase C 相关？ → 移动到 07-PhaseC部署插件/
    ├─ 是部署相关？ → 移动到 05-临时文件归档/部署记录/
    ├─ 是分析报告？ → 移动到 01-版本历史/项目报告/
    ├─ 是测试文件？ → 移动到 02-测试验证/
    ├─ 是备份文件？ → 移动到 05-临时文件归档/备份文件/
    ├─ 是 .py/.sh/.js？ → 移动到 临时池/暂存脚本/
    ├─ 是 .md？ → 移动到 临时池/暂存文档/
    ├─ 是 .json？ → 移动到 临时池/暂存数据/
    └─ 其他？ → 移动到 临时池/不确定文件/
    ↓
创建目标目录（如果不存在）
    ↓
处理文件名冲突（自动添加序号）
    ↓
移动文件
    ↓
输出日志
```

### 2. 核心系统文件（不移动）

以下文件会**保留在根目录**：

- `AGENTS.md` - 主配置文件
- `.agent-state.json` - 状态文件
- `.agent-state-template.json` - 状态模板
- `check_root.sh` - 检查脚本
- `smart_file_organizer.py` - 整理器脚本
- `.DS_Store` - macOS 系统文件

### 3. 自动创建目录结构

首次运行时，会自动创建以下目录：

```
版本汇总/
├── 临时池/
│   ├── 暂存脚本/
│   ├── 暂存文档/
│   ├── 暂存数据/
│   └── 不确定文件/
├── 01-版本历史/
│   └── 项目报告/
├── 02-测试验证/
│   ├── 测试脚本/
│   └── 测试数据/
├── 05-临时文件归档/
│   ├── 部署记录/
│   └── 备份文件/
└── 07-PhaseC部署插件/
    ├── 核心功能/
    ├── 脚本工具/
    ├── 文档/
    └── 配置文件/
```

---

## 🎯 使用场景

### 场景1：日常开发

**问题**：开发新功能时，创建了大量临时测试文件，根目录越来越乱。

**解决**：
```bash
# 终端1：启动整理器（持续运行）
./start_organizer.sh

# 终端2：正常开发
# 新创建的文件会自动被整理，你无需关心文件放哪里
```

### 场景2：首次整理现有文件

**问题**：根目录已经有很多文件，需要一次性整理。

**解决**：
```bash
# 先试运行，查看将会执行的操作
python3 smart_file_organizer.py --dry-run

# 确认无误后，执行实际整理
python3 smart_file_organizer.py --once
```

### 场景3：测试分类规则

**问题**：不确定某个文件会被分类到哪里。

**解决**：
```bash
# 创建一个测试文件
echo "test" > test_file.txt

# 观察整理器的输出
# 会显示：✓ test_file.txt -> 临时池/不确定文件/

# 查看实际移动的文件
ls 版本汇总/临时池/不确定文件/
```

---

## 🔧 自定义规则

你可以修改 `smart_file_organizer.py` 中的配置来自定义规则：

### 1. 修改允许保留的文件

```python
ALLOWED_ROOT_FILES = {
    "AGENTS.md",
    ".agent-state.json",
    # 添加你的文件...
}
```

### 2. 添加新的分类规则

在 `FileClassifier.classify()` 方法中添加新规则：

```python
@staticmethod
def classify(filepath: Path) -> dict:
    # ... 现有规则 ...

    # 添加你的规则
    if "myproject" in stem:
        return {
            "target_dir": ROOT_DIR / "版本汇总" / "08-MyProject插件",
            "reason": "MyProject相关文件",
            "subdir": "核心功能"
        }

    # ... 后续规则 ...
```

---

## ⚙️ 高级用法

### 1. 作为系统服务（macOS）

创建一个 Launch Agent，让整理器开机自启：

```bash
# 创建配置文件
cat > ~/Library/LaunchAgents/com.anineo.organizer.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.anineo.organizer</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/achi/Desktop/JEREMY/NEW/smart_file_organizer.py</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/Users/achi/Desktop/JEREMY/NEW</string>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
EOF

# 加载服务
launchctl load ~/Library/LaunchAgents/com.anineo.organizer.plist
```

### 2. 定时整理（Cron）

如果你不想持续监控，可以定时执行单次扫描：

```bash
# 编辑 crontab
crontab -e

# 添加以下行（每小时执行一次）
0 * * * * cd /Users/achi/Desktop/JEREMY/NEW && python3 smart_file_organizer.py --once
```

---

## 📊 与三原则法的关系

### 三原则回顾

| 原则 | 内容 |
|------|------|
| 原则1 | 根目录仅保留AGENTS.md |
| 原则2 | 新文件必问属于01-06哪个分类？ |
| 原则3 | 新增插件参照03/04现有结构 |

### 智能整理器如何实现三原则

| 原则 | 实现方式 |
|------|----------|
| 原则1 | 自动识别核心系统文件，保留在根目录；其他文件自动移动 |
| 原则2 | 智能分类文件，自动放入01-06对应分类或临时池 |
| 原则3 | 自动为 Phase C 等新功能创建插件目录，参照现有插件结构 |

**关键优势**：
- ✅ 无需手动记住三原则
- ✅ 自动执行，无需用户干预
- ✅ 预防性管理，从源头防止混乱
- ✅ 轻量级，不增加开发负担

---

## 🐛 故障排查

### 问题1：watchdog 库未安装

**错误信息**：
```
警告: watchdog 库未安装
请运行: pip install watchdog
```

**解决**：
```bash
pip3 install watchdog
```

或使用单次扫描模式（不需要 watchdog）：
```bash
python3 smart_file_organizer.py --once
```

### 问题2：权限错误

**错误信息**：
```
PermissionError: [Errno 13] Permission denied
```

**解决**：
```bash
# 确保脚本有执行权限
chmod +x smart_file_organizer.py
chmod +x start_organizer.sh
```

### 问题3：文件未移动

可能原因：
1. 文件名以 `.` 开头（隐藏文件，不处理）
2. 文件在 `ALLOWED_ROOT_FILES` 中（核心系统文件）
3. 文件不在根目录（只监控根目录）

**调试方法**：
```bash
# 使用试运行模式查看详情
python3 smart_file_organizer.py --dry-run --once
```

---

## 📝 更新日志

### V1.0 (2026-01-31)

**初始版本**：
- ✅ 实时监控新文件创建
- ✅ 智能分类，支持多种文件类型
- ✅ 自动创建目录结构
- ✅ 单次扫描模式和试运行模式
- ✅ 文件名冲突处理
- ✅ Phase C 专用插件目录支持

---

## 📞 反馈与建议

如有问题或建议，请联系 ANINEO 团队。

---

**记住**：
- 根目录只放核心文件，其他全进版本汇总
- 不确定放哪里，就先放临时池
- 新插件参照03/04，必须有README

**智能整理器**会帮你自动执行！✨
