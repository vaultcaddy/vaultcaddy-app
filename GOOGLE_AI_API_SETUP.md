# 🤖 Google AI API 設置指南

## 📋 **當前狀態檢查**

### ✅ **已完成的配置**
- ✅ 統一的 API Key 管理系統 (`config.js`)
- ✅ 開發環境 API Key 提示界面
- ✅ 生產環境安全 API Key 獲取
- ✅ Google Vision Service 整合
- ✅ 模擬數據後備系統

### 🔄 **需要完成的步驟**

---

## 🚀 **第一步：獲取 Google AI API Key**

### 1. **前往 Google Cloud Console**
```
https://console.cloud.google.com/
```

### 2. **創建或選擇項目**
- 點擊項目選擇器
- 創建新項目或選擇現有項目 `vaultcaddy-production`

### 3. **啟用必要的 API**
```bash
# 需要啟用的 APIs：
- AI Platform API
- Cloud Vision API  
- Cloud Document AI API
- Cloud Translation API (可選)
```

在 APIs & Services → Library 中搜索並啟用上述 API。

### 4. **創建 API Key**
```bash
# 步驟：
1. 前往 APIs & Services → Credentials
2. 點擊 "CREATE CREDENTIALS" → "API key"
3. 複製生成的 API Key (格式: AIza...)
4. 建議設置 API Key 限制（可選但推薦）
```

---

## 🔧 **第二步：設置 API Key**

### **開發環境 (本地測試)**
```javascript
// 在瀏覽器控制台執行：
localStorage.setItem('google_ai_api_key', 'AIza..._your_actual_api_key');

// 然後重新載入頁面
location.reload();
```

### **生產環境 (vaultcaddy.com)**

#### **方法 1：Meta Tag (推薦)**
在 HTML `<head>` 中添加：
```html
<meta name="google-ai-api-key" content="AIza..._your_actual_api_key">
```

#### **方法 2：服務器端環境變量**
```bash
# 設置環境變量
export GOOGLE_AI_API_KEY="AIza..._your_actual_api_key"
```

#### **方法 3：JavaScript 全局變量**
在頁面加載前設置：
```html
<script>
    window.GOOGLE_AI_API_KEY = "AIza..._your_actual_api_key";
</script>
```

---

## 🧪 **第三步：測試 API 整合**

### **快速測試腳本**
```javascript
// 在控制台執行以測試 API：
async function testGoogleAI() {
    const config = window.VaultCaddyConfig;
    const apiKey = config.apiConfig.google.apiKey;
    
    if (!apiKey) {
        console.error('❌ API Key 未設置');
        return;
    }
    
    console.log('✅ API Key 已設置:', apiKey.substring(0, 10) + '...');
    
    // 簡單的 API 測試
    try {
        const response = await fetch(`https://vision.googleapis.com/v1/images:annotate?key=${apiKey}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                requests: [{
                    image: { content: 'test' },
                    features: [{ type: 'TEXT_DETECTION', maxResults: 1 }]
                }]
            })
        });
        
        if (response.ok) {
            console.log('✅ Google AI API 連接成功');
        } else {
            console.error('❌ API 調用失敗:', response.status);
        }
    } catch (error) {
        console.error('❌ API 測試錯誤:', error);
    }
}

testGoogleAI();
```

---

## 🔒 **安全最佳實踐**

### **API Key 安全建議**
1. **限制 API Key 範圍**
   - 只啟用需要的 APIs
   - 設置 HTTP referrer 限制
   - 限制 IP 地址（如適用）

2. **定期輪換 API Key**
   - 建議每 3-6 個月更新一次
   - 保留舊 Key 一段時間以防中斷

3. **監控使用量**
   - 設置配額和警報
   - 監控異常使用模式

### **生產環境安全設置**
```javascript
// 推薦的安全配置
const secureConfig = {
    // 設置 API Key 限制
    restrictions: {
        apiKeyRestrictions: {
            androidKeyRestrictions: null,
            iosKeyRestrictions: null,
            browserKeyRestrictions: {
                allowedReferrers: [
                    "https://vaultcaddy.com/*",
                    "https://www.vaultcaddy.com/*"
                ]
            }
        }
    },
    
    // 設置配額限制
    quotas: {
        requestsPerDay: 10000,
        requestsPerMinute: 100
    }
};
```

---

## 📊 **監控和調試**

### **API 使用狀態檢查**
```javascript
// 檢查當前 API 配置
function checkAPIStatus() {
    const config = window.VaultCaddyConfig.getConfig();
    
    console.group('🔍 API 狀態檢查');
    console.log('環境:', config.environment);
    console.log('生產模式:', config.isProduction);
    console.log('API Key 已設置:', !!config.apiConfig.google.apiKey);
    
    if (config.apiConfig.google.apiKey) {
        console.log('API Key 前綴:', config.apiConfig.google.apiKey.substring(0, 10) + '...');
    }
    
    console.groupEnd();
}

// 執行檢查
checkAPIStatus();
```

### **錯誤排除**
```javascript
// 常見問題檢查
function troubleshootAPI() {
    console.group('🔧 API 問題排除');
    
    // 檢查配置對象
    if (!window.VaultCaddyConfig) {
        console.error('❌ VaultCaddyConfig 未載入 - 確保 config.js 已正確引入');
        return;
    }
    
    // 檢查 API Key
    const apiKey = window.VaultCaddyConfig.apiConfig.google.apiKey;
    if (!apiKey) {
        console.warn('⚠️ API Key 未設置');
        console.info('💡 請設置 Google AI API Key');
        return;
    }
    
    // 檢查 API Key 格式
    if (!apiKey.startsWith('AIza')) {
        console.error('❌ API Key 格式不正確 - 應該以 "AIza" 開頭');
        return;
    }
    
    if (apiKey.length < 30) {
        console.error('❌ API Key 長度不足 - 可能不完整');
        return;
    }
    
    console.log('✅ API Key 格式檢查通過');
    console.groupEnd();
}

troubleshootAPI();
```

---

## 📈 **使用量監控**

### **Google Cloud Console 監控**
1. 前往 APIs & Services → Dashboard
2. 查看 API 使用統計
3. 設置配額和警報
4. 監控成本

### **代碼中的使用追蹤**
```javascript
// API 使用統計
class APIUsageTracker {
    constructor() {
        this.stats = {
            totalRequests: 0,
            successfulRequests: 0,
            failedRequests: 0,
            lastRequestTime: null
        };
    }
    
    trackRequest(success = true) {
        this.stats.totalRequests++;
        this.stats.lastRequestTime = new Date();
        
        if (success) {
            this.stats.successfulRequests++;
        } else {
            this.stats.failedRequests++;
        }
        
        // 儲存到 localStorage
        localStorage.setItem('api_usage_stats', JSON.stringify(this.stats));
    }
    
    getStats() {
        return this.stats;
    }
}

window.apiTracker = new APIUsageTracker();
```

---

## ✅ **完成檢查清單**

### **設置完成確認**
- [ ] ✅ Google Cloud 項目已創建
- [ ] ✅ 必要 APIs 已啟用
- [ ] ✅ API Key 已創建並設置限制
- [ ] ✅ API Key 已正確配置到生產環境
- [ ] ✅ 本地開發環境可以正常使用
- [ ] ✅ API 連接測試通過
- [ ] ✅ 監控和配額已設置

### **驗證步驟**
```javascript
// 最終驗證腳本
async function finalVerification() {
    console.group('🎯 最終驗證');
    
    // 1. 配置檢查
    console.log('1. 檢查配置...');
    checkAPIStatus();
    
    // 2. API 連接測試
    console.log('2. 測試 API 連接...');
    await testGoogleAI();
    
    // 3. 文檔處理測試
    console.log('3. 測試文檔處理功能...');
    // 這裡可以添加實際的文檔處理測試
    
    console.log('🎉 驗證完成！');
    console.groupEnd();
}

finalVerification();
```

設置完成後，您的 VaultCaddy 將能夠使用真實的 Google AI API 進行文檔處理！🚀
