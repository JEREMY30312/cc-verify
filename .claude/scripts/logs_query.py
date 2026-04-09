#!/usr/bin/env python3
"""
日志查询系统
Usage: python logs_query.py <command> [args]
Commands:
    list                    - 显示最近3次执行摘要
    last                    - 显示最近1次执行详情
    <exec-id>               - 显示特定执行详情
    files                   - 文件操作统计
    deps <file>             - 文件依赖图
    timeline                - 执行时间线
    modules                 - 模块使用统计
    debug                   - 调试信息
    search <keyword>        - 搜索日志记录
"""

import json
import sys
from datetime import datetime
from pathlib import Path

LOG_FILE = Path(__file__).parent.parent / ".execution-log.json"


def load_log():
    """加载日志文件"""
    if not LOG_FILE.exists():
        return {
            "executions": {},
            "last_execution_id": None,
            "statistics": {
                "total_executions": 0,
                "successful_executions": 0,
                "failed_executions": 0,
            },
        }
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {
            "executions": {},
            "last_execution_id": None,
            "statistics": {
                "total_executions": 0,
                "successful_executions": 0,
                "failed_executions": 0,
            },
        }


def format_duration(ms):
    """格式化时长"""
    if ms < 1000:
        return f"{ms}ms"
    return f"{ms / 1000:.1f}s"


def cmd_list(log):
    """显示最近执行摘要"""
    executions = log.get("executions", {})
    if not executions:
        print("📊 最近执行摘要\n\n暂无执行记录")
        return

    sorted_ids = sorted(executions.keys(), reverse=True)[:3]
    print("📊 最近执行摘要\n")
    for exec_id in sorted_ids:
        exec_data = executions[exec_id]
        status = "✅ 成功" if exec_data.get("status") == "success" else "❌ 失败"
        duration = format_duration(exec_data.get("duration_ms", 0))
        cmd = exec_data.get("command", "")
        print(f"{exec_id} [{cmd}] - {duration} - {status}")


def cmd_last(log):
    """显示最近一次执行详情"""
    executions = log.get("executions", {})
    if not executions:
        print("📋 执行详情\n\n暂无执行记录")
        return

    last_id = log.get("last_execution_id") or sorted(executions.keys())[-1]
    if last_id not in executions:
        last_id = sorted(executions.keys())[-1]

    exec_data = executions[last_id]
    print(f"📋 执行详情 ({last_id}: {exec_data.get('command', '')})")
    print(f"\n执行时间: {exec_data.get('timestamp', '')}")
    print(f"总耗时: {format_duration(exec_data.get('duration_ms', 0))}")
    status = "✅ 成功" if exec_data.get("status") == "success" else "❌ 失败"
    print(f"状态: {status}")

    print("\n步骤详情:")
    for i, step in enumerate(exec_data.get("steps", []), 1):
        duration = format_duration(step.get("duration_ms", 0))
        name = step.get("name", f"步骤{i}")
        print(f"[步骤{i}] {name} ({duration})")
        for f in step.get("files_read", []):
            print(f"  📖 读取: {f}")
        for m in step.get("modules_used", []):
            print(f"  🧩 模块: {m}")
        if step.get("output"):
            print(f"  📝 输出: {step.get('output')}")


def cmd_show(log, exec_id):
    """显示特定执行详情"""
    executions = log.get("executions", {})
    if exec_id not in executions:
        print(f"未找到执行记录: {exec_id}")
        return

    exec_data = executions[exec_id]
    print(f"📋 执行详情 ({exec_id}: {exec_data.get('command', '')})")
    print(f"\n执行时间: {exec_data.get('timestamp', '')}")
    print(f"总耗时: {format_duration(exec_data.get('duration_ms', 0))}")
    status = "✅ 成功" if exec_data.get("status") == "success" else "❌ 失败"
    print(f"状态: {status}")

    print("\n步骤详情:")
    for i, step in enumerate(exec_data.get("steps", []), 1):
        duration = format_duration(step.get("duration_ms", 0))
        name = step.get("name", f"步骤{i}")
        print(f"[步骤{i}] {name} ({duration})")
        for f in step.get("files_read", []):
            print(f"  📖 读取: {f}")
        for m in step.get("modules_used", []):
            print(f"  🧩 模块: {m}")


def cmd_files(log):
    """文件操作统计"""
    executions = log.get("executions", {})
    if not executions:
        print("📁 文件操作统计\n\n暂无执行记录")
        return

    file_count = {}
    for exec_data in executions.values():
        for step in exec_data.get("steps", []):
            for f in step.get("files_read", []):
                file_count[f] = file_count.get(f, 0) + 1

    sorted_files = sorted(file_count.items(), key=lambda x: -x[1])
    print("📁 文件操作统计\n\n最常读取:")
    for f, count in sorted_files[:10]:
        print(f"  {count}次 - {f}")

    print("\n最近写入:")
    recent_writes = set()
    for exec_data in executions.values():
        for step in exec_data.get("steps", []):
            if step.get("output"):
                recent_writes.add(step.get("output"))
    for w in list(recent_writes)[-5:]:
        print(f"  - {w}")


def cmd_timeline(log):
    """执行时间线"""
    executions = log.get("executions", {})
    if not executions:
        print("⏱️ 执行时间线\n\n暂无执行记录")
        return

    last_id = log.get("last_execution_id") or sorted(executions.keys())[-1]
    exec_data = executions.get(last_id, {})
    if not exec_data:
        print("⏱️ 执行时间线\n\n暂无执行记录")
        return

    print(f"⏱️ 执行时间线 ({last_id})")
    print(f"命令: {exec_data.get('command', '')}")
    print(f"总耗时: {format_duration(exec_data.get('duration_ms', 0))}\n")

    base_time = exec_data.get("timestamp", "")
    print(f"[{base_time}] 开始执行 {exec_data.get('command', '')}")
    for i, step in enumerate(exec_data.get("steps", []), 1):
        duration = format_duration(step.get("duration_ms", 0))
        name = step.get("name", f"步骤{i}")
        print(f"[{base_time} + {duration}] ✓ {name}")


def cmd_modules(log):
    """模块使用统计"""
    executions = log.get("executions", {})
    if not executions:
        print("🧩 模块使用统计\n\n暂无执行记录")
        return

    module_count = {}
    for exec_data in executions.values():
        for step in exec_data.get("steps", []):
            for m in step.get("modules_used", []):
                module_count[m] = module_count.get(m, 0) + 1

    sorted_modules = sorted(module_count.items(), key=lambda x: -x[1])
    print("🧩 模块使用统计\n")
    for m, count in sorted_modules[:10]:
        print(f"  {count}次 - {m}")


def cmd_debug(log):
    """调试信息"""
    executions = log.get("executions", {})
    stats = log.get("statistics", {})
    print("🐛 调试信息")
    print(f"\n总执行次数: {stats.get('total_executions', 0)}")
    print(f"成功: {stats.get('successful_executions', 0)}")
    print(f"失败: {stats.get('failed_executions', 0)}")

    print("\n最近的错误:")
    errors_found = False
    for exec_id in sorted(executions.keys(), reverse=True):
        exec_data = executions[exec_id]
        if exec_data.get("status") == "failed":
            errors_found = True
            print(f"  {exec_id} - {exec_data.get('command', '')}")
            for step in exec_data.get("steps", []):
                if step.get("error"):
                    print(f"    错误: {step.get('error')}")
    if not errors_found:
        print("  无错误记录")


def cmd_search(log, keyword):
    """搜索日志记录"""
    executions = log.get("executions", {})
    if not executions:
        print(f"🔍 搜索: {keyword}\n\n暂无执行记录")
        return

    keyword = keyword.lower()
    print(f"🔍 搜索: {keyword}\n")
    results = []
    for exec_id, exec_data in executions.items():
        cmd = exec_data.get("command", "").lower()
        if keyword in cmd:
            results.append((exec_id, exec_data.get("command", ""), "命令匹配"))
        for step in exec_data.get("steps", []):
            name = step.get("name", "").lower()
            if keyword in name:
                results.append((exec_id, step.get("name", ""), "步骤匹配"))
            for f in step.get("files_read", []):
                if keyword in f.lower():
                    results.append((exec_id, f, "文件匹配"))

    if results:
        for exec_id, match, reason in results[:20]:
            print(f"  {exec_id} - {match[:50]}... [{reason}]")
    else:
        print("  未找到匹配结果")


def main():
    """主函数"""
    log = load_log()

    if len(sys.argv) < 2:
        cmd_list(log)
        return

    cmd = sys.argv[1]

    if cmd == "list":
        cmd_list(log)
    elif cmd == "last":
        cmd_last(log)
    elif cmd == "files":
        cmd_files(log)
    elif cmd == "timeline":
        cmd_timeline(log)
    elif cmd == "modules":
        cmd_modules(log)
    elif cmd == "debug":
        cmd_debug(log)
    elif cmd == "search":
        if len(sys.argv) < 3:
            print("用法: python logs_query.py search <关键词>")
        else:
            cmd_search(log, sys.argv[2])
    elif cmd.startswith("exec-"):
        cmd_show(log, cmd)
    else:
        print(f"未知命令: {cmd}")
        print(
            "可用命令: list, last, files, timeline, modules, debug, search <关键词>, <exec-id>"
        )


if __name__ == "__main__":
    main()
