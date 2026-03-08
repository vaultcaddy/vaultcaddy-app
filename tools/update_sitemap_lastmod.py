#!/usr/bin/env python3
"""
更新sitemap.xml的lastmod日期
作用: 将Phase 2优化的40个页面的lastmod更新为今天，告诉Google内容已更新
"""

from datetime import datetime
import xml.etree.ElementTree as ET

def update_sitemap_lastmod():
    """更新sitemap.xml中的lastmod日期"""
    
    # 读取现有sitemap
    try:
        tree = ET.parse('sitemap.xml')
        root = tree.getroot()
    except FileNotFoundError:
        print("❌ 错误：未找到sitemap.xml文件")
        return False
    
    # 今天的日期
    today = datetime.now().strftime('%Y-%m-%d')
    
    # 需要更新lastmod的页面（Phase 2优化的40个页面）
    updated_pages = [
        # 中文银行页面（10个）
        'hsbc-bank-statement.html',
        'hangseng-bank-statement.html',
        'bochk-bank-statement.html',
        'sc-bank-statement.html',
        'dbs-bank-statement.html',
        'bea-bank-statement.html',
        'citibank-bank-statement.html',
        'dahsing-bank-statement.html',
        'citic-bank-statement.html',
        'bankcomm-bank-statement.html',
        
        # 英文银行页面（10个）
        'en/hsbc-bank-statement.html',
        'en/hangseng-bank-statement.html',
        'en/bochk-bank-statement.html',
        'en/sc-bank-statement.html',
        'en/dbs-bank-statement.html',
        'en/bea-bank-statement.html',
        'en/citibank-bank-statement.html',
        'en/dahsing-bank-statement.html',
        'en/citic-bank-statement.html',
        'en/bankcomm-bank-statement.html',
        
        # 日文银行页面（10个）
        'ja/hsbc-bank-statement.html',
        'ja/hangseng-bank-statement.html',
        'ja/bochk-bank-statement.html',
        'ja/sc-bank-statement.html',
        'ja/dbs-bank-statement.html',
        'ja/bea-bank-statement.html',
        'ja/citibank-bank-statement.html',
        'ja/dahsing-bank-statement.html',
        'ja/citic-bank-statement.html',
        'ja/bankcomm-bank-statement.html',
        
        # 韩文银行页面（10个）
        'ko/hsbc-bank-statement.html',
        'ko/hangseng-bank-statement.html',
        'ko/bochk-bank-statement.html',
        'ko/sc-bank-statement.html',
        'ko/dbs-bank-statement.html',
        'ko/bea-bank-statement.html',
        'ko/citibank-bank-statement.html',
        'ko/dahsing-bank-statement.html',
        'ko/citic-bank-statement.html',
        'ko/bankcomm-bank-statement.html',
    ]
    
    # 命名空间
    namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    
    updated_count = 0
    
    # 遍历所有URL元素
    for url in root.findall('ns:url', namespace):
        loc = url.find('ns:loc', namespace)
        if loc is not None:
            url_text = loc.text
            
            # 检查是否是需要更新的页面
            for page in updated_pages:
                if url_text.endswith(page):
                    lastmod = url.find('ns:lastmod', namespace)
                    if lastmod is not None:
                        lastmod.text = today
                        updated_count += 1
                        print(f"  ✅ 更新: {page}")
                    break
    
    # 保存更新后的sitemap
    tree.write('sitemap.xml', encoding='utf-8', xml_declaration=True)
    
    print()
    print(f"✅ 成功更新 {updated_count} 个页面的lastmod日期为 {today}")
    
    return True

def main():
    """主函数"""
    
    print("=" * 80)
    print("📅 更新Sitemap.xml的lastmod日期")
    print("=" * 80)
    print()
    print("Phase 2优化的40个页面将更新lastmod为今天")
    print("这会告诉Google这些页面的内容已更新，建议重新抓取")
    print()
    
    if update_sitemap_lastmod():
        print()
        print("=" * 80)
        print("✅ Sitemap更新完成！")
        print("=" * 80)
        print()
        print("📍 下一步:")
        print("  1. 上传更新后的 sitemap.xml 到网站根目录")
        print("  2. 在Google Search Console中点击 sitemap.xml 右侧的「重新提交」")
        print("  3. 或者直接访问：https://search.google.com/search-console")
        print()
        print("💡 提示：更新sitemap后，Google通常会在几天内重新抓取")
        print("   如果想立即生效，建议使用「网址审查」手动请求索引")
    else:
        print()
        print("❌ 更新失败，请检查sitemap.xml文件是否存在")

if __name__ == '__main__':
    main()

