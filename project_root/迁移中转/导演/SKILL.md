---
name: storyboard-review-skill
description: 分镜审核技能。用于审核分镜师产出的节拍拆解、九宫格提示词、四宫格提示词，以及动画师产出的动态提示词，确保符合方法论标准。支持三种审核状态：PASS、FAIL、UNCERTAIN。
---

# 分镜审核技能

[技能说明]
    分镜审核技能，用于审核分镜师和动画师产出是否符合方法论标准。审核前必须先读取上游产物建立整体理解，再按 review-checklist.md 逐项检查。支持三种审核状态：
    - PASS：全部验收项通过
    - FAIL：存在必须修改的问题
    - UNCERTAIN：存在不确定项，需要用户决策

[文件结构]
    storyboard-review-skill/
    ├── storyboard-review-skill/               # 审核技能核心（已拆分）
    │   ├── index.md                           # 入口文件
    │   ├── 01-skill-overview.md               # 技能说明与文件结构
    │   ├── 02-review-functions.md             # 审核功能详解
    │   ├── 03-output-format.md                # 输出格式规范
    │   └── 04-notes.md                       # 注意事项与版本记录
    ├── review-checklist.md                    # 验收清单（检查项列表）
    ├── storyboard-methodology-playbook/       # 分镜方法论（已拆分到独立文件夹）
    ├── motion-prompt-methodology/             # 动态提示词方法论（已拆分到独立文件夹）
    ├── uncertainty-judgment-protocol.md       # 不确定项判定协议
    ├── asset-consistency-rules.md             # 资产一致性规则库
    └── templates/                             # 审核报告模板目录（可选）

[基准文档]
    分镜审核基准：
    - review-checklist.md
    - storyboard-methodology-playbook/（分镜判定标准）
    - asset-consistency-rules.md

    动态提示词审核基准：
    - review-checklist.md
    - motion-prompt-methodology/

    不确定项判定基准：
    - uncertainty-judgment-protocol.md

[功能]
    [审核节拍拆解]
        步骤0: JSON 数据完整性验证 [V4.1-CRITICAL]
            - 验证 JSON: outputs/scene-breakdown-{集数}.json 存在
            - 验证 shots数组非空且长度在 8-50 之间
            - 验证每个shot包含必填字段：
              - shot_id, ndi_score, shot_type, motivation
              - axis_side, relay_point（如适用）
            - 验证 NDI分布合理（至少包含高、中、低三种类型）
            - ⚠️ 任一检查失败 → 审核状态 = FAIL
            - ⚠️ 错误信息："JSON 缺失或字段不完整，要求重新执行 /breakdown"
<!-- LOG:STEP read=outputs/scene-breakdown-{集数}.json,algorithm=json_validation,check=shots_count,check=required_fields,status=critical -->

        第一步：建立整体理解
            - 读取 script/（剧本原文）

        第二步：读取基准
            - 读取 review-checklist.md → 节拍拆解验收
            - 读取 storyboard-methodology-playbook/index.md
<!-- LOG:STEP read=.claude/skills/storyboard-review-skill/review-checklist.md,.claude/skills/storyboard-review-skill/storyboard-methodology-playbook/index.md,module=review_standards,checklist=breakdown -->

        第三步：读取待审核内容
            - 读取 outputs/beat-breakdown.md

        第四步：逐项检查
            - 按照 review-checklist.md 中的"节拍拆解验收"逐项检查
            - 检查"核心策略"字段是否正确填写
            - 检查"关键信息点"和"辅助信息"是否完整
            - 检查"复杂度评分"和"建议格子数"是否合理
<!-- LOG:STEP algorithm=review_checklist,check_items_count=25,output=review_status,checklist=breakdown_review -->
            
        第四点五步：新增审核维度检查
            - 调用 asset-consistency-rules.md → 资产一致性审核（如适用）
            
        第四点六步：不确定项判定
            - 调用 uncertainty-judgment-protocol.md
            - 识别潜在不确定项
            - 生成决策选项

        第五步：输出结果
            - 无问题 → PASS
            - 有必须修改问题 → FAIL
            - 有不确项 → UNCERTAIN

    [审核 Beat Board 九宫格提示词]
        步骤0: JSON 数据完整性验证 [V4.1-CRITICAL]
            - 验证 JSON: outputs/scene-breakdown-{集数}.json 存在
            - 验证 JSON: outputs/beat-board-full-list-{集数}.json 存在
            - 验证 grids数组长度 = 9
            - 验证每个grid：
              - grid_id, beat_number包含必填字段, keyframe_level
              - inheritance（如存在）
            - 验证 waterfall_shots映射准确（🔵和⚪级别镜头）
            - ⚠️ 任一检查失败 → 审核状态 = FAIL
            - ⚠️ 错误信息："JSON 缺失或字段不完整，要求重新执行 /beatboard"
<!-- LOG:STEP read=outputs/scene-breakdown-{集数}.json,outputs/beat-board-full-list-{集数}.json,algorithm=json_validation,check=grids_count,status=critical -->

        第一步：建立整体理解
            - 读取 script/（剧本原文）
            - 读取 outputs/beat-breakdown.md（节拍拆解）

        第二步：读取基准
            - 读取 review-checklist.md → Beat Board 验收
            - 读取 storyboard-methodology-playbook/index.md
<!-- LOG:STEP read=.claude/skills/storyboard-review-skill/review-checklist.md,.claude/skills/storyboard-review-skill/storyboard-methodology-playbook/index.md,module=review_standards,checklist=beatboard -->

        第三步：读取待审核内容
            - 读取 outputs/beat-board-prompt.md

        第四步：逐项检查
            - 按照 review-checklist.md 中的"Beat Board 验收"逐项检查
            - 检查是否继承了节拍拆解的"关键信息点"和"辅助信息"
            - 检查引擎输出摘要是否完整
<!-- LOG:STEP algorithm=review_checklist,check_items_count=30,output=review_status,checklist=beatboard_review -->
            
        第四点五步：新增审核维度检查
            - 调用 asset-consistency-rules.md → 资产一致性审核
            - 执行关键帧合理性审核（基于 review-checklist.md 新增维度B）
            - 执行创意融合度审核（基于 review-checklist.md 新增维度C）
            
        第四点六步：不确定项判定
            - 调用 uncertainty-judgment-protocol.md
            - 识别潜在不确定项
            - 生成决策选项

        第五步：输出结果
            - 无问题 → PASS
            - 有必须修改问题 → FAIL
            - 有不确项 → UNCERTAIN

    [审核 Sequence Board 四宫格提示词]
        步骤0: JSON 数据完整性验证 [V4.1-CRITICAL]
            - 验证 JSON: outputs/scene-breakdown-{集数}.json 存在
            - 验证 JSON: outputs/beat-board-full-list-{集数}.json 存在
            - 验证 JSON: outputs/sequence-board-data-{集数}.json 存在
            - 验证 boards数组与 Markdown 文件数量一致
            - 验证每个card包含必填字段：
              - card_id, strategy_tags, camera_info
            - 验证 cross_grid_continuity评分 ≥ 80
            - 验证 策略覆盖率 ≥ 95%
            - ⚠️ 任一检查失败 → 审核状态 = FAIL
            - ⚠️ 错误信息："JSON 缺失或字段不完整，要求重新执行 /sequence"
<!-- LOG:STEP read=outputs/scene-breakdown-{集数}.json,outputs/beat-board-full-list-{集数}.json,outputs/sequence-board-data-{集数}.json,algorithm=json_validation,check=boards_count,check=cards_count,status=critical -->

        第一步：建立整体理解
            - 读取 script/（剧本原文）
            - 读取 outputs/beat-breakdown.md（节拍拆解）
            - 读取 outputs/beat-board-prompt.md（九宫格提示词）

        第二步：读取基准
            - 读取 review-checklist.md → Sequence Board 验收
            - 读取 storyboard-methodology-playbook/index.md
<!-- LOG:STEP read=.claude/skills/storyboard-review-skill/review-checklist.md,.claude/skills/storyboard-review-skill/storyboard-methodology-playbook/index.md,module=review_standards,checklist=sequence -->

        第三步：读取待审核内容
            - 读取 outputs/sequence-board-prompt.md

        第四步：逐项检查
            - 按照 review-checklist.md 中的"Sequence Board 验收"逐项检查
            - 重点检查与九宫格的一致性继承
            - 检查是否正确使用了"核心策略"进行格子数分配
            - 检查是否继承了"关键信息点"和"辅助信息"
            - 检查跨板连贯性是否正确处理
<!-- LOG:STEP algorithm=review_checklist,check_items_count=35,output=review_status,checklist=sequence_review -->
            
        第四点五步：新增审核维度检查
            - 调用 asset-consistency-rules.md → 资产一致性审核
            - 执行关键帧合理性审核（基于 review-checklist.md 新增维度B）
            - 执行创意融合度审核（基于 review-checklist.md 新增维度C）
            
        第四点六步：不确定项判定
            - 调用 uncertainty-judgment-protocol.md
            - 识别潜在不确定项
            - 生成决策选项

        第五步：输出结果
            - 无问题 → PASS
            - 有必须修改问题 → FAIL
            - 有不确项 → UNCERTAIN

    [审核 Motion Prompt 动态提示词]
        步骤0: JSON 数据完整性验证 [V4.1-CRITICAL]
            - 验证 JSON: outputs/scene-breakdown-{集数}.json 存在
            - 验证 JSON: outputs/sequence-board-data-{集数}.json 存在
            - 验证 JSON: outputs/motion-prompt-data-{集数}.json 存在
            - 验证 motion_groups数量 = 9（每组对应一个九宫格）
            - 验证每组包含 5 个 Motion Prompt（1关键帧+4四宫格）
            - 验证 physics_verification统计完整
            - 验证 五模块合规性 = 100%
            - ⚠️ 任一检查失败 → 审核状态 = FAIL
            - ⚠️ 错误信息："JSON 缺失或字段不完整，要求重新执行 /motion"
<!-- LOG:STEP read=outputs/scene-breakdown-{集数}.json,outputs/sequence-board-data-{集数}.json,outputs/motion-prompt-data-{集数}.json,algorithm=json_validation,check=motion_groups,status=critical -->

        第一步：建立整体理解
            - 读取 script/（剧本原文）
            - 读取 outputs/beat-breakdown.md（节拍拆解）
            - 读取 outputs/beat-board-prompt.md（九宫格提示词）
            - 读取 outputs/sequence-board-prompt.md（四宫格提示词）

        第二步：读取基准
            - 读取 review-checklist.md → Motion Prompt 验收
            - 读取 motion-prompt-methodology/index.md
<!-- LOG:STEP read=.claude/skills/storyboard-review-skill/review-checklist.md,.claude/skills/storyboard-review-skill/motion-prompt-methodology/index.md,module=review_standards,checklist=motion -->

        第三步：读取待审核内容
            - 读取 outputs/motion-prompt.md

        第四步：逐项检查
            - 按照 review-checklist.md 中的"Motion Prompt 验收"逐项检查
            - 重点检查动作是否与分镜匹配
<!-- LOG:STEP algorithm=review_checklist,physics_verification,check_items_count=40,output=review_status,checklist=motion_review,note=包含物理验证 -->
            
        第四点五步：新增审核维度检查
            - 执行关键帧合理性审核（基于 review-checklist.md 新增维度B）
            - 执行创意融合度审核（基于 review-checklist.md 新增维度C）
            
        第四点六步：不确定项判定
            - 调用 uncertainty-judgment-protocol.md
            - 识别潜在不确定项
            - 生成决策选项

        第五步：输出结果
            - 无问题 → PASS
            - 有必须修改问题 → FAIL
            - 有不确项 → UNCERTAIN

    [整体交付审核]
        第一步：建立整体理解
            - 读取 script/（剧本原文）
            - 读取 outputs/beat-breakdown.md（节拍拆解）
            - 读取 outputs/beat-board-prompt.md（九宫格提示词）
            - 读取 outputs/sequence-board-prompt.md（四宫格提示词）
            - 读取 outputs/motion-prompt.md（动态提示词）

        第二步：读取基准
            - 读取 review-checklist.md → 最终交付验收
            - 读取 storyboard-methodology-playbook/index.md → [规则库]
            - 读取 motion-prompt-methodology/index.md → [验收清单]
            - 读取 asset-consistency-rules.md → 资产一致性规则

        第三步：逐项检查
            - 按照 review-checklist.md 中的"最终交付验收"逐项检查
            
        第四步：新增审核维度检查
            - 调用 asset-consistency-rules.md → 完整资产一致性审核
            - 执行关键帧合理性审核（基于 review-checklist.md 新增维度B）
            - 执行创意融合度审核（基于 review-checklist.md 新增维度C）
            
        第五步：不确定项判定
            - 调用 uncertainty-judgment-protocol.md
            - 识别潜在不确定项
            - 生成决策选项

        第六步：输出结果
            - 无问题 → PASS
            - 有必须修改问题 → FAIL
            - 有不确项 → UNCERTAIN

[注意事项]
    - 审核前必须先读取上游产物，建立整体理解
    - 审核分镜内容时使用 storyboard-methodology-playbook/ 作为判定依据
    - 审核动态提示词时使用 motion-prompt-methodology/ 作为判定依据
    - 资产一致性审核使用 asset-consistency-rules.md 作为判定依据
    - 不确定项判定使用 uncertainty-judgment-protocol.md 作为判定依据
    - 审核必须基于 review-checklist.md，不能随意增减标准
    - 问题描述必须具体到位置，不能泛泛而谈
    - 只有全部验收项通过且无不确项才能输出 PASS
    - UNCERTAIN 状态需要等待用户决策后才能继续流程

[版本变更记录]
    v2.0 (当前版本)
    - 新增资产一致性审核维度
    - 新增关键帧合理性审核维度
    - 新增创意融合度审核维度
    - 新增不确定项判定机制
    - 支持三种审核状态：PASS、FAIL、UNCERTAIN
    - 更新文件结构，方法论文件已拆分到独立文件夹

    v1.0 (初始版本)
    - 基础审核功能
    - 仅支持PASS/FAIL两种状态
    - 基于review-checklist.md的基本验收项
