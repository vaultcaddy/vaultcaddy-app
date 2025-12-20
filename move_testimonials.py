#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将"香港會計師都在用的 AI 工具"中的用户评价移动到正确的"VaultCaddy 使用者評價"section
"""

import re

def move_testimonials():
    """移动用户评价到正确位置"""
    
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. 删除"香港社会证明"整个section（1297-1357行）
    # 查找并删除这个section
    old_section_pattern = r'<!-- 香港社会证明 -->.*?</div>\s*</div>\s*</div>'
    
    content = re.sub(old_section_pattern, '', content, flags=re.DOTALL)
    
    # 2. 创建3个香港用户评价卡片（匹配现有的样式）
    hong_kong_testimonials = '''                    <!-- 評價卡片 1 - 陳小姐 -->
                    <div style="background: white; border-radius: 16px; padding: 2rem; box-shadow: 0 2px 10px rgba(0,0,0,0.08); transition: transform 0.3s, box-shadow 0.3s;" onmouseover="this.style.transform='translateY(-5px)'; this.style.boxShadow='0 8px 25px rgba(0,0,0,0.12)'" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 10px rgba(0,0,0,0.08)'">
                        <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1.5rem;">
                            <div style="width: 60px; height: 60px; border-radius: 50%; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); display: flex; align-items: center; justify-content: center; flex-shrink: 0; color: white; font-weight: 700; font-size: 1.5rem;">
                                陳
                            </div>
                            <div>
                                <h4 style="font-size: 1rem; font-weight: 600; color: #1f2937; margin: 0 0 0.25rem 0;">陳小姐</h4>
                                <p style="font-size: 0.875rem; color: #6b7280; margin: 0;">中環會計師事務所</p>
                            </div>
                        </div>
                        <p style="color: #4b5563; line-height: 1.6; font-size: 0.9375rem;">"以前每個月要花 2-3 天處理客戶的銀行對帳單，現在用 VaultCaddy 只需要半天。節省的時間可以服務更多客戶！"</p>
                        <div style="margin-top: 1rem; color: #f59e0b; font-size: 1.125rem;">⭐⭐⭐⭐⭐</div>
                    </div>
                    
                    <!-- 評價卡片 2 - 李先生 -->
                    <div style="background: white; border-radius: 16px; padding: 2rem; box-shadow: 0 2px 10px rgba(0,0,0,0.08); transition: transform 0.3s, box-shadow 0.3s;" onmouseover="this.style.transform='translateY(-5px)'; this.style.boxShadow='0 8px 25px rgba(0,0,0,0.12)'" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 10px rgba(0,0,0,0.08)'">
                        <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1.5rem;">
                            <div style="width: 60px; height: 60px; border-radius: 50%; background: linear-gradient(135deg, #10b981 0%, #059669 100%); display: flex; align-items: center; justify-content: center; flex-shrink: 0; color: white; font-weight: 700; font-size: 1.5rem;">
                                李
                            </div>
                            <div>
                                <h4 style="font-size: 1rem; font-weight: 600; color: #1f2937; margin: 0 0 0.25rem 0;">李先生</h4>
                                <p style="font-size: 0.875rem; color: #6b7280; margin: 0;">灣仔餐廳老闆</p>
                            </div>
                        </div>
                        <p style="color: #4b5563; line-height: 1.6; font-size: 0.9375rem;">"以前請人做帳每月要 HK$8,000，現在用 VaultCaddy 自己處理，每月只需幾百元。省下的錢可以請多一個員工！"</p>
                        <div style="margin-top: 1rem; color: #f59e0b; font-size: 1.125rem;">⭐⭐⭐⭐⭐</div>
                    </div>
                    
                    <!-- 評價卡片 3 - 黃小姐 -->
                    <div style="background: white; border-radius: 16px; padding: 2rem; box-shadow: 0 2px 10px rgba(0,0,0,0.08); transition: transform 0.3s, box-shadow 0.3s;" onmouseover="this.style.transform='translateY(-5px)'; this.style.boxShadow='0 8px 25px rgba(0,0,0,0.12)'" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 10px rgba(0,0,0,0.08)'">
                        <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1.5rem;">
                            <div style="width: 60px; height: 60px; border-radius: 50%; background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); display: flex; align-items: center; justify-content: center; flex-shrink: 0; color: white; font-weight: 700; font-size: 1.5rem;">
                                黃
                            </div>
                            <div>
                                <h4 style="font-size: 1rem; font-weight: 600; color: #1f2937; margin: 0 0 0.25rem 0;">黃小姐</h4>
                                <p style="font-size: 0.875rem; color: #6b7280; margin: 0;">自僱會計師</p>
                            </div>
                        </div>
                        <p style="color: #4b5563; line-height: 1.6; font-size: 0.9375rem;">"準確率超高，匯豐、恆生、中銀的對帳單都能完美識別。現在可以準時下班，多陪陪家人了！"</p>
                        <div style="margin-top: 1rem; color: #f59e0b; font-size: 1.125rem;">⭐⭐⭐⭐⭐</div>
                    </div>
                    
'''
    
    # 3. 在第一个评价卡片之前插入这3个香港用户评价
    # 查找第一个评价卡片的位置
    first_card_pattern = r'(<!-- 6張評價卡片 3x2 網格.*?<div id="testimonials"[^>]*>)\s*(<!-- 評價卡片 1 -->)'
    
    content = re.sub(
        first_card_pattern,
        r'\1\n' + hong_kong_testimonials + r'\2',
        content,
        flags=re.DOTALL
    )
    
    # 4. 保存修改后的文件
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def main():
    """主函数"""
    print("=" * 70)
    print("📋 开始移动用户评价")
    print("=" * 70)
    print()
    
    try:
        print("处理中...", end=" ")
        move_testimonials()
        print("✅ 完成")
        print()
        
        print("=" * 70)
        print("🎉 用户评价移动完成！")
        print("=" * 70)
        print()
        print("📊 完成内容：")
        print("  ✅ 删除了「香港會計師都在用的 AI 工具」section")
        print("  ✅ 将3个香港用户评价添加到「VaultCaddy 使用者評價」")
        print("     • 陳小姐 - 中環會計師事務所")
        print("     • 李先生 - 灣仔餐廳老闆")
        print("     • 黃小姐 - 自僱會計師")
        print()
        print("  现在「VaultCaddy 使用者評價」section 共有 9 个评价")
        print("  前3个是香港本地用户，后6个是国际用户")
        print()
        print("🚀 立即刷新浏览器查看效果！")
        print()
        
    except Exception as e:
        print(f"❌ 错误：{e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()

