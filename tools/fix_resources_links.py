#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复resources.html中的无效锚点链接"""

import re

def fix_anchor_links(file_path, target_url):
    """将锚点链接替换为auth.html或其他有效链接"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        changes = []
        
        # ========== 1. 查找所有锚点链接 ==========
        # 匹配 <a href="#xxx" class="link-card">
        anchor_pattern = r'<a href="#[^"]+"\s+class="link-card">'
        anchor_matches = list(re.finditer(anchor_pattern, content))
        
        if not anchor_matches:
            return False, ['未找到锚点链接']
        
        # ========== 2. 替换所有锚点链接 ==========
        # 从后往前替换，避免位置偏移
        for match in reversed(anchor_matches):
            start_pos = match.start()
            end_pos = match.end()
            
            # 替换为目标URL
            new_tag = f'<a href="{target_url}" class="link-card">'
            content = content[:start_pos] + new_tag + content[end_pos:]
        
        changes.append(f'修复{len(anchor_matches)}个锚点链接 -> {target_url}')
        
        # ========== 3. 保存 ==========
        if content != original:
            with open(file_path + '.backup_links', 'w', encoding='utf-8') as f:
                f.write(original)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True, changes
        else:
            return False, ['无需修改']
        
    except Exception as e:
        return False, [f'错误: {str(e)}']

# 处理文件
files_to_fix = [
    ('en/resources.html', '/en/auth.html'),
    ('jp/resources.html', '/jp/auth.html'),
    ('kr/resources.html', '/kr/auth.html'),
]

print("=" * 70)
print("🔧 修复resources.html中的无效锚点链接")
print("=" * 70)
print()
print(f"处理 {len(files_to_fix)} 个文件")
print()

processed = 0

for i, (file_path, target_url) in enumerate(files_to_fix, 1):
    success, messages = fix_anchor_links(file_path, target_url)
    
    if success:
        processed += 1
        print(f"✅ [{i}/{len(files_to_fix)}] {file_path}")
        for msg in messages:
            print(f"   {msg}")
    else:
        print(f"⏭️  [{i}/{len(files_to_fix)}] {file_path} - {messages[0]}")

print()
print("=" * 70)
print(f"✅ 已处理：{processed}/{len(files_to_fix)} 个文件")
print()
print("📝 修复说明：")
print("   - 所有锚点链接（href=\"#xxx\"）已改为指向auth.html")
print("   - 用户点击后会跳转到免费试用页面")
print("   - 这样既展示了支持的银行范围，又引导用户注册")
print()
print("🎉 完成！")

