"""
> **Description:** 增强版项目地图生成器 V2.0 - 支持Git状态、学习机制、YAML描述

项目地图生成器 V2.0
支持Git集成、完整学习机制、YAML front matter描述提取
"""

import os
import datetime
import time
import json
import subprocess
import re
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Any
from collections import defaultdict
from dataclasses import dataclass, field, asdict

# ================= 配置区域 =================

TARGET_FILE = 'PROJECT_MAP.md'
FINGERPRINT_FILE = 'PROJECT_FINGERPRINT.json'
TIME_RANGE_HOURS = 168  # 7天
MAX_DESCRIPTION_LENGTH = 20

# 忽略列表
IGNORE_LIST = {
    '.git', 'node_modules', '__pycache__', '.DS_Store',
    'dist', 'build', '.idea', '.vscode', '.sisyphus',
    '.opencode', '.backup', '.backups'
}

# 折叠目录
COLLAPSE_FOLDERS = {'backups', '.strategic-snapshots', '版本汇总', '.backup'}

# 变更图标映射
CHANGE_ICONS = {
    'M': ('🟢', '修改'),
    'A': ('🔵', '新增'),
    'D': ('🔴', '删除'),
    'R': ('🟡', '重命名'),
    'C': ('🟣', '复制'),
    'U': ('🟠', '冲突'),
    '??': ('⚪', '未跟踪'),
}

# ================= 数据类定义 =================

@dataclass
class FileInfo:
    """文件信息"""
    path: str
    name: str
    directory: str
    mtime: float
    size: int
    description: str = ""
    is_new_format: bool = False  # 是否使用YAML front matter

@dataclass
class GitChange:
    """Git变更记录"""
    status: str
    file_path: str
    original_path: Optional[str] = None
    change_time: Optional[datetime.datetime] = None

@dataclass
class ProjectInsight:
    """项目洞察"""
    domain: str
    architecture: str
    primary_language: str
    key_characteristics: List[str]

@dataclass
class ProjectFingerprint:
    """项目指纹"""
    metadata: Dict[str, Any]
    project_profile: Dict[str, Any]
    structural_insights: Dict[str, Any]
    temporal_analysis: Dict[str, Any]
    ai_optimized_index: Dict[str, Any]

# ================= 描述提取器 =================

def extract_yaml_description(file_path: str) -> Optional[str]:
    """从YAML front matter提取描述"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read(1000)  # 只读取前1000字符
        
        # 检查是否有YAML front matter
        if not content.startswith('---'):
            return None
        
        # 查找结束的 ---
        end_match = re.search(r'\n---\s*\n', content)
        if not end_match:
            return None
        
        yaml_content = content[3:end_match.start()]
        
        # 查找 description 字段
        desc_match = re.search(r'^description:\s*(.+)$', yaml_content, re.MULTILINE)
        if desc_match:
            desc = desc_match.group(1).strip()
            # 去除引号
            if (desc.startswith('"') and desc.endswith('"')) or \
               (desc.startswith("'") and desc.endswith("'")):
                desc = desc[1:-1]
            return desc[:MAX_DESCRIPTION_LENGTH]
        
        return None
    except Exception:
        return None

def extract_markdown_description(file_path: str) -> Optional[str]:
    """从Markdown引用块提取描述（兼容旧格式）"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()[:10]
        
        for line in lines:
            # 匹配 > **Description:** ...
            match = re.search(r'>\s*\*\*(?:Desc|Description):\*\*\s*(.+)', line, re.IGNORECASE)
            if match:
                return match.group(1).strip()[:MAX_DESCRIPTION_LENGTH]
        
        return None
    except Exception:
        return None

def get_file_description(file_path: str) -> Tuple[str, bool]:
    """
    获取文件描述
    
    Returns:
        (描述字符串, 是否为新格式YAML)
    """
    if not file_path.endswith('.md'):
        return "", False
    
    # 优先尝试YAML格式
    yaml_desc = extract_yaml_description(file_path)
    if yaml_desc:
        return yaml_desc, True
    
    # 回退到Markdown格式
    md_desc = extract_markdown_description(file_path)
    if md_desc:
        return md_desc, False
    
    return "", False

# ================= Git集成模块 =================

def is_git_repository(path: str = ".") -> bool:
    """检查是否为Git仓库"""
    try:
        result = subprocess.run(
            ["git", "-C", path, "rev-parse", "--git-dir"],
            capture_output=True, text=True, check=False
        )
        return result.returncode == 0
    except Exception:
        return False

def get_git_status(repo_path: str = ".") -> List[GitChange]:
    """获取Git状态"""
    if not is_git_repository(repo_path):
        return []
    
    try:
        result = subprocess.run(
            ["git", "-C", repo_path, "status", "--porcelain"],
            capture_output=True, text=True, check=True
        )
        
        changes = []
        for line in result.stdout.strip().split('\n'):
            if not line:
                continue
            
            staged = line[0]
            unstaged = line[1]
            status = unstaged if unstaged != ' ' and unstaged != '?' else staged
            rest = line[3:]
            
            # 处理重命名
            if status == 'R' and ' -> ' in rest:
                parts = rest.split(' -> ')
                changes.append(GitChange(status, parts[1], parts[0]))
            else:
                changes.append(GitChange(status, rest))
        
        return changes
    except Exception:
        return []

def get_file_git_info(file_path: str) -> Optional[datetime.datetime]:
    """获取文件的最后Git提交时间"""
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%ct", "--", file_path],
            capture_output=True, text=True, check=False
        )
        if result.returncode == 0 and result.stdout.strip():
            timestamp = int(result.stdout.strip())
            return datetime.datetime.fromtimestamp(timestamp)
        return None
    except Exception:
        return None

# ================= 项目结构扫描 =================

def scan_project_structure(dir_path: str = '.') -> List[FileInfo]:
    """扫描项目结构"""
    files_info = []
    
    for root, dirs, files in os.walk(dir_path):
        # 过滤目录
        dirs[:] = [d for d in dirs if d not in IGNORE_LIST and not d.startswith('.')]
        
        for file in files:
            if file in IGNORE_LIST or file.startswith('.'):
                continue
            
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, start='.')
            
            try:
                stat = os.stat(full_path)
                desc, is_new = get_file_description(full_path)
                
                files_info.append(FileInfo(
                    path=rel_path,
                    name=file,
                    directory=os.path.dirname(rel_path) if os.path.dirname(rel_path) else '根目录',
                    mtime=stat.st_mtime,
                    size=stat.st_size,
                    description=desc,
                    is_new_format=is_new
                ))
            except Exception:
                continue
    
    return files_info

# ================= 学习机制模块 =================

def analyze_project_domain(files_info: List[FileInfo]) -> str:
    """分析项目领域"""
    # 基于文件类型和名称关键词分析
    extensions = defaultdict(int)
    name_keywords = defaultdict(int)
    
    for f in files_info:
        ext = Path(f.name).suffix.lower()
        if ext:
            extensions[ext] += 1
        
        # 提取关键词
        words = re.findall(r'[a-zA-Z_]+', f.name.lower())
        for word in words:
            if len(word) > 2:
                name_keywords[word] += 1
    
    # 判断领域
    if '.py' in extensions and extensions['.py'] > 5:
        return "Python项目"
    elif '.js' in extensions or '.ts' in extensions:
        return "JavaScript/TypeScript项目"
    elif '.md' in extensions and extensions['.md'] > 20:
        return "文档型项目"
    else:
        return "通用项目"

def detect_architecture(files_info: List[FileInfo]) -> str:
    """检测架构模式"""
    dirs = set(f.directory for f in files_info)
    
    patterns = []
    
    # 检查常见架构模式
    if any('skills' in d or 'skill' in d for d in dirs):
        patterns.append("SKILL-based")
    if any('agents' in d or 'agent' in d for d in dirs):
        patterns.append("Agent协作")
    if any('test' in d for d in dirs):
        patterns.append("测试驱动")
    if any('.claude' in d for d in dirs):
        patterns.append("Claude集成")
    
    return ", ".join(patterns) if patterns else "标准结构"

def identify_key_characteristics(files_info: List[FileInfo]) -> List[str]:
    """识别关键特征"""
    characteristics = []
    dirs = set(f.directory for f in files_info)
    
    # 检查特定模式
    if any('workflow' in f.name.lower() for f in files_info):
        characteristics.append("工作流驱动")
    if any('review' in f.name.lower() for f in files_info):
        characteristics.append("审核机制")
    if any('prompt' in f.name.lower() for f in files_info):
        characteristics.append("提示词工程")
    if any('config' in d.lower() for d in dirs):
        characteristics.append("配置化")
    
    # 统计信息
    md_files = sum(1 for f in files_info if f.name.endswith('.md'))
    if md_files > 30:
        characteristics.append("重度文档化")
    
    return characteristics[:5]  # 最多返回5个

def analyze_file_relationships(files_info: List[FileInfo]) -> Dict[str, List[str]]:
    """分析文件关系"""
    relationships = defaultdict(list)
    
    # 基于命名模式推断关系
    for f in files_info:
        base_name = Path(f.name).stem
        
        # 查找相关文件
        for other in files_info:
            if other.path == f.path:
                continue
            
            other_base = Path(other.name).stem
            
            # 检查是否是变体（如 xxx.md 和 xxx-review.md）
            if other_base.startswith(base_name) or base_name.startswith(other_base):
                relationships[f.path].append(other.path)
    
    return dict(relationships)

def generate_ai_index(files_info: List[FileInfo], git_changes: List[GitChange]) -> Dict[str, Any]:
    """生成AI优化索引"""
    
    # 快速回答映射
    quick_answers = {}
    
    # 基于文件内容推断常见问题
    for f in files_info:
        if 'README' in f.name or 'AGENTS' in f.name:
            quick_answers['如何开始'] = f.path
        if 'config' in f.name.lower():
            quick_answers['配置在哪里'] = f.path
        if 'skill' in f.path.lower():
            quick_answers['技能文档'] = f.path
        if 'review' in f.name.lower():
            quick_answers['审核流程'] = f.path
    
    # 搜索快捷方式
    search_shortcuts = defaultdict(list)
    for f in files_info:
        if f.name.endswith('.md'):
            search_shortcuts['Markdown文档'].append(f.path)
        elif f.name.endswith('.py'):
            search_shortcuts['Python脚本'].append(f.path)
        elif f.name.endswith('.json'):
            search_shortcuts['JSON配置'].append(f.path)
    
    # 热点目录
    recent_dirs = defaultdict(int)
    for change in git_changes:
        dir_path = os.path.dirname(change.file_path) or '根目录'
        recent_dirs[dir_path] += 1
    
    hot_directories = sorted(recent_dirs.items(), key=lambda x: x[1], reverse=True)[:5]
    
    return {
        'quick_answers': quick_answers,
        'search_shortcuts': dict(search_shortcuts),
        'hot_directories': hot_directories,
        'file_count': len(files_info),
        'git_change_count': len(git_changes)
    }

def generate_project_fingerprint(files_info: List[FileInfo], git_changes: List[GitChange]) -> Dict[str, Any]:
    """生成项目指纹"""
    
    # 基础统计
    total_files = len(files_info)
    total_dirs = len(set(f.directory for f in files_info))
    
    # 项目画像
    domain = analyze_project_domain(files_info)
    architecture = detect_architecture(files_info)
    characteristics = identify_key_characteristics(files_info)
    
    # 关键目录
    key_dirs = defaultdict(lambda: {'count': 0, 'files': []})
    for f in files_info:
        top_dir = f.directory.split('/')[0] if '/' in f.directory else f.directory
        key_dirs[top_dir]['count'] += 1
        if len(key_dirs[top_dir]['files']) < 5:
            key_dirs[top_dir]['files'].append(f.name)
    
    # 时序分析
    now = datetime.datetime.now()
    cutoff_time = now - datetime.timedelta(hours=TIME_RANGE_HOURS)
    
    recent_changes = []
    for change in git_changes:
        if change.change_time and change.change_time >= cutoff_time:
            recent_changes.append(change)
    
    # AI索引
    ai_index = generate_ai_index(files_info, git_changes)
    
    fingerprint = {
        'metadata': {
            'generated_at': now.isoformat(),
            'generator_version': '2.0',
            'total_files': total_files,
            'total_directories': total_dirs,
            'time_range_hours': TIME_RANGE_HOURS
        },
        'project_profile': {
            'domain': domain,
            'architecture': architecture,
            'key_characteristics': characteristics
        },
        'structural_insights': {
            'key_directories': dict(key_dirs),
            'file_type_distribution': dict(
                (ext, count) for ext, count in 
                sorted(
                    [(Path(f.name).suffix, sum(1 for x in files_info if x.name.endswith(Path(f.name).suffix))) 
                     for f in files_info if Path(f.name).suffix],
                    key=lambda x: x[1], reverse=True
                )[:5]
            )
        },
        'temporal_analysis': {
            'recent_changes_count': len(recent_changes),
            'hot_directories': ai_index['hot_directories']
        },
        'ai_optimized_index': ai_index
    }
    
    return fingerprint

# ================= 输出生成 =================

def generate_change_table(changes: List[GitChange], files_info: List[FileInfo]) -> str:
    """生成变更表格"""
    if not changes:
        return "_暂无变更记录_"
    
    # 按时间排序
    sorted_changes = sorted(
        changes, 
        key=lambda x: x.change_time or datetime.datetime.min, 
        reverse=True
    )
    
    lines = ['| 文件 | 目录 | 变更 | 时间 | 描述 |', '|------|------|------|------|------|']
    
    for change in sorted_changes[:20]:  # 最多显示20条
        file_name = os.path.basename(change.file_path)
        directory = os.path.dirname(change.file_path) or '根目录'
        
        icon, desc = CHANGE_ICONS.get(change.status, ('⚪', '未知'))
        change_str = f"{icon} {desc}"
        
        time_str = change.change_time.strftime('%m-%d %H:%M') if change.change_time else '-'
        
        # 查找文件描述
        file_desc = ""
        for f in files_info:
            if f.path == change.file_path:
                file_desc = f.description
                break
        
        lines.append(f"| {file_name} | {directory} | {change_str} | {time_str} | {file_desc or '-'} |")
    
    return '\n'.join(lines)

def generate_tree(dir_path: str, prefix: str = '', depth: int = 0, files_info: List[FileInfo] = None) -> List[str]:
    """生成目录树"""
    if depth > 5:
        return []
    
    if files_info is None:
        files_info = scan_project_structure(dir_path)
    
    try:
        entries = sorted(os.listdir(dir_path))
    except PermissionError:
        return []
    
    filtered = [e for e in entries if e not in IGNORE_LIST and not e.startswith('.')]
    
    result = []
    pointers = [('├── ', '│   ')] * (len(filtered) - 1) + [('└── ', '    ')]
    
    for pointer, entry in zip(pointers, filtered):
        full_path = os.path.join(dir_path, entry)
        rel_path = os.path.relpath(full_path, start='.')
        
        # 查找描述
        desc = ""
        for f in files_info:
            if f.path == rel_path:
                desc = f.description
                break
        
        comment = f"  # {desc}" if desc else ""
        result.append(f"{prefix}{pointer[0]}{entry}{comment}")
        
        if os.path.isdir(full_path):
            if entry in COLLAPSE_FOLDERS:
                result.append(f"{prefix}{pointer[1]}└── ...")
            else:
                result.extend(generate_tree(full_path, prefix + pointer[1], depth + 1, files_info))
    
    return result

def generate_project_map(files_info: List[FileInfo], git_changes: List[GitChange]) -> str:
    """生成项目地图"""
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # 生成变更表格
    change_table = generate_change_table(git_changes, files_info)
    
    # 生成目录树
    tree_lines = generate_tree('.', files_info=files_info)
    
    content = f"""# 🗺️ 项目地图 (Live)

> **Updated:** {timestamp}
> **Version:** 2.0 | **Mode:** Git集成 + 学习机制

## 🔥 最近变动 (7天)

{change_table}

## 📂 文件目录

```text
.
{chr(10).join(tree_lines)}
```

---
*由 generate_map_v2.py 自动生成*
"""
    
    return content

# ================= 主函数 =================

def main():
    """主函数"""
    print("🚀 开始生成项目地图 V2.0...")
    
    # 1. 扫描项目结构
    print("📁 扫描项目结构...")
    files_info = scan_project_structure('.')
    print(f"   找到 {len(files_info)} 个文件")
    
    # 2. 获取Git状态
    print("🔍 获取Git状态...")
    git_changes = get_git_status('.')
    print(f"   找到 {len(git_changes)} 个变更")
    
    # 3. 生成项目地图
    print("📝 生成项目地图...")
    map_content = generate_project_map(files_info, git_changes)
    
    with open(TARGET_FILE, 'w', encoding='utf-8') as f:
        f.write(map_content)
    print(f"   ✅ 已保存到 {TARGET_FILE}")
    
    # 4. 生成项目指纹
    print("🧠 生成项目指纹...")
    fingerprint = generate_project_fingerprint(files_info, git_changes)
    
    with open(FINGERPRINT_FILE, 'w', encoding='utf-8') as f:
        json.dump(fingerprint, f, ensure_ascii=False, indent=2)
    print(f"   ✅ 已保存到 {FINGERPRINT_FILE}")
    
    print("\n✨ 完成！")
    print(f"   - 项目地图: {TARGET_FILE}")
    print(f"   - 项目指纹: {FINGERPRINT_FILE}")

if __name__ == '__main__':
    main()
