#!/usr/bin/env python3
"""
生成所有页面的 OG 图片 - SEO 优化版

特点：
1. 文件名包含 SEO 关键词
2. 自动生成所有重要页面
3. 优化图片质量和大小
4. 支持多语言版本

使用方法：
    python3 generate_all_og_images_seo.py
"""

import asyncio
from pathlib import Path
from PIL import Image, ImageEnhance
import os
import sys

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("\n❌ 缺少依赖包！请先安装：")
    print("   pip3 install playwright pillow")
    print("   playwright install chromium")
    sys.exit(1)

# 配置
BASE_URL = "https://vaultcaddy.com"
OUTPUT_DIR = Path(__file__).parent / "images" / "og"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 所有页面列表（SEO 优化文件名）
ALL_PAGES = [
    # ============ 中文版 ============
    # 首页
    {"path": "/index.html", "selector": ".hero", 
     "seo_name": "vaultcaddy-bank-statement-receipt-invoice-ai-hong-kong"},
    
    # 对比页面
    {"path": "/ai-vs-manual-comparison.html", "selector": ".hero",
     "seo_name": "ai-vs-manual-dext-autoentry-comparison-hong-kong-2025"},
    
    {"path": "/vaultcaddy-vs-dext.html", "selector": ".hero",
     "seo_name": "vaultcaddy-vs-dext-receipt-bank-price-comparison-hk"},
    
    {"path": "/vaultcaddy-vs-autoentry.html", "selector": ".hero",
     "seo_name": "vaultcaddy-vs-autoentry-bookkeeping-automation-hk"},
    
    {"path": "/vaultcaddy-vs-receiptbank.html", "selector": ".hero",
     "seo_name": "vaultcaddy-vs-receipt-bank-accounting-software-hk"},
    
    # 银行特定页面（香港）
    {"path": "/hsbc-bank-statement.html", "selector": ".hero",
     "seo_name": "hsbc-bank-statement-to-excel-converter-hong-kong"},
    
    {"path": "/hangseng-bank-statement.html", "selector": ".hero",
     "seo_name": "hang-seng-bank-statement-pdf-to-excel-hk"},
    
    {"path": "/bochk-bank-statement.html", "selector": ".hero",
     "seo_name": "bank-of-china-hk-statement-ocr-converter"},
    
    {"path": "/citibank-bank-statement.html", "selector": ".hero",
     "seo_name": "citibank-hong-kong-statement-excel-converter"},
    
    {"path": "/sc-bank-statement.html", "selector": ".hero",
     "seo_name": "standard-chartered-hk-bank-statement-automation"},
    
    {"path": "/dbs-bank-statement.html", "selector": ".hero",
     "seo_name": "dbs-bank-hong-kong-statement-processing-tool"},
    
    {"path": "/bea-bank-statement.html", "selector": ".hero",
     "seo_name": "bank-of-east-asia-statement-to-excel-hk"},
    
    {"path": "/dahsing-bank-statement.html", "selector": ".hero",
     "seo_name": "dah-sing-bank-statement-converter-hong-kong"},
    
    {"path": "/citic-bank-statement.html", "selector": ".hero",
     "seo_name": "citic-bank-hong-kong-statement-ocr-tool"},
    
    {"path": "/bankcomm-bank-statement.html", "selector": ".hero",
     "seo_name": "bank-of-communications-hk-statement-automation"},
    
    # ============ 英文版 ============
    {"path": "/en/index.html", "selector": ".hero",
     "seo_name": "bank-statement-receipt-invoice-ai-ocr-hong-kong-en"},
    
    {"path": "/en/ai-vs-manual-comparison.html", "selector": ".hero",
     "seo_name": "ai-vs-manual-bookkeeping-comparison-hong-kong-2025-en"},
    
    {"path": "/en/vaultcaddy-vs-dext.html", "selector": ".hero",
     "seo_name": "vaultcaddy-vs-dext-receipt-bank-comparison-en"},
    
    {"path": "/en/vaultcaddy-vs-autoentry.html", "selector": ".hero",
     "seo_name": "vaultcaddy-vs-autoentry-accounting-automation-en"},
    
    {"path": "/en/vaultcaddy-vs-receiptbank.html", "selector": ".hero",
     "seo_name": "vaultcaddy-vs-receipt-bank-price-comparison-en"},
    
    {"path": "/en/hsbc-bank-statement.html", "selector": ".hero",
     "seo_name": "hsbc-bank-statement-converter-hong-kong-english"},
    
    {"path": "/en/hangseng-bank-statement.html", "selector": ".hero",
     "seo_name": "hang-seng-bank-statement-excel-converter-en"},
    
    # ============ 日文版 ============
    {"path": "/jp/index.html", "selector": ".hero",
     "seo_name": "bank-statement-ai-converter-hong-kong-japanese"},
    
    {"path": "/jp/ai-vs-manual-comparison.html", "selector": ".hero",
     "seo_name": "ai-accounting-automation-comparison-japan"},
    
    {"path": "/jp/vaultcaddy-vs-dext.html", "selector": ".hero",
     "seo_name": "vaultcaddy-vs-dext-price-comparison-japanese"},
    
    {"path": "/jp/vaultcaddy-vs-autoentry.html", "selector": ".hero",
     "seo_name": "vaultcaddy-vs-autoentry-bookkeeping-jp"},
    
    {"path": "/jp/vaultcaddy-vs-receiptbank.html", "selector": ".hero",
     "seo_name": "vaultcaddy-vs-receipt-bank-japan"},
    
    # ============ 韩文版 ============
    {"path": "/kr/index.html", "selector": ".hero",
     "seo_name": "bank-statement-ai-converter-hong-kong-korean"},
    
    {"path": "/kr/ai-vs-manual-comparison.html", "selector": ".hero",
     "seo_name": "ai-accounting-automation-comparison-korea"},
    
    {"path": "/kr/vaultcaddy-vs-dext.html", "selector": ".hero",
     "seo_name": "vaultcaddy-vs-dext-price-comparison-korean"},
    
    {"path": "/kr/vaultcaddy-vs-autoentry.html", "selector": ".hero",
     "seo_name": "vaultcaddy-vs-autoentry-bookkeeping-kr"},
    
    {"path": "/kr/vaultcaddy-vs-receiptbank.html", "selector": ".hero",
     "seo_name": "vaultcaddy-vs-receipt-bank-korea"},
]


def optimize_image(image_path, target_size=(1200, 630), quality=85):
    """优化图片：调整尺寸、锐化、压缩"""
    try:
        img = Image.open(image_path)
        
        # 调整尺寸
        img_ratio = img.width / img.height
        target_ratio = target_size[0] / target_size[1]
        
        if img_ratio > target_ratio:
            new_height = target_size[1]
            new_width = int(new_height * img_ratio)
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            left = (new_width - target_size[0]) // 2
            img = img.crop((left, 0, left + target_size[0], target_size[1]))
        else:
            new_width = target_size[0]
            new_height = int(new_width / img_ratio)
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            top = (new_height - target_size[1]) // 2
            img = img.crop((0, top, target_size[0], top + target_size[1]))
        
        # 锐化和对比度增强
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(1.5)
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.1)
        
        # 保存为 JPEG
        output_path = image_path.replace('.png', '.jpg')
        img.convert('RGB').save(output_path, 'JPEG', quality=quality, optimize=True)
        
        # 删除原始 PNG
        if output_path != image_path and os.path.exists(image_path):
            os.remove(image_path)
        
        file_size = os.path.getsize(output_path) / 1024
        return output_path, file_size
        
    except Exception as e:
        print(f"   ❌ 优化失败: {e}")
        return None, 0


async def screenshot_page(page_info, browser):
    """截图单个页面"""
    path = page_info['path']
    selector = page_info['selector']
    seo_name = page_info['seo_name']
    
    try:
        page = await browser.new_page(viewport={'width': 1920, 'height': 1080})
        
        url = f"{BASE_URL}{path}"
        print(f"   → 访问: {url}")
        
        try:
            await page.goto(url, wait_until='networkidle', timeout=30000)
        except Exception as e:
            print(f"   ⚠️  加载超时，继续尝试截图")
        
        # 等待 Hero 部分
        try:
            await page.wait_for_selector(selector, timeout=10000)
        except Exception:
            print(f"   ⚠️  未找到 {selector}，截取整个页面")
            selector = 'body'
        
        element = await page.query_selector(selector)
        if not element:
            print(f"   ❌ 未找到元素")
            await page.close()
            return False
        
        # 截图（使用 SEO 优化文件名）
        screenshot_path = OUTPUT_DIR / f"{seo_name}-og-image.png"
        await element.screenshot(path=str(screenshot_path))
        print(f"   ✅ 截图: {screenshot_path.name}")
        
        # 优化图片
        optimized_path, file_size = optimize_image(str(screenshot_path))
        if optimized_path:
            final_name = f"{seo_name}-og-image.jpg"
            print(f"   ✅ 优化: {final_name} ({file_size:.0f}KB)")
        
        await page.close()
        return True
        
    except Exception as e:
        print(f"   ❌ 失败: {e}")
        return False


async def main():
    """主函数"""
    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("🚀 生成所有页面的 OG 图片（SEO 优化版）")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    
    print(f"📂 输出目录: {OUTPUT_DIR}")
    print(f"🌐 网站地址: {BASE_URL}")
    print(f"📋 总页面数: {len(ALL_PAGES)} 个")
    print(f"💡 文件名: SEO 优化（包含关键词）\n")
    
    print("🔧 正在启动浏览器...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        print("✅ 浏览器已启动\n")
        
        success_count = 0
        fail_count = 0
        
        # 逐个截图
        for i, page_info in enumerate(ALL_PAGES, 1):
            print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            print(f"📸 [{i}/{len(ALL_PAGES)}] {page_info['seo_name']}")
            result = await screenshot_page(page_info, browser)
            if result:
                success_count += 1
            else:
                fail_count += 1
            print()
        
        await browser.close()
    
    # 统计
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("📊 生成完成统计：")
    print(f"✅ 成功：{success_count} 个")
    print(f"❌ 失败：{fail_count} 个")
    print(f"📂 位置：{OUTPUT_DIR}")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    
    # 列出所有图片
    if success_count > 0:
        print("📁 生成的图片文件：")
        total_size = 0
        for jpg_file in sorted(OUTPUT_DIR.glob("*-og-image.jpg")):
            file_size = os.path.getsize(jpg_file) / 1024
            total_size += file_size
            print(f"   • {jpg_file.name} ({file_size:.0f}KB)")
        print(f"\n📦 总大小：{total_size:.0f}KB ({total_size/1024:.1f}MB)")
        print()
    
    # 下一步
    print("🎯 下一步：")
    print("1. 上传图片到网站 /images/og/ 目录")
    print("2. 在 HTML 中添加 OG 标签：")
    print('   <meta property="og:image" content="https://vaultcaddy.com/images/og/[文件名].jpg">')
    print("3. 测试：Facebook Debugger https://developers.facebook.com/tools/debug/")
    print("\n💡 SEO 优化文件名已包含关键词，有助于图片 SEO！")


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

