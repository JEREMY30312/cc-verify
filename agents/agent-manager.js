/**
 * ANINEO Agent 管理器
 * 负责管理 subagent 的 agentId 和状态
 * 
 * 功能：
 * 1. 首次调用 subagent 并捕获 agentId
 * 2. Resume 调用 subagent
 * 3. 更新 .agent-state.json 中的 agentId 状态
 * 4. 验证 agentId 有效性
 * 5. Fallback 机制
 */

const fs = require('fs');
const path = require('path');

// 状态文件路径
const STATE_FILE = '.agent-state.json';

/**
 * 读取状态文件
 */
function readAgentState() {
    if (!fs.existsSync(STATE_FILE)) {
        // 创建初始状态文件
        const initialState = {
            version: "2.0",
            projectConfig: {},
            phase: null,
            current_episode: null,
            subagents: {
                "storyboard-artist": {
                    agentId: null,
                    last_task: null,
                    last_used: null,
                    status: "not_created"
                },
                "director": {
                    agentId: null,
                    last_task: null,
                    last_used: null,
                    status: "not_created"
                },
                "animator": {
                    agentId: null,
                    last_task: null,
                    last_used: null,
                    status: "not_created"
                }
            },
            snapshots: []
        };
        writeAgentState(initialState);
        return initialState;
    }
    
    try {
        const content = fs.readFileSync(STATE_FILE, 'utf8');
        return JSON.parse(content);
    } catch (error) {
        console.error(`读取状态文件失败: ${error.message}`);
        throw error;
    }
}

/**
 * 写入状态文件（原子操作）
 */
function writeAgentState(state) {
    try {
        // 使用临时文件确保原子性
        const tempFile = `${STATE_FILE}.tmp`;
        fs.writeFileSync(tempFile, JSON.stringify(state, null, 2), 'utf8');
        fs.renameSync(tempFile, STATE_FILE);
        console.log(`状态文件已更新: ${STATE_FILE}`);
    } catch (error) {
        console.error(`写入状态文件失败: ${error.message}`);
        throw error;
    }
}

/**
 * 从子 Agent 输出中捕获 agentId
 * @param {string} subagentOutput - 子 Agent 的输出
 * @returns {string|null} agentId 或 null
 */
function captureAgentId(subagentOutput) {
    try {
        // 尝试从输出中提取 JSON 元数据
        const jsonMatch = subagentOutput.match(/\{[\s\S]*\}/);
        if (!jsonMatch) {
            console.warn('子 Agent 输出中没有找到 JSON 元数据');
            return null;
        }
        
        const metadata = JSON.parse(jsonMatch[0]);
        const agentId = metadata.agentId;
        
        if (agentId && agentId !== '系统自动生成的agentId，制片人需要捕获并记录') {
            console.log(`捕获到 agentId: ${agentId}`);
            return agentId;
        } else {
            console.warn('子 Agent 输出中没有有效的 agentId');
            return null;
        }
    } catch (error) {
        console.error(`捕获 agentId 失败: ${error.message}`);
        return null;
    }
}

/**
 * 获取指定 subagent 的 agentId
 * @param {string} agentType - subagent 类型
 * @returns {string|null} agentId 或 null
 */
function getAgentId(agentType) {
    const state = readAgentState();
    const subagent = state.subagents[agentType];
    
    if (!subagent) {
        console.warn(`未知的 subagent 类型: ${agentType}`);
        return null;
    }
    
    return subagent.agentId;
}

/**
 * 更新 subagent 状态
 * @param {string} agentType - subagent 类型
 * @param {string} agentId - agentId
 * @param {string} task - 任务类型
 * @param {string} status - 状态
 */
function updateAgentState(agentType, agentId, task, status = 'idle') {
    const state = readAgentState();
    
    if (!state.subagents[agentType]) {
        console.warn(`未知的 subagent 类型: ${agentType}`);
        return;
    }
    
    // 更新状态
    state.subagents[agentType].agentId = agentId;
    state.subagents[agentType].last_task = task;
    state.subagents[agentType].last_used = new Date().toISOString();
    state.subagents[agentType].status = status;
    
    writeAgentState(state);
    console.log(`更新 ${agentType} 状态: agentId=${agentId}, task=${task}, status=${status}`);
}

/**
 * 重置 subagent 状态
 * @param {string} agentType - subagent 类型
 */
function resetAgentState(agentType) {
    const state = readAgentState();
    
    if (!state.subagents[agentType]) {
        console.warn(`未知的 subagent 类型: ${agentType}`);
        return;
    }
    
    // 重置状态
    state.subagents[agentType].agentId = null;
    state.subagents[agentType].last_task = null;
    state.subagents[agentType].last_used = null;
    state.subagents[agentType].status = "not_created";
    
    writeAgentState(state);
    console.log(`重置 ${agentType} 状态`);
}

/**
 * 验证 agentId 有效性
 * @param {string} agentType - subagent 类型
 * @returns {boolean} 是否有效
 */
function validateAgentId(agentType) {
    const state = readAgentState();
    const subagent = state.subagents[agentType];
    
    if (!subagent) {
        console.warn(`未知的 subagent 类型: ${agentType}`);
        return false;
    }
    
    // 检查 agentId 是否存在
    if (!subagent.agentId) {
        console.warn(`${agentType} 的 agentId 为空`);
        return false;
    }
    
    // 检查状态是否为 error
    if (subagent.status === 'error') {
        console.warn(`${agentType} 状态为 error`);
        return false;
    }
    
    // 检查 last_used 时间（如果超过24小时，认为失效）
    if (subagent.last_used) {
        const lastUsed = new Date(subagent.last_used);
        const now = new Date();
        const hoursDiff = (now - lastUsed) / (1000 * 60 * 60);
        
        if (hoursDiff > 24) {
            console.warn(`${agentType} 的 agentId 已过期 (${hoursDiff.toFixed(1)} 小时)`);
            return false;
        }
    }
    
    return true;
}

/**
 * 调用 subagent（支持 Resume 机制）
 * @param {string} agentType - subagent 类型
 * @param {string} taskDescription - 任务描述
 * @param {Array} contextFiles - 上下文文件
 * @returns {string} 调用结果
 */
function callSubagent(agentType, taskDescription, contextFiles = []) {
    console.log(`调用 ${agentType}: ${taskDescription}`);
    
    // 验证 agentId 有效性
    const isValid = validateAgentId(agentType);
    const agentId = getAgentId(agentType);
    
    let output;
    
    if (isValid && agentId) {
        // 使用 Resume 调用
        console.log(`使用 Resume 调用: agentId=${agentId}`);
        // 这里应该实际调用 Resume agent <agentId> and <taskDescription>
        // 暂时返回模拟结果
        output = `Resume agent ${agentId} and ${taskDescription}\n\n`;
        output += `[${agentType} 执行 ${taskDescription}]\n`;
        output += `JSON元数据: {"agentId": "${agentId}", "task_type": "${taskDescription}", "status": "success"}`;
    } else {
        // 使用首次调用
        console.log(`使用首次调用: Use ${agentType} agent to ${taskDescription}`);
        // 这里应该实际调用 Use <agentType> agent to <taskDescription>
        // 暂时返回模拟结果
        const newAgentId = `agent_${agentType}_${Date.now()}`;
        output = `Use ${agentType} agent to ${taskDescription}\n\n`;
        output += `[${agentType} 执行 ${taskDescription}]\n`;
        output += `JSON元数据: {"agentId": "${newAgentId}", "task_type": "${taskDescription}", "status": "success"}`;
        
        // 捕获 agentId
        const capturedAgentId = captureAgentId(output) || newAgentId;
        
        // 更新状态
        updateAgentState(agentType, capturedAgentId, taskDescription, 'idle');
    }
    
    return output;
}

/**
 * 验证状态文件完整性
 */
function validateStateIntegrity() {
    const state = readAgentState();
    const errors = [];
    
    // 检查必需字段
    if (!state.version) errors.push('缺少 version 字段');
    if (!state.subagents) errors.push('缺少 subagents 字段');
    
    // 检查每个 subagent
    const requiredSubagents = ['storyboard-artist', 'director', 'animator'];
    for (const agentType of requiredSubagents) {
        if (!state.subagents[agentType]) {
            errors.push(`缺少 ${agentType} 配置`);
            continue;
        }
        
        const subagent = state.subagents[agentType];
        
        // 检查状态一致性
        if (subagent.status === 'idle' && !subagent.agentId) {
            errors.push(`${agentType}: status=idle 但 agentId=null`);
        }
        
        if (subagent.status === 'busy' && !subagent.last_task) {
            errors.push(`${agentType}: status=busy 但 last_task=null`);
        }
        
        if (subagent.status !== 'not_created' && !subagent.last_used) {
            errors.push(`${agentType}: status=${subagent.status} 但 last_used=null`);
        }
    }
    
    if (errors.length > 0) {
        console.error('状态文件完整性检查失败:');
        errors.forEach(error => console.error(`  - ${error}`));
        return false;
    }
    
    console.log('状态文件完整性检查通过');
    return true;
}

// 导出模块
module.exports = {
    readAgentState,
    writeAgentState,
    captureAgentId,
    getAgentId,
    updateAgentState,
    resetAgentState,
    validateAgentId,
    callSubagent,
    validateStateIntegrity
};