# OCR API 成本對比：Google Vision vs 百度 OCR

## 📋 對比日期
2025-11-16

## 🎯 對比目的
評估是否應該從 Google Vision API 切換到百度 OCR API 以降低成本。

---

## 💰 價格對比

### **Google Vision API 價格**

| 用量 | 單價（USD） | 單價（HKD） | 備註 |
|-----|-----------|-----------|------|
| **前 1,000 張/月** | 免費 | 免費 | ✅ 適合小規模測試 |
| **1,001 - 5,000,000 張** | $1.50/1000 張 | HKD $11.70/1000 張 | HKD $0.0117/張 |
| **5,000,001 - 20,000,000 張** | $0.60/1000 張 | HKD $4.68/1000 張 | HKD $0.00468/張 |

**匯率：** 1 USD = 7.8 HKD

---

### **百度 OCR API 價格**

| 用量 | 單價（CNY） | 單價（HKD） | 備註 |
|-----|-----------|-----------|------|
| **前 1,000 次/天** | 免費 | 免費 | ✅ 每月 30,000 次免費 |
| **超過免費額度** | ¥0.002/次 | HKD $0.0022/次 | HKD $0.0022/張 |
| **QPS 提升（可選）** | ¥50/QPS/天 | HKD $55/QPS/天 | 高並發場景 |

**匯率：** 1 CNY = 1.1 HKD

**免費額度計算：**
- 每天 1,000 次免費
- 每月 30 天 × 1,000 次 = **30,000 次免費**

---

## 📊 成本對比表（HKD）

### **1,000 張**

| API | 免費額度 | 付費部分 | 總成本（HKD） | 推薦 |
|-----|---------|---------|--------------|------|
| **Google Vision** | 1,000 張免費 | 0 張 | **HKD $0** | ✅ |
| **百度 OCR** | 1,000 張免費 | 0 張 | **HKD $0** | ✅ |

**結論：** 兩者都免費 ✅

---

### **10,000 張**

| API | 免費額度 | 付費部分 | 總成本（HKD） | 推薦 |
|-----|---------|---------|--------------|------|
| **Google Vision** | 1,000 張免費 | 9,000 張 × HKD $0.0117 | **HKD $105.30** | ❌ |
| **百度 OCR** | 30,000 張免費 | 0 張 | **HKD $0** | ✅ |

**結論：** 百度 OCR 便宜 **HKD $105.30**（節省 100%）✅

---

### **100,000 張**

| API | 免費額度 | 付費部分 | 總成本（HKD） | 推薦 |
|-----|---------|---------|--------------|------|
| **Google Vision** | 1,000 張免費 | 99,000 張 × HKD $0.0117 | **HKD $1,158.30** | ❌ |
| **百度 OCR** | 30,000 張免費 | 70,000 張 × HKD $0.0022 | **HKD $154.00** | ✅ |

**結論：** 百度 OCR 便宜 **HKD $1,004.30**（節省 87%）✅

---

### **1,000,000 張（大規模）**

| API | 免費額度 | 付費部分 | 總成本（HKD） | 推薦 |
|-----|---------|---------|--------------|------|
| **Google Vision** | 1,000 張免費 | 999,000 張 × HKD $0.0117 | **HKD $11,688.30** | ❌ |
| **百度 OCR** | 30,000 張免費 | 970,000 張 × HKD $0.0022 | **HKD $2,134.00** | ✅ |

**結論：** 百度 OCR 便宜 **HKD $9,554.30**（節省 82%）✅

---

## 📈 成本節省總結

| 用量 | Google Vision | 百度 OCR | 節省（HKD） | 節省比例 |
|-----|--------------|---------|-----------|---------|
| **1,000 張** | HKD $0 | HKD $0 | HKD $0 | - |
| **10,000 張** | HKD $105.30 | HKD $0 | **HKD $105.30** | **100%** ✅ |
| **100,000 張** | HKD $1,158.30 | HKD $154.00 | **HKD $1,004.30** | **87%** ✅ |
| **1,000,000 張** | HKD $11,688.30 | HKD $2,134.00 | **HKD $9,554.30** | **82%** ✅ |

---

## 🔍 功能對比

### **Google Vision API**

| 功能 | 支持 | 說明 |
|-----|------|------|
| **文檔 OCR** | ✅ | `DOCUMENT_TEXT_DETECTION` |
| **表格識別** | ✅ | 自動識別表格結構 |
| **多語言** | ✅ | 支持 100+ 語言 |
| **手寫識別** | ✅ | 支持手寫文字 |
| **PDF 支持** | ⚠️ | 需要上傳到 GCS（不支持 base64） |
| **圖片格式** | ✅ | JPG, PNG, GIF, BMP, WebP |
| **最大文件大小** | 20 MB | 單個圖片 |
| **API 穩定性** | ✅ | 99.9% SLA |
| **香港可用** | ✅ | 無區域限制 |

---

### **百度 OCR API**

| 功能 | 支持 | 說明 |
|-----|------|------|
| **文檔 OCR** | ✅ | 通用文字識別 |
| **表格識別** | ✅ | 需要單獨調用表格識別 API |
| **多語言** | ✅ | 支持中文、英文、日文等 |
| **手寫識別** | ✅ | 需要單獨調用手寫識別 API |
| **PDF 支持** | ✅ | 支持 PDF 直接上傳 |
| **圖片格式** | ✅ | JPG, PNG, BMP |
| **最大文件大小** | 4 MB | 單個圖片 |
| **API 穩定性** | ✅ | 99.9% SLA |
| **香港可用** | ✅ | 無區域限制 |

---

## ⚖️ 優劣勢對比

### **Google Vision API**

**優勢：**
- ✅ 功能更強大（表格識別、手寫識別整合在一個 API）
- ✅ 準確度更高（特別是英文文檔）
- ✅ 文檔更完善
- ✅ 支持更多圖片格式
- ✅ 最大文件大小 20 MB

**劣勢：**
- ❌ 成本更高（超過 1,000 張後）
- ❌ PDF 支持不友好（需要上傳到 GCS）
- ❌ 免費額度較少（1,000 張/月）

---

### **百度 OCR API**

**優勢：**
- ✅ 成本更低（超過 1,000 張後）
- ✅ 免費額度更多（30,000 張/月）
- ✅ PDF 支持更友好（直接上傳）
- ✅ 中文識別準確度高

**劣勢：**
- ❌ 功能較分散（表格識別需要單獨調用）
- ❌ 最大文件大小 4 MB
- ❌ 文檔相對較少（中文為主）

---

## 🎯 切換建議

### **建議切換到百度 OCR 的場景：**

1. ✅ **月處理量 > 10,000 張**
   - 節省 HKD $105.30/月
   - 節省比例：100%

2. ✅ **月處理量 > 100,000 張**
   - 節省 HKD $1,004.30/月
   - 節省比例：87%

3. ✅ **主要處理中文文檔**
   - 百度 OCR 中文識別準確度更高

4. ✅ **需要處理 PDF 文件**
   - 百度 OCR 支持 PDF 直接上傳
   - Google Vision 需要先轉換為圖片

---

### **建議保持 Google Vision 的場景：**

1. ✅ **月處理量 < 1,000 張**
   - 兩者都免費，無需切換

2. ✅ **主要處理英文文檔**
   - Google Vision 英文識別準確度更高

3. ✅ **需要處理大文件（> 4 MB）**
   - Google Vision 支持最大 20 MB

4. ✅ **需要一體化功能**
   - Google Vision 表格識別、手寫識別整合在一個 API

---

## 🔧 切換實施方案

### **階段 1：評估（1 週）**

1. ✅ 統計當前月處理量
2. ✅ 評估未來增長趨勢
3. ✅ 計算潛在節省成本

---

### **階段 2：測試（2 週）**

1. ✅ 註冊百度 OCR API
2. ✅ 創建測試適配器（`baidu-ocr-adapter.js`）
3. ✅ 測試準確度（對比 Google Vision）
4. ✅ 測試處理速度
5. ✅ 測試 PDF 支持

---

### **階段 3：切換（1 週）**

1. ✅ 修改 `hybrid-vision-deepseek.js`
2. ✅ 添加配置選項（Google Vision / 百度 OCR）
3. ✅ 灰度發布（10% 流量使用百度 OCR）
4. ✅ 監控錯誤率和準確度
5. ✅ 全量切換

---

### **階段 4：優化（持續）**

1. ✅ 監控成本節省
2. ✅ 優化錯誤處理
3. ✅ 收集用戶反饋

---

## 📝 技術實施示例

### **創建百度 OCR 適配器**

```javascript
// baidu-ocr-adapter.js

class BaiduOCRAdapter {
    constructor() {
        this.apiKey = 'YOUR_BAIDU_API_KEY';
        this.secretKey = 'YOUR_BAIDU_SECRET_KEY';
        this.apiUrl = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general';
        
        console.log('🤖 百度 OCR 適配器初始化');
        console.log('   📊 免費額度: 1,000 次/天');
        console.log('   💰 成本: HKD $0.0022/張');
    }
    
    async extractText(file) {
        // 1. 獲取 Access Token
        const accessToken = await this.getAccessToken();
        
        // 2. 轉換文件為 Base64
        const base64Data = await this.fileToBase64(file);
        
        // 3. 調用百度 OCR API
        const response = await fetch(`${this.apiUrl}?access_token=${accessToken}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: `image=${encodeURIComponent(base64Data)}`
        });
        
        const data = await response.json();
        
        // 4. 提取文本
        if (data.words_result) {
            const text = data.words_result.map(item => item.words).join('\n');
            return text;
        } else {
            throw new Error('百度 OCR 未能提取文本');
        }
    }
    
    async getAccessToken() {
        const response = await fetch(
            `https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=${this.apiKey}&client_secret=${this.secretKey}`
        );
        const data = await response.json();
        return data.access_token;
    }
    
    async fileToBase64(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = () => {
                const base64 = reader.result.split(',')[1];
                resolve(base64);
            };
            reader.onerror = error => reject(error);
            reader.readAsDataURL(file);
        });
    }
}
```

---

### **修改 `hybrid-vision-deepseek.js`**

```javascript
class HybridVisionDeepSeekProcessor {
    constructor(ocrProvider = 'google') {
        this.ocrProvider = ocrProvider; // 'google' 或 'baidu'
        
        if (ocrProvider === 'google') {
            this.visionApiKey = 'YOUR_GOOGLE_API_KEY';
            this.visionApiUrl = 'https://vision.googleapis.com/v1/images:annotate';
        } else if (ocrProvider === 'baidu') {
            this.baiduOCR = new BaiduOCRAdapter();
        }
        
        console.log(`🤖 混合處理器初始化（OCR: ${ocrProvider}）`);
    }
    
    async extractTextWithVision(file) {
        if (this.ocrProvider === 'google') {
            return await this.extractTextWithGoogleVision(file);
        } else if (this.ocrProvider === 'baidu') {
            return await this.baiduOCR.extractText(file);
        }
    }
    
    async extractTextWithGoogleVision(file) {
        // 原有的 Google Vision 邏輯
        // ...
    }
}
```

---

## 💡 最終建議

### **立即行動（月處理量 > 10,000 張）**

如果您的月處理量超過 10,000 張：
1. ✅ **立即切換到百度 OCR**
2. ✅ **節省 100% OCR 成本**（在免費額度內）
3. ✅ **年節省 HKD $1,263.60**（10,000 張/月）

---

### **觀望等待（月處理量 < 10,000 張）**

如果您的月處理量少於 10,000 張：
1. ✅ **保持 Google Vision**
2. ✅ **等待處理量增長**
3. ✅ **定期評估成本**

---

### **混合方案（推薦）**

1. ✅ **中文文檔使用百度 OCR**（成本更低，準確度更高）
2. ✅ **英文文檔使用 Google Vision**（準確度更高）
3. ✅ **PDF 文件使用百度 OCR**（支持直接上傳）
4. ✅ **大文件（> 4 MB）使用 Google Vision**（支持最大 20 MB）

---

## 🎉 總結

| 用量 | 推薦方案 | 節省成本 | 理由 |
|-----|---------|---------|------|
| **< 1,000 張/月** | Google Vision | HKD $0 | 兩者都免費 |
| **1,000 - 30,000 張/月** | 百度 OCR | HKD $105 - $351 | 100% 節省 |
| **> 30,000 張/月** | 百度 OCR | HKD $1,004+ | 87% 節省 |

**最終建議：** 如果月處理量 > 10,000 張，**強烈建議切換到百度 OCR API**！✅

