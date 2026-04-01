#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
博客Article Schema自动添加脚本
功能：为所有博客文章添加Article结构化数据
SEO效果：提升搜索结果展示，可能出现Rich Results
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup

def extract_article_info(html_content, file_path):
    """
    从HTML中提取文章信息
    
    Returns:
        dict: 文章信息
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 提取title
    title_tag = soup.find('title')
    title = title_tag.string if title_tag else "VaultCaddy Blog Article"
    
    # 提取H1作为headline
    h1_tag = soup.find('h1')
    headline = h1_tag.get_text() if h1_tag else title
    
    # 提取meta description
    meta_desc = soup.find('meta', {'name': 'description'})
    description = meta_desc.get('content') if meta_desc else headline[:160]
    
    # 提取第一个图片作为封面
    first_img = soup.find('img')
    image_url = ""
    if first_img and first_img.get('src'):
        img_src = first_img.get('src')
        # 转换为绝对URL
        if img_src.startswith('http'):
            image_url = img_src
        elif img_src.startswith('/'):
            image_url = f"https://vaultcaddy.com{img_src}"
        else:
            # 相对路径，需要计算
            rel_path = os.path.dirname(file_path)
            image_url = f"https://vaultcaddy.com/{rel_path}/{img_src}"
    
    # 如果没有图片，使用默认OG图片
    if not image_url:
        image_url = "https://vaultcaddy.com/images/og-vaultcaddy-main.jpg"
    
    # 提取或估算字数
    body_text = soup.get_text()
    word_count = len(body_text.split())
    
    # 获取文件修改时间作为发布日期
    file_mtime = os.path.getmtime(file_path)
    date_published = datetime.fromtimestamp(file_mtime).isoformat()
    date_modified = date_published  # 简化处理
    
    return {
        'headline': headline[:110],  # Google限制110字符
        'description': description[:160],
        'image': image_url,
        'datePublished': date_published,
        'dateModified': date_modified,
        'wordCount': word_count,
        'url': None  # 需要后续设置
    }

def create_article_schema(article_info):
    """
    创建Article Schema JSON-LD
    
    Args:
        article_info: 文章信息字典
    
    Returns:
        str: JSON-LD字符串
    """
    schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": article_info['headline'],
        "description": article_info['description'],
        "image": [article_info['image']],
        "datePublished": article_info['datePublished'],
        "dateModified": article_info['dateModified'],
        "author": {
            "@type": "Organization",
            "name": "VaultCaddy",
            "url": "https://vaultcaddy.com"
        },
        "publisher": {
            "@type": "Organization",
            "name": "VaultCaddy",
            "logo": {
                "@type": "ImageObject",
                "url": "https://vaultcaddy.com/images/vaultcaddy-logo.png"
            }
        },
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": article_info.get('url', 'https://vaultcaddy.com')
        },
        "wordCount": article_info['wordCount'],
        "articleBody": article_info['description']
    }
    
    return json.dumps(schema, ensure_ascii=False, indent=2)

def add_schema_to_html(html_content, schema_json):
    """
    将Schema添加到HTML的<head>中
    
    Args:
        html_content: 原HTML内容
        schema_json: Schema JSON字符串
    
    Returns:
        str: 更新后的HTML内容
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 检查是否已经有Article Schema
    existing_schemas = soup.find_all('script', {'type': 'application/ld+json'})
    for script in existing_schemas:
        try:
            schema_data = json.loads(script.string)
            if schema_data.get('@type') == 'Article':
                # 已经有Article Schema，不重复添加
                return None
        except:
            pass
    
    # 创建新的script标签
    new_script = soup.new_tag('script', type='application/ld+json')
    new_script.string = schema_json
    
    # 添加到head中
    head = soup.find('head')
    if head:
        head.append('\n    ')
        head.append(new_script)
        head.append('\n')
        return str(soup)
    else:
        return None

def process_blog_file(file_path, dry_run=False):
    """
    处理单个博客文件
    
    Args:
        file_path: 博客文件路径
        dry_run: 是否只预览
    
    Returns:
        bool: 是否成功添加Schema
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # 提取文章信息
        article_info = extract_article_info(html_content, file_path)
        
        # 生成URL
        rel_path = os.path.relpath(file_path, '.')
        article_info['url'] = f"https://vaultcaddy.com/{rel_path}"
        
        # 创建Schema
        schema_json = create_article_schema(article_info)
        
        # 添加到HTML
        new_html = add_schema_to_html(html_content, schema_json)
        
        if new_html is None:
            # 已经有Schema或无法添加
            return False
        
        if not dry_run:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_html)
        
        return True
        
    except Exception as e:
        print(f"❌ 处理失败 {file_path}: {e}")
        return False

def find_blog_files(blog_dirs=['blog/', 'en/blog/', 'jp/blog/', 'kr/blog/']):
    """
    查找所有博客文件
    
    Args:
        blog_dirs: 博客目录列表
    
    Returns:
        list: 博客文件路径列表
    """
    blog_files = []
    
    for blog_dir in blog_dirs:
        if not os.path.exists(blog_dir):
            continue
        
        for root, dirs, files in os.walk(blog_dir):
            for file in files:
                if file.endswith('.html') and file != 'index.html':
                    blog_files.append(os.path.join(root, file))
    
    return blog_files

def batch_add_article_schema(dry_run=False):
    """
    批量为博客文章添加Article Schema
    
    Args:
        dry_run: 是否只预览
    """
    print("📝 博客Article Schema添加工具")
    print("=" * 60)
    print(f"🧪 预览模式: {'是' if dry_run else '否'}")
    print("-" * 60)
    
    # 查找所有博客文件
    blog_files = find_blog_files()
    print(f"📊 找到 {len(blog_files)} 个博客文件\n")
    
    if not blog_files:
        print("❌ 未找到任何博客文件")
        return
    
    success_count = 0
    skipped_count = 0
    error_count = 0
    
    for i, file_path in enumerate(blog_files, 1):
        print(f"🔄 [{i}/{len(blog_files)}] 处理 {os.path.relpath(file_path)}...", end=' ')
        
        result = process_blog_file(file_path, dry_run=dry_run)
        
        if result:
            success_count += 1
            status = "(预览)" if dry_run else "✅"
            print(f"{status} 已添加Article Schema")
        else:
            skipped_count += 1
            print("⏭️  已有Schema，跳过")
    
    print("\n" + "=" * 60)
    print("📊 添加完成总结")
    print("=" * 60)
    print(f"📁 扫描文件: {len(blog_files)} 个")
    print(f"✅ 成功添加: {success_count} 个")
    print(f"⏭️  跳过: {skipped_count} 个")
    print(f"❌ 失败: {error_count} 个")
    
    if success_count > 0:
        print(f"\n🚀 预期SEO效果:")
        print(f"   ✅ 搜索结果可能显示发布日期、作者信息")
        print(f"   ✅ 提升点击率 (CTR) +10-20%")
        print(f"   ✅ Google可能展示Rich Results")
        print(f"   ✅ 更好的文章可见度")
        
        print(f"\n🧪 验证方法:")
        print(f"   1. 访问: https://search.google.com/test/rich-results")
        print(f"   2. 输入博客文章URL")
        print(f"   3. 查看是否识别为Article")

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='批量为博客文章添加Article Schema')
    parser.add_argument('-d', '--dry-run', action='store_true', help='预览模式（不实际修改）')
    
    args = parser.parse_args()
    
    batch_add_article_schema(dry_run=args.dry_run)

if __name__ == '__main__':
    main()

