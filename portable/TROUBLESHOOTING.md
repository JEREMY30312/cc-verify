# 故障排除指南

## 常见问题

### Q1: 运行后没有生成 PROJECT_MAP.md

**症状**：运行 `python3 generate_map.py` 后，没有生成输出文件。

**排查步骤**：

1. **检查Python版本**
   ```bash
   python3 --version
   ```
   需要 Python 3.6 或更高版本。

2. **检查写入权限**
   ```bash
   ls -la .
   ```
   确保当前目录有写入权限。

3. **查看详细错误**
   ```bash
   python3 generate_map.py 2>&1 | tail -20
   ```

4. **检查文件数量**
   ```bash
   ls -la *.py *.md *.json 2>/dev/null | wc -l
   ```
   如果项目为空，可能没有文件可扫描。

---

### Q2: 钩子不工作

**症状**：Git 操作后，项目地图没有自动更新。

**排查步骤**：

1. **检查钩子是否安装**
   ```bash
   ls -la .git/hooks/post-*
   ```
   应该看到 `post-commit`、`post-merge`、`post-checkout` 三个文件。

2. **检查钩子是否可执行**
   ```bash
   ls -l .git/hooks/post-commit
   ```
   输出应包含 `x` 权限，如 `-rwxr-xr-x`。

3. **检查配置文件**
   ```bash
   cat .project-map-config.json
   ```
   确保 `hooks` 部分的开关为 `true`。

4. **手动测试钩子**
   ```bash
   bash .git/hooks/post-commit
   ```
   应该看到 "🗺️ 提交后更新项目地图..." 等输出。

5. **检查Git仓库状态**
   ```bash
   git status
   ```
   确保当前目录是Git仓库。

---

### Q3: 描述提取不正确

**症状**：文件描述为空或内容错误。

**排查步骤**：

1. **检查文件格式**
   - 只有 `.md` 文件会提取描述
   - 其他文件类型描述为空

2. **检查YAML格式**
   ```markdown
   ---
   description: "正确的描述格式"
   ---
   ```
   - 必须以 `---` 开头
   - `description:` 后面要有内容
   - 内容不超过20字

3. **检查Markdown格式**
   ```markdown
   > **Description:** 正确的描述格式
   ```
   - 必须在文件前3行
   - 格式必须完全匹配

4. **测试描述提取**
   ```python
   python3 -c "
   from generate_map import get_file_description
   desc, is_new = get_file_description('your_file.md')
   print(f'描述: {desc}')
   print(f'新格式: {is_new}')
   "
   ```

---

### Q4: Git状态显示异常

**症状**：变更记录为空或显示错误。

**排查步骤**：

1. **检查是否为Git仓库**
   ```bash
   git rev-parse --git-dir
   ```
   应该输出 `.git`。

2. **检查Git状态**
   ```bash
   git status --porcelain
   ```
   应该有输出变更记录。

3. **检查时间范围**
   ```bash
   # 查看配置文件中的时间范围
   python3 -c "import json; print(json.load(open('.project-map-config.json'))['time_range_hours'])"
   ```
   默认168小时（7天）。

---

### Q5: 项目指纹生成失败

**症状**：`PROJECT_FINGERPRINT.json` 未生成或内容错误。

**排查步骤**：

1. **检查JSON格式**
   ```bash
   python3 -m json.tool PROJECT_FINGERPRINT.json
   ```
   如果格式错误，会显示具体错误位置。

2. **检查文件内容**
   ```bash
   cat PROJECT_FINGERPRINT.json | python3 -m json.tool | head -30
   ```

3. **重新生成**
   ```bash
   rm PROJECT_FINGERPRINT.json
   python3 generate_map.py
   ```

---

### Q6: 钩子执行超时

**症状**：钩子执行时显示 "更新超时（60秒）"。

**排查步骤**：

1. **检查项目大小**
   ```bash
   find . -type f | wc -l
   ```
   如果文件数量过多（>10000），扫描会较慢。

2. **手动运行测试**
   ```bash
   time python3 generate_map.py
   ```
   查看实际耗时。

3. **优化配置**
   - 增加 `ignore_list` 忽略更多文件夹
   - 减少 `time_range_hours` 时间范围

---

### Q7: 配置文件格式错误

**症状**：显示 "配置文件格式错误，使用默认配置"。

**排查步骤**：

1. **验证JSON格式**
   ```bash
   python3 -m json.tool .project-map-config.json
   ```

2. **检查注释**
   - JSON不支持 `//` 注释
   - 如果使用了示例文件的注释，需要删除

3. **使用示例文件**
   ```bash
   cp .project-map-config.example.json .project-map-config.json
   ```
   然后删除所有 `//` 开头的注释行。

---

### Q8: standalone.py 与 generate_map.py 的区别

**问题**：两个文件有什么不同？

**回答**：

| 特性 | generate_map.py | standalone.py |
|------|----------------|---------------|
| 依赖 | 需要配置文件 | 内置默认配置 |
| 使用场景 | 当前项目 | 可移植到其他项目 |
| 配置 | 读取外部配置文件 | 优先用内置配置 |
| 钩子 | 需要手动安装 | 支持 `--install-hooks` |

**建议**：
- 当前项目使用 `generate_map.py`
- 分享给他人使用 `standalone.py`

---

## 高级排查

### 启用调试模式

```bash
python3 generate_map.py --debug
```

### 查看完整错误堆栈

```bash
python3 -c "
import traceback
try:
    import generate_map
    generate_map.main()
except Exception as e:
    traceback.print_exc()
"
```

### 检查依赖模块

```bash
python3 -c "
import sys
print(f'Python版本: {sys.version}')
print(f'当前路径: {sys.path}')
"
```

---

## 获取帮助

如果以上方法都无法解决问题：

1. 检查项目是否有特殊结构
2. 查看是否有权限问题
3. 尝试在全新项目测试脚本
4. 联系开发者提供以下信息：
   - Python版本
   - 操作系统
   - 错误输出
   - 项目结构（`tree -L 2`）
