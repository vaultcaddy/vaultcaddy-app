#!/usr/bin/env node
/**
 * 删除旧价格并重新创建多货币价格
 * 使用 currency_options 在一个 Price 对象中支持多种货币
 */

const stripeSecretKey = process.argv[2];

if (!stripeSecretKey) {
    console.error('❌ 错误：请提供 Stripe Secret Key');
    process.exit(1);
}

const stripe = require('stripe')(stripeSecretKey);

// 刚才创建的价格 ID
const pricesToDelete = [
    'price_1SnF1SJmiQ31C0GTZCQntCRf', // Monthly HKD
    'price_1SnF1TJmiQ31C0GTPO0wAQBq', // Monthly USD
    'price_1SnF1TJmiQ31C0GTAQ7w1wqQ', // Monthly JPY
    'price_1SnF1UJmiQ31C0GTok9B24Ob', // Monthly KRW
    'price_1SnF1UJmiQ31C0GTgHOSMEZp', // Monthly EUR
    'price_1SnF1UJmiQ31C0GTyv4v1k9p', // Monthly GBP
    'price_1SnF1VJmiQ31C0GTqN5n4Baf', // Yearly HKD
    'price_1SnF1VJmiQ31C0GTx5eSL7FR', // Yearly USD
    'price_1SnF1WJmiQ31C0GTI9eWWDiZ', // Yearly JPY
    'price_1SnF1WJmiQ31C0GTbAVLIoKH', // Yearly KRW
    'price_1SnF1WJmiQ31C0GTvtmIFJJL', // Yearly EUR
    'price_1SnF1XJmiQ31C0GTFkXv4Vmd'  // Yearly GBP
];

const MONTHLY_PRODUCT = 'prod_Tb24SiE4usHRDS';
const YEARLY_PRODUCT = 'prod_Tb2443GvCbe4Pp';

async function main() {
    console.log('🗑️  步骤 1: 删除旧价格\n');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
    
    // 停用所有刚创建的价格
    for (const priceId of pricesToDelete) {
        try {
            await stripe.prices.update(priceId, { active: false });
            console.log(`✅ 已停用: ${priceId}`);
        } catch (error) {
            console.log(`⚠️  无法停用 ${priceId}: ${error.message}`);
        }
    }
    
    console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
    console.log('🆕 步骤 2: 创建多货币价格\n');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
    
    // 创建 Monthly 价格（支持 6 种货币）
    console.log('📋 创建 VaultCaddy Monthly（包含 6 种货币）');
    console.log('   🇨🇳 HKD $28/月');
    console.log('   🇺🇸 USD $3.88/月');
    console.log('   🇯🇵 JPY ¥599/月');
    console.log('   🇰🇷 KRW ₩5,588/월');
    console.log('   🇪🇺 EUR €3.28/月');
    console.log('   🇬🇧 GBP £2.88/月\n');
    
    const monthlyPrice = await stripe.prices.create({
        product: MONTHLY_PRODUCT,
        currency: 'hkd',
        unit_amount: 2800,
        recurring: {
            interval: 'month'
        },
        currency_options: {
            usd: {
                unit_amount: 388
            },
            jpy: {
                unit_amount: 599
            },
            krw: {
                unit_amount: 5588
            },
            eur: {
                unit_amount: 328
            },
            gbp: {
                unit_amount: 288
            }
        },
        metadata: {
            plan_type: 'starter_monthly',
            credits: '100',
            monthly_credits: '100',
            created_at: new Date().toISOString()
        }
    });
    console.log(`✅ Monthly 价格创建成功！Price ID: ${monthlyPrice.id}\n`);
    
    // 创建 Yearly 价格（支持 6 种货币）
    console.log('📋 创建 VaultCaddy Yearly（包含 6 种货币）');
    console.log('   🇨🇳 HKD $264/年（每月 $22）');
    console.log('   🇺🇸 USD $34.56/年（每月 $2.88）');
    console.log('   🇯🇵 JPY ¥5,748/年（每月 ¥479）');
    console.log('   🇰🇷 KRW ₩53,616/년（每月 ₩4,468）');
    console.log('   🇪🇺 EUR €29.76/年（每月 €2.48）');
    console.log('   🇬🇧 GBP £22.56/年（每月 £1.88）\n');
    
    const yearlyPrice = await stripe.prices.create({
        product: YEARLY_PRODUCT,
        currency: 'hkd',
        unit_amount: 26400,
        recurring: {
            interval: 'year'
        },
        currency_options: {
            usd: {
                unit_amount: 3456
            },
            jpy: {
                unit_amount: 5748
            },
            krw: {
                unit_amount: 53616
            },
            eur: {
                unit_amount: 2976
            },
            gbp: {
                unit_amount: 2256
            }
        },
        metadata: {
            plan_type: 'starter_yearly',
            credits: '1200',
            monthly_credits: '100',
            created_at: new Date().toISOString()
        }
    });
    console.log(`✅ Yearly 价格创建成功！Price ID: ${yearlyPrice.id}\n`);
    
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('✅ 完成！\n');
    console.log('📦 新创建的价格（每个支持 6 种货币）：\n');
    console.log(`   Monthly: ${monthlyPrice.id}`);
    console.log(`            ├─ HKD $28/月`);
    console.log(`            ├─ USD $3.88/月`);
    console.log(`            ├─ JPY ¥599/月`);
    console.log(`            ├─ KRW ₩5,588/월`);
    console.log(`            ├─ EUR €3.28/月`);
    console.log(`            └─ GBP £2.88/月\n`);
    
    console.log(`   Yearly:  ${yearlyPrice.id}`);
    console.log(`            ├─ HKD $264/年`);
    console.log(`            ├─ USD $34.56/年`);
    console.log(`            ├─ JPY ¥5,748/年`);
    console.log(`            ├─ KRW ₩53,616/년`);
    console.log(`            ├─ EUR €29.76/年`);
    console.log(`            └─ GBP £22.56/年\n`);
    
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
    console.log('📝 下一步：');
    console.log('1. 访问 Stripe Dashboard 验证价格');
    console.log('2. 应该看到每个价格都支持 6 种货币');
    console.log('3. 在 Dashboard 中会显示类似图1-4的效果\n');
    
    console.log('💾 JSON 格式：\n');
    console.log(JSON.stringify({
        monthly: {
            priceId: monthlyPrice.id,
            productId: MONTHLY_PRODUCT
        },
        yearly: {
            priceId: yearlyPrice.id,
            productId: YEARLY_PRODUCT
        }
    }, null, 2));
    console.log('\n');
}

main().catch(error => {
    console.error('❌ 错误:', error.message);
    if (error.raw) {
        console.error('详细信息:', JSON.stringify(error.raw, null, 2));
    }
    process.exit(1);
});
