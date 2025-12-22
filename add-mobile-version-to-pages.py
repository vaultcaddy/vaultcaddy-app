#!/usr/bin/env python3
"""
批量为英文/日文/韩文版页面添加手机版代码

作用：
- 扫描en/, jp/, kr/目录下缺少手机版的页面
- 从中文版对应页面提取手机版代码
- 应用到英文/日文/韩文版

使用方法：
python3 add-mobile-version-to-pages.py
"""

import os
import re
from pathlib import Path

# 需要处理的语言版本
LANGUAGES = {
    'en': 'English',
    'jp': 'Japanese', 
    'kr': 'Korean'
}

# 手机版相关的HTML和CSS代码模板
MOBILE_HTML_TEMPLATE = '''
    <!-- 漢堡菜單按鈕（僅手機顯示）-->
    <button id="mobile-menu-btn" onclick="openMobileSidebar()" style="display: none; background: none; border: none; cursor: pointer; padding: 0.5rem; color: #1f2937; font-size: 1.5rem;">
        <i class="fas fa-bars"></i>
    </button>
'''

MOBILE_SIDEBAR_OVERLAY = '''
<!-- 🔥 側邊欄遮罩 -->
<div id="mobile-sidebar-overlay" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 1999; display: none;" onclick="closeMobileSidebar()"></div>
'''

MOBILE_CSS = '''
/* 響應式設計 */
@media (max-width: 768px) {
    /* 導航欄 */
    .vaultcaddy-navbar {
        padding: 0 0.75rem !important;
    }
    
    /* 顯示漢堡菜單按鈕 */
    #mobile-menu-btn {
        display: block !important;
    }
    
    /* 隱藏桌面導航鏈接 */
    .vaultcaddy-navbar > div:first-child > div:nth-child(2) {
        display: none !important;
    }
    
    /* Footer 響應式 */
    footer > div > div {
        grid-template-columns: 1fr !important;
        gap: 2rem !important;
    }
}
'''

MOBILE_JS = '''
<script>
    // ==================== 漢堡菜單功能 ====================
    (function() {
        window.openMobileSidebar = function() {
            const sidebar = document.getElementById('mobile-sidebar');
            const overlay = document.getElementById('mobile-sidebar-overlay');
            if (sidebar && overlay) {
                sidebar.style.left = '0';
                overlay.style.display = 'block';
                document.body.style.overflow = 'hidden';
            }
        };

        window.closeMobileSidebar = function() {
            const sidebar = document.getElementById('mobile-sidebar');
            const overlay = document.getElementById('mobile-sidebar-overlay');
            if (sidebar && overlay) {
                sidebar.style.left = '-100%';
                overlay.style.display = 'none';
                document.body.style.overflow = '';
            }
        };

        function bindMenuButton() {
            const menuBtn = document.getElementById('mobile-menu-btn');
            if (menuBtn) {
                menuBtn.addEventListener('click', window.openMobileSidebar);
            }
        }

        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', bindMenuButton);
        } else {
            bindMenuButton();
        }
    })();
</script>
'''

def check_has_mobile_version(file_path):
    """检查文件是否已有手机版代码"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            return 'mobile-menu-btn' in content and 'mobile-sidebar' in content
    except Exception as e:
        print(f"❌ 错误读取文件 {file_path}: {e}")
        return False

def get_mobile_sidebar_from_reference(lang):
    """从参考文件获取移动侧边栏HTML"""
    # 尝试从对应语言的terms.html获取
    reference_file = f"{lang}/terms.html"
    if os.path.exists(reference_file):
        try:
            with open(reference_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # 提取mobile-sidebar部分
                match = re.search(r'<div id="mobile-sidebar".*?</div>\s*</div>\s*</div>', content, re.DOTALL)
                if match:
                    return match.group(0)
        except Exception as e:
            print(f"⚠️ 无法从{reference_file}提取侧边栏: {e}")
    
    # 返回通用模板
    return get_generic_mobile_sidebar(lang)

def get_generic_mobile_sidebar(lang):
    """返回通用的移动侧边栏模板"""
    # 根据语言设置菜单项文字
    menu_labels = {
        'en': {'features': 'Features', 'pricing': 'Pricing', 'learning': 'Learning Center', 
               'dashboard': 'Dashboard', 'privacy': 'Privacy Policy', 'terms': 'Terms'},
        'jp': {'features': '機能', 'pricing': '料金', 'learning': '学習センター',
               'dashboard': 'ダッシュボード', 'privacy': 'プライバシーポリシー', 'terms': '利用規約'},
        'kr': {'features': '기능', 'pricing': '가격', 'learning': '학습 센터',
               'dashboard': '대시보드', 'privacy': '개인정보 처리방침', 'terms': '이용약관'}
    }
    
    labels = menu_labels.get(lang, menu_labels['en'])
    
    return f'''
<!-- 手機側邊欄菜單 -->
<div id="mobile-sidebar" style="position: fixed; top: 0; left: -100%; width: 280px; height: 100vh; background: white; z-index: 2000; transition: left 0.3s ease; box-shadow: 2px 0 10px rgba(0,0,0,0.1); overflow-y: auto;">
    <div style="padding: 1.5rem;">
        <!-- 菜單項 -->
        <div style="display: flex; flex-direction: column; gap: 0.5rem;">
            <a href="index.html#features" style="padding: 0.875rem 1rem; color: #374151; text-decoration: none; border-radius: 8px; transition: background 0.2s; display: flex; align-items: center; gap: 0.75rem;" onclick="closeMobileSidebar()">
                <i class="fas fa-star" style="width: 20px; color: #667eea;"></i>
                <span>{labels['features']}</span>
            </a>
            <a href="index.html#pricing" style="padding: 0.875rem 1rem; color: #374151; text-decoration: none; border-radius: 8px; transition: background 0.2s; display: flex; align-items: center; gap: 0.75rem;" onclick="closeMobileSidebar()">
                <i class="fas fa-dollar-sign" style="width: 20px; color: #667eea;"></i>
                <span>{labels['pricing']}</span>
            </a>
            <a href="/blog/" style="padding: 0.875rem 1rem; color: #374151; text-decoration: none; border-radius: 8px; transition: background 0.2s; display: flex; align-items: center; gap: 0.75rem;" onclick="closeMobileSidebar()">
                <i class="fas fa-graduation-cap" style="width: 20px; color: #667eea;"></i>
                <span>{labels['learning']}</span>
            </a>
            <a href="dashboard.html" style="padding: 0.875rem 1rem; color: #374151; text-decoration: none; border-radius: 8px; transition: background 0.2s; display: flex; align-items: center; gap: 0.75rem;" onclick="closeMobileSidebar()">
                <i class="fas fa-th-large" style="width: 20px; color: #667eea;"></i>
                <span>{labels['dashboard']}</span>
            </a>
            
            <div style="height: 1px; background: #e5e7eb; margin: 1rem 0;"></div>
            
            <a href="privacy.html" style="padding: 0.875rem 1rem; color: #374151; text-decoration: none; border-radius: 8px; transition: background 0.2s; display: flex; align-items: center; gap: 0.75rem;" onclick="closeMobileSidebar()">
                <i class="fas fa-shield-alt" style="width: 20px; color: #6b7280;"></i>
                <span>{labels['privacy']}</span>
            </a>
            <a href="terms.html" style="padding: 0.875rem 1rem; color: #374151; text-decoration: none; border-radius: 8px; transition: background 0.2s; display: flex; align-items: center; gap: 0.75rem;" onclick="closeMobileSidebar()">
                <i class="fas fa-file-contract" style="width: 20px; color: #6b7280;"></i>
                <span>{labels['terms']}</span>
            </a>
        </div>
    </div>
</div>
'''

def add_mobile_version_to_file(file_path, lang):
    """为单个文件添加手机版代码"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已有手机版
        if 'mobile-menu-btn' in content:
            print(f"  ⏭️  已有手机版，跳过")
            return False
        
        # 1. 在导航栏添加汉堡按钮（在logo后面）
        if '<nav class="vaultcaddy-navbar"' in content:
            content = re.sub(
                r'(<div style="display: flex; align-items: center; gap: 0\.5rem;">)',
                r'\1' + MOBILE_HTML_TEMPLATE,
                content,
                count=1
            )
        
        # 2. 在</nav>后添加侧边栏遮罩和侧边栏
        if '</nav>' in content:
            mobile_sidebar = get_mobile_sidebar_from_reference(lang)
            insertion = MOBILE_SIDEBAR_OVERLAY + mobile_sidebar
            content = content.replace('</nav>', '</nav>' + insertion, 1)
        
        # 3. 在</style>前添加CSS
        if '</style>' in content:
            content = content.replace('</style>', MOBILE_CSS + '</style>', 1)
        
        # 4. 在</body>前添加JavaScript
        if '</body>' in content:
            content = content.replace('</body>', MOBILE_JS + '</body>', 1)
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  ✅ 已添加手机版")
        return True
        
    except Exception as e:
        print(f"  ❌ 错误: {e}")
        return False

def process_directory(lang, directory):
    """处理目录下的所有HTML文件"""
    processed = 0
    skipped = 0
    failed = 0
    
    dir_path = Path(lang) / directory
    if not dir_path.exists():
        return processed, skipped, failed
    
    for html_file in dir_path.glob('**/*.html'):
        # 跳过.tmp文件
        if html_file.suffix == '.tmp' or '.tmp' in html_file.suffixes:
            continue
        
        print(f"\n📄 处理: {html_file}")
        
        if check_has_mobile_version(html_file):
            print(f"  ⏭️  已有手机版，跳过")
            skipped += 1
            continue
        
        if add_mobile_version_to_file(html_file, lang):
            processed += 1
        else:
            failed += 1
    
    return processed, skipped, failed

def main():
    print("🚀 开始批量添加手机版...")
    print("=" * 60)
    
    total_processed = 0
    total_skipped = 0
    total_failed = 0
    
    for lang, lang_name in LANGUAGES.items():
        print(f"\n\n{'=' * 60}")
        print(f"🌐 处理 {lang_name} 版本 ({lang}/)")
        print(f"{'=' * 60}")
        
        # 处理blog文章
        print(f"\n📚 处理 Blog 文章...")
        p, s, f = process_directory(lang, 'blog')
        total_processed += p
        total_skipped += s
        total_failed += f
        print(f"  ✅ 已处理: {p} | ⏭️  跳过: {s} | ❌ 失败: {f}")
        
        # 处理solutions页面
        print(f"\n💼 处理 Solutions 页面...")
        p, s, f = process_directory(lang, 'solutions')
        total_processed += p
        total_skipped += s
        total_failed += f
        print(f"  ✅ 已处理: {p} | ⏭️  跳过: {s} | ❌ 失败: {f}")
    
    # 最终总结
    print(f"\n\n{'=' * 60}")
    print(f"📊 批量处理完成统计")
    print(f"{'=' * 60}")
    print(f"✅ 成功添加手机版: {total_processed} 个文件")
    print(f"⏭️  跳过（已有手机版）: {total_skipped} 个文件")
    print(f"❌ 处理失败: {total_failed} 个文件")
    print(f"{'=' * 60}")

if __name__ == '__main__':
    main()

