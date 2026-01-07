/**
 * Qwen-VL 配置文件
 * 
 * 使用说明：
 * 1. 在阿里云百炼控制台获取 API Key
 * 2. 将 API Key 填入下面的 qwenApiKey 变量
 * 3. 确保使用新加坡地域（国际版）
 * 
 * 推荐模型：qwen3-vl-plus-2025-12-19
 * - 最新Qwen3架构（2025-12-18发布）
 * - 功能最全面（OCR + 视觉理解 + 推理）
 * - 成本适中（约HK$0.03/页，节省95%）
 * - 适合银行对账单、收据、保单、医疗发票、理赔单据等
 * 
 * 详细模型对比请参考：📊_通义千问视觉模型选型分析_VaultCaddy.md
 */

// ⚠️ 请在此处填入您的 Qwen-VL Max API Key
// 获取步骤请参考：📋_Qwen-VL_Max_API_Key获取教学_国际版.md
const QWEN_VL_CONFIG = {
    // 从阿里云百炼控制台获取（国际版）：
    // 1. 访问 https://www.alibabacloud.com/ 注册账号
    // 2. 开通 Model Studio 服务（选择新加坡地域）
    // 3. 创建 API Key
    // 4. 填入下方
    apiKey: '', // 例如: 'sk-xxxxxxxxxxxxxxxxxxxxx'
    
    // API 端点（新加坡地域 - 国际版）
    apiUrl: 'https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions',
    
    // 模型名称
    // 推荐使用 Qwen3-VL-Plus（2025-12-18发布，最新模型）
    // 详细对比请参考：📊_通义千问视觉模型选型分析_VaultCaddy.md
    model: 'qwen3-vl-plus-2025-12-19', // ⭐推荐（最新、最全能、成本适中）
    
    // 其他可选模型：
    // - 'qwen-vl-ocr-2025-11-20'（纯OCR场景，成本最低）
    // - 'qwen-vl-max'（极复杂文档，成本较高）
    
    // 请求配置
    temperature: 0.1, // 降低随机性，提高准确性
    maxTokens: 4000,  // 最大输出token数
};

// 导出配置（如果使用模块系统）
if (typeof module !== 'undefined' && module.exports) {
    module.exports = QWEN_VL_CONFIG;
}


