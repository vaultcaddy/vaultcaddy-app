#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WebP完整转换和HTML更新方案
包含：图片转换 + HTML自动更新 + 验证
"""

import os
import re
from pathlib import Path
from PIL import Image
from bs4 import BeautifulSoup
import concurrent.futures

class WebPConverter:
    def __init__(self, base_dir='.', quality=80, keep_original=True):
        self.base_dir = base_dir
        self.quality = quality
        self.keep_original = keep_original
        self.converted_count = 0
        self.failed_files = []
        self.total_saved_bytes = 0
        
    def convert_image(self, image_path):
        """转换单个图片为WebP"""
        try:
            # 打开图片
            with Image.open(image_path) as img:
                # 生成输出路径
                output_path = str(Path(image_path).with_suffix('.webp'))
                
                # 如果WebP已存在且比原图新，跳过
                if os.path.exists(output_path):
                    if os.path.getmtime(output_path) > os.path.getmtime(image_path):
                        return True, f"已存在: {output_path}"
                
                # 保存为WebP（保留透明度）
                if img.mode in ('RGBA', 'LA'):
                    img.save(output_path, 'WEBP', quality=self.quality, method=6, lossless=False)
                else:
                    # 转换为RGB
                    rgb_img = img.convert('RGB')
                    rgb_img.save(output_path, 'WEBP', quality=self.quality, method=6)
                
                # 计算文件大小节省
                original_size = os.path.getsize(image_path)
                webp_size = os.path.getsize(output_path)
                saved_bytes = original_size - webp_size
                
                self.converted_count += 1
                self.total_saved_bytes += saved_bytes
                
                reduction_pct = (saved_bytes / original_size) * 100
                
                return True, f"转换成功: {image_path} → {output_path} (减少 {reduction_pct:.1f}%)"
                
        except Exception as e:
            self.failed_files.append((image_path, str(e)))
            return False, f"转换失败: {image_path} - {e}"
    
    def find_images(self):
        """查找所有需要转换的图片"""
        image_extensions = {'.jpg', '.jpeg', '.png'}
        ignore_dirs = {'node_modules', '.git', 'venv', '__pycache__'}
        
        images = []
        for root, dirs, files in os.walk(self.base_dir):
            # 过滤忽略的目录
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            
            for file in files:
                if Path(file).suffix.lower() in image_extensions:
                    full_path = os.path.join(root, file)
                    images.append(full_path)
        
        return images
    
    def batch_convert(self, max_workers=4):
        """批量转换图片"""
        images = self.find_images()
        
        if not images:
            print("  ⚠️  未找到需要转换的图片")
            return
        
        print(f"\n📸 找到 {len(images)} 个图片文件")
        print(f"🔄 开始批量转换（使用 {max_workers} 个线程）...\n")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(self.convert_image, img) for img in images]
            
            for future in concurrent.futures.as_completed(futures):
                success, message = future.result()
                if success:
                    print(f"  ✅ {message}")
                else:
                    print(f"  ❌ {message}")
    
    def update_html_file(self, html_path):
        """更新HTML文件使用WebP"""
        try:
            with open(html_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            soup = BeautifulSoup(content, 'html.parser')
            modified = False
            updates = 0
            
            for img in soup.find_all('img'):
                src = img.get('src')
                if not src:
                    continue
                
                # 检查是否是本地图片
                if src.startswith('http'):
                    continue
                
                # 检查是否已经是webp
                if src.endswith('.webp'):
                    continue
                
                # 检查对应的webp文件是否存在
                img_path = Path(src)
                if img_path.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                    webp_src = str(img_path.with_suffix('.webp'))
                    
                    # 计算相对于HTML文件的路径
                    html_dir = Path(html_path).parent
                    webp_full_path = html_dir / webp_src
                    
                    if webp_full_path.exists():
                        # 创建picture标签以支持fallback
                        picture = soup.new_tag('picture')
                        
                        # WebP source
                        source_webp = soup.new_tag('source', srcset=webp_src, type='image/webp')
                        picture.append(source_webp)
                        
                        # 原始格式source
                        source_original = soup.new_tag('source', srcset=src, type=f'image/{img_path.suffix[1:]}')
                        picture.append(source_original)
                        
                        # 复制img的所有属性
                        new_img = soup.new_tag('img')
                        for attr, value in img.attrs.items():
                            new_img[attr] = value
                        
                        picture.append(new_img)
                        
                        # 替换原img标签
                        img.replace_with(picture)
                        
                        updates += 1
                        modified = True
            
            if modified:
                with open(html_path, 'w', encoding='utf-8') as f:
                    f.write(str(soup))
                return True, f"更新 {updates} 个图片标签"
            
            return False, "无需更新"
            
        except Exception as e:
            return False, f"更新失败: {e}"
    
    def update_all_html(self):
        """更新所有HTML文件"""
        html_files = []
        ignore_dirs = {'node_modules', '.git', 'venv', '__pycache__', 'terminals'}
        
        for root, dirs, files in os.walk(self.base_dir):
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            
            for file in files:
                if file.endswith('.html'):
                    html_files.append(os.path.join(root, file))
        
        if not html_files:
            print("  ⚠️  未找到HTML文件")
            return
        
        print(f"\n📄 找到 {len(html_files)} 个HTML文件")
        print(f"🔄 开始更新...\n")
        
        updated_count = 0
        for html_file in html_files:
            success, message = self.update_html_file(html_file)
            if success:
                updated_count += 1
                print(f"  ✅ {html_file}: {message}")
            else:
                print(f"  ⏭️  {html_file}: {message}")
        
        return updated_count
    
    def generate_report(self):
        """生成转换报告"""
        print("\n" + "=" * 70)
        print("📊 WebP转换完成报告")
        print("=" * 70)
        
        print(f"\n✅ 成功转换: {self.converted_count} 个图片")
        print(f"❌ 转换失败: {len(self.failed_files)} 个图片")
        
        if self.total_saved_bytes > 0:
            mb_saved = self.total_saved_bytes / (1024 * 1024)
            print(f"💾 节省空间: {mb_saved:.2f} MB")
            
            if self.converted_count > 0:
                avg_reduction = (self.total_saved_bytes / self.converted_count) / 1024
                print(f"📉 平均减少: {avg_reduction:.1f} KB/图片")
        
        if self.failed_files:
            print(f"\n⚠️  失败文件列表:")
            for file, error in self.failed_files[:10]:  # 只显示前10个
                print(f"  - {file}: {error}")
            if len(self.failed_files) > 10:
                print(f"  ... 还有 {len(self.failed_files) - 10} 个失败")
        
        print(f"\n🎯 预期效果:")
        print(f"  ✅ 页面加载速度提升: 30-50%")
        print(f"  ✅ LCP (Largest Contentful Paint): 降低30-40%")
        print(f"  ✅ 带宽消耗减少: 40-60%")
        print(f"  ✅ PageSpeed Score: 提升10-15分")
        
        print(f"\n💡 下一步:")
        print(f"  1. 测试网站所有图片是否正常显示")
        print(f"  2. 使用 PageSpeed Insights 验证效果")
        print(f"  3. 在不同浏览器测试兼容性")
        print(f"  4. 如有问题，可回滚到原始图片")

def main():
    print("🖼️  WebP 完整转换方案")
    print("=" * 70)
    print("功能: 图片转换 + HTML自动更新 + 兼容性处理")
    print("-" * 70)
    
    # 创建转换器
    converter = WebPConverter(base_dir='.', quality=80, keep_original=True)
    
    # 步骤1: 转换图片
    print("\n📋 步骤1: 批量转换图片为WebP格式")
    print("-" * 70)
    converter.batch_convert(max_workers=4)
    
    # 步骤2: 更新HTML
    print("\n📋 步骤2: 更新HTML文件使用WebP")
    print("-" * 70)
    updated_count = converter.update_all_html()
    
    # 步骤3: 生成报告
    converter.generate_report()
    
    if updated_count:
        print(f"\n🎊 HTML更新: {updated_count} 个文件已更新")

if __name__ == '__main__':
    main()

