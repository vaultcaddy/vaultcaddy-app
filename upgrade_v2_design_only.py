#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
升级v2页面的设计到v3标准
只更新：CSS样式 + 定价格式 + auth链接
保留：原有内容和文字
"""

import os
import re
from pathlib import Path

class V2DesignUpgrader:
    def __init__(self, root_dir):
        self.root_dir = Path(root_dir)
        self.upgraded_count = 0
        
        # v3 CSS样式
        self.v3_css = '''
<style>
    /* v3 现代化设计样式 */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    body {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
        line-height: 1.6;
        color: #1a202c;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Hero Section */
    .hero {
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 100px 24px 50px 24px;
        position: relative;
    }
    
    .hero-content {
        max-width: 900px;
        text-align: center;
        color: white;
    }
    
    .hero h1 {
        font-size: 64px;
        font-weight: 900;
        margin-bottom: 24px;
        line-height: 1.1;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .hero p {
        font-size: 22px;
        margin-bottom: 40px;
        opacity: 0.95;
    }
    
    /* Stats */
    .stats {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 40px;
        margin: 50px 0;
    }
    
    .stat {
        text-align: center;
    }
    
    .stat-number {
        font-size: 56px;
        font-weight: 900;
        display: block;
        margin-bottom: 8px;
    }
    
    .stat-label {
        font-size: 18px;
        opacity: 0.9;
    }
    
    /* Buttons */
    .btn {
        display: inline-block;
        padding: 18px 48px;
        border-radius: 50px;
        font-weight: 700;
        font-size: 18px;
        text-decoration: none;
        transition: all 0.3s;
        cursor: pointer;
        border: none;
    }
    
    .btn-primary {
        background: white;
        color: #667eea;
        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
    }
    
    .btn-primary:hover {
        transform: translateY(-2px);
        box-shadow: 0 15px 50px rgba(0,0,0,0.3);
    }
    
    .btn-secondary {
        background: rgba(255,255,255,0.2);
        color: white;
        border: 2px solid rgba(255,255,255,0.5);
    }
    
    .btn-secondary:hover {
        background: rgba(255,255,255,0.3);
    }
    
    /* Content Sections */
    .section {
        padding: 80px 24px;
        background: white;
    }
    
    .section-title {
        text-align: center;
        margin-bottom: 60px;
    }
    
    .section-title h2 {
        font-size: 42px;
        font-weight: 800;
        color: #1a202c;
        margin-bottom: 16px;
    }
    
    .section-title p {
        font-size: 20px;
        color: #64748b;
    }
    
    /* Feature Grid */
    .features {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 40px;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .feature {
        padding: 40px;
        background: #f8fafc;
        border-radius: 16px;
        transition: all 0.3s;
    }
    
    .feature:hover {
        transform: translateY(-4px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
    }
    
    .feature h3 {
        font-size: 24px;
        font-weight: 700;
        color: #1a202c;
        margin-bottom: 16px;
    }
    
    .feature p {
        color: #64748b;
        line-height: 1.8;
    }
    
    /* Pricing */
    .pricing {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 40px;
        max-width: 900px;
        margin: 0 auto;
    }
    
    .pricing-card {
        background: white;
        padding: 48px;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        transition: all 0.3s;
        position: relative;
    }
    
    .pricing-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 60px rgba(0,0,0,0.15);
    }
    
    .pricing-card.popular {
        border: 3px solid #667eea;
        transform: scale(1.05);
    }
    
    .pricing-badge {
        position: absolute;
        top: -16px;
        right: 40px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 8px 20px;
        border-radius: 20px;
        font-size: 14px;
        font-weight: 700;
    }
    
    .pricing-price {
        font-size: 56px;
        font-weight: 900;
        color: #1a202c;
        margin-bottom: 8px;
    }
    
    .pricing-period {
        color: #64748b;
        font-size: 18px;
        margin-bottom: 32px;
    }
    
    .pricing-features {
        list-style: none;
        margin-bottom: 40px;
    }
    
    .pricing-features li {
        padding: 12px 0;
        color: #475569;
        font-size: 16px;
    }
    
    .pricing-features li:before {
        content: "✓";
        color: #10b981;
        font-weight: 700;
        margin-right: 12px;
    }
    
    /* FAQ */
    .faq-item {
        background: white;
        margin-bottom: 16px;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    .faq-question {
        width: 100%;
        padding: 24px;
        background: white;
        border: none;
        text-align: left;
        font-size: 18px;
        font-weight: 600;
        color: #1a202c;
        cursor: pointer;
        display: flex;
        justify-content: space-between;
        align-items: center;
        transition: all 0.3s;
    }
    
    .faq-question:hover {
        background: #f8fafc;
    }
    
    .faq-icon {
        font-size: 24px;
        font-weight: 300;
        color: #667eea;
    }
    
    .faq-answer {
        max-height: 0;
        overflow: hidden;
        transition: max-height 0.3s ease;
    }
    
    .faq-item.active .faq-answer {
        max-height: 500px;
    }
    
    .faq-answer-content {
        padding: 0 24px 24px 24px;
        color: #64748b;
        line-height: 1.8;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .hero h1 {
            font-size: 42px;
        }
        
        .stats {
            grid-template-columns: 1fr;
            gap: 24px;
        }
        
        .features {
            grid-template-columns: 1fr;
        }
        
        .pricing {
            grid-template-columns: 1fr;
        }
        
        .pricing-card.popular {
            transform: scale(1);
        }
    }
</style>
'''
        
        # 定价和auth链接映射
        self.pricing_map = {
            'en': {
                'monthly': '$7',
                'annual': '$5.59',
                'auth': '/en/auth.html',
            },
            'zh': {
                'monthly': 'HK$46',
                'annual': 'HK$37',
                'auth': '/auth.html',
            },
            'ko': {
                'monthly': '₩7998',
                'annual': '₩6398',
                'auth': '/kr/auth.html',
            },
            'ja': {
                'monthly': '¥926',
                'annual': '¥741',
                'auth': '/jp/auth.html',
            },
        }
    
    def detect_language(self, content):
        """检测页面语言"""
        if '免費試用' in content or '立即註冊' in content:
            return 'zh'
        elif '무료 체험' in content or '지금 등록' in content:
            return 'ko'
        elif '無料トライアル' in content or '今すぐ登録' in content:
            return 'ja'
        else:
            return 'en'
    
    def upgrade_file(self, file_path):
        """升级单个文件"""
        try:
            print(f"\n🔧 处理: {file_path.name}")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检测语言
            lang = self.detect_language(content)
            print(f"  🌐 语言: {lang}")
            
            # 备份
            backup_path = str(file_path) + '.backup_v2_design'
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # 1. 替换CSS（移除旧样式，添加v3样式）
            content = re.sub(r'<style>.*?</style>', self.v3_css, content, flags=re.DOTALL)
            
            # 2. 更新定价
            pricing = self.pricing_map[lang]
            content = re.sub(r'\$\d+(\.\d+)?/month', f"{pricing['monthly']}/month", content)
            content = re.sub(r'\$\d+(\.\d+)?\s*/\s*month', f"{pricing['annual']}/month", content)
            
            # 3. 更新auth链接
            content = re.sub(r'href="[^"]*auth\.html"', f'href="{pricing["auth"]}"', content)
            
            # 写入
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"  ✅ 已升级设计")
            self.upgraded_count += 1
            return True
            
        except Exception as e:
            print(f"  ❌ 失败: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def upgrade_all(self):
        """升级所有v2页面"""
        print("🚀 升级所有v2页面设计为v3标准...")
        print("=" * 80)
        
        v2_files = list(self.root_dir.glob('*-v2.html'))
        
        print(f"📊 找到 {len(v2_files)} 个v2页面\n")
        
        for file_path in v2_files:
            if 'backup' in file_path.name:
                continue
            self.upgrade_file(file_path)
        
        print("\n" + "=" * 80)
        print("🎉 设计升级完成！")
        print("=" * 80)
        print(f"\n📊 总计:")
        print(f"   - 找到 {len(v2_files)} 个v2页面")
        print(f"   - 成功升级 {self.upgraded_count} 个页面")

def main():
    root_dir = '/Users/cavlinyeung/ai-bank-parser'
    
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║              🎨 v2设计升级工具                                                ║
║                                                                              ║
║  升级内容:                                                                    ║
║    ✓ v3现代化CSS样式                                                          ║
║    ✓ 正确的本地化定价                                                        ║
║    ✓ 正确的auth.html链接                                                     ║
║                                                                              ║
║  保留内容:                                                                    ║
║    ✓ 原有文字和描述                                                          ║
║    ✓ 页面结构和内容                                                          ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    upgrader = V2DesignUpgrader(root_dir)
    upgrader.upgrade_all()

if __name__ == '__main__':
    main()

