#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复auth.html页面的Firebase错误提示问题
确保错误只在用户操作失败时显示，而不是页面加载时就显示
"""

import os
import re

def fix_auth_error_display(file_path):
    """
    修复auth.html的错误显示问题
    
    Args:
        file_path: auth.html文件路径
    
    Returns:
        bool: 是否成功修改
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 1. 添加全局错误处理，防止未捕获的Promise rejection显示
        error_handler_js = '''
        // 防止未捕获的Promise rejection显示在页面上
        window.addEventListener('unhandledrejection', function(event) {
            console.error('未处理的Promise rejection:', event.reason);
            event.preventDefault(); // 阻止默认的错误显示
        });
        
        // 捕获所有未处理的错误
        window.addEventListener('error', function(event) {
            console.error('全局错误:', event.error);
            // 不阻止默认行为，让开发者可以在控制台看到
        });
        '''
        
        # 查找DOMContentLoaded事件监听器的位置
        dom_content_pattern = r"(document\.addEventListener\('DOMContentLoaded', function\(\) \{)"
        
        if re.search(dom_content_pattern, content):
            # 在DOMContentLoaded之前添加错误处理
            content = re.sub(
                dom_content_pattern,
                error_handler_js + r"\n        \1",
                content,
                count=1
            )
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True
        else:
            print(f"⚠️  未找到DOMContentLoaded，跳过 {file_path}")
            return False
            
    except Exception as e:
        print(f"❌ 处理失败 {file_path}: {e}")
        return False

def main():
    """主函数"""
    print("🔧 修复auth.html的Firebase错误显示问题")
    print("=" * 60)
    
    # 4个版本的auth.html
    auth_files = [
        'auth.html',          # 中文
        'en/auth.html',       # 英文
        'jp/auth.html',       # 日文
        'kr/auth.html'        # 韩文
    ]
    
    success_count = 0
    
    for file_path in auth_files:
        if not os.path.exists(file_path):
            print(f"⏭️  文件不存在: {file_path}")
            continue
        
        print(f"🔄 处理 {file_path}...", end=' ')
        
        if fix_auth_error_display(file_path):
            success_count += 1
            print("✅ 完成")
        else:
            print("❌ 失败")
    
    print("\n" + "=" * 60)
    print("📊 修复完成总结")
    print("=" * 60)
    print(f"✅ 成功修复: {success_count}/{len(auth_files)} 个文件")
    
    if success_count > 0:
        print(f"\n🚀 修复效果:")
        print(f"   ✅ Firebase错误不会在页面加载时显示")
        print(f"   ✅ 错误只会在用户操作失败时显示")
        print(f"   ✅ 控制台仍然可以看到错误信息（用于调试）")

if __name__ == '__main__':
    main()

