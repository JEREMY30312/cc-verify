# 导演决策记录 Director Decision

[功能]
    记录导演在流程中的决策，包括预设参数和审核意见

[决策参数预设]
    yaml
    director_presets:
      project_name: "项目名称"
      episode: "ep01"
      visual_style: "国潮动漫风格"
      
      # 关键帧选择偏好
      selection_preferences:
        mandatory_levels: ["🔴"]           # 必须入选的等级
        optional_levels: ["🟠"]            # 可选入选的等级
        max_frames: 50                    # 最多关键帧数
        min_frames: 10                  # 最少关键帧数
      
      # 布局偏好
      layout_preferences:
        default_layout: "3×3标准网格"
        allow_special_layouts: true
        min_frames_for_2x2: 3
        max_boards_per_episode: 10
      
      # 视觉叙事偏好
      narrative_preferences:
        focus_on_action: true
        emotion_intensity: "中高"
        pacing: "快节奏"

[决策记录格式]
    markdown
    ## 导演决策记录

    ### 板号：board03
    - **创建时间**：2024-01-20 14:30
    - **关键帧数量**：7/9
    - **布局类型**：2×2聚焦网格（覆盖系统建议的3×3）

    ### 选择理由
    - **叙事考量**：需要突出主角的情感转变，减少环境干扰
    - **视觉考量**：聚焦于面部表情和肢体语言
    - **节奏考量**：此处需要放缓节奏，让观众感受情绪变化

    ### 特殊指示
    - **传递给四宫格**：重点处理眼神光的变化和泪水反射
    - **传递给动态提示词**：强调微表情的连续性
    - **制作注意**：此板为情感高潮，建议增加10%制作时间

    ### 审核状态
    - **导演审核**：✅ 已通过（张导演，14:35）
    - **用户审核**：⏳ 待审核
    - **修改记录**：无

[审核流程]
    1. 系统自动生成初版
    2. 导演审核并调整
    3. 用户审核确认
    4. 版本锁定
    5. 修改追踪

[使用方式]
    直接读取此文件，按格式记录导演决策
