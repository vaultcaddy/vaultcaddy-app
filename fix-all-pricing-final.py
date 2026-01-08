#!/usr/bin/env python3
"""
最终修复所有定价问题
1. 更新中文版billing.html的Pro功能列表（移除"专属客户经理"）
2. 更新所有语言版本index.html为双层定价结构
"""

import re
from pathlib import Path

# 英文版双层定价HTML
PRICING_SECTION_EN = '''                <!-- Starter and Pro side by side -->
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; max-width: 1000px; margin: 0 auto;">
                    <!-- Starter Plan -->
                    <div class="pricing-card fade-in-left" style="border: 2px solid #e5e7eb; border-radius: 16px; padding: 2.5rem; background: white; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05); max-width: 500px; width: 100%;">
                        <!-- Title and Price -->
                        <div class="pricing-header" style="margin-bottom: 1.5rem;">
                            <h3 style="font-size: 1.5rem; font-weight: 700; color: #1f2937; margin-bottom: 0.5rem;">Starter</h3>
                            <div style="display: flex; align-items: baseline; gap: 0.25rem; margin-bottom: 0.5rem;">
                                <span style="font-size: 1rem; color: #6b7280;">USD $</span>
                                <span style="font-size: 3rem; font-weight: 700; color: #1f2937; line-height: 1;">3.88</span>
                                <span style="font-size: 1rem; color: #6b7280;">/month</span>
                            </div>
                            <p style="font-size: 0.875rem; color: #6b7280;">Yearly: $2.88/month (Save 20%)</p>
                        </div>
                        
                        <!-- Features -->
                        <div style="margin-bottom: 1.5rem;">
                            <p style="font-weight: 600; margin-bottom: 1rem; color: #1f2937;">What's Included:</p>
                            <div style="display: flex; flex-direction: column; gap: 0.75rem;">
                                <div style="display: flex; align-items: start; font-size: 0.875rem;">
                                    <i class="fas fa-check" style="color: #10b981; margin-right: 0.75rem; margin-top: 0.2rem;"></i>
                                    <span>100 Credits/month (Then $0.05/page)</span>
                                </div>
                                <div style="display: flex; align-items: start; font-size: 0.875rem;">
                                    <i class="fas fa-check" style="color: #10b981; margin-right: 0.75rem; margin-top: 0.2rem;"></i>
                                    <span>Unlimited Batch Processing</span>
                                </div>
                                <div style="display: flex; align-items: start; font-size: 0.875rem;">
                                    <i class="fas fa-check" style="color: #10b981; margin-right: 0.75rem; margin-top: 0.2rem;"></i>
                                    <span>Excel/CSV/QBO Export</span>
                                </div>
                                <div style="display: flex; align-items: start; font-size: 0.875rem;">
                                    <i class="fas fa-check" style="color: #10b981; margin-right: 0.75rem; margin-top: 0.2rem;"></i>
                                    <span>QuickBooks/Xero Integration</span>
                                </div>
                                <div style="display: flex; align-items: start; font-size: 0.875rem;">
                                    <i class="fas fa-check" style="color: #10b981; margin-right: 0.75rem; margin-top: 0.2rem;"></i>
                                    <span>8 Languages Support</span>
                                </div>
                                <div style="display: flex; align-items: start; font-size: 0.875rem;">
                                    <i class="fas fa-check" style="color: #10b981; margin-right: 0.75rem; margin-top: 0.2rem;"></i>
                                    <span>365 Days Data Retention</span>
                                </div>
                            </div>
                        </div>
                        
                        <!-- CTA Button -->
                        <button class="cta-btn" onclick="window.location.href='billing.html?plan=starter'" style="width: 100%; padding: 1rem; font-size: 1rem; font-weight: 600; background: #8b5cf6; color: white; border: none; border-radius: 8px; cursor: pointer; transition: background 0.2s;">Choose Starter</button>
                    </div>

                    <!-- Pro Unlimited -->
                    <div class="pricing-card fade-in-right" style="border: 2px solid #8b5cf6; border-radius: 16px; padding: 2.5rem; background: linear-gradient(135deg, #ffffff 0%, #f3f0ff 100%); box-shadow: 0 4px 20px rgba(139, 92, 246, 0.1); max-width: 500px; width: 100%; position: relative;">
                        <div style="position: absolute; top: -12px; left: 50%; transform: translateX(-50%); background: #8b5cf6; color: white; padding: 0.25rem 1rem; border-radius: 12px; font-size: 0.75rem; font-weight: 600;">Most Popular</div>
                        
                        <!-- Title and Price -->
                        <div class="pricing-header" style="margin-bottom: 1.5rem;">
                            <h3 style="font-size: 1.5rem; font-weight: 700; color: #1f2937; margin-bottom: 0.5rem;">Pro Unlimited</h3>
                            <div style="display: flex; align-items: baseline; gap: 0.25rem; margin-bottom: 0.5rem;">
                                <span style="font-size: 1rem; color: #6b7280;">USD $</span>
                                <span style="font-size: 3rem; font-weight: 700; color: #1f2937; line-height: 1;">14.99</span>
                                <span style="font-size: 1rem; color: #6b7280;">/month</span>
                            </div>
                            <p style="font-size: 0.875rem; color: #6b7280;">Yearly: $11.99/month (Save 20%)</p>
                        </div>
                        
                        <!-- Features -->
                        <div style="margin-bottom: 1.5rem;">
                            <p style="font-weight: 600; margin-bottom: 1rem; color: #1f2937;">All Starter features, plus:</p>
                            <div style="display: flex; flex-direction: column; gap: 0.75rem;">
                                <div style="display: flex; align-items: start; font-size: 0.875rem;">
                                    <i class="fas fa-star" style="color: #f59e0b; margin-right: 0.75rem; margin-top: 0.2rem;"></i>
                                    <span><strong>Unlimited Processing</strong></span>
                                </div>
                                <div style="display: flex; align-items: start; font-size: 0.875rem;">
                                    <i class="fas fa-star" style="color: #f59e0b; margin-right: 0.75rem; margin-top: 0.2rem;"></i>
                                    <span><strong>Priority Processing Speed</strong></span>
                                </div>
                                <div style="display: flex; align-items: start; font-size: 0.875rem;">
                                    <i class="fas fa-star" style="color: #f59e0b; margin-right: 0.75rem; margin-top: 0.2rem;"></i>
                                    <span><strong>Batch Upload (Up to 50)</strong></span>
                                </div>
                                <div style="display: flex; align-items: start; font-size: 0.875rem;">
                                    <i class="fas fa-star" style="color: #f59e0b; margin-right: 0.75rem; margin-top: 0.2rem;"></i>
                                    <span>Permanent Data Retention</span>
                                </div>
                            </div>
                        </div>
                        
                        <!-- CTA Button -->
                        <button class="cta-btn" onclick="window.location.href='billing.html?plan=pro'" style="width: 100%; padding: 1rem; font-size: 1rem; font-weight: 600; background: #8b5cf6; color: white; border: none; border-radius: 8px; cursor: pointer; transition: background 0.2s;">Choose Pro</button>
                    </div>
                </div>'''

def update_en_index(filepath):
    """更新英文版index.html的pricing section"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 找到并替换pricing section
        pattern = r'(<!-- 月付和年付並列顯示 -->.*?</div>\s*</div>\s*</section>)'
        match = re.search(pattern, content, re.DOTALL)
        
        if match:
            old_section = match.group(1)
            new_section = PRICING_SECTION_EN + '\n            </div>\n        </section>'
            
            content = content.replace(old_section, new_section)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ 已更新: {filepath}")
            return True
        else:
            print(f"⚠️  未找到pricing section: {filepath}")
            return False
            
    except Exception as e:
        print(f"❌ 更新失败 {filepath}: {e}")
        return False

def update_zh_billing_pro_features():
    """更新中文版billing.html的Pro功能列表"""
    filepath = Path('billing.html')
    if not filepath.exists():
        print(f"❌ 找不到文件: {filepath}")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 替换Pro功能列表 - 移除"专属客户经理"，修改为完整列表
        # 找到Pro Unlimited的功能列表部分
        old_features = r'Starter 所有功能，plus：.*?</div>\s*</div>\s*</div>'
        
        new_features = '''Starter 所有功能，plus：</p>
                            <div style="display: flex; flex-direction: column; gap: 0.75rem;">
                                <div style="display: flex; align-items: start; font-size: 0.875rem;">
                                    <i class="fas fa-star" style="color: #f59e0b; margin-right: 0.75rem; margin-top: 0.2rem;"></i>
                                    <span><strong>無限處理頁數</strong></span>
                                </div>
                                <div style="display: flex; align-items: start; font-size: 0.875rem;">
                                    <i class="fas fa-star" style="color: #f59e0b; margin-right: 0.75rem; margin-top: 0.2rem;"></i>
                                    <span><strong>優先處理速度</strong></span>
                                </div>
                                <div style="display: flex; align-items: start; font-size: 0.875rem;">
                                    <i class="fas fa-star" style="color: #f59e0b; margin-right: 0.75rem; margin-top: 0.2rem;"></i>
                                    <span><strong>批量上傳（最多50份）</strong></span>
                                </div>
                                <div style="display: flex; align-items: start; font-size: 0.875rem;">
                                    <i class="fas fa-star" style="color: #f59e0b; margin-right: 0.75rem; margin-top: 0.2rem;"></i>
                                    <span>永久數據保留</span>
                                </div>
                            </div>
                        </div>'''
        
        content = re.sub(old_features, new_features, content, flags=re.DOTALL)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 已更新中文版billing.html的Pro功能列表")
        return True
        
    except Exception as e:
        print(f"❌ 更新失败: {e}")
        return False

def main():
    print("🚀 开始最终修复...")
    print()
    
    # 1. 更新中文版billing.html
    print("📂 更新中文版billing.html的Pro功能列表...")
    update_zh_billing_pro_features()
    print()
    
    # 2. 更新英文版index.html
    print("📂 更新英文版index.html为双层定价...")
    root = Path('.')
    en_index = root / 'en' / 'index.html'
    if en_index.exists():
        update_en_index(en_index)
    else:
        print(f"❌ 找不到文件: {en_index}")
    
    print()
    print("=" * 80)
    print("✨ 修复完成！")
    print()
    print("📋 请检查：")
    print("  1. 中文版billing.html - Pro功能列表已更新（移除专属客户经理）")
    print("  2. 英文版index.html - 双层定价结构已应用")

if __name__ == '__main__':
    main()

