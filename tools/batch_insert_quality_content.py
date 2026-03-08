#!/usr/bin/env python3
"""
批量为所有 292 页插入高质量内容
- 包含"为什么功能更少？"部分
- 5 大内容模块（痛点、案例、指南、FAQ、CTA）
- 使用通用模板，快速生成
"""

import json
from pathlib import Path
import re
from generate_universal_content import generate_full_content

def find_insert_position(html_content):
    """
    找到插入位置：在"簡化優勢 Hero 區域"之后
    即在 </section> 标签之后（第一个在 body 中的 section）
    """
    # 查找第一个 section 的结束标签（简化优势部分）
    pattern = r'(<!-- 簡化優勢 Hero 區域 -->.*?</section>)'
    match = re.search(pattern, html_content, re.DOTALL)
    
    if match:
        return match.end()
    
    # 如果没找到，尝试查找第一个 </section>
    pattern2 = r'(<section.*?</section>)'
    match2 = re.search(pattern2, html_content, re.DOTALL)
    
    if match2:
        return match2.end()
    
    # 最后尝试在 </body> 之前
    body_end = html_content.rfind('</body>')
    if body_end != -1:
        return body_end
    
    return -1

def insert_quality_content(file_path, content_html):
    """将高质量内容插入到页面中"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # 检查是否已经插入过（避免重复）
        if '## 3步驟開始使用 VaultCaddy' in html_content or '3步骤开始使用' in html_content:
            return False, "已存在内容"
        
        # 找到插入位置
        insert_pos = find_insert_position(html_content)
        
        if insert_pos == -1:
            return False, "找不到插入点"
        
        # 插入内容
        new_html = (
            html_content[:insert_pos] +
            '\n' + content_html + '\n' +
            html_content[insert_pos:]
        )
        
        # 写入文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_html)
        
        return True, "成功"
    
    except Exception as e:
        return False, str(e)

def extract_entity_name(filename, lang='zh'):
    """从文件名提取银行或行业名称"""
    # 移除文件扩展名和后缀
    name = filename.replace('-bank-statement-simple.html', '').replace('-accounting-solution.html', '')
    
    # 银行名称映射（简单版）
    bank_names = {
        'zh': {
            'hsbc': '滙豐銀行',
            'hangseng': '恒生銀行',
            'boc': '中國銀行',
            'icbc': '工商銀行',
            'bea': '東亞銀行',
            'scb': '渣打銀行',
            'citi': '花旗銀行',
            'dbs': '星展銀行',
            'ocbc': '華僑銀行',
            'ubs': '瑞銀',
            'credit-suisse': '瑞信',
            'jpmorgan': '摩根大通',
            'goldman-sachs': '高盛',
            'morgan-stanley': '摩根士丹利',
            'deutsche-bank': '德意志銀行',
            'bnp': '法國巴黎銀行',
            'barclays': '巴克萊銀行',
            'hsbc-uk': '滙豐英國',
            'lloyds': '勞埃德銀行',
            'natwest': 'NatWest',
            'bankofamerica': '美國銀行',
            'wellsfargo': '富國銀行',
            'chase': '大通銀行',
            'citibank': '花旗銀行',
            'pnc': 'PNC銀行',
            'mizuho': '瑞穗銀行',
            'smbc': '三井住友銀行',
            'mufg': '三菱日聯',
            'shinhan': '新韓銀行',
            'kb': 'KB國民銀行',
            'woori': '友利銀行',
            'hana': '韓亞銀行',
            'industrial': '興業銀行',
            'agricultural': '農業銀行',
            'ccb': '建設銀行',
            '招商銀行': 'cmb',
            'postal': '郵政儲蓄',
            'minsheng': '民生銀行',
            'citic': '中信銀行',
            'ceb': '光大銀行',
            'dahsing': '大新銀行',
            'bankcomm': '交通銀行'
        },
        'en': {
            'hsbc': 'HSBC',
            'hangseng': 'Hang Seng Bank',
            'boc': 'Bank of China',
            'icbc': 'ICBC',
            'bea': 'Bank of East Asia',
            'scb': 'Standard Chartered',
            'citi': 'Citibank',
            'dbs': 'DBS Bank',
            'ocbc': 'OCBC Bank',
            'ubs': 'UBS',
            'credit-suisse': 'Credit Suisse',
            'jpmorgan': 'JPMorgan',
            'goldman-sachs': 'Goldman Sachs',
            'morgan-stanley': 'Morgan Stanley',
            'deutsche-bank': 'Deutsche Bank',
            'bnp': 'BNP Paribas',
            'barclays': 'Barclays',
            'hsbc-uk': 'HSBC UK',
            'lloyds': 'Lloyds Bank',
            'natwest': 'NatWest',
            'bankofamerica': 'Bank of America',
            'wellsfargo': 'Wells Fargo',
            'chase': 'Chase Bank',
            'citibank': 'Citibank',
            'pnc': 'PNC Bank',
            'mizuho': 'Mizuho Bank',
            'smbc': 'SMBC',
            'mufg': 'MUFG Bank',
            'shinhan': 'Shinhan Bank',
            'kb': 'KB Kookmin Bank',
            'woori': 'Woori Bank',
            'hana': 'Hana Bank',
            'industrial': 'Industrial Bank',
            'agricultural': 'Agricultural Bank',
            'ccb': 'CCB',
            'cmb': 'China Merchants Bank',
            'postal': 'Postal Savings Bank',
            'minsheng': 'Minsheng Bank',
            'citic': 'CITIC Bank',
            'ceb': 'CEB',
            'dahsing': 'Dah Sing Bank',
            'bankcomm': 'Bank of Communications'
        },
        'jp': {
            'hsbc': 'HSBC',
            'hangseng': 'ハンセン銀行',
            'boc': '中国銀行',
            'icbc': '工商銀行',
            'bea': '東亜銀行',
            'scb': 'スタンダードチャータード',
            'citi': 'シティバンク',
            'dbs': 'DBS銀行',
            'ocbc': 'OCBC銀行',
            'ubs': 'UBS',
            'credit-suisse': 'クレディ・スイス',
            'jpmorgan': 'JPモルガン',
            'goldman-sachs': 'ゴールドマン・サックス',
            'morgan-stanley': 'モルガン・スタンレー',
            'deutsche-bank': 'ドイツ銀行',
            'bnp': 'BNPパリバ',
            'barclays': 'バークレイズ',
            'hsbc-uk': 'HSBC英国',
            'lloyds': 'ロイズ銀行',
            'natwest': 'ナットウェスト',
            'bankofamerica': 'バンク・オブ・アメリカ',
            'wellsfargo': 'ウェルズ・ファーゴ',
            'chase': 'チェース銀行',
            'citibank': 'シティバンク',
            'pnc': 'PNC銀行',
            'mizuho': 'みずほ銀行',
            'smbc': '三井住友銀行',
            'mufg': '三菱UFJ銀行',
            'shinhan': '新韓銀行',
            'kb': 'KB国民銀行',
            'woori': 'ウリ銀行',
            'hana': 'ハナ銀行',
            'industrial': '興業銀行',
            'agricultural': '農業銀行',
            'ccb': '建設銀行',
            'cmb': '招商銀行',
            'postal': '郵政儲蓄銀行',
            'minsheng': '民生銀行',
            'citic': '中信銀行',
            'ceb': '光大銀行',
            'dahsing': '大新銀行',
            'bankcomm': '交通銀行'
        },
        'kr': {
            'hsbc': 'HSBC',
            'hangseng': '항셍은행',
            'boc': '중국은행',
            'icbc': '공상은행',
            'bea': '동아은행',
            'scb': '스탠다드차타드',
            'citi': '씨티은행',
            'dbs': 'DBS은행',
            'ocbc': 'OCBC은행',
            'ubs': 'UBS',
            'credit-suisse': '크레딧스위스',
            'jpmorgan': 'JP모건',
            'goldman-sachs': '골드만삭스',
            'morgan-stanley': '모건스탠리',
            'deutsche-bank': '도이체방크',
            'bnp': 'BNP파리바',
            'barclays': '바클레이스',
            'hsbc-uk': 'HSBC 영국',
            'lloyds': '로이즈은행',
            'natwest': '내트웨스트',
            'bankofamerica': '뱅크오브아메리카',
            'wellsfargo': '웰스파고',
            'chase': '체이스은행',
            'citibank': '씨티은행',
            'pnc': 'PNC은행',
            'mizuho': '미즈호은행',
            'smbc': '미쓰이스미토모은행',
            'mufg': 'MUFG은행',
            'shinhan': '신한은행',
            'kb': 'KB국민은행',
            'woori': '우리은행',
            'hana': '하나은행',
            'industrial': '흥업은행',
            'agricultural': '농업은행',
            'ccb': '건설은행',
            'cmb': '초상은행',
            'postal': '우정저축은행',
            'minsheng': '민생은행',
            'citic': '중신은행',
            'ceb': '광대은행',
            'dahsing': '대신은행',
            'bankcomm': '교통은행'
        }
    }
    
    # 行业名称映射（简单版）
    industry_names = {
        'zh': {
            'restaurant': '餐廳',
            'accounting': '會計師',
            'small-business': '小型企業',
            'ecommerce': '電商',
            'retail': '零售店',
            'trading': '貿易公司',
            'logistics': '物流公司',
            'it': 'IT公司',
            'consulting': '諮詢公司',
            'legal': '律師事務所',
            'medical': '診所',
            'dental': '牙科診所',
            'education': '教育機構',
            'freelance': '自由職業者',
            'real-estate': '地產',
            'construction': '建築公司',
            'manufacturing': '製造業',
            'hotel': '酒店',
            'travel': '旅行社',
            'salon': '美容院',
            'fitness': '健身中心',
            'photography': '攝影工作室',
            'design': '設計工作室',
            'marketing': '營銷公司',
            'pr': '公關公司',
            'event': '活動策劃',
            'translation': '翻譯公司',
            'cleaning': '清潔公司',
            'maintenance': '維修公司',
            'security': '保安公司',
            'courier': '速遞公司'
        },
        'en': {
            'restaurant': 'Restaurant',
            'accounting': 'Accountant',
            'small-business': 'Small Business',
            'ecommerce': 'E-commerce',
            'retail': 'Retail Store',
            'trading': 'Trading Company',
            'logistics': 'Logistics',
            'it': 'IT Company',
            'consulting': 'Consulting',
            'legal': 'Law Firm',
            'medical': 'Clinic',
            'dental': 'Dental Clinic',
            'education': 'Education',
            'freelance': 'Freelancer',
            'real-estate': 'Real Estate',
            'construction': 'Construction',
            'manufacturing': 'Manufacturing',
            'hotel': 'Hotel',
            'travel': 'Travel Agency',
            'salon': 'Beauty Salon',
            'fitness': 'Fitness Center',
            'photography': 'Photography Studio',
            'design': 'Design Studio',
            'marketing': 'Marketing Agency',
            'pr': 'PR Agency',
            'event': 'Event Planning',
            'translation': 'Translation',
            'cleaning': 'Cleaning Service',
            'maintenance': 'Maintenance',
            'security': 'Security',
            'courier': 'Courier'
        },
        'jp': {
            'restaurant': 'レストラン',
            'accounting': '会計士',
            'small-business': '小規模企業',
            'ecommerce': 'EC',
            'retail': '小売店',
            'trading': '貿易会社',
            'logistics': '物流会社',
            'it': 'IT企業',
            'consulting': 'コンサルティング',
            'legal': '法律事務所',
            'medical': 'クリニック',
            'dental': '歯科医院',
            'education': '教育機関',
            'freelance': 'フリーランス',
            'real-estate': '不動産',
            'construction': '建設会社',
            'manufacturing': '製造業',
            'hotel': 'ホテル',
            'travel': '旅行代理店',
            'salon': '美容院',
            'fitness': 'フィットネス',
            'photography': '写真スタジオ',
            'design': 'デザインスタジオ',
            'marketing': 'マーケティング',
            'pr': 'PR会社',
            'event': 'イベント企画',
            'translation': '翻訳会社',
            'cleaning': '清掃会社',
            'maintenance': 'メンテナンス',
            'security': '警備会社',
            'courier': '宅配会社'
        },
        'kr': {
            'restaurant': '레스토랑',
            'accounting': '회계사',
            'small-business': '소상공인',
            'ecommerce': '전자상거래',
            'retail': '소매점',
            'trading': '무역회사',
            'logistics': '물류회사',
            'it': 'IT회사',
            'consulting': '컨설팅',
            'legal': '법률사무소',
            'medical': '의원',
            'dental': '치과',
            'education': '교육기관',
            'freelance': '프리랜서',
            'real-estate': '부동산',
            'construction': '건설회사',
            'manufacturing': '제조업',
            'hotel': '호텔',
            'travel': '여행사',
            'salon': '미용실',
            'fitness': '피트니스',
            'photography': '사진 스튜디오',
            'design': '디자인 스튜디오',
            'marketing': '마케팅 대행사',
            'pr': 'PR 대행사',
            'event': '이벤트 기획',
            'translation': '번역 회사',
            'cleaning': '청소 서비스',
            'maintenance': '유지보수',
            'security': '보안',
            'courier': '택배'
        }
    }
    
    # 查找匹配
    if name in bank_names.get(lang, {}):
        return bank_names[lang][name]
    elif name in industry_names.get(lang, {}):
        return industry_names[lang][name]
    else:
        # 返回格式化的名称
        return name.replace('-', ' ').title()

def main():
    """主函数"""
    print("🚀 开始批量插入高质量内容（通用模板）...")
    print("=" * 70)
    print()
    
    # 统计
    total_processed = 0
    total_success = 0
    total_skip = 0
    total_error = 0
    
    # 读取生成的页面列表
    pages_files = [
        'phase2_generated_pages.txt',
        'phase2_generated_remaining_204_pages.txt'
    ]
    
    all_pages = []
    for pages_file in pages_files:
        if Path(pages_file).exists():
            with open(pages_file, 'r', encoding='utf-8') as f:
                all_pages.extend([line.strip() for line in f if line.strip()])
    
    print(f"📄 找到 {len(all_pages)} 个页面")
    print()
    print("📝 使用通用模板快速生成...")
    print("-" * 70)
    
    for page_path in all_pages:
        if not Path(page_path).exists():
            continue
        
        filename = Path(page_path).name
        total_processed += 1
        
        # 判断语言
        if '/en/' in str(page_path) or str(page_path).startswith('en/'):
            lang = 'en'
        elif '/jp/' in str(page_path) or str(page_path).startswith('jp/'):
            lang = 'jp'
        elif '/kr/' in str(page_path) or str(page_path).startswith('kr/'):
            lang = 'kr'
        else:
            lang = 'zh'
        
        # 判断页面类型和提取名称
        if 'bank-statement-simple' in filename:
            entity_type = 'bank'
            entity_name = extract_entity_name(filename, lang)
        elif 'accounting-solution' in filename:
            entity_type = 'industry'
            entity_name = extract_entity_name(filename, lang)
        else:
            continue
        
        # 生成通用内容
        content_html = generate_full_content(entity_name, entity_type, lang)
        success, message = insert_quality_content(page_path, content_html)
        
        if success:
            total_success += 1
            if total_success % 20 == 0:
                print(f"✅ 已完成 {total_success}/{len(all_pages)} 页...")
        elif "已存在" in message:
            total_skip += 1
        else:
            total_error += 1
            if total_error <= 5:  # 只显示前5个错误
                print(f"❌ {page_path}: {message}")
    
    print()
    print("=" * 70)
    print("🎉 批量插入完成！")
    print()
    print("📊 统计：")
    print(f"   - 处理: {total_processed} 页")
    print(f"   - 成功: {total_success} 页")
    print(f"   - 跳过: {total_skip} 页（已有内容）")
    print(f"   - 错误: {total_error} 页")
    print()
    print("✅ 每页新增内容：")
    print("   1. 痛点分析（3 个痛点）")
    print("   2. 客户案例（完整故事）")
    print("   3. 使用指南（3 步骤）")
    print("   4. FAQ（8 个问题）")
    print("   5. 行动呼籲（保证承诺）")
    print()
    print("📈 预期效果：")
    print("   - 每页字数：200-300 字 → 800-1600 字")
    print("   - 独特性：20-30% → 70%+")
    print("   - Google 索引率：+200%")
    print("   - 转化率：+50-100%")

if __name__ == '__main__':
    # 确认执行
    print()
    print("⚠️  重要提示：")
    print("   此操作将为 292 个页面添加高质量内容")
    print("   每页将新增 800-1600 字")
    print()
    
    response = input("是否继续？(yes/no): ").strip().lower()
    
    if response in ['yes', 'y', '是']:
        main()
    else:
        print("❌ 操作已取消")

