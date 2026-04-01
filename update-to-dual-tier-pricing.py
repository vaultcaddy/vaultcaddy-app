#!/usr/bin/env python3
"""
更新所有页面到双层定价结构
- Starter: 入门版（100页/月）
- Pro Unlimited: 专业版（无限页）
"""

import re
from pathlib import Path

# 双层定价HTML模板 - 中文版
PRICING_SECTION_ZH = '''                <!-- Starter 和 Pro 並列顯示 -->
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; max-width: 1000px; margin: 0 auto;">
                    <!-- Starter 入門版 -->
                    <div class="pricing-card fade-in-left" style="border: 2px solid #e5e7eb; border-radius: 16px; padding: 2.5rem; background: white; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05); max-width: 500px; width: 100%;">
                        <!-- 標題和價格 -->
                        <div class="pricing-header" style="margin-bottom: 1.5rem;">
                            <h3 style="font-size: 1.5rem; font-weight: 700; color: #1f2937; margin-bottom: 0.5rem;">Starter 入門版</h3>
                            <div style="display: flex; align-items: baseline; gap: 0.25rem; margin-bottom: 0.5rem;">
                                <span style="font-size: 1rem; color: #6b7280;">HKD $</span>
                                <span style="font-size: 3rem; font-weight: 700; color: #1f2937; line-height: 1;">28</span>
                                <span style="font-size: 1rem; color: #6b7280;">/月</span>
                            </div>
                            <p style="font-size: 0.875rem; color: #6b7280;">年付僅 $22/月（省20%）</p>
                        </div>
                        
                        <!-- 功能列表 -->
                        <div style="margin-bottom: 1.5rem;">
                            <p style="font-weight: 600; margin-bottom: 1rem; color: #1f2937;">包含功能：</p>
                            <div style="display: flex; flex-direction: column; gap: 0.75rem;">
                                <div style="display: flex; align-items: start; font-size: 0.875rem;">
                                    <i class="fas fa-check" style="color: #10b981; margin-right: 0.75rem; margin-top: 0.2rem;"></i>
                                    <span>每月 100 Credits（超出 $0.5/頁）</span>
                                </div>
                                <div style="display: flex; align-items: start; font-size: 0.875rem;">
                                    <i class="fas fa-check" style="color: #10b981; margin-right: 0.75rem; margin-top: 0.2rem;"></i>
                                    <span>批次處理無限制文件</span>
                                </div>
                                <div style="display: flex; align-items: start; font-size: 0.875rem;">
                                    <i class="fas fa-check" style="color: #10b981; margin-right: 0.75rem; margin-top: 0.2rem;"></i>
                                    <span>Excel/CSV/QBO 匯出</span>
                                </div>
                                <div style="display: flex; align-items: start; font-size: 0.875rem;">
                                    <i class="fas fa-check" style="color: #10b981; margin-right: 0.75rem; margin-top: 0.2rem;"></i>
                                    <span>QuickBooks/Xero 整合</span>
                                </div>
                                <div style="display: flex; align-items: start; font-size: 0.875rem;">
                                    <i class="fas fa-check" style="color: #10b981; margin-right: 0.75rem; margin-top: 0.2rem;"></i>
                                    <span>8 種語言支援</span>
                                </div>
                                <div style="display: flex; align-items: start; font-size: 0.875rem;">
                                    <i class="fas fa-check" style="color: #10b981; margin-right: 0.75rem; margin-top: 0.2rem;"></i>
                                    <span>365 天數據保留</span>
                                </div>
                            </div>
                        </div>
                        
                        <!-- CTA 按鈕 -->
                        <button class="cta-btn" onclick="window.location.href='billing.html?plan=starter'" style="width: 100%; padding: 1rem; font-size: 1rem; font-weight: 600; background: #8b5cf6; color: white; border: none; border-radius: 8px; cursor: pointer; transition: background 0.2s;">選擇 Starter</button>
                    </div>

                    <!-- Pro Unlimited 專業版 -->
                    <div class="pricing-card fade-in-right" style="border: 2px solid #8b5cf6; border-radius: 16px; padding: 2.5rem; background: linear-gradient(135deg, #ffffff 0%, #f3f0ff 100%); box-shadow: 0 4px 20px rgba(139, 92, 246, 0.1); max-width: 500px; width: 100%; position: relative;">
                        <div style="position: absolute; top: -12px; left: 50%; transform: translateX(-50%); background: #8b5cf6; color: white; padding: 0.25rem 1rem; border-radius: 12px; font-size: 0.75rem; font-weight: 600;">最受歡迎</div>
                        
                        <!-- 標題和價格 -->
                        <div class="pricing-header" style="margin-bottom: 1.5rem;">
                            <h3 style="font-size: 1.5rem; font-weight: 700; color: #1f2937; margin-bottom: 0.5rem;">Pro Unlimited</h3>
                            <div style="display: flex; align-items: baseline; gap: 0.25rem; margin-bottom: 0.5rem;">
                                <span style="font-size: 1rem; color: #6b7280;">HKD $</span>
                                <span style="font-size: 3rem; font-weight: 700; color: #1f2937; line-height: 1;">118</span>
                                <span style="font-size: 1rem; color: #6b7280;">/月</span>
                            </div>
                            <p style="font-size: 0.875rem; color: #6b7280;">年付僅 $93/月（省20%）</p>
                        </div>
                        
                        <!-- 功能列表 -->
                        <div style="margin-bottom: 1.5rem;">
                            <p style="font-weight: 600; margin-bottom: 1rem; color: #1f2937;">Starter 所有功能，plus：</p>
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
                                    <span>專屬客戶經理</span>
                                </div>
                                <div style="display: flex; align-items: start; font-size: 0.875rem;">
                                    <i class="fas fa-star" style="color: #f59e0b; margin-right: 0.75rem; margin-top: 0.2rem;"></i>
                                    <span>永久數據保留</span>
                                </div>
                            </div>
                        </div>
                        
                        <!-- CTA 按鈕 -->
                        <button class="cta-btn" onclick="window.location.href='billing.html?plan=pro'" style="width: 100%; padding: 1rem; font-size: 1rem; font-weight: 600; background: #8b5cf6; color: white; border: none; border-radius: 8px; cursor: pointer; transition: background 0.2s;">選擇 Pro</button>
                    </div>
                </div>'''

def update_index_html(filepath):
    """更新index.html的pricing section"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 找到pricing section的开始和结束
        pattern = r'(<!-- 月付和年付並列顯示 -->.*?</div>\s*</div>\s*</section>)'
        match = re.search(pattern, content, re.DOTALL)
        
        if match:
            # 替换整个pricing section
            old_section = match.group(1)
            new_section = PRICING_SECTION_ZH + '\n            </div>\n        </section>'
            
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

def main():
    """主函数"""
    print("🚀 开始更新到双层定价结构...")
    print()
    
    # 更新中文版index.html
    root = Path('.')
    index_file = root / 'index.html'
    
    if index_file.exists():
        if update_index_html(index_file):
            print()
            print("✨ 更新完成！")
            print()
            print("📋 新定价结构:")
            print("  - Starter 入門版: HKD $28/月（年付$22）")
            print("  - Pro Unlimited: HKD $118/月（年付$93）")
        else:
            print()
            print("❌ 更新失败")
    else:
        print(f"❌ 找不到文件: {index_file}")

if __name__ == '__main__':
    main()

