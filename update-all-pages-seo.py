#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新所有landing pages和学习中心页面的标题
在现有标题后加上 | 📱拍照上傳 💰46元/月 ⚡3秒完成（对应语言版本）
"""

import re
from pathlib import Path

# 定义不同语言的后缀
SUFFIX_BY_LANG = {
    'zh': ' | 📱拍照上傳 💰46元/月 ⚡3秒完成',
    'en': ' | 📱Photo Upload 💰$46/mo ⚡3sec Done',
    'jp': ' | 📱写真アップ 💰46元/月 ⚡3秒完了',
    'kr': ' | 📱사진업로드 💰46원/월 ⚡3초완료',
}

def detect_language_from_path(file_path):
    """根据文件路径判断语言"""
    path_str = str(file_path)
    if '/en/' in path_str:
        return 'en'
    elif '/jp/' in path_str:
        return 'jp'
    elif '/kr/' in path_str:
        return 'kr'
    else:
        return 'zh'

def update_title_tag(content, suffix):
    """更新title标签，在现有标题后加上后缀"""
    # 查找title标签
    pattern = r'<title>([^<]+)</title>'
    match = re.search(pattern, content, flags=re.IGNORECASE)
    
    if not match:
        return content, False
    
    current_title = match.group(1).strip()
    
    # 检查是否已经包含后缀（避免重复添加）
    if '📱' in current_title and '💰' in current_title and '⚡' in current_title:
        return content, False
    
    # 移除可能已存在的旧后缀
    for old_suffix in SUFFIX_BY_LANG.values():
        if current_title.endswith(old_suffix):
            current_title = current_title[:-len(old_suffix)].strip()
            break
    
    # 添加新后缀
    new_title = current_title + suffix
    new_content = re.sub(pattern, f'<title>{new_title}</title>', content, flags=re.IGNORECASE)
    
    return new_content, True

def process_file(file_path):
    """处理单个文件"""
    try:
        # 检测语言
        lang = detect_language_from_path(file_path)
        suffix = SUFFIX_BY_LANG[lang]
        
        # 读取文件
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 更新title
        new_content, updated = update_title_tag(content, suffix)
        
        if updated:
            # 写回文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
        else:
            return None  # 表示已经包含后缀或没有title标签
            
    except Exception as e:
        print(f'  ❌ 错误: {e}')
        return False

def find_all_html_files():
    """查找所有需要更新的HTML文件"""
    files = []
    
    # 中文版 solutions 和 blog
    files.extend(Path('solutions').rglob('*.html'))
    files.extend(Path('blog').rglob('*.html'))
    
    # 英文版
    files.extend(Path('en/solutions').rglob('*.html'))
    files.extend(Path('en/blog').rglob('*.html'))
    
    # 日文版
    files.extend(Path('jp/solutions').rglob('*.html'))
    files.extend(Path('jp/blog').rglob('*.html'))
    
    # 韩文版
    files.extend(Path('kr/solutions').rglob('*.html'))
    files.extend(Path('kr/blog').rglob('*.html'))
    
    return files

def main():
    """主函数"""
    print('='*60)
    print('🔄 更新所有Landing Pages和学习中心的标题')
    print('='*60)
    print('\n📋 更新范围:')
    print('  ✅ solutions/ - 所有解决方案页面（4个语言版本）')
    print('  ✅ blog/ - 所有学习中心文章（4个语言版本）')
    print('')
    print('📝 添加后缀:')
    print('  🇨🇳 中文: | 📱拍照上傳 💰46元/月 ⚡3秒完成')
    print('  🇬🇧 英文: | 📱Photo Upload 💰$46/mo ⚡3sec Done')
    print('  🇯🇵 日文: | 📱写真アップ 💰46元/月 ⚡3秒完了')
    print('  🇰🇷 韩文: | 📱사진업로드 💰46원/월 ⚡3초완료')
    print('')
    
    # 查找所有文件
    print('🔍 查找文件...')
    files = find_all_html_files()
    print(f'找到 {len(files)} 个文件')
    print('')
    
    success_count = 0
    skip_count = 0
    fail_count = 0
    
    # 处理每个文件
    for file_path in files:
        result = process_file(file_path)
        
        if result is True:
            print(f'✅ {file_path}')
            success_count += 1
        elif result is None:
            skip_count += 1
        else:
            print(f'❌ {file_path}')
            fail_count += 1
    
    print('\n' + '='*60)
    print(f'✅ 处理完成:')
    print(f'   - {success_count} 个文件已更新')
    print(f'   - {skip_count} 个文件跳过（已包含后缀）')
    print(f'   - {fail_count} 个文件失败')
    print('='*60)
    
    if success_count > 0:
        print('\n✨ 更新结果:')
        print('  ✅ 所有landing pages和学习中心的标题已更新')
        print('  ✅ 标题包含: 📱拍照上传 💰价格 ⚡速度')

if __name__ == '__main__':
    main()

