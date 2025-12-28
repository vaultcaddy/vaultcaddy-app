#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量优化Landing Page的SEO元数据（Title/Meta/H1）
实施关键词差异化战略，避免关键词竞食
"""

import os
import re
from pathlib import Path

BASE_DIR = Path(__file__).parent

# ==================== 银行页面SEO配置 ====================

BANK_SEO_CONFIG = {
    'hsbc': {
        'zh': {
            'title': '滙豐銀行對帳單AI自動處理｜HSBC PDF轉Excel/QuickBooks｜98%準確｜香港',
            'description': '滙豐銀行（HSBC）個人+商業帳戶對帳單AI識別，支持網銀PDF、手機App截圖、紙質月結單。3秒轉Excel/QuickBooks/Xero，準確率98%。支持國際轉賬、多幣種、信用卡賬單。香港200+企業使用｜免費試用20頁',
            'h1': '滙豐銀行對帳單AI自動處理 - 個人+商業帳戶',
            'keywords': ['滙豐銀行對帳單AI', 'HSBC PDF轉Excel', '滙豐網銀處理', 'HSBC商業帳戶']
        },
        'en': {
            'title': 'HSBC Bank Statement AI Processing｜PDF to Excel/QuickBooks｜98% Accuracy｜HK',
            'description': 'HSBC personal + business account statement AI recognition. Supports online banking PDF, mobile screenshots, paper statements. 3-second conversion to Excel/QuickBooks/Xero, 98% accuracy. International transfers, multi-currency, credit cards. Used by 200+ HK businesses',
            'h1': 'HSBC Bank Statement AI Processing - Personal + Business Accounts',
            'keywords': ['HSBC statement AI', 'HSBC PDF to Excel', 'HSBC online banking', 'HSBC business account']
        },
        'kr': {
            'title': 'HSBC 은행 명세서 AI 처리｜PDF를 Excel로 변환｜98% 정확도｜홍콩',
            'description': 'HSBC 개인+비즈니스 계좌 명세서 AI 인식. 온라인 뱅킹 PDF, 모바일 스크린샷 지원. 3초 만에 Excel/QuickBooks로 변환, 정확도 98%. 국제 송금, 다중 통화 지원. 홍콩 200개 이상 기업 사용',
            'h1': 'HSBC 은행 명세서 AI 자동 처리 - 개인+비즈니스',
            'keywords': ['HSBC 명세서 AI', 'HSBC PDF Excel 변환', 'HSBC 온라인뱅킹']
        },
        'jp': {
            'title': 'HSBC銀行明細AI処理｜PDFをExcelに変換｜98%精度｜香港',
            'description': 'HSBC個人+ビジネス口座明細のAI認識。オンラインバンキングPDF、モバイルスクリーンショット対応。3秒でExcel/QuickBooksに変換、精度98%。国際送金、多通貨対応。香港200社以上が利用',
            'h1': 'HSBC銀行明細AI自動処理 - 個人+ビジネス口座',
            'keywords': ['HSBC明細AI', 'HSBC PDF Excel変換', 'HSBCオンラインバンキング']
        }
    },
    'hangseng': {
        'zh': {
            'title': '恒生銀行月結單轉Excel教學｜中小企對帳自動化｜Hang Seng Statement OCR',
            'description': '恒生銀行月結單手動輸入太慢？VaultCaddy專為香港中小企設計，自動識別恒生網銀PDF、優越理財月結單，轉成Excel/CSV/Xero。支持企業戶口、Savings、信用卡。3秒處理｜98%準確｜HK$46/月起',
            'h1': '恒生銀行月結單自動轉Excel - 中小企對帳解決方案',
            'keywords': ['恒生銀行月結單', '中小企對帳', 'Hang Seng Statement OCR', '恒生優越理財']
        },
        'en': {
            'title': 'Hang Seng Bank Statement to Excel｜SME Accounting Automation｜OCR Processing',
            'description': 'Manual input of Hang Seng statements too slow? VaultCaddy designed for HK SMEs. Auto-recognize online banking PDF, Prestige statements to Excel/CSV/Xero. Business accounts, Savings, credit cards. 3-sec processing｜98% accuracy｜From HK$46/mo',
            'h1': 'Hang Seng Bank Statement to Excel - SME Accounting Solution',
            'keywords': ['Hang Seng statement', 'SME accounting', 'Hang Seng OCR', 'Hang Seng Prestige']
        },
        'kr': {
            'title': 'Hang Seng 은행 명세서 Excel 변환｜중소기업 회계 자동화｜OCR 처리',
            'description': 'Hang Seng 명세서 수동 입력이 너무 느리신가요? 홍콩 중소기업을 위한 VaultCaddy. 온라인뱅킹 PDF, Prestige 명세서를 Excel/CSV로 자동 변환. 3초 처리｜98% 정확도｜월 HK$46부터',
            'h1': 'Hang Seng 은행 명세서 Excel 변환 - 중소기업 솔루션',
            'keywords': ['Hang Seng 명세서', '중소기업 회계', 'Hang Seng OCR']
        },
        'jp': {
            'title': 'Hang Seng銀行明細Excel変換｜中小企業会計自動化｜OCR処理',
            'description': 'Hang Seng明細の手動入力が遅すぎる？香港中小企業向けVaultCaddy。オンラインバンキングPDF、Prestige明細をExcel/CSVに自動変換。3秒処理｜98%精度｜月HK$46から',
            'h1': 'Hang Seng銀行明細Excel変換 - 中小企業ソリューション',
            'keywords': ['Hang Seng明細', '中小企業会計', 'Hang Seng OCR']
        }
    },
    'bochk': {
        'zh': {
            'title': '中國銀行香港對帳單處理｜BOCHK多幣種月結單｜iBanking PDF轉Excel',
            'description': '中國銀行（香港）對帳單AI處理，支持iBanking網銀PDF、多幣種賬戶、企業戶口月結單。自動識別人民幣/美元/港幣交易，轉Excel/CSV。官方背景銀行首選方案｜3秒處理｜98%準確率',
            'h1': '中國銀行香港對帳單AI處理 - 多幣種企業帳戶',
            'keywords': ['中國銀行香港對帳單', 'BOCHK多幣種', 'iBanking PDF', '中銀企業戶口']
        },
        'en': {
            'title': 'Bank of China HK Statement Processing｜BOCHK Multi-Currency｜iBanking PDF to Excel',
            'description': 'Bank of China (Hong Kong) statement AI processing. Supports iBanking PDF, multi-currency accounts, corporate statements. Auto-recognize RMB/USD/HKD transactions to Excel/CSV. Official bank solution｜3-sec processing｜98% accuracy',
            'h1': 'BOCHK Statement AI Processing - Multi-Currency Corporate Accounts',
            'keywords': ['BOCHK statement', 'BOCHK multi-currency', 'iBanking PDF', 'BOCHK corporate']
        },
        'kr': {
            'title': 'Bank of China 홍콩 명세서 처리｜BOCHK 다중통화｜iBanking PDF Excel 변환',
            'description': 'Bank of China (홍콩) 명세서 AI 처리. iBanking PDF, 다중통화 계좌, 기업 명세서 지원. 위안화/달러/홍콩달러 거래 자동 인식, Excel/CSV 변환. 3초 처리｜98% 정확도',
            'h1': 'BOCHK 명세서 AI 처리 - 다중통화 기업 계좌',
            'keywords': ['BOCHK 명세서', 'BOCHK 다중통화', 'iBanking PDF']
        },
        'jp': {
            'title': 'Bank of China 香港明細処理｜BOCHK多通貨｜iBanking PDF Excel変換',
            'description': 'Bank of China（香港）明細AI処理。iBanking PDF、多通貨口座、法人明細対応。人民元/ドル/香港ドル取引を自動認識、Excel/CSV変換。3秒処理｜98%精度',
            'h1': 'BOCHK明細AI処理 - 多通貨法人口座',
            'keywords': ['BOCHK明細', 'BOCHK多通貨', 'iBanking PDF']
        }
    },
    'sc': {
        'zh': {
            'title': '渣打銀行對帳單OCR識別｜外資銀行月結單處理｜Standard Chartered PDF',
            'description': '渣打銀行（Standard Chartered）對帳單自動處理，支持Priority Banking、外幣帳戶、國際業務月結單。AI識別網銀PDF轉Excel/QuickBooks，適合跨境貿易企業｜3秒處理｜HK$46/月',
            'h1': '渣打銀行對帳單OCR - 外資銀行+國際業務專用',
            'keywords': ['渣打銀行對帳單OCR', '外資銀行', 'Standard Chartered PDF', 'Priority Banking']
        },
        'en': {
            'title': 'Standard Chartered Statement OCR｜Foreign Bank Processing｜SC PDF to Excel',
            'description': 'Standard Chartered bank statement auto-processing. Supports Priority Banking, foreign currency accounts, international business statements. AI recognition of PDF to Excel/QuickBooks, ideal for cross-border trade｜3-sec｜HK$46/mo',
            'h1': 'Standard Chartered Statement OCR - Foreign Bank + International Business',
            'keywords': ['SC statement OCR', 'foreign bank', 'Standard Chartered PDF', 'Priority Banking']
        },
        'kr': {
            'title': 'Standard Chartered 명세서 OCR｜외국계 은행｜SC PDF Excel 변환',
            'description': 'Standard Chartered 은행 명세서 자동 처리. Priority Banking, 외화 계좌, 국제 비즈니스 명세서 지원. PDF를 Excel/QuickBooks로 AI 인식, 국경간 무역에 적합｜3초｜HK$46/월',
            'h1': 'Standard Chartered 명세서 OCR - 외국계 은행 + 국제 비즈니스',
            'keywords': ['SC 명세서 OCR', '외국계 은행', 'Standard Chartered PDF']
        },
        'jp': {
            'title': 'Standard Chartered 明細OCR｜外資系銀行｜SC PDF Excel変換',
            'description': 'Standard Chartered銀行明細自動処理。Priority Banking、外貨口座、国際ビジネス明細対応。PDFをExcel/QuickBooksにAI認識、クロスボーダー貿易に最適｜3秒｜HK$46/月',
            'h1': 'Standard Chartered 明細OCR - 外資系銀行 + 国際ビジネス',
            'keywords': ['SC明細OCR', '外資系銀行', 'Standard Chartered PDF']
        }
    },
    'dbs': {
        'zh': {
            'title': '星展銀行對帳單AI處理｜DBS數字化對帳方案｜ideal網銀PDF轉Excel',
            'description': '星展銀行（DBS）對帳單自動化處理，支持ideal網銀、SME Banking、企業戶口月結單。數字化銀行首選AI方案，PDF轉Excel/Xero/CSV。新加坡最大銀行｜3秒處理｜98%準確',
            'h1': '星展銀行對帳單AI自動化 - DBS數字銀行方案',
            'keywords': ['星展銀行對帳單AI', 'DBS數字化', 'ideal網銀', 'DBS SME Banking']
        },
        'en': {
            'title': 'DBS Bank Statement AI Processing｜Digital Banking Solution｜ideal PDF to Excel',
            'description': 'DBS bank statement automation. Supports ideal online banking, SME Banking, corporate statements. Digital bank preferred AI solution, PDF to Excel/Xero/CSV. Singapore largest bank｜3-sec processing｜98% accuracy',
            'h1': 'DBS Bank Statement AI Automation - Digital Banking Solution',
            'keywords': ['DBS statement AI', 'DBS digital', 'ideal online banking', 'DBS SME']
        },
        'kr': {
            'title': 'DBS 은행 명세서 AI 처리｜디지털 뱅킹 솔루션｜ideal PDF Excel 변환',
            'description': 'DBS 은행 명세서 자동화. ideal 온라인뱅킹, SME Banking, 기업 명세서 지원. 디지털 은행 선호 AI 솔루션, PDF를 Excel/Xero/CSV로 변환. 싱가포르 최대 은행｜3초 처리｜98% 정확도',
            'h1': 'DBS 은행 명세서 AI 자동화 - 디지털 뱅킹 솔루션',
            'keywords': ['DBS 명세서 AI', 'DBS 디지털', 'ideal 온라인뱅킹']
        },
        'jp': {
            'title': 'DBS銀行明細AI処理｜デジタルバンキングソリューション｜ideal PDF Excel変換',
            'description': 'DBS銀行明細自動化。idealオンラインバンキング、SME Banking、法人明細対応。デジタル銀行優先AIソリューション、PDFをExcel/Xero/CSVに変換。シンガポール最大銀行｜3秒処理｜98%精度',
            'h1': 'DBS銀行明細AI自動化 - デジタルバンキングソリューション',
            'keywords': ['DBS明細AI', 'DBSデジタル', 'idealオンラインバンキング']
        }
    },
    # 其他银行使用通用模板（根据银行名自动生成）
    'default': {
        'zh': {
            'title': '{bank_name}對帳單AI處理｜網銀PDF轉Excel｜3秒完成｜香港',
            'description': '{bank_name}對帳單、收據、發票手工錄入太慢？VaultCaddy AI自動識別網銀PDF，3秒轉成Excel/CSV/QuickBooks，準確率98%。支持企業帳戶、個人帳戶。月費$46起，免費試用20頁',
            'h1': '{bank_name}對帳單AI自動處理',
            'keywords': ['{bank_name}對帳單', '{bank_name} PDF轉Excel', '{bank_name}網銀']
        },
        'en': {
            'title': '{bank_name} Statement AI Processing｜PDF to Excel｜3-Second｜Hong Kong',
            'description': '{bank_name} statement, receipt, invoice manual entry too slow? VaultCaddy AI auto-recognizes online banking PDF, 3-sec conversion to Excel/CSV/QuickBooks, 98% accuracy. Business & personal accounts. From HK$46/mo, free trial',
            'h1': '{bank_name} Statement AI Auto-Processing',
            'keywords': ['{bank_name} statement', '{bank_name} PDF Excel', '{bank_name} online banking']
        },
        'kr': {
            'title': '{bank_name} 명세서 AI 처리｜PDF Excel 변환｜3초｜홍콩',
            'description': '{bank_name} 명세서, 영수증 수동 입력이 너무 느리신가요? VaultCaddy AI가 온라인뱅킹 PDF를 자동 인식, 3초 만에 Excel/CSV로 변환, 정확도 98%. 월 HK$46부터, 무료 체험',
            'h1': '{bank_name} 명세서 AI 자동 처리',
            'keywords': ['{bank_name} 명세서', '{bank_name} PDF Excel', '{bank_name} 온라인뱅킹']
        },
        'jp': {
            'title': '{bank_name}明細AI処理｜PDF Excel変換｜3秒｜香港',
            'description': '{bank_name}明細、領収書の手動入力が遅すぎる？VaultCaddy AIがオンラインバンキングPDFを自動認識、3秒でExcel/CSVに変換、精度98%。月HK$46から、無料トライアル',
            'h1': '{bank_name}明細AI自動処理',
            'keywords': ['{bank_name}明細', '{bank_name} PDF Excel', '{bank_name}オンラインバンキング']
        }
    }
}

# 银行中英文名称映射
BANK_NAMES = {
    'hsbc': {'zh': '滙豐銀行', 'en': 'HSBC', 'kr': 'HSBC', 'jp': 'HSBC'},
    'hangseng': {'zh': '恒生銀行', 'en': 'Hang Seng', 'kr': 'Hang Seng', 'jp': 'Hang Seng'},
    'hang-seng': {'zh': '恒生銀行', 'en': 'Hang Seng', 'kr': 'Hang Seng', 'jp': 'Hang Seng'},
    'bochk': {'zh': '中國銀行香港', 'en': 'Bank of China HK', 'kr': 'Bank of China 홍콩', 'jp': 'Bank of China 香港'},
    'boc-hk': {'zh': '中國銀行香港', 'en': 'Bank of China HK', 'kr': 'Bank of China 홍콩', 'jp': 'Bank of China 香港'},
    'sc': {'zh': '渣打銀行', 'en': 'Standard Chartered', 'kr': 'Standard Chartered', 'jp': 'Standard Chartered'},
    'dbs': {'zh': '星展銀行', 'en': 'DBS', 'kr': 'DBS', 'jp': 'DBS'},
    'bea': {'zh': '東亞銀行', 'en': 'Bank of East Asia', 'kr': 'Bank of East Asia', 'jp': '東亜銀行'},
    'citibank': {'zh': '花旗銀行', 'en': 'Citibank', 'kr': 'Citibank', 'jp': 'Citibank'},
    'dahsing': {'zh': '大新銀行', 'en': 'Dah Sing', 'kr': 'Dah Sing', 'jp': '大新銀行'},
    'citic': {'zh': '中信銀行', 'en': 'CITIC', 'kr': 'CITIC', 'jp': '中信銀行'},
    'bankcomm': {'zh': '交通銀行', 'en': 'Bank of Communications', 'kr': 'Bank of Communications', 'jp': '交通銀行'},
    'fubon': {'zh': '富邦銀行', 'en': 'Fubon', 'kr': 'Fubon', 'jp': '富邦銀行'},
    'ocbc': {'zh': '華僑銀行', 'en': 'OCBC', 'kr': 'OCBC', 'jp': '華僑銀行'},
    # 韩国银行
    'hana': {'zh': 'Hana銀行', 'en': 'Hana Bank', 'kr': '하나은행', 'jp': 'Hana銀行'},
    'kb': {'zh': 'KB銀行', 'en': 'KB Bank', 'kr': 'KB은행', 'jp': 'KB銀行'},
    'nh': {'zh': 'NH銀行', 'en': 'NH Bank', 'kr': 'NH은행', 'jp': 'NH銀行'},
    'shinhan': {'zh': 'Shinhan銀行', 'en': 'Shinhan Bank', 'kr': '신한은행', 'jp': 'Shinhan銀行'},
    'woori': {'zh': 'Woori銀行', 'en': 'Woori Bank', 'kr': '우리은행', 'jp': 'Woori銀行'},
    # 日本银行
    'mizuho': {'zh': '瑞穗銀行', 'en': 'Mizuho', 'kr': 'Mizuho', 'jp': 'みずほ銀行'},
    'mufg': {'zh': '三菱UFJ銀行', 'en': 'MUFG', 'kr': 'MUFG', 'jp': '三菱UFJ銀行'},
    'smbc': {'zh': '三井住友銀行', 'en': 'SMBC', 'kr': 'SMBC', 'jp': '三井住友銀行'},
    'resona': {'zh': 'Resona銀行', 'en': 'Resona', 'kr': 'Resona', 'jp': 'りそな銀行'},
    'shinsei': {'zh': 'Shinsei銀行', 'en': 'Shinsei', 'kr': 'Shinsei', 'jp': '新生銀行'},
}

# ==================== 行业页面SEO配置 ====================

INDUSTRY_SEO_CONFIG = {
    'restaurant': {
        'zh': {
            'title': '餐廳會計軟件香港｜食肆收據管理系統｜餐飲業QuickBooks對接｜月費$46',
            'description': '香港餐廳專用會計軟件，自動處理食材發票、員工薪酬、POS對帳單。AI識別收據轉Excel/QuickBooks，支持成本控制、報稅合規。200+餐廳使用｜3秒處理｜98%準確｜免費試用',
            'h1': '餐廳會計軟件 - 食材成本+員工薪酬+報稅一站式',
            'keywords': ['餐廳會計軟件香港', '餐廳收據管理', '餐飲業QuickBooks', '食肆記帳']
        },
        'en': {
            'title': 'Restaurant Accounting Software HK｜F&B Receipt Management｜QuickBooks Integration',
            'description': 'Hong Kong restaurant accounting software. Auto-process ingredient invoices, staff payroll, POS statements. AI recognition of receipts to Excel/QuickBooks. Cost control, tax compliance. 200+ restaurants｜3-sec｜98% accuracy',
            'h1': 'Restaurant Accounting Software - Ingredient Cost + Payroll + Tax',
            'keywords': ['restaurant accounting HK', 'F&B receipt management', 'restaurant QuickBooks']
        },
        'kr': {
            'title': '레스토랑 회계 소프트웨어 홍콩｜식당 영수증 관리｜QuickBooks 연동',
            'description': '홍콩 레스토랑 전용 회계 소프트웨어. 식재료 청구서, 직원 급여, POS 명세서 자동 처리. AI 영수증 인식, Excel/QuickBooks 변환. 비용 관리, 세금 규정 준수. 200개 이상 레스토랑 사용',
            'h1': '레스토랑 회계 소프트웨어 - 식재료 + 급여 + 세금',
            'keywords': ['레스토랑 회계 홍콩', '식당 영수증 관리', '레스토랑 QuickBooks']
        },
        'jp': {
            'title': 'レストラン会計ソフト香港｜飲食店レシート管理｜QuickBooks連携',
            'description': '香港レストラン専用会計ソフト。食材請求書、スタッフ給与、POSステートメント自動処理。AIレシート認識、Excel/QuickBooks変換。コスト管理、税務コンプライアンス。200店舗以上利用',
            'h1': 'レストラン会計ソフト - 食材 + 給与 + 税務',
            'keywords': ['レストラン会計香港', '飲食店レシート管理', 'レストランQuickBooks']
        }
    },
    # 其他行业使用通用模板
    'default': {
        'zh': {
            'title': '{industry_name}會計軟件香港｜{industry_name}收據管理｜QuickBooks對接｜$46/月',
            'description': '香港{industry_name}專用會計軟件，自動處理收據、發票、對帳單。AI識別轉Excel/QuickBooks/Xero，支持報稅合規。3秒處理｜98%準確｜免費試用20頁',
            'h1': '{industry_name}會計軟件 - 收據管理+報稅合規一站式',
            'keywords': ['{industry_name}會計軟件', '{industry_name}收據管理', '{industry_name}記帳']
        },
        'en': {
            'title': '{industry_name} Accounting Software HK｜Receipt Management｜QuickBooks｜$46/mo',
            'description': 'Hong Kong {industry_name} accounting software. Auto-process receipts, invoices, statements. AI recognition to Excel/QuickBooks/Xero. Tax compliance. 3-sec｜98% accuracy｜Free trial',
            'h1': '{industry_name} Accounting Software - Receipt + Tax Compliance',
            'keywords': ['{industry_name} accounting', '{industry_name} receipt management', '{industry_name} bookkeeping']
        },
        'kr': {
            'title': '{industry_name} 회계 소프트웨어 홍콩｜영수증 관리｜QuickBooks｜$46/월',
            'description': '홍콩 {industry_name} 회계 소프트웨어. 영수증, 청구서, 명세서 자동 처리. AI 인식, Excel/QuickBooks/Xero 변환. 세금 규정 준수. 3초｜98% 정확도｜무료 체험',
            'h1': '{industry_name} 회계 소프트웨어 - 영수증 + 세금 규정',
            'keywords': ['{industry_name} 회계', '{industry_name} 영수증 관리', '{industry_name} 부기']
        },
        'jp': {
            'title': '{industry_name}会計ソフト香港｜レシート管理｜QuickBooks｜$46/月',
            'description': '香港{industry_name}会計ソフト。レシート、請求書、明細自動処理。AI認識、Excel/QuickBooks/Xero変換。税務コンプライアンス。3秒｜98%精度｜無料トライアル',
            'h1': '{industry_name}会計ソフト - レシート + 税務コンプライアンス',
            'keywords': ['{industry_name}会計', '{industry_name}レシート管理', '{industry_name}帳簿']
        }
    }
}

# 行业中英文名称映射
INDUSTRY_NAMES = {
    'restaurant': {'zh': '餐廳', 'en': 'Restaurant', 'kr': '레스토랑', 'jp': 'レストラン'},
    'retail': {'zh': '零售店', 'en': 'Retail', 'kr': '소매점', 'jp': '小売店'},
    'beauty': {'zh': '美容院', 'en': 'Beauty Salon', 'kr': '미용실', 'jp': '美容院'},
    'cleaning': {'zh': '清潔服務', 'en': 'Cleaning Service', 'kr': '청소 서비스', 'jp': '清掃サービス'},
    'pet': {'zh': '寵物服務', 'en': 'Pet Service', 'kr': '애완동물 서비스', 'jp': 'ペットサービス'},
    'travel': {'zh': '旅行社', 'en': 'Travel Agency', 'kr': '여행사', 'jp': '旅行代理店'},
    'event': {'zh': '活動策劃', 'en': 'Event Planning', 'kr': '이벤트 기획', 'jp': 'イベント企画'},
    'coworking': {'zh': '共享辦公', 'en': 'Coworking', 'kr': '공유 오피스', 'jp': 'コワーキング'},
    'property': {'zh': '物業管理', 'en': 'Property Management', 'kr': '부동산 관리', 'jp': '不動産管理'},
    'delivery': {'zh': '配送服務', 'en': 'Delivery Service', 'kr': '배달 서비스', 'jp': '配送サービス'},
    'healthcare': {'zh': '醫療保健', 'en': 'Healthcare', 'kr': '의료', 'jp': '医療'},
    'accountant': {'zh': '會計師事務所', 'en': 'Accounting Firm', 'kr': '회계사무소', 'jp': '会計事務所'},
    'lawyer': {'zh': '律師事務所', 'en': 'Law Firm', 'kr': '법무법인', 'jp': '法律事務所'},
    'consultant': {'zh': '顧問服務', 'en': 'Consulting', 'kr': '컨설팅', 'jp': 'コンサルティング'},
    'marketing': {'zh': '營銷機構', 'en': 'Marketing Agency', 'kr': '마케팅 에이전시', 'jp': 'マーケティング'},
    'realestate': {'zh': '房地產', 'en': 'Real Estate', 'kr': '부동산', 'jp': '不動産'},
    'designer': {'zh': '設計師', 'en': 'Designer', 'kr': '디자이너', 'jp': 'デザイナー'},
    'developer': {'zh': '開發者', 'en': 'Developer', 'kr': '개발자', 'jp': '開発者'},
    'photographer': {'zh': '攝影師', 'en': 'Photographer', 'kr': '사진작가', 'jp': '写真家'},
    'tutor': {'zh': '補習老師', 'en': 'Tutor', 'kr': '과외교사', 'jp': '家庭教師'},
    'fitness': {'zh': '健身教練', 'en': 'Fitness Trainer', 'kr': '피트니스 트레이너', 'jp': 'フィットネストレーナー'},
    'artist': {'zh': '藝術家', 'en': 'Artist', 'kr': '예술가', 'jp': 'アーティスト'},
    'musician': {'zh': '音樂家', 'en': 'Musician', 'kr': '음악가', 'jp': 'ミュージシャン'},
    'freelancer': {'zh': '自由職業者', 'en': 'Freelancer', 'kr': '프리랜서', 'jp': 'フリーランサー'},
    'contractor': {'zh': '承包商', 'en': 'Contractor', 'kr': '계약자', 'jp': '請負業者'},
    'smallbiz': {'zh': '小型企業', 'en': 'Small Business', 'kr': '소기업', 'jp': '小企業'},
    'startup': {'zh': '創業公司', 'en': 'Startup', 'kr': '스타트업', 'jp': 'スタートアップ'},
    'ecommerce': {'zh': '電商企業', 'en': 'E-commerce', 'kr': '전자상거래', 'jp': 'Eコマース'},
    'finance': {'zh': '個人理財', 'en': 'Personal Finance', 'kr': '개인 금융', 'jp': '個人金融'},
    'nonprofit': {'zh': '非營利組織', 'en': 'Non-profit', 'kr': '비영리단체', 'jp': '非営利団体'},
    'education': {'zh': '教育機構', 'en': 'Education', 'kr': '교육기관', 'jp': '教育機関'},
}

def get_language_from_path(file_path):
    """从文件路径识别语言"""
    path_str = str(file_path)
    if '/en/' in path_str:
        return 'en'
    elif '/kr/' in path_str:
        return 'kr'
    elif '/jp/' in path_str:
        return 'jp'
    else:
        return 'zh'

def get_bank_key(filename):
    """从文件名提取银行key"""
    filename_lower = filename.lower()
    # 优先匹配长的key（避免hang-seng被识别为hang）
    keys = sorted(BANK_NAMES.keys(), key=len, reverse=True)
    for key in keys:
        if key in filename_lower:
            return key
    return None

def get_industry_key(filename):
    """从文件名提取行业key"""
    filename_lower = filename.lower()
    for key in INDUSTRY_NAMES.keys():
        if key in filename_lower:
            return key
    return None

def get_bank_seo_config(bank_key, lang):
    """获取银行的SEO配置"""
    if bank_key in BANK_SEO_CONFIG:
        return BANK_SEO_CONFIG[bank_key].get(lang, BANK_SEO_CONFIG[bank_key]['zh'])
    else:
        # 使用默认模板
        bank_name = BANK_NAMES.get(bank_key, {}).get(lang, bank_key.upper())
        template = BANK_SEO_CONFIG['default'][lang]
        return {
            'title': template['title'].replace('{bank_name}', bank_name),
            'description': template['description'].replace('{bank_name}', bank_name),
            'h1': template['h1'].replace('{bank_name}', bank_name),
            'keywords': [kw.replace('{bank_name}', bank_name) for kw in template['keywords']]
        }

def get_industry_seo_config(industry_key, lang):
    """获取行业的SEO配置"""
    if industry_key in INDUSTRY_SEO_CONFIG:
        return INDUSTRY_SEO_CONFIG[industry_key].get(lang, INDUSTRY_SEO_CONFIG[industry_key]['zh'])
    else:
        # 使用默认模板
        industry_name = INDUSTRY_NAMES.get(industry_key, {}).get(lang, industry_key.title())
        template = INDUSTRY_SEO_CONFIG['default'][lang]
        return {
            'title': template['title'].replace('{industry_name}', industry_name),
            'description': template['description'].replace('{industry_name}', industry_name),
            'h1': template['h1'].replace('{industry_name}', industry_name),
            'keywords': [kw.replace('{industry_name}', industry_name) for kw in template['keywords']]
        }

def update_bank_page_seo(file_path):
    """更新银行页面的SEO元数据"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        bank_key = get_bank_key(file_path.name)
        if not bank_key:
            print(f"  ⚠️  无法识别银行: {file_path.name}")
            return False
        
        lang = get_language_from_path(file_path)
        seo_config = get_bank_seo_config(bank_key, lang)
        
        # 更新Title
        title_pattern = r'<title>.*?</title>'
        new_title = f'<title>{seo_config["title"]}</title>'
        if re.search(title_pattern, content, re.DOTALL):
            content = re.sub(title_pattern, new_title, content, count=1, flags=re.DOTALL)
        else:
            print(f"  ⚠️  找不到<title>: {file_path.name}")
            return False
        
        # 更新Meta Description
        meta_pattern = r'<meta name="description" content=".*?">'
        new_meta = f'<meta name="description" content="{seo_config["description"]}">'
        if re.search(meta_pattern, content, re.DOTALL):
            content = re.sub(meta_pattern, new_meta, content, count=1, flags=re.DOTALL)
        
        # 更新H1
        h1_pattern = r'<h1>.*?</h1>'
        new_h1 = f'<h1>{seo_config["h1"]}</h1>'
        if re.search(h1_pattern, content, re.DOTALL):
            content = re.sub(h1_pattern, new_h1, content, count=1, flags=re.DOTALL)
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        bank_name = BANK_NAMES.get(bank_key, {}).get(lang, bank_key)
        print(f"  ✅ {file_path.name} ({bank_name} - {lang})")
        return True
        
    except Exception as e:
        print(f"  ❌ 错误 {file_path.name}: {str(e)}")
        return False

def update_industry_page_seo(file_path):
    """更新行业页面的SEO元数据"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        industry_key = get_industry_key(file_path.name)
        if not industry_key:
            print(f"  ⚠️  无法识别行业: {file_path.name}")
            return False
        
        lang = get_language_from_path(file_path)
        seo_config = get_industry_seo_config(industry_key, lang)
        
        # 更新Title
        title_pattern = r'<title>.*?</title>'
        new_title = f'<title>{seo_config["title"]}</title>'
        if re.search(title_pattern, content, re.DOTALL):
            content = re.sub(title_pattern, new_title, content, count=1, flags=re.DOTALL)
        else:
            print(f"  ⚠️  找不到<title>: {file_path.name}")
            return False
        
        # 更新Meta Description
        meta_pattern = r'<meta name="description" content=".*?">'
        new_meta = f'<meta name="description" content="{seo_config["description"]}">'
        if re.search(meta_pattern, content, re.DOTALL):
            content = re.sub(meta_pattern, new_meta, content, count=1, flags=re.DOTALL)
        
        # 更新H1
        h1_pattern = r'<h1>.*?</h1>'
        new_h1 = f'<h1>{seo_config["h1"]}</h1>'
        if re.search(h1_pattern, content, re.DOTALL):
            content = re.sub(h1_pattern, new_h1, content, count=1, flags=re.DOTALL)
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        industry_name = INDUSTRY_NAMES.get(industry_key, {}).get(lang, industry_key)
        print(f"  ✅ {file_path.name} ({industry_name} - {lang})")
        return True
        
    except Exception as e:
        print(f"  ❌ 错误 {file_path.name}: {str(e)}")
        return False

def main():
    """主函数"""
    print("🚀 开始批量优化SEO元数据（Title/Meta/H1）...")
    print("🎯 实施关键词差异化战略，避免关键词竞食")
    print("=" * 70)
    
    total = 0
    success = 0
    failed = 0
    
    # 优化银行页面
    print("\n🏦 优化银行页面...")
    bank_files = list(BASE_DIR.glob('*-bank-statement.html'))
    for file_path in sorted(bank_files):
        total += 1
        if update_bank_page_seo(file_path):
            success += 1
        else:
            failed += 1
    
    # 多语言版银行页面
    for lang in ['en', 'kr', 'jp']:
        lang_dir = BASE_DIR / lang
        if lang_dir.exists():
            bank_files = list(lang_dir.glob('*-bank-statement.html'))
            for file_path in sorted(bank_files):
                total += 1
                if update_bank_page_seo(file_path):
                    success += 1
                else:
                    failed += 1
    
    # 优化行业页面
    print("\n🏢 优化行业页面...")
    industry_files = list(BASE_DIR.glob('*-accounting-solution.html'))
    for file_path in sorted(industry_files):
        total += 1
        if update_industry_page_seo(file_path):
            success += 1
        else:
            failed += 1
    
    # 多语言版行业页面
    for lang in ['en', 'kr', 'jp']:
        lang_dir = BASE_DIR / lang
        if lang_dir.exists():
            industry_files = list(lang_dir.glob('*-accounting-solution.html'))
            for file_path in sorted(industry_files):
                total += 1
                if update_industry_page_seo(file_path):
                    success += 1
                else:
                    failed += 1
    
    # 打印统计
    print("\n" + "=" * 70)
    print("📊 优化统计:")
    print(f"  总计: {total} 个文件")
    print(f"  ✅ 成功: {success} 个")
    print(f"  ❌ 失败: {failed} 个")
    print("=" * 70)
    print("\n✨ SEO元数据优化完成！")
    print("\n📈 下一步建议:")
    print("  1. 提交sitemap到Google Search Console")
    print("  2. 使用Google Rich Results测试工具验证")
    print("  3. 监控Google Analytics流量变化")
    print("  4. 2周后检查关键词排名变化")

if __name__ == '__main__':
    main()

