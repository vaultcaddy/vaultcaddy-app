#!/usr/bin/env python3
"""
統一所有頁面的導航欄到 dashboard.html 的版本
並簡化會員 Logo 邏輯為只顯示 'YC'
"""

import re

# 要統一的頁面列表
pages = [
    'index.html',
    'firstproject.html',
    'account.html',
    'billing.html',
    'privacy.html',
    'terms.html'
]

# Dashboard 的導航欄模板（已移除多餘的 Logo 邏輯）
navbar_template = '''<nav class="vaultcaddy-navbar" id="main-navbar" style="position: fixed; top: 0; left: 0; right: 0; height: 60px; background: #ffffff; border-bottom: 1px solid #e5e7eb; display: flex; align-items: center; justify-content: space-between; padding: 0 2rem; z-index: 1000; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);">
        <div style="display: flex; align-items: center; gap: 0.5rem;">
            <!-- 漢堡菜單按鈕（僅手機顯示）-->
            <button id="mobile-menu-btn" onclick="openMobileSidebar()" style="display: none; background: none; border: none; cursor: pointer; padding: 0.5rem; color: #1f2937; font-size: 1.5rem;">
                <i class="fas fa-bars"></i>
            </button>
            
            <a href="index.html" style="display: flex; align-items: center; gap: 0.75rem; text-decoration: none; color: #1f2937; font-weight: 600; font-size: 1.125rem;">
                <div class="desktop-logo" style="width: 32px; height: 32px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; font-weight: 700; font-size: 1.25rem;">
                    V
                </div>
                <div class="desktop-logo-text">
                    <div>VaultCaddy</div>
                    <div style="font-size: 0.75rem; color: #6b7280; font-weight: 400; text-transform: uppercase; letter-spacing: 0.05em;">AI DOCUMENT PROCESSING</div>
                </div>
            </a>
        </div>
        <div style="display: flex; align-items: center; gap: 2rem;">
            <div style="display: flex; align-items: center; gap: 2rem;">
                <a href="index.html#features" style="color: #4b5563; text-decoration: none; font-size: 0.9375rem; font-weight: 500; transition: color 0.2s;">功能</a>
                <a href="index.html#pricing" style="color: #4b5563; text-decoration: none; font-size: 0.9375rem; font-weight: 500; transition: color 0.2s;">價格</a>
                <a href="dashboard.html" style="color: #4b5563; text-decoration: none; font-size: 0.9375rem; font-weight: 500; transition: color 0.2s;">儀表板</a>
            </div>
            <div id="user-menu" style="position: relative; display: flex; align-items: center; gap: 0.75rem; cursor: pointer; padding: 0.5rem; border-radius: 8px; transition: background 0.2s;">
                <div id="user-avatar" style="width: 32px; height: 32px; border-radius: 50%; background: #667eea; display: flex; align-items: center; justify-content: center; color: white; font-weight: 600; font-size: 0.875rem;">U</div>
            </div>
        </div>
    </nav>'''

# 手機側邊欄模板
mobile_sidebar_template = '''<!-- 手機側邊欄菜單 -->
    <div id="mobile-sidebar" style="position: fixed; top: 0; left: -100%; width: 280px; height: 100vh; background: white; z-index: 2000; transition: left 0.3s ease; box-shadow: 2px 0 10px rgba(0,0,0,0.1); overflow-y: auto;">
        <div style="padding: 1.5rem;">
            <!-- 菜單項 -->
            <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                <a href="index.html#features" style="padding: 0.875rem 1rem; color: #374151; text-decoration: none; border-radius: 8px; transition: background 0.2s; display: flex; align-items: center; gap: 0.75rem;" onclick="closeMobileSidebar()">
                    <i class="fas fa-star" style="width: 20px; color: #667eea;"></i>
                    <span>功能</span>
                </a>
                <a href="index.html#pricing" style="padding: 0.875rem 1rem; color: #374151; text-decoration: none; border-radius: 8px; transition: background 0.2s; display: flex; align-items: center; gap: 0.75rem;" onclick="closeMobileSidebar()">
                    <i class="fas fa-dollar-sign" style="width: 20px; color: #667eea;"></i>
                    <span>價格</span>
                </a>
                <a href="dashboard.html" style="padding: 0.875rem 1rem; color: #374151; text-decoration: none; border-radius: 8px; transition: background 0.2s; display: flex; align-items: center; gap: 0.75rem;" onclick="closeMobileSidebar()">
                    <i class="fas fa-th-large" style="width: 20px; color: #667eea;"></i>
                    <span>儀表板</span>
                </a>
                
                <div style="height: 1px; background: #e5e7eb; margin: 1rem 0;"></div>
                
                <a href="privacy.html" style="padding: 0.875rem 1rem; color: #374151; text-decoration: none; border-radius: 8px; transition: background 0.2s; display: flex; align-items: center; gap: 0.75rem;" onclick="closeMobileSidebar()">
                    <i class="fas fa-shield-alt" style="width: 20px; color: #6b7280;"></i>
                    <span>隱私政策</span>
                </a>
                <a href="terms.html" style="padding: 0.875rem 1rem; color: #374151; text-decoration: none; border-radius: 8px; transition: background 0.2s; display: flex; align-items: center; gap: 0.75rem;" onclick="closeMobileSidebar()">
                    <i class="fas fa-file-contract" style="width: 20px; color: #6b7280;"></i>
                    <span>服務條款</span>
                </a>
            </div>
        </div>
    </div>'''

def unify_navbar(filename):
    """統一單個頁面的導航欄"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 移除舊的導航欄（從 <nav 到 </nav>，允許跨多行）
        content = re.sub(
            r'<nav[^>]*class="vaultcaddy-navbar"[^>]*>.*?</nav>',
            navbar_template,
            content,
            flags=re.DOTALL
        )
        
        # 移除舊的手機側邊欄（從 <!-- 手機側邊欄菜單 --> 到 </div>）
        content = re.sub(
            r'<!-- 手機側邊欄菜單 -->.*?</div>\s*</div>',
            mobile_sidebar_template,
            content,
            flags=re.DOTALL,
            count=1
        )
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ {filename} - 導航欄已統一")
        return True
    except Exception as e:
        print(f"❌ {filename} - 錯誤: {e}")
        return False

def simplify_unified_auth():
    """簡化 unified-auth.js 的 Logo 邏輯為只顯示 'YC'"""
    try:
        with open('unified-auth.js', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 找到並替換 getUserInitial 或類似的邏輯
        # 簡化為直接返回 'YC'
        content = re.sub(
            r'const initial = .*?;',
            "const initial = 'YC';",
            content
        )
        
        # 也替換任何 user.email.substring 或 user.email.charAt 的邏輯
        content = re.sub(
            r'user\.email\.substring\([^)]+\)\.toUpperCase\(\)',
            "'YC'",
            content
        )
        content = re.sub(
            r'user\.email\.charAt\([^)]+\)\.toUpperCase\(\)',
            "'Y'",
            content
        )
        
        with open('unified-auth.js', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ unified-auth.js - Logo 邏輯已簡化為 'YC'")
        return True
    except Exception as e:
        print(f"❌ unified-auth.js - 錯誤: {e}")
        return False

def main():
    print("=" * 60)
    print("開始統一導航欄並簡化 Logo 邏輯...")
    print("=" * 60)
    
    # 統一所有頁面的導航欄
    success_count = 0
    for page in pages:
        if unify_navbar(page):
            success_count += 1
    
    print(f"\n導航欄統一: {success_count}/{len(pages)} 頁面成功")
    
    # 簡化 unified-auth.js
    if simplify_unified_auth():
        print("✅ Logo 邏輯簡化成功")
    
    print("=" * 60)
    print("✅ 完成！")
    print("=" * 60)

if __name__ == "__main__":
    main()

