#!/usr/bin/env python3
"""
批量截图生成 Open Graph 图片

作用：
1. 自动访问每个 landing page
2. 截取 Hero 部分
3. 调整为 1200x630px
4. 保存为 OG 图片
5. 自动优化（压缩、锐化）

依赖：
    pip install playwright pillow
    playwright install chromium

使用方法：
    python3 batch_screenshot_og_images.py
"""

import asyncio
from pathlib import Path
from PIL import Image, ImageEnhance
import os

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("❌ 请先安装依赖：")
    print("   pip install playwright pillow")
    print("   playwright install chromium")
    exit(1)

# 配置
BASE_URL = "https://vaultcaddy.com"  # 使用线上网站
OUTPUT_DIR = Path(__file__).parent / "images" / "og"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 需要截图的页面列表
PAGES = [
    # 主要对比页面
    {"path": "/ai-vs-manual-comparison.html", "selector": ".hero", "name": "ai-vs-manual-comparison"},
    {"path": "/vaultcaddy-vs-dext.html", "selector": ".hero", "name": "vaultcaddy-vs-dext"},
    {"path": "/vaultcaddy-vs-autoentry.html", "selector": ".hero", "name": "vaultcaddy-vs-autoentry"},
    {"path": "/vaultcaddy-vs-receiptbank.html", "selector": ".hero", "name": "vaultcaddy-vs-receiptbank"},
    
    # 首页
    {"path": "/index.html", "selector": ".hero", "name": "index"},
    
    # 银行特定页面（香港）
    {"path": "/hsbc-bank-statement.html", "selector": ".hero", "name": "hsbc-bank-statement"},
    {"path": "/hangseng-bank-statement.html", "selector": ".hero", "name": "hangseng-bank-statement"},
    {"path": "/bochk-bank-statement.html", "selector": ".hero", "name": "bochk-bank-statement"},
    {"path": "/citibank-bank-statement.html", "selector": ".hero", "name": "citibank-bank-statement"},
    {"path": "/sc-bank-statement.html", "selector": ".hero", "name": "sc-bank-statement"},
    {"path": "/dbs-bank-statement.html", "selector": ".hero", "name": "dbs-bank-statement"},
    {"path": "/bea-bank-statement.html", "selector": ".hero", "name": "bea-bank-statement"},
    {"path": "/dahsing-bank-statement.html", "selector": ".hero", "name": "dahsing-bank-statement"},
    {"path": "/citic-bank-statement.html", "selector": ".hero", "name": "citic-bank-statement"},
    {"path": "/bankcomm-bank-statement.html", "selector": ".hero", "name": "bankcomm-bank-statement"},
    
    # 英文版
    {"path": "/en/index.html", "selector": ".hero", "name": "en-index"},
    {"path": "/en/ai-vs-manual-comparison.html", "selector": ".hero", "name": "en-ai-vs-manual-comparison"},
    {"path": "/en/vaultcaddy-vs-dext.html", "selector": ".hero", "name": "en-vaultcaddy-vs-dext"},
    {"path": "/en/hsbc-bank-statement.html", "selector": ".hero", "name": "en-hsbc-bank-statement"},
    {"path": "/en/hangseng-bank-statement.html", "selector": ".hero", "name": "en-hangseng-bank-statement"},
    
    # 日文版
    {"path": "/jp/index.html", "selector": ".hero", "name": "jp-index"},
    {"path": "/jp/ai-vs-manual-comparison.html", "selector": ".hero", "name": "jp-ai-vs-manual-comparison"},
    {"path": "/jp/vaultcaddy-vs-dext.html", "selector": ".hero", "name": "jp-vaultcaddy-vs-dext"},
    
    # 韩文版
    {"path": "/kr/index.html", "selector": ".hero", "name": "kr-index"},
    {"path": "/kr/ai-vs-manual-comparison.html", "selector": ".hero", "name": "kr-ai-vs-manual-comparison"},
    {"path": "/kr/vaultcaddy-vs-dext.html", "selector": ".hero", "name": "kr-vaultcaddy-vs-dext"},
]


def optimize_image(image_path, target_size=(1200, 630), quality=85):
    """
    优化图片：调整尺寸、锐化、压缩
    
    Args:
        image_path: 原始图片路径
        target_size: 目标尺寸 (width, height)
        quality: JPEG 质量 (1-100)
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
        img = enhancer.enhance(1.5)  # 1.5倍锐化
        
        # 3. 对比度增强（让颜色更鲜艳）
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.1)  # 1.1倍对比度
        
        # 4. 保存为高质量 JPEG
        output_path = image_path.replace('.png', '.jpg')
        img.convert('RGB').save(output_path, 'JPEG', quality=quality, optimize=True)
        
        # 5. 删除原始 PNG（如果不同）
        if output_path != image_path and os.path.exists(image_path):
            os.remove(image_path)
        
        # 6. 检查文件大小
        file_size = os.path.getsize(output_path) / 1024  # KB
        if file_size > 1024:  # > 1MB
            print(f"   ⚠️  文件较大（{file_size:.0f}KB），建议降低质量")
        
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
        print(f"\n📸 正在截图: {path}")
        
        # 创建新页面
        page = await browser.new_page(viewport={'width': 1920, 'height': 1080})
        
        # 访问页面
        url = f"{BASE_URL}{path}"
        print(f"   → 访问: {url}")
        await page.goto(url, wait_until='networkidle', timeout=30000)
        
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
        
        await page.close()
        return True
        
    except Exception as e:
        print(f"   ❌ 截图失败: {e}")
        return False


async def main():
    """主函数"""
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("🚀 开始批量截图生成 Open Graph 图片...")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    
    print(f"📂 输出目录: {OUTPUT_DIR}")
    print(f"🌐 基础URL: {BASE_URL}")
    print(f"📋 需要截图: {len(PAGES)} 个页面\n")
    
    # 启动浏览器
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        print("✅ 浏览器已启动\n")
        
        success_count = 0
        fail_count = 0
        
        # 逐个截图
        for i, page_info in enumerate(PAGES, 1):
            print(f"[{i}/{len(PAGES)}]", end=" ")
            result = await screenshot_page(page_info, browser)
            if result:
                success_count += 1
            else:
                fail_count += 1
        
        await browser.close()
    
    # 统计
    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("📊 截图完成统计：")
    print(f"✅ 成功：{success_count} 个")
    print(f"❌ 失败：{fail_count} 个")
    print(f"📂 保存位置：{OUTPUT_DIR}")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    
    # 下一步提示
    print("🎯 下一步：")
    print("1. 检查 images/og/ 目录中的图片")
    print("2. 如果满意，上传到网站 /images/ 目录")
    print("3. 更新 HTML 中的 OG 图片路径：")
    print('   <meta property="og:image" content="https://vaultcaddy.com/images/og/[文件名].jpg">')
    print("4. 使用 Facebook Debugger 测试：https://developers.facebook.com/tools/debug/")
    print("\n💡 提示：如果需要调整截图范围，修改脚本中的 selector 参数")


if __name__ == '__main__':
    asyncio.run(main())

