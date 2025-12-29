#!/usr/bin/env python3
"""
批量升级银行页面 - 添加Features + FAQ Sections
Phase 1: 先处理10个美国银行页面
"""
import os
import re

# 美国10个银行页面
US_BANKS = [
    'chase-bank-statement-v2.html',
    'bank-of-america-statement-v2.html',
    'wells-fargo-statement-v2.html',
    'citibank-statement-v2.html',
    'capital-one-statement-v2.html',
    'us-bank-statement-v2.html',
    'pnc-bank-statement-v2.html',
    'td-bank-statement-v2.html',
    'truist-bank-statement-v2.html',
    'ally-bank-statement-v2.html'
]

def get_bank_name(filename):
    """从文件名提取银行名称"""
    name_map = {
        'chase': 'Chase Bank',
        'bank-of-america': 'Bank of America',
        'wells-fargo': 'Wells Fargo',
        'citibank': 'Citibank',
        'capital-one': 'Capital One',
        'us-bank': 'US Bank',
        'pnc': 'PNC Bank',
        'td-bank': 'TD Bank',
        'truist': 'Truist Bank',
        'ally': 'Ally Bank'
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

def generate_faq_section(bank_name):
    """生成FAQ Section"""
    return f'''
    <!-- FAQ Section -->
    <section style="padding: var(--space-20) var(--space-6); background: var(--gray-50);">
        <div style="max-width: 900px; margin: 0 auto;">
            <h2 style="font-size: var(--text-4xl); font-weight: var(--font-bold); text-align: center; margin-bottom: var(--space-4); color: var(--gray-900);">
                Frequently Asked Questions
            </h2>
            <p style="text-align: center; color: var(--gray-600); font-size: var(--text-lg); margin-bottom: var(--space-16);">
                Everything you need to know about converting {bank_name} statements
            </p>
            
            <div style="background: white; border-radius: var(--radius-2xl); padding: var(--space-8); box-shadow: var(--shadow-lg);">
                <!-- FAQ 1 -->
                <div class="faq-item" style="border-bottom: 1px solid var(--gray-200); padding: var(--space-6) 0; position: relative;">
                    <div class="faq-question-container" style="position: relative;">
                        <button class="faq-question" style="width: 100%; text-align: left; background: none; border: none; padding-right: 40px; cursor: pointer; font-size: var(--text-lg); font-weight: var(--font-semibold); color: var(--gray-900); display: flex; align-items: center; justify-content: space-between;">
                            <span>How accurate is VaultCaddy for {bank_name} statements?</span>
                            <span class="faq-toggle-icon" style="position: absolute; right: 0; top: 50%; transform: translateY(-50%); font-size: var(--text-2xl); color: var(--primary-blue); transition: transform 0.3s; flex-shrink: 0;">+</span>
                        </button>
                    </div>
                    <div class="faq-answer" style="max-height: 0; overflow: hidden; transition: max-height 0.3s ease;">
                        <p style="color: var(--gray-600); line-height: 1.8; margin-top: var(--space-4); padding-right: var(--space-10);">
                            VaultCaddy achieves 98% accuracy for {bank_name} statements using advanced AI trained specifically on {bank_name} formats. Our system recognizes all transaction types, dates, amounts, and descriptions with industry-leading precision.
                        </p>
                    </div>
                </div>
                
                <!-- FAQ 2 -->
                <div class="faq-item" style="border-bottom: 1px solid var(--gray-200); padding: var(--space-6) 0; position: relative;">
                    <div class="faq-question-container" style="position: relative;">
                        <button class="faq-question" style="width: 100%; text-align: left; background: none; border: none; padding-right: 40px; cursor: pointer; font-size: var(--text-lg); font-weight: var(--font-semibold); color: var(--gray-900); display: flex; align-items: center; justify-content: space-between;">
                            <span>What file formats are supported?</span>
                            <span class="faq-toggle-icon" style="position: absolute; right: 0; top: 50%; transform: translateY(-50%); font-size: var(--text-2xl); color: var(--primary-blue); transition: transform 0.3s; flex-shrink: 0;">+</span>
                        </button>
                    </div>
                    <div class="faq-answer" style="max-height: 0; overflow: hidden; transition: max-height 0.3s ease;">
                        <p style="color: var(--gray-600); line-height: 1.8; margin-top: var(--space-4); padding-right: var(--space-10);">
                            We support PDF, JPG, and PNG files from {bank_name}. You can export to Excel (XLSX), CSV, QuickBooks (QBO), or Xero formats. Batch upload multiple files for faster processing.
                        </p>
                    </div>
                </div>
                
                <!-- FAQ 3 -->
                <div class="faq-item" style="border-bottom: 1px solid var(--gray-200); padding: var(--space-6) 0; position: relative;">
                    <div class="faq-question-container" style="position: relative;">
                        <button class="faq-question" style="width: 100%; text-align: left; background: none; border: none; padding-right: 40px; cursor: pointer; font-size: var(--text-lg); font-weight: var(--font-semibold); color: var(--gray-900); display: flex; align-items: center; justify-content: space-between;">
                            <span>How long does it take to process a statement?</span>
                            <span class="faq-toggle-icon" style="position: absolute; right: 0; top: 50%; transform: translateY(-50%); font-size: var(--text-2xl); color: var(--primary-blue); transition: transform 0.3s; flex-shrink: 0;">+</span>
                        </button>
                    </div>
                    <div class="faq-answer" style="max-height: 0; overflow: hidden; transition: max-height 0.3s ease;">
                        <p style="color: var(--gray-600); line-height: 1.8; margin-top: var(--space-4); padding-right: var(--space-10);">
                            Most {bank_name} statements are processed in 3-5 seconds. Larger statements with 50+ pages may take up to 30 seconds. Our batch processing can handle hundreds of pages simultaneously.
                        </p>
                    </div>
                </div>
                
                <!-- FAQ 4 -->
                <div class="faq-item" style="border-bottom: 1px solid var(--gray-200); padding: var(--space-6) 0; position: relative;">
                    <div class="faq-question-container" style="position: relative;">
                        <button class="faq-question" style="width: 100%; text-align: left; background: none; border: none; padding-right: 40px; cursor: pointer; font-size: var(--text-lg); font-weight: var(--font-semibold); color: var(--gray-900); display: flex; align-items: center; justify-content: space-between;">
                            <span>Is my {bank_name} data secure?</span>
                            <span class="faq-toggle-icon" style="position: absolute; right: 0; top: 50%; transform: translateY(-50%); font-size: var(--text-2xl); color: var(--primary-blue); transition: transform 0.3s; flex-shrink: 0;">+</span>
                        </button>
                    </div>
                    <div class="faq-answer" style="max-height: 0; overflow: hidden; transition: max-height 0.3s ease;">
                        <p style="color: var(--gray-600); line-height: 1.8; margin-top: var(--space-4); padding-right: var(--space-10);">
                            Yes. We use bank-level encryption (AES-256) for all data. Your files are automatically deleted after 24 hours. We are SOC 2 Type II certified and GDPR compliant.
                        </p>
                    </div>
                </div>
                
                <!-- FAQ 5 -->
                <div class="faq-item" style="border-bottom: 1px solid var(--gray-200); padding: var(--space-6) 0; position: relative;">
                    <div class="faq-question-container" style="position: relative;">
                        <button class="faq-question" style="width: 100%; text-align: left; background: none; border: none; padding-right: 40px; cursor: pointer; font-size: var(--text-lg); font-weight: var(--font-semibold); color: var(--gray-900); display: flex; align-items: center; justify-content: space-between;">
                            <span>Can I try it for free?</span>
                            <span class="faq-toggle-icon" style="position: absolute; right: 0; top: 50%; transform: translateY(-50%); font-size: var(--text-2xl); color: var(--primary-blue); transition: transform 0.3s; flex-shrink: 0;">+</span>
                        </button>
                    </div>
                    <div class="faq-answer" style="max-height: 0; overflow: hidden; transition: max-height 0.3s ease;">
                        <p style="color: var(--gray-600); line-height: 1.8; margin-top: var(--space-4); padding-right: var(--space-10);">
                            Yes! Verify your email to get 20 free credits (pages). No credit card required. Test our service with your actual {bank_name} statements before subscribing.
                        </p>
                    </div>
                </div>
                
                <!-- FAQ 6 -->
                <div class="faq-item" style="padding: var(--space-6) 0; position: relative;">
                    <div class="faq-question-container" style="position: relative;">
                        <button class="faq-question" style="width: 100%; text-align: left; background: none; border: none; padding-right: 40px; cursor: pointer; font-size: var(--text-lg); font-weight: var(--font-semibold); color: var(--gray-900); display: flex; align-items: center; justify-content: space-between;">
                            <span>Do you integrate with accounting software?</span>
                            <span class="faq-toggle-icon" style="position: absolute; right: 0; top: 50%; transform: translateY(-50%); font-size: var(--text-2xl); color: var(--primary-blue); transition: transform 0.3s; flex-shrink: 0;">+</span>
                        </button>
                    </div>
                    <div class="faq-answer" style="max-height: 0; overflow: hidden; transition: max-height 0.3s ease;">
                        <p style="color: var(--gray-600); line-height: 1.8; margin-top: var(--space-4); padding-right: var(--space-10);">
                            Yes! We export directly to QuickBooks Online, Xero, and Excel. Our QBO and Xero formats are ready to import without any manual formatting.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </section>
    
    <!-- FAQ JavaScript -->
    <script>
        document.addEventListener('DOMContentLoaded', function() {{
            const faqQuestions = document.querySelectorAll('.faq-question');
            
            faqQuestions.forEach(question => {{
                question.addEventListener('click', function() {{
                    const faqItem = this.closest('.faq-item');
                    const answer = faqItem.querySelector('.faq-answer');
                    const icon = this.querySelector('.faq-toggle-icon');
                    const isOpen = answer.style.maxHeight && answer.style.maxHeight !== '0px';
                    
                    // Close all other FAQs
                    document.querySelectorAll('.faq-answer').forEach(a => {{
                        a.style.maxHeight = '0';
                    }});
                    document.querySelectorAll('.faq-toggle-icon').forEach(i => {{
                        i.textContent = '+';
                        i.style.transform = 'translateY(-50%)';
                    }});
                    
                    // Toggle current FAQ
                    if (!isOpen) {{
                        answer.style.maxHeight = answer.scrollHeight + 'px';
                        icon.textContent = '−';
                        icon.style.transform = 'translateY(-50%) rotate(0deg)';
                    }}
                }});
            }});
        }});
    </script>
'''

def upgrade_bank_page(filename):
    """升级单个银行页面"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已升级
        if '<!-- Features Section -->' in content and '<!-- FAQ Section -->' in content:
            return False, "已升级"
        
        bank_name = get_bank_name(filename)
        
        # 生成新sections
        features_html = generate_features_section(bank_name)
        faq_html = generate_faq_section(bank_name)
        
        # 在Pricing Section之后插入Features
        # 在Related Pages之前插入FAQ
        
        # 找到插入点
        pricing_end = content.find('</section>', content.find('id="pricing"'))
        if pricing_end == -1:
            return False, "找不到Pricing Section"
        
        related_start = content.find('<!-- Related Pages Section -->')
        if related_start == -1:
            related_start = content.find('</body>')
        
        # 插入Features和FAQ
        new_content = (
            content[:pricing_end + 10] +
            features_html +
            faq_html +
            content[related_start:]
        )
        
        # 写回文件
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True, "成功"
    
    except Exception as e:
        return False, str(e)

# 执行升级
print("🚀 开始升级美国10个银行页面...\n")

success_count = 0
skip_count = 0
error_count = 0

for filename in US_BANKS:
    if not os.path.exists(filename):
        print(f"  ❌ {filename} - 文件不存在")
        error_count += 1
        continue
    
    success, message = upgrade_bank_page(filename)
    
    if success:
        bank_name = get_bank_name(filename)
        print(f"  ✅ {bank_name:20s} - {filename}")
        success_count += 1
    elif message == "已升级":
        print(f"  ⏭️  {filename} - 已升级，跳过")
        skip_count += 1
    else:
        print(f"  ❌ {filename} - {message}")
        error_count += 1

print(f"\n📊 美国银行页面升级完成:")
print(f"  成功: {success_count}")
print(f"  跳过: {skip_count}")
print(f"  失败: {error_count}")
