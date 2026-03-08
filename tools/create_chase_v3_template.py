#!/usr/bin/env python3
"""
创建Chase Bank v3完整内容模板
添加: How It Works + Use Cases + Comparison + Extended FAQ + Technical Details
"""
import os

# 读取v2版本
with open('chase-bank-statement-v2.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 新增内容sections
how_it_works_section = '''
    <!-- How It Works Section -->
    <section style="padding: var(--space-20) var(--space-6); background: white;">
        <div style="max-width: 1200px; margin: 0 auto;">
            <h2 style="font-size: var(--text-4xl); font-weight: var(--font-bold); text-align: center; margin-bottom: var(--space-4); color: var(--gray-900);">
                How to Convert Chase Bank Statements in 4 Simple Steps
            </h2>
            <p style="text-align: center; color: var(--gray-600); font-size: var(--text-lg); margin-bottom: var(--space-16); max-width: 800px; margin-left: auto; margin-right: auto;">
                From PDF to Excel/QuickBooks in under 3 seconds. No manual data entry required.
            </p>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: var(--space-10);">
                <!-- Step 1 -->
                <div style="position: relative; padding: var(--space-8); background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); border-radius: var(--radius-2xl); border-left: 4px solid var(--primary-blue);">
                    <div style="position: absolute; top: -16px; left: var(--space-6); background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); width: 48px; height: 48px; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: var(--font-bold); font-size: var(--text-2xl); box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);">
                        1
                    </div>
                    <h3 style="font-size: var(--text-xl); font-weight: var(--font-bold); color: var(--gray-900); margin-top: var(--space-8); margin-bottom: var(--space-3);">
                        Upload Your Chase Statement
                    </h3>
                    <p style="color: var(--gray-600); line-height: 1.7; margin: 0;">
                        Simply drag and drop your PDF, JPG, or PNG files. We support all Chase account types including checking, savings, credit cards, and business accounts.
                    </p>
                </div>
                
                <!-- Step 2 -->
                <div style="position: relative; padding: var(--space-8); background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%); border-radius: var(--radius-2xl); border-left: 4px solid var(--success);">
                    <div style="position: absolute; top: -16px; left: var(--space-6); background: linear-gradient(135deg, #10b981 0%, #059669 100%); width: 48px; height: 48px; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: var(--font-bold); font-size: var(--text-2xl); box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);">
                        2
                    </div>
                    <h3 style="font-size: var(--text-xl); font-weight: var(--font-bold); color: var(--gray-900); margin-top: var(--space-8); margin-bottom: var(--space-3);">
                        AI Processing
                    </h3>
                    <p style="color: var(--gray-600); line-height: 1.7; margin: 0;">
                        Our AI engine, specifically trained on Chase Bank formats, automatically extracts all transactions, dates, amounts, and descriptions with 98% accuracy in just 3 seconds.
                    </p>
                </div>
                
                <!-- Step 3 -->
                <div style="position: relative; padding: var(--space-8); background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); border-radius: var(--radius-2xl); border-left: 4px solid var(--warning);">
                    <div style="position: absolute; top: -16px; left: var(--space-6); background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); width: 48px; height: 48px; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: var(--font-bold); font-size: var(--text-2xl); box-shadow: 0 4px 12px rgba(245, 158, 11, 0.4);">
                        3
                    </div>
                    <h3 style="font-size: var(--text-xl); font-weight: var(--font-bold); color: var(--gray-900); margin-top: var(--space-8); margin-bottom: var(--space-3);">
                        Export to Your System
                    </h3>
                    <p style="color: var(--gray-600); line-height: 1.7; margin: 0;">
                        Choose your preferred format: Excel (XLSX), CSV, QuickBooks (QBO), or Xero. Our exports are pre-formatted and ready to import without any manual adjustments.
                    </p>
                </div>
                
                <!-- Step 4 -->
                <div style="position: relative; padding: var(--space-8); background: linear-gradient(135deg, #fce7f3 0%, #fbcfe8 100%); border-radius: var(--radius-2xl); border-left: 4px solid var(--pink);">
                    <div style="position: absolute; top: -16px; left: var(--space-6); background: linear-gradient(135deg, #ec4899 0%, #db2777 100%); width: 48px; height: 48px; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: var(--font-bold); font-size: var(--text-2xl); box-shadow: 0 4px 12px rgba(236, 72, 153, 0.4);">
                        4
                    </div>
                    <h3 style="font-size: var(--text-xl); font-weight: var(--font-bold); color: var(--gray-900); margin-top: var(--space-8); margin-bottom: var(--space-3);">
                        Verify & Save
                    </h3>
                    <p style="color: var(--gray-600); line-height: 1.7; margin: 0;">
                        Review the extracted data in our dashboard. Make any necessary adjustments, then download or directly sync to your accounting software. All files auto-delete after 24 hours.
                    </p>
                </div>
            </div>
        </div>
    </section>
'''

print("🚀 Phase 1: Creating Chase Bank v3 Complete Template")
print("=" * 60)
print("\n📝 Adding new sections:")
print("  ✅ How It Works (4 steps)")
print("  ⏳ Use Cases (3 customer stories)")
print("  ⏳ Comparison Table")
print("  ⏳ Extended FAQ (10 questions)")
print("  ⏳ Technical Details")
print("\n⏳ Processing...")

# 找到Features Section后面的位置插入
insert_point = content.find('<!-- Related Pages Section -->')

if insert_point == -1:
    print("❌ Error: Could not find Related Pages Section")
    exit(1)

# 插入How It Works Section
new_content = content[:insert_point] + how_it_works_section + '\n' + content[insert_point:]

# 写入新文件
with open('chase-bank-statement-v3.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"\n✅ Step 1/5 Complete: How It Works Section added")
print(f"📄 File: chase-bank-statement-v3.html")
print(f"📊 Current size: {len(new_content)} characters")
print(f"\n⏭️  Next: Adding Use Cases Section...")
