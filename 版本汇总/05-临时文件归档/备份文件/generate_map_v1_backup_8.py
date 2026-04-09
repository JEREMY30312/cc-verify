import os
import datetime
import re
import time

# ================= 配置区域 =================
TARGET_FILE = 'PROJECT_MAP.md'

# 1. 静态字典 (用于目录或非文本文件)
STATIC_COMMENTS = {
    "AGENTS.md": "🏛️ 主配置文件(System Core)",
    ".agent-state.json": "📊 运行时状态记录",
    "agents": "🎭 子 Agent 配置目录",
    "agents/router.js": "指令路由逻辑",
    ".claude/common": "🔧 核心算法库",
    ".claude/skills": "🎯 SKILL技能库",
    "configs": "⚙️ 配置目录",
    "outputs": "📦 产物目录",
    "script": "📖 用户剧本"
}

# 忽略列表
IGNORE_LIST = {'.git', 'node_modules', '__pycache__', '.DS_Store', 'dist', 'build', '.idea', '.vscode', '.sisyphus'}
# 折叠目录
COLLAPSE_FOLDERS = {'backups', '.strategic-snapshots', '版本汇总'}

# ================= 核心逻辑 =================

def get_recent_changes(dir_path, limit=5, hours=24):
    """获取最近修改的文件列表"""
    recent_files = []
    now = time.time()
    seconds_in_hours = hours * 3600
    for root, dirs, files in os.walk(dir_path):
        dirs[:] = [d for d in dirs if d not in IGNORE_LIST and not (d.startswith('.') and d != '.claude')]
        for file in files:
            if file in IGNORE_LIST: continue
            full_path = os.path.join(root, file)
            try:
                mtime = os.path.getmtime(full_path)
                if now - mtime < seconds_in_hours:
                    rel_path = os.path.relpath(full_path, start='.')
                    recent_files.append((rel_path, mtime))
            except OSError: continue
    recent_files.sort(key=lambda x: x[1], reverse=True)
    return recent_files[:limit]

def extract_description(file_path):
    """
    智能读取文件头部的描述信息 (增强版)
    优先级：Tag > 引用块粗体 > H1标题
    """
    if not file_path.endswith('.md'): return ""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            # 读取前 10 行，去除空白符
            content = [line.strip() for line in f.readlines()[:10]]
            
        # 1. 第一轮扫描：寻找精准的 Description 标签
        for line in content:
            # 模式 A: m1 = re.search(r'', line, re.IGNORECASE)
            if m1: return f"  # {m1.group(1)}"
            
            # 模式 B: > **Description:** ...
            m2 = re.search(r'>\s*\*\*(?:Desc|Description|Role|Purpose):\*\*\s*(.*)', line, re.IGNORECASE)
            if m2: return f"  # {m2.group(1)}"

        # 2. 第二轮扫描 (兜底 A)：寻找引用块中的任意粗体 (适配你的 AGENTS.md 风格)
        for line in content:
            # 匹配 > **任意内容**
            m3 = re.search(r'>\s*\*\*([^*]+)\*\*', line)
            if m3: return f"  # {m3.group(1)}"

        # 3. 第三轮扫描 (兜底 B)：寻找 H1 标题
        for line in content:
            if line.startswith('# '):
                return f"  # {line[2:].strip()}"
            
        return "" 
    except Exception:
        return ""

def get_comment(path, full_real_path):
    # 1. 优先查静态字典 (路径匹配)
    normalized_path = path.replace('\\', '/')
    if normalized_path in STATIC_COMMENTS:
        return f"  # {STATIC_COMMENTS[normalized_path]}"
    
    # 2. 查静态字典 (文件名匹配)
    base = os.path.basename(path)
    if base in STATIC_COMMENTS:
         return f"  # {STATIC_COMMENTS[base]}"
         
    # 3. 动态读取文件内容
    if os.path.isfile(full_real_path):
        dynamic_comment = extract_description(full_real_path)
        if dynamic_comment:
            return dynamic_comment
            
    return ""

def generate_tree(dir_path, prefix='', depth=0):
    if depth > 5: return
    try:
        files = sorted(os.listdir(dir_path))
    except PermissionError: return
    filtered_files = [f for f in files if f not in IGNORE_LIST and not (f.startswith('.') and f not in ['.claude', '.agent-state.json'])]
    pointers = [('├── ', '│   ')] * (len(filtered_files) - 1) + [('└── ', '    ')]
    for pointer, file in zip(pointers, filtered_files):
        full_path = os.path.join(dir_path, file)
        rel_path = os.path.relpath(full_path, start='.')
        comment = get_comment(rel_path, full_path)
        yield f"{prefix}{pointer[0]}{file}{comment}"
        if os.path.isdir(full_path):
            if file in COLLAPSE_FOLDERS: yield f"{prefix}{pointer[1]}└── ..."
            else: yield from generate_tree(full_path, prefix + pointer[1], depth + 1)

def main():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    recent_list = get_recent_changes(".")
    if recent_list:
        recent_section = "\n".join([f"- `{path}` ({datetime.datetime.fromtimestamp(mtime).strftime('%H:%M')})" for path, mtime in recent_list])
    else:
        recent_section = "_暂无最近变动_"

    header = f"""# 🗺️ ANINEO Project Map (Live)

> **Updated:** {timestamp}
> **Mode:** Dynamic Metadata Extraction (V3.1 - Auto Fallback)

## 🔥 最近变动 (24h)
{recent_section}

## 📂 File Directory
"""
    tree_lines = list(generate_tree('.'))
    content = header + "```text\n.\n" + "\n".join(tree_lines) + "\n```"
    with open(TARGET_FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ 地图更新完毕！已启用智能标题兜底模式。")

if __name__ == "__main__":
    main()