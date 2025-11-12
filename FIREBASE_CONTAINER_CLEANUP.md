# Firebase Container 清理策略配置

## 📦 什麼是 Container Images？

Firebase Cloud Functions 部署時會創建 Docker container images。這些 images 會佔用 Google Cloud 的存儲空間。

## 💰 費用影響

**Container Registry 存儲費用：**
- 每月前 0.5 GB：免費
- 超過部分：約 $0.026/GB/月

**建議保留天數：**
- 對於小型項目：**7-30 天**已足夠
- 對於中型項目：**30-60 天**
- 對於大型項目：**60-90 天**

## 🎯 VaultCaddy 建議配置

### 方案 1：保守配置（推薦）✅
```
保留天數：30 天
```

**優點：**
- ✅ 足夠的回滾時間
- ✅ 控制存儲成本
- ✅ 適合初期運營

**預估費用：** 幾乎免費（< $1/月）

---

### 方案 2：標準配置
```
保留天數：60 天
```

**優點：**
- ✅ 更長的回滾窗口
- ✅ 符合基礎版數據保留政策

**預估費用：** < $2/月

---

### 方案 3：長期配置
```
保留天數：90 天
```

**優點：**
- ✅ 最長的回滾窗口
- ✅ 符合專業版數據保留政策

**預估費用：** < $3/月

---

## ⚠️ 重要說明

### Container Images ≠ 用戶數據

**Container Images（圖2）：**
- 這是 Cloud Functions 的部署版本
- 只影響 Functions 的回滾能力
- 不影響用戶數據保留

**用戶數據保留（圖3）：**
- 基礎版：60 天
- 專業版：90 天
- 商業版：365 天
- 這是 Firestore 和 Storage 中的用戶文檔數據

### 兩者是獨立的！

```
Container Images 保留 = Functions 版本回滾能力
用戶數據保留 = 用戶文檔在系統中保存時間
```

---

## 🚀 立即操作

### 推薦回答（圖2）：

```
30
```

**理由：**
1. ✅ 足夠的回滾時間（1個月）
2. ✅ 控制存儲成本
3. ✅ 適合初期運營
4. ✅ 隨時可以調整

---

## 📋 完整部署流程

### 步驟 1：回答 Container 清理策略
在終端輸入：
```
30
```

### 步驟 2：等待部署完成
預計時間：2-3 分鐘

### 步驟 3：驗證部署
```bash
firebase functions:list
```

應該看到 8 個 Functions：
- ✅ stripeWebhook
- ✅ monthlyCreditsReset
- ✅ checkExpiredSubscriptions
- ✅ addCreditsManual
- ✅ getCreditsHistory
- ✅ sendVerificationCode
- ✅ verifyCode
- ✅ checkEmailVerified

---

## 🔄 如何實現用戶數據保留策略？

### 方案 1：使用 Firestore TTL（推薦）

創建一個 Cloud Function 定期清理過期數據：

```javascript
// 每天執行一次
exports.cleanupExpiredData = functions.pubsub
    .schedule('0 2 * * *')
    .timeZone('Asia/Hong_Kong')
    .onRun(async (context) => {
        const now = admin.firestore.Timestamp.now();
        
        // 獲取所有用戶
        const usersSnapshot = await db.collection('users').get();
        
        for (const userDoc of usersSnapshot.docs) {
            const userData = userDoc.data();
            const plan = userData.plan || 'free';
            
            // 根據計劃設置保留天數
            let retentionDays;
            switch(plan) {
                case 'basic': retentionDays = 60; break;
                case 'professional': retentionDays = 90; break;
                case 'business': retentionDays = 365; break;
                default: retentionDays = 30; // Free plan
            }
            
            const cutoffDate = new Date();
            cutoffDate.setDate(cutoffDate.getDate() - retentionDays);
            
            // 刪除過期文檔
            const expiredDocs = await db
                .collection('users')
                .doc(userDoc.id)
                .collection('projects')
                .where('createdAt', '<', cutoffDate)
                .get();
            
            for (const doc of expiredDocs.docs) {
                await doc.ref.delete();
                console.log(`🗑️ 刪除過期文檔: ${doc.id}`);
            }
        }
        
        console.log('✅ 數據清理完成');
    });
```

### 方案 2：在前端顯示過期提示

在 `dashboard.html` 中添加過期提示：

```javascript
function checkDocumentExpiration(doc, userPlan) {
    const retentionDays = {
        'free': 30,
        'basic': 60,
        'professional': 90,
        'business': 365
    };
    
    const days = retentionDays[userPlan] || 30;
    const expiryDate = new Date(doc.createdAt);
    expiryDate.setDate(expiryDate.getDate() + days);
    
    const daysUntilExpiry = Math.ceil((expiryDate - new Date()) / (1000 * 60 * 60 * 24));
    
    if (daysUntilExpiry <= 7) {
        return `⚠️ 將在 ${daysUntilExpiry} 天後過期`;
    }
    return null;
}
```

---

## 💡 建議執行順序

### 現在（立即）：
1. 在終端輸入 `30`（回答圖2的問題）
2. 等待 Cloud Functions 部署完成
3. 測試 Email 驗證功能

### 稍後（本週內）：
1. 實現數據清理 Cloud Function
2. 在前端添加過期提示
3. 測試數據保留策略

---

## ❓ 常見問題

### Q1: 如果輸入 30 天，以後可以改嗎？
**A:** 可以！隨時可以在 Firebase Console 或重新部署時修改。

### Q2: Container Images 會影響用戶數據嗎？
**A:** 不會！這只影響 Cloud Functions 的版本回滾能力。

### Q3: 建議輸入多少天？
**A:** 建議 **30 天**，足夠回滾需求且成本低。

### Q4: 用戶數據保留需要現在配置嗎？
**A:** 不需要。可以先完成 Functions 部署，之後再實現數據清理邏輯。

---

**準備好了嗎？請在終端輸入 `30` 繼續部署！** 🚀

