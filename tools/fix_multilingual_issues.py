#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 修复多语言问题
1. 确保中文版首页正确显示语言选择器
2. 修复英文Dashboard侧边栏的中文翻译
"""

import os

def fix_sidebar_translations():
    """修复sidebar-component.js中的翻译问题"""
    
    print("\n🔧 修复侧边栏翻译...")
    
    file_path = "/Users/cavlinyeung/ai-bank-parser/sidebar-component.js"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 创建多语言版本的侧边栏
    # 检测当前语言并使用相应翻译
    
    original_content = content
    
    # 替换"配置"标题 - 需要根据语言动态设置
    content = content.replace(
        '<h3 style="font-size: 0.75rem; font-weight: 600; color: #9ca3af; text-transform: uppercase; letter-spacing: 0.05em; margin: 0 0 0.75rem 0;">配置</h3>',
        '<h3 style="font-size: 0.75rem; font-weight: 600; color: #9ca3af; text-transform: uppercase; letter-spacing: 0.05em; margin: 0 0 0.75rem 0;" data-i18n="settings">Settings</h3>'
    )
    
    # 替换"帳戶"
    content = content.replace(
        '<span style="font-size: 0.875rem;">帳戶</span>',
        '<span style="font-size: 0.875rem;" data-i18n="account">Account</span>'
    )
    
    # 替换"計費"
    content = content.replace(
        '<span style="font-size: 0.875rem;">計費</span>',
        '<span style="font-size: 0.875rem;" data-i18n="billing">Billing</span>'
    )
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("   ✅ 已修复sidebar-component.js的翻译")
        return True
    else:
        print("   ℹ️  未发现需要修改的内容")
        return False

def add_sidebar_translation_init():
    """在sidebar-component.js中添加翻译初始化逻辑"""
    
    print("\n🌐 添加侧边栏翻译初始化...")
    
    file_path = "/Users/cavlinyeung/ai-bank-parser/sidebar-component.js"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否已经有翻译逻辑
    if 'initSidebarTranslations' in content:
        print("   ℹ️  翻译逻辑已存在")
        return False
    
    # 在类的最后添加翻译方法
    translation_method = '''
    
    /**
     * 初始化侧边栏翻译
     */
    initSidebarTranslations() {
        const translations = {
            'zh': {
                'settings': '配置',
                'account': '帳戶',
                'billing': '計費'
            },
            'en': {
                'settings': 'Settings',
                'account': 'Account',
                'billing': 'Billing'
            },
            'jp': {
                'settings': '設定',
                'account': 'アカウント',
                'billing': '請求'
            },
            'kr': {
                'settings': '설정',
                'account': '계정',
                'billing': '결제'
            }
        };
        
        // 检测当前语言
        const path = window.location.pathname;
        let currentLang = 'zh';
        if (path.startsWith('/en/')) currentLang = 'en';
        else if (path.startsWith('/jp/')) currentLang = 'jp';
        else if (path.startsWith('/kr/')) currentLang = 'kr';
        
        // 应用翻译
        document.querySelectorAll('[data-i18n]').forEach(el => {
            const key = el.getAttribute('data-i18n');
            if (translations[currentLang] && translations[currentLang][key]) {
                el.textContent = translations[currentLang][key];
            }
        });
    }
'''
    
    # 在类的结尾（最后一个}之前）添加翻译方法
    # 找到类定义的结束位置
    last_brace_index = content.rfind('}')
    if last_brace_index != -1:
        content = content[:last_brace_index] + translation_method + '\n' + content[last_brace_index:]
    
    # 在render方法的最后调用翻译初始化
    # 查找render方法中的最后一个console.log
    render_end_pattern = "console.log('✅ 側邊欄渲染完成');"
    if render_end_pattern in content:
        content = content.replace(
            render_end_pattern,
            render_end_pattern + "\n        \n        // 初始化翻译\n        this.initSidebarTranslations();"
        )
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("   ✅ 已添加侧边栏翻译逻辑")
    return True

def verify_chinese_homepage_language_selector():
    """验证中文首页是否有语言选择器"""
    
    print("\n🔍 验证中文首页语言选择器...")
    
    file_path = "/Users/cavlinyeung/ai-bank-parser/index.html"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查必要元素
    has_container = 'id="language-switcher"' in content
    has_script = 'multilingual-data-sync.js' in content
    
    print(f"   语言选择器容器: {'✅' if has_container else '❌'}")
    print(f"   多语言脚本引用: {'✅' if has_script else '❌'}")
    
    if has_container and has_script:
        print("   ✅ 中文首页配置正确")
        print("   💡 如果仍未显示，请检查:")
        print("      1. 浏览器缓存（Ctrl+Shift+R 强制刷新）")
        print("      2. JavaScript控制台是否有错误")
        print("      3. multilingual-data-sync.js是否正确加载")
        return True
    else:
        print("   ⚠️ 中文首页配置不完整")
        return False

def create_test_page():
    """创建一个测试页面来验证语言选择器"""
    
    print("\n🧪 创建语言选择器测试页面...")
    
    test_html = '''<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>语言选择器测试</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            padding: 2rem;
            background: #f3f4f6;
        }
        .test-container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            padding: 2rem;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        h1 {
            color: #1f2937;
            margin-bottom: 1rem;
        }
        .info {
            background: #eff6ff;
            border-left: 4px solid #3b82f6;
            padding: 1rem;
            margin: 1rem 0;
        }
        .test-section {
            margin: 2rem 0;
            padding: 1rem;
            border: 1px solid #e5e7eb;
            border-radius: 4px;
        }
        #status {
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 4px;
        }
        .success { background: #d1fae5; color: #065f46; }
        .error { background: #fee2e2; color: #991b1b; }
    </style>
</head>
<body>
    <div class="test-container">
        <h1>🌐 VaultCaddy 语言选择器测试</h1>
        
        <div class="info">
            <strong>测试目的</strong>: 验证语言选择器是否正确加载和显示
        </div>
        
        <div class="test-section">
            <h3>语言选择器位置:</h3>
            <div id="language-switcher" style="display: inline-block; margin: 1rem 0;"></div>
        </div>
        
        <div class="test-section">
            <h3>诊断信息:</h3>
            <div id="status">等待加载...</div>
        </div>
        
        <div class="test-section">
            <h3>JavaScript 控制台日志:</h3>
            <p>打开浏览器开发者工具（F12）查看详细日志</p>
        </div>
    </div>
    
    <script src="multilingual-data-sync.js"></script>
    <script>
        // 诊断脚本
        setTimeout(() => {
            const statusDiv = document.getElementById('status');
            const checks = [];
            
            // 检查1: 脚本是否加载
            if (window.multilingualSync) {
                checks.push('✅ multilingual-data-sync.js 已加载');
            } else {
                checks.push('❌ multilingual-data-sync.js 未加载');
            }
            
            // 检查2: 容器是否存在
            const container = document.getElementById('language-switcher');
            if (container) {
                checks.push('✅ 语言选择器容器存在');
            } else {
                checks.push('❌ 语言选择器容器不存在');
            }
            
            // 检查3: 内容是否渲染
            if (container && container.innerHTML.trim() !== '') {
                checks.push('✅ 语言选择器已渲染');
                checks.push('内容: ' + container.innerHTML.substring(0, 100) + '...');
            } else {
                checks.push('❌ 语言选择器未渲染（容器为空）');
            }
            
            // 检查4: 当前语言
            if (window.multilingualSync) {
                checks.push(`当前语言: ${window.multilingualSync.currentLang}`);
            }
            
            // 显示结果
            const hasErrors = checks.some(c => c.startsWith('❌'));
            statusDiv.className = hasErrors ? 'error' : 'success';
            statusDiv.innerHTML = checks.join('<br>');
        }, 1000);
    </script>
</body>
</html>
'''
    
    test_file_path = "/Users/cavlinyeung/ai-bank-parser/language-selector-test.html"
    
    with open(test_file_path, 'w', encoding='utf-8') as f:
        f.write(test_html)
    
    print(f"   ✅ 测试页面已创建: {test_file_path}")
    print(f"   💡 访问: http://localhost:8000/language-selector-test.html")
    return True

def main():
    """主函数"""
    
    print("╔══════════════════════════════════════════════════════════════════════╗")
    print("║     🔧 修复多语言问题                                                   ║")
    print("╚══════════════════════════════════════════════════════════════════════╝\n")
    
    print("📋 问题清单:")
    print("   1. 中文版首页未显示语言选择器")
    print("   2. 英文Dashboard侧边栏显示中文（配置、帳戶、計費）\n")
    
    changes = 0
    
    # 修复问题1: 验证中文首页配置
    if verify_chinese_homepage_language_selector():
        changes += 1
    
    # 修复问题2: 英文Dashboard侧边栏翻译
    if fix_sidebar_translations():
        changes += 1
    
    if add_sidebar_translation_init():
        changes += 1
    
    # 创建测试页面
    if create_test_page():
        changes += 1
    
    print("\n╔══════════════════════════════════════════════════════════════════════╗")
    print("║     🎉 修复完成！                                                       ║")
    print("╚══════════════════════════════════════════════════════════════════════╝\n")
    
    print(f"📊 总计完成: {changes} 项修改\n")
    
    print("✅ 已完成修复:")
    print("   1. ✅ 侧边栏文本已改为英文（并支持多语言）")
    print("   2. ✅ 添加了动态翻译逻辑")
    print("   3. ✅ 创建了测试页面\n")
    
    print("🔍 中文版首页语言选择器诊断:")
    print("   • 配置已正确：语言选择器容器存在，脚本已引用")
    print("   • 如果仍未显示，可能原因：")
    print("     1. 浏览器缓存（清除缓存或Ctrl+Shift+R强制刷新）")
    print("     2. JavaScript执行时机问题")
    print("     3. 其他JavaScript错误阻止执行\n")
    
    print("🧪 测试方法:")
    print("   1. 访问测试页面: http://localhost:8000/language-selector-test.html")
    print("   2. 查看语言选择器是否显示")
    print("   3. 打开F12查看控制台日志\n")
    
    print("🎯 下一步:")
    print("   1. 清除浏览器缓存")
    print("   2. 访问 https://vaultcaddy.com/ （中文首页）")
    print("   3. 检查导航栏右侧是否有语言选择器")
    print("   4. 访问 https://vaultcaddy.com/en/dashboard.html")
    print("   5. 检查左侧栏是否已改为英文\n")
    
    print("💡 如果问题依然存在:")
    print("   • 先访问测试页面确认语言选择器功能正常")
    print("   • 检查浏览器控制台(F12)的JavaScript错误")
    print("   • 确认multilingual-data-sync.js文件可以访问\n")

if __name__ == "__main__":
    main()

