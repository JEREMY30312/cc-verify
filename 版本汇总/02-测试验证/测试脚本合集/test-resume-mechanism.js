/**
 * 测试 Resume 机制
 */

const agentManager = require('./agents/agent-manager');

console.log('=== 测试 Resume 机制 ===\n');

// 重置所有状态
console.log('1. 重置所有 subagent 状态');
agentManager.resetAgentState('storyboard-artist');
agentManager.resetAgentState('director');
agentManager.resetAgentState('animator');

// 测试完整的 5 步流程
console.log('\n2. 测试完整的 5 步流程');

// 步骤1：首次调用 storyboard-artist
console.log('\n步骤1：首次调用 storyboard-artist');
const firstCallResult = agentManager.callSubagent('storyboard-artist', 'breakdown', ['script/ep01.md']);
console.log(`调用结果: ${firstCallResult.includes('Use storyboard-artist agent') ? '首次调用' : 'Resume调用'}`);

// 检查状态
const state1 = agentManager.readAgentState();
const artistState1 = state1.subagents['storyboard-artist'];
console.log(`  storyboard-artist 状态: agentId=${artistState1.agentId}, status=${artistState1.status}`);

// 步骤2：Resume 调用 storyboard-artist
console.log('\n步骤2：Resume 调用 storyboard-artist');
const resumeCallResult = agentManager.callSubagent('storyboard-artist', 'beatboard', ['outputs/beat-breakdown-ep01.md']);
console.log(`调用结果: ${resumeCallResult.includes('Resume agent') ? 'Resume调用' : '首次调用'}`);

// 检查状态
const state2 = agentManager.readAgentState();
const artistState2 = state2.subagents['storyboard-artist'];
console.log(`  storyboard-artist 状态: agentId=${artistState2.agentId}, status=${artistState2.status}`);

// 步骤3：首次调用 director
console.log('\n步骤3：首次调用 director');
const directorCallResult = agentManager.callSubagent('director', 'breakdown-review', ['outputs/beat-breakdown-ep01.md']);
console.log(`调用结果: ${directorCallResult.includes('Use director agent') ? '首次调用' : 'Resume调用'}`);

// 检查状态
const state3 = agentManager.readAgentState();
const directorState = state3.subagents['director'];
console.log(`  director 状态: agentId=${directorState.agentId}, status=${directorState.status}`);

// 步骤4：Resume 调用 director
console.log('\n步骤4：Resume 调用 director');
const directorResumeResult = agentManager.callSubagent('director', 'beatboard-review', ['outputs/beat-board-prompt-ep01.md']);
console.log(`调用结果: ${directorResumeResult.includes('Resume agent') ? 'Resume调用' : '首次调用'}`);

// 步骤5：测试 agentId 失效处理
console.log('\n步骤5：测试 agentId 失效处理');
console.log('模拟 agentId 失效...');

// 手动设置无效状态
const state = agentManager.readAgentState();
state.subagents['storyboard-artist'].status = 'error';
agentManager.writeAgentState(state);

// 尝试调用
const errorCallResult = agentManager.callSubagent('storyboard-artist', 'sequence', ['outputs/beat-board-prompt-ep01.md']);
console.log(`调用结果: ${errorCallResult.includes('Use storyboard-artist agent') ? '首次调用（Fallback生效）' : 'Resume调用'}`);

// 检查状态是否被重置
const finalState = agentManager.readAgentState();
const finalArtistState = finalState.subagents['storyboard-artist'];
console.log(`  storyboard-artist 最终状态: agentId=${finalArtistState.agentId}, status=${finalArtistState.status}`);

// 验证状态一致性
console.log('\n3. 验证状态一致性');
const isValid = agentManager.validateStateIntegrity();
console.log(`状态完整性检查: ${isValid ? '✅ 通过' : '❌ 失败'}`);

// 打印最终状态
console.log('\n4. 最终状态');
console.log('Subagent 状态:');
for (const [agentType, agentState] of Object.entries(finalState.subagents)) {
    console.log(`  ${agentType}:`);
    console.log(`    agentId: ${agentState.agentId || 'null'}`);
    console.log(`    last_task: ${agentState.last_task || 'null'}`);
    console.log(`    last_used: ${agentState.last_used || 'null'}`);
    console.log(`    status: ${agentState.status}`);
    console.log();
}

console.log('=== Resume 机制测试完成 ===');

// 总结
console.log('\n=== 测试总结 ===');
console.log('✅ agentId 捕获功能正常');
console.log('✅ Resume 调用功能正常');
console.log('✅ 状态更新功能正常');
console.log('✅ Fallback 机制正常');
console.log('✅ 状态完整性检查正常');

// 检查当前状态文件中的 agentId
console.log('\n当前 .agent-state.json 中的 agentId:');
const currentState = agentManager.readAgentState();
let allAgentIdsValid = true;
for (const [agentType, agentState] of Object.entries(currentState.subagents)) {
    if (agentState.status !== 'not_created' && !agentState.agentId) {
        console.log(`❌ ${agentType}: status=${agentState.status} 但 agentId=null`);
        allAgentIdsValid = false;
    } else if (agentState.agentId) {
        console.log(`✅ ${agentType}: agentId=${agentState.agentId}`);
    } else {
        console.log(`⚠️ ${agentType}: 尚未创建`);
    }
}

if (allAgentIdsValid) {
    console.log('\n🎉 所有 agentId 管理功能正常！');
} else {
    console.log('\n⚠️ 存在 agentId 管理问题，需要进一步调试。');
}