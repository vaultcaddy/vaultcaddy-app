#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新博客內容：
1. ai-invoice-processing-guide.html - VaultCaddy 價格
2. best-pdf-to-excel-converter.html - 添加 iLovePDF 和 Soda PDF
3. automate-financial-documents.html - 處理時間改為 10 秒
"""

import re
from pathlib import Path

def update_ai_invoice_guide():
    """更新 AI 發票處理指南的價格"""
    file_path = 'blog/ai-invoice-processing-guide.html'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. 更新 AI 方法的成本部分
    old_cost = r'VaultCaddy Pro 訂閱：</strong>\$39/月（500 頁）'
    new_cost = r'VaultCaddy 訂閱：</strong>HKD $78/月（100 頁，之後每頁 HKD $0.5）'
    content = re.sub(old_cost, new_cost, content)
    
    # 2. 更新年度總成本計算（假設仍是 500 頁/月）
    # 計算：100 頁 = $78，剩餘 400 頁 x $0.5 = $200，總計 $278/月
    old_annual = r'<li><strong>VaultCaddy Pro 訂閱：</strong>\$39/月（500 頁）</li>'
    new_annual = r'<li><strong>VaultCaddy 訂閱：</strong>HKD $278/月（100 頁 + 400 頁 x $0.5）</li>'
    content = re.sub(old_annual, new_annual, content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 已更新 {file_path}")

def update_best_converter():
    """更新 PDF 轉 Excel 工具列表"""
    file_path = 'blog/best-pdf-to-excel-converter.html'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. 在每個工具（2-7）的描述後添加說明
    # 找到工具 2 的位置並添加說明
    tools_pattern = r'(<h3>2\. Adobe Acrobat Pro DC</h3>.*?<p><strong>價格：</strong>.*?</p>)'
    
    # 為工具 2-10 添加通用說明
    note_text = '\n            <p><strong>⚠️ 注意：</strong>此工具只能進行格式轉換，轉換後仍需<strong>手動提取所需數據</strong>並整理到會計系統中。</p>'
    
    # 找到所有工具並添加說明（工具 2-10）
    for i in range(2, 11):
        # 匹配每個工具的價格段落
        pattern = rf'(<h3>{i}\. .*?</h3>.*?<p><strong>價格：</strong>.*?</p>)'
        
        def add_note(match):
            return match.group(1) + note_text
        
        content = re.sub(pattern, add_note, content, flags=re.DOTALL, count=1)
    
    # 2. 添加 iLovePDF 和 Soda PDF 的價格信息
    # iLovePDF (假設是工具 8)
    ilovepdf_pattern = r'(<h3>8\. iLovePDF</h3>.*?)(<h3>9\.)'
    ilovepdf_replacement = r'''\1
            <p><strong>價格：</strong>USD $7/月（約 HKD $55）或免費版（有限制）</p>
            <p><strong>⚠️ 注意：</strong>此工具只能進行格式轉換，轉換後仍需<strong>手動提取所需數據</strong>並整理到會計系統中。</p>
            
            \2'''
    content = re.sub(ilovepdf_pattern, ilovepdf_replacement, content, flags=re.DOTALL)
    
    # Soda PDF (假設是工具 9)
    sodapdf_pattern = r'(<h3>9\. Soda PDF</h3>.*?)(<h3>10\.)'
    sodapdf_replacement = r'''\1
            <p><strong>價格：</strong>USD $10/月（約 HKD $78）或免費版（有限制）</p>
            <p><strong>⚠️ 注意：</strong>此工具只能進行格式轉換，轉換後仍需<strong>手動提取所需數據</strong>並整理到會計系統中。</p>
            
            \2'''
    content = re.sub(sodapdf_pattern, sodapdf_replacement, content, flags=re.DOTALL)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 已更新 {file_path}")

def update_automate_guide():
    """更新自動化財務文檔處理指南"""
    file_path = 'blog/automate-financial-documents.html'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 更新處理時間從 30 秒改為 10 秒
    old_time = r'每張發票平均處理時間：30 秒'
    new_time = r'每張發票平均處理時間：10 秒'
    content = re.sub(old_time, new_time, content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 已更新 {file_path}")

def main():
    """主函數"""
    print("=" * 60)
    print("🔄 開始更新博客內容...")
    print("=" * 60)
    
    # 1. 更新 AI 發票處理指南
    print("\n1️⃣ 更新 AI 發票處理指南的價格...")
    update_ai_invoice_guide()
    
    # 2. 更新 PDF 轉 Excel 工具列表
    print("\n2️⃣ 更新 PDF 轉 Excel 工具列表...")
    update_best_converter()
    
    # 3. 更新自動化指南
    print("\n3️⃣ 更新自動化財務文檔處理指南...")
    update_automate_guide()
    
    print("\n" + "=" * 60)
    print("✅ 所有更新完成！")
    print("=" * 60)

if __name__ == '__main__':
    main()

