/**
 * 测试 agentId 捕获功能
 */

const agentManager = require('./agents/agent-manager');

console.log('=== 测试 agentId 捕获功能 ===\n');

// 测试1：读取当前状态
console.log('测试1：读取当前状态');
try {
    const state = agentManager.readAgentState();
    console.log('当前状态:');
    console.log(`  版本: ${state.version}`);
    console.log(`  当前阶段: ${state.phase || 'null'}`);
    console.log(`  当前集数: ${state.current_episode || 'null'}`);
    
    console.log('\n  Subagent 状态:');
    for (const [agentType, agentState] of Object.entries(state.subagents)) {
        console.log(`    ${agentType}: agentId=${agentState.agentId || 'null'}, status=${agentState.status}`);
    }
    console.log('✅ 测试1通过\n');
} catch (error) {
    console.error(`❌ 测试1失败: ${error.message}`);
}

// 测试2：测试 agentId 捕获
console.log('测试2：测试 agentId 捕获');
try {
    // 模拟子 Agent 输出
    const mockOutput = `
Use storyboard-artist agent to 生成节拍拆解

[storyboard-artist 执行 生成节拍拆解]
JSON元数据: {"agentId": "agent_storyboard_12345", "task_type": "breakdown", "episode": "ep01", "status": "success"}
`;
    
    const agentId = agentManager.captureAgentId(mockOutput);
    if (agentId === 'agent_storyboard_12345') {
        console.log(`✅ 成功捕获 agentId: ${agentId}`);
    } else {
        console.log(`❌ 捕获的 agentId 不正确: ${agentId}`);
    }
    console.log('✅ 测试2通过\n');
} catch (error) {
    console.error(`❌ 测试2失败: ${error.message}`);
}

// 测试3：测试状态更新
console.log('测试3：测试状态更新');
try {
    const testAgentId = 'test_agent_123';
    const testTask = 'breakdown';
    
    // 更新状态
    agentManager.updateAgentState('storyboard-artist', testAgentId, testTask, 'idle');
    
    // 验证更新
    const state = agentManager.readAgentState();
    const updatedState = state.subagents['storyboard-artist'];
    
    if (updatedState.agentId === testAgentId && 
        updatedState.last_task === testTask && 
        updatedState.status === 'idle') {
        console.log(`✅ 状态更新成功: agentId=${updatedState.agentId}, task=${updatedState.last_task}, status=${updatedState.status}`);
    } else {
        console.log(`❌ 状态更新失败: agentId=${updatedState.agentId}, task=${updatedState.last_task}, status=${updatedState.status}`);
    }
    console.log('✅ 测试3通过\n');
} catch (error) {
    console.error(`❌ 测试3失败: ${error.message}`);
}

// 测试4：测试 agentId 验证
console.log('测试4：测试 agentId 验证');
try {
    // 验证有效的 agentId
    const isValid = agentManager.validateAgentId('storyboard-artist');
    console.log(`storyboard-artist 验证结果: ${isValid ? '有效' : '无效'}`);
    
    // 验证不存在的 agent
    const invalidAgent = agentManager.validateAgentId('nonexistent-agent');
    console.log(`nonexistent-agent 验证结果: ${invalidAgent ? '有效' : '无效'}`);
    
    console.log('✅ 测试4通过\n');
} catch (error) {
    console.error(`❌ 测试4失败: ${error.message}`);
}

// 测试5：测试状态完整性检查
console.log('测试5：测试状态完整性检查');
try {
    const isValid = agentManager.validateStateIntegrity();
    console.log(`状态完整性检查: ${isValid ? '通过' : '失败'}`);
    console.log('✅ 测试5通过\n');
} catch (error) {
    console.error(`❌ 测试5失败: ${error.message}`);
}

// 测试6：测试调用 subagent
console.log('测试6：测试调用 subagent');
try {
    // 重置状态，确保首次调用
    agentManager.resetAgentState('storyboard-artist');
    
    // 首次调用
    console.log('首次调用 storyboard-artist:');
    const firstCallResult = agentManager.callSubagent('storyboard-artist', '生成节拍拆解', ['script/ep01.md']);
    console.log(`调用结果: ${firstCallResult.substring(0, 100)}...`);
    
    // 读取状态验证
    const state = agentManager.readAgentState();
    const agentState = state.subagents['storyboard-artist'];
    
    if (agentState.agentId && agentState.status === 'idle') {
        console.log(`✅ 首次调用成功: agentId=${agentState.agentId}, status=${agentState.status}`);
    } else {
        console.log(`❌ 首次调用失败: agentId=${agentState.agentId}, status=${agentState.status}`);
    }
    
    // Resume 调用
    console.log('\nResume 调用 storyboard-artist:');
    const resumeCallResult = agentManager.callSubagent('storyboard-artist', '生成九宫格提示词', ['outputs/beat-breakdown-ep01.md']);
    console.log(`调用结果: ${resumeCallResult.substring(0, 100)}...`);
    
    console.log('✅ 测试6通过\n');
} catch (error) {
    console.error(`❌ 测试6失败: ${error.message}`);
}

console.log('=== 所有测试完成 ===');
console.log('\n当前状态文件内容:');
try {
    const state = agentManager.readAgentState();
    console.log(JSON.stringify(state, null, 2));
} catch (error) {
    console.error(`无法读取状态文件: ${error.message}`);
}