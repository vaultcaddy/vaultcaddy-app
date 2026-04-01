#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片WebP转换脚本
功能：批量将PNG/JPG图片转换为WebP格式
优势：文件大小减少30-50%，加载速度提升40-60%
"""

import os
import sys
from pathlib import Path
from PIL import Image
import shutil

def convert_to_webp(image_path, output_path=None, quality=85):
    """
    将图片转换为WebP格式
    
    Args:
        image_path: 输入图片路径
        output_path: 输出WebP路径（如不指定，将替换原文件）
        quality: WebP质量（0-100，默认85）
    """
    try:
        # 打开图片
        img = Image.open(image_path)
        
        # 如果是RGBA模式，转换为RGB（WebP不支持透明度的RGB）
        if img.mode == 'RGBA':
            # 创建白色背景
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])  # 使用alpha通道作为mask
            img = background
        elif img.mode not in ('RGB', 'L'):
            img = img.convert('RGB')
        
        # 确定输出路径
        if output_path is None:
            output_path = str(Path(image_path).with_suffix('.webp'))
        
        # 保存为WebP
        img.save(output_path, 'WEBP', quality=quality, method=6)
        
        # 获取文件大小
        original_size = os.path.getsize(image_path)
        webp_size = os.path.getsize(output_path)
        reduction = ((original_size - webp_size) / original_size) * 100
        
        return {
            'success': True,
            'original_path': image_path,
            'webp_path': output_path,
            'original_size': original_size,
            'webp_size': webp_size,
            'reduction': reduction
        }
        
    except Exception as e:
        return {
            'success': False,
            'original_path': image_path,
            'error': str(e)
        }

def find_images(directory, extensions=('.png', '.jpg', '.jpeg', '.PNG', '.JPG', '.JPEG')):
    """
    递归查找所有图片文件
    
    Args:
        directory: 搜索目录
        extensions: 图片扩展名元组
    
    Returns:
        图片路径列表
    """
    image_files = []
    
    # 排除的目录
    exclude_dirs = {
        'node_modules', '.git', '.vscode', '__pycache__', 
        'venv', 'dist', 'build', '.next', '.nuxt'
    }
    
    for root, dirs, files in os.walk(directory):
        # 过滤排除的目录
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in files:
            if file.endswith(extensions):
                # 跳过已经是WebP的文件
                if not file.endswith('.webp'):
                    image_files.append(os.path.join(root, file))
    
    return image_files

def batch_convert_to_webp(directory='.', quality=85, keep_original=True, dry_run=False):
    """
    批量转换目录下的所有图片为WebP格式
    
    Args:
        directory: 目标目录
        quality: WebP质量
        keep_original: 是否保留原文件
        dry_run: 是否只预览不执行
    """
    print(f"🔍 开始扫描目录: {directory}")
    print(f"⚙️  WebP质量: {quality}")
    print(f"💾 保留原文件: {'是' if keep_original else '否'}")
    print(f"🧪 预览模式: {'是' if dry_run else '否'}")
    print("-" * 60)
    
    # 查找所有图片
    image_files = find_images(directory)
    print(f"📊 找到 {len(image_files)} 个图片文件\n")
    
    if not image_files:
        print("❌ 未找到任何图片文件")
        return
    
    # 统计数据
    total_original_size = 0
    total_webp_size = 0
    success_count = 0
    error_count = 0
    skipped_count = 0
    
    # 转换每个图片
    for i, image_path in enumerate(image_files, 1):
        # 检查是否已有WebP版本
        webp_path = str(Path(image_path).with_suffix('.webp'))
        if os.path.exists(webp_path):
            print(f"⏭️  [{i}/{len(image_files)}] 跳过 {os.path.basename(image_path)} (已有WebP版本)")
            skipped_count += 1
            continue
        
        print(f"🔄 [{i}/{len(image_files)}] 转换 {os.path.basename(image_path)}...", end=' ')
        
        if dry_run:
            print("(预览模式，未实际转换)")
            continue
        
        result = convert_to_webp(image_path, quality=quality)
        
        if result['success']:
            total_original_size += result['original_size']
            total_webp_size += result['webp_size']
            success_count += 1
            
            print(f"✅ 完成!")
            print(f"   原始: {result['original_size'] / 1024:.1f} KB → WebP: {result['webp_size'] / 1024:.1f} KB (减少 {result['reduction']:.1f}%)")
            
            # 如果不保留原文件，删除原文件
            if not keep_original:
                os.remove(image_path)
                print(f"   🗑️  已删除原文件")
        else:
            error_count += 1
            print(f"❌ 失败: {result['error']}")
    
    # 打印总结
    print("\n" + "=" * 60)
    print("📊 转换完成总结")
    print("=" * 60)
    print(f"✅ 成功转换: {success_count} 个")
    print(f"❌ 转换失败: {error_count} 个")
    print(f"⏭️  跳过: {skipped_count} 个")
    print(f"📁 总文件数: {len(image_files)} 个")
    
    if success_count > 0:
        total_reduction = ((total_original_size - total_webp_size) / total_original_size) * 100
        print(f"\n💾 存储节省:")
        print(f"   原始总大小: {total_original_size / 1024 / 1024:.2f} MB")
        print(f"   WebP总大小: {total_webp_size / 1024 / 1024:.2f} MB")
        print(f"   节省空间: {(total_original_size - total_webp_size) / 1024 / 1024:.2f} MB ({total_reduction:.1f}%)")
        
        print(f"\n🚀 预期性能提升:")
        print(f"   加载速度提升: 40-60%")
        print(f"   带宽节省: {total_reduction:.1f}%")
        print(f"   Core Web Vitals (LCP): 可能提升 0.5-1.5秒")

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='批量将图片转换为WebP格式')
    parser.add_argument('directory', nargs='?', default='.', help='目标目录（默认：当前目录）')
    parser.add_argument('-q', '--quality', type=int, default=85, help='WebP质量 0-100（默认：85）')
    parser.add_argument('-k', '--keep', action='store_true', help='保留原文件')
    parser.add_argument('-d', '--dry-run', action='store_true', help='预览模式（不实际转换）')
    
    args = parser.parse_args()
    
    print("🖼️  图片WebP转换工具")
    print("=" * 60)
    
    # 检查PIL是否支持WebP
    try:
        img = Image.new('RGB', (1, 1))
        img.save('/tmp/test.webp', 'WEBP')
        os.remove('/tmp/test.webp')
    except Exception as e:
        print("❌ 错误: PIL不支持WebP格式")
        print("   请安装: pip install Pillow")
        print("   如果已安装Pillow，可能需要重新编译支持WebP")
        sys.exit(1)
    
    # 执行转换
    batch_convert_to_webp(
        directory=args.directory,
        quality=args.quality,
        keep_original=args.keep,
        dry_run=args.dry_run
    )

if __name__ == '__main__':
    main()

