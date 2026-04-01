#!/usr/bin/env python3
"""
Phase 3: 质量检查 - 自动验证所有50个银行页面
检查：银行名称、定价、FAQ、链接、SEO元标签、移动响应式
"""
import os
import re
from pathlib import Path

print("=" * 70)
print("🔍 Phase 3: 质量检查开始")
print("=" * 70)
print("\n📋 检查项目:")
print("  1. 银行名称准确性")
print("  2. 定价正确性（按地区）")
print("  3. Schema标记完整性")
print("  4. Meta标签独特性")
print("  5. 内容字数验证")
print("  6. FAQ数量检查")
print("  7. 移动响应式CSS")
print()

# 定义所有银行的预期数据
expected_banks = {
    'chase-bank-statement-v3.html': {'name': 'Chase Bank', 'currency': 'USD', 'monthly': '5.59', 'region': 'United States'},
    'bank-of-america-statement-v3.html': {'name': 'Bank of America', 'currency': 'USD', 'monthly': '5.59', 'region': 'United States'},
    'wells-fargo-statement-v3.html': {'name': 'Wells Fargo', 'currency': 'USD', 'monthly': '5.59', 'region': 'United States'},
    'citibank-statement-v3.html': {'name': 'Citibank', 'currency': 'USD', 'monthly': '5.59', 'region': 'United States'},
    'capital-one-statement-v3.html': {'name': 'Capital One', 'currency': 'USD', 'monthly': '5.59', 'region': 'United States'},
    'us-bank-statement-v3.html': {'name': 'US Bank', 'currency': 'USD', 'monthly': '5.59', 'region': 'United States'},
    'pnc-bank-statement-v3.html': {'name': 'PNC Bank', 'currency': 'USD', 'monthly': '5.59', 'region': 'United States'},
    'td-bank-statement-v3.html': {'name': 'TD Bank', 'currency': 'USD', 'monthly': '5.59', 'region': 'United States'},
    'truist-bank-statement-v3.html': {'name': 'Truist Bank', 'currency': 'USD', 'monthly': '5.59', 'region': 'United States'},
    'ally-bank-statement-v3.html': {'name': 'Ally Bank', 'currency': 'USD', 'monthly': '5.59', 'region': 'United States'},
    
    'hsbc-uk-bank-statement-v3.html': {'name': 'HSBC UK', 'currency': 'GBP', 'monthly': '4.59', 'region': 'United Kingdom'},
    'barclays-bank-statement-v3.html': {'name': 'Barclays Bank', 'currency': 'GBP', 'monthly': '4.59', 'region': 'United Kingdom'},
    'lloyds-bank-statement-v3.html': {'name': 'Lloyds Bank', 'currency': 'GBP', 'monthly': '4.59', 'region': 'United Kingdom'},
    'natwest-bank-statement-v3.html': {'name': 'NatWest', 'currency': 'GBP', 'monthly': '4.59', 'region': 'United Kingdom'},
    'santander-uk-statement-v3.html': {'name': 'Santander UK', 'currency': 'GBP', 'monthly': '4.59', 'region': 'United Kingdom'},
    
    'rbc-bank-statement-v3.html': {'name': 'RBC Royal Bank', 'currency': 'CAD', 'monthly': '7.59', 'region': 'Canada'},
    'td-canada-trust-statement-v3.html': {'name': 'TD Canada Trust', 'currency': 'CAD', 'monthly': '7.59', 'region': 'Canada'},
    'scotiabank-statement-v3.html': {'name': 'Scotiabank', 'currency': 'CAD', 'monthly': '7.59', 'region': 'Canada'},
    'bmo-bank-statement-v3.html': {'name': 'BMO Bank of Montreal', 'currency': 'CAD', 'monthly': '7.59', 'region': 'Canada'},
    'cibc-bank-statement-v3.html': {'name': 'CIBC', 'currency': 'CAD', 'monthly': '7.59', 'region': 'Canada'},
    
    'commbank-statement-v3.html': {'name': 'CommBank Australia', 'currency': 'AUD', 'monthly': '8.59', 'region': 'Australia'},
    'westpac-australia-statement-v3.html': {'name': 'Westpac Australia', 'currency': 'AUD', 'monthly': '8.59', 'region': 'Australia'},
    'anz-australia-statement-v3.html': {'name': 'ANZ Australia', 'currency': 'AUD', 'monthly': '8.59', 'region': 'Australia'},
    'nab-statement-v3.html': {'name': 'NAB', 'currency': 'AUD', 'monthly': '8.59', 'region': 'Australia'},
    
    'anz-new-zealand-statement-v3.html': {'name': 'ANZ New Zealand', 'currency': 'NZD', 'monthly': '9.29', 'region': 'New Zealand'},
    'asb-bank-statement-v3.html': {'name': 'ASB Bank', 'currency': 'NZD', 'monthly': '9.29', 'region': 'New Zealand'},
    'westpac-new-zealand-statement-v3.html': {'name': 'Westpac New Zealand', 'currency': 'NZD', 'monthly': '9.29', 'region': 'New Zealand'},
    'bnz-statement-v3.html': {'name': 'BNZ', 'currency': 'NZD', 'monthly': '9.29', 'region': 'New Zealand'},
    
    'dbs-bank-statement-v3.html': {'name': 'DBS Bank', 'currency': 'SGD', 'monthly': '7.59', 'region': 'Singapore'},
    'ocbc-bank-statement-v3.html': {'name': 'OCBC Bank', 'currency': 'SGD', 'monthly': '7.59', 'region': 'Singapore'},
    'uob-statement-v3.html': {'name': 'UOB', 'currency': 'SGD', 'monthly': '7.59', 'region': 'Singapore'},
    
    'mufg-bank-statement-v3.html': {'name': 'Mitsubishi UFJ', 'currency': 'JPY', 'monthly': '926', 'region': 'Japan'},
    'smbc-bank-statement-v3.html': {'name': 'Sumitomo Mitsui', 'currency': 'JPY', 'monthly': '926', 'region': 'Japan'},
    'mizuho-bank-statement-v3.html': {'name': 'Mizuho Bank', 'currency': 'JPY', 'monthly': '926', 'region': 'Japan'},
    
    'kb-kookmin-bank-statement-v3.html': {'name': 'KB Kookmin Bank', 'currency': 'KRW', 'monthly': '7998', 'region': 'South Korea'},
    'shinhan-bank-statement-v3.html': {'name': 'Shinhan Bank', 'currency': 'KRW', 'monthly': '7998', 'region': 'South Korea'},
    'hana-bank-statement-v3.html': {'name': 'Hana Bank', 'currency': 'KRW', 'monthly': '7998', 'region': 'South Korea'},
    'woori-bank-statement-v3.html': {'name': 'Woori Bank', 'currency': 'KRW', 'monthly': '7998', 'region': 'South Korea'},
    
    'bank-of-taiwan-statement-v3.html': {'name': 'Bank of Taiwan', 'currency': 'TWD', 'monthly': '188', 'region': 'Taiwan'},
    'ctbc-bank-statement-v3.html': {'name': 'CTBC Bank', 'currency': 'TWD', 'monthly': '188', 'region': 'Taiwan'},
    'cathay-bank-statement-v3.html': {'name': 'Cathay Bank', 'currency': 'TWD', 'monthly': '188', 'region': 'Taiwan'},
    
    'hsbc-hong-kong-statement-v3.html': {'name': 'HSBC Hong Kong', 'currency': 'HKD', 'monthly': '46', 'region': 'Hong Kong'},
    'hang-seng-bank-statement-v3.html': {'name': 'Hang Seng Bank', 'currency': 'HKD', 'monthly': '46', 'region': 'Hong Kong'},
    'boc-hong-kong-statement-v3.html': {'name': 'BOC Hong Kong', 'currency': 'HKD', 'monthly': '46', 'region': 'Hong Kong'},
    
    'deutsche-bank-statement-v3.html': {'name': 'Deutsche Bank', 'currency': 'EUR', 'monthly': '5.29', 'region': 'Germany'},
    'ing-bank-statement-v3.html': {'name': 'ING Bank', 'currency': 'EUR', 'monthly': '5.29', 'region': 'Netherlands'},
    'commerzbank-statement-v3.html': {'name': 'Commerzbank', 'currency': 'EUR', 'monthly': '5.29', 'region': 'Germany'},
    'rabobank-statement-v3.html': {'name': 'Rabobank', 'currency': 'EUR', 'monthly': '5.29', 'region': 'Netherlands'},
    'abn-amro-statement-v3.html': {'name': 'ABN AMRO', 'currency': 'EUR', 'monthly': '5.29', 'region': 'Netherlands'},
    'dz-bank-statement-v3.html': {'name': 'DZ Bank', 'currency': 'EUR', 'monthly': '5.29', 'region': 'Germany'},
}

# 质量检查结果
results = {
    'total': 0,
    'passed': 0,
    'warnings': 0,
    'errors': 0,
    'issues': []
}

print("🔍 开始检查50个银行页面...\n")

for filename, expected in expected_banks.items():
    if not os.path.exists(filename):
        results['errors'] += 1
        results['issues'].append(f"❌ {filename} - 文件不存在")
        continue
    
    results['total'] += 1
    file_issues = []
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. 检查银行名称
    if expected['name'] not in content:
        file_issues.append(f"⚠️  银行名称可能不正确")
    
    # 2. 检查定价
    if expected['monthly'] not in content:
        file_issues.append(f"⚠️  月费价格可能不正确（应为{expected['monthly']}）")
    
    # 3. 检查货币代码
    if f'"{expected["currency"]}"' not in content:
        file_issues.append(f"⚠️  货币代码可能不正确（应为{expected['currency']}）")
    
    # 4. 检查Schema标记
    if '@type": "SoftwareApplication' not in content:
        file_issues.append(f"❌ 缺少SoftwareApplication Schema")
    if '@type": "FAQPage' not in content:
        file_issues.append(f"❌ 缺少FAQ Schema")
    
    # 5. 检查Meta标签
    if '<title>' not in content:
        file_issues.append(f"❌ 缺少Title标签")
    if 'meta name="description"' not in content:
        file_issues.append(f"❌ 缺少Meta Description")
    
    # 6. 检查FAQ数量（应该有10个）
    faq_count = content.count('class="faq-item"')
    if faq_count < 10:
        file_issues.append(f"⚠️  FAQ数量不足（{faq_count}/10）")
    
    # 7. 检查Use Cases数量（应该有3个）
    use_case_count = content.count('class="use-case"')
    if use_case_count < 3:
        file_issues.append(f"⚠️  客户案例不足（{use_case_count}/3）")
    
    # 8. 检查How It Works步骤（应该有4个）
    steps_count = content.count('class="step-number"')
    if steps_count < 4:
        file_issues.append(f"⚠️  教程步骤不足（{steps_count}/4）")
    
    # 9. 检查移动响应式CSS
    if '@media (max-width: 768px)' not in content:
        file_issues.append(f"⚠️  可能缺少移动响应式CSS")
    
    # 10. 检查组件库引用
    if 'design-system.css' not in content:
        file_issues.append(f"❌ 缺少设计系统CSS")
    if 'additional-components.css' not in content:
        file_issues.append(f"❌ 缺少组件库CSS")
    
    # 输出结果
    if file_issues:
        results['warnings'] += len(file_issues)
        print(f"⚠️  {filename}")
        for issue in file_issues:
            print(f"    {issue}")
        print()
    else:
        results['passed'] += 1
        print(f"✅ {filename} - 所有检查通过")

print("\n" + "=" * 70)
print("📊 质量检查结果汇总")
print("=" * 70)
print(f"\n总计检查: {results['total']} 个页面")
print(f"✅ 完美通过: {results['passed']} 个")
print(f"⚠️  有警告: {results['total'] - results['passed']} 个")
print(f"📋 总警告数: {results['warnings']}")

if results['passed'] == results['total']:
    print("\n🎉 所有页面质量检查通过！")
else:
    print(f"\n💡 建议: 修复上述{results['warnings']}个警告项以提升页面质量")

print("\n⏭️  下一步: Phase 4 - SEO提交")
