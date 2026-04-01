#!/usr/bin/env python3
"""
简化版 OG 图片截图脚本 - 只截图最重要的6个页面

作用：
1. 访问 VaultCaddy 线上网站
2. 截取 Hero 部分
3. 调整为 1200x630px
4. 保存为 OG 图片

依赖：
    pip install playwright pillow
    playwright install chromium

使用方法：
    python3 screenshot_og_images_simple.py
"""

import asyncio
from pathlib import Path
from PIL import Image, ImageEnhance
import os
import sys

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("❌ 缺少依赖包！请先安装：")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    print("运行以下命令：\n")
    print("pip3 install playwright pillow")
    print("playwright install chromium\n")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    sys.exit(1)

# 配置
BASE_URL = "https://vaultcaddy.com"
OUTPUT_DIR = Path(__file__).parent / "images" / "og"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# P0 优先级页面（最重要的6个）
PRIORITY_PAGES = [
    {"path": "/index.html", "selector": ".hero", "name": "og-index"},
    {"path": "/ai-vs-manual-comparison.html", "selector": ".hero", "name": "og-ai-vs-manual-comparison"},
    {"path": "/vaultcaddy-vs-dext.html", "selector": ".hero", "name": "og-vaultcaddy-vs-dext"},
    {"path": "/vaultcaddy-vs-autoentry.html", "selector": ".hero", "name": "og-vaultcaddy-vs-autoentry"},
    {"path": "/hsbc-bank-statement.html", "selector": ".hero", "name": "og-hsbc-bank-statement"},
    {"path": "/hangseng-bank-statement.html", "selector": ".hero", "name": "og-hangseng-bank-statement"},
]


def optimize_image(image_path, target_size=(1200, 630), quality=85):
    """
    优化图片：调整尺寸、锐化、压缩
    
    Args:
        image_path: 原始图片路径
        target_size: 目标尺寸 (width, height)
        quality: JPEG 质量 (1-100)
    
    Returns:
        (output_path, file_size_kb)
    """
    try:
        img = Image.open(image_path)
        
        # 1. 调整尺寸（保持比例，然后裁剪）
        img_ratio = img.width / img.height
        target_ratio = target_size[0] / target_size[1]
        
        if img_ratio > target_ratio:
            # 图片更宽，裁剪左右
            new_height = target_size[1]
            new_width = int(new_height * img_ratio)
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            left = (new_width - target_size[0]) // 2
            img = img.crop((left, 0, left + target_size[0], target_size[1]))
        else:
            # 图片更高，裁剪上下
            new_width = target_size[0]
            new_height = int(new_width / img_ratio)
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            top = (new_height - target_size[1]) // 2
            img = img.crop((0, top, target_size[0], top + target_size[1]))
        
        # 2. 锐化（增强文字清晰度）
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(1.5)
        
        # 3. 对比度增强（让颜色更鲜艳）
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.1)
        
        # 4. 保存为高质量 JPEG
        output_path = image_path.replace('.png', '.jpg')
        img.convert('RGB').save(output_path, 'JPEG', quality=quality, optimize=True)
        
        # 5. 删除原始 PNG
        if output_path != image_path and os.path.exists(image_path):
            os.remove(image_path)
        
        # 6. 检查文件大小
        file_size = os.path.getsize(output_path) / 1024  # KB
        
        return output_path, file_size
        
    except Exception as e:
        print(f"   ❌ 优化失败: {e}")
        return None, 0


async def screenshot_page(page_info, browser):
    """截图单个页面"""
    path = page_info['path']
    selector = page_info['selector']
    name = page_info['name']
    
    try:
        # 创建新页面
        page = await browser.new_page(viewport={'width': 1920, 'height': 1080})
        
        # 访问页面
        url = f"{BASE_URL}{path}"
        print(f"   → 访问: {url}")
        
        try:
            await page.goto(url, wait_until='networkidle', timeout=30000)
        except Exception as e:
            print(f"   ⚠️  加载超时，继续尝试截图: {e}")
        
        # 等待 Hero 部分加载
        try:
            await page.wait_for_selector(selector, timeout=10000)
        except Exception:
            print(f"   ⚠️  未找到选择器 {selector}，尝试截取整个页面")
            selector = 'body'
        
        # 获取元素
        element = await page.query_selector(selector)
        if not element:
            print(f"   ❌ 未找到元素")
            await page.close()
            return False
        
        # 截图
        screenshot_path = OUTPUT_DIR / f"{name}-raw.png"
        await element.screenshot(path=str(screenshot_path))
        print(f"   ✅ 原始截图: {screenshot_path.name}")
        
        # 优化图片
        optimized_path, file_size = optimize_image(str(screenshot_path))
        if optimized_path:
            print(f"   ✅ 优化完成: {Path(optimized_path).name} ({file_size:.0f}KB)")
            
            # 检查尺寸
            img = Image.open(optimized_path)
            if img.size == (1200, 630):
                print(f"   ✓ 尺寸正确: 1200 x 630 px")
            else:
                print(f"   ⚠️  尺寸: {img.width} x {img.height} px")
        
        await page.close()
        return True
        
    except Exception as e:
        print(f"   ❌ 截图失败: {e}")
        return False


async def main():
    """主函数"""
    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("🚀 开始批量截图生成 Open Graph 图片...")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    
    print(f"📂 输出目录: {OUTPUT_DIR}")
    print(f"🌐 网站地址: {BASE_URL}")
    print(f"📋 截图页面: {len(PRIORITY_PAGES)} 个（P0 优先级）\n")
    
    # 启动浏览器
    print("🔧 正在启动浏览器...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        print("✅ 浏览器已启动\n")
        
        success_count = 0
        fail_count = 0
        
        # 逐个截图
        for i, page_info in enumerate(PRIORITY_PAGES, 1):
            print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            print(f"📸 [{i}/{len(PRIORITY_PAGES)}] {page_info['name']}")
            result = await screenshot_page(page_info, browser)
            if result:
                success_count += 1
            else:
                fail_count += 1
            print()
        
        await browser.close()
    
    # 统计
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("📊 截图完成统计：")
    print(f"✅ 成功：{success_count} 个")
    print(f"❌ 失败：{fail_count} 个")
    print(f"📂 保存位置：{OUTPUT_DIR}")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    
    # 列出所有生成的图片
    if success_count > 0:
        print("📁 生成的图片文件：")
        for jpg_file in sorted(OUTPUT_DIR.glob("*.jpg")):
            file_size = os.path.getsize(jpg_file) / 1024
            print(f"   • {jpg_file.name} ({file_size:.0f}KB)")
        print()
    
    # 下一步提示
    print("🎯 下一步：")
    print("1. 查看 images/og/ 目录中的图片")
    print("2. 在 HTML 中添加 OG 标签：")
    print('   <meta property="og:image" content="https://vaultcaddy.com/images/og/og-index.jpg">')
    print('   <meta property="og:image:width" content="1200">')
    print('   <meta property="og:image:height" content="630">')
    print("3. 测试预览：")
    print("   • Facebook Debugger: https://developers.facebook.com/tools/debug/")
    print("   • WhatsApp: 发送链接给自己测试")
    print("\n💡 提示：图片需要上传到网站 /images/og/ 目录才能使用")


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

