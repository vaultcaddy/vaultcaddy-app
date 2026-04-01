#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复landing pages和blog页面的语言后缀
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

def fix_title_suffix(content, correct_suffix):
    """修复title标签的后缀"""
    # 查找title标签
    pattern = r'<title>([^<]+)</title>'
    match = re.search(pattern, content, flags=re.IGNORECASE)
    
    if not match:
        return content, False
    
    current_title = match.group(1).strip()
    
    # 移除所有可能的后缀
    original_title = current_title
    for suffix in SUFFIX_BY_LANG.values():
        if suffix in current_title:
            current_title = current_title.replace(suffix, '').strip()
            break
    
    # 添加正确的后缀
    new_title = current_title + correct_suffix
    
    # 如果标题没有变化，则跳过
    if new_title == original_title:
        return content, False
    
    new_content = re.sub(pattern, f'<title>{new_title}</title>', content, flags=re.IGNORECASE)
    
    return new_content, True

def process_file(file_path):
    """处理单个文件"""
    try:
        # 检测语言
        lang = detect_language_from_path(file_path)
        correct_suffix = SUFFIX_BY_LANG[lang]
        
        # 读取文件
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 修复suffix
        new_content, updated = fix_title_suffix(content, correct_suffix)
        
        if updated:
            # 写回文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
        else:
            return None  # 表示不需要更新
            
    except Exception as e:
        print(f'  ❌ 错误: {e}')
        return False

def find_all_files():
    """查找所有需要检查的文件"""
    files = []
    
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
    print('🔧 修复Landing Pages和Blog的语言后缀')
    print('='*60)
    print('')
    
    # 查找所有文件
    print('🔍 查找文件...')
    files = find_all_files()
    print(f'找到 {len(files)} 个文件需要检查')
    print('')
    
    success_count = 0
    skip_count = 0
    fail_count = 0
    
    # 处理每个文件
    for file_path in files:
        result = process_file(file_path)
        
        if result is True:
            print(f'✅ 已修复: {file_path}')
            success_count += 1
        elif result is None:
            skip_count += 1
        else:
            print(f'❌ 失败: {file_path}')
            fail_count += 1
    
    print('\n' + '='*60)
    print(f'✅ 处理完成:')
    print(f'   - {success_count} 个文件已修复')
    print(f'   - {skip_count} 个文件跳过（无需修复）')
    print(f'   - {fail_count} 个文件失败')
    print('='*60)
    
    if success_count > 0:
        print('\n✨ 修复结果:')
        print('  ✅ 英文版使用: 📱Photo Upload 💰$46/mo ⚡3sec Done')
        print('  ✅ 日文版使用: 📱写真アップ 💰46元/月 ⚡3秒完了')
        print('  ✅ 韩文版使用: 📱사진업로드 💰46원/월 ⚡3초완료')

if __name__ == '__main__':
    main()

