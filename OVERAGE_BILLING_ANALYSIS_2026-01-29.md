# 🔍 超額計費功能完整分析報告
**日期**: 2026-01-29  
**分析對象**: VaultCaddy 超額計費實現狀態

---

## 📊 用戶提供的 Price ID

### ✅ 已在 Stripe 中創建的價格

#### 基本訂閱價格（包含 100 Credits）

**月付計劃** (VaultCaddy Monthly)：
- 🇭🇰 中文版: `price_1SuruFJmiQ31C0GTdJxUaknj` (HKD $38/月)
- 🇺🇸 英文版: `price_1SuruGJmiQ31C0GThdoiTbTM` (USD $4.88/月)
- 🇯🇵 日文版: `price_1SuruGJmiQ31C0GTGQVpiEuP` (JPY ¥788/月)
- 🇰🇷 韓文版: `price_1SuruGJmiQ31C0GTpBz3jbMo` (KRW ₩6,988/月)

**年付計劃** (VaultCaddy Yearly)：
- 🇭🇰 中文版: `price_1SuruEJmiQ31C0GTWqMAZeuM` (HKD $336/年 = $28/月)
- 🇺🇸 英文版: `price_1SuruEJmiQ31C0GTBVhLSAtA` (USD $42.96/年 = $3.58/月)
- 🇯🇵 日文版: `price_1SuruEJmiQ31C0GTde3o97rx` (JPY ¥7,056/年 = ¥588/月)
- 🇰🇷 韓文版: `price_1SuruFJmiQ31C0GTUL0Yxltm` (KRW ₩62,256/年 = ₩5,188/月)

#### 超額收費價格（超出 100 Credits 後按頁計費）

- 🔥 **月付超額收費**: `price_1SfZQQJmiQ31C0GTeUu6TSXE` ($0.3/頁)
- 🔥 **年付超額收費**: `price_1SfZQVJmiQ31C0GTOYgabmaJ` ($0.3/頁)

---

## ✅ 已實現的部分

### 1️⃣ 前端顯示（100% 完成）

#### `billing.html` 系列（4 個版本）
- ✅ 顯示「超出後每頁 HKD/USD/JPY/KRW $0.3」
- ✅ 價格已更新為新定價
- ✅ 所有語言版本一致

#### `stripe-manager.js`
```javascript
// 第 385-415 行
async trackUsageMetered(pagesUsed, subscriptionId) {
    // 呼叫後端 Cloud Function 報告使用量給 Stripe
    const reportUsage = firebase.functions().httpsCallable('reportStripeUsage');
    
    const result = await reportUsage({
        subscriptionId: subscriptionId,
        quantity: pagesUsed,
        timestamp: Date.now()
    });
    
    console.log('✅ 使用量已報告給 Stripe:', result.data);
    return result.data;
}

calculateOverage(totalPagesUsed, includedCredits) {
    const overage = Math.max(0, totalPagesUsed - includedCredits);
    console.log(`📊 使用量計算: 總使用 ${totalPagesUsed} 頁，包含 ${includedCredits} 頁，超出 ${overage} 頁`);
    return overage;
}
```

**狀態**: ✅ 函數已創建，但**未被調用**

---

### 2️⃣ Credits 管理邏輯（70% 完成）

#### `credits-manager.js`

##### ✅ 已實現：Pro Plan 允許負數 Credits

```javascript
// 第 185-189 行
if (planType === 'Pro Plan') {
    console.log('✅ Pro Plan 用戶，允許使用負數 Credits（按量計費）');
    console.log('✅ 跳過 Credits 檢查，允許繼續');
    return true; // 🔥 Pro Plan 用戶可以使用超過 100 Credits
}
```

**解釋**：
- Pro Plan 用戶在 Credits 為 0 時仍可繼續使用
- 系統允許 Credits 變為負數（例如：-50 Credits = 超額使用 50 頁）

##### ✅ 已實現：調用後端扣除 Credits

```javascript
// 第 241-293 行
window.creditsManager.deductCredits = async function(pages) {
    // 🔥 调用后端 Cloud Function 扣除 Credits
    const deductCreditsFunction = firebase.functions().httpsCallable('deductCreditsClient');
    const result = await deductCreditsFunction({
        userId: user.uid,
        amount: pages,
        metadata: {
            source: 'document_upload',
            timestamp: new Date().toISOString()
        }
    });
    
    // 更新本地狀態
    window.creditsManager.currentCredits = result.data.newCredits;
    updateCreditsDisplay(result.data.newCredits);
}
```

**狀態**: ✅ 前端代碼已實現，但**後端函數不存在**

---

## ❌ 缺失的關鍵組件

### 1️⃣ 後端 Firebase Function：`deductCreditsClient`（**不存在**）

**應該實現的功能**：
```javascript
exports.deductCreditsClient = functions.https.onCall(async (data, context) => {
    // 1. 驗證用戶身份
    // 2. 扣除 Credits
    // 3. 檢查是否為 Pro Plan 且 Credits 變為負數
    // 4. 如果超額，報告使用量到 Stripe Billing Meter
    // 5. 返回新的 Credits 餘額
});
```

**當前狀態**: ❌ **完全不存在**

---

### 2️⃣ 後端 Firebase Function：`reportStripeUsage`（**不存在**）

**應該實現的功能**：
```javascript
exports.reportStripeUsage = functions.https.onCall(async (data, context) => {
    const { subscriptionId, quantity } = data;
    
    // 1. 獲取訂閱的計費項 ID
    const subscription = await stripe.subscriptions.retrieve(subscriptionId);
    const subscriptionItemId = subscription.items.data[0].id;
    
    // 2. 報告使用量給 Stripe
    const usageRecord = await stripe.subscriptionItems.createUsageRecord(
        subscriptionItemId,
        { quantity, timestamp: Math.floor(Date.now() / 1000) }
    );
    
    return { success: true, usageRecord };
});
```

**當前狀態**: ❌ **完全不存在**

---

### 3️⃣ Stripe Webhook 處理（**不存在**）

**應該實現的功能**：
- 監聽 `invoice.payment_succeeded` - 每月續費成功後重置 Credits
- 監聽 `customer.subscription.created` - 訂閱創建時初始化 Credits
- 監聽 `customer.subscription.deleted` - 訂閱取消時處理

**當前狀態**: ❌ **完全不存在**

---

### 4️⃣ Firestore 數據結構（**部分存在**）

**當前結構**（`users/{userId}`）：
```json
{
  "credits": 100,
  "currentCredits": 100,
  "planType": "Pro Plan"
}
```

**缺少的字段**：
```json
{
  "subscription": {
    "stripeSubscriptionId": "sub_xxx",      // ❌ 缺少
    "stripePriceId": "price_xxx",           // ❌ 缺少
    "planType": "monthly",                  // ❌ 缺少
    "currency": "hkd",                      // ❌ 缺少
    "monthlyCredits": 100,                  // ❌ 缺少
    "currentPeriodStart": "2026-01-01",     // ❌ 缺少
    "currentPeriodEnd": "2026-02-01"        // ❌ 缺少
  },
  "usageThisPeriod": {
    "totalPages": 150,                      // ❌ 缺少
    "overagePages": 50                      // ❌ 缺少 (150 - 100 免費額度)
  }
}
```

---

## 📊 實現進度總結

| 組件 | 狀態 | 完成度 | 說明 |
|------|------|--------|------|
| **Stripe 價格創建** | ✅ 已完成 | 100% | 8 個基本價格 + 2 個超額價格 |
| **前端價格顯示** | ✅ 已完成 | 100% | 4 個版本 billing.html 已更新 |
| **前端超額顯示** | ✅ 已完成 | 100% | 顯示「$0.3/頁」 |
| **Credits 檢查邏輯** | ✅ 已完成 | 100% | Pro Plan 允許負數 Credits |
| **前端扣費調用** | ✅ 已完成 | 100% | 調用 deductCreditsClient |
| **後端 deductCreditsClient** | ❌ 不存在 | 0% | **需要實現** |
| **後端 reportStripeUsage** | ❌ 不存在 | 0% | **需要實現** |
| **Stripe Webhook** | ❌ 不存在 | 0% | **需要實現** |
| **Firestore 數據結構** | ⚠️ 部分存在 | 40% | 缺少訂閱和使用量字段 |

**總體完成度**: **40%**

---

## 🚀 完成超額計費所需步驟

### 步驟 1: 實現後端 Firebase Functions（3-4 小時）

需要在 `firebase-functions/index.js` 添加：

1. **`deductCreditsClient`** - 扣除 Credits 並檢查超額
2. **`reportStripeUsage`** - 報告使用量給 Stripe
3. **`stripeWebhook`** - 處理 Stripe 事件（續費、重置 Credits）

### 步驟 2: 更新 Firestore 數據結構（1 小時）

在訂閱成功時（Webhook 或 Checkout 成功後）保存：
- `subscription.*` 字段
- `usageThisPeriod.*` 字段

### 步驟 3: 設置 Stripe Webhook（30 分鐘）

1. 部署 `stripeWebhook` 函數
2. 在 Stripe Dashboard 添加 Webhook endpoint
3. 配置 Webhook Secret

### 步驟 4: 測試完整流程（2-3 小時）

1. 測試訂閱流程
2. 測試 Credits 扣除和負數
3. 測試超額計費
4. 測試續費和 Credits 重置

---

## 💡 結論

### 回答用戶問題：「之前已經有做過超額收費的內容，了解後講解是否完成」

**答案：❌ 未完成，僅完成 40%**

#### ✅ 已完成部分：
1. Stripe 價格已創建（包括超額計費 Price ID）
2. 前端顯示已完成（billing.html 顯示 $0.3/頁）
3. 前端邏輯已完成（Pro Plan 允許負數 Credits）
4. 前端調用已實現（調用後端 Cloud Function）

#### ❌ 未完成部分（關鍵）：
1. **後端 Cloud Functions 完全不存在**
   - `deductCreditsClient` - 不存在
   - `reportStripeUsage` - 不存在
   - `stripeWebhook` - 不存在

2. **Firestore 數據結構不完整**
   - 缺少訂閱信息
   - 缺少使用量追蹤

3. **實際計費邏輯未實現**
   - 無法報告使用量給 Stripe
   - 無法處理每月續費和 Credits 重置

#### ⚠️ 當前問題：
**前端代碼會調用不存在的 Cloud Functions，導致錯誤**

當 Pro Plan 用戶嘗試上傳文件時：
```javascript
// 前端嘗試調用...
const deductCreditsFunction = firebase.functions().httpsCallable('deductCreditsClient');
// ❌ 這個函數不存在，會返回錯誤
```

---

## 📝 建議行動

### 選項 A: 完整實現超額計費（推薦）

**時間**: 6-8 小時  
**優勢**: 完整功能，自動計費  
**劣勢**: 需要較長開發和測試時間

### 選項 B: 簡化實現（快速方案）

**時間**: 2-3 小時  
**方案**: 
- 實現 `deductCreditsClient`（僅扣除 Credits，不報告 Stripe）
- Pro Plan 用戶可以負數 Credits
- 手動在 Stripe 中查看用戶使用量並開具發票

**優勢**: 快速上線  
**劣勢**: 需要手動處理超額計費

---

**需要我立即開始實現後端 Firebase Functions 嗎？**

