#!/usr/bin/env python3
"""
智能升级剩余的31个银行页面
检查每个页面是否已有Features，如果没有则添加
"""
import os
import re

# 剩余的31个真实银行页面（排除功能页面）
REMAINING_BANKS = [
    'ally-bank-statement-v2.html',
    'anz-bank-statement-v2.html',
    'anz-nz-bank-statement-v2.html',
    'asb-bank-statement-v2.html',
    'bank-of-america-statement-v2.html',
    'barclays-bank-statement-v2.html',
    'bmo-bank-statement-v2.html',
    'bnz-bank-statement-v2.html',
    'capital-one-statement-v2.html',
    'chase-bank-statement-v2.html',
    'cibc-bank-statement-v2.html',
    'citibank-statement-v2.html',
    'commbank-statement-v2.html',
    'dbs-bank-statement-v2.html',
    'hsbc-uk-bank-statement-v2.html',
    'lloyds-bank-statement-v2.html',
    'nab-bank-statement-v2.html',
    'natwest-bank-statement-v2.html',
    'ocbc-bank-statement-v2.html',
    'pnc-bank-statement-v2.html',
    'rbc-bank-statement-v2.html',
    'santander-uk-statement-v2.html',
    'scotiabank-statement-v2.html',
    'td-bank-statement-v2.html',
    'td-canada-trust-statement-v2.html',
    'truist-bank-statement-v2.html',
    'uob-bank-statement-v2.html',
    'us-bank-statement-v2.html',
    'wells-fargo-statement-v2.html',
    'westpac-bank-statement-v2.html',
    'westpac-nz-statement-v2.html'
]

def get_bank_name(filename):
    """从文件名提取银行名称"""
    name_map = {
        'ally': 'Ally Bank',
        'anz-bank': 'ANZ Australia',
        'anz-nz': 'ANZ New Zealand',
        'asb': 'ASB Bank',
        'bank-of-america': 'Bank of America',
        'barclays': 'Barclays Bank',
        'bmo': 'BMO Bank',
        'bnz': 'BNZ',
        'capital-one': 'Capital One',
        'chase': 'Chase Bank',
        'cibc': 'CIBC',
        'citibank': 'Citibank',
        'commbank': 'CommBank',
        'dbs': 'DBS Bank',
        'hsbc-uk': 'HSBC UK',
        'lloyds': 'Lloyds Bank',
        'nab': 'NAB',
        'natwest': 'NatWest',
        'ocbc': 'OCBC Bank',
        'pnc': 'PNC Bank',
        'rbc': 'RBC',
        'santander-uk': 'Santander UK',
        'scotiabank': 'Scotiabank',
        'td-bank': 'TD Bank',
        'td-canada': 'TD Canada Trust',
        'truist': 'Truist Bank',
        'uob': 'UOB',
        'us-bank': 'US Bank',
        'wells-fargo': 'Wells Fargo',
        'westpac-bank': 'Westpac Australia',
        'westpac-nz': 'Westpac New Zealand'
    }
    
    for key, value in name_map.items():
        if key in filename:
            return value
    return 'Bank'

def generate_features_section(bank_name):
    """生成Features Section"""
    return f'''
    <!-- Features Section -->
    <section style="padding: var(--space-20) var(--space-6); background: white;">
        <div style="max-width: 1200px; margin: 0 auto;">
            <h2 style="font-size: var(--text-4xl); font-weight: var(--font-bold); text-align: center; margin-bottom: var(--space-4); color: var(--gray-900);">
                Why Choose VaultCaddy for {bank_name}?
            </h2>
            <p style="text-align: center; color: var(--gray-600); font-size: var(--text-lg); margin-bottom: var(--space-16); max-width: 800px; margin-left: auto; margin-right: auto;">
                Industry-leading AI technology specifically trained on {bank_name} statement formats
            </p>
            
            <div class="feature-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: var(--space-8);">
                <!-- Feature 1 -->
                <div style="background: var(--gray-50); padding: var(--space-8); border-radius: var(--radius-xl); border-left: 4px solid var(--primary-blue);">
                    <div style="display: flex; align-items: center; gap: var(--space-4); margin-bottom: var(--space-4);">
                        <div style="background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); width: 48px; height: 48px; border-radius: var(--radius-lg); display: flex; align-items: center; justify-content: center;">
                            <i class="fas fa-robot" style="color: white; font-size: 24px;"></i>
                        </div>
                        <h3 style="font-size: var(--text-xl); font-weight: var(--font-bold); color: var(--gray-900); margin: 0;">98% AI Accuracy</h3>
                    </div>
                    <p style="color: var(--gray-600); line-height: 1.6; margin: 0;">
                        Our AI is specifically trained on {bank_name} statement formats, ensuring industry-leading 98% accuracy in data extraction
                    </p>
                </div>
                
                <!-- Feature 2 -->
                <div style="background: var(--gray-50); padding: var(--space-8); border-radius: var(--radius-xl); border-left: 4px solid var(--success);">
                    <div style="display: flex; align-items: center; gap: var(--space-4); margin-bottom: var(--space-4);">
                        <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); width: 48px; height: 48px; border-radius: var(--radius-lg); display: flex; align-items: center; justify-content: center;">
                            <i class="fas fa-bolt" style="color: white; font-size: 24px;"></i>
                        </div>
                        <h3 style="font-size: var(--text-xl); font-weight: var(--font-bold); color: var(--gray-900); margin: 0;">3-Second Processing</h3>
                    </div>
                    <p style="color: var(--gray-600); line-height: 1.6; margin: 0;">
                        Convert your {bank_name} PDF statements in just 3 seconds. Batch upload multiple files for even faster processing
                    </p>
                </div>
                
                <!-- Feature 3 -->
                <div style="background: var(--gray-50); padding: var(--space-8); border-radius: var(--radius-xl); border-left: 4px solid var(--warning);">
                    <div style="display: flex; align-items: center; gap: var(--space-4); margin-bottom: var(--space-4);">
                        <div style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); width: 48px; height: 48px; border-radius: var(--radius-lg); display: flex; align-items: center; justify-content: center;">
                            <i class="fas fa-file-export" style="color: white; font-size: 24px;"></i>
                        </div>
                        <h3 style="font-size: var(--text-xl); font-weight: var(--font-bold); color: var(--gray-900); margin: 0;">Multiple Export Formats</h3>
                    </div>
                    <p style="color: var(--gray-600); line-height: 1.6; margin: 0;">
                        Export to Excel, CSV, QuickBooks, or Xero. Perfect for accountants and small businesses
                    </p>
                </div>
                
                <!-- Feature 4 -->
                <div style="background: var(--gray-50); padding: var(--space-8); border-radius: var(--radius-xl); border-left: 4px solid var(--purple);">
                    <div style="display: flex; align-items: center; gap: var(--space-4); margin-bottom: var(--space-4);">
                        <div style="background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%); width: 48px; height: 48px; border-radius: var(--radius-lg); display: flex; align-items: center; justify-content: center;">
                            <i class="fas fa-shield-alt" style="color: white; font-size: 24px;"></i>
                        </div>
                        <h3 style="font-size: var(--text-xl); font-weight: var(--font-bold); color: var(--gray-900); margin: 0;">Bank-Level Security</h3>
                    </div>
                    <p style="color: var(--gray-600); line-height: 1.6; margin: 0;">
                        Your {bank_name} data is encrypted in transit and at rest. SOC 2 Type II certified with automatic deletion after 24 hours
                    </p>
                </div>
                
                <!-- Feature 5 -->
                <div style="background: var(--gray-50); padding: var(--space-8); border-radius: var(--radius-xl); border-left: 4px solid var(--info);">
                    <div style="display: flex; align-items: center; gap: var(--space-4); margin-bottom: var(--space-4);">
                        <div style="background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); width: 48px; height: 48px; border-radius: var(--radius-lg); display: flex; align-items: center; justify-content: center;">
                            <i class="fas fa-layer-group" style="color: white; font-size: 24px;"></i>
                        </div>
                        <h3 style="font-size: var(--text-xl); font-weight: var(--font-bold); color: var(--gray-900); margin: 0;">Batch Processing</h3>
                    </div>
                    <p style="color: var(--gray-600); line-height: 1.6; margin: 0;">
                        Upload unlimited {bank_name} statements at once. Process hundreds of pages in minutes, not hours
                    </p>
                </div>
                
                <!-- Feature 6 -->
                <div style="background: var(--gray-50); padding: var(--space-8); border-radius: var(--radius-xl); border-left: 4px solid var(--pink);">
                    <div style="display: flex; align-items: center; gap: var(--space-4); margin-bottom: var(--space-4);">
                        <div style="background: linear-gradient(135deg, #ec4899 0%, #db2777 100%); width: 48px; height: 48px; border-radius: var(--radius-lg); display: flex; align-items: center; justify-content: center;">
                            <i class="fas fa-headset" style="color: white; font-size: 24px;"></i>
                        </div>
                        <h3 style="font-size: var(--text-xl); font-weight: var(--font-bold); color: var(--gray-900); margin: 0;">Expert Support</h3>
                    </div>
                    <p style="color: var(--gray-600); line-height: 1.6; margin: 0;">
                        Get help from our team of accounting automation experts. Email support included with all plans
                    </p>
                </div>
            </div>
        </div>
    </section>
'''

def upgrade_page(filename):
    """智能升级页面 - 检查是否已有Features Section"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已有Features Section
        if '<!-- Features Section -->' in content:
            return False, "已有Features"
        
        bank_name = get_bank_name(filename)
        features_html = generate_features_section(bank_name)
        
        # 在"Related Pages Section"前插入
        insert_point = content.find('<!-- Related Pages Section -->')
        if insert_point == -1:
            insert_point = content.find('</body>')
        
        if insert_point == -1:
            return False, "找不到插入点"
        
        new_content = content[:insert_point] + features_html + '\n' + content[insert_point:]
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True, "成功"
    
    except Exception as e:
        return False, str(e)

# 执行升级
print("🚀 升级剩余的31个银行页面...\n")

success = 0
skip = 0
error = 0

for filename in REMAINING_BANKS:
    if not os.path.exists(filename):
        print(f"  ❌ {filename} - 文件不存在")
        error += 1
        continue
    
    ok, msg = upgrade_page(filename)
    bank_name = get_bank_name(filename)
    
    if ok:
        print(f"  ✅ {bank_name:25s} - {filename}")
        success += 1
    elif msg == "已有Features":
        print(f"  ⏭️  {bank_name:25s} - 已有Features，跳过")
        skip += 1
    else:
        print(f"  ❌ {bank_name:25s} - {msg}")
        error += 1

print(f"\n📊 升级完成:")
print(f"  成功: {success}/31")
print(f"  跳过: {skip}")
print(f"  失败: {error}")
print(f"\n🎉 总计: {18 + success} 个银行页面已升级！")
