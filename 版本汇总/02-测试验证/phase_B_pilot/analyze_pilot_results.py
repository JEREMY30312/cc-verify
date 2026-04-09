#!/usr/bin/env python3
"""
试点结果分析脚本
"""

import json
from pathlib import Path

def analyze_results():
    """分析试点结果"""

    # 读取处理结果
    processed_file = Path("results/pilot_processed_examples.json")
    with open(processed_file, 'r', encoding='utf-8') as f:
        processed_data = json.load(f)

    # 读取评审结果
    review_file = Path("results/pilot_review_results.json")
    with open(review_file, 'r', encoding='utf-8') as f:
        review_data = json.load(f)

    # 生成详细分析报告
    analysis = {
        'executive_summary': {},
        'mode_performance': {},
        'quality_metrics': {},
        'recommendations': [],
        'next_steps': []
    }

    # 提取关键指标
    processed_examples = processed_data.get('modes', {})

    # 分析各模式的表现
    for mode_name, mode_data in processed_examples.items():
        reduction = mode_data.get('reduction', 0)
        p1_preserved = mode_data.get('preserved_p1', 0)
        p2_preserved = mode_data.get('preserved_p2', 0)
        achieved = mode_data.get('achieved_target', False)

        analysis['mode_performance'][mode_name] = {
            'token_reduction': round(reduction, 1),
            'p1_elements_retained': p1_preserved,
            'p2_elements_retained': p2_preserved,
            'target_achieved': achieved,
            'length': len(mode_data.get('content', ''))
        }

    # 分析评审结果
    reviews = review_data.get('reviews', {})

    # 收集各版本的得分
    version_scores = {}
    for reviewer_key, reviewer_data in reviews.items():
        for version, version_data in reviewer_data.get('scores', {}).items():
            if version not in version_scores:
                version_scores[version] = []
            version_scores[version].append(version_data.get('total_score', 0))

    # 计算平均分
    for version, scores in version_scores.items():
        avg_score = sum(scores) / len(scores) if scores else 0
        analysis['quality_metrics'][version] = {
            'average_score': round(avg_score, 2),
            'score_range': f"{min(scores):.1f} - {max(scores):.1f}",
            'reviewer_count': len(scores)
        }

    # 执行摘要
    analysis['executive_summary'] = {
        'best_mode': max(analysis['quality_metrics'].items(),
                        key=lambda x: x[1]['average_score'])[0],
        'best_reduction': max(analysis['mode_performance'].items(),
                            key=lambda x: x[1]['token_reduction'])[0],
        'best_balance': _find_best_balance(analysis)
    }

    # 生成建议
    analysis['recommendations'] = _generate_recommendations(analysis)

    # 下一步
    analysis['next_steps'] = [
        "如果标准模式达成目标→进入阶段C大规模实施",
        "如质量未达标→调整参数后重新试点",
        "保留完整版本作为高质量场景备选"
    ]

    # 保存分析报告
    output_path = Path("results/pilot_analysis_report.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2)

    return analysis

def _find_best_balance(analysis):
    """找出最佳平衡模式"""
    best_mode = 'standard'
    best_score = 0

    for mode in ['full', 'standard', 'fast']:
        if mode in analysis['quality_metrics'] and mode in analysis['mode_performance']:
            quality = analysis['quality_metrics'][mode]['average_score']
            reduction = analysis['mode_performance'][mode]['token_reduction']
            balance_score = quality * (1 + reduction / 100)  # 综合质量+精简率

            if balance_score > best_score:
                best_score = balance_score
                best_mode = mode

    return best_mode

def _generate_recommendations(analysis):
    """生成建议"""
    recommendations = []

    mode_performance = analysis.get('mode_performance', {})
    quality_metrics = analysis.get('quality_metrics', {})

    # 检查标准模式
    if 'standard' in quality_metrics:
        std_score = quality_metrics['standard']['average_score']
        std_reduction = mode_performance['standard']['token_reduction']

        if std_score >= 4.0:
            recommendations.append("✅ 标准模式表现优秀，推荐作为主要输出模式")
            recommendations.append(f"   - 创意质量: {std_score}/5.0")
            recommendations.append(f"   - Token节省: {std_reduction}%")
        elif std_score >= 3.5:
            recommendations.append("✓ 标准模式质量良好，可以作为默认模式")
        else:
            recommendations.append("⚠ 标准模式质量待提升，建议优化P2元素保留率")

    # 检查快速模式
    if 'fast' in quality_metrics:
        fast_score = quality_metrics['fast']['average_score']
        fast_reduction = mode_performance['fast']['token_reduction']

        if fast_score >= 3.0:
            recommendations.append("✓ 快速模式可用于批量处理或快速预览")
        else:
            recommendations.append("⚠ 快速模式质量较低，谨慎使用")

    # 检查完整模式
    if 'full' in quality_metrics:
        full_score = quality_metrics['full']['average_score']
        full_reduction = mode_performance['full']['token_reduction']

        if full_score >= 4.5:
            recommendations.append("✅ 完整模式适合高质量、关键场景")
        else:
            recommendations.append("⚠ 完整模式未达预期，检查P1元素保护")

    return recommendations

if __name__ == "__main__":
    analysis = analyze_results()

    print("=" * 80)
    print("试点结果分析")
    print("=" * 80)

    print(f"\n执行摘要:")
    print(f"  最佳质量模式: {analysis['executive_summary']['best_mode']}")
    print(f"  最大精简模式: {analysis['executive_summary']['best_reduction']}")
    print(f"  最佳平衡模式: {analysis['executive_summary']['best_balance']}")

    print(f"\n各模式表现:")
    for mode, data in analysis['mode_performance'].items():
        print(f"  {mode.upper()}:")
        print(f"    精简率: {data['token_reduction']}%")
        print(f"    P1元素: {data['p1_elements_retained']}个")
        print(f"    P2元素: {data['p2_elements_retained']}个")
        print(f"    质量评分: {analysis['quality_metrics'][mode]['average_score']}/5.0")

    print(f"\n改进建议:")
    for rec in analysis['recommendations']:
        print(f"  {rec}")

    print(f"\n下一步:")
    for step in analysis['next_steps']:
        print(f"  • {step}")

    print("\n✅ 试点分析完成")
