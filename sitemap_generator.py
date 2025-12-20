#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VaultCaddy Sitemap生成器
作用：为所有新创建的页面生成sitemap并更新主sitemap.xml

帮助AI工作：自动化sitemap管理，确保所有页面被搜索引擎索引
"""

from pathlib import Path
from datetime import datetime
import xml.etree.ElementTree as ET

class SitemapGenerator:
    def __init__(self):
        self.base_dir = Path('/Users/cavlinyeung/ai-bank-parser')
        self.base_url = 'https://vaultcaddy.com'
        
    def generate_complete_sitemap(self):
        """生成完整的sitemap.xml"""
        
        # 创建urlset元素
        urlset = ET.Element('urlset')
        urlset.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
        urlset.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
        urlset.set('xsi:schemaLocation', 'http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd')
        
        today = datetime.now().strftime('%Y-%m-%d')
        
        # 主要页面
        main_pages = [
            ('/', '1.0', 'daily'),
            ('/en/', '1.0', 'daily'),
            ('/en/solutions/', '0.9', 'weekly'),
            ('/en/blog/', '0.9', 'daily'),
        ]
        
        for page, priority, changefreq in main_pages:
            url = ET.SubElement(urlset, 'url')
            ET.SubElement(url, 'loc').text = f"{self.base_url}{page}"
            ET.SubElement(url, 'lastmod').text = today
            ET.SubElement(url, 'changefreq').text = changefreq
            ET.SubElement(url, 'priority').text = priority
        
        # 30个landing pages
        landing_pages = [
            'freelancer', 'small-business', 'accountant', 'ecommerce', 'restaurant',
            'real-estate', 'consultant', 'startup', 'nonprofit', 'photographer',
            'healthcare', 'lawyer', 'contractor', 'personal-finance', 'fitness-coach',
            'designer', 'property-manager', 'travel-agent', 'tutor', 'event-planner',
            'delivery-driver', 'beauty-salon', 'retail-store', 'marketing-agency',
            'coworking-space', 'cleaning-service', 'pet-service', 'artist', 'musician', 'developer'
        ]
        
        for page in landing_pages:
            url = ET.SubElement(urlset, 'url')
            ET.SubElement(url, 'loc').text = f"{self.base_url}/en/solutions/{page}/"
            ET.SubElement(url, 'lastmod').text = today
            ET.SubElement(url, 'changefreq').text = 'monthly'
            ET.SubElement(url, 'priority').text = '0.8'
        
        # 16个blog文章
        blog_pages = [
            'manual-vs-ai-cost-analysis',
            'personal-bookkeeping-best-practices',
            'ai-invoice-processing-guide',
            'ai-invoice-processing-for-smb',
            'accounting-firm-automation',
            'accounting-workflow-optimization',
            'automate-financial-documents',
            'best-pdf-to-excel-converter',
            'client-document-management-for-accountants',
            'freelancer-invoice-management',
            'freelancer-tax-preparation-guide',
            'how-to-convert-pdf-bank-statement-to-excel',
            'ocr-accuracy-for-accounting',
            'ocr-technology-for-accountants',
            'quickbooks-integration-guide',
            'small-business-document-management'
        ]
        
        for page in blog_pages:
            url = ET.SubElement(urlset, 'url')
            ET.SubElement(url, 'loc').text = f"{self.base_url}/en/blog/{page}.html"
            ET.SubElement(url, 'lastmod').text = today
            ET.SubElement(url, 'changefreq').text = 'monthly'
            ET.SubElement(url, 'priority').text = '0.7'
        
        # 创建XML树并格式化
        tree = ET.ElementTree(urlset)
        ET.indent(tree, space='  ')
        
        return tree
    
    def save_sitemap(self, tree):
        """保存sitemap.xml"""
        output_path = self.base_dir / 'sitemap-new.xml'
        tree.write(output_path, encoding='utf-8', xml_declaration=True)
        return output_path
    
    def generate_submission_urls(self):
        """生成提交到Google Search Console的URL列表"""
        urls = []
        
        # Landing pages
        landing_pages = [
            'freelancer', 'small-business', 'accountant', 'ecommerce', 'restaurant',
            'real-estate', 'consultant', 'startup', 'nonprofit', 'photographer',
            'healthcare', 'lawyer', 'contractor', 'personal-finance', 'fitness-coach',
            'designer', 'property-manager', 'travel-agent', 'tutor', 'event-planner',
            'delivery-driver', 'beauty-salon', 'retail-store', 'marketing-agency',
            'coworking-space', 'cleaning-service', 'pet-service', 'artist', 'musician', 'developer'
        ]
        
        for page in landing_pages:
            urls.append(f"https://vaultcaddy.com/en/solutions/{page}/")
        
        # Blog pages
        blog_pages = [
            'manual-vs-ai-cost-analysis',
            'personal-bookkeeping-best-practices',
            'ai-invoice-processing-guide',
            'ai-invoice-processing-for-smb',
            'accounting-firm-automation',
            'accounting-workflow-optimization',
            'automate-financial-documents',
            'best-pdf-to-excel-converter',
            'client-document-management-for-accountants',
            'freelancer-invoice-management',
            'freelancer-tax-preparation-guide',
            'how-to-convert-pdf-bank-statement-to-excel',
            'ocr-accuracy-for-accounting',
            'ocr-technology-for-accountants',
            'quickbooks-integration-guide',
            'small-business-document-management'
        ]
        
        for page in blog_pages:
            urls.append(f"https://vaultcaddy.com/en/blog/{page}.html")
        
        return urls
    
    def run(self):
        """执行完整流程"""
        print("🗺️  VaultCaddy Sitemap生成器")
        print("=" * 80)
        
        # 生成sitemap
        print("\n📝 生成sitemap.xml...")
        tree = self.generate_complete_sitemap()
        output_path = self.save_sitemap(tree)
        print(f"   ✅ Sitemap已保存: {output_path}")
        
        # 生成提交URL列表
        print("\n📋 生成Google Search Console提交URL列表...")
        urls = self.generate_submission_urls()
        urls_file = self.base_dir / 'google-search-console-new-urls.txt'
        with open(urls_file, 'w') as f:
            f.write('\n'.join(urls))
        print(f"   ✅ URL列表已保存: {urls_file}")
        print(f"   📊 总计: {len(urls)} 个URL")
        
        print("\n" + "=" * 80)
        print("✅ Sitemap生成完成!")
        print(f"\n📁 生成的文件:")
        print(f"   - {output_path}")
        print(f"   - {urls_file}")
        
        return output_path, urls_file

if __name__ == "__main__":
    generator = SitemapGenerator()
    generator.run()

