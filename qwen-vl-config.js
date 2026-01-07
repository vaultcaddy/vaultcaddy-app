/**
 * Qwen-VL Max 配置文件
 * 
 * 使用说明：
 * 1. 在阿里云百炼控制台获取 API Key
 * 2. 将 API Key 填入下面的 qwenApiKey 变量
 * 3. 确保使用新加坡地域（国际版）
 */

// ⚠️ 请在此处填入您的 Qwen-VL Max API Key
const QWEN_VL_CONFIG = {
    // 从阿里云百炼控制台获取：https://bailian.console.aliyun.com/
    apiKey: '', // 例如: 'sk-xxxxxxxxxxxxxxxxxxxxx'
    
    // API 端点（新加坡地域 - 国际版）
    apiUrl: 'https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions',
    
    // 模型名称
    model: 'qwen-vl-max', // 或 'qwen-vl-plus'（更便宜但能力稍弱）
    
    // 请求配置
    temperature: 0.1, // 降低随机性，提高准确性
    maxTokens: 4000,  // 最大输出token数
};

// 导出配置（如果使用模块系统）
if (typeof module !== 'undefined' && module.exports) {
    module.exports = QWEN_VL_CONFIG;
}


