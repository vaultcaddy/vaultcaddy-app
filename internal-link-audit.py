#!/usr/bin/env python3
"""
内部链接审计脚本

功能：
1. 扫描所有HTML文件
2. 提取所有内部链接
3. 检测断链（404）
4. 识别孤立页面（入站链接=0）
5. 计算链接深度
6. 生成详细报告

使用方法：
python3 internal-link-audit.py
"""

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup
from collections import defaultdict
import csv

class InternalLinkAuditor:
    def __init__(self, root_dir='.'):
        self.root_dir = root_dir
        self.all_pages = set()
        self.links = defaultdict(list)  # page -> list of links
        self.incoming_links = defaultdict(list)  # page -> list of referring pages
        self.broken_links = []
        self.orphan_pages = []
        
    def find_all_html_files(self):
        """查找所有HTML文件"""
        html_files = []
        
        # 排除目录
        exclude_dirs = {'node_modules', '.git', 'terminals', '__pycache__', '.vscode'}
        
        for root, dirs, files in os.walk(self.root_dir):
            # 移除排除的目录
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            for file in files:
                if file.endswith('.html'):
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, self.root_dir)
                    html_files.append(rel_path)
                    self.all_pages.add(rel_path)
        
        return html_files
    
    def normalize_link(self, link, current_page):
        """规范化链接路径"""
        # 移除锚点
        if '#' in link:
            link = link.split('#')[0]
        
        # 移除查询参数
        if '?' in link:
            link = link.split('?')[0]
        
        # 如果链接为空，返回None
        if not link or link == '':
            return None
        
        # 绝对URL，忽略
        if link.startswith('http://') or link.startswith('https://'):
            return None
        
        # 相对路径转换为绝对路径
        if link.startswith('/'):
            # 从根目录开始
            link = link[1:]
        else:
            # 相对于当前页面
            current_dir = os.path.dirname(current_page)
            link = os.path.normpath(os.path.join(current_dir, link))
        
        return link
    
    def extract_links(self, file_path):
        """提取页面中的所有内部链接"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            soup = BeautifulSoup(content, 'html.parser')
            links = []
            
            # 提取所有<a>标签的href
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                normalized = self.normalize_link(href, os.path.relpath(file_path, self.root_dir))
                if normalized:
                    links.append(normalized)
            
            return links
        except Exception as e:
            print(f"  ❌ 错误处理 {file_path}: {e}")
            return []
    
    def check_broken_links(self):
        """检查断链"""
        for page, links in self.links.items():
            for link in links:
                link_path = os.path.join(self.root_dir, link)
                if not os.path.exists(link_path):
                    self.broken_links.append({
                        'source': page,
                        'broken_link': link
                    })
    
    def find_orphan_pages(self):
        """找出孤立页面（没有入站链接）"""
        # 排除特殊页面
        exclude_pages = {'404.html', 'index.html', 'en/index.html', 'jp/index.html', 'kr/index.html'}
        
        for page in self.all_pages:
            if page not in exclude_pages:
                if len(self.incoming_links[page]) == 0:
                    self.orphan_pages.append(page)
    
    def calculate_link_depth(self, start_page='index.html', max_depth=10):
        """计算页面链接深度（从首页开始）"""
        depths = {start_page: 0}
        queue = [(start_page, 0)]
        visited = set()
        
        while queue:
            current_page, depth = queue.pop(0)
            
            if current_page in visited or depth >= max_depth:
                continue
            
            visited.add(current_page)
            
            # 遍历当前页面的链接
            for link in self.links.get(current_page, []):
                if link not in depths:
                    depths[link] = depth + 1
                    queue.append((link, depth + 1))
        
        return depths
    
    def generate_report(self):
        """生成审计报告"""
        # 计算统计数据
        total_pages = len(self.all_pages)
        total_internal_links = sum(len(links) for links in self.links.values())
        avg_links_per_page = total_internal_links / total_pages if total_pages > 0 else 0
        
        # 链接深度
        depths = self.calculate_link_depth()
        
        print("\n" + "=" * 60)
        print("📊 内部链接审计报告")
        print("=" * 60)
        
        print(f"\n✅ 基本统计：")
        print(f"  - 总页面数：{total_pages}")
        print(f"  - 总内部链接数：{total_internal_links}")
        print(f"  - 平均每页链接数：{avg_links_per_page:.1f}")
        
        print(f"\n❌ 问题发现：")
        print(f"  - 断链数量：{len(self.broken_links)}")
        print(f"  - 孤立页面：{len(self.orphan_pages)}")
        
        if self.broken_links:
            print(f"\n🔴 断链详情（前10个）：")
            for i, broken in enumerate(self.broken_links[:10], 1):
                print(f"  {i}. {broken['source']} → {broken['broken_link']}")
            if len(self.broken_links) > 10:
                print(f"  ... 还有 {len(self.broken_links) - 10} 个断链")
        
        if self.orphan_pages:
            print(f"\n🟡 孤立页面（前10个）：")
            for i, orphan in enumerate(self.orphan_pages[:10], 1):
                print(f"  {i}. {orphan}")
            if len(self.orphan_pages) > 10:
                print(f"  ... 还有 {len(self.orphan_pages) - 10} 个孤立页面")
        
        # 链接深度分析
        print(f"\n📏 链接深度分析：")
        depth_counts = defaultdict(int)
        for page, depth in depths.items():
            depth_counts[depth] += 1
        
        for depth in sorted(depth_counts.keys()):
            print(f"  - 深度 {depth}：{depth_counts[depth]} 页面")
        
        # 入站链接最多的页面
        print(f"\n🔗 入站链接最多的页面（Top 10）：")
        top_pages = sorted(self.incoming_links.items(), key=lambda x: len(x[1]), reverse=True)[:10]
        for i, (page, referring_pages) in enumerate(top_pages, 1):
            print(f"  {i}. {page}: {len(referring_pages)} 入站链接")
        
        # 出站链接最多的页面
        print(f"\n🔗 出站链接最多的页面（Top 10）：")
        top_pages = sorted(self.links.items(), key=lambda x: len(x[1]), reverse=True)[:10]
        for i, (page, links) in enumerate(top_pages, 1):
            print(f"  {i}. {page}: {len(links)} 出站链接")
        
        return {
            'total_pages': total_pages,
            'total_links': total_internal_links,
            'broken_links': len(self.broken_links),
            'orphan_pages': len(self.orphan_pages)
        }
    
    def export_to_csv(self):
        """导出详细报告到CSV"""
        # 导出链接详情
        with open('internal-links-report.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['源页面', '目标链接', '入站链接数'])
            
            for page, links in sorted(self.links.items()):
                for link in links:
                    incoming_count = len(self.incoming_links.get(link, []))
                    writer.writerow([page, link, incoming_count])
        
        print(f"\n✅ 详细报告已导出到：internal-links-report.csv")
        
        # 导出断链
        if self.broken_links:
            with open('broken-links.csv', 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['源页面', '断链'])
                for broken in self.broken_links:
                    writer.writerow([broken['source'], broken['broken_link']])
            print(f"✅ 断链报告已导出到：broken-links.csv")
        
        # 导出孤立页面
        if self.orphan_pages:
            with open('orphan-pages.txt', 'w', encoding='utf-8') as f:
                for orphan in self.orphan_pages:
                    f.write(orphan + '\n')
            print(f"✅ 孤立页面列表已导出到：orphan-pages.txt")
    
    def run(self):
        """运行审计"""
        print("🚀 开始内部链接审计...")
        print("=" * 60)
        
        # 1. 找到所有HTML文件
        print(f"\n📁 扫描HTML文件...")
        html_files = self.find_all_html_files()
        print(f"  找到 {len(html_files)} 个HTML文件")
        
        # 2. 提取所有链接
        print(f"\n🔍 提取内部链接...")
        for html_file in html_files:
            file_path = os.path.join(self.root_dir, html_file)
            links = self.extract_links(file_path)
            self.links[html_file] = links
            
            # 记录入站链接
            for link in links:
                self.incoming_links[link].append(html_file)
        
        print(f"  提取了 {sum(len(links) for links in self.links.values())} 个内部链接")
        
        # 3. 检查断链
        print(f"\n🔎 检查断链...")
        self.check_broken_links()
        print(f"  发现 {len(self.broken_links)} 个断链")
        
        # 4. 找出孤立页面
        print(f"\n🔎 查找孤立页面...")
        self.find_orphan_pages()
        print(f"  发现 {len(self.orphan_pages)} 个孤立页面")
        
        # 5. 生成报告
        self.generate_report()
        
        # 6. 导出CSV
        self.export_to_csv()
        
        print("\n" + "=" * 60)
        print("🎉 审计完成！")
        print("=" * 60)

def main():
    auditor = InternalLinkAuditor()
    auditor.run()

if __name__ == '__main__':
    main()

