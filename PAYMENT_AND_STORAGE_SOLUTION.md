# 💳 VaultCaddy 支付系統和數據存儲解決方案

## 🎯 **Credits 系統設計**

### 💰 **定價策略**
| 方案 | 月費 Credits | 年費 Credits | 價格 (月) | 價格 (年) |
|------|-------------|-------------|-----------|-----------|
| **基礎** | 200 | 2,400 | $19 | $15/月 |
| **專業** | 500 | 6,000 | $39 | $31/月 |
| **商業** | 1,200 | 14,400 | $79 | $63/月 |

### 🛒 **額外 Credits 購買**
| Credits | 價格 | 每 Credit 成本 | 適用場景 |
|---------|------|---------------|----------|
| 50 | $15 | $0.30 | 臨時需求 |
| 100 | $30 | $0.30 | 中等使用 |
| 200 | $60 | $0.30 | 批量處理 |
| **500** | **$150** | **$0.30** | **企業推薦** |

### ⚡ **Credits 消耗規則**
- **1 頁文檔 = 1 Credit**
- **支援 AI 服務**：
  - ✅ Google Vision API
  - ✅ Google Document AI
  - ✅ 多語言翻譯處理
  - ✅ 智能分類和異常偵測

---

## 🏦 **Stripe 支付整合方案**

### 🚀 **為什麼選擇 Stripe？**

#### ✅ **技術優勢**
- **全球支援**：190+ 國家，135+ 貨幣
- **即時 Webhook**：支付成功立即更新 Credits
- **安全性**：PCI DSS Level 1 認證
- **開發者友善**：優秀的 API 和測試環境

#### 💸 **費用結構**
```
- 線上支付：2.9% + $0.30 per transaction
- 國際卡：+1.5%
- 爭議費用：$15 per dispute
- 無月費，無設置費
```

### 🔧 **Stripe 整合實施**

#### **第一步：Stripe 帳戶設置**
```bash
# 1. 註冊 Stripe 帳戶
https://dashboard.stripe.com/register

# 2. 獲取 API 金鑰
# Test keys (開發階段)
STRIPE_PUBLISHABLE_KEY_TEST="pk_test_..."
STRIPE_SECRET_KEY_TEST="sk_test_..."

# Live keys (生產環境)
STRIPE_PUBLISHABLE_KEY_LIVE="pk_live_..."
STRIPE_SECRET_KEY_LIVE="sk_live_..."
```

#### **第二步：前端 Stripe Checkout 整合**
```javascript
// stripe-checkout.js
class StripePaymentProcessor {
    constructor() {
        this.stripe = Stripe('pk_test_...');  // 您的 Publishable Key
        this.elements = this.stripe.elements();
    }
    
    // 創建 Credits 購買 Session
    async createCreditsCheckoutSession(credits, price) {
        try {
            const response = await fetch('/create-checkout-session', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    credits: credits,
                    amount: price * 100, // Stripe 使用分為單位
                    currency: 'usd',
                    userId: this.getCurrentUserId()
                })
            });
            
            const session = await response.json();
            
            // 重定向到 Stripe Checkout
            const result = await this.stripe.redirectToCheckout({
                sessionId: session.id
            });
            
            if (result.error) {
                console.error('Stripe Checkout error:', result.error);
            }
        } catch (error) {
            console.error('Payment error:', error);
        }
    }
    
    // 處理支付成功回調
    handlePaymentSuccess(sessionId) {
        // 驗證支付並更新 Credits
        this.verifyPaymentAndUpdateCredits(sessionId);
    }
    
    async verifyPaymentAndUpdateCredits(sessionId) {
        try {
            const response = await fetch('/verify-payment', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    sessionId: sessionId,
                    userId: this.getCurrentUserId()
                })
            });
            
            const result = await response.json();
            
            if (result.success) {
                // 更新本地 Credits 顯示
                this.updateCreditsDisplay(result.newCreditsBalance);
                this.showSuccessMessage(result.creditsAdded);
            }
        } catch (error) {
            console.error('Payment verification error:', error);
        }
    }
    
    getCurrentUserId() {
        // 從認證系統獲取當前用戶 ID
        return localStorage.getItem('userId') || 'anonymous';
    }
    
    updateCreditsDisplay(newBalance) {
        const creditsElement = document.querySelector('.stat-value');
        if (creditsElement) {
            creditsElement.textContent = newBalance;
        }
    }
    
    showSuccessMessage(creditsAdded) {
        window.VaultCaddyNavbar.showNotification(
            `成功購買 ${creditsAdded} Credits！`, 
            'success'
        );
    }
}

// 全局實例
window.stripeProcessor = new StripePaymentProcessor();
```

#### **第三步：後端 API 端點 (Node.js + Express)**
```javascript
// server.js
const express = require('express');
const stripe = require('stripe')('sk_test_...');  // 您的 Secret Key
const { Firestore } = require('@google-cloud/firestore');

const app = express();
const db = new Firestore();

// 創建 Checkout Session
app.post('/create-checkout-session', async (req, res) => {
    try {
        const { credits, amount, currency, userId } = req.body;
        
        const session = await stripe.checkout.sessions.create({
            payment_method_types: ['card'],
            line_items: [{
                price_data: {
                    currency: currency,
                    product_data: {
                        name: `${credits} VaultCaddy Credits`,
                        description: `處理 ${credits} 頁文檔的 AI Credits`,
                    },
                    unit_amount: amount,
                },
                quantity: 1,
            }],
            mode: 'payment',
            success_url: `${req.headers.origin}/billing.html?success=true&session_id={CHECKOUT_SESSION_ID}`,
            cancel_url: `${req.headers.origin}/billing.html?canceled=true`,
            metadata: {
                userId: userId,
                credits: credits.toString()
            }
        });
        
        res.json({ id: session.id });
    } catch (error) {
        console.error('Stripe session creation error:', error);
        res.status(500).json({ error: error.message });
    }
});

// Webhook 處理支付成功
app.post('/webhook', express.raw({type: 'application/json'}), async (req, res) => {
    const sig = req.headers['stripe-signature'];
    let event;
    
    try {
        event = stripe.webhooks.constructEvent(req.body, sig, 'whsec_...');
    } catch (err) {
        console.log(`Webhook signature verification failed.`, err.message);
        return res.status(400).send(`Webhook Error: ${err.message}`);
    }
    
    if (event.type === 'checkout.session.completed') {
        const session = event.data.object;
        
        // 提取支付信息
        const userId = session.metadata.userId;
        const creditsToAdd = parseInt(session.metadata.credits);
        
        // 更新用戶 Credits
        await updateUserCredits(userId, creditsToAdd);
    }
    
    res.json({ received: true });
});

// 更新用戶 Credits
async function updateUserCredits(userId, creditsToAdd) {
    try {
        const userRef = db.collection('users').doc(userId);
        
        await db.runTransaction(async (transaction) => {
            const userDoc = await transaction.get(userRef);
            
            if (!userDoc.exists) {
                // 新用戶，創建記錄
                transaction.set(userRef, {
                    credits: creditsToAdd,
                    totalCreditsEverPurchased: creditsToAdd,
                    lastUpdated: new Date()
                });
            } else {
                // 現有用戶，增加 Credits
                const currentCredits = userDoc.data().credits || 0;
                const totalEverPurchased = userDoc.data().totalCreditsEverPurchased || 0;
                
                transaction.update(userRef, {
                    credits: currentCredits + creditsToAdd,
                    totalCreditsEverPurchased: totalEverPurchased + creditsToAdd,
                    lastUpdated: new Date()
                });
            }
        });
        
        console.log(`Successfully added ${creditsToAdd} credits to user ${userId}`);
    } catch (error) {
        console.error('Error updating user credits:', error);
        throw error;
    }
}

app.listen(3000, () => console.log('Server running on port 3000'));
```

---

## ☁️ **Google Cloud 數據存儲方案**

### 🗃️ **推薦架構：Firestore + Cloud Storage**

#### **為什麼選擇這個組合？**
- ✅ **Firestore**：實時數據庫，完美處理 Credits 交易
- ✅ **Cloud Storage**：安全存儲處理後的文檔
- ✅ **無縫整合**：與 Google AI 服務天然整合
- ✅ **自動擴展**：根據使用量自動調整

### 📊 **數據結構設計**

#### **Firestore 集合結構**
```javascript
// /users/{userId}
{
    email: "user@example.com",
    displayName: "John Doe",
    credits: 150,                    // 當前 Credits 餘額
    totalCreditsEverPurchased: 500,  // 總購買 Credits
    subscriptionPlan: "pro",         // 訂閱方案
    subscriptionCredits: 500,        // 方案包含的月度 Credits
    subscriptionRenewsAt: "2024-02-01",
    createdAt: "2024-01-01T00:00:00Z",
    lastLoginAt: "2024-01-15T10:30:00Z"
}

// /transactions/{transactionId}
{
    userId: "user123",
    type: "purchase",              // purchase, consumption, subscription
    credits: 100,
    amount: 30.00,                 // 僅購買交易有此欄位
    currency: "USD",
    stripeSessionId: "cs_...",
    status: "completed",
    createdAt: "2024-01-15T10:30:00Z"
}

// /documents/{documentId}
{
    userId: "user123",
    originalFileName: "bank_statement.pdf",
    storagePath: "documents/user123/2024/01/doc123.pdf",
    processedDataPath: "processed/user123/2024/01/doc123.json",
    documentType: "bank-statement",
    pagesProcessed: 3,
    creditsUsed: 3,
    aiService: "google-document-ai",
    processingTime: 2500,          // 毫秒
    accuracy: 0.98,
    status: "completed",
    createdAt: "2024-01-15T10:30:00Z"
}
```

#### **Cloud Storage 目錄結構**
```
vaultcaddy-documents/
├── documents/              # 原始文檔
│   └── {userId}/
│       └── {year}/
│           └── {month}/
│               └── {documentId}.pdf
├── processed/              # 處理後的數據
│   └── {userId}/
│       └── {year}/
│           └── {month}/
│               ├── {documentId}.json
│               ├── {documentId}.csv
│               └── {documentId}.xlsx
└── temp/                   # 臨時文件（24小時後自動刪除）
    └── {sessionId}/
        └── uploads/
```

### 🔧 **實施代碼**

#### **Credits 管理系統**
```javascript
// credits-manager.js
class CreditsManager {
    constructor() {
        this.db = new Firestore();
    }
    
    // 檢查用戶是否有足夠 Credits
    async checkCreditsAvailable(userId, requiredCredits) {
        try {
            const userRef = this.db.collection('users').doc(userId);
            const userDoc = await userRef.get();
            
            if (!userDoc.exists) {
                return { available: false, currentCredits: 0 };
            }
            
            const currentCredits = userDoc.data().credits || 0;
            return {
                available: currentCredits >= requiredCredits,
                currentCredits: currentCredits
            };
        } catch (error) {
            console.error('Error checking credits:', error);
            return { available: false, currentCredits: 0 };
        }
    }
    
    // 消耗 Credits
    async consumeCredits(userId, creditsToConsume, documentId, aiService) {
        try {
            const userRef = this.db.collection('users').doc(userId);
            
            await this.db.runTransaction(async (transaction) => {
                const userDoc = await transaction.get(userRef);
                
                if (!userDoc.exists) {
                    throw new Error('User not found');
                }
                
                const currentCredits = userDoc.data().credits || 0;
                
                if (currentCredits < creditsToConsume) {
                    throw new Error('Insufficient credits');
                }
                
                // 更新用戶 Credits
                transaction.update(userRef, {
                    credits: currentCredits - creditsToConsume,
                    lastUpdated: new Date()
                });
                
                // 記錄交易
                const transactionRef = this.db.collection('transactions').doc();
                transaction.set(transactionRef, {
                    userId: userId,
                    type: 'consumption',
                    credits: -creditsToConsume,
                    documentId: documentId,
                    aiService: aiService,
                    status: 'completed',
                    createdAt: new Date()
                });
            });
            
            console.log(`Successfully consumed ${creditsToConsume} credits for user ${userId}`);
            return { success: true };
        } catch (error) {
            console.error('Error consuming credits:', error);
            return { success: false, error: error.message };
        }
    }
    
    // 獲取用戶 Credits 餘額
    async getUserCredits(userId) {
        try {
            const userRef = this.db.collection('users').doc(userId);
            const userDoc = await userRef.get();
            
            if (!userDoc.exists) {
                return 0;
            }
            
            return userDoc.data().credits || 0;
        } catch (error) {
            console.error('Error getting user credits:', error);
            return 0;
        }
    }
    
    // 月度 Credits 重置（訂閱用戶）
    async resetMonthlyCredits(userId) {
        try {
            const userRef = this.db.collection('users').doc(userId);
            const userDoc = await userRef.get();
            
            if (!userDoc.exists) {
                return;
            }
            
            const userData = userDoc.data();
            const subscriptionCredits = userData.subscriptionCredits || 0;
            const currentCredits = userData.credits || 0;
            
            // 只有當訂閱 Credits 大於當前 Credits 時才重置
            if (subscriptionCredits > currentCredits) {
                await userRef.update({
                    credits: subscriptionCredits,
                    lastMonthlyReset: new Date()
                });
            }
        } catch (error) {
            console.error('Error resetting monthly credits:', error);
        }
    }
}

// 全局實例
window.creditsManager = new CreditsManager();
```

#### **文檔處理整合**
```javascript
// ai-processor-with-credits.js
class AIProcessorWithCredits extends AIDocumentProcessor {
    constructor() {
        super();
        this.creditsManager = new CreditsManager();
        this.storageManager = new StorageManager();
    }
    
    async processDocumentWithCredits(file, documentType, userId, options = {}) {
        try {
            // 計算需要的 Credits（按頁數）
            const pagesCount = await this.estimatePageCount(file);
            const requiredCredits = pagesCount;
            
            // 檢查 Credits 是否足夠
            const creditsCheck = await this.creditsManager.checkCreditsAvailable(userId, requiredCredits);
            
            if (!creditsCheck.available) {
                throw new Error(`需要 ${requiredCredits} Credits，但您只有 ${creditsCheck.currentCredits} Credits`);
            }
            
            // 先消耗 Credits
            const consumeResult = await this.creditsManager.consumeCredits(
                userId, 
                requiredCredits, 
                null, // documentId 將在處理後生成
                'google-document-ai'
            );
            
            if (!consumeResult.success) {
                throw new Error(consumeResult.error);
            }
            
            // 處理文檔
            const result = await this.processDocument(file, documentType, options);
            
            if (result.success) {
                // 保存處理結果到 Cloud Storage
                const documentId = await this.storageManager.saveProcessedDocument(
                    userId,
                    file,
                    result.data,
                    result.formats
                );
                
                // 更新 Firestore 記錄
                await this.saveDocumentRecord(userId, documentId, file, pagesCount, result);
                
                // 更新 UI 顯示的 Credits
                const newCreditsBalance = await this.creditsManager.getUserCredits(userId);
                this.updateCreditsDisplay(newCreditsBalance);
                
                return {
                    ...result,
                    documentId: documentId,
                    creditsUsed: requiredCredits,
                    remainingCredits: newCreditsBalance
                };
            } else {
                // 處理失敗，退還 Credits
                await this.refundCredits(userId, requiredCredits);
                throw new Error(result.error);
            }
            
        } catch (error) {
            console.error('AI processing with credits failed:', error);
            this.showErrorStatus(file.name, error.message);
            return {
                success: false,
                error: error.message
            };
        }
    }
    
    async estimatePageCount(file) {
        // 簡單估算：每 100KB 約 1 頁
        const fileSizeMB = file.size / (1024 * 1024);
        const estimatedPages = Math.max(1, Math.ceil(fileSizeMB * 10));
        return estimatedPages;
    }
    
    async refundCredits(userId, credits) {
        // 實施 Credits 退款邏輯
        const userRef = this.creditsManager.db.collection('users').doc(userId);
        await userRef.update({
            credits: FieldValue.increment(credits)
        });
    }
    
    updateCreditsDisplay(newBalance) {
        const creditsElement = document.querySelector('.stat-value');
        if (creditsElement) {
            creditsElement.textContent = newBalance;
        }
    }
}
```

---

## 📊 **成本分析**

### 💰 **Google Cloud 預估成本 (月)**

#### **Firestore**
```
- 讀取：$0.06 per 100K
- 寫入：$0.18 per 100K
- 刪除：$0.02 per 100K
- 存儲：$0.18 per GB/month

預估：1000 用戶，每月 10,000 文檔處理
≈ $20-30/月
```

#### **Cloud Storage**
```
- 標準存儲：$0.020 per GB/month
- 操作費用：$0.05 per 10K operations

預估：100GB 存儲，50K 操作/月
≈ $10-15/月
```

#### **總計：$30-45/月** (遠低於收入)

### 💳 **Stripe 成本**
```
- 基本費率：2.9% + $0.30
- 月收入 $10,000 預估手續費：≈ $320

投資回報率：收入 $10,000 - 手續費 $320 - 雲端 $45 = $9,635 淨收入
```

---

## 🚀 **部署時程表**

### 📅 **第 1 週：基礎設置**
- [ ] Stripe 帳戶設置和測試
- [ ] Google Cloud 項目配置
- [ ] Firestore 數據庫結構設計

### 📅 **第 2 週：支付整合**
- [ ] Stripe Checkout 前端整合
- [ ] Webhook 端點實施
- [ ] Credits 購買流程測試

### 📅 **第 3 週：Credits 系統**
- [ ] Credits 管理邏輯實施
- [ ] AI 處理與 Credits 消耗整合
- [ ] 餘額顯示和通知系統

### 📅 **第 4 週：數據存儲**
- [ ] Cloud Storage 整合
- [ ] 文檔處理結果保存
- [ ] 用戶數據管理界面

### 📅 **第 5 週：測試和上線**
- [ ] 完整流程測試
- [ ] 安全性檢查
- [ ] 生產環境部署

這個完整的解決方案將為 VaultCaddy 提供專業級的支付和數據管理能力！
