#!/usr/bin/env python3
"""
修复 firstproject.html 中的重复内容区域问题

作用：
1. 检测并移除重复的 <main class="main-content"> 容器
2. 添加防护 JavaScript 代码防止未来出现重复
3. 备份原文件

使用方法：
python3 fix_duplicate_content.py
"""

import re
import shutil
from datetime import datetime

def fix_duplicate_content():
    input_file = 'firstproject.html'
    backup_file = f'{input_file}.backup.{datetime.now().strftime("%Y%m%d_%H%M%S")}'
    
    print(f'📁 读取文件: {input_file}')
    
    # 备份原文件
    shutil.copy2(input_file, backup_file)
    print(f'✅ 已备份到: {backup_file}')
    
    # 读取文件内容
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检测重复的 main-content
    main_content_pattern = r'<main[^>]*class="main-content"[^>]*>.*?</main>'
    matches = re.findall(main_content_pattern, content, re.DOTALL)
    
    print(f'\n🔍 检测到 {len(matches)} 个 <main class="main-content"> 容器')
    
    if len(matches) > 1:
        print(f'⚠️  发现重复内容！正在修复...')
        
        # 策略：只保留第一个 main-content
        # 为了安全起见，我们添加 CSS 来隐藏重复的内容
        
        # 在 </head> 之前添加修复 CSS
        fix_css = '''
    <!-- 修复重复内容区域 -->
    <style>
        /* 隐藏重复的主内容区域 */
        .main-content:not(:first-of-type) {
            display: none !important;
        }
        
        /* 确保只有一个主内容区域可见 */
        body > .main-content ~ .main-content,
        .dashboard-container > .main-content ~ .main-content {
            display: none !important;
        }
    </style>
'''
        
        if fix_css.strip() not in content:
            content = content.replace('</head>', f'{fix_css}</head>')
            print('✅ 已添加修复 CSS')
        
        # 添加防护 JavaScript
        fix_js = '''
        // 防止重复内容区域
        (function() {
            console.log('🔍 检查重复内容区域...');
            const mainContents = document.querySelectorAll('.main-content');
            if (mainContents.length > 1) {
                console.warn('⚠️ 检测到', mainContents.length, '个主内容区域，正在清理...');
                for (let i = 1; i < mainContents.length; i++) {
                    console.log('   删除重复的内容区域', i);
                    mainContents[i].remove();
                }
                console.log('✅ 已清理重复的主内容区域');
            } else {
                console.log('✅ 内容区域正常，只有 1 个');
            }
        })();
'''
        
        # 在 DOMContentLoaded 之后添加防护代码
        if "document.addEventListener('DOMContentLoaded'" in content and fix_js.strip() not in content:
            # 找到第一个 DOMContentLoaded
            dom_ready_pattern = r"(document\.addEventListener\('DOMContentLoaded',\s*function\(\)\s*\{)"
            content = re.sub(
                dom_ready_pattern,
                r"\1" + fix_js,
                content,
                count=1
            )
            print('✅ 已添加防护 JavaScript')
    
    # 写回文件
    with open(input_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f'\n✅ 修复完成！')
    print(f'   - 原文件: {input_file}')
    print(f'   - 备份文件: {backup_file}')
    print(f'\n📝 请刷新浏览器查看效果')

if __name__ == '__main__':
    try:
        fix_duplicate_content()
    except Exception as e:
        print(f'\n❌ 错误: {e}')
        import traceback
        traceback.print_exc()

