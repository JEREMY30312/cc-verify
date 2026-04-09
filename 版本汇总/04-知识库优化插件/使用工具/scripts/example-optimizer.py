#!/usr/bin/env python3
"""
示例文件精简优化脚本
安全精简03-examples.md，提取规则，保留黄金示例
"""

import re
import json
import os
from pathlib import Path
from typing import Dict, List, Tuple

class ExampleOptimizer:
    def __init__(self, input_file: str):
        self.input_file = input_file
        self.content = Path(input_file).read_text(encoding='utf-8')
        self.examples = self._parse_examples()
        
    def _parse_examples(self) -> List[Dict]:
        """解析Markdown中的示例"""
        examples = []
        
        # 匹配示例标题和内容
        pattern = r'## 示例(\d+)：(.*?)\n\*\*模板类型：\*\* (.*?)\n\n(.*?)(?=\n## 示例|\n## 影视术语|$)'
        matches = re.findall(pattern, self.content, re.DOTALL)
        
        for match in matches:
            example_id, title, template_type, content = match
            examples.append({
                'id': int(example_id),
                'title': title.strip(),
                'template_type': template_type.strip(),
                'content': content.strip(),
                'word_count': len(content.split())
            })
            
        return examples
    
    def select_golden_examples(self) -> List[int]:
        """选择3个黄金示例"""
        # 基于使用频率、教学价值、类型覆盖度选择
        golden_ids = [1, 4, 7]  # 紧张对峙、动作高潮、压迫与威胁
        return golden_ids
    
    def extract_rules_from_example(self, example: Dict) -> Dict:
        """从示例中提取规则"""
        rules = {
            'id': example['id'],
            'title': example['title'],
            'template_type': example['template_type'],
            'framing_rule': '',
            'lighting_rule': '',
            'color_rule': '',
            'emotion_rule': '',
            'camera_rule': ''
        }
        
        content = example['content']
        
        # 提取景别信息
        if '中景' in content:
            rules['framing_rule'] = '中景，适合表现人物关系'
        elif '特写' in content:
            rules['framing_rule'] = '特写，强调情感细节'
        elif '极远景' in content:
            rules['framing_rule'] = '极远景，表现环境与人物关系'
            
        # 提取光线信息
        if '冷蓝色调' in content or '冷蓝绿色调' in content:
            rules['color_rule'] = '冷色调，营造紧张/悬疑氛围'
        elif '黄金时段' in content or '温暖' in content:
            rules['color_rule'] = '暖色调，表现温馨/怀旧情绪'
            
        # 提取情绪关键词
        emotion_keywords = ['紧张', '温馨', '孤独', '爆发', '恐惧', '敬畏', '压迫']
        for keyword in emotion_keywords:
            if keyword in content:
                rules['emotion_rule'] = f'核心情绪：{keyword}'
                break
                
        return rules
    
    def simplify_example(self, example: Dict) -> str:
        """精简示例内容"""
        content = example['content']
        
        # 移除冗余描述
        simplifications = [
            (r'。\n', '。'),  # 合并短句
            (r'，\n', '，'),
            (r'\n{2,}', '\n'),  # 减少空行
            (r'（.*?）', ''),  # 移除括号注释
            (r'【.*?】', ''),
        ]
        
        for pattern, replacement in simplifications:
            content = re.sub(pattern, replacement, content)
            
        # 压缩重复词汇
        compression_rules = [
            (r'显得\s+', ''),
            (r'非常\s+', ''),
            (r'极为\s+', ''),
            (r'充满了\s+', '充满'),
        ]
        
        for pattern, replacement in compression_rules:
            content = re.sub(pattern, replacement, content)
            
        return content.strip()
    
    def create_knowledge_base_entry(self, example: Dict, rules: Dict) -> Dict:
        """创建知识库条目"""
        return {
            'example_id': example['id'],
            'title': example['title'],
            'full_content': example['content'],
            'simplified_content': self.simplify_example(example),
            'extracted_rules': rules,
            'keywords': self.extract_keywords(example['content']),
            'applicable_templates': [example['template_type']],
            'retention_priority': 'high' if example['id'] in [1, 4, 7] else 'medium'
        }
    
    def extract_keywords(self, content: str) -> List[str]:
        """提取关键词"""
        keywords = []
        
        # 影视术语关键词
        cinematic_terms = ['中景', '特写', '远景', '仰拍', '俯拍', '侧光', '逆光', 
                          '冷色调', '暖色调', '低饱和', '高对比', '浅景深']
        
        for term in cinematic_terms:
            if term in content:
                keywords.append(term)
                
        return list(set(keywords))
    
    def optimize(self):
        """执行完整优化流程"""
        print(f"开始优化 {self.input_file}")
        print(f"找到 {len(self.examples)} 个示例")
        
        # 选择黄金示例
        golden_ids = self.select_golden_examples()
        print(f"选择黄金示例: {golden_ids}")
        
        # 处理每个示例
        optimized_examples = []
        knowledge_base_entries = []
        
        for example in self.examples:
            # 提取规则
            rules = self.extract_rules_from_example(example)
            
            # 创建知识库条目
            kb_entry = self.create_knowledge_base_entry(example, rules)
            knowledge_base_entries.append(kb_entry)
            
            # 如果是黄金示例，生成精简版
            if example['id'] in golden_ids:
                simplified = self.simplify_example(example)
                optimized_examples.append({
                    'id': example['id'],
                    'title': example['title'],
                    'original_content': example['content'],
                    'simplified_content': simplified,
                    'word_count_reduction': example['word_count'] - len(simplified.split()),
                    'reduction_percentage': round((example['word_count'] - len(simplified.split())) / example['word_count'] * 100, 1)
                })
        
        return {
            'optimized_examples': optimized_examples,
            'knowledge_base_entries': knowledge_base_entries,
            'summary': {
                'total_examples': len(self.examples),
                'golden_examples': len(golden_ids),
                'moved_to_kb': len(self.examples) - len(golden_ids)
            }
        }

if __name__ == "__main__":
    optimizer = ExampleOptimizer("03-examples.md")
    results = optimizer.optimize()
    
    # 保存结果
    with open('tests/example-verification/results/optimization_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print("\n优化完成！")
    print(f"优化结果保存至: tests/example-verification/results/optimization_results.json")