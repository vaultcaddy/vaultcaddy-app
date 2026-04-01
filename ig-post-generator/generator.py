#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VaultCaddy IG Post 自動生成器
一鍵生成 5 張 IG 圖片，包括背景、內容、文案和標籤
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import json
from datetime import datetime

class IGPostGenerator:
    """IG Post 自動生成器"""
    
    def __init__(self, output_dir='output'):
        """初始化生成器
        
        Args:
            output_dir: 輸出目錄
        """
        self.output_dir = output_dir
        self.width = 1080  # IG 方形帖子標準寬度
        self.height = 1080  # IG 方形帖子標準高度
        
        # 品牌配色
        self.colors = {
            'primary': '#6B5FCF',      # 主紫色
            'primary_light': '#9B87E8', # 淺紫色
            'accent': '#FFC107',        # 黃色強調
            'success': '#10B981',       # 綠色
            'text': '#1F2937',          # 深灰文字
            'text_light': '#6B7280',    # 淺灰文字
            'white': '#FFFFFF',
            'bg_beige': '#F5F3EF'       # 米色背景
        }
        
        # 創建輸出目錄
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"✅ IG Post 生成器已初始化")
        print(f"   輸出目錄: {output_dir}")
        print(f"   圖片尺寸: {self.width}x{self.height}px")
    
    def hex_to_rgb(self, hex_color):
        """轉換 HEX 顏色到 RGB
        
        Args:
            hex_color: HEX 顏色碼（如 '#6B5FCF'）
            
        Returns:
            RGB 元組
        """
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def create_gradient_background(self, color1, color2, direction='diagonal'):
        """創建漸變背景
        
        Args:
            color1: 起始顏色（HEX）
            color2: 結束顏色（HEX）
            direction: 漸變方向（diagonal/vertical/horizontal）
            
        Returns:
            PIL Image 對象
        """
        img = Image.new('RGB', (self.width, self.height))
        draw = ImageDraw.Draw(img)
        
        rgb1 = self.hex_to_rgb(color1)
        rgb2 = self.hex_to_rgb(color2)
        
        if direction == 'diagonal':
            for i in range(self.height):
                ratio = i / self.height
                r = int(rgb1[0] + (rgb2[0] - rgb1[0]) * ratio)
                g = int(rgb1[1] + (rgb2[1] - rgb1[1]) * ratio)
                b = int(rgb1[2] + (rgb2[2] - rgb1[2]) * ratio)
                draw.line([(0, i), (self.width, i)], fill=(r, g, b))
        
        return img
    
    def create_solid_background(self, color):
        """創建純色背景
        
        Args:
            color: 顏色（HEX）
            
        Returns:
            PIL Image 對象
        """
        img = Image.new('RGB', (self.width, self.height), self.hex_to_rgb(color))
        return img
    
    def add_text(self, img, text, position, font_size=60, color='#FFFFFF', align='center', bold=False):
        """添加文字到圖片
        
        Args:
            img: PIL Image 對象
            text: 要添加的文字
            position: 位置 (x, y) 或 'center'
            font_size: 字體大小
            color: 文字顏色（HEX）
            align: 對齊方式
            bold: 是否粗體
            
        Returns:
            更新後的 Image 對象
        """
        draw = ImageDraw.Draw(img)
        
        # 嘗試使用系統字體（macOS）
        font_paths = [
            '/System/Library/AssetsV2/com_apple_MobileAsset_Font7/3419f2a427639ad8c8e139149a287865a90fa17e.asset/AssetData/PingFang.ttc',
            '/System/Library/Fonts/PingFang.ttc',
            '/System/Library/Fonts/STHeiti Medium.ttc',
            '/System/Library/Fonts/Helvetica.ttc'
        ]
        
        font = None
        for font_path in font_paths:
            try:
                font = ImageFont.truetype(font_path, font_size, index=0)
                break
            except:
                continue
        
        if font is None:
            # 如果找不到字體，使用默認字體
            font = ImageFont.load_default()
        
        # 計算文字位置
        if position == 'center':
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            x = (self.width - text_width) // 2
            y = (self.height - text_height) // 2
            position = (x, y)
        
        draw.text(position, text, fill=self.hex_to_rgb(color), font=font)
        
        return img
    
    def add_multiline_text(self, img, lines, start_y, font_size=50, color='#FFFFFF', line_spacing=20):
        """添加多行文字
        
        Args:
            img: PIL Image 對象
            lines: 文字行列表
            start_y: 起始 Y 坐標
            font_size: 字體大小
            color: 文字顏色
            line_spacing: 行間距
            
        Returns:
            更新後的 Image 對象
        """
        draw = ImageDraw.Draw(img)
        
        font_paths = [
            '/System/Library/AssetsV2/com_apple_MobileAsset_Font7/3419f2a427639ad8c8e139149a287865a90fa17e.asset/AssetData/PingFang.ttc',
            '/System/Library/Fonts/PingFang.ttc',
            '/System/Library/Fonts/STHeiti Medium.ttc',
            '/System/Library/Fonts/Helvetica.ttc'
        ]
        
        font = None
        for font_path in font_paths:
            try:
                font = ImageFont.truetype(font_path, font_size, index=0)
                break
            except:
                continue
        
        if font is None:
            font = ImageFont.load_default()
        
        y = start_y
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            x = (self.width - text_width) // 2
            draw.text((x, y), line, fill=self.hex_to_rgb(color), font=font)
            y += font_size + line_spacing
        
        return img
    
    def generate_post_1_intro(self):
        """生成第 1 張：品牌介紹（痛點）
        
        基於圖1：你的時間值幾多錢？
        """
        print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("📸 生成第 1 張：痛點展示")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        # 創建米色背景
        img = self.create_solid_background(self.colors['bg_beige'])
        
        # 添加主標題
        self.add_multiline_text(
            img,
            lines=['你的時間', '值幾多錢？'],
            start_y=250,
            font_size=90,
            color=self.colors['text']
        )
        
        # 添加副標題
        self.add_multiline_text(
            img,
            lines=[
                '想像一下：',
                '每個月花 40 小時',
                '手動輸入發票、收據和銀行對帳',
                '單。'
            ],
            start_y=550,
            font_size=40,
            color=self.colors['text_light'],
            line_spacing=15
        )
        
        # 添加底部強調
        self.add_text(
            img,
            '💰 但真正的成本不只是時間...',
            (540, 900),
            font_size=38,
            color=self.colors['text']
        )
        
        # 保存
        output_path = os.path.join(self.output_dir, '01_痛點展示.png')
        img.save(output_path, quality=95)
        print(f"✅ 第 1 張已生成: {output_path}")
        
        return output_path
    
    def generate_post_2_benefits(self):
        """生成第 2 張：免費試用優惠
        
        基於圖2：立即免費試用
        """
        print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("📸 生成第 2 張：免費試用優惠")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        # 創建米色背景
        img = self.create_solid_background(self.colors['bg_beige'])
        draw = ImageDraw.Draw(img)
        
        # 添加禮物圖標（簡化版，用文字代替）
        self.add_text(img, '🎁', (540, 150), font_size=120)
        
        # 主標題
        self.add_text(img, '立即免費試用', (540, 320), font_size=80, color=self.colors['text'])
        
        # 副標題
        self.add_multiline_text(
            img,
            lines=[
                '針對香港銀行對賬單及收據處理',
                '低至 HKD 0.5/頁'
            ],
            start_y=450,
            font_size=42,
            color=self.colors['text']
        )
        
        # 優惠內容
        self.add_text(img, '免費試用包含：', (540, 600), font_size=40, color=self.colors['text'])
        
        self.add_multiline_text(
            img,
            lines=[
                '✅ 20 頁免費轉換（無需信用卡）',
                '',
                '✅ 完整功能體驗',
                '',
                '✅ 即時處理，立即看到效果'
            ],
            start_y=680,
            font_size=36,
            color=self.colors['success'],
            line_spacing=10
        )
        
        # 底部 CTA
        self.add_text(img, '無需預約，2 分鐘開始使用', (540, 980), font_size=34, color=self.colors['text_light'])
        
        # 保存
        output_path = os.path.join(self.output_dir, '02_免費試用優惠.png')
        img.save(output_path, quality=95)
        print(f"✅ 第 2 張已生成: {output_path}")
        
        return output_path
    
    def generate_post_3_cost_comparison(self):
        """生成第 3 張：成本對比
        
        人手處理 vs AI 自動化
        """
        print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("📸 生成第 3 張：成本對比")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        img = self.create_solid_background(self.colors['bg_beige'])
        
        # 標題
        self.add_multiline_text(
            img,
            lines=['人手處理 vs', 'AI 自動化'],
            start_y=120,
            font_size=70,
            color=self.colors['text']
        )
        
        # 人手處理部分
        self.add_multiline_text(
            img,
            lines=[
                '人手處理 HK$12,000/月：',
                '40 小時/月',
                '（每份文檔 12 分鐘）'
            ],
            start_y=350,
            font_size=38,
            color=self.colors['text'],
            line_spacing=10
        )
        
        # VS
        self.add_text(img, 'VS', (540, 550), font_size=60, color=self.colors['text_light'])
        
        # AI 自動化部分
        self.add_multiline_text(
            img,
            lines=[
                'AI 自動化（HK$46/月）：',
                '2 小時/月',
                '（每份文檔 10 秒）'
            ],
            start_y=650,
            font_size=38,
            color=self.colors['primary']
        )
        
        # 結論
        self.add_multiline_text(
            img,
            lines=[
                '節省 38 小時/月',
                '效率提升 24 倍！',
                '',
                '✅ 節省 HK$11,954/月'
            ],
            start_y=820,
            font_size=42,
            color=self.colors['success'],
            line_spacing=15
        )
        
        output_path = os.path.join(self.output_dir, '03_成本對比.png')
        img.save(output_path, quality=95)
        print(f"✅ 第 3 張已生成: {output_path}")
        
        return output_path
    
    def generate_post_4_accuracy(self):
        """生成第 4 張：準確率對比"""
        print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("📸 生成第 4 張：準確率對比")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        img = self.create_solid_background(self.colors['bg_beige'])
        
        # 標題
        self.add_text(img, '錯誤率對比', (540, 150), font_size=80, color=self.colors['text'])
        
        # 人手處理
        self.add_multiline_text(
            img,
            lines=[
                '人手處理錯誤率：',
                '5-10%',
                '需要重新檢查和修正'
            ],
            start_y=320,
            font_size=42,
            color=self.colors['text'],
            line_spacing=15
        )
        
        # VS
        self.add_text(img, 'VS', (540, 550), font_size=60, color=self.colors['text_light'])
        
        # AI 自動化
        self.add_multiline_text(
            img,
            lines=[
                'AI 自動化錯誤率：',
                '< 2%',
                'AI 準確度 98%+'
            ],
            start_y=650,
            font_size=42,
            color=self.colors['primary']
        )
        
        # 結論
        self.add_multiline_text(
            img,
            lines=[
                '✅ 減少 70% 錯誤',
                '提升數據品質！'
            ],
            start_y=870,
            font_size=48,
            color=self.colors['success'],
            line_spacing=15
        )
        
        output_path = os.path.join(self.output_dir, '04_準確率對比.png')
        img.save(output_path, quality=95)
        print(f"✅ 第 4 張已生成: {output_path}")
        
        return output_path
    
    def generate_post_5_cta(self):
        """生成第 5 張：CTA 行動呼籲（基於圖2 - 免費試用）"""
        print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("📸 生成第 5 張：CTA 行動呼籲")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        # 創建紫色漸變背景
        img = self.create_gradient_background(
            self.colors['primary'],
            self.colors['primary_light']
        )
        
        # Logo（用文字代替）
        self.add_text(img, 'V', (540, 180), font_size=120, color=self.colors['white'])
        
        # 品牌名稱
        self.add_text(img, 'VaultCaddy', (540, 320), font_size=72, color=self.colors['white'])
        self.add_text(img, 'AI 銀行對賬單處理', (540, 410), font_size=54, color=self.colors['white'])
        
        # 副標題
        self.add_multiline_text(
            img,
            lines=[
                '香港會計師首選',
                '免費試用 20 頁'
            ],
            start_y=520,
            font_size=36,
            color=self.colors['white'],
            line_spacing=10
        )
        
        # 三大特點
        self.add_multiline_text(
            img,
            lines=[
                '⚡ 10秒處理',
                '✓ 98%準確率',
                '💰 HKD 0.5/頁'
            ],
            start_y=660,
            font_size=42,
            color=self.colors['white'],
            line_spacing=20
        )
        
        # CTA
        self.add_text(img, '立即試用', (540, 880), font_size=50, color=self.colors['accent'])
        
        # 底部提示
        self.add_text(img, '掃描 QR Code 開始 →', (540, 980), font_size=28, color=self.colors['white'])
        
        # TODO: 添加 QR Code（需要 qrcode 庫）
        
        output_path = os.path.join(self.output_dir, '05_CTA行動呼籲.png')
        img.save(output_path, quality=95)
        print(f"✅ 第 5 張已生成: {output_path}")
        
        return output_path
    
    def generate_caption_and_tags(self):
        """生成貼文文案和標籤
        
        Returns:
            dict: 包含 caption 和 hashtags
        """
        print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("📝 生成貼文文案和標籤")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        caption = """💡 還在花 40 小時手動處理銀行對賬單？

VaultCaddy AI 只需 10 秒！⚡

我們專為香港中小企和會計師打造：

✅ 10秒處理完成（效率提升 24x）
✅ 98%+ 準確率（錯誤減少 70%）
✅ HKD 0.5/頁（成本降低 99%）

🎁 免費試用 20 頁
無需信用卡，2分鐘開始

👉 訪問 VaultCaddy.com
或掃描最後一張圖的 QR Code

讓 AI 為你工作，把時間用在更重要的事上！

━━━━━━━━━━━━━━━━━━

#VaultCaddy #AI自動化 #財務管理 #會計軟件 #銀行對賬單
#香港創業 #香港中小企 #香港會計 #HongKongBusiness #HKStartup
#會計師 #簿記 #財務自動化 #數碼轉型 #FinTech
#時間管理 #效率提升 #成本節省 #業務增長 #中小企方案
#人工智能 #機器學習 #OCR技術 #文檔處理 #AITechnology
#會計科技 #智能會計 #企業管理 #商業工具 #SaaS"""
        
        # 保存文案到文件
        caption_file = os.path.join(self.output_dir, 'caption.txt')
        with open(caption_file, 'w', encoding='utf-8') as f:
            f.write(caption)
        
        print(f"✅ 貼文文案已生成: {caption_file}")
        
        return {
            'caption': caption,
            'file': caption_file
        }
    
    def generate_all(self):
        """生成所有 IG Post（一鍵生成）
        
        Returns:
            dict: 包含所有生成文件的路徑
        """
        print("\n" + "="*60)
        print("🚀 VaultCaddy IG Post 自動生成器")
        print("="*60)
        print(f"\n⏰ 開始時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        results = {
            'images': [],
            'caption': None,
            'timestamp': datetime.now().isoformat()
        }
        
        # 生成 5 張圖片
        results['images'].append(self.generate_post_1_intro())
        results['images'].append(self.generate_post_2_benefits())
        results['images'].append(self.generate_post_3_cost_comparison())
        results['images'].append(self.generate_post_4_accuracy())
        results['images'].append(self.generate_post_5_cta())
        
        # 生成文案
        caption_data = self.generate_caption_and_tags()
        results['caption'] = caption_data['file']
        
        # 保存生成報告
        report = {
            'generated_at': results['timestamp'],
            'images': results['images'],
            'caption': results['caption'],
            'total_images': len(results['images'])
        }
        
        report_file = os.path.join(self.output_dir, 'generation_report.json')
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print("\n" + "="*60)
        print("🎉 生成完成！")
        print("="*60)
        print(f"\n📊 生成總結:")
        print(f"   圖片數量: {len(results['images'])} 張")
        print(f"   輸出目錄: {self.output_dir}")
        print(f"   生成報告: {report_file}")
        print(f"\n📁 生成的文件:")
        for i, img_path in enumerate(results['images'], 1):
            print(f"   {i}. {os.path.basename(img_path)}")
        print(f"   6. {os.path.basename(results['caption'])}")
        
        print(f"\n⏰ 完成時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("\n🎯 下一步:")
        print("   1. 檢查生成的圖片")
        print("   2. 在手機上預覽效果")
        print("   3. 根據需要調整文案")
        print("   4. 發布到 Instagram")
        
        return results


def main():
    """主函數"""
    # 創建生成器
    generator = IGPostGenerator(output_dir='ig-posts')
    
    # 一鍵生成所有內容
    results = generator.generate_all()
    
    print("\n✅ 所有文件已生成！")
    print(f"📂 查看輸出: {os.path.abspath('ig-posts')}")


if __name__ == '__main__':
    main()

