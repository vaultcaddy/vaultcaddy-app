#!/usr/bin/env node
/**
 * 添加缺失的页面到sitemap.xml
 */

const fs = require('fs');
const path = require('path');

// 需要添加的6个页面
const missingPages = [
    'https://vaultcaddy.com/m&t-bank-statement-to-qbo.html',
    'https://vaultcaddy.com/jp/blog/how-to-convert-pdf-bank-statement-to-excel.html',
    'https://vaultcaddy.com/en-gb/blog/pdf-bank-statement-cannot-copy-text-solutions-2025.html',
    'https://vaultcaddy.com/en-au/blog/pdf-bank-statement-cannot-copy-text-solutions-2025.html',
    'https://vaultcaddy.com/en-ca/blog/pdf-bank-statement-cannot-copy-text-solutions-2025.html',
    'https://vaultcaddy.com/kr/blog/ai-invoice-processing-for-smb.html'
];

// 读取sitemap.xml
const sitemapPath = path.join(__dirname, 'sitemap.xml');
const sitemapContent = fs.readFileSync(sitemapPath, 'utf-8');

// 检查哪些页面已经在sitemap中
const alreadyInSitemap = missingPages.filter(url => sitemapContent.includes(url));
const needToAdd = missingPages.filter(url => !sitemapContent.includes(url));

console.log('📊 检查结果:');
console.log(`✅ 已在sitemap中: ${alreadyInSitemap.length} 个`);
console.log(`❌ 需要添加: ${needToAdd.length} 个\n`);

if (needToAdd.length === 0) {
    console.log('✅ 所有页面已在sitemap中，无需添加');
    process.exit(0);
}

// 确定优先级和更新频率
function getPriority(url) {
    if (url.includes('blog')) return '0.8';
    if (url.includes('to-qbo')) return '0.7';
    return '0.6';
}

function getChangeFreq(url) {
    if (url.includes('blog')) return 'weekly';
    return 'monthly';
}

// 生成新的URL条目
const today = new Date().toISOString().split('T')[0];
const newEntries = needToAdd.map(url => {
    const priority = getPriority(url);
    const changefreq = getChangeFreq(url);
    
    return `  <url>
    <loc>${url}</loc>
    <lastmod>${today}</lastmod>
    <changefreq>${changefreq}</changefreq>
    <priority>${priority}</priority>
  </url>`;
}).join('\n');

// 找到</urlset>标签的位置，在之前插入
const urlsetEndIndex = sitemapContent.indexOf('</urlset>');
if (urlsetEndIndex === -1) {
    console.error('❌ 无法找到</urlset>标签');
    process.exit(1);
}

// 插入新条目
const newSitemapContent = 
    sitemapContent.slice(0, urlsetEndIndex) + 
    '\n' + newEntries + '\n' +
    sitemapContent.slice(urlsetEndIndex);

// 保存更新后的sitemap
fs.writeFileSync(sitemapPath, newSitemapContent, 'utf-8');

console.log('✅ 已添加以下页面到sitemap.xml:');
needToAdd.forEach(url => {
    console.log(`   - ${url}`);
});

console.log(`\n✅ sitemap.xml 已更新！`);
console.log(`📋 下一步：在Google Search Console中提交更新的sitemap`);
