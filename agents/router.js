#!/usr/bin/env node

/**
 * ANINEO Agent 路由模块 v3.0（轻量化版）
 * 
 * 负责解析用户指令，路由到对应的子 Agent
 * 按 SKILL.md 定义的完整工作流程执行
 * 
 * 轻量化特性：
 * - 智能引导从 router.js 动态生成（零维护）
 * - 欢迎消息和状态检测自动从 .agent-state.json 读取
 * 
 * 使用方式：
 *   node router.js "/breakdown ep01"
 *   node router.js "/beatboard"
 */

const path = require('path');
const fs = require('fs');

// 指令路由表
const ROUTING_TABLE = {
    // 启动指令
    '/start': { 
        agent: 'producer', 
        task: 'start',
        description: '启动欢迎（动态生成）'
    },
    // 主指令
    '/breakdown': { 
        agent: 'storyboard-artist', 
        task: 'breakdown',
        description: '节拍拆解'
    },
    '/beatboard': { 
        agent: 'storyboard-artist', 
        task: 'beatboard',
        description: '九宫格提示词'
    },
    '/sequence': { 
        agent: 'storyboard-artist', 
        task: 'sequence',
        description: '四宫格提示词'
    },
    '/motion': { 
        agent: 'animator', 
        task: 'motion',
        description: '动态提示词'
    },
    '/interactive': { 
        agent: 'producer', 
        task: 'interactive',
        description: '交互式配置向导'
    },
    '/status': { 
        agent: 'producer', 
        task: 'status',
        description: '项目状态检测（动态生成）'
    },
    '/help': { 
        agent: 'producer', 
        task: 'help',
        description: '显示帮助信息'
    },
    
    // 带参数的指令变体
    '/breakdown': { 
        agent: 'storyboard-artist', 
        task: 'breakdown',
        description: '节拍拆解（可带集数参数）'
    },
    '/beatboard': { 
        agent: 'storyboard-artist', 
        task: 'beatboard',
        description: '九宫格提示词（可带集数参数）'
    },
    '/sequence': { 
        agent: 'storyboard-artist', 
        task: 'sequence',
        description: '四宫格提示词（可带集数参数）'
    },
    '/motion': { 
        agent: 'animator', 
        task: 'motion',
        description: '动态提示词（可带集数参数）'
    },
    
    // 创意指令
    '/creative': {
        agent: 'storyboard-artist',
        task: 'creative',
        description: '添加创意指令'
    },
    
    // 管理指令
    '/snapshot': {
        agent: 'producer',
        task: 'snapshot_menu',
        description: '快照管理（显示菜单）'
    },
    '/snapshot list': {
        agent: 'producer',
        task: 'snapshot_list',
        description: '列出所有快照'
    },
    '/snapshot preview': {
        agent: 'producer',
        task: 'snapshot_preview',
        description: '预览指定快照'
    },
    '/snapshot rollback': {
        agent: 'producer',
        task: 'snapshot_rollback',
        description: '回滚到指定快照'
    },
    '/snapshot create': {
        agent: 'producer',
        task: 'snapshot_create',
        description: '创建快照'
    },
    
    // 审核指令
    '/review': {
        agent: 'director',
        task: 'review',
        description: '审核产出'
    }
};

// 集数正则
const EPISODE_REGEX = /(ep\d{2}|ch\d{2})/i;

// 模块依赖配置 - 按 SKILL.md 定义
const MODULE_DEPENDENCIES = {
    breakdown: [
        'common/beat-analyzer.md',
        'film-storyboard-skill/templates/beat-breakdown-template.md',
        'common/quality-check.md',
        'common/director-decision.md'
    ],
    beatboard: [
        'common/keyframe-selector.md',
        'common/layout-calculator.md',
        'film-storyboard-skill/templates/beat-board-template.md',
        'common/coherence-checker.md'
    ],
    sequence: [
        'common/coherence-checker.md',
        'film-storyboard-skill/templates/sequence-board-template.md'
    ],
    motion: [
        'animator-skill/motion-prompt-methodology/index.md',
        'animator-skill/physics-verification-rules.md',
        'animator-skill/templates/motion-prompt-template.md'
    ],
    creative: [
        'film-storyboard-skill/creative-engines-integration/index.md'
    ],
    review: [
        'storyboard-review-skill/review-checklist.md',
        'storyboard-review-skill/uncertainty-judgment-protocol.md',
        'storyboard-review-skill/asset-consistency-rules.md'
    ]
};

// 协议文件配置
const PROTOCOL_FILES = {
    userConfirmation: 'common/user-confirmation-protocol.md',
    snapshotManagement: 'common/snapshot-management.md',
    informationFlow: 'common/信息传递机制.md',
    collaborationMode: 'common/协作模式.md'
};

// ============================================================================
// 轻量化：智能引导函数（从 router.js 动态生成，无需外部文档）
// ============================================================================

/**
 * 读取项目状态
 * @returns {object} 项目状态对象
 */
function getProjectState() {
    const stateFile = '.agent-state.json';
    if (!fs.existsSync(stateFile)) {
        return { 
            initialized: false,
            currentEpisode: 'ep01'
        };
    }
    
    try {
        const state = JSON.parse(fs.readFileSync(stateFile, 'utf8'));
        return {
            initialized: !!state.project_config,
            config: state.project_config || null,
            phases: state.phases || {},
            currentEpisode: state.current_episode || 'ep01',
            lastPhase: state.last_phase || null,
            subagents: state.subagents || {
                "storyboard-artist": { agentId: null, status: "not_created" },
                "director": { agentId: null, status: "not_created" },
                "animator": { agentId: null, status: "not_created" }
            }
        };
    } catch (e) {
        return { 
            initialized: false,
            currentEpisode: 'ep01',
            subagents: {
                "storyboard-artist": { agentId: null, status: "not_created" },
                "director": { agentId: null, status: "not_created" },
                "animator": { agentId: null, status: "not_created" }
            }
        };
    }
}

/**
 * 检测下一个需要执行的阶段
 * @param {object} phases - 阶段状态对象
 * @returns {string} 下一阶段名称
 */
function detectNextPhase(phases) {
    // 注意：.agent-state.json 中的字段名是 beat-breakdown, beatboard 等（带连字符）
    // 不是 beat_breakdown（下划线）
    if (!phases || !phases['beat-breakdown'] || phases['beat-breakdown'].status !== 'completed') {
        return 'breakdown';
    }
    if (!phases.beatboard || phases.beatboard.status !== 'completed') {
        return 'beatboard';
    }
    if (!phases.sequence || phases.sequence.status !== 'completed') {
        return 'sequence';
    }
    if (!phases.motion || phases.motion.status !== 'completed') {
        return 'motion';
    }
    return 'all_complete';
}

/**
 * 生成欢迎消息
 * @param {object} state - 项目状态
 * @returns {string} 欢迎消息
 */
function generateWelcomeMessage(state) {
    const ep = state.currentEpisode || 'ep01';
    
    if (!state.initialized) {
        return `👋 欢迎使用 ANINEO！

📝 检测到新项目，尚未配置。

🎯 建议下一步：
/interactive    # 配置项目参数（推荐）
/breakdown ${ep}  # 直接开始（使用默认配置）
`;
    }
    
    const nextPhase = detectNextPhase(state.phases);
    
    const phaseMessages = {
        breakdown: `📊 当前进度：未开始

🎯 建议下一步：
/breakdown ${ep}  # 开始节拍拆解
`,
        beatboard: `📊 当前进度：节拍拆解完成 ✅

🎯 建议下一步：
/beatboard ${ep}  # 生成九宫格提示词
`,
        sequence: `📊 当前进度：九宫格完成 ✅

🎯 建议下一步：
/sequence ${ep}  # 生成四宫格提示词
`,
        motion: `📊 当前进度：四宫格完成 ✅

🎯 建议下一步：
/motion ${ep}  # 生成动态提示词
`,
        all_complete: `🎉 ${ep} 全部完成！

🎯 可选操作：
/creative [指令]  # 添加创意修改
/review all ${ep}  # 审核产出
/breakdown ep02   # 开始下一集
`
    };
    
    return `👋 欢迎回来，ANINEO 已就绪！

当前配置：
- 视觉风格：${state.config.visual_style}
- 目标媒介：${state.config.target_medium}
- 画面比例：${state.config.aspect_ratio}
- 当前集数：${ep}

${phaseMessages[nextPhase]}
`;
}

/**
 * 生成状态报告（/status 命令）
 * @param {object} state - 项目状态
 * @returns {string} 状态报告
 */
function generateStatusReport(state) {
    const ep = state.currentEpisode || 'ep01';
    const nextPhase = detectNextPhase(state.phases);
    
    let progressDetails = '';
    const phasesList = [
        { key: 'beat-breakdown', name: '节拍拆解', icon: '📝' },
        { key: 'beatboard', name: '九宫格提示词', icon: '🎨' },
        { key: 'sequence', name: '四宫格提示词', icon: '🎬' },
        { key: 'motion', name: '动态提示词', icon: '🎭' }
    ];
    
    phasesList.forEach(p => {
        const phase = state.phases[p.key];
        const status = (phase && phase.status === 'completed') ? '✅' : '⏳';
        const date = (phase && phase.completed_at) ? phase.completed_at : '-';
        progressDetails += `| ${p.icon} ${p.name.padEnd(10)} | ${status} | ${date} |\n`;
    });
    
    const nextCommand = {
        breakdown: `/breakdown ${ep}`,
        beatboard: `/beatboard ${ep}`,
        sequence: `/sequence ${ep}`,
        motion: `/motion ${ep}`,
        all_complete: '所有阶段已完成'
    };
    
    return `📊 项目状态报告 - ${ep}

当前配置：
- 视觉风格：${state.config?.visual_style || '未配置'}
- 目标媒介：${state.config?.target_medium || '未配置'}
- 画面比例：${state.config?.aspect_ratio || '未配置'}

完成进度：
| 阶段 | 状态 | 完成时间 |
|------|------|----------|
${progressDetails}
当前阶段：${nextPhase === 'all_complete' ? '🎉 全部完成' : nextPhase}

下一步建议：
\`${nextCommand[nextPhase]}\`

其他命令：
- /status         # 查看此报告
- /start          # 欢迎 + 智能引导
- /interactive    # 重新配置项目
`;
}

// ============================================================================
// 原有函数保持不变
// ============================================================================

/**
 * 解析指令
 * @param {string} input - 用户输入
 * @returns {object} 解析结果
 */
function parseInstruction(input) {
    const trimmed = input.trim();
    const parts = trimmed.split(/\s+/);

    // 支持子命令：/snapshot list -> command = '/snapshot list'
    let command;
    let args;

    // 检查是否是子命令（/snapshot list, /snapshot preview 等）
    if (parts[0] === '/snapshot' && parts.length > 1) {
        const subcommand = parts[1].toLowerCase();
        if (['list', 'preview', 'rollback', 'create'].includes(subcommand)) {
            command = `/snapshot ${subcommand}`;
            // 剩余部分作为参数
            args = parts.slice(2).join(' ');
        } else {
            // 如果不是已知的子命令，则当作普通参数处理
            command = '/snapshot';
            args = parts.slice(1).join(' ');
        }
    } else {
        // 普通命令
        command = parts[0];
        args = parts.slice(1).join(' ');
    }

    // 匹配集数参数
    let episode = null;
    if (args) {
        const match = args.match(EPISODE_REGEX);
        if (match) {
            episode = match[1];
        }
    }

    // 如果没有集数参数，尝试从 command 中提取
    if (!episode) {
        const match = command.match(EPISODE_REGEX);
        if (match) {
            episode = match[1];
        }
    }

    return { command, args, episode };
}

/**
 * 路由到对应 Agent
 * @param {string} input - 用户输入
 * @returns {object} 路由结果
 */
function route(input) {
    const { command, args, episode } = parseInstruction(input);
    
    // 查找路由规则
    let routeInfo = ROUTING_TABLE[command];
    
    // 如果找不到，尝试匹配带参数的变体
    if (!routeInfo) {
        // 检查是否是带集数的指令
        for (const [key, value] of Object.entries(ROUTING_TABLE)) {
            if (command.startsWith(key)) {
                routeInfo = value;
                break;
            }
        }
    }
    
    // 如果还是找不到，返回 null
    if (!routeInfo) {
        return null;
    }
    
    return {
        agent: routeInfo.agent,
        task: routeInfo.task,
        episode: episode,
        originalInput: input,
        description: routeInfo.description
    };
}

/**
 * 获取模块依赖列表
 * @param {string} task - 任务类型
 * @returns {string} 模块依赖字符串
 */
function getModuleDependencies(task) {
    const modules = MODULE_DEPENDENCIES[task] || [];
    return modules.map(m => `- ${m}`).join('\n');
}

/**
 * 构建完整的执行流程
 * @param {string} task - 任务类型
 * @param {string} episode - 集数
 * @returns {string} 完整执行流程
 */
function buildExecutionFlow(task, episode) {
    const episodeDefault = episode || 'ep01';
    
    // 根据任务类型构建不同的工作流程
    const workflows = {
        breakdown: `
## 节拍拆解工作流程

### 步骤1: 读取项目配置
- 读取 .agent-state.json
- 获取: visual_style, target_medium, aspect_ratio, episode_id

### 步骤2: 读取输入文件
- 读取剧本文件: script/*-${episodeDefault}.md
- 读取导演参数: common/director-decision.md（如存在）

### 步骤3: 读取分析模块
- 读取 common/beat-analyzer.md ← 核心节拍分析逻辑
- 读取 film-storyboard-skill/templates/beat-breakdown-template.md ← 输出格式模板
- 读取 common/quality-check.md ← 质量检查清单

### 步骤4: 执行节拍分析
按 beat-analyzer.md 规则执行:
- 三幕结构比例: 15-25% / 50-70% / 15-25%
- 节拍数量: 8-12个为宜
- 每个节拍必须包含: 场景描述、角色行动、情感表达
- 计算综合权重和关键帧等级

### 步骤5: 执行质量自检
按 quality-check.md 逐项检查:
□ 三幕比例符合标准
□ 节拍数量在 8-12 范围内
□ 叙事完整性（有开篇、发展、高潮、结局）
□ 每个节拍有明确的场景描述
□ 每个节拍有清晰的角色行动
□ 每个节拍有具体的情感表达

### 步骤6: 保存输出文件
- 保存到: outputs/beat-breakdown-${episodeDefault}.md
`,
        beatboard: `
## 九宫格提示词工作流程

### 步骤1: 读取前置产物
- 读取 outputs/beat-breakdown-${episodeDefault}.md（节拍拆解表）
- 读取 .agent-state.json 获取项目配置

### 步骤2: 读取分析模块
- 读取 common/keyframe-selector.md ← 关键帧选择逻辑
- 读取 common/layout-calculator.md ← 布局计算逻辑
- 读取 film-storyboard-skill/templates/beat-board-template.md ← 输出格式模板
- 读取 common/coherence-checker.md ← 连贯性检查

### 步骤3: 执行关键帧选择
按 keyframe-selector.md 规则执行:
- 从节拍拆解中选择关键帧
- 动态扩展：每检测到1个氛围转折点 → 增加1个关键帧
- 动作强化：重大动作节拍可拆分为2-3个关键帧

### 步骤4: 计算布局
按 layout-calculator.md 规则执行:
- 计算每板关键帧数量
- 确定分板数（每板9格）
- 布局类型选择

### 步骤5: 生成九宫格提示词
按 beat-board-template.md 格式生成:
- 每板9个格子的详细提示词
- 继承节拍拆解的视觉风格和角色设定

### 步骤6: 执行连贯性检查
按 coherence-checker.md 逐项检查:
□ 角色外观一致性
□ 服装状态连续性
□ 光线/时间连续性
□ 空间关系稳定性

### 步骤7: 保存输出文件
- 总览文件: outputs/beat-board-prompt-${episodeDefault}.md
- 分板文件: outputs/beat-board-prompt-${episodeDefault}-board{##}.md
`,
        sequence: `
## 四宫格提示词工作流程

### 步骤1: 读取前置产物
- 读取 outputs/beat-board-prompt-${episodeDefault}.md（九宫格总览）
- 读取 outputs/beat-board-prompt-${episodeDefault}-board*.md（九宫格分板）
- 读取 .agent-state.json 获取项目配置

### 步骤2: 读取分析模块
- 读取 common/coherence-checker.md ← 连贯性检查
- 读取 film-storyboard-skill/templates/sequence-board-template.md ← 输出格式模板

### 步骤3: 继承九宫格要素
每个四宫格必须继承对应九宫格格子的:
- 人物外观/服装状态
- 场景要素/环境设定
- 光色基调/氛围

### 步骤4: 生成四宫格提示词
按 sequence-board-template.md 格式生成:
- 起承转合结构（起→承→转→合）
- 每格包含：镜头类型、画面要素、情绪基调
- 变化必须显式说明原因

### 步骤5: 执行连贯性检查
按 coherence-checker.md 逐项检查:
□ 与九宫格的一致性继承
□ 屏幕方向/视线/轴线稳定
□ 动作连续性
□ 剪接风险检查

### 步骤6: 保存输出文件
- 保存到: outputs/sequence-board-prompt-${episodeDefault}.md
`,
        motion: `
## 动态提示词工作流程

### 步骤1: 读取前置产物
- 读取 outputs/sequence-board-prompt-${episodeDefault}.md（四宫格提示词）
- 读取 outputs/beat-board-prompt-${episodeDefault}.md（九宫格总览）
- 读取 outputs/beat-breakdown-${episodeDefault}.md（节拍拆解）
- 读取 .agent-state.json 获取项目配置

### 步骤2: 读取分析模块
- 读取 animator-skill/motion-prompt-methodology/index.md ← 动态提示词方法论
- 读取 animator-skill/physics-verification-rules.md ← 物理验证规则
- 读取 animator-skill/templates/motion-prompt-template.md ← 输出格式模板

### 步骤3: 执行五模块构造
按 motion-prompt-methodology 规则构造:
1. 镜头运动模块（1-2种运动）
2. 主体动作模块（1-2种动作）
3. 环境动态模块（必须包含）
4. 节奏控制模块
5. 氛围强化模块

### 步骤4: 执行物理合理性检查
按 physics-verification-rules.md 逐项检查:
□ 重力影响检查
□ 惯性表现检查
□ 材质反应检查
□ 能量守恒检查

### 步骤5: 保存输出文件
- 保存到: outputs/motion-prompt-${episodeDefault}.md
`,
        creative: `
## 添加创意指令工作流程

### 步骤1: 解析创意指令
- 解析指令类型（style fusion / reference / character variant / atmosphere / effect）
- 提取参数和目标阶段

### 步骤2: 调用创意引擎
- 读取 film-storyboard-skill/creative-engines-integration/index.md
- 执行对应类型的创意融合

### 步骤3: 更新产出文件
- 根据创意指令修改对应阶段的产出文件
- 标记已修改状态
`,
        review: `
## 审核工作流程

### 步骤1: 确定审核类型
- breakdown / beatboard / sequence / motion / all

### 步骤2: 读取基准文件
- 读取 storyboard-review-skill/review-checklist.md
- 读取 storyboard-review-skill/uncertainty-judgment-protocol.md
- 读取 storyboard-review-skill/asset-consistency-rules.md（如适用）

### 步骤3: 读取待审核内容
- 读取对应的 outputs/*.md 文件
- 读取上游产物（如果有）

### 步骤4: 逐项检查
按 review-checklist.md 逐项检查:
□ 结构完整性
□ 内容质量
□ 风格一致性
□ 技术规范

### 步骤5: 执行不确定项判定
按 uncertainty-judgment-protocol.md 判定:
- 识别潜在不确定项
- 生成决策选项

### 步骤6: 生成审核报告
- 保存到: outputs/{产物类型}-{集数}-review.md
`
    };
    
    return workflows[task] || `\n## ${task} 工作流程\n未定义的流程`;
}

/**
 * 构建用户确认步骤
 * @param {string} task - 任务类型
 * @returns {string} 用户确认步骤字符串
 */
function buildConfirmationSteps(task) {
    const confirmPoints = {
        breakdown: 'CP1',
        beatboard: 'CP2',
        sequence: 'CP3',
        motion: 'CP4',
        creative: 'CP2',
        review: '审核确认'
    };
    
    const confirmPoint = confirmPoints[task] || 'CP';
    
    return `
### 步骤8: 执行用户确认（${confirmPoint}）
执行前必须读取: ${PROTOCOL_FILES.userConfirmation}
- 展示标准确认UI模板
- 包含: 进度条、质量评分、审核状态、操作选项
- 等待用户选择: [通过] ✅ / [修改] ✏️ / [重生成] 🔄 / [回滚] ⏪

### 步骤9: 执行快照管理
执行前必须读取: ${PROTOCOL_FILES.snapshotManagement}
- 根据确认点类型创建对应快照
- 完整快照（CP1/CP5）/ 分板快照（CP2）/ 分组快照（CP3）/ 参数快照（CP4）
- 更新 .agent-state.json 记录快照信息

### 步骤10: 进入下一阶段或结束
根据用户选择决定:
- [通过] → 进入下一阶段或结束
- [修改] → 等待修改后重新审核
- [重生成] → 重新执行生成流程
- [回滚] → 恢复到历史快照
`;
}

/**
 * 构建完整的 Agent 调用参数
 * @param {object} routeResult - 路由结果
 * @returns {object} 调用参数
 */
function buildAgentCall(routeResult) {
    const { agent, task, episode, originalInput } = routeResult;
    const episodeDefault = episode || 'ep01';
    
    const moduleDeps = getModuleDependencies(task);
    const executionFlow = buildExecutionFlow(task, episodeDefault);
    const confirmationSteps = buildConfirmationSteps(task);
    
    // 轻量化：start 和 status 从 router.js 动态生成
    if (task === 'start') {
        const state = getProjectState();
        const welcomeMsg = generateWelcomeMessage(state);
        return {
            subagent_type: 'general',
            prompt: welcomeMsg,
            description: `${routeResult.description} - ${episodeDefault}`
        };
    }
    
    if (task === 'status') {
        const state = getProjectState();
        const statusReport = generateStatusReport(state);
        return {
            subagent_type: 'general',
            prompt: statusReport,
            description: `${routeResult.description} - ${episodeDefault}`
        };
    }
    
    // 其他命令保持原有逻辑
    const prompt = `[角色]
你是一名专业的 ${agent === 'storyboard-artist' ? '分镜师' : agent === 'director' ? '导演' : '动画师'}。
你将按照 SKILL.md 定义的完整工作流程执行任务。

[任务]
执行 ${routeResult.description} 任务
集数: ${episodeDefault}

[必须读取的模块]
${moduleDeps}

[协议文件]
- 用户确认协议: ${PROTOCOL_FILES.userConfirmation}
- 快照管理规则: ${PROTOCOL_FILES.snapshotManagement}
- 信息传递机制: ${PROTOCOL_FILES.informationFlow}
- 协作模式: ${PROTOCOL_FILES.collaborationMode}

[完整工作流程]
${executionFlow}

${confirmationSteps}

[参考规范]
详细规范参考: ${PROTOCOL_FILES.informationFlow} 和 ${PROTOCOL_FILES.collaborationMode}

请严格按照上述流程执行任务。`;
    
    return {
        subagent_type: 'general',
        prompt: prompt,
        description: `${routeResult.description} - ${episodeDefault}`
    };
}

/**
 * 打印路由结果
 * @param {object} routeResult - 路由结果
 */
function printRouteResult(routeResult) {
    if (!routeResult) {
        console.log(`
❌ 无法识别的指令：${routeResult?.originalInput}

可用指令：
${Object.entries(ROUTING_TABLE)
    .filter(([key]) => !key.includes(':'))
    .map(([key, value]) => `  ${key.padEnd(15)} - ${value.description}`)
    .join('\n')}
        `);
        return;
    }
    
    console.log(`
┌─────────────────────────────────────────┐
│  路由结果                                │
├─────────────────────────────────────────┤
│  指令：${routeResult.originalInput.padEnd(35)}│
│  Agent：${routeResult.agent.padEnd(39)}│
│  任务：${routeResult.task.padEnd(39)}│
│  集数：${(routeResult.episode || '默认').padEnd(39)}│
│  描述：${routeResult.description.padEnd(39)}│
└─────────────────────────────────────────┘
    `);
}

/**
 * 主函数
 */
function main() {
    const args = process.argv.slice(2);
    
    if (args.length === 0) {
        console.log(`
╔═══════════════════════════════════════════════════════════════╗
║  ANINEO Agent 路由模块 v3.0（轻量化版）                        ║
╠═══════════════════════════════════════════════════════════════╣
║  快速开始：                                                    ║
║    任意输入 → 自动检测状态 → 显示引导                          ║
║                                                                ║
║  手动命令：                                                     ║
║    /start          # 欢迎 + 智能引导（动态生成）               ║
║    /interactive    # 项目配置向导                              ║
║    /status         # 项目状态报告（动态生成）                  ║
║    /breakdown ep01 # 节拍拆解                                  ║
║    /beatboard ep01 # 九宫格提示词                              ║
║    /sequence ep01  # 四宫格提示词                              ║
║    /motion ep01    # 动态提示词                                ║
║    /review ep01    # 审核产出                                  ║
║                                                                ║
║  轻量化特性：                                                   ║
║    ✓ 智能引导从 router.js 动态生成（零维护）                   ║
║    ✓ 欢迎消息自动从 .agent-state.json 读取                     ║
║    ✓ 减少 .opencode/command/ 文档文件                         ║
╚═══════════════════════════════════════════════════════════════╝
        `);
        return;
    }
    
    const input = args.join(' ');
    const routeResult = route(input);
    
    if (routeResult) {
        printRouteResult(routeResult);
        
        const agentCall = buildAgentCall(routeResult);
        console.log(`
在 OpenCode 中使用：

task(
    subagent_type="${agentCall.subagent_type}",
    prompt=\`
${agentCall.prompt}
\`
);
        `);
    } else {
        // 打印帮助
        const { command } = parseInstruction(input);
        printRouteResult(null);
    }
}

// 导出供其他模块使用
module.exports = {
    route,
    parseInstruction,
    buildAgentCall,
    ROUTING_TABLE,
    // 轻量化：导出新增函数供外部使用
    getProjectState,
    detectNextPhase,
    generateWelcomeMessage,
    generateStatusReport
};

// 如果直接运行
if (require.main === module) {
    main();
}
