#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复Hero Section：恢复背景颜色和图片"""

import glob
import re

def fix_hero_section(file_path):
    """修复单个页面的Hero Section"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        changes = []
        
        # ========== 1. 查找Hero Section注释的位置 ==========
        hero_comment_pattern = r'<!-- Hero Section -->\s*(?:\n\s*)*(?:\n\s*)*(?:\n\s*)*\s*<div class="container hero-content">'
        hero_comment_match = re.search(hero_comment_pattern, content)
        
        if not hero_comment_match:
            return False, ['未找到Hero Section注释']
        
        # ========== 2. 查找错误位置的<section class="hero">标签并删除 ==========
        # 查找案例section中的错误hero标签
        wrong_hero_pattern = r'<!-- 案例 Section -->\s*<section class="hero">[\s\S]*?<img[^>]+class="hero-background"[^>]*>\s*'
        wrong_hero_match = re.search(wrong_hero_pattern, content)
        
        if wrong_hero_match:
            # 删除错误的hero section开始标签和背景图片
            content = content[:wrong_hero_match.start()] + '    <!-- 案例 Section -->\n    ' + content[wrong_hero_match.end():]
            changes.append('删除错误位置的hero标签')
        
        # ========== 3. 在正确位置插入Hero Section标签和背景图片 ==========
        # 查找Hero Section注释
        hero_comment_match = re.search(hero_comment_pattern, content)
        
        # 准备要插入的Hero Section开始标签
        hero_section_start = '''<section class="hero">
        <!-- 背景图片 -->
        <img src="https://images.unsplash.com/photo-1563013544-824ae1b704d3?w=1920&h=800&fit=crop" 
             alt="Banking Background" 
             class="hero-background"
             loading="eager">
        
        '''
        
        # 在Hero Section注释后插入
        insert_pos = hero_comment_match.end()
        content = (
            content[:hero_comment_match.start()] +
            '    <!-- Hero Section -->\n    ' +
            hero_section_start +
            content[insert_pos:]
        )
        changes.append('在正确位置添加hero标签和背景图片')
        
        # ========== 4. 查找Hero Section的结束位置并添加</section> ==========
        # 查找"免費試用"按钮后的位置
        hero_end_pattern = r'(<a href="[^"]*auth\.html"[^>]*>立即免費試用[^<]*</a>[\s\S]*?</div>[\s\S]*?</div>[\s\S]*?</div>\s*)'
        hero_end_match = re.search(hero_end_pattern, content)
        
        if hero_end_match:
            insert_pos = hero_end_match.end()
            # 检查是否已经有</section>
            after_text = content[insert_pos:insert_pos+100]
            if '</section>' not in after_text[:20]:
                content = content[:insert_pos] + '\n    </section>\n\n' + content[insert_pos:]
                changes.append('添加hero section结束标签')
        
        # ========== 5. 保存 ==========
        if content != original:
            with open(file_path + '.backup_hero', 'w', encoding='utf-8') as f:
                f.write(original)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True, changes
        else:
            return False, ['无需修改']
        
    except Exception as e:
        return False, [f'错误: {str(e)}']

# 获取所有银行页面
patterns = [
    '*-bank-statement.html',
]

all_files = []
for pattern in patterns:
    all_files.extend(glob.glob(pattern))

all_files = list(set(all_files))
all_files.sort()

print("=" * 70)
print("🔧 修复Hero Section（恢复背景颜色和图片）")
print("=" * 70)
print()
print(f"找到 {len(all_files)} 个中文银行页面")
print()

processed = 0

for i, file_path in enumerate(all_files, 1):
    success, messages = fix_hero_section(file_path)
    
    if success:
        processed += 1
        print(f"✅ [{i}/{len(all_files)}] {file_path}")
        print(f"   {', '.join(messages)}")
    else:
        print(f"⏭️  [{i}/{len(all_files)}] {file_path} - {messages[0]}")

print()
print("=" * 70)
print(f"✅ 已处理：{processed}/{len(all_files)} 个文件")
print("🎉 完成！")

