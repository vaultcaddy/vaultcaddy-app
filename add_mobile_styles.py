#!/usr/bin/env python3
"""
將手機版 UI 優化樣式添加到各個頁面
"""

import re

def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(filename, content):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

# 讀取手機版樣式
mobile_styles = read_file('mobile_ui_styles.css')

# 要更新的文件
files = {
    'dashboard.html': {
        'extra_css': '''
        /* Dashboard 特定樣式 */
        @media (max-width: 768px) {
            .create-btn {
                width: 100% !important;
                justify-content: center !important;
            }
            
            .projects-table {
                font-size: 0.875rem !important;
            }
            
            .projects-table td {
                padding: 0.75rem 0.5rem !important;
            }
        }
        '''
    },
    'firstproject.html': {
        'extra_css': '''
        /* First Project 特定樣式 */
        @media (max-width: 768px) {
            .project-header {
                flex-direction: column !important;
                gap: 1rem !important;
            }
            
            .project-title {
                font-size: 1.5rem !important;
            }
            
            .action-buttons {
                width: 100% !important;
                flex-direction: column !important;
            }
            
            .action-buttons button {
                width: 100% !important;
            }
        }
        '''
    },
    'account.html': {
        'extra_css': '''
        /* Account 特定樣式 */
        @media (max-width: 768px) {
            .account-header {
                text-align: center !important;
            }
            
            .settings-section {
                padding: 1rem !important;
            }
            
            .danger-zone {
                margin-top: 2rem !important;
            }
        }
        '''
    },
    'billing.html': {
        'extra_css': '''
        /* Billing 特定樣式 */
        @media (max-width: 768px) {
            .billing-header {
                flex-direction: column !important;
            }
            
            .plan-selector {
                width: 100% !important;
            }
            
            .payment-method {
                flex-direction: column !important;
            }
        }
        '''
    }
}

for filename, config in files.items():
    print(f"\n處理 {filename}...")
    
    try:
        content = read_file(filename)
        
        # 檢查是否已經有手機版樣式
        if '/* 手機版 UI 優化樣式 */' in content:
            print(f"  ⚠️  {filename} 已有手機版樣式，跳過")
            continue
        
        # 找到最後一個 </style> 標籤
        last_style_end = content.rfind('</style>')
        
        if last_style_end == -1:
            print(f"  ❌ 找不到 </style> 標籤")
            continue
        
        # 插入樣式
        new_styles = f"\n        {mobile_styles}\n        {config['extra_css']}\n        "
        content = content[:last_style_end] + new_styles + content[last_style_end:]
        
        # 寫入文件
        write_file(filename, content)
        print(f"  ✅ 已添加手機版樣式")
        
    except Exception as e:
        print(f"  ❌ 處理失敗: {e}")

print("\n✅ 完成！")

