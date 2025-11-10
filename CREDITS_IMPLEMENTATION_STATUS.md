# Credits 管理系統實現進度

## ✅ 已完成功能

### 1. Cloud Functions 自動處理 Credits ✅

**文件：** `firebase-functions/index.js`

**實現功能：**
- ✅ Stripe Webhook 處理（支付成功、訂閱變更）
- ✅ 自動添加 Credits（購買後）
- ✅ 自動扣除 Credits（使用時）
- ✅ 訂閱計劃管理
- ✅ 每月 Credits 重置（定時任務）
- ✅ 檢查過期訂閱（每6小時）
- ✅ Credits 歷史記錄

**部署指南：** `CLOUD_FUNCTIONS_SETUP.md`

---

### 2. Credits 購買記錄 UI ✅

**文件：** `billing.html`

**實現功能：**
- ✅ 購買記錄表格（日期、描述、類型、Credits、餘額）
- ✅ 按月份過濾功能
- ✅ 白色背景設計

---

## 🔄 待實現功能

### 3. Credits 過期機制顯示 - account.html

**需要實現：**
- [ ] 在 account.html 的「目前計劃」區域顯示 Credits 使用情況
- [ ] 類似圖片中的進度條（500 / 500）
- [ ] 顯示「Included-Request Usage」
- [ ] 顯示「Usage included in your plan」
- [ ] 顯示重置日期「Resets 2025年11月4日」
- [ ] 白色背景設計

**計劃對應的 Credits：**
- Free Plan: 0 Credits
- Basic Plan: 200 Credits/月 (2,400 Credits/年)
- Pro Plan: 500 Credits/月 (6,000 Credits/年)  
- Business Plan: 1,200 Credits/月 (14,400 Credits/年)

---

### 4. Stripe 充值功能集成

**需要實現：**
- [ ] 將 https://buy.stripe.com/aFa3cwga8alc1CSeIOf7i03 集成到購買流程
- [ ] 點擊「購買 Credits」按鈕時跳轉到 Stripe Checkout
- [ ] 支付成功後自動添加 Credits
- [ ] 使用 Stripe Customer Portal 管理訂閱

---

### 5. 載入 Credits 歷史記錄

**需要實現：**
- [ ] 從 Firebase Cloud Functions 獲取 Credits 歷史
- [ ] 在 billing.html 表格中顯示記錄
- [ ] 按月份過濾功能
- [ ] 分頁功能（如果記錄很多）

---

## 📋 實現建議

### 優先級 1：Credits 過期機制顯示（account.html）

這是用戶最常看到的頁面，應該優先實現。

**實現步驟：**
1. 修改 account.html 的「目前計劃」區域
2. 從 Firestore 讀取用戶的訂閱信息
3. 計算 Credits 使用百分比
4. 顯示進度條和到期日期
5. 添加「升級計劃」按鈕

**示例代碼：**
```javascript
async function loadSubscriptionStatus() {
    const user = firebase.auth().currentUser;
    const userDoc = await firebase.firestore()
        .collection('users')
        .doc(user.uid)
        .get();
    
    const userData = userDoc.data();
    const subscription = userData.subscription || {};
    
    // 顯示 Credits 使用情況
    const credits = userData.credits || 0;
    const monthlyCredits = subscription.monthlyCredits || 0;
    const percentage = (credits / monthlyCredits) * 100;
    
    // 更新 UI
    document.getElementById('credits-used').textContent = credits;
    document.getElementById('credits-total').textContent = monthlyCredits;
    document.getElementById('credits-progress').style.width = percentage + '%';
    
    // 顯示重置日期
    if (subscription.currentPeriodEnd) {
        const resetDate = subscription.currentPeriodEnd.toDate();
        document.getElementById('reset-date').textContent = 
            resetDate.toLocaleDateString('zh-TW', { 
                year: 'numeric', 
                month: 'long', 
                day: 'numeric' 
            });
    }
}
```

---

### 優先級 2：Stripe 充值功能

這是收入來源，應該盡快實現。

**實現步驟：**
1. 在 Stripe Dashboard 創建產品和價格
2. 獲取 Stripe Checkout URL 或 Price ID
3. 修改 `purchaseCredits()` 函數，跳轉到 Stripe
4. 設置 Stripe Webhook 接收付款成功通知
5. Cloud Functions 自動添加 Credits

**示例代碼：**
```javascript
async function purchaseCredits(credits, price) {
    try {
        const user = firebase.auth().currentUser;
        
        // 創建 Stripe Checkout Session
        const response = await fetch('YOUR_CLOUD_FUNCTION_URL/createCheckoutSession', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                userId: user.uid,
                credits: credits,
                amount: price,
                successUrl: window.location.origin + '/billing.html?success=true',
                cancelUrl: window.location.origin + '/billing.html?cancel=true'
            })
        });
        
        const { sessionId } = await response.json();
        
        // 跳轉到 Stripe Checkout
        const stripe = Stripe('YOUR_PUBLISHABLE_KEY');
        await stripe.redirectToCheckout({ sessionId });
        
    } catch (error) {
        console.error('創建支付失敗:', error);
        alert('創建支付失敗，請重試');
    }
}
```

---

### 優先級 3：載入 Credits 歷史記錄

這是補充功能，可以最後實現。

**實現步驟：**
1. 調用 Cloud Functions 的 `getCreditsHistory`
2. 在 billing.html 表格中渲染數據
3. 實現按月份過濾
4. 添加分頁功能

**示例代碼：**
```javascript
async function loadCreditsHistory() {
    try {
        const getHistory = firebase.functions().httpsCallable('getCreditsHistory');
        const result = await getHistory({ limit: 50 });
        
        const history = result.data.history;
        const tbody = document.getElementById('credits-history-tbody');
        
        if (history.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="5" style="text-align: center; padding: 2rem; color: #9ca3af;">
                        暫無記錄
                    </td>
                </tr>
            `;
            return;
        }
        
        tbody.innerHTML = history.map(record => {
            const date = new Date(record.createdAt).toLocaleDateString('zh-TW');
            const type = record.type === 'add' ? '增加' : 
                        record.type === 'deduct' ? '使用' : '重置';
            const typeColor = record.type === 'add' ? '#10b981' : 
                            record.type === 'deduct' ? '#ef4444' : '#6b7280';
            const sign = record.type === 'add' ? '+' : 
                        record.type === 'deduct' ? '-' : '';
            
            return `
                <tr style="border-bottom: 1px solid #e5e7eb;">
                    <td style="padding: 1rem; color: #6b7280; font-size: 0.875rem;">${date}</td>
                    <td style="padding: 1rem; color: #1f2937;">
                        ${record.metadata?.source === 'subscription' ? '訂閱計劃' : 
                          record.metadata?.source === 'purchase' ? '購買 Credits' : 
                          record.metadata?.projectName || '文檔處理'}
                    </td>
                    <td style="padding: 1rem; text-align: center;">
                        <span style="display: inline-flex; padding: 0.25rem 0.75rem; background: ${typeColor}15; color: ${typeColor}; border-radius: 12px; font-size: 0.875rem; font-weight: 500;">
                            ${type}
                        </span>
                    </td>
                    <td style="padding: 1rem; text-align: right; font-weight: 600; color: ${typeColor};">
                        ${sign}${record.amount}
                    </td>
                    <td style="padding: 1rem; text-align: right; color: #1f2937;">
                        ${record.after}
                    </td>
                </tr>
            `;
        }).join('');
        
    } catch (error) {
        console.error('載入歷史記錄失敗:', error);
    }
}
```

---

## 🚀 下一步行動

1. **部署 Cloud Functions**
   ```bash
   cd firebase-functions
   npm install
   firebase deploy --only functions
   ```

2. **配置 Stripe Webhook**
   - 在 Stripe Dashboard 設置 Webhook URL
   - 監聽必要的事件

3. **實現 account.html 的 Credits 顯示**
   - 最直觀的用戶體驗改進

4. **集成 Stripe 支付**
   - 實現真實的收入功能

5. **測試完整流程**
   - 購買 Credits
   - 使用 Credits
   - 訂閱計劃
   - Credits 重置

---

## 📞 需要幫助？

如果需要我繼續實現剩餘功能，請告訴我：
1. 優先實現哪個功能？
2. 是否需要修改設計？
3. 是否有其他要求？

