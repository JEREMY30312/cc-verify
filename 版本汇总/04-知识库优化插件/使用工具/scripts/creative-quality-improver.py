#!/usr/bin/env python3
"""
创意质量改进器
在精简过程中保持创意质量，避免过度简化
"""

import re
import json
from typing import Dict, List, Set
from pathlib import Path

class CreativeQualityImprover:
    """创意质量改进系统"""
    
    def __init__(self):
        # 创意核心元素关键词
        self.creative_keywords = {
            'visual_metaphors': ['光晕', '剪影', '残影', '光斑', '阴影', '轮廓', '轮廓光'],
            'emotional_details': ['皱纹', '泪光', '瞳孔', '嘴角', '微表情', '发丝光'],
            'environmental_details': ['虚化', '散景', '色块', '质感', '纹理'],
            'cinematic_techniques': ['荷兰角', '低机位', '高角度', '仰拍', '俯拍', '浅景深', '景深'],
            'lighting_effects': ['体积光', '侧光', '逆光', '眼神光', '发丝光', '轮廓光', '丁达尔效应'],
            'color_grading': ['饱和', '色调', '色温', '色偏', '对比度', '高调', '低调']
        }
        
        # 创意质量检查点
        self.quality_checkpoints = {
            'min_creative_elements': 3,  # 最少创意元素数量
            'min_visual_density': 2,     # 最少视觉密度
            'emotional_depth': True,      # 是否有情感深度
            'cinematic_completeness': True # 是否有完整的电影语言
        }
    
    def analyze_creative_quality(self, content: str) -> Dict:
        """分析创意质量"""
        analysis = {
            'total_elements': 0,
            'element_counts': {},
            'visual_density': 0,
            'emotional_depth': 0,
            'cinematic_completeness': 0,
            'quality_score': 0.0,
            'missing_elements': []
        }
        
        # 统计各类创意元素
        for category, keywords in self.creative_keywords.items():
            count = sum(1 for keyword in keywords if keyword in content)
            analysis['element_counts'][category] = count
            analysis['total_elements'] += count
            
            # 计算视觉密度
            if category in ['visual_metaphors', 'environmental_details', 'lighting_effects', 'color_grading']:
                analysis['visual_density'] += count
            
            # 计算情感深度
            if category in ['emotional_details']:
                analysis['emotional_depth'] += count
            
            # 计算电影语言完整性
            if category in ['cinematic_techniques', 'lighting_effects']:
                analysis['cinematic_completeness'] += count
        
        # 检查缺失元素
        for category, keywords in self.creative_keywords.items():
            if analysis['element_counts'][category] == 0:
                analysis['missing_elements'].append(category)
        
        # 计算质量分数 (0-100)
        analysis['quality_score'] = self._calculate_quality_score(analysis)
        
        return analysis
    
    def _calculate_quality_score(self, analysis: Dict) -> float:
        """计算创意质量分数"""
        score = 0.0
        
        # 创意元素数量 (30分)
        element_score = min(analysis['total_elements'] / 10, 1.0) * 30
        score += element_score
        
        # 视觉密度 (25分)
        density_score = min(analysis['visual_density'] / 5, 1.0) * 25
        score += density_score
        
        # 情感深度 (20分)
        emotion_score = min(analysis['emotional_depth'] / 3, 1.0) * 20
        score += emotion_score
        
        # 电影语言完整性 (25分)
        cinematic_score = min(analysis['cinematic_completeness'] / 4, 1.0) * 25
        score += cinematic_score
        
        return round(score, 1)
    
    def enhance_creative_content(self, content: str, target_score: float = 85.0) -> Dict:
        """增强创意内容，提高质量分数"""
        analysis = self.analyze_creative_quality(content)
        
        if analysis['quality_score'] >= target_score:
            return {
                'enhanced_content': content,
                'original_score': analysis['quality_score'],
                'new_score': analysis['quality_score'],
                'enhancements': [],
                'score_improvement': 0.0
            }  # 已达到目标质量
        
        enhanced_content = content
        enhancements = []
        
        # 基于缺失元素进行增强
        for category in analysis['missing_elements']:
            if category == 'visual_metaphors':
                # 添加视觉隐喻
                enhanced_content = self._add_visual_metaphor(enhanced_content)
                enhancements.append(f"添加{category}元素")
            elif category == 'emotional_details':
                # 添加情感细节
                enhanced_content = self._add_emotional_detail(enhanced_content)
                enhancements.append(f"添加{category}元素")
            elif category == 'environmental_details':
                # 添加环境细节
                enhanced_content = self._add_environmental_detail(enhanced_content)
                enhancements.append(f"添加{category}元素")
            elif category == 'cinematic_techniques':
                # 添加电影技术
                enhanced_content = self._add_cinematic_technique(enhanced_content)
                enhancements.append(f"添加{category}元素")
            elif category == 'lighting_effects':
                # 添加光影效果
                enhanced_content = self._add_lighting_effect(enhanced_content)
                enhancements.append(f"添加{category}元素")
            elif category == 'color_grading':
                # 添加色彩信息
                enhanced_content = self._add_color_grading(enhanced_content)
                enhancements.append(f"添加{category}元素")
        
        # 重新检查质量
        new_analysis = self.analyze_creative_quality(enhanced_content)
        
        return {
            'enhanced_content': enhanced_content,
            'original_score': analysis['quality_score'],
            'new_score': new_analysis['quality_score'],
            'enhancements': enhancements,
            'score_improvement': new_analysis['quality_score'] - analysis['quality_score']
        }
    
    def _add_visual_metaphor(self, content: str) -> str:
        """添加视觉隐喻"""
        metaphors = [
            "形成牢笼般的框架",
            "如萤火虫般穿梭",
            "光斑在空中飞舞",
            "光影如流水般流淌"
        ]
        
        # 在合适位置插入
        if '，' in content:
            parts = content.split('，', 1)
            if len(parts) > 1:
                return f"{parts[0]}，{metaphors[0]}。{parts[1]}"
        
        return content
    
    def _add_emotional_detail(self, content: str) -> str:
        """添加情感细节"""
        if '面部' in content or '脸' in content:
            # 在面部描述后添加细节
            content = re.sub(r'(面部|脸)(。|，)', r'\1，皱纹深刻，瞳孔收缩。\2', content)
        
        return content
    
    def _add_environmental_detail(self, content: str) -> str:
        """添加环境细节"""
        if '背景' in content:
            content = re.sub(r'背景([^。]+)(。)', r'背景\1，虚化为柔和的色块。\2', content)
        
        return content
    
    def _add_cinematic_technique(self, content: str) -> str:
        """添加电影技术"""
        techniques = ['浅景深', '低机位', '高角度']
        for tech in techniques:
            if tech not in content:
                content = content + f" {tech}。"
                break
        
        return content
    
    def _add_lighting_effect(self, content: str) -> str:
        """添加光影效果"""
        if '光' in content and '光晕' not in content:
            content = re.sub(r'光([^。]+)(。)', r'光\1，形成光晕。\2', content)
        
        return content
    
    def _add_color_grading(self, content: str) -> str:
        """添加色彩信息"""
        if '色调' not in content and '色彩' not in content:
            content = content + " 精致色调。"
        
        return content
    
    def intelligent_simplify(self, content: str, reduction_target: float = 0.4) -> Dict:
        """智能精简：保留创意核心，精简冗余描述"""
        
        # 分析创意质量
        quality_analysis = self.analyze_creative_quality(content)
        
        # 提取创意核心元素
        creative_elements = self._extract_creative_elements(content)
        
        # 执行智能精简
        simplified_content = self._perform_intelligent_simplification(
            content, 
            creative_elements, 
            reduction_target
        )
        
        # 分析精简后的质量
        new_quality_analysis = self.analyze_creative_quality(simplified_content)
        
        return {
            'original_content': content,
            'simplified_content': simplified_content,
            'original_quality_score': quality_analysis['quality_score'],
            'new_quality_score': new_quality_analysis['quality_score'],
            'quality_change': new_quality_analysis['quality_score'] - quality_analysis['quality_score'],
            'reduction_percentage': reduction_target * 100,
            'preserved_elements': creative_elements,
            'quality_maintained': new_quality_analysis['quality_score'] >= quality_analysis['quality_score'] * 0.9
        }
    
    def _extract_creative_elements(self, content: str) -> List[str]:
        """提取创意核心元素"""
        elements = []
        
        for category, keywords in self.creative_keywords.items():
            for keyword in keywords:
                if keyword in content:
                    elements.append(keyword)
        
        return elements
    
    def _perform_intelligent_simplification(self, content: str, 
                                         creative_elements: List[str], 
                                         reduction_target: float) -> str:
        """执行智能精简"""
        simplified = content
        
        # 步骤1：移除非核心的修饰词
        non_essential_words = ['非常', '极其', '十分', '特别', '相当', '显得']
        for word in non_essential_words:
            simplified = simplified.replace(word, '')
        
        # 步骤2：合并短句
        simplified = re.sub(r'。\n', '。', simplified)
        simplified = re.sub(r'，\n', '，', simplified)
        simplified = re.sub(r'\n{2,}', '\n', simplified)
        
        # 步骤3：精简重复描述
        simplified = re.sub(r'([^，。]+)，\s*\1', r'\1', simplified)
        
        # 步骤4：确保创意元素完整保留
        # 检查所有创意元素是否还在
        for element in creative_elements:
            if element not in simplified:
                # 如果丢失了创意元素，从原文中找回
                original_pos = content.find(element)
                if original_pos != -1:
                    context = content[max(0, original_pos-20):original_pos+20]
                    simplified += ' ' + context
        
        # 步骤5：移除括号注释
        simplified = re.sub(r'（.*?）', '', simplified)
        simplified = re.sub(r'【.*?】', '', simplified)
        
        return simplified.strip()

if __name__ == "__main__":
    # 测试创意质量改进器
    improver = CreativeQualityImprover()
    
    # 测试案例1：温馨回忆场景
    test_content = """特写，老人的面容。
他望向雨水划过的窗户，眼中闪着未落的泪光，嘴角却浮现一丝温柔的微笑。手中握着一张老照片，手指轻轻描摹着边缘。
黄金时段的柔光透过窗户，温暖她的面容，在凌乱的发丝上晕出光晕。
背景是温馨的客厅和书架，85mm镜头虚化成柔和的色块。
苦涩而温柔，私密的回忆时刻。"""
    
    # 分析创意质量
    analysis = improver.analyze_creative_quality(test_content)
    print(f"创意质量分数: {analysis['quality_score']}")
    print(f"创意元素总数: {analysis['total_elements']}")
    print(f"缺失元素: {analysis['missing_elements']}")
    
    # 测试智能精简
    result = improver.intelligent_simplify(test_content, reduction_target=0.3)
    print(f"\n智能精简结果:")
    print(f"原始质量: {result['original_quality_score']}")
    print(f"精简后质量: {result['new_quality_score']}")
    print(f"质量变化: {result['quality_change']}")
    print(f"质量维持: {result['quality_maintained']}")
    print(f"\n精简后内容:\n{result['simplified_content']}")