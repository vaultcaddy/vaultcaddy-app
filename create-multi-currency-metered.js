#!/usr/bin/env node

/**
 * 为多个币种创建 Metered Price
 * 
 * 使用方法：
 * node create-multi-currency-metered.js <stripe_secret_key> <product_id>
 */

const stripeSecretKey = process.argv[2];
const productId = process.argv[3];

// 币种配置
const currencies = {
    hkd: {
        name: 'HKD',
        free_tier: 100,
        overage_price: 50 // 0.50 HKD
    },
    usd: {
        name: 'USD',
        free_tier: 100,
        overage_price: 6 // 0.06 USD
    },
    eur: {
        name: 'EUR',
        free_tier: 100,
        overage_price: 6 // 0.06 EUR
    },
    gbp: {
        name: 'GBP',
        free_tier: 100,
        overage_price: 5 // 0.05 GBP
    },
    jpy: {
        name: 'JPY',
        free_tier: 100,
        overage_price: 9 // 9 JPY
    }
};

async function main() {
    if (!stripeSecretKey || !productId) {
        console.error('使用方法：node create-multi-currency-metered.js <stripe_secret_key> <product_id>');
        process.exit(1);
    }

    console.log('🚀 为多个币种创建 Metered Price\n');
    
    const stripe = require('stripe')(stripeSecretKey);
    console.log('✅ Stripe 客户端已初始化\n');
    
    // 获取或创建 Meter
    console.log('📋 步骤 1：获取或创建 Meter...\n');
    
    const meters = await stripe.billing.meters.list({ limit: 100 });
    let meter = meters.data.find(m => m.event_name === 'vaultcaddy_credit_usage');
    
    if (!meter) {
        meter = await stripe.billing.meters.create({
            display_name: 'VaultCaddy Credits 使用量',
            event_name: 'vaultcaddy_credit_usage',
            default_aggregation: {
                formula: 'sum'
            }
        });
        console.log('✅ Meter 创建成功！');
    } else {
        console.log('✅ 找到现有的 Meter！');
    }
    console.log(`   Meter ID: ${meter.id}\n`);
    
    // 为每个币种创建 Metered Price
    console.log('📋 步骤 2：为每个币种创建 Metered Price...\n');
    
    const createdPrices = [];
    
    for (const [code, config] of Object.entries(currencies)) {
        console.log(`\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
        console.log(`创建 ${config.name} Metered Price...`);
        console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
        
        try {
            const price = await stripe.prices.create({
                product: productId,
                currency: code,
                recurring: {
                    interval: 'month',
                    usage_type: 'metered',
                    meter: meter.id
                },
                billing_scheme: 'tiered',
                tiers_mode: 'graduated',
                tiers: [
                    {
                        up_to: config.free_tier,
                        unit_amount: 0
                    },
                    {
                        up_to: 'inf',
                        unit_amount: config.overage_price
                    }
                ],
                metadata: {
                    type: 'metered_credits',
                    currency: code.toUpperCase(),
                    description: `超额 Credits 按量计费 (${config.name})`
                }
            });
            
            console.log(`✅ ${config.name} Metered Price 创建成功！`);
            console.log(`   Price ID: ${price.id}`);
            console.log(`   分层定价:`);
            console.log(`   ├─ 第 1-${config.free_tier} 个 Credits: 0.00 ${config.name}`);
            console.log(`   └─ 第 ${config.free_tier + 1}+ 个 Credits: ${(config.overage_price / 100).toFixed(2)} ${config.name}`);
            
            createdPrices.push({
                currency: config.name,
                priceId: price.id
            });
            
        } catch (error) {
            console.error(`❌ 创建 ${config.name} Metered Price 失败:`, error.message);
        }
    }
    
    // 总结
    console.log('\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('🎉 配置完成！');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
    
    console.log('📊 创建的 Metered Prices:\n');
    createdPrices.forEach(p => {
        console.log(`   ${p.currency}: ${p.priceId}`);
    });
    
    console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('📋 下一步：');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('1. 根据用户选择的币种，将对应的 Fixed Price 添加到订阅');
    console.log('2. 同时将对应的 Metered Price 添加到订阅');
    console.log('3. 存储 Subscription Item ID 到 Firestore\n');
}

main().catch(error => {
    console.error('❌ 发生错误:', error);
    process.exit(1);
});

