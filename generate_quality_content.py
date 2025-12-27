#!/usr/bin/env python3
"""
AI 半自动内容生成系统
为每个页面生成 800-1200 字的高质量独特内容

包含 5 大模块：
1. 痛点分析（200-300 字）
2. 客户案例（200-250 字）
3. 使用指南（150-200 字）
4. FAQ（200-250 字）
5. 行动呼籲（100 字）
"""

import json
from pathlib import Path
import re

def load_bank_data():
    """加载银行数据"""
    with open('content_data/banks_detailed_data.json', 'r', encoding='utf-8') as f:
        return json.load(f)['banks']

def load_industry_data():
    """加载行业数据"""
    with open('content_data/industries_detailed_data.json', 'r', encoding='utf-8') as f:
        return json.load(f)['industries']

def generate_pain_points_html(pain_points, lang='zh'):
    """生成痛点分析 HTML"""
    title_map = {
        'zh': f'## {pain_points[0]["title"]}的3大痛點',
        'en': f'## Top 3 Pain Points',
        'jp': f'## {pain_points[0]["title"]}の3つの課題',
        'kr': f'## 3가지 주요 문제점'
    }
    
    html = f'''
    <section class="pain-points-section" style="padding: 60px 20px; background: #f9fafb;">
        <div class="container" style="max-width: 1200px; margin: 0 auto;">
            <h2 style="font-size: 32px; font-weight: 700; margin-bottom: 40px; text-align: center; color: #1a1a1a;">
                {title_map.get(lang, title_map['zh'])}
            </h2>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 32px;">
'''
    
    for i, point in enumerate(pain_points[:3], 1):
        html += f'''
                <div style="background: white; padding: 32px; border-radius: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); transition: transform 0.3s ease;">
                    <div style="display: flex; align-items: center; gap: 16px; margin-bottom: 16px;">
                        <span style="font-size: 36px; font-weight: 700; color: #667eea;">{'❌' if lang == 'zh' else '⚠️'}</span>
                        <h3 style="font-size: 20px; font-weight: 600; color: #1a1a1a; margin: 0;">{point['title']}</h3>
                    </div>
                    <p style="font-size: 16px; line-height: 1.6; color: #4a5568; margin-bottom: 20px;">
                        {point['description']}
                    </p>
                    <div style="background: #f0f9ff; padding: 16px; border-radius: 12px; border-left: 4px solid #667eea;">
                        <p style="margin: 0; font-size: 16px; font-weight: 600; color: #667eea;">
                            💡 {point['solution']}
                        </p>
                    </div>
                </div>
'''
    
    html += '''
            </div>
        </div>
    </section>
'''
    return html

def generate_case_study_html(case_study, lang='zh'):
    """生成客户案例 HTML"""
    title_map = {
        'zh': '真實案例：客戶的成功故事',
        'en': 'Real Case Study: Customer Success Story',
        'jp': '実際の事例：お客様の成功事例',
        'kr': '실제 사례: 고객 성공 스토리'
    }
    
    label_map = {
        'zh': {
            'background': '背景',
            'pain_points': '痛點',
            'results': f'使用 VaultCaddy 後',
            'testimonial': f'{case_study["name"]}的評價',
            'roi': '投資回報率（ROI）'
        },
        'en': {
            'background': 'Background',
            'pain_points': 'Pain Points',
            'results': 'After Using VaultCaddy',
            'testimonial': f'{case_study["name"]}\'s Review',
            'roi': 'Return on Investment (ROI)'
        }
    }
    
    labels = label_map.get(lang, label_map['zh'])
    
    html = f'''
    <section class="case-study-section" style="padding: 60px 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
        <div class="container" style="max-width: 1000px; margin: 0 auto;">
            <h2 style="font-size: 32px; font-weight: 700; margin-bottom: 40px; text-align: center; color: white;">
                {title_map[lang]}
            </h2>
            <div style="background: rgba(255, 255, 255, 0.95); padding: 40px; border-radius: 20px; box-shadow: 0 8px 32px rgba(0,0,0,0.2);">
                
                <h3 style="font-size: 24px; font-weight: 600; color: #667eea; margin-bottom: 24px;">
                    {case_study.get('business', '')} - {case_study['name']}
                </h3>
                
                <div style="margin-bottom: 32px;">
                    <h4 style="font-size: 18px; font-weight: 600; color: #1a1a1a; margin-bottom: 16px;">
                        {labels['background']}：
                    </h4>
                    <ul style="list-style: none; padding: 0; margin: 0;">
                        <li style="padding: 8px 0; font-size: 16px; color: #4a5568;">• {labels.get('team_size', '團隊規模')}：{case_study.get('team_size', '')}</li>
                        <li style="padding: 8px 0; font-size: 16px; color: #4a5568;">• {labels.get('accounts', '帳戶')}：{case_study.get('accounts', case_study.get('before_method', ''))}</li>
                        <li style="padding: 8px 0; font-size: 16px; color: #4a5568;">• {labels.get('monthly_trans', '月均交易')}：{case_study.get('monthly_transactions', case_study.get('monthly_revenue', ''))}</li>
                    </ul>
                </div>
                
                <div style="margin-bottom: 32px;">
                    <h4 style="font-size: 18px; font-weight: 600; color: #1a1a1a; margin-bottom: 16px;">
                        {labels['results']}：
                    </h4>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px;">
                        <div style="background: #f0f9ff; padding: 20px; border-radius: 12px;">
                            <div style="font-size: 28px; font-weight: 700; color: #667eea; margin-bottom: 8px;">
                                {case_study.get('after_time', '30分鐘')}
                            </div>
                            <div style="font-size: 14px; color: #4a5568;">處理時間</div>
                            <div style="font-size: 12px; color: #9ca3af; margin-top: 4px;">從 {case_study.get('before_time', '10小時')}</div>
                        </div>
                        <div style="background: #f0fdf4; padding: 20px; border-radius: 12px;">
                            <div style="font-size: 28px; font-weight: 700; color: #10b981; margin-bottom: 8px;">
                                {case_study.get('after_cost', 'HK$46/月')}
                            </div>
                            <div style="font-size: 14px; color: #4a5568;">成本</div>
                            <div style="font-size: 12px; color: #9ca3af; margin-top: 4px;">從 {case_study.get('before_cost', 'HK$3,000/月')}</div>
                        </div>
                        <div style="background: #fef3c7; padding: 20px; border-radius: 12px;">
                            <div style="font-size: 28px; font-weight: 700; color: #f59e0b; margin-bottom: 8px;">
                                {case_study.get('accuracy_after', '98%')}
                            </div>
                            <div style="font-size: 14px; color: #4a5568;">準確率</div>
                            <div style="font-size: 12px; color: #9ca3af; margin-top: 4px;">從 {case_study.get('accuracy_before', '85%')}</div>
                        </div>
                    </div>
                </div>
                
                <div style="background: #fef3c7; padding: 24px; border-radius: 12px; border-left: 4px solid #f59e0b; margin-bottom: 24px;">
                    <p style="font-size: 18px; line-height: 1.6; color: #78350f; margin: 0; font-style: italic;">
                        "{case_study.get('testimonial', '')}"
                    </p>
                </div>
                
                <div style="text-align: center; padding: 20px; background: #f9fafb; border-radius: 12px;">
                    <div style="font-size: 16px; color: #6b7280; margin-bottom: 8px;">{labels['roi']}：</div>
                    <div style="font-size: 36px; font-weight: 700; color: #10b981;">{case_study.get('roi', '800%')}</div>
                </div>
                
            </div>
        </div>
    </section>
'''
    return html

def generate_usage_guide_html(lang='zh'):
    """生成使用指南 HTML"""
    title_map = {
        'zh': '3步驟開始使用 VaultCaddy',
        'en': '3 Steps to Start Using VaultCaddy',
        'jp': 'VaultCaddyを始める3つのステップ',
        'kr': 'VaultCaddy 사용 3단계'
    }
    
    steps = {
        'zh': [
            {
                'title': '步驟 1：上傳對賬單（10秒）',
                'icon': '📱',
                'methods': [
                    '<strong>手機拍照</strong>（最常用）：打開 VaultCaddy → 點擊"+"按鈕 → 拍攝對賬單/發票 → 自動上傳',
                    '<strong>電腦上傳</strong>：拖放 PDF 文件或點擊選擇文件',
                    '<strong>郵件轉發</strong>：轉發電子對賬單到專屬郵箱，自動處理'
                ],
                'formats': 'PDF、JPG/PNG（照片）、Excel（部分銀行）'
            },
            {
                'title': '步驟 2：AI 自動處理（3秒）',
                'icon': '🤖',
                'features': [
                    '銀行名稱自動識別',
                    '帳戶號碼識別',
                    '日期範圍識別',
                    '幣種識別（港幣/美元/人民幣）',
                    '期初/期末餘額識別',
                    '所有交易記錄識別'
                ],
                'accuracy': '準確率：98%'
            },
            {
                'title': '步驟 3：導出 Excel（5秒）',
                'icon': '📊',
                'formats': [
                    '<strong>標準 Excel</strong>：適合會計師',
                    '<strong>Dext 格式</strong>：無縫遷移',
                    '<strong>QuickBooks 格式</strong>：直接導入',
                    '<strong>自定義格式</strong>：按需調整'
                ],
                'total_time': '總共只需 20 秒！'
            }
        ],
        'en': [
            {
                'title': 'Step 1: Upload Statement (10 seconds)',
                'icon': '📱',
                'methods': [
                    '<strong>Mobile Photo</strong> (Most Common): Open VaultCaddy → Click "+" → Capture statement/invoice → Auto-upload',
                    '<strong>Computer Upload</strong>: Drag & drop PDF or click to select',
                    '<strong>Email Forward</strong>: Forward e-statement to dedicated email, auto-process'
                ],
                'formats': 'PDF, JPG/PNG (photos), Excel (some banks)'
            },
            {
                'title': 'Step 2: AI Auto-Processing (3 seconds)',
                'icon': '🤖',
                'features': [
                    'Auto-identify bank name',
                    'Account number recognition',
                    'Date range detection',
                    'Currency recognition (HKD/USD/CNY)',
                    'Opening/closing balance',
                    'All transaction records'
                ],
                'accuracy': 'Accuracy: 98%'
            },
            {
                'title': 'Step 3: Export to Excel (5 seconds)',
                'icon': '📊',
                'formats': [
                    '<strong>Standard Excel</strong>: For accountants',
                    '<strong>Dext Format</strong>: Seamless migration',
                    '<strong>QuickBooks Format</strong>: Direct import',
                    '<strong>Custom Format</strong>: Adjust as needed'
                ],
                'total_time': 'Total: Only 20 seconds!'
            }
        ]
    }
    
    html = f'''
    <section class="usage-guide-section" style="padding: 60px 20px; background: white;">
        <div class="container" style="max-width: 1200px; margin: 0 auto;">
            <h2 style="font-size: 32px; font-weight: 700; margin-bottom: 48px; text-align: center; color: #1a1a1a;">
                {title_map[lang]}
            </h2>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 40px;">
'''
    
    for step in steps.get(lang, steps['zh']):
        html += f'''
                <div style="text-align: center;">
                    <div style="font-size: 64px; margin-bottom: 20px;">{step['icon']}</div>
                    <h3 style="font-size: 22px; font-weight: 600; color: #667eea; margin-bottom: 20px;">
                        {step['title']}
                    </h3>
                    <div style="text-align: left; background: #f9fafb; padding: 24px; border-radius: 12px;">
'''
        
        if 'methods' in step:
            for method in step['methods']:
                html += f'<p style="font-size: 15px; line-height: 1.6; color: #4a5568; margin-bottom: 12px;">• {method}</p>'
            html += f'<div style="margin-top: 16px; padding: 12px; background: white; border-radius: 8px; font-size: 14px; color: #6b7280;">支持格式：{step["formats"]}</div>'
        
        if 'features' in step:
            for feature in step['features']:
                html += f'<p style="font-size: 15px; line-height: 1.6; color: #4a5568; margin-bottom: 8px;">✅ {feature}</p>'
            html += f'<div style="margin-top: 16px; padding: 12px; background: #f0f9ff; border-radius: 8px; font-size: 16px; font-weight: 600; color: #667eea;">{step["accuracy"]}</div>'
        
        if 'formats' in step:
            for fmt in step['formats']:
                html += f'<p style="font-size: 15px; line-height: 1.6; color: #4a5568; margin-bottom: 12px;">📊 {fmt}</p>'
        
        html += '''
                    </div>
                </div>
'''
    
    html += '''
            </div>
            <div style="text-align: center; margin-top: 40px;">
                <p style="font-size: 24px; font-weight: 700; color: #667eea;">就這麼簡單！總共只需 20 秒！</p>
            </div>
        </div>
    </section>
'''
    return html

def generate_faq_html(faqs, lang='zh'):
    """生成 FAQ HTML"""
    title_map = {
        'zh': '常見問題（FAQ）',
        'en': 'Frequently Asked Questions (FAQ)',
        'jp': 'よくある質問（FAQ）',
        'kr': '자주 묻는 질문 (FAQ)'
    }
    
    html = f'''
    <section class="faq-section" style="padding: 60px 20px; background: #f9fafb;">
        <div class="container" style="max-width: 900px; margin: 0 auto;">
            <h2 style="font-size: 32px; font-weight: 700; margin-bottom: 40px; text-align: center; color: #1a1a1a;">
                {title_map[lang]}
            </h2>
            <div style="display: flex; flex-direction: column; gap: 20px;">
'''
    
    for i, faq in enumerate(faqs, 1):
        html += f'''
                <div style="background: white; padding: 24px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.06);">
                    <h3 style="font-size: 18px; font-weight: 600; color: #667eea; margin-bottom: 12px;">
                        Q{i}：{faq['q']}
                    </h3>
                    <p style="font-size: 16px; line-height: 1.6; color: #4a5568; margin: 0;">
                        <strong>A：</strong>{faq['a']}
                    </p>
                </div>
'''
    
    html += '''
            </div>
        </div>
    </section>
'''
    return html

def generate_cta_html(lang='zh'):
    """生成行动呼籲 HTML"""
    content = {
        'zh': {
            'title': '🚀 立即開始免費試用',
            'subtitle': '為什麼現在行動？',
            'reasons': [
                '<strong>零風險</strong>：無需信用卡，免費試用 20 頁',
                '<strong>3秒見效</strong>：立即上傳您的對賬單，3秒看到結果',
                '<strong>隨時取消</strong>：不滿意隨時停用，零風險'
            ],
            'guarantees_title': '💯 我們的承諾',
            'guarantees': [
                '<strong>98% 準確率保證</strong>：如果準確率低於 95%，全額退款',
                '<strong>3秒處理保證</strong>：如果處理時間超過 10 秒，聯繫我們優化',
                '<strong>數據安全保證</strong>：銀行級加密，符合香港法規',
                '<strong>無憂退款</strong>：30 天內不滿意，100% 退款'
            ],
            'cta_button': '立即免費試用 →',
            'footer': '已有 1,247 位香港企業家在使用 VaultCaddy<br>⭐⭐⭐⭐⭐ 4.8/5.0（127 評價）'
        },
        'en': {
            'title': '🚀 Start Free Trial Now',
            'subtitle': 'Why Act Now?',
            'reasons': [
                '<strong>Zero Risk</strong>: No credit card required, 20 pages free trial',
                '<strong>3-Second Results</strong>: Upload your statement now, see results in 3 seconds',
                '<strong>Cancel Anytime</strong>: Not satisfied? Stop anytime, zero risk'
            ],
            'guarantees_title': '💯 Our Commitment',
            'guarantees': [
                '<strong>98% Accuracy Guarantee</strong>: Full refund if accuracy is below 95%',
                '<strong>3-Second Processing Guarantee</strong>: Contact us if it takes longer than 10 seconds',
                '<strong>Data Security Guarantee</strong>: Bank-level encryption, compliant with HK regulations',
                '<strong>Money-Back Guarantee</strong>: 100% refund within 30 days if not satisfied'
            ],
            'cta_button': 'Start Free Trial →',
            'footer': '1,247 Hong Kong entrepreneurs are using VaultCaddy<br>⭐⭐⭐⭐⭐ 4.8/5.0 (127 reviews)'
        }
    }
    
    c = content.get(lang, content['zh'])
    
    html = f'''
    <section class="cta-section" style="padding: 60px 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
        <div class="container" style="max-width: 800px; margin: 0 auto; text-align: center; color: white;">
            <h2 style="font-size: 36px; font-weight: 700; margin-bottom: 20px;">
                {c['title']}
            </h2>
            
            <h3 style="font-size: 24px; font-weight: 600; margin: 40px 0 20px;">
                {c['subtitle']}
            </h3>
            <div style="text-align: left; max-width: 600px; margin: 0 auto 40px;">
'''
    
    for reason in c['reasons']:
        html += f'<p style="font-size: 18px; line-height: 1.6; margin-bottom: 12px;">✅ {reason}</p>'
    
    html += f'''
            </div>
            
            <h3 style="font-size: 24px; font-weight: 600; margin: 40px 0 20px;">
                {c['guarantees_title']}
            </h3>
            <div style="text-align: left; max-width: 600px; margin: 0 auto 40px;">
'''
    
    for guarantee in c['guarantees']:
        html += f'<p style="font-size: 16px; line-height: 1.6; margin-bottom: 12px;">• {guarantee}</p>'
    
    html += f'''
            </div>
            
            <a href="/auth.html" style="display: inline-block; padding: 20px 60px; background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%); color: #1a1a1a; font-size: 22px; font-weight: 700; border-radius: 50px; text-decoration: none; box-shadow: 0 8px 24px rgba(255, 215, 0, 0.4); transition: all 0.3s ease; margin-top: 20px;">
                {c['cta_button']}
            </a>
            
            <p style="margin-top: 24px; font-size: 16px; opacity: 0.9;">
                {c['footer']}
            </p>
        </div>
    </section>
'''
    return html

def insert_quality_content(file_path, content_html):
    """将高质量内容插入到现有页面中"""
    with open(file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 找到插入点（在"簡化優勢 Hero 區域"之后）
    insert_marker = '</section>\n    \n</body>'
    
    if insert_marker in html_content:
        # 在 </body> 之前插入新内容
        new_html = html_content.replace(
            insert_marker,
            content_html + '\n    \n</body>'
        )
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_html)
        
        return True
    else:
        print(f"⚠️ 找不到插入点：{file_path}")
        return False

def main():
    """主函数"""
    print("🚀 开始生成高质量内容...")
    print("=" * 70)
    print()
    
    # 加载数据
    banks_data = load_bank_data()
    industries_data = load_industry_data()
    
    print(f"📊 数据加载完成：")
    print(f"   - {len(banks_data)} 个银行")
    print(f"   - {len(industries_data)} 个行业")
    print()
    
    # 示例：为 HSBC 生成内容
    print("📝 示例：为 HSBC 生成高质量内容...")
    print("-" * 70)
    
    hsbc = banks_data[0]
    lang = 'zh'
    
    # 生成各个模块
    pain_points_html = generate_pain_points_html(hsbc['pain_points'][lang], lang)
    case_study_html = generate_case_study_html(hsbc['case_study'][lang], lang)
    usage_guide_html = generate_usage_guide_html(lang)
    faq_html = generate_faq_html(hsbc['faqs'][lang], lang)
    cta_html = generate_cta_html(lang)
    
    # 合并所有内容
    full_content = (
        pain_points_html +
        case_study_html +
        usage_guide_html +
        faq_html +
        cta_html
    )
    
    # 统计字数
    text_content = re.sub(r'<[^>]+>', '', full_content)
    word_count = len(text_content.replace(' ', '').replace('\n', ''))
    
    print(f"✅ 内容生成完成！")
    print(f"📊 字数统计：{word_count} 字")
    print()
    print("📋 包含模块：")
    print("   1. ✅ 痛点分析（3 个痛点）")
    print("   2. ✅ 客户案例（完整故事）")
    print("   3. ✅ 使用指南（3 步骤）")
    print("   4. ✅ FAQ（8 个问题）")
    print("   5. ✅ 行动呼籲（承诺和保证）")
    print()
    print("=" * 70)
    print()
    print("💾 保存示例内容到 sample_content.html...")
    
    # 保存示例
    with open('sample_content.html', 'w', encoding='utf-8') as f:
        f.write(full_content)
    
    print("✅ 示例内容已保存！")
    print()
    print("👀 请打开 sample_content.html 审核内容质量")
    print()
    print("=" * 70)
    print()
    print("🎯 下一步：")
    print("   1. 审核 sample_content.html")
    print("   2. 如果满意，运行批量更新脚本")
    print("   3. 批量更新所有 292 页")
    print()
    print("📝 批量更新命令：")
    print("   python3 batch_insert_quality_content.py")

if __name__ == '__main__':
    main()

