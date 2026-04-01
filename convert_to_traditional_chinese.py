#!/usr/bin/env python3
"""
將所有簡體中文頁面轉換為繁體中文

作用：
1. 自動將 <title> 和 <meta name="description"> 中的簡體轉繁體
2. 保持 HTML 標籤和其他內容不變
3. 自動備份原始文件

使用方法：
    python3 convert_to_traditional_chinese.py
"""

import re
from pathlib import Path
import shutil
from datetime import datetime
from opencc import OpenCC

# 配置
BASE_DIR = Path(__file__).parent
BACKUP_DIR = BASE_DIR / f"backup_before_traditional_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
BACKUP_DIR.mkdir(exist_ok=True)

# 初始化簡繁轉換器（簡體 -> 台灣繁體）
cc = OpenCC('s2hk')  # s2hk = Simplified to Hong Kong Traditional

def convert_to_traditional(text):
    """將簡體中文轉換為繁體中文（香港標準）"""
    if not text or not isinstance(text, str):
        return text
    return cc.convert(text)


def update_meta_tags(html_content):
    """更新 HTML 中的 title 和 description 為繁體中文"""
    modified = False
    
    # 1. 更新 <title>
    title_pattern = r'<title>(.*?)</title>'
    def replace_title(match):
        nonlocal modified
        original = match.group(1)
        traditional = convert_to_traditional(original)
        if original != traditional:
            modified = True
            print(f"  📝 標題: {original[:50]}... → {traditional[:50]}...")
        return f'<title>{traditional}</title>'
    
    html_content = re.sub(title_pattern, replace_title, html_content, flags=re.DOTALL)
    
    # 2. 更新 <meta name="description">
    desc_pattern = r'(<meta\s+name="description"\s+content=")([^"]+)(")'
    def replace_desc(match):
        nonlocal modified
        original = match.group(2)
        traditional = convert_to_traditional(original)
        if original != traditional:
            modified = True
            print(f"  📝 描述: {original[:50]}... → {traditional[:50]}...")
        return f'{match.group(1)}{traditional}{match.group(3)}'
    
    html_content = re.sub(desc_pattern, replace_desc, html_content, flags=re.IGNORECASE)
    
    # 3. 更新 <meta property="og:title">
    og_title_pattern = r'(<meta\s+property="og:title"\s+content=")([^"]+)(")'
    html_content = re.sub(og_title_pattern, lambda m: f'{m.group(1)}{convert_to_traditional(m.group(2))}{m.group(3)}', html_content, flags=re.IGNORECASE)
    
    # 4. 更新 <meta property="og:description">
    og_desc_pattern = r'(<meta\s+property="og:description"\s+content=")([^"]+)(")'
    html_content = re.sub(og_desc_pattern, lambda m: f'{m.group(1)}{convert_to_traditional(m.group(2))}{m.group(3)}', html_content, flags=re.IGNORECASE)
    
    return html_content, modified


def process_file(file_path):
    """處理單個文件"""
    try:
        # 讀取文件
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 備份
        backup_path = BACKUP_DIR / file_path.name
        shutil.copy2(file_path, backup_path)
        
        # 轉換
        new_content, modified = update_meta_tags(content)
        
        if modified:
            # 保存
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"  ✅ 已更新並保存")
            return True
        else:
            print(f"  ⏭️  無需更新（已是繁體）")
            return False
            
    except Exception as e:
        print(f"  ❌ 錯誤: {e}")
        return False


def main():
    """主函數"""
    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("🔄 開始將簡體中文轉換為繁體中文...")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    
    print(f"📂 備份目錄: {BACKUP_DIR}")
    print(f"🔧 轉換器: OpenCC (s2hk - 簡體 → 香港繁體)\n")
    
    # 查找所有 HTML 文件（排除英文、日文、韓文目錄）
    html_files = []
    for pattern in ['*.html']:
        html_files.extend(BASE_DIR.glob(pattern))
    
    # 過濾掉非中文版本
    html_files = [f for f in html_files if not any(x in str(f) for x in ['/en/', '/ja/', '/jp/', '/ko/', '/kr/', 'auth.html', 'account.html', 'admin.html', 'firstproject.html'])]
    
    print(f"📋 找到 {len(html_files)} 個中文 HTML 文件需要轉換\n")
    
    success_count = 0
    skip_count = 0
    error_count = 0
    
    for i, file_path in enumerate(sorted(html_files), 1):
        print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"[{i}/{len(html_files)}] 處理: {file_path.name}")
        
        result = process_file(file_path)
        if result:
            success_count += 1
        else:
            skip_count += 1
    
    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("📊 轉換完成統計：")
    print(f"✅ 成功轉換：{success_count} 個")
    print(f"⏭️  無需更新：{skip_count} 個")
    print(f"❌ 錯誤：{error_count} 個")
    print(f"📂 備份位置：{BACKUP_DIR}")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    
    print("🎯 下一步：")
    print("1. 檢查轉換後的文件")
    print("2. 在瀏覽器中查看效果")
    print("3. git add & commit & push")
    print("\n💡 轉換示例：")
    print("   简体：对账单+收据+发票 → 繁體：對賬單+收據+發票")
    print("   简体：处理 → 繁體：處理")
    print("   简体：识别 → 繁體：識別")


if __name__ == '__main__':
    main()

