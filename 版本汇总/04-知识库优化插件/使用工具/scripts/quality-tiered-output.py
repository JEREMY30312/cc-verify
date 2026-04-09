#!/usr/bin/env python3
"""
分级输出模式
完整/标准/快速三种模式，平衡性能与质量
"""

import json
from typing import Dict, List, Optional
from pathlib import Path
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from creative_quality_improver import CreativeQualityImprover

class TieredOutputManager:
    """分级输出管理器"""
    
    def __init__(self):
        self.quality_improver = CreativeQualityImprover()
        self.tiers = {
            'complete': {
                'name': '完整模式',
                'description': '最高质量，保留所有创意细节和电影语言',
                'token_budget': 100,  # 100% of original
                'quality_target': 95.0,
                'preservation_rate': 1.0
            },
            'standard': {
                'name': '标准模式',
                'description': '平衡质量与性能，保留核心创意元素',
                'token_budget': 70,   # 70% of original
                'quality_target': 80.0,
                'preservation_rate': 0.8
            },
            'fast': {
                'name': '快速模式',
                'description': '最佳性能，精简但保持创意核心',
                'token_budget': 50,   # 50% of original
                'quality_target': 70.0,
                'preservation_rate': 0.6
            }
        }
    
    def generate_tiered_output(self, content: str, tier: str = 'standard') -> Dict:
        """生成分级输出"""
        if tier not in self.tiers:
            raise ValueError(f"无效的输出层级: {tier}")
        
        tier_config = self.tiers[tier]
        
        # 分析原始内容质量
        original_analysis = self.quality_improver.analyze_creative_quality(content)
        
        # 根据层级选择策略
        result = {}
        if tier == 'complete':
            result = self._generate_complete_mode(content, tier_config)
        elif tier == 'standard':
            result = self._generate_standard_mode(content, tier_config)
        elif tier == 'fast':
            result = self._generate_fast_mode(content, tier_config)
        else:
            raise ValueError(f"无效的输出层级: {tier}")
        
        # 分析输出质量
        output_analysis = self.quality_improver.analyze_creative_quality(result['content'])
        
        return {
            'tier': tier,
            'tier_name': tier_config['name'],
            'original_content': content,
            'output_content': result['content'],
            'original_quality': original_analysis['quality_score'],
            'output_quality': output_analysis['quality_score'],
            'quality_change': output_analysis['quality_score'] - original_analysis['quality_score'],
            'token_reduction': result['token_reduction'],
            'quality_target': tier_config['quality_target'],
            'quality_met': output_analysis['quality_score'] >= tier_config['quality_target'],
            'enhancements_applied': result['enhancements']
        }
    
    def _generate_complete_mode(self, content: str, tier_config: Dict) -> Dict:
        """完整模式：增强质量，保留所有细节"""
        # 不精简，只增强创意质量
        enhancement = self.quality_improver.enhance_creative_content(content, target_score=95.0)
        
        return {
            'content': enhancement['enhanced_content'],
            'token_reduction': 0,
            'enhancements': enhancement['enhancements']
        }
    
    def _generate_standard_mode(self, content: str, tier_config: Dict) -> Dict:
        """标准模式：智能精简，保持核心创意"""
        # 智能精简，保持90%的质量
        simplification = self.quality_improver.intelligent_simplify(
            content, 
            reduction_target=0.3
        )
        
        return {
            'content': simplification['simplified_content'],
            'token_reduction': simplification['reduction_percentage'],
            'enhancements': ['智能精简', '保留创意核心']
        }
    
    def _generate_fast_mode(self, content: str, tier_config: Dict) -> Dict:
        """快速模式：大幅精简，保留创意核心"""
        # 更激进的精简
        simplification = self.quality_improver.intelligent_simplify(
            content, 
            reduction_target=0.5
        )
        
        # 如果质量下降太多，进行创意增强
        quality_maintained = simplification['quality_maintained']
        if not quality_maintained:
            enhancement = self.quality_improver.enhance_creative_content(
                simplification['simplified_content'],
                target_score=70.0
            )
            final_content = enhancement['enhanced_content']
            enhancements = ['激进精简', '创意增强']
        else:
            final_content = simplification['simplified_content']
            enhancements = ['激进精简', '保留创意核心']
        
        return {
            'content': final_content,
            'token_reduction': simplification['reduction_percentage'],
            'enhancements': enhancements
        }
    
    def compare_tiers(self, content: str) -> Dict:
        """比较所有输出层级"""
        results = {}
        
        for tier in self.tiers.keys():
            results[tier] = self.generate_tiered_output(content, tier)
        
        return {
            'comparison': results,
            'recommendations': self._make_recommendations(results)
        }
    
    def _make_recommendations(self, results: Dict) -> List[Dict]:
        """根据结果推荐层级"""
        recommendations = []
        
        # 完整模式：质量最高，适合创意要求高的场景
        if results['complete']['quality_met']:
            recommendations.append({
                'tier': 'complete',
                'use_case': '创意要求高、Token预算充足',
                'benefit': '最佳创意质量，适合最终输出'
            })
        
        # 标准模式：平衡，适合一般场景
        if results['standard']['quality_met']:
            recommendations.append({
                'tier': 'standard',
                'use_case': '一般使用场景',
                'benefit': '平衡质量与性能，推荐默认使用'
            })
        
        # 快速模式：最佳性能，适合快速迭代
        if results['fast']['quality_met']:
            recommendations.append({
                'tier': 'fast',
                'use_case': '快速迭代、草稿生成',
                'benefit': '最佳性能，适合内部评审'
            })
        
        return recommendations

if __name__ == "__main__":
    # 测试分级输出
    manager = TieredOutputManager()
    
    # 测试内容
    test_content = """特写，老人的面容。
他望向雨水划过的窗户，眼中闪着未落的泪光，嘴角却浮现一丝温柔的微笑。手中握着一张老照片，手指轻轻描摹着边缘。
黄金时段的柔光透过窗户，温暖她的面容，在凌乱的发丝上晕出光晕。
背景是温馨的客厅和书架，85mm镜头虚化成柔和的色块。
苦涩而温柔，私密的回忆时刻。"""
    
    print("测试分级输出模式\n")
    
    # 比较所有层级
    comparison = manager.compare_tiers(test_content)
    
    for tier, result in comparison['comparison'].items():
        print(f"\n{result['tier_name']}:")
        print(f"  质量变化: {result['original_quality']:.1f} → {result['output_quality']:.1f}")
        print(f"  Token减少: {result['token_reduction']:.1f}%")
        print(f"  质量目标: {result['quality_target']}")
        print(f"  质量达成: {'✅' if result['quality_met'] else '❌'}")
        print(f"  应用增强: {', '.join(result['enhancements_applied'])}")
    
    print("\n" + "="*50)
    print("推荐:")
    for rec in comparison['recommendations']:
        print(f"\n  {rec['tier']}模式:")
        print(f"    适用场景: {rec['use_case']}")
        print(f"    优势: {rec['benefit']}")