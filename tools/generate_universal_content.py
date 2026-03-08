#!/usr/bin/env python3
"""
通用模板内容生成系统
为所有银行和行业快速生成高质量内容
"""

from generate_quality_content import (
    generate_usage_guide_html,
    generate_cta_html
)

def generate_universal_pain_points(entity_name, entity_type='bank', lang='zh'):
    """生成通用痛点分析"""
    
    if entity_type == 'bank':
        if lang == 'zh':
            pain_points = [
                {
                    'title': f'{entity_name}對賬單處理費時費力',
                    'description': f'{entity_name}的客戶每月需要處理大量對賬單，人工處理平均需要3-5小時。需要逐筆核對交易記錄、手動輸入 Excel、處理不同帳戶類型。特別是月底對賬時期，工作量激增，容易出錯。',
                    'solution': 'VaultCaddy 自動識別，3秒完成處理'
                },
                {
                    'title': '交易記錄複雜難以整理',
                    'description': f'{entity_name}對賬單包含多種交易類型：轉帳、支付、提款、手續費、利息等。人工分類耗時且容易遺漏，影響財務報表準確性。',
                    'solution': 'VaultCaddy 98%準確識別所有交易細節'
                },
                {
                    'title': '報稅和審計準備壓力大',
                    'description': f'每年報稅季節，需要整理全年{entity_name}對賬單。紙質或 PDF 檔案堆積如山，查找特定交易記錄困難，經常加班到深夜。',
                    'solution': 'VaultCaddy 雲端存儲，隨時搜索，一鍵導出'
                }
            ]
        elif lang == 'en':
            pain_points = [
                {
                    'title': f'{entity_name} Statement Processing is Time-Consuming',
                    'description': f'{entity_name} customers spend 3-5 hours monthly processing statements. Need to check transactions manually, input to Excel, handle different account types. Workload surges during month-end, prone to errors.',
                    'solution': 'VaultCaddy auto-identifies, completes in 3 seconds'
                },
                {
                    'title': 'Complex Transaction Records Hard to Organize',
                    'description': f'{entity_name} statements contain various transaction types: transfers, payments, withdrawals, fees, interest. Manual categorization is time-consuming and error-prone.',
                    'solution': 'VaultCaddy identifies all transaction details with 98% accuracy'
                },
                {
                    'title': 'Tax and Audit Preparation Stress',
                    'description': f'During tax season, need to organize annual {entity_name} statements. Paper or PDF files pile up, finding specific transactions is difficult, often working late nights.',
                    'solution': 'VaultCaddy cloud storage, search anytime, one-click export'
                }
            ]
        elif lang == 'jp':
            pain_points = [
                {
                    'title': f'{entity_name}の明細処理に時間がかかる',
                    'description': f'{entity_name}のお客様は毎月3-5時間かけて明細を処理しています。取引を1つずつ確認し、Excelに手入力し、異なる口座タイプを処理する必要があります。',
                    'solution': 'VaultCaddyは自動認識、3秒で完了'
                },
                {
                    'title': '複雑な取引記録の整理が困難',
                    'description': f'{entity_name}の明細には、振込、支払い、引き出し、手数料、利息など、さまざまな取引タイプが含まれています。手動分類は時間がかかり、エラーが発生しやすいです。',
                    'solution': 'VaultCaddyは98%の精度で全ての取引詳細を認識'
                },
                {
                    'title': '税務・監査準備のストレス',
                    'description': f'確定申告の時期には、年間の{entity_name}明細を整理する必要があります。紙やPDFファイルが山積みになり、特定の取引を見つけるのが困難です。',
                    'solution': 'VaultCaddyクラウド保存、いつでも検索、ワンクリック出力'
                }
            ]
        else:  # kr
            pain_points = [
                {
                    'title': f'{entity_name} 명세서 처리에 시간 소요',
                    'description': f'{entity_name} 고객은 매월 3-5시간 동안 명세서를 처리합니다. 거래를 하나씩 확인하고 Excel에 수동 입력하며 다양한 계정 유형을 처리해야 합니다.',
                    'solution': 'VaultCaddy 자동 인식, 3초 완료'
                },
                {
                    'title': '복잡한 거래 기록 정리 어려움',
                    'description': f'{entity_name} 명세서에는 이체, 결제, 인출, 수수료, 이자 등 다양한 거래 유형이 포함됩니다. 수동 분류는 시간이 걸리고 오류가 발생하기 쉽습니다.',
                    'solution': 'VaultCaddy 98% 정확도로 모든 거래 세부정보 인식'
                },
                {
                    'title': '세금 및 감사 준비 스트레스',
                    'description': f'세금 시즌에는 연간 {entity_name} 명세서를 정리해야 합니다. 종이나 PDF 파일이 쌓여 특정 거래를 찾기 어렵습니다.',
                    'solution': 'VaultCaddy 클라우드 저장, 언제든지 검색, 원클릭 내보내기'
                }
            ]
    
    else:  # industry
        if lang == 'zh':
            pain_points = [
                {
                    'title': f'{entity_name}財務管理混亂',
                    'description': f'{entity_name}每月需要處理大量收據、發票和對賬單。傳統的紙質記賬或手動 Excel 方式效率低下，容易遺失單據，月底整理時一片混亂。',
                    'solution': 'VaultCaddy 拍照上傳，3秒完成處理'
                },
                {
                    'title': '報稅準備壓力大',
                    'description': f'{entity_name}每年報稅前需要整理全年財務記錄。查找發票和收據耗時費力，經常發現遺漏，需要緊急補救。會計師也經常要求補充資料。',
                    'solution': 'VaultCaddy 雲端存儲，一鍵導出全年記錄'
                },
                {
                    'title': '缺少專業會計支援',
                    'description': f'許多{entity_name}沒有專職會計，老闆或員工兼職處理財務。缺乏專業知識，不清楚如何正確分類和記賬，擔心稅務問題。',
                    'solution': 'VaultCaddy 自動分類，符合會計標準'
                }
            ]
        elif lang == 'en':
            pain_points = [
                {
                    'title': f'{entity_name} Financial Management Chaos',
                    'description': f'{entity_name} businesses handle numerous receipts, invoices and statements monthly. Traditional paper records or manual Excel is inefficient, documents get lost, month-end is chaotic.',
                    'solution': 'VaultCaddy photo upload, 3-second processing'
                },
                {
                    'title': 'Tax Preparation Stress',
                    'description': f'{entity_name} businesses need to organize annual financial records before tax season. Finding invoices and receipts is time-consuming, often finding gaps, needing urgent fixes.',
                    'solution': 'VaultCaddy cloud storage, one-click annual export'
                },
                {
                    'title': 'Lack of Professional Accounting Support',
                    'description': f'Many {entity_name} businesses lack dedicated accountants, owners or staff handle finances part-time. Lack expertise, unsure about proper categorization, worried about tax issues.',
                    'solution': 'VaultCaddy auto-categorization, accounting-compliant'
                }
            ]
        elif lang == 'jp':
            pain_points = [
                {
                    'title': f'{entity_name}の財務管理が混乱',
                    'description': f'{entity_name}は毎月多くの領収書、請求書、明細を処理する必要があります。従来の紙の記録や手動Excelは非効率で、書類を紛失し、月末の整理が混乱します。',
                    'solution': 'VaultCaddy 写真アップロード、3秒処理'
                },
                {
                    'title': '確定申告準備のストレス',
                    'description': f'{entity_name}は確定申告前に年間の財務記録を整理する必要があります。請求書や領収書を探すのに時間がかかり、よく抜けがあり、緊急対応が必要です。',
                    'solution': 'VaultCaddyクラウド保存、ワンクリック年間出力'
                },
                {
                    'title': '専門的な会計サポートの不足',
                    'description': f'多くの{entity_name}には専任の会計士がおらず、オーナーやスタッフが財務を兼任しています。専門知識が不足し、正しい分類方法が分からず、税務問題を心配しています。',
                    'solution': 'VaultCaddy 自動分類、会計基準準拠'
                }
            ]
        else:  # kr
            pain_points = [
                {
                    'title': f'{entity_name} 재무 관리 혼란',
                    'description': f'{entity_name}는 매월 수많은 영수증, 인보이스, 명세서를 처리해야 합니다. 전통적인 종이 기록이나 수동 Excel은 비효율적이며 문서를 분실하고 월말 정리가 혼란스럽습니다.',
                    'solution': 'VaultCaddy 사진 업로드, 3초 처리'
                },
                {
                    'title': '세금 준비 스트레스',
                    'description': f'{entity_name}는 세금 시즌 전에 연간 재무 기록을 정리해야 합니다. 인보이스와 영수증을 찾는 데 시간이 걸리고 누락이 자주 발견되어 긴급 수정이 필요합니다.',
                    'solution': 'VaultCaddy 클라우드 저장, 원클릭 연간 내보내기'
                },
                {
                    'title': '전문 회계 지원 부족',
                    'description': f'많은 {entity_name}에는 전담 회계사가 없으며 소유자나 직원이 재무를 겸임합니다. 전문 지식이 부족하고 올바른 분류 방법을 모르며 세금 문제를 걱정합니다.',
                    'solution': 'VaultCaddy 자동 분류, 회계 기준 준수'
                }
            ]
    
    # 生成 HTML
    title_map = {
        'zh': f'{entity_name}的3大痛點',
        'en': f'Top 3 Pain Points for {entity_name}',
        'jp': f'{entity_name}の3つの課題',
        'kr': f'{entity_name} 3가지 주요 문제점'
    }
    
    html = f'''
    <section class="pain-points-section" style="padding: 60px 20px; background: #f9fafb;">
        <div class="container" style="max-width: 1200px; margin: 0 auto;">
            <h2 style="font-size: 32px; font-weight: 700; margin-bottom: 40px; text-align: center; color: #1a1a1a;">
                {title_map[lang]}
            </h2>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 32px;">
'''
    
    for i, point in enumerate(pain_points, 1):
        html += f'''
                <div style="background: white; padding: 32px; border-radius: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.08);">
                    <div style="display: flex; align-items: center; gap: 16px; margin-bottom: 16px;">
                        <span style="font-size: 36px; font-weight: 700; color: #667eea;">❌</span>
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

def generate_universal_case_study(entity_name, entity_type='bank', lang='zh'):
    """生成通用客户案例"""
    
    if entity_type == 'bank':
        if lang == 'zh':
            case_study = {
                'name': '王先生',
                'business': f'使用{entity_name}的貿易公司',
                'team_size': '5-10人團隊',
                'before_time': '每月 6-8 小時',
                'after_time': '30 分鐘',
                'before_cost': 'HK$2,500/月',
                'after_cost': 'HK$46/月',
                'accuracy_before': '88%',
                'accuracy_after': '98%',
                'testimonial': f'以前每月處理{entity_name}對賬單都很頭痛，現在用 VaultCaddy 只需要拍照上傳，3秒就搞定。省下的時間可以專注業務發展！',
                'roi': '5,000%+'
            }
        elif lang == 'en':
            case_study = {
                'name': 'Mr. Wang',
                'business': f'Trading Company using {entity_name}',
                'team_size': '5-10 person team',
                'before_time': '6-8 hours/month',
                'after_time': '30 minutes',
                'before_cost': '$330/month',
                'after_cost': '$6/month',
                'accuracy_before': '88%',
                'accuracy_after': '98%',
                'testimonial': f'Used to have headaches processing {entity_name} statements monthly. Now with VaultCaddy, just photo upload and done in 3 seconds. Time saved for business growth!',
                'roi': '5,000%+'
            }
        elif lang == 'jp':
            case_study = {
                'name': '王さん',
                'business': f'{entity_name}を使用する貿易会社',
                'team_size': '5-10人チーム',
                'before_time': '毎月6-8時間',
                'after_time': '30分',
                'before_cost': '¥45,000/月',
                'after_cost': '¥660/月',
                'accuracy_before': '88%',
                'accuracy_after': '98%',
                'testimonial': f'以前は毎月{entity_name}の明細処理に頭を悩ませていましたが、今はVaultCaddyで写真を撮ってアップロードするだけ、3秒で完了！節約した時間をビジネス成長に使えます！',
                'roi': '5,000%+'
            }
        else:  # kr
            case_study = {
                'name': '왕 씨',
                'business': f'{entity_name}를 사용하는 무역 회사',
                'team_size': '5-10명 팀',
                'before_time': '매월 6-8시간',
                'after_time': '30분',
                'before_cost': '₩300,000/월',
                'after_cost': '₩9,900/월',
                'accuracy_before': '88%',
                'accuracy_after': '98%',
                'testimonial': f'매월 {entity_name} 명세서 처리에 골치를 앓았는데, 이제 VaultCaddy로 사진만 찍어 업로드하면 3초 완료! 절약한 시간을 비즈니스 성장에 사용합니다!',
                'roi': '5,000%+'
            }
    
    else:  # industry
        if lang == 'zh':
            case_study = {
                'name': '李小姐',
                'business': entity_name,
                'team_size': '3-5人',
                'before_time': '每月 10-15 小時',
                'after_time': '1-2 小時',
                'before_cost': '人工成本 HK$4,000/月',
                'after_cost': 'HK$46/月',
                'accuracy_before': '85%',
                'accuracy_after': '98%',
                'testimonial': f'作為{entity_name}，我最怕月底整理賬目。現在用 VaultCaddy，每天拍照上傳，月底一鍵導出，超級輕鬆！',
                'roi': '8,000%+'
            }
        elif lang == 'en':
            case_study = {
                'name': 'Ms. Li',
                'business': entity_name,
                'team_size': '3-5 people',
                'before_time': '10-15 hours/month',
                'after_time': '1-2 hours',
                'before_cost': '$530/month',
                'after_cost': '$6/month',
                'accuracy_before': '85%',
                'accuracy_after': '98%',
                'testimonial': f'As a {entity_name} owner, I used to dread month-end accounting. Now with VaultCaddy, daily photo uploads and month-end one-click export. Super easy!',
                'roi': '8,000%+'
            }
        elif lang == 'jp':
            case_study = {
                'name': '李さん',
                'business': entity_name,
                'team_size': '3-5人',
                'before_time': '毎月10-15時間',
                'after_time': '1-2時間',
                'before_cost': '¥72,000/月',
                'after_cost': '¥660/月',
                'accuracy_before': '85%',
                'accuracy_after': '98%',
                'testimonial': f'{entity_name}として、月末の経理整理が一番怖かったです。今はVaultCaddyで毎日写真をアップロードし、月末にワンクリック出力。超簡単！',
                'roi': '8,000%+'
            }
        else:  # kr
            case_study = {
                'name': '이 씨',
                'business': entity_name,
                'team_size': '3-5명',
                'before_time': '매월 10-15시간',
                'after_time': '1-2시간',
                'before_cost': '₩480,000/월',
                'after_cost': '₩9,900/월',
                'accuracy_before': '85%',
                'accuracy_after': '98%',
                'testimonial': f'{entity_name}로서 월말 회계 정리가 가장 두려웠습니다. 이제 VaultCaddy로 매일 사진을 업로드하고 월말에 원클릭 내보내기. 정말 쉽습니다!',
                'roi': '8,000%+'
            }
    
    # 生成 HTML（使用之前的 generate_case_study_html 函数）
    from generate_quality_content import generate_case_study_html
    return generate_case_study_html(case_study, lang)

def generate_universal_faq(entity_name, entity_type='bank', lang='zh'):
    """生成通用 FAQ"""
    
    if lang == 'zh':
        faqs = [
            {'q': f'VaultCaddy 支持{entity_name}的對賬單嗎？', 'a': f'完全支持！我們的 AI 已經訓練了數千份{entity_name}對賬單，可以自動識別所有交易類型和格式。準確率達到 98%。'},
            {'q': '處理一份對賬單需要多久？', 'a': '通常3-5秒。簡單對賬單（1-10頁）約3秒，複雜對賬單（20+頁或100+筆交易）約5-8秒。'},
            {'q': '如果識別錯誤怎麼辦？', 'a': '您可以在線直接修改（2秒），系統會學習您的修改，下次更準確。我們的準確率已達 98%，錯誤極少。'},
            {'q': '數據安全嗎？', 'a': '絕對安全！我們使用銀行級 256-bit 加密，符合香港個人資料私隱條例，定期進行安全審計。只有您可以訪問自己的數據。'},
            {'q': '可以批量處理嗎？', 'a': '可以！一次最多上傳50個文件，系統自動按月份分類，一鍵導出全年數據。非常適合報稅準備。'},
            {'q': '支持哪些格式？', 'a': '支持 PDF、JPG/PNG（照片）、部分銀行的 Excel 格式。推薦使用 PDF 或清晰照片以獲得最佳識別效果。'},
            {'q': '與會計師如何協作？', 'a': '可以導出 Excel 發送給會計師，或免費邀請會計師加入項目，他們可以直接查看和下載所有資料。'},
            {'q': '免費試用有什麼限制？', 'a': '20頁免費試用，所有功能完全開放，無需信用卡，3秒註冊即可開始。試用無任何限制。'}
        ]
    elif lang == 'en':
        faqs = [
            {'q': f'Does VaultCaddy support {entity_name} statements?', 'a': f'Fully supported! Our AI has been trained on thousands of {entity_name} statements, automatically recognizing all transaction types and formats. 98% accuracy.'},
            {'q': 'How long does it take to process one statement?', 'a': 'Usually 3-5 seconds. Simple statements (1-10 pages) about 3 seconds, complex statements (20+ pages or 100+ transactions) about 5-8 seconds.'},
            {'q': 'What if there are recognition errors?', 'a': 'You can edit directly online (2 seconds), system learns from your corrections for better accuracy next time. Our accuracy is 98%, errors are rare.'},
            {'q': 'Is my data secure?', 'a': 'Absolutely! We use bank-level 256-bit encryption, compliant with HK privacy regulations, regular security audits. Only you can access your data.'},
            {'q': 'Can I batch process?', 'a': 'Yes! Upload up to 50 files at once, system auto-categorizes by month, one-click export annual data. Perfect for tax preparation.'},
            {'q': 'What formats are supported?', 'a': 'PDF, JPG/PNG (photos), Excel format from some banks. Recommend PDF or clear photos for best recognition.'},
            {'q': 'How to collaborate with accountants?', 'a': 'Export Excel to send to accountant, or invite accountant to join project for free, they can view and download all materials directly.'},
            {'q': 'Any limits on free trial?', 'a': '20 pages free trial, all features fully accessible, no credit card required, 3-second signup to start. No limitations during trial.'}
        ]
    elif lang == 'jp':
        faqs = [
            {'q': f'VaultCaddyは{entity_name}の明細に対応していますか？', 'a': f'完全対応！私たちのAIは数千枚の{entity_name}明細で訓練されており、すべての取引タイプとフォーマットを自動認識します。98%の精度です。'},
            {'q': '1枚の明細処理にどのくらい時間がかかりますか？', 'a': '通常3-5秒です。シンプルな明細（1-10ページ）は約3秒、複雑な明細（20+ページまたは100+取引）は約5-8秒です。'},
            {'q': '認識エラーがあった場合は？', 'a': 'オンラインで直接編集できます（2秒）。システムは修正から学習し、次回はより正確になります。精度は98%で、エラーはまれです。'},
            {'q': 'データは安全ですか？', 'a': '絶対に安全です！銀行レベルの256ビット暗号化を使用し、香港のプライバシー規制に準拠し、定期的なセキュリティ監査を実施しています。'},
            {'q': 'バッチ処理は可能ですか？', 'a': 'はい！一度に最大50ファイルをアップロードでき、システムが自動的に月別に分類し、ワンクリックで年間データを出力します。'},
            {'q': 'どの形式をサポートしていますか？', 'a': 'PDF、JPG/PNG（写真）、一部の銀行のExcel形式をサポートしています。最良の認識のためにPDFまたは鮮明な写真を推奨します。'},
            {'q': '会計士とどのように協力しますか？', 'a': 'Excelをエクスポートして会計士に送信するか、会計士を無料でプロジェクトに招待し、すべての資料を直接表示およびダウンロードできます。'},
            {'q': '無料トライアルに制限はありますか？', 'a': '20ページの無料トライアル、すべての機能にフルアクセス、クレジットカード不要、3秒でサインアップして開始できます。'}
        ]
    else:  # kr
        faqs = [
            {'q': f'VaultCaddy는 {entity_name} 명세서를 지원합니까?', 'a': f'완전 지원합니다! 우리 AI는 수천 개의 {entity_name} 명세서로 학습되어 모든 거래 유형과 형식을 자동으로 인식합니다. 98% 정확도입니다.'},
            {'q': '명세서 하나를 처리하는 데 얼마나 걸립니까?', 'a': '보통 3-5초입니다. 간단한 명세서(1-10페이지)는 약 3초, 복잡한 명세서(20+페이지 또는 100+거래)는 약 5-8초입니다.'},
            {'q': '인식 오류가 있으면 어떻게 합니까?', 'a': '온라인에서 직접 편집할 수 있습니다(2초). 시스템은 수정 사항을 학습하여 다음번에 더 정확해집니다. 정확도는 98%이며 오류는 드뭅니다.'},
            {'q': '데이터는 안전합니까?', 'a': '절대 안전합니다! 은행급 256비트 암호화를 사용하고 홍콩 개인정보 보호 규정을 준수하며 정기적인 보안 감사를 수행합니다.'},
            {'q': '일괄 처리가 가능합니까?', 'a': '예! 한 번에 최대 50개 파일을 업로드할 수 있으며 시스템이 자동으로 월별로 분류하고 원클릭으로 연간 데이터를 내보냅니다.'},
            {'q': '어떤 형식을 지원합니까?', 'a': 'PDF, JPG/PNG(사진), 일부 은행의 Excel 형식을 지원합니다. 최상의 인식을 위해 PDF 또는 선명한 사진을 권장합니다.'},
            {'q': '회계사와 어떻게 협력합니까?', 'a': 'Excel을 내보내 회계사에게 보내거나 회계사를 프로젝트에 무료로 초대하여 모든 자료를 직접 보고 다운로드할 수 있습니다.'},
            {'q': '무료 체험에 제한이 있습니까?', 'a': '20페이지 무료 체험, 모든 기능에 완전히 액세스, 신용카드 불필요, 3초 가입으로 시작할 수 있습니다.'}
        ]
    
    # 生成 HTML（使用之前的 generate_faq_html 函数）
    from generate_quality_content import generate_faq_html
    return generate_faq_html(faqs, lang)

def generate_full_content(entity_name, entity_type='bank', lang='zh'):
    """生成完整的页面内容"""
    pain_points_html = generate_universal_pain_points(entity_name, entity_type, lang)
    case_study_html = generate_universal_case_study(entity_name, entity_type, lang)
    usage_guide_html = generate_usage_guide_html(lang)
    faq_html = generate_universal_faq(entity_name, entity_type, lang)
    cta_html = generate_cta_html(lang)
    
    return (
        pain_points_html +
        case_study_html +
        usage_guide_html +
        faq_html +
        cta_html
    )

if __name__ == '__main__':
    # 测试生成内容
    print("生成测试内容...")
    content = generate_full_content("測試銀行", "bank", "zh")
    
    # 统计字数
    import re
    text_content = re.sub(r'<[^>]+>', '', content)
    word_count = len(text_content.replace(' ', '').replace('\n', ''))
    
    print(f"✅ 生成完成！字数：{word_count} 字")

