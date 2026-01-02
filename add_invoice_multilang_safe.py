#!/usr/bin/env python3
"""
🌏 为发票添加安全的多语言支持

参考银行对账单的实现方式：
1. 在 i18n 对象中添加发票相关的翻译键
2. 使用 t() 函数获取翻译文本
3. 不使用递归，确保安全
"""

import os
import re

def add_invoice_translations():
    """在 i18n 对象中添加发票翻译"""
    
    file_path = 'document-detail-new.js'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 找到每个语言的 i18n 定义并添加发票翻译
    
    # 1. 中文翻译（zh-TW）
    zh_invoice_translations = """        no_transactions: '無交易記錄',
        // 發票相關翻譯
        invoice_details: '發票詳情',
        invoice_number: '發票號碼',
        vendor: '供應商',
        total_amount: '總金額',
        line_items: '項目明細',
        code: '代碼',
        quantity: '數量',
        unit: '單位',
        unit_price: '單價',
        unit_default: '件',
        no_items: '無項目數據'"""
    
    content = re.sub(
        r"(no_transactions: '無交易記錄')(\s*}\s*,\s*'en':)",
        zh_invoice_translations + r"\2",
        content
    )
    
    # 2. 英文翻译（en）
    en_invoice_translations = """        no_transactions: 'No transactions',
        // Invoice translations
        invoice_details: 'Invoice Details',
        invoice_number: 'Invoice Number',
        vendor: 'Vendor',
        total_amount: 'Total Amount',
        line_items: 'Line Items',
        code: 'Code',
        quantity: 'Quantity',
        unit: 'Unit',
        unit_price: 'Unit Price',
        unit_default: 'pcs',
        no_items: 'No item data'"""
    
    content = re.sub(
        r"(no_transactions: 'No transactions')(\s*}\s*,\s*'ja':)",
        en_invoice_translations + r"\2",
        content
    )
    
    # 3. 日文翻译（ja）
    ja_invoice_translations = """        no_transactions: '取引記録がありません',
        // 請求書関連の翻訳
        invoice_details: '請求書詳細',
        invoice_number: '請求書番号',
        vendor: '仕入先',
        total_amount: '合計金額',
        line_items: '明細項目',
        code: 'コード',
        quantity: '数量',
        unit: '単位',
        unit_price: '単価',
        unit_default: '個',
        no_items: '項目データなし'"""
    
    content = re.sub(
        r"(no_transactions: '取引記録がありません')(\s*}\s*,\s*'ko':)",
        ja_invoice_translations + r"\2",
        content
    )
    
    # 4. 韩文翻译（ko）
    ko_invoice_translations = """        no_transactions: '거래 내역 없음',
        // 송장 관련 번역
        invoice_details: '송장 상세',
        invoice_number: '송장 번호',
        vendor: '공급업체',
        total_amount: '총액',
        line_items: '항목 명세',
        code: '코드',
        quantity: '수량',
        unit: '단위',
        unit_price: '단가',
        unit_default: '개',
        no_items: '항목 데이터 없음'"""
    
    content = re.sub(
        r"(no_transactions: '거래 내역 없음')(\s*}\s*};)",
        ko_invoice_translations + r"\2",
        content
    )
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ 已添加发票翻译到 i18n 对象")
    return True

def replace_invoice_hardcoded_text():
    """替换发票硬编码文本为 t() 函数调用"""
    
    file_path = 'document-detail-new.js'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替换发票详情区域的硬编码文本
    replacements = [
        # 标题和标签
        (r"Invoice Details", r"${t('invoice_details')}"),
        (r"Invoice Number", r"${t('invoice_number')}"),
        (r">Date<", r">${t('date')}<"),
        (r">Vendor<", r">${t('vendor')}<"),
        (r"Total Amount", r"${t('total_amount')}"),
        (r"Line Items", r"${t('line_items')}"),
        (r"\(Editable\)", r"${t('editable')}"),
        
        # 表头
        (r">Code<", r">${t('code')}<"),
        (r">Description<", r">${t('description')}<"),
        (r">Quantity<", r">${t('quantity')}<"),
        (r">Unit<", r">${t('unit')}<"),
        (r">Unit Price<", r">${t('unit_price')}<"),
        (r">Amount<", r">${t('amount')}<"),
        
        # 默认值
        (r"'pcs'", r"t('unit_default')"),
        (r"'No item data'", r"t('no_items')"),
    ]
    
    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ 已替换硬编码文本为 t() 函数调用")
    return True

def main():
    print("🌏 为发票添加安全的多语言支持...\n")
    
    print("=" * 60)
    print("第1步：在 i18n 对象中添加发票翻译")
    print("=" * 60)
    add_invoice_translations()
    
    print("\n" + "=" * 60)
    print("第2步：替换硬编码文本为 t() 函数")
    print("=" * 60)
    replace_invoice_hardcoded_text()
    
    print("\n" + "=" * 60)
    print("✅ 多语言支持添加完成！")
    print("=" * 60)
    
    print("\n📋 实现方式：")
    print("✅ 使用与银行对账单相同的 i18n 对象")
    print("✅ 使用 t() 函数获取翻译（安全，无递归）")
    print("✅ 支持 4 种语言：中文、英文、日文、韩文")
    
    print("\n🌏 支持的语言：")
    print("• 中文 (zh-TW): 發票詳情、發票號碼、供應商...")
    print("• 英文 (en): Invoice Details, Invoice Number, Vendor...")
    print("• 日文 (ja): 請求書詳細、請求書番号、仕入先...")
    print("• 韩文 (ko): 송장 상세、송장 번호、공급업체...")
    
    print("\n🔍 验证步骤：")
    print("1. 清除浏览器缓存")
    print("2. 访问英文版: /en/document-detail.html")
    print("3. 访问日文版: /jp/document-detail.html")
    print("4. 访问韩文版: /kr/document-detail.html")
    print("5. 确认发票详情显示对应语言")

if __name__ == '__main__':
    main()

