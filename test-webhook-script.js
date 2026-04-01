/**
 * Stripe Webhook 測試腳本
 * 用途：自動發送測試請求到 stripeWebhook 函數
 * 
 * 使用方法：
 * node test-webhook-script.js
 */

const https = require('https');
const crypto = require('crypto');

// Firebase Function URL
const WEBHOOK_URL = 'https://us-central1-vaultcaddy-production-cbbe2.cloudfunctions.net/stripeWebhook';

// 模擬 Stripe 測試事件
const testEvent = {
    id: 'evt_test_webhook_' + Date.now(),
    object: 'event',
    api_version: '2023-10-16',
    created: Math.floor(Date.now() / 1000),
    data: {
        object: {
            id: 'in_test_' + Date.now(),
            object: 'invoice',
            amount_due: 5300, // $53.00 (月費 $38 + 超額 $15)
            amount_paid: 5300,
            billing_reason: 'subscription_cycle',
            currency: 'hkd',
            customer: 'cus_test_123',
            subscription: 'sub_test_123',
            status: 'paid'
        }
    },
    livemode: false,
    pending_webhooks: 1,
    request: {
        id: null,
        idempotency_key: null
    },
    type: 'invoice.payment_succeeded'
};

// 發送測試請求
function sendTestWebhook() {
    const payload = JSON.stringify(testEvent);
    
    console.log('🚀 發送測試 Webhook...');
    console.log('📍 URL:', WEBHOOK_URL);
    console.log('📦 事件類型:', testEvent.type);
    console.log('');

    const url = new URL(WEBHOOK_URL);
    const options = {
        hostname: url.hostname,
        port: 443,
        path: url.pathname,
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Content-Length': Buffer.byteLength(payload),
            'User-Agent': 'Stripe/1.0 (+https://stripe.com/docs/webhooks)',
            // 注意：這裡缺少 Stripe-Signature，Firebase Function 會返回錯誤
            // 這是正常的，因為我們只是測試連接性
        }
    };

    const req = https.request(options, (res) => {
        let data = '';

        console.log('📊 響應狀態:', res.statusCode);
        console.log('📋 響應頭:', JSON.stringify(res.headers, null, 2));
        console.log('');

        res.on('data', (chunk) => {
            data += chunk;
        });

        res.on('end', () => {
            console.log('📥 響應內容:', data || '(空)');
            console.log('');

            if (res.statusCode === 200) {
                console.log('✅ Webhook 端點正常工作！');
            } else if (res.statusCode === 400 && data.includes('signature')) {
                console.log('✅ Webhook 端點正常工作！');
                console.log('ℹ️  簽名驗證失敗是預期的（因為這是測試請求）');
            } else {
                console.log('⚠️  意外的響應狀態碼');
            }
            console.log('');
            console.log('🎯 下一步：請到 Stripe Dashboard 發送真實的測試事件');
            console.log('   https://dashboard.stripe.com/webhooks');
        });
    });

    req.on('error', (error) => {
        console.error('❌ 請求失敗:', error.message);
        console.log('');
        console.log('🔍 可能的原因：');
        console.log('   1. Firebase Function 尚未完全部署');
        console.log('   2. 網絡連接問題');
        console.log('   3. URL 錯誤');
    });

    req.write(payload);
    req.end();
}

// 執行測試
console.log('═══════════════════════════════════════════════════');
console.log('  Stripe Webhook 連接性測試');
console.log('═══════════════════════════════════════════════════');
console.log('');

sendTestWebhook();


