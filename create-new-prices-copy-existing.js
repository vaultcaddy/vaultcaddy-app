#!/usr/bin/env node
/**
 * 为现有 Stripe 产品创建新价格
 * 复制现有价格的所有设置，只更新价格金额
 * 
 * 使用方法：
 * node create-new-prices-copy-existing.js <stripe_secret_key> <product_id>
 * 
 * 例如：
 * node create-new-prices-copy-existing.js sk_live_xxx prod_Tb2443GvCbe4Pp
 */

const stripeSecretKey = process.argv[2];
const productId = process.argv[3];

if (!stripeSecretKey || !productId) {
    console.error('❌ 使用方法：node create-new-prices-copy-existing.js <stripe_secret_key> <product_id>');
    console.error('   例如：node create-new-prices-copy-existing.js sk_live_xxx prod_Tb2443GvCbe4Pp');
    process.exit(1);
}

const stripe = require('stripe')(stripeSecretKey);

// 新价格配置（根据单层定价方案）
const newPricing = {
    hkd: {
        monthly: 2800,  // $28.00 HKD
        yearly: 26400   // $264.00 HKD/年 (每月 $22)
    },
    usd: {
        monthly: 388,   // $3.88 USD
        yearly: 3456    // $34.56 USD/年 (每月 $2.88)
    },
    jpy: {
        monthly: 599,   // ¥599 JPY
        yearly: 5748    // ¥5,748 JPY/年 (每月 ¥479)
    },
    krw: {
        monthly: 5588,  // ₩5,588 KRW
        yearly: 53616   // ₩53,616 KRW/年 (每月 ₩4,468)
    }
};

async function getProductAndPrices(productId) {
    try {
        // 获取产品信息
        const product = await stripe.products.retrieve(productId);
        console.log(`\n📦 产品: ${product.name}`);
        console.log(`   Product ID: ${product.id}\n`);
        
        // 获取所有价格（包括激活和停用的）
        const prices = await stripe.prices.list({
            product: productId,
            limit: 100
        });
        
        console.log(`💰 找到 ${prices.data.length} 个价格\n`);
        
        // 按货币和周期分组
        const pricesByCurrency = {};
        
        prices.data.forEach(price => {
            const currency = price.currency.toLowerCase();
            const interval = price.recurring?.interval || 'one_time';
            
            if (!pricesByCurrency[currency]) {
                pricesByCurrency[currency] = {};
            }
            if (!pricesByCurrency[currency][interval]) {
                pricesByCurrency[currency][interval] = [];
            }
            
            pricesByCurrency[currency][interval].push(price);
        });
        
        // 显示现有价格
        console.log('📋 现有价格分组：\n');
        for (const [currency, intervals] of Object.entries(pricesByCurrency)) {
            console.log(`   ${currency.toUpperCase()}:`);
            for (const [interval, priceList] of Object.entries(intervals)) {
                console.log(`     ${interval}: ${priceList.length} 个价格`);
                priceList.forEach((price, idx) => {
                    const amount = price.unit_amount || 0;
                    const amountDisplay = (currency === 'jpy' || currency === 'krw') 
                        ? `${amount} ${currency.toUpperCase()}`
                        : `${(amount / 100).toFixed(2)} ${currency.toUpperCase()}`;
                    const active = price.active ? '✅' : '❌';
                    console.log(`       ${idx + 1}. ${active} ${price.id}: ${amountDisplay} (${price.active ? '激活' : '停用'})`);
                });
            }
        }
        
        return { product, prices: prices.data, pricesByCurrency };
    } catch (error) {
        console.error(`❌ 获取产品信息失败: ${error.message}`);
        throw error;
    }
}

async function createNewPriceFromExisting(existingPrice, newAmount) {
    try {
        const currency = existingPrice.currency.toLowerCase();
        const interval = existingPrice.recurring?.interval || 'one_time';
        const amountDisplay = (currency === 'jpy' || currency === 'krw') 
            ? `${newAmount} ${currency.toUpperCase()}`
            : `${(newAmount / 100).toFixed(2)} ${currency.toUpperCase()}`;
        
        console.log(`\n🆕 创建新价格: ${currency.toUpperCase()} ${interval}`);
        console.log(`   基于: ${existingPrice.id}`);
        console.log(`   新金额: ${amountDisplay}`);
        
        // 构建新价格对象，复制所有现有设置
        const newPriceData = {
            product: existingPrice.product,
            unit_amount: newAmount,
            currency: existingPrice.currency,
        };
        
        // 复制 recurring 设置
        if (existingPrice.recurring) {
            newPriceData.recurring = {
                interval: existingPrice.recurring.interval,
                interval_count: existingPrice.recurring.interval_count || 1,
            };
            
            // 复制其他 recurring 属性
            if (existingPrice.recurring.usage_type) {
                newPriceData.recurring.usage_type = existingPrice.recurring.usage_type;
            }
            if (existingPrice.recurring.aggregate_usage) {
                newPriceData.recurring.aggregate_usage = existingPrice.recurring.aggregate_usage;
            }
            if (existingPrice.recurring.trial_period_days !== undefined) {
                newPriceData.recurring.trial_period_days = existingPrice.recurring.trial_period_days;
            }
            if (existingPrice.recurring.meter) {
                newPriceData.recurring.meter = existingPrice.recurring.meter;
            }
        }
        
        // 复制 billing_scheme
        if (existingPrice.billing_scheme) {
            newPriceData.billing_scheme = existingPrice.billing_scheme;
        }
        
        // 复制 tiers（如果有）
        if (existingPrice.tiers && existingPrice.tiers.length > 0) {
            newPriceData.tiers = existingPrice.tiers;
            newPriceData.tiers_mode = existingPrice.tiers_mode;
        }
        
        // 复制 transform_quantity（如果有）
        if (existingPrice.transform_quantity) {
            newPriceData.transform_quantity = existingPrice.transform_quantity;
        }
        
        // 复制 metadata（添加新价格标记）
        if (existingPrice.metadata) {
            newPriceData.metadata = { ...existingPrice.metadata };
        } else {
            newPriceData.metadata = {};
        }
        newPriceData.metadata.created_at = new Date().toISOString();
        newPriceData.metadata.pricing_update = '2026-01-08';
        newPriceData.metadata.based_on_price = existingPrice.id;
        
        // 复制 nickname（如果有）
        if (existingPrice.nickname) {
            newPriceData.nickname = existingPrice.nickname;
        }
        
        // 复制 tax_behavior（如果有）
        if (existingPrice.tax_behavior) {
            newPriceData.tax_behavior = existingPrice.tax_behavior;
        }
        
        // 创建新价格
        const newPrice = await stripe.prices.create(newPriceData);
        
        console.log(`✅ 新价格创建成功！`);
        console.log(`   Price ID: ${newPrice.id}`);
        console.log(`   金额: ${amountDisplay}`);
        console.log(`   周期: ${newPrice.recurring?.interval || 'one_time'}`);
        
        return newPrice;
    } catch (error) {
        console.error(`❌ 创建价格失败: ${error.message}`);
        if (error.code) {
            console.error(`   错误代码: ${error.code}`);
        }
        throw error;
    }
}

async function main() {
    console.log('🚀 开始为产品创建新价格\n');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('产品 ID:', productId);
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
    
    try {
        // 1. 获取产品和现有价格
        const { product, prices, pricesByCurrency } = await getProductAndPrices(productId);
        
        // 2. 为每个货币和周期创建新价格
        console.log('\n\n📋 步骤 2: 创建新价格');
        console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
        
        const newPrices = [];
        
        // 遍历所有货币
        for (const currency of ['hkd', 'usd', 'jpy', 'krw']) {
            if (!pricesByCurrency[currency]) {
                console.log(`\n⚠️  未找到 ${currency.toUpperCase()} 的价格，跳过`);
                continue;
            }
            
            // 处理 monthly
            if (pricesByCurrency[currency]['month'] && pricesByCurrency[currency]['month'].length > 0) {
                // 使用第一个激活的价格作为模板，如果没有激活的则使用第一个
                const templatePrice = pricesByCurrency[currency]['month'].find(p => p.active) 
                    || pricesByCurrency[currency]['month'][0];
                
                if (newPricing[currency] && newPricing[currency].monthly) {
                    const newPrice = await createNewPriceFromExisting(
                        templatePrice,
                        newPricing[currency].monthly
                    );
                    newPrices.push(newPrice);
                }
            }
            
            // 处理 yearly
            if (pricesByCurrency[currency]['year'] && pricesByCurrency[currency]['year'].length > 0) {
                // 使用第一个激活的价格作为模板，如果没有激活的则使用第一个
                const templatePrice = pricesByCurrency[currency]['year'].find(p => p.active) 
                    || pricesByCurrency[currency]['year'][0];
                
                if (newPricing[currency] && newPricing[currency].yearly) {
                    const newPrice = await createNewPriceFromExisting(
                        templatePrice,
                        newPricing[currency].yearly
                    );
                    newPrices.push(newPrice);
                }
            }
        }
        
        // 3. 输出总结
        console.log('\n\n✅ 完成！新价格已创建');
        console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
        console.log(`\n📦 共创建 ${newPrices.length} 个新价格:\n`);
        
        newPrices.forEach((price, index) => {
            const amount = price.unit_amount || 0;
            const currency = price.currency.toUpperCase();
            const amountDisplay = (currency === 'JPY' || currency === 'KRW') 
                ? `${amount} ${currency}`
                : `${(amount / 100).toFixed(2)} ${currency}`;
            const interval = price.recurring?.interval || 'one_time';
            
            console.log(`${index + 1}. ${price.id}`);
            console.log(`   金额: ${amountDisplay}/${interval}`);
            console.log(`   货币: ${currency}`);
        });
        
        // 输出 JSON 格式
        console.log('\n\n📄 JSON 格式（方便复制到代码中）：');
        console.log(JSON.stringify({
            productId: productId,
            newPrices: newPrices.map(p => ({
                priceId: p.id,
                currency: p.currency.toUpperCase(),
                amount: p.unit_amount,
                interval: p.recurring?.interval || 'one_time',
                displayAmount: (p.currency === 'jpy' || p.currency === 'krw') 
                    ? `${p.unit_amount} ${p.currency.toUpperCase()}`
                    : `${(p.unit_amount / 100).toFixed(2)} ${p.currency.toUpperCase()}`
            }))
        }, null, 2));
        
        console.log('\n\n📝 下一步操作:');
        console.log('1. 在 Stripe Dashboard 中验证新价格已创建');
        console.log('2. 更新代码中的 Price ID 为新创建的 Price ID');
        console.log('3. 测试支付流程确保正常工作');
        console.log('4. （可选）在 Stripe Dashboard 中停用旧价格');
        
    } catch (error) {
        console.error('\n❌ 操作失败:', error.message);
        if (error.type) {
            console.error(`   错误类型: ${error.type}`);
        }
        if (error.code) {
            console.error(`   错误代码: ${error.code}`);
        }
        process.exit(1);
    }
}

main();

