#!/usr/bin/env python3
"""
批量优化所有页面的 Meta 标签文案

作用：
1. 将平淡的标题改为高转化率文案
2. 优化 description 提升点击率
3. 添加情感触发词和数字证明
4. 保持 SEO 最佳实践

使用方法：
    python3 batch_update_meta_copywriting.py
"""

import re
from pathlib import Path
import shutil
from datetime import datetime

# 配置
BASE_DIR = Path(__file__).parent
BACKUP_DIR = BASE_DIR / f"backup_meta_tags_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
BACKUP_DIR.mkdir(exist_ok=True)

# 高转化率文案模板
COPYWRITING_TEMPLATES = {
    # 首页
    'index.html': {
        'zh': {
            'title': '对账单+收据+发票AI识别转Excel｜3秒完成｜月费$46起｜比Dext便宜70% - VaultCaddy',
            'description': '告别手工录入！VaultCaddy AI自动处理银行对账单、收据、发票，3秒转成Excel。准确率98%，比人工便宜95%，比Dext便宜70%。支持汇丰、恒生等所有香港银行，支持餐饮、零售、交通等各类商户收据。月费$46起，免费试用20页。'
        },
        'en': {
            'title': 'Bank Statements+Receipts+Invoices AI OCR to Excel | 3 Seconds | From $46/month - VaultCaddy',
            'description': 'Stop manual data entry! VaultCaddy AI processes bank statements, receipts, and invoices to Excel in 3 seconds. 98% accuracy, 95% cheaper than manual, 70% cheaper than Dext. Supports all HK banks and merchant receipts. From $46/month, 20 pages free trial.'
        },
        'ja': {
            'title': '銀行明細書+領収書+請求書AI認識→Excel｜3秒完了｜月額$46〜｜Dextより70%安い',
            'description': '手作業入力にさようなら！VaultCaddy AIで銀行明細書、領収書、請求書を3秒でExcel変換。正確率98%、手作業より95%安く、Dextより70%安い。香港の全銀行と店舗レシート対応。月額$46〜、20ページ無料。'
        },
        'ko': {
            'title': '은행 명세서+영수증+청구서 AI 인식→Excel｜3초 완료｜월$46부터｜Dext보다 70% 저렴',
            'description': '수동 입력 안녕！VaultCaddy AI로 은행 명세서, 영수증, 청구서를 3초 만에 Excel로 변환. 정확도 98%, 수동보다 95% 저렴, Dext보다 70% 저렴. 홍콩 모든 은행과 상점 영수증 지원. 월$46부터, 20페이지 무료.'
        }
    },
    
    # AI vs 人工对比页
    'ai-vs-manual-comparison.html': {
        'zh': {
            'title': 'VaultCaddy vs 人工 vs Dext vs AutoEntry｜对账单+收据+发票AI处理完整对比 2025｜年省35,000港币',
            'description': '人工处理对账单、收据、发票每月花30小时？年费3万港币？VaultCaddy AI 3秒搞定全部文档，年费仅$552，比人工便宜95%，比Dext便宜70%，比AutoEntry便宜85%。支持所有香港银行和商户。查看完整对比表→'
        },
        'en': {
            'title': 'VaultCaddy vs Manual vs Dext vs AutoEntry | Statements+Receipts+Invoices AI Comparison 2025',
            'description': 'Manual processing takes 30 hours/month? HK$30,000/year? VaultCaddy AI does all documents in 3 seconds, only $552/year, 95% cheaper than manual, 70% cheaper than Dext. Full comparison→'
        },
        'ja': {
            'title': 'VaultCaddy vs 手作業 vs Dext vs AutoEntry｜明細書+領収書+請求書AI処理完全比較 2025',
            'description': '手作業で明細書、領収書、請求書の処理に月30時間？年間3万香港ドル？VaultCaddy AIなら全文書を3秒で処理、年間552ドル、手作業より95%安く、Dextより70%安い。'
        },
        'ko': {
            'title': 'VaultCaddy vs 수동 vs Dext vs AutoEntry｜명세서+영수증+청구서 AI 처리 완전 비교 2025',
            'description': '수동 처리로 명세서, 영수증, 청구서 처리에 월 30시간? 연간 3만 홍콩달러? VaultCaddy AI는 모든 문서를 3초에 처리, 연간 $552, 수동보다 95% 저렴, Dext보다 70% 저렴.'
        }
    },
    
    # vs Dext
    'vaultcaddy-vs-dext.html': {
        'zh': {
            'title': 'VaultCaddy vs Dext（原Receipt Bank）对比｜年费便宜70%｜对账单+收据+发票｜月费$46 vs $273',
            'description': 'Dext（原Receipt Bank）太贵？年费$3,276？VaultCaddy提供相同功能，年费仅$552，便宜70%！处理银行对账单、商户收据、供应商发票全覆盖，更适合香港银行和商户格式。1,000+企业从Dext转到VaultCaddy→'
        },
        'en': {
            'title': 'VaultCaddy vs Dext Comparison | 70% Cheaper | Statements+Receipts+Invoices | $46/mo vs $273/mo',
            'description': 'Dext (ex-Receipt Bank) too expensive? $3,276/year? VaultCaddy $552/year, 70% cheaper! Process bank statements, receipts, invoices. Better for Hong Kong formats. 1,000+ businesses switched→'
        },
        'ja': {
            'title': 'VaultCaddy vs Dext 比較｜年間70%安い｜明細書+領収書+請求書｜月額$46 vs $273',
            'description': 'Dext（旧Receipt Bank）は高すぎる？年間3,276ドル？VaultCaddyは年間552ドル、70%安い！銀行明細書、店舗領収書、仕入先請求書すべて処理。香港の銀行・店舗形式に最適→'
        },
        'ko': {
            'title': 'VaultCaddy vs Dext 비교｜연간 70% 저렴｜명세서+영수증+청구서｜월$46 vs $273',
            'description': 'Dext (구 Receipt Bank) 너무 비싸요? 연간 $3,276? VaultCaddy는 연간 $552, 70% 저렴! 은행 명세서, 상점 영수증, 공급업체 청구서 모두 처리. 홍콩 형식에 최적→'
        }
    },
    
    # vs AutoEntry
    'vaultcaddy-vs-autoentry.html': {
        'zh': {
            'title': 'VaultCaddy vs AutoEntry 对比｜年费便宜85%｜对账单+收据+发票｜月费$46 vs $325',
            'description': 'AutoEntry太贵？年费$3,900？VaultCaddy提供相同功能，年费仅$552，便宜85%！处理银行对账单、商户收据、供应商发票，更适合香港银行格式，全中文界面，24/7中文客服。1,000+香港企业使用→'
        },
        'en': {
            'title': 'VaultCaddy vs AutoEntry | 85% Cheaper | Statements+Receipts+Invoices | $46/mo vs $325/mo',
            'description': 'AutoEntry too expensive? $3,900/year? VaultCaddy $552/year, 85% cheaper! Process bank statements, receipts, invoices. Chinese interface, 24/7 Chinese support. 1,000+ HK businesses→'
        },
        'ja': {
            'title': 'VaultCaddy vs AutoEntry｜年間85%安い｜明細書+領収書+請求書｜月額$46 vs $325',
            'description': 'AutoEntryは高すぎる？年間3,900ドル？VaultCaddyは年間552ドル、85%安い！銀行明細書、店舗領収書、仕入先請求書を処理。中国語インターフェース、24時間サポート→'
        },
        'ko': {
            'title': 'VaultCaddy vs AutoEntry｜연간 85% 저렴｜명세서+영수증+청구서｜월$46 vs $325',
            'description': 'AutoEntry 너무 비싸요? 연간 $3,900? VaultCaddy는 연간 $552, 85% 저렴! 은행 명세서, 상점 영수증, 공급업체 청구서 처리. 중국어 인터페이스, 24시간 지원→'
        }
    },
    
    # vs Receipt Bank
    'vaultcaddy-vs-receiptbank.html': {
        'zh': {
            'title': 'VaultCaddy vs Receipt Bank（现Dext）｜年费便宜70%｜对账单+收据+发票｜月费$46 vs $273',
            'description': 'Receipt Bank（现已更名Dext）太贵？年费$3,276？VaultCaddy年费仅$552，便宜70%！处理银行对账单、商户收据、供应商发票全覆盖，更适合香港银行和商户格式。1,000+企业从Receipt Bank转到VaultCaddy→'
        },
        'en': {
            'title': 'VaultCaddy vs Receipt Bank (now Dext) | 70% Cheaper | Statements+Receipts+Invoices | $46/mo',
            'description': 'Receipt Bank (rebranded as Dext) too expensive? $3,276/year? VaultCaddy $552/year, 70% cheaper! Process bank statements, receipts, invoices. Better for HK formats→'
        },
        'ja': {
            'title': 'VaultCaddy vs Receipt Bank（現Dext）｜年間70%安い｜明細書+領収書+請求書｜月額$46',
            'description': 'Receipt Bank（Dextに改名）は高すぎる？年間3,276ドル？VaultCaddyは年間552ドル、70%安い！銀行明細書、店舗領収書、仕入先請求書すべて処理。香港形式に最適→'
        },
        'ko': {
            'title': 'VaultCaddy vs Receipt Bank (현 Dext)｜연간 70% 저렴｜명세서+영수증+청구서｜월$46',
            'description': 'Receipt Bank (Dext로 개명) 너무 비싸요? 연간 $3,276? VaultCaddy는 연간 $552, 70% 저렴! 은행 명세서, 상점 영수증, 공급업체 청구서 모두 처리. 홍콩 형식에 최적→'
        }
    },
    
    # HSBC
    'hsbc-bank-statement.html': {
        'zh': {
            'title': '汇丰银行对账单+收据+发票转Excel｜3秒处理｜支持HSBC网银PDF｜月费$46起',
            'description': '汇丰银行（HSBC）对账单、收据、发票手工录入太慢？VaultCaddy AI自动识别汇丰网银PDF和商户收据，3秒转成Excel/CSV，准确率98%。支持企业账户、个人账户、信用卡账单、商户收据。月费$46起，免费试用20页→'
        },
        'en': {
            'title': 'HSBC Bank Statements+Receipts+Invoices to Excel | 3 Seconds | From $46/month',
            'description': 'Manual entry of HSBC statements, receipts, invoices too slow? VaultCaddy AI processes HSBC PDFs and merchant receipts to Excel/CSV in 3 seconds, 98% accuracy. From $46/month, free 20-page trial→'
        }
    },
    
    # 恒生
    'hangseng-bank-statement.html': {
        'zh': {
            'title': '恒生银行对账单+收据+发票转Excel｜3秒处理｜支持Hang Seng网银PDF｜月费$46起',
            'description': '恒生银行对账单、收据、发票手工录入太慢？VaultCaddy AI自动识别恒生网银PDF和商户收据，3秒转成Excel/CSV，准确率98%。支持企业账户、个人账户、商户收据。月费$46起，免费试用20页→'
        },
        'en': {
            'title': 'Hang Seng Bank Statements+Receipts+Invoices to Excel | 3 Seconds | From $46/month',
            'description': 'Manual entry of Hang Seng statements, receipts, invoices too slow? VaultCaddy AI processes Hang Seng PDFs and merchant receipts to Excel/CSV in 3 seconds, 98% accuracy. From $46/month→'
        }
    },
    
    # 中银
    'bochk-bank-statement.html': {
        'zh': {
            'title': '中国银行（香港）对账单+收据+发票转Excel｜3秒处理｜支持BOCHK网银PDF｜月费$46起',
            'description': '中国银行（香港）对账单、收据、发票手工录入太慢？VaultCaddy AI自动识别中银网银PDF和商户收据，3秒转成Excel/CSV，准确率98%。月费$46起，免费试用20页→'
        }
    },
    
    # 花旗
    'citibank-bank-statement.html': {
        'zh': {
            'title': '花旗银行对账单+收据+发票转Excel｜3秒处理｜支持Citibank网银PDF｜月费$46起',
            'description': '花旗银行对账单、收据、发票手工录入太慢？VaultCaddy AI自动识别花旗网银PDF和商户收据，3秒转成Excel/CSV，准确率98%。月费$46起，免费试用20页→'
        }
    },
    
    # 渣打
    'sc-bank-statement.html': {
        'zh': {
            'title': '渣打银行对账单+收据+发票转Excel｜3秒处理｜支持Standard Chartered网银PDF｜月费$46起',
            'description': '渣打银行对账单、收据、发票手工录入太慢？VaultCaddy AI自动识别渣打网银PDF和商户收据，3秒转成Excel/CSV，准确率98%。月费$46起，免费试用20页→'
        }
    },
    
    # 星展
    'dbs-bank-statement.html': {
        'zh': {
            'title': '星展银行对账单+收据+发票转Excel｜3秒处理｜支持DBS网银PDF｜月费$46起',
            'description': '星展银行对账单、收据、发票手工录入太慢？VaultCaddy AI自动识别星展网银PDF和商户收据，3秒转成Excel/CSV，准确率98%。月费$46起，免费试用20页→'
        }
    },
    
    # 东亚
    'bea-bank-statement.html': {
        'zh': {
            'title': '东亚银行对账单+收据+发票转Excel｜3秒处理｜支持BEA网银PDF｜月费$46起',
            'description': '东亚银行对账单、收据、发票手工录入太慢？VaultCaddy AI自动识别东亚网银PDF和商户收据，3秒转成Excel/CSV，准确率98%。月费$46起，免费试用20页→'
        }
    },
    
    # 大新
    'dahsing-bank-statement.html': {
        'zh': {
            'title': '大新银行对账单+收据+发票转Excel｜3秒处理｜支持Dah Sing网银PDF｜月费$46起',
            'description': '大新银行对账单、收据、发票手工录入太慢？VaultCaddy AI自动识别大新网银PDF和商户收据，3秒转成Excel/CSV，准确率98%。月费$46起，免费试用20页→'
        }
    },
    
    # 中信
    'citic-bank-statement.html': {
        'zh': {
            'title': '中信银行对账单+收据+发票转Excel｜3秒处理｜支持CITIC网银PDF｜月费$46起',
            'description': '中信银行对账单、收据、发票手工录入太慢？VaultCaddy AI自动识别中信网银PDF和商户收据，3秒转成Excel/CSV，准确率98%。月费$46起，免费试用20页→'
        }
    },
    
    # 交通银行
    'bankcomm-bank-statement.html': {
        'zh': {
            'title': '交通银行对账单+收据+发票转Excel｜3秒处理｜支持BankComm网银PDF｜月费$46起',
            'description': '交通银行对账单、收据、发票手工录入太慢？VaultCaddy AI自动识别交通银行网银PDF和商户收据，3秒转成Excel/CSV，准确率98%。月费$46起，免费试用20页→'
        }
    },
}


def detect_language(file_path):
    """检测文件语言"""
    path_str = str(file_path)
    if '/en/' in path_str or path_str.startswith('en/'):
        return 'en'
    elif '/ja/' in path_str or path_str.startswith('ja/') or '/jp/' in path_str or path_str.startswith('jp/'):
        return 'ja'
    elif '/ko/' in path_str or path_str.startswith('ko/') or '/kr/' in path_str or path_str.startswith('kr/'):
        return 'ko'
    else:
        return 'zh'


def get_copywriting(file_name, lang='zh'):
    """获取文案模板"""
    # 移除路径前缀
    base_name = Path(file_name).name
    
    if base_name in COPYWRITING_TEMPLATES:
        templates = COPYWRITING_TEMPLATES[base_name]
        if lang in templates:
            return templates[lang]
        elif 'zh' in templates:
            return templates['zh']
    
    return None


def update_meta_tags(file_path):
    """更新单个文件的 meta 标签"""
    try:
        # 读取文件
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检测语言
        lang = detect_language(file_path)
        
        # 获取文案
        copywriting = get_copywriting(file_path.name, lang)
        if not copywriting:
            print(f"  ⏭️  跳过（无文案模板）: {file_path.name}")
            return False
        
        # 备份原文件
        backup_path = BACKUP_DIR / file_path.name
        shutil.copy2(file_path, backup_path)
        
        # 更新 title
        title_pattern = r'<title>.*?</title>'
        new_title = f'<title>{copywriting["title"]}</title>'
        if re.search(title_pattern, content, re.DOTALL):
            content = re.sub(title_pattern, new_title, content, flags=re.DOTALL)
            print(f"  ✅ 更新 title")
        
        # 更新 description
        desc_pattern = r'<meta\s+name="description"\s+content="[^"]*"[^>]*>'
        new_desc = f'<meta name="description" content="{copywriting["description"]}">'
        if re.search(desc_pattern, content):
            content = re.sub(desc_pattern, new_desc, content)
            print(f"  ✅ 更新 description")
        else:
            # 如果没有 description，添加在 title 后面
            content = re.sub(
                r'(</title>)',
                f'\\1\n{new_desc}',
                content,
                count=1
            )
            print(f"  ✅ 添加 description")
        
        # 保存文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  📝 新标题: {copywriting['title'][:50]}...")
        print(f"  📝 新描述: {copywriting['description'][:50]}...")
        
        return True
        
    except Exception as e:
        print(f"  ❌ 错误: {e}")
        return False


def main():
    """主函数"""
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("🎯 开始批量优化文案...")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    
    print(f"📂 备份目录: {BACKUP_DIR}")
    print(f"📋 文案模板: {len(COPYWRITING_TEMPLATES)} 个\n")
    
    # 查找所有 HTML 文件
    html_files = []
    
    # 主目录
    for file_name in COPYWRITING_TEMPLATES.keys():
        file_path = BASE_DIR / file_name
        if file_path.exists():
            html_files.append(file_path)
    
    # 子目录（en, ja, jp, ko, kr）
    for lang_dir in ['en', 'ja', 'jp', 'ko', 'kr']:
        lang_path = BASE_DIR / lang_dir
        if lang_path.exists():
            for file_name in COPYWRITING_TEMPLATES.keys():
                file_path = lang_path / file_name
                if file_path.exists():
                    html_files.append(file_path)
    
    print(f"📁 找到 {len(html_files)} 个文件需要优化\n")
    
    success_count = 0
    skip_count = 0
    error_count = 0
    
    for i, file_path in enumerate(html_files, 1):
        print(f"[{i}/{len(html_files)}] 处理: {file_path.relative_to(BASE_DIR)}")
        result = update_meta_tags(file_path)
        if result is True:
            success_count += 1
        elif result is False:
            skip_count += 1
        else:
            error_count += 1
        print()
    
    # 统计
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("📊 优化完成统计：")
    print(f"✅ 成功：{success_count} 个文件")
    print(f"⏭️  跳过：{skip_count} 个文件")
    print(f"❌ 错误：{error_count} 个文件")
    print(f"📂 备份位置：{BACKUP_DIR}")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    
    print("🎯 下一步：")
    print("1. 检查优化后的文件（特别是首页）")
    print("2. 在浏览器中查看效果")
    print("3. 提交 Google Search Console 重新抓取")
    print("4. 使用 Facebook Debugger 测试")
    print("\n⚠️  如果需要恢复，备份文件在：", BACKUP_DIR)
    print("\n💡 预期效果：CTR 从 0% 提升到 3-5%（1-4周内）")


if __name__ == '__main__':
    main()

