#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复translations.js中的语言检测逻辑

问题：
1. 默认语言是zh-TW（繁体中文），导致英文/日文/韩文页面显示中文
2. 应该优先使用页面路径（/en/, /jp/, /kr/）来决定语言

解决方案：
1. 修改getLanguageFromPath()，优先使用页面路径
2. 修改默认语言逻辑
3. 确保不会错误地应用翻译覆盖HTML内容
"""

import re
import os
from datetime import datetime

def backup_file(filepath):
    """创建备份"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = f"{filepath}.backup_lang_detect_{timestamp}"
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ 备份: {backup_path}")
    return True

def fix_translations_js():
    """修复translations.js的语言检测逻辑"""
    
    filepath = 'translations.js'
    
    if not os.path.exists(filepath):
        print(f"❌ 文件不存在: {filepath}")
        return False
    
    print(f"\n🔧 修复: {filepath}")
    backup_file(filepath)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # 修复1：getLanguageFromPath方法 - 优先使用页面路径
    old_get_lang = r'''getLanguageFromPath\(\) \{
        // 優先使用URL路徑判斷語言
        const pathname = window\.location\.pathname;
        if \(pathname\.includes\('/en/'\)\) return 'en';
        if \(pathname\.includes\('/jp/'\)\) return 'ja';
        if \(pathname\.includes\('/kr/'\)\) return 'ko';
        
        // 檢測瀏覽器語言
        const browserLang = navigator\.language \|\| navigator\.userLanguage \|\| 'zh-TW';
        
        // 語言映射表
        const languageMap = \{
            'zh-TW': 'zh-TW',
            'zh-HK': 'zh-TW',
            'zh': 'zh-TW',
            'zh-CN': 'zh-CN',
            'en': 'en',
            'en-US': 'en',
            'en-GB': 'en',
            'ja': 'ja',
            'ja-JP': 'ja',
            'ko': 'ko',
            'ko-KR': 'ko',
            'en-CA': 'en',
            'en-AU': 'en'
        \};
        
        // 精確匹配
        if \(languageMap\[browserLang\]\) \{
            console\.log\('🌐 使用瀏覽器語言:', browserLang, '→', languageMap\[browserLang\]\);
            return languageMap\[browserLang\];
        \}
        
        // 模糊匹配（只匹配語言代碼前兩位）
        const langCode = browserLang\.substring\(0, 2\);
        if \(languageMap\[langCode\]\) \{
            console\.log\('🌐 使用瀏覽器語言代碼:', langCode, '→', languageMap\[langCode\]\);
            return languageMap\[langCode\];
        \}
        
        // 默認返回繁體中文
        console\.log\('🌐 使用默認語言: zh-TW'\);
        return 'zh-TW';
    \}'''
    
    new_get_lang = '''getLanguageFromPath() {
        // ✅ 第一優先：使用URL路徑判斷語言
        const pathname = window.location.pathname;
        if (pathname.includes('/en/')) {
            console.log('🌐 從路徑檢測到語言: en');
            return 'en';
        }
        if (pathname.includes('/jp/')) {
            console.log('🌐 從路徑檢測到語言: ja');
            return 'ja';
        }
        if (pathname.includes('/kr/')) {
            console.log('🌐 從路徑檢測到語言: ko');
            return 'ko';
        }
        
        // ✅ 第二優先：檢測瀏覽器語言
        const browserLang = navigator.language || navigator.userLanguage || 'zh-TW';
        
        // 語言映射表
        const languageMap = {
            'zh-TW': 'zh-TW',
            'zh-HK': 'zh-TW',
            'zh': 'zh-TW',
            'zh-CN': 'zh-CN',
            'en': 'en',
            'en-US': 'en',
            'en-GB': 'en',
            'ja': 'ja',
            'ja-JP': 'ja',
            'ko': 'ko',
            'ko-KR': 'ko',
            'en-CA': 'en',
            'en-AU': 'en'
        };
        
        // 精確匹配
        if (languageMap[browserLang]) {
            console.log('🌐 使用瀏覽器語言:', browserLang, '→', languageMap[browserLang]);
            return languageMap[browserLang];
        }
        
        // 模糊匹配（只匹配語言代碼前兩位）
        const langCode = browserLang.substring(0, 2);
        if (languageMap[langCode]) {
            console.log('🌐 使用瀏覽器語言代碼:', langCode, '→', languageMap[langCode]);
            return languageMap[langCode];
        }
        
        // ✅ 最終默認：如果都檢測不到，根據根目錄還是子目錄返回不同默認語言
        if (pathname === '/' || pathname.includes('index.html')) {
            console.log('🌐 根目錄，使用默認語言: zh-TW');
            return 'zh-TW';
        } else {
            // 如果在子目錄但無法識別，使用英文
            console.log('🌐 子目錄，使用默認語言: en');
            return 'en';
        }
    }'''
    
    if re.search(old_get_lang, content, re.DOTALL):
        content = re.sub(old_get_lang, new_get_lang, content, flags=re.DOTALL)
        print("✅ 修復了 getLanguageFromPath() 方法")
    else:
        print("⚠️  未找到 getLanguageFromPath() 方法的完整匹配")
        # 尝试部分修复
        content = re.sub(
            r"// 默認返回繁體中文\s+console\.log\('🌐 使用默認語言: zh-TW'\);\s+return 'zh-TW';",
            "// ✅ 最終默認：根據路徑決定\n        if (pathname === '/' || pathname.includes('index.html')) {\n            console.log('🌐 根目錄，使用默認語言: zh-TW');\n            return 'zh-TW';\n        } else {\n            console.log('🌐 子目錄，使用默認語言: en');\n            return 'en';\n        }",
            content
        )
        print("✅ 部分修復了默認語言邏輯")
    
    # 修復2：init方法 - 確保不會錯誤地覆蓋內容
    init_fix = r'''// 只有當檢測到的語言與當前頁面語言不同時，才需要應用翻譯
        // 大多數情況下，HTML已經包含了正確的語言內容，無需覆蓋
        const pathname = window\.location\.pathname;
        const pageLanguage = pathname\.includes\('/en/'\) \? 'en' 
                           : pathname\.includes\('/jp/'\) \? 'ja'
                           : pathname\.includes\('/kr/'\) \? 'ko'
                           : 'zh-TW';
        
        if \(this\.currentLanguage === pageLanguage\) \{
            console\.log\('✅ 頁面語言與檢測語言一致，無需應用翻譯'\);
            // 不執行 loadLanguage，保留HTML原始內容
        \} else \{
            console\.log\('⚠️ 頁面語言與檢測語言不一致，應用翻譯:', pageLanguage, '→', this\.currentLanguage\);
            this\.loadLanguage\(this\.currentLanguage\);
        \}'''
    
    init_new = '''// ✅ 頁面語言應該始終與路徑一致
        // 如果當前語言與頁面路徑不一致，優先使用頁面路徑的語言
        const pathname = window.location.pathname;
        const pageLanguage = pathname.includes('/en/') ? 'en' 
                           : pathname.includes('/jp/') ? 'ja'
                           : pathname.includes('/kr/') ? 'ko'
                           : 'zh-TW';
        
        if (this.currentLanguage !== pageLanguage) {
            console.log('⚠️ 修正語言:', this.currentLanguage, '→', pageLanguage);
            this.currentLanguage = pageLanguage;
        }
        
        console.log('✅ 頁面語言已確認:', this.currentLanguage);
        // 不執行 loadLanguage，保留HTML原始內容（HTML已經是正確的語言）'''
    
    content = re.sub(init_fix, init_new, content, flags=re.DOTALL)
    print("✅ 修復了 init() 方法")
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"\n✅ {filepath} 修復完成！")
        return True
    else:
        print(f"\nℹ️  {filepath} 沒有需要修復的內容")
        return False

def main():
    """主函數"""
    print("=" * 70)
    print("🔧 語言檢測邏輯修復工具")
    print("=" * 70)
    print("\n問題: 英文/日文/韓文頁面顯示中文內容")
    print("原因: translations.js默認語言是zh-TW")
    print("解決: 優先使用頁面路徑判斷語言\n")
    
    if fix_translations_js():
        print("\n" + "=" * 70)
        print("🎉 修復完成！")
        print("=" * 70)
        print("\n📝 下一步:")
        print("1. 強制刷新所有頁面 (Shift + Command + R)")
        print("2. 測試英文版: /en/document-detail.html")
        print("3. 測試日文版: /jp/document-detail.html")
        print("4. 測試韓文版: /kr/document-detail.html")
        print("\n✅ 應該看到:")
        print("   - 英文頁面顯示英文")
        print("   - 日文頁面顯示日文")
        print("   - 韓文頁面顯示韓文")
        return True
    else:
        print("\n⚠️  修復未執行或部分失敗")
        return False

if __name__ == '__main__':
    main()

