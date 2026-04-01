#!/usr/bin/env node

/**
 * VaultCaddy 多货币产品配置脚本（英文版）
 * 支持：HKD, USD, GBP, JPY, KRW, EUR
 * 
 * 使用方法：
 * node setup-multi-currency-en.js <stripe_secret_key>
 */

const stripeSecretKey = process.argv[2];

if (!stripeSecretKey || !stripeSecretKey.startsWith('sk_')) {
    console.error('❌ 请提供有效的 Stripe Secret Key');
    console.error('用法: node setup-multi-currency-en.js <stripe_secret_key>');
    process.exit(1);
}

const isTestMode = stripeSecretKey.includes('_test_');
const stripe = require('stripe')(stripeSecretKey);

// 价格配置
const PRICING = {
    monthly: {
        hkd: 5800,      // HK$58.00
        usd: 748,       // $7.48
        gbp: 558,       // £5.58
        jpy: 1158,      // ¥1,158
        krw: 10888,     // ₩10,888
        eur: 628        // €6.28
    },
    yearly: {
        hkd: 55700,     // HK$557.00 (节省 20%)
        usd: 7181,      // $71.81
        gbp: 5357,      // £53.57
        jpy: 11117,     // ¥11,117
        krw: 104525,    // ₩104,525
        eur: 6029       // €60.29
    }
};

// 格式化货币显示
function formatCurrency(amount, currency) {
    const divisor = ['jpy', 'krw'].includes(currency) ? 1 : 100;
    const value = amount / divisor;
    
    const symbols = {
        hkd: 'HK$',
        usd: '$',
        gbp: '£',
        jpy: '¥',
        krw: '₩',
        eur: '€'
    };
    
    return `${symbols[currency]}${value.toLocaleString('en-US', {
        minimumFractionDigits: divisor === 100 ? 2 : 0,
        maximumFractionDigits: divisor === 100 ? 2 : 0
    })}`;
}

async function main() {
    console.log('🚀 VaultCaddy Multi-Currency Product Setup (English)\n');
    console.log(`📋 Mode: ${isTestMode ? 'Test Mode' : 'Live Mode'}\n');
    
    try {
        // ============================================
        // Step 1: Create or Get Meter
        // ============================================
        console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
        console.log('📋 Step 1/5: Create or Get Meter');
        console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
        
        const meters = await stripe.billing.meters.list({ limit: 100 });
        let meter = meters.data.find(m => m.event_name === 'vaultcaddy_credit_usage');
        
        if (meter) {
            console.log('✅ Found existing Meter');
            console.log(`   Meter ID: ${meter.id}\n`);
        } else {
            meter = await stripe.billing.meters.create({
                display_name: 'VaultCaddy Credits Usage',
                event_name: 'vaultcaddy_credit_usage',
                default_aggregation: { formula: 'sum' }
            });
            console.log('✅ Meter created successfully');
            console.log(`   Meter ID: ${meter.id}\n`);
        }
        
        // ============================================
        // Step 2: Create Monthly Product
        // ============================================
        console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
        console.log('📋 Step 2/5: Create Monthly Product');
        console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
        
        const monthlyProduct = await stripe.products.create({
            name: 'VaultCaddy Monthly',
            description: '100 Credits per month, with usage-based billing for overages',
            metadata: {
                plan_type: 'monthly',
                monthly_credits: '100',
                credits: '100'
            }
        });
        
        console.log('✅ Monthly product created');
        console.log(`   Product ID: ${monthlyProduct.id}\n`);
        
        // Create Monthly Fixed Price
        console.log('   Creating monthly fixed price...');
        const monthlyFixedPrice = await stripe.prices.create({
            product: monthlyProduct.id,
            currency: 'hkd',
            unit_amount: PRICING.monthly.hkd,
            recurring: { interval: 'month' },
            currency_options: {
                'usd': { unit_amount: PRICING.monthly.usd },
                'gbp': { unit_amount: PRICING.monthly.gbp },
                'jpy': { unit_amount: PRICING.monthly.jpy },
                'krw': { unit_amount: PRICING.monthly.krw },
                'eur': { unit_amount: PRICING.monthly.eur }
            },
            metadata: {
                plan_type: 'monthly',
                monthly_credits: '100',
                credits: '100'
            }
        });
        
        console.log('   ✅ Monthly fixed price created');
        console.log(`   Price ID: ${monthlyFixedPrice.id}`);
        console.log('   Supported currencies:');
        console.log(`   - HKD: ${formatCurrency(PRICING.monthly.hkd, 'hkd')}/mo`);
        console.log(`   - USD: ${formatCurrency(PRICING.monthly.usd, 'usd')}/mo`);
        console.log(`   - GBP: ${formatCurrency(PRICING.monthly.gbp, 'gbp')}/mo`);
        console.log(`   - JPY: ${formatCurrency(PRICING.monthly.jpy, 'jpy')}/mo`);
        console.log(`   - KRW: ${formatCurrency(PRICING.monthly.krw, 'krw')}/mo`);
        console.log(`   - EUR: ${formatCurrency(PRICING.monthly.eur, 'eur')}/mo\n`);
        
        // Create Monthly Metered Price
        console.log('   Creating metered price (for overages)...');
        const monthlyMeteredPrice = await stripe.prices.create({
            product: monthlyProduct.id,
            currency: 'hkd',
            recurring: {
                interval: 'month',
                usage_type: 'metered',
                meter: meter.id
            },
            billing_scheme: 'tiered',
            tiers_mode: 'graduated',
            tiers: [
                { up_to: 100, unit_amount: 0 },
                { up_to: 'inf', unit_amount: 50 }
            ],
            currency_options: {
                'usd': {
                    tiers: [
                        { up_to: 100, unit_amount: 0 },
                        { up_to: 'inf', unit_amount: 7 }
                    ]
                },
                'gbp': {
                    tiers: [
                        { up_to: 100, unit_amount: 0 },
                        { up_to: 'inf', unit_amount: 5 }
                    ]
                },
                'jpy': {
                    tiers: [
                        { up_to: 100, unit_amount: 0 },
                        { up_to: 'inf', unit_amount: 10 }
                    ]
                },
                'krw': {
                    tiers: [
                        { up_to: 100, unit_amount: 0 },
                        { up_to: 'inf', unit_amount: 94 }
                    ]
                },
                'eur': {
                    tiers: [
                        { up_to: 100, unit_amount: 0 },
                        { up_to: 'inf', unit_amount: 5 }
                    ]
                }
            },
            metadata: {
                type: 'metered_credits',
                description: 'Overage credits charged per usage',
                meter_id: meter.id
            }
        });
        
        console.log('   ✅ Metered price created');
        console.log(`   Price ID: ${monthlyMeteredPrice.id}`);
        console.log('   Tiered pricing:');
        console.log('   - First 100 credits: Free (included in monthly fee)');
        console.log('   - 101+ credits: Usage-based pricing');
        console.log('     · HKD: HK$0.50 each');
        console.log('     · USD: $0.07 each');
        console.log('     · GBP: £0.05 each');
        console.log('     · JPY: ¥10 each');
        console.log('     · KRW: ₩94 each');
        console.log('     · EUR: €0.05 each\n');
        
        // ============================================
        // Step 3: Create Yearly Product
        // ============================================
        console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
        console.log('📋 Step 3/5: Create Yearly Product');
        console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
        
        const yearlyProduct = await stripe.products.create({
            name: 'VaultCaddy Yearly',
            description: '1,200 Credits per year (Save 20%), with usage-based billing for overages',
            metadata: {
                plan_type: 'yearly',
                monthly_credits: '1200',
                credits: '1200'
            }
        });
        
        console.log('✅ Yearly product created');
        console.log(`   Product ID: ${yearlyProduct.id}\n`);
        
        // Create Yearly Fixed Price
        console.log('   Creating yearly fixed price...');
        const yearlyFixedPrice = await stripe.prices.create({
            product: yearlyProduct.id,
            currency: 'hkd',
            unit_amount: PRICING.yearly.hkd,
            recurring: { interval: 'year' },
            currency_options: {
                'usd': { unit_amount: PRICING.yearly.usd },
                'gbp': { unit_amount: PRICING.yearly.gbp },
                'jpy': { unit_amount: PRICING.yearly.jpy },
                'krw': { unit_amount: PRICING.yearly.krw },
                'eur': { unit_amount: PRICING.yearly.eur }
            },
            metadata: {
                plan_type: 'yearly',
                monthly_credits: '1200',
                credits: '1200'
            }
        });
        
        console.log('   ✅ Yearly fixed price created');
        console.log(`   Price ID: ${yearlyFixedPrice.id}`);
        console.log('   Supported currencies (Save 20%):');
        console.log(`   - HKD: ${formatCurrency(PRICING.yearly.hkd, 'hkd')}/yr`);
        console.log(`   - USD: ${formatCurrency(PRICING.yearly.usd, 'usd')}/yr`);
        console.log(`   - GBP: ${formatCurrency(PRICING.yearly.gbp, 'gbp')}/yr`);
        console.log(`   - JPY: ${formatCurrency(PRICING.yearly.jpy, 'jpy')}/yr`);
        console.log(`   - KRW: ${formatCurrency(PRICING.yearly.krw, 'krw')}/yr`);
        console.log(`   - EUR: ${formatCurrency(PRICING.yearly.eur, 'eur')}/yr\n`);
        
        // Create Yearly Metered Price
        console.log('   Creating metered price (for overages)...');
        const yearlyMeteredPrice = await stripe.prices.create({
            product: yearlyProduct.id,
            currency: 'hkd',
            recurring: {
                interval: 'year',
                usage_type: 'metered',
                meter: meter.id
            },
            billing_scheme: 'tiered',
            tiers_mode: 'graduated',
            tiers: [
                { up_to: 1200, unit_amount: 0 },
                { up_to: 'inf', unit_amount: 50 }
            ],
            currency_options: {
                'usd': {
                    tiers: [
                        { up_to: 1200, unit_amount: 0 },
                        { up_to: 'inf', unit_amount: 7 }
                    ]
                },
                'gbp': {
                    tiers: [
                        { up_to: 1200, unit_amount: 0 },
                        { up_to: 'inf', unit_amount: 5 }
                    ]
                },
                'jpy': {
                    tiers: [
                        { up_to: 1200, unit_amount: 0 },
                        { up_to: 'inf', unit_amount: 10 }
                    ]
                },
                'krw': {
                    tiers: [
                        { up_to: 1200, unit_amount: 0 },
                        { up_to: 'inf', unit_amount: 94 }
                    ]
                },
                'eur': {
                    tiers: [
                        { up_to: 1200, unit_amount: 0 },
                        { up_to: 'inf', unit_amount: 5 }
                    ]
                }
            },
            metadata: {
                type: 'metered_credits',
                description: 'Overage credits charged per usage',
                meter_id: meter.id
            }
        });
        
        console.log('   ✅ Metered price created');
        console.log(`   Price ID: ${yearlyMeteredPrice.id}\n`);
        
        // ============================================
        // Step 4: Summary
        // ============================================
        console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
        console.log('📋 Step 4/5: Configuration Summary');
        console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
        
        console.log('✅ All products and prices created successfully!\n');
        
        console.log('📊 Monthly Product:');
        console.log(`   Product ID: ${monthlyProduct.id}`);
        console.log(`   Fixed Price ID: ${monthlyFixedPrice.id}`);
        console.log(`   Metered Price ID: ${monthlyMeteredPrice.id}\n`);
        
        console.log('📊 Yearly Product:');
        console.log(`   Product ID: ${yearlyProduct.id}`);
        console.log(`   Fixed Price ID: ${yearlyFixedPrice.id}`);
        console.log(`   Metered Price ID: ${yearlyMeteredPrice.id}\n`);
        
        // ============================================
        // Step 5: Next Steps
        // ============================================
        console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
        console.log('📋 Step 5/5: Next Steps');
        console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
        
        console.log('🎯 Use these Price IDs in your frontend:\n');
        console.log('// Monthly prices');
        console.log(`const MONTHLY_PRICE_ID = '${monthlyFixedPrice.id}';`);
        console.log(`const MONTHLY_METERED_PRICE_ID = '${monthlyMeteredPrice.id}';\n`);
        console.log('// Yearly prices');
        console.log(`const YEARLY_PRICE_ID = '${yearlyFixedPrice.id}';`);
        console.log(`const YEARLY_METERED_PRICE_ID = '${yearlyMeteredPrice.id}';\n`);
        
        console.log('🎉 Setup complete!\n');
        console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
        
        // Save configuration
        const config = {
            mode: isTestMode ? 'test' : 'live',
            meter: {
                id: meter.id,
                event_name: meter.event_name
            },
            monthly: {
                product_id: monthlyProduct.id,
                product_name: 'VaultCaddy Monthly',
                fixed_price_id: monthlyFixedPrice.id,
                metered_price_id: monthlyMeteredPrice.id
            },
            yearly: {
                product_id: yearlyProduct.id,
                product_name: 'VaultCaddy Yearly',
                fixed_price_id: yearlyFixedPrice.id,
                metered_price_id: yearlyMeteredPrice.id
            }
        };
        
        const fs = require('fs');
        const configFile = `stripe-config-en-${isTestMode ? 'test' : 'live'}.json`;
        fs.writeFileSync(configFile, JSON.stringify(config, null, 2));
        console.log(`✅ Configuration saved to: ${configFile}\n`);
        
    } catch (error) {
        console.error('❌ Error occurred:', error.message);
        if (error.type === 'StripeInvalidRequestError') {
            console.error('\nDetailed error:', error.raw?.message);
        }
        process.exit(1);
    }
}

main();

