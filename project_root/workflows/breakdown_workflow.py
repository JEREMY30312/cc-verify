> **Description:** 节拍拆解工作流程编排脚本，协调颗粒度重组、权重计算和策略标签生成

#!/usr/bin/env python3
"""
节拍拆解工作流程 V4.1
完整的breakdown流程编排
"""

import json
import sys
sys.path.append('../tools')
from weight_calculator import calculate_weight
from strategy_mapper import generate_strategy_tags, calculate_suggested_grids

class BreakdownWorkflow:
    """节拍拆解工作流编排器"""
    
    def __init__(self, script_content, project_config):
        self.script = script_content
        self.config = project_config
        self.genre = project_config.get('genre', 'action')
    
    def step_0_granularity_reorg(self, beats):
        """步骤0: 颗粒度重组（一拍一策）"""
        # 检测需要拆分的节拍
        reorganized = []
        for beat in beats:
            # 检测条件：对话密度>30%且时长>15秒、包含3个以上动作动词等
            if self._should_split(beat):
                sub_beats = self._split_beat(beat)
                reorganized.extend(sub_beats)
            else:
                reorganized.append(beat)
        return reorganized
    
    def step_1_weight_analysis(self, beat):
        """步骤1: 戏剧权重分析"""
        event_type = beat['event_type']
        narrative_func = beat['narrative_function']
        complexity = beat.get('complexity_score', 2.5)
        
        weight_result = calculate_weight(
            event_type, self.genre, narrative_func, complexity
        )
        
        return weight_result
    
    def step_2_strategy_generation(self, beat, weight_result):
        """步骤2: 策略标签生成"""
        tags = generate_strategy_tags(
            beat['event_type'], 
            weight_result['final_weight'],
            beat.get('complexity_score', 2.5)
        )
        
        grids = calculate_suggested_grids(
            tags,
            beat.get('complexity_score', 2.5)
        )
        
        return {
            "strategy_tags": tags,
            "suggested_grids": grids
        }
    
    def execute(self):
        """执行完整流程"""
        # 1. 识别最小叙事单元
        beats = self._identify_beats(self.script)
        
        # 2. 颗粒度重组
        beats = self.step_0_granularity_reorg(beats)
        
        # 3. 对每个节拍执行分析和策略生成
        results = []
        for beat in beats:
            weight = self.step_1_weight_analysis(beat)
            strategy = self.step_2_strategy_generation(beat, weight)
            
            result = {
                **beat,
                **weight,
                **strategy
            }
            results.append(result)
        
        return results
    
    def _should_split(self, beat):
        """检测是否需要拆分"""
        # 简化版检测逻辑
        return False
    
    def _split_beat(self, beat):
        """拆分节拍"""
        return [beat]
    
    def _identify_beats(self, script):
        """从剧本识别节拍（简化版）"""
        return []

if __name__ == "__main__":
    workflow = BreakdownWorkflow("测试剧本", {"genre": "action"})
    results = workflow.execute()
    print(json.dumps(results, ensure_ascii=False, indent=2))
