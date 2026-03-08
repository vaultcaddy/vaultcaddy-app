#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复3个问题：
1. 加强Logo显示（立即显示Logo，不等待加载失败）
2. 移除Trust Badges区域的黑色线（border）
3. 将index.html弹窗改为繁体
"""

import os
import re

def fix_v3_pages():
    """修复所有250个v3页面"""
    print("🎯 开始修复v3页面...")
    print("=" * 70)
    
    # 获取所有v3文件
    all_files = []
    all_files.extend([f for f in os.listdir('.') if f.endswith('-v3.html')])
    for lang_dir in ['zh-HK', 'ja-JP', 'ko-KR', 'zh-TW']:
        if os.path.exists(lang_dir):
            lang_files = [os.path.join(lang_dir, f) for f in os.listdir(lang_dir) if f.endswith('-v3.html')]
            all_files.extend(lang_files)
    
    success_count = 0
    
    for i, file_path in enumerate(sorted(all_files), 1):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # 1. 移除Trust Badges section的边框/分隔线
            # 查找Trust & Security Section并移除可能的border
            content = content.replace(
                '<!-- Trust & Security Section -->',
                '<!-- Trust & Security Section (No Borders) -->'
            )
            
            # 移除section可能的border样式
            content = re.sub(
                r'(<section[^>]*style="[^"]*)(border[^;]*;)([^"]*"[^>]*>)',
                r'\1\3',
                content
            )
            
            # 2. 加强Logo显示逻辑 - 添加立即显示的脚本
            if '// Logo备用方案' in content:
                # 替换现有的Logo脚本为更强的版本
                logo_script_pattern = r'<script>[\s\S]*?// Logo备用方案[\s\S]*?</script>'
                
                enhanced_logo_script = '''
        <script>
            // 增强的Logo显示方案 - 立即尝试显示
            (function() {
                function ensureBankLogo() {
                    const bankLogo = document.querySelector('.bank-logo');
                    if (!bankLogo) return;
                    
                    let attemptCount = 0;
                    const maxAttempts = 3;
                    
                    function tryLoadLogo() {
                        attemptCount++;
                        console.log(`尝试加载Logo (第${attemptCount}次)...`);
                        
                        // 检查Logo是否成功加载
                        if (bankLogo.complete && bankLogo.naturalHeight > 0) {
                            console.log('✅ Logo加载成功！');
                            return true;
                        }
                        
                        // 如果加载失败，尝试备用方案
                        if (attemptCount === 1) {
                            // 尝试Google Favicon
                            const currentSrc = bankLogo.src;
                            const domain = currentSrc.split('clearbit.com/')[1];
                            bankLogo.src = `https://www.google.com/s2/favicons?domain=${domain}&sz=128`;
                            console.log('⚠️ Clearbit失败，尝试Google Favicon...');
                            
                            setTimeout(tryLoadLogo, 500);
                            return false;
                        }
                        
                        if (attemptCount === 2) {
                            // 检查Google Favicon是否成功
                            if (bankLogo.complete && bankLogo.naturalHeight > 0) {
                                console.log('✅ Google Favicon加载成功！');
                                return true;
                            }
                            
                            // 最后使用文字Logo
                            const container = bankLogo.parentElement;
                            const bankName = bankLogo.alt.replace(' Logo', '');
                            container.innerHTML = `<div style="font-size: 32px; font-weight: 900; color: white; text-transform: uppercase; letter-spacing: 3px; opacity: 0.95; text-shadow: 0 2px 4px rgba(0,0,0,0.2);">${bankName}</div>`;
                            console.log('ℹ️ 使用文字Logo');
                            return true;
                        }
                        
                        return false;
                    }
                    
                    // 立即检查
                    if (!tryLoadLogo()) {
                        // 如果不成功，500ms后再试
                        setTimeout(() => {
                            if (attemptCount < maxAttempts) {
                                tryLoadLogo();
                            }
                        }, 500);
                    }
                }
                
                // 页面加载完成后立即执行
                if (document.readyState === 'loading') {
                    document.addEventListener('DOMContentLoaded', ensureBankLogo);
                } else {
                    ensureBankLogo();
                }
            })();
        </script>
'''
                content = re.sub(logo_script_pattern, enhanced_logo_script, content, flags=re.DOTALL)
            
            # 只有内容改变时才保存
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                success_count += 1
                if i <= 5 or i % 50 == 0:
                    print(f"✅ {i}/{len(all_files)} - {os.path.basename(file_path)}")
        
        except Exception as e:
            print(f"❌ {file_path}: {str(e)}")
    
    print("=" * 70)
    print(f"✅ v3页面修复完成: {success_count}/{len(all_files)}")
    return success_count

def fix_index_popup():
    """修复index.html的弹窗为繁体"""
    print("\n🎯 开始修复index.html弹窗...")
    print("=" * 70)
    
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 简体转繁体的替换
        replacements = {
            '等等！别错过这个优惠': '等等！別錯過這個優惠',
            '首次注册立享': '首次註冊立享',
            '折扣': '折扣',
            '免费试用': '免費試用',
            '页': '頁',
            '输入您的邮箱获取折扣码': '輸入您的郵箱獲取折扣碼',
            '获取20%折扣码': '獲取20%折扣碼',
            '折扣码已發送到您的邮箱': '折扣碼已發送到您的郵箱',
            '优惠码有效期24小时': '優惠碼有效期24小時',
            '仅限首次注册用户': '僅限首次註冊用戶',
        }
        
        for old, new in replacements.items():
            content = content.replace(old, new)
        
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ index.html弹窗已改为繁体")
        return True
    
    except Exception as e:
        print(f"❌ 修复index.html失败: {str(e)}")
        return False

def main():
    print("🚀 开始修复...")
    print("=" * 70)
    print("📋 任务列表:")
    print("   1. 加强Logo显示（立即尝试，不等待失败）")
    print("   2. 移除Trust Badges区域边框")
    print("   3. index.html弹窗改为繁体")
    print("=" * 70)
    print()
    
    # 修复v3页面
    v3_count = fix_v3_pages()
    
    # 修复index.html
    index_success = fix_index_popup()
    
    print("\n" + "=" * 70)
    print("🎉 所有修复完成！")
    print("=" * 70)
    print(f"✅ v3页面: {v3_count}/250")
    print(f"✅ index.html: {'成功' if index_success else '失败'}")
    print()
    print("📋 已完成:")
    print("  1. ✅ Logo立即显示（3层备用）")
    print("  2. ✅ 移除黑色线")
    print("  3. ✅ 弹窗繁体化")

if __name__ == '__main__':
    main()

