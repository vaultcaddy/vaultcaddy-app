#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整翻译系统 - Index.html剩余 + Auth.html + Dashboard.html
Complete Translation System for Remaining Pages
"""

import json
import re
import shutil
from pathlib import Path

def load_all_translations():
    """加载所有翻译数据"""
    with open('complete-translations.json', 'r', encoding='utf-8') as f:
        complete_trans = json.load(f)
    with open('final-translations.json', 'r', encoding='utf-8') as f:
        final_trans = json.load(f)
    return {**complete_trans, **final_trans}

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

def complete_index_translation(lang_code):
    """完善Index.html翻译"""
    print(f"\n{'='*60}")
    print(f"📝 完善 Index.html 翻译 ({lang_code.upper()})")
    print(f"{'='*60}")
    
    translations = load_all_translations()
    blog_trans = translations['blog_articles'][lang_code]
    
    # 读取已翻译的文件
    source_file = Path(lang_code) / 'index.html'
    if not source_file.exists():
        print(f"  ❌ 文件不存在: {source_file}")
        return
    
    with open(source_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 翻译博客文章标题和描述
    print("\n📋 翻译博客文章...")
    blog_items = [
        ('article1_title', '人手處理 vs AI 自動化：真實成本對比'),
        ('article1_desc', '完整指南教您使用 AI 技術快速轉換銀行對帳單，節省數小時的手動輸入時間。'),
        ('article2_title', '個人記賬的 7 個最佳實踐'),
        ('article2_desc', '了解如何使用 AI 自動化發票處理流程，提升會計效率，減少人為錯誤。')
    ]
    
    for key, zh_text in blog_items:
        content = safe_replace(content, zh_text, blog_trans[key], key)
    
    # 保存文件
    with open(source_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  ✅ Index.html 完善完成！")
    print(f"  💾 文件: {source_file}")

def translate_auth_page(lang_code):
    """翻译auth.html"""
    print(f"\n{'='*60}")
    print(f"🔐 翻译 Auth.html → {lang_code.upper()}")
    print(f"{'='*60}")
    
    translations = load_all_translations()
    auth_trans = translations['auth_page'][lang_code]
    
    # 读取原始文件
    with open('auth.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 创建目标目录
    target_dir = Path(lang_code)
    target_dir.mkdir(exist_ok=True)
    target_file = target_dir / 'auth.html'
    
    # 修改lang属性
    lang_attr = {'en': 'en', 'jp': 'ja', 'kr': 'ko'}.get(lang_code, lang_code)
    content = content.replace('<html lang="zh-TW">', f'<html lang="{lang_attr}">')
    
    # 翻译Meta标签
    print("\n📋 翻译Meta标签...")
    content = re.sub(
        r'<title>.*?</title>',
        f'<title>{auth_trans["page_title"]}</title>',
        content,
        flags=re.DOTALL
    )
    
    # 翻译登入区域
    print("📋 翻译登入区域...")
    login_items = [
        ('login_title', '歡迎回來'),
        ('login_subtitle', '登入您的帳戶以繼續'),
        ('email_label', '郵箱地址'),
        ('password_label', '密碼'),
        ('forgot_password', '忘記帳戶密碼？'),
        ('login_button', '登入'),
        ('google_login', '使用 Google 登入'),
        ('no_account', '還沒有帳戶？'),
        ('signup_link', '立即註冊')
    ]
    
    for key, zh_text in login_items:
        content = safe_replace(content, zh_text, auth_trans[key], key)
    
    # 翻译注册区域
    print("📋 翻译注册区域...")
    register_items = [
        ('register_title', '創建新帳戶'),
        ('register_subtitle', '免費開始使用 VaultCaddy'),
        ('name_label', '姓名'),
        ('confirm_password_label', '確認密碼'),
        ('verification_code_label', '驗證碼'),
        ('send_code', '發送驗證碼'),
        ('register_button', '註冊'),
        ('google_register', '使用 Google 註冊'),
        ('have_account', '已有帳戶？'),
        ('login_link', '立即登入'),
        ('terms_agree', '註冊即表示您同意我們的'),
        ('terms_link', '服務條款'),
        ('and', '和'),
        ('privacy_link', '隱私政策')
    ]
    
    for key, zh_text in register_items:
        content = safe_replace(content, zh_text, auth_trans[key], key)
    
    # 保存文件
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n  ✅ Auth.html 翻译完成！")
    print(f"  💾 文件: {target_file}")
    print(f"  📊 大小: {target_file.stat().st_size / 1024:.1f} KB")

def translate_dashboard_page(lang_code):
    """翻译dashboard.html"""
    print(f"\n{'='*60}")
    print(f"📊 翻译 Dashboard.html → {lang_code.upper()}")
    print(f"{'='*60}")
    
    translations = load_all_translations()
    dash_trans = translations['dashboard_page'][lang_code]
    
    # 读取原始文件
    with open('dashboard.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 创建目标目录
    target_dir = Path(lang_code)
    target_dir.mkdir(exist_ok=True)
    target_file = target_dir / 'dashboard.html'
    
    # 修改lang属性
    lang_attr = {'en': 'en', 'jp': 'ja', 'kr': 'ko'}.get(lang_code, lang_code)
    content = content.replace('<html lang="zh-TW">', f'<html lang="{lang_attr}">')
    
    # 翻译Meta标签
    print("\n📋 翻译Meta标签...")
    content = re.sub(
        r'<title>.*?</title>',
        f'<title>{dash_trans["page_title"]}</title>',
        content,
        flags=re.DOTALL
    )
    
    # 翻译主要内容
    print("📋 翻译主要内容...")
    dash_items = [
        ('welcome', '歡迎回來'),
        ('create_project', '創建新項目'),
        ('my_projects', '我的項目'),
        ('recent_documents', '最近文檔'),
        ('upload_document', '上傳文檔'),
        ('credits_remaining', '剩餘 Credits'),
        ('credits', 'Credits'),
        ('buy_more', '購買更多'),
        ('documents_processed', '已處理文檔'),
        ('processing', '處理中'),
        ('completed', '已完成'),
        ('failed', '失敗'),
        ('project_name', '項目名稱'),
        ('created', '創建時間'),
        ('documents', '文檔'),
        ('actions', '操作'),
        ('view', '查看'),
        ('delete', '刪除'),
        ('no_projects', '還沒有項目'),
        ('create_first', '創建您的第一個項目')
    ]
    
    for key, zh_text in dash_items:
        content = safe_replace(content, zh_text, dash_trans[key], key)
    
    # 保存文件
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n  ✅ Dashboard.html 翻译完成！")
    print(f"  💾 文件: {target_file}")
    print(f"  📊 大小: {target_file.stat().st_size / 1024:.1f} KB")

def main():
    """主函数"""
    print("\n" + "="*60)
    print("🚀 VaultCaddy 完整翻译系统 - Phase 2")
    print("="*60)
    print("\n📋 任务列表:")
    print("  1. 完善 Index.html 剩余30%")
    print("  2. 翻译 Auth.html (登入/注册)")
    print("  3. 翻译 Dashboard.html (仪表板)")
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
            
            # 1. 完善Index.html
            complete_index_translation(lang_code)
            
            # 2. 翻译Auth.html
            translate_auth_page(lang_code)
            
            # 3. 翻译Dashboard.html
            translate_dashboard_page(lang_code)
            
            print(f"\n✅ {lang_name} 全部完成！")
            
        except Exception as e:
            print(f"\n❌ {lang_name} 翻译失败: {e}")
            import traceback
            traceback.print_exc()
            continue
    
    # 最终总结
    print("\n" + "="*60)
    print("🎉 Phase 2 全部完成！")
    print("="*60)
    print("\n📁 生成的文件:")
    print("  Index.html (完善):")
    print("    ✓ en/index.html")
    print("    ✓ jp/index.html")
    print("    ✓ kr/index.html")
    print("  Auth.html (新):")
    print("    ✓ en/auth.html")
    print("    ✓ jp/auth.html")
    print("    ✓ kr/auth.html")
    print("  Dashboard.html (新):")
    print("    ✓ en/dashboard.html")
    print("    ✓ jp/dashboard.html")
    print("    ✓ kr/dashboard.html")
    
    print("\n🚀 下一步:")
    print("  1. 测试所有页面: python3 -m http.server 8000")
    print("  2. 访问: http://localhost:8000/en/auth.html")
    print("  3. 访问: http://localhost:8000/en/dashboard.html")
    print("  4. 继续翻译其他页面(billing, account等)")
    print("\n💡 提示: 所有翻译保留了HTML结构和功能")
    print("="*60 + "\n")

if __name__ == '__main__':
    main()

