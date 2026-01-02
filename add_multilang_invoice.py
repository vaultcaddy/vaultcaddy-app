#!/usr/bin/env python3
"""
🌏 为 Invoice 详情添加日文和韩文支持

策略：在 document-detail-new.js 中添加语言检测和翻译映射
"""

import os
import re

def add_multilingual_support():
    """在 document-detail-new.js 开头添加多语言支持"""
    
    file_path = 'document-detail-new.js'
    
    if not os.path.exists(file_path):
        print(f"❌ 文件不存在: {file_path}")
        return False
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否已经添加过多语言支持
    if 'getInvoiceText' in content:
        print("ℹ️  多语言支持已存在，跳过")
        return False
    
    # 多语言支持代码
    multilang_code = '''// 🌏 多语言支持 - Invoice 详情
function getInvoiceText(key) {
    const path = window.location.pathname;
    let lang = 'en';
    if (path.includes('/jp/')) lang = 'ja';
    else if (path.includes('/kr/')) lang = 'ko';
    else if (!path.includes('/en/')) lang = 'zh-TW';
    
    const translations = {
        en: {
            invoiceDetails: 'Invoice Details',
            invoiceNumber: 'Invoice Number',
            date: 'Date',
            vendor: 'Vendor',
            totalAmount: 'Total Amount',
            lineItems: 'Line Items',
            editable: '(Editable)',
            code: 'Code',
            description: 'Description',
            quantity: 'Quantity',
            unit: 'Unit',
            unitPrice: 'Unit Price',
            amount: 'Amount',
            unitDefault: 'pcs',
            noItems: 'No item data'
        },
        ja: {
            invoiceDetails: '請求書詳細',
            invoiceNumber: '請求書番号',
            date: '日付',
            vendor: '仕入先',
            totalAmount: '合計金額',
            lineItems: '明細項目',
            editable: '(編集可能)',
            code: 'コード',
            description: '説明',
            quantity: '数量',
            unit: '単位',
            unitPrice: '単価',
            amount: '金額',
            unitDefault: '個',
            noItems: '項目データなし'
        },
        ko: {
            invoiceDetails: '송장 상세',
            invoiceNumber: '송장 번호',
            date: '날짜',
            vendor: '공급업체',
            totalAmount: '총액',
            lineItems: '항목 명세',
            editable: '(편집 가능)',
            code: '코드',
            description: '설명',
            quantity: '수량',
            unit: '단위',
            unitPrice: '단가',
            amount: '금액',
            unitDefault: '개',
            noItems: '항목 데이터 없음'
        },
        'zh-TW': {
            invoiceDetails: '發票詳情',
            invoiceNumber: '發票號碼',
            date: '日期',
            vendor: '供應商',
            totalAmount: '總金額',
            lineItems: '項目明細',
            editable: '(可編輯)',
            code: '代碼',
            description: '描述',
            quantity: '數量',
            unit: '單位',
            unitPrice: '單價',
            amount: '金額',
            unitDefault: '件',
            noItems: '無項目數據'
        }
    };
    
    return translations[lang][key] || translations['en'][key] || key;
}

'''
    
    # 在文件开头添加多语言支持代码
    content = multilang_code + content
    
    # 替换硬编码的英文文本为函数调用
    replacements = [
        (r'Invoice Details', lambda m: "' + getInvoiceText('invoiceDetails') + '"),
        (r'Invoice Number', lambda m: "' + getInvoiceText('invoiceNumber') + '"),
        # 只替换 label 中的 Date
        (r'(<label[^>]*>)Date(</label>)', r"\1' + getInvoiceText('date') + '\2"),
        (r'(<label[^>]*>)Vendor(</label>)', r"\1' + getInvoiceText('vendor') + '\2"),
        (r'(<label[^>]*>)Total Amount(</label>)', r"\1' + getInvoiceText('totalAmount') + '\2"),
        (r'Line Items', lambda m: "' + getInvoiceText('lineItems') + '"),
        (r'\(Editable\)', lambda m: "' + getInvoiceText('editable') + '"),
        (r'(<th>)Code(</th>)', r"\1' + getInvoiceText('code') + '\2"),
        (r'(<th>)Description(</th>)', r"\1' + getInvoiceText('description') + '\2"),
        (r'(<th[^>]*>)Quantity(</th>)', r"\1' + getInvoiceText('quantity') + '\2"),
        (r'(<th[^>]*>)Unit(</th>)', r"\1' + getInvoiceText('unit') + '\2"),
        (r'(<th[^>]*>)Unit Price(</th>)', r"\1' + getInvoiceText('unitPrice') + '\2"),
        (r'(<th[^>]*>)Amount(</th>)', r"\1' + getInvoiceText('amount') + '\2"),
        (r"item\.unit \|\| 'pcs'", r"item.unit || getInvoiceText('unitDefault')"),
        (r'無項目數據', lambda m: "' + getInvoiceText('noItems') + '"),
    ]
    
    for pattern, replacement in replacements:
        if callable(replacement):
            content = re.sub(pattern, replacement, content)
        else:
            content = re.sub(pattern, replacement, content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 已添加多语言支持到 {file_path}")
    return True

def main():
    print("🌏 添加日文和韩文支持...\n")
    
    print("=" * 60)
    print("为 document-detail-new.js 添加多语言支持")
    print("=" * 60)
    
    add_multilingual_support()
    
    print("\n" + "=" * 60)
    print("✅ 完成！")
    print("=" * 60)
    print("\n📋 添加的语言支持：")
    print("• ✅ 英文 (en)")
    print("• ✅ 日文 (ja)")
    print("• ✅ 韩文 (ko)")
    print("• ✅ 中文 (zh-TW)")
    
    print("\n🔍 测试步骤：")
    print("1. 清除浏览器缓存")
    print("2. 访问日文版: /jp/document-detail.html")
    print("3. 访问韩文版: /kr/document-detail.html")
    print("4. 确认 Invoice 详情显示对应语言")

if __name__ == '__main__':
    main()

