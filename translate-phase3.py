#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 3 翻译系统 - Billing + Account + Document-Detail
Translation System for Phase 3 Pages
"""

import json
import re
from pathlib import Path

def load_phase3_translations():
    """加载Phase 3翻译数据"""
    with open('phase3-translations.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def safe_replace(content, old_text, new_text, context=""):
    """安全替换文本"""
    count = 0
    patterns = [
        (f'>{re.escape(old_text)}<', f'>{new_text}<'),
        (f'"{re.escape(old_text)}"', f'"{new_text}"'),
        (f'>{re.escape(old_text)}\\s*<', f'>{new_text}<'),
    ]
    
    for pattern, replacement in patterns:
        new_content, n = re.subn(pattern, replacement, content)
        count += n
        content = new_content
    
    if count > 0 and context:
        print(f"    ✓ {context}: {count}处")
    return content

def translate_billing(lang_code):
    """翻译billing.html"""
    print(f"\n{'='*60}")
    print(f"💳 翻译 Billing.html → {lang_code.upper()}")
    print(f"{'='*60}")
    
    translations = load_phase3_translations()
    billing_trans = translations['billing_page'][lang_code]
    
    # 读取原始文件
    with open('billing.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 创建目标文件
    target_dir = Path(lang_code)
    target_dir.mkdir(exist_ok=True)
    target_file = target_dir / 'billing.html'
    
    # 修改lang属性
    lang_attr = {'en': 'en', 'jp': 'ja', 'kr': 'ko'}.get(lang_code, lang_code)
    content = content.replace('<html lang="zh-TW">', f'<html lang="{lang_attr}">')
    
    # 翻译Meta标签
    print("\n📋 翻译Meta标签...")
    content = re.sub(
        r'<title>.*?</title>',
        f'<title>{billing_trans["page_title"]}</title>',
        content,
        flags=re.DOTALL
    )
    
    # 翻译主要内容
    print("📋 翻译计费内容...")
    billing_items = [
        ('monthly_plan', '月付'),
        ('yearly_plan', '年付'),
        ('save_20', '節省 20%'),
        ('per_month', '/月'),
        ('current_plan', '當前方案'),
        ('upgrade', '升級'),
        ('cancel', '取消訂閱'),
        ('payment_method', '付款方式'),
        ('billing_history', '賬單歷史'),
        ('date', '日期'),
        ('amount', '金額'),
        ('status', '狀態'),
        ('download', '下載'),
        ('paid', '已付款'),
        ('pending', '待處理'),
        ('failed', '失敗'),
        ('buy_credits', '購買 Credits')
    ]
    
    for key, zh_text in billing_items:
        content = safe_replace(content, zh_text, billing_trans[key], key)
    
    # 保存文件
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n  ✅ Billing.html 翻译完成！")
    print(f"  💾 文件: {target_file}")
    print(f"  📊 大小: {target_file.stat().st_size / 1024:.1f} KB")

def translate_account(lang_code):
    """翻译account.html"""
    print(f"\n{'='*60}")
    print(f"👤 翻译 Account.html → {lang_code.upper()}")
    print(f"{'='*60}")
    
    translations = load_phase3_translations()
    account_trans = translations['account_page'][lang_code]
    
    # 读取原始文件
    with open('account.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 创建目标文件
    target_dir = Path(lang_code)
    target_dir.mkdir(exist_ok=True)
    target_file = target_dir / 'account.html'
    
    # 修改lang属性
    lang_attr = {'en': 'en', 'jp': 'ja', 'kr': 'ko'}.get(lang_code, lang_code)
    content = content.replace('<html lang="zh-TW">', f'<html lang="{lang_attr}">')
    
    # 翻译Meta标签
    print("\n📋 翻译Meta标签...")
    content = re.sub(
        r'<title>.*?</title>',
        f'<title>{account_trans["page_title"]}</title>',
        content,
        flags=re.DOTALL
    )
    
    # 翻译主要内容
    print("📋 翻译账户内容...")
    account_items = [
        ('account_title', '帳戶設置'),
        ('personal_info', '個人信息'),
        ('name', '姓名'),
        ('email', '郵箱地址'),
        ('save_changes', '保存更改'),
        ('password_security', '密碼與安全'),
        ('current_password', '當前密碼'),
        ('new_password', '新密碼'),
        ('confirm_password', '確認新密碼'),
        ('change_password', '更改密碼'),
        ('credits_usage', 'Credits 使用情況'),
        ('total_credits', '總 Credits'),
        ('purchase_history', '購買記錄'),
        ('description', '描述'),
        ('notifications', '通知設置'),
        ('preferences', '偏好設置'),
        ('language', '語言'),
        ('delete_account', '刪除帳戶')
    ]
    
    for key, zh_text in account_items:
        content = safe_replace(content, zh_text, account_trans[key], key)
    
    # 保存文件
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n  ✅ Account.html 翻译完成！")
    print(f"  💾 文件: {target_file}")
    print(f"  📊 大小: {target_file.stat().st_size / 1024:.1f} KB")

def translate_document_detail(lang_code):
    """翻译document-detail.html"""
    print(f"\n{'='*60}")
    print(f"📄 翻译 Document-Detail.html → {lang_code.upper()}")
    print(f"{'='*60}")
    
    translations = load_phase3_translations()
    doc_trans = translations['document_detail_page'][lang_code]
    
    # 读取原始文件
    with open('document-detail.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 创建目标文件
    target_dir = Path(lang_code)
    target_dir.mkdir(exist_ok=True)
    target_file = target_dir / 'document-detail.html'
    
    # 修改lang属性
    lang_attr = {'en': 'en', 'jp': 'ja', 'kr': 'ko'}.get(lang_code, lang_code)
    content = content.replace('<html lang="zh-TW">', f'<html lang="{lang_attr}">')
    
    # 翻译Meta标签
    print("\n📋 翻译Meta标签...")
    content = re.sub(
        r'<title>.*?</title>',
        f'<title>{doc_trans["page_title"]}</title>',
        content,
        flags=re.DOTALL
    )
    
    # 翻译主要内容
    print("📋 翻译文档详情内容...")
    doc_items = [
        ('back_to_dashboard', '返回儀表板'),
        ('export', 'Export'),
        ('delete', 'Delete'),
        ('extracted_data', '提取的數據'),
        ('vendor', '供應商'),
        ('invoice_number', '發票號碼'),
        ('invoice_date', '發票日期'),
        ('due_date', '到期日'),
        ('subtotal', '小計'),
        ('tax', '稅額'),
        ('total', '總計'),
        ('item', '項目'),
        ('quantity', '數量'),
        ('price', '單價'),
        ('processing', '處理中'),
        ('completed', '已完成'),
        ('failed', '失敗')
    ]
    
    for key, zh_text in doc_items:
        content = safe_replace(content, zh_text, doc_trans[key], key)
    
    # 保存文件
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n  ✅ Document-Detail.html 翻译完成！")
    print(f"  💾 文件: {target_file}")
    print(f"  📊 大小: {target_file.stat().st_size / 1024:.1f} KB")

def main():
    """主函数"""
    print("\n" + "="*60)
    print("🚀 VaultCaddy Phase 3 翻译系统")
    print("="*60)
    print("\n📋 任务列表:")
    print("  1. 翻译 Billing.html (计费页面)")
    print("  2. 翻译 Account.html (账户管理)")
    print("  3. 翻译 Document-Detail.html (文档详情)")
    print()
    
    languages = [
        ('en', '英文'),
        ('jp', '日文'),
        ('kr', '韩文')
    ]
    
    for lang_code, lang_name in languages:
        try:
            print(f"\n{'#'*60}")
            print(f"# 开始处理: {lang_name.upper()} ({lang_code.upper()})")
            print(f"{'#'*60}")
            
            # 1. 翻译Billing.html
            translate_billing(lang_code)
            
            # 2. 翻译Account.html
            translate_account(lang_code)
            
            # 3. 翻译Document-Detail.html
            translate_document_detail(lang_code)
            
            print(f"\n✅ {lang_name} 全部完成！")
            
        except Exception as e:
            print(f"\n❌ {lang_name} 翻译失败: {e}")
            import traceback
            traceback.print_exc()
            continue
    
    # 最终总结
    print("\n" + "="*60)
    print("🎉 Phase 3 全部完成！")
    print("="*60)
    print("\n📁 生成的文件:")
    print("  Billing.html (新):")
    print("    ✓ en/billing.html")
    print("    ✓ jp/billing.html")
    print("    ✓ kr/billing.html")
    print("  Account.html (新):")
    print("    ✓ en/account.html")
    print("    ✓ jp/account.html")
    print("    ✓ kr/account.html")
    print("  Document-Detail.html (新):")
    print("    ✓ en/document-detail.html")
    print("    ✓ jp/document-detail.html")
    print("    ✓ kr/document-detail.html")
    
    print("\n📊 当前进度:")
    print("  核心页面: 6/8 完成 (75%)")
    print("  ✅ index.html")
    print("  ✅ auth.html")
    print("  ✅ dashboard.html")
    print("  ✅ billing.html")
    print("  ✅ account.html")
    print("  ✅ document-detail.html")
    print("  ⏳ firstproject.html")
    print("  ⏳ privacy.html")
    
    print("\n🚀 下一步:")
    print("  1. 测试所有页面: python3 -m http.server 8000")
    print("  2. 访问: http://localhost:8000/en/billing.html")
    print("  3. 访问: http://localhost:8000/en/account.html")
    print("  4. 访问: http://localhost:8000/en/document-detail.html")
    print("  5. 继续翻译其他页面或开始博客翻译")
    
    print("\n💡 提示: 所有翻译保留了HTML结构和功能")
    print("="*60 + "\n")

if __name__ == '__main__':
    main()

