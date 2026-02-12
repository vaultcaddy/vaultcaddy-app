#!/usr/bin/env node
/**
 * 修复未索引页面问题
 * 
 * 问题：125个页面"已检索但未建立索引"
 * 原因分析：
 * 1. 页面可能不在sitemap中
 * 2. 页面内容质量不足
 * 3. 缺少内部链接
 * 4. 页面加载速度慢
 * 
 * 解决方案：
 * 1. 检查并添加缺失页面到sitemap
 * 2. 验证页面内容质量
 * 3. 添加内部链接
 */

const fs = require('fs');
const path = require('path');

// 未索引的页面列表（从用户提供的数据）
const unindexedPages = [
    'https://vaultcaddy.com/kr/maybank-bank-statement-simple.html',
    'https://vaultcaddy.com/kr/scb-thai-bank-statement-simple.html',
    'https://vaultcaddy.com/citibank-bank-statement-simple.html',
    'https://vaultcaddy.com/kr/hangseng-bank-statement-simple.html',
    'https://vaultcaddy.com/convert-bank-pdf-to-qbo.html',
    'https://vaultcaddy.com/bendigo-bank-statement-to-qbo.html',
    'https://vaultcaddy.com/zh-HK/hang-seng-bank-statement-to-qbo.html',
    'https://vaultcaddy.com/huntington-bank-statement-to-qbo.html',
    'https://vaultcaddy.com/boc-hong-kong-statement-to-qbo.html',
    'https://vaultcaddy.com/permanent-tsb-statement-to-qbo.html',
    'https://vaultcaddy.com/uob-hong-kong-statement-to-qbo.html',
    'https://vaultcaddy.com/bmo-bank-statement-to-qbo.html',
    'https://vaultcaddy.com/what-is-qbo-file-format.html',
    'https://vaultcaddy.com/comerica-statement-to-qbo.html',
    'https://vaultcaddy.com/barclays-statement-to-qbo.html',
    'https://vaultcaddy.com/bank-of-nova-scotia-statement-to-qbo.html',
    'https://vaultcaddy.com/rcbc-bank-statement-to-qbo.html',
    'https://vaultcaddy.com/convert-pdf-bank-statement-to-qbo-format.html',
    'https://vaultcaddy.com/zh-HK/standard-chartered-hk-statement-to-qbo.html',
    'https://vaultcaddy.com/jp/shinsei-bank-statement-to-qbo.html',
    'https://vaultcaddy.com/kr/wellsfargo-bank-statement-simple.html',
    'https://vaultcaddy.com/kr/shinhan-bank-statement-to-qbo.html',
    'https://vaultcaddy.com/truist-bank-statement-to-qbo.html',
    'https://vaultcaddy.com/revolut-statement-to-qbo.html',
    'https://vaultcaddy.com/dbs-bank-statement-to-qbo.html',
    'https://vaultcaddy.com/eastwest-bank-statement-to-qbo.html',
    'https://vaultcaddy.com/bank-of-america-statement-to-qbo.html',
    'https://vaultcaddy.com/ulster-bank-statement-to-qbo.html',
    'https://vaultcaddy.com/scotiabank-statement-to-qbo.html',
    'https://vaultcaddy.com/fifth-third-bank-statement-to-qbo.html',
    'https://vaultcaddy.com/mizrahi-tefahot-statement-to-qbo.html',
    'https://vaultcaddy.com/hsbc-hong-kong-statement-to-qbo.html',
    'https://vaultcaddy.com/monzo-statement-to-qbo.html',
    'https://vaultcaddy.com/nab-australia-statement-to-qbo.html',
    'https://vaultcaddy.com/dubai-islamic-bank-statement-to-qbo.html',
    'https://vaultcaddy.com/starling-bank-statement-to-qbo.html',
    'https://vaultcaddy.com/kr/bochk-bank-statement-simple.html',
    'https://vaultcaddy.com/capital-one-statement-to-qbo.html',
    'https://vaultcaddy.com/macquarie-bank-statement-to-qbo.html',
    'https://vaultcaddy.com/pnc-bank-statement-to-qbo.html',
    'https://vaultcaddy.com/rhb-bank-statement-to-qbo.html',
    'https://vaultcaddy.com/canara-bank-statement-to-qbo.html',
    'https://vaultcaddy.com/cimb-bank-statement-to-qbo.html',
    'https://vaultcaddy.com/royal-bank-of-canada-statement-to-qbo.html',
    'https://vaultcaddy.com/standard-bank-statement-to-qbo.html',
    'https://vaultcaddy.com/zh-HK/hsbc-hong-kong-statement-to-qbo.html',
    'https://vaultcaddy.com/rakbank-statement-to-qbo.html',
    'https://vaultcaddy.com/alliance-bank-statement-to-qbo.html',
    'https://vaultcaddy.com/zh-HK/boc-hong-kong-statement-to-qbo.html',
    'https://vaultcaddy.com/kr/woori-bank-statement-to-qbo.html',
    'https://vaultcaddy.com/tsb-bank-statement-to-qbo.html',
    'https://vaultcaddy.com/goldman-sachs-statement-to-qbo.html',
    'https://vaultcaddy.com/bank-leumi-statement-to-qbo.html',
    'https://vaultcaddy.com/convert-pdf-to-qbo-format.html',
    'https://vaultcaddy.com/bpi-bank-statement-to-qbo.html',
    'https://vaultcaddy.com/kr/ocbc-bank-statement-simple.html',
    'https://vaultcaddy.com/cimb-singapore-statement-to-qbo.html',
    'https://vaultcaddy.com/convert-statement-to-qbo-format-free.html',
    'https://vaultcaddy.com/quickbooks-online-file-converter.html',
    'https://vaultcaddy.com/bank-statement-to-qbo-file-online.html',
    'https://vaultcaddy.com/qbo-import-converter.html',
    'https://vaultcaddy.com/m&t-bank-statement-to-qbo.html',
    'https://vaultcaddy.com/us-bank-statement-to-qbo.html',
    'https://vaultcaddy.com/hsbc-bank-statement-to-qbo.html',
    'https://vaultcaddy.com/zh-HK/wing-hang-bank-statement-to-qbo.html',
    'https://vaultcaddy.com/cibc-statement-to-qbo.html',
    'https://vaultcaddy.com/lloyds-statement-to-qbo.html',
    'https://vaultcaddy.com/hsbc-uk-statement-to-qbo.html',
    'https://vaultcaddy.com/nab-bank-statement-to-qbo.html',
    'https://vaultcaddy.com/santander-uk-statement-to-qbo.html',
    'https://vaultcaddy.com/keybank-statement-to-qbo.html',
    'https://vaultcaddy.com/uob-bank-statement-to-qbo.html',
    'https://vaultcaddy.com/scotiabank-caribbean-statement-to-qbo.html',
    'https://vaultcaddy.com/clydesdale-bank-statement-to-qbo.html',
    'https://vaultcaddy.com/citibank-hk-statement-to-qbo.html',
    'https://vaultcaddy.com/citibank-singapore-statement-to-qbo.html',
    'https://vaultcaddy.com/zh-HK/chong-hing-bank-statement-to-qbo.html',
    'https://vaultcaddy.com/boc-hk-statement-to-qbo.html',
    'https://vaultcaddy.com/jp/resona-bank-statement-to-qbo.html',
    'https://vaultcaddy.com/ocbc-bank-statement-to-qbo.html',
    'https://vaultcaddy.com/adib-bank-statement-to-qbo.html',
    'https://vaultcaddy.com/axis-bank-statement-to-qbo.html',
    'https://vaultcaddy.com/hsbc-malaysia-statement-to-qbo.html',
    'https://vaultcaddy.com/morgan-stanley-statement-to-qbo.html',
    'https://vaultcaddy.com/asb-bank-statement-to-qbo.html',
    'https://vaultcaddy.com/wing-hang-bank-statement-to-qbo.html',
    'https://vaultcaddy.com/icici-bank-statement-to-qbo.html',
    'https://vaultcaddy.com/adcb-bank-statement-to-qbo.html',
    'https://vaultcaddy.com/bank-of-china-hk-statement-to-qbo.html',
    'https://vaultcaddy.com/suncorp-bank-statement-to-qbo.html',
    'https://vaultcaddy.com/cibc-bank-statement-to-qbo.html',
    'https://vaultcaddy.com/kr/developer-accounting-solution.html',
    'https://vaultcaddy.com/jp/blog/how-to-convert-pdf-bank-statement-to-excel.html',
    'https://vaultcaddy.com/ko-KR/hsbc-uk-bank-statement-v3.html',
    'https://vaultcaddy.com/kr/education-accounting-solution.html',
    'https://vaultcaddy.com/kr/smbc-bank-statement-simple.html',
    'https://vaultcaddy.com/ko-KR/westpac-australia-statement-v3.html',
    'https://vaultcaddy.com/kr/resources.html',
    'https://vaultcaddy.com/ko-KR/asb-bank-statement-v3.html',
    'https://vaultcaddy.com/ko-KR/ally-bank-statement-v3.html',
    'https://vaultcaddy.com/blog/manual-data-entry-vs-ai-automation-2025.html',
    'https://vaultcaddy.com/ko-KR/dbs-bank-statement-v3.html',
    'https://vaultcaddy.com/ko-KR/cathay-bank-statement-v3.html',
    'https://vaultcaddy.com/ko-KR/abn-amro-statement-v3.html',
    'https://vaultcaddy.com/ko-KR/mizuho-bank-statement-v3.html',
    'https://vaultcaddy.com/blog/hsbc-bank-statement-to-excel-guide-2025.html',
    'https://vaultcaddy.com/ko-KR/hang-seng-bank-statement-v3.html',
    'https://vaultcaddy.com/kr/kb-bank-statement.html',
    'https://vaultcaddy.com/ko-KR/ing-bank-statement-v3.html',
    'https://vaultcaddy.com/unified-blog-sidebar.html',
    'https://vaultcaddy.com/zh-TW/lloyds-bank-statement-v3.html',
    'https://vaultcaddy.com/blog/restaurant-accounting-system-guide-2025.html',
    'https://vaultcaddy.com/ko-KR/cibc-bank-statement-v3.html',
    'https://vaultcaddy.com/ko-KR/chase-bank-statement-v3.html',
    'https://vaultcaddy.com/ko-KR/anz-australia-statement-v3.html',
    'https://vaultcaddy.com/zh-TW/hang-seng-bank-statement-v3.html',
    'https://vaultcaddy.com/zh-HK/bmo-bank-statement-v3.html',
    'https://vaultcaddy.com/en-gb/blog/pdf-bank-statement-cannot-copy-text-solutions-2025.html',
    'https://vaultcaddy.com/en-au/blog/pdf-bank-statement-cannot-copy-text-solutions-2025.html',
    'https://vaultcaddy.com/kr/musician-accounting-solution.html',
    'https://vaultcaddy.com/en-ca/blog/pdf-bank-statement-cannot-copy-text-solutions-2025.html',
    'https://vaultcaddy.com/bea-bank-statement-simple.html',
    'https://vaultcaddy.com/kr/designer-accounting-solution.html',
    'https://vaultcaddy.com/kr/blog/ai-invoice-processing-for-smb.html',
    'https://vaultcaddy.com/hang-seng-bank-statement.html'
];

// 读取sitemap.xml
function readSitemap() {
    const sitemapPath = path.join(__dirname, 'sitemap.xml');
    if (!fs.existsSync(sitemapPath)) {
        console.error('❌ sitemap.xml 不存在');
        return null;
    }
    
    const sitemapContent = fs.readFileSync(sitemapPath, 'utf-8');
    return sitemapContent;
}

// 检查URL是否在sitemap中
function isUrlInSitemap(url, sitemapContent) {
    return sitemapContent.includes(url);
}

// 从URL提取文件路径
function getFilePathFromUrl(url) {
    const baseUrl = 'https://vaultcaddy.com/';
    if (!url.startsWith(baseUrl)) {
        return null;
    }
    
    const relativePath = url.replace(baseUrl, '');
    const filePath = path.join(__dirname, relativePath);
    return filePath;
}

// 检查文件是否存在
function fileExists(filePath) {
    return fs.existsSync(filePath);
}

// 检查页面内容质量（简单检查：是否有足够的文本内容）
function checkContentQuality(filePath) {
    try {
        const content = fs.readFileSync(filePath, 'utf-8');
        
        // 提取可见文本（去除HTML标签）
        const textContent = content.replace(/<[^>]*>/g, ' ').replace(/\s+/g, ' ').trim();
        const wordCount = textContent.split(/\s+/).length;
        
        // 检查是否有meta description
        const hasMetaDesc = /<meta\s+name=["']description["']/i.test(content);
        
        // 检查是否有title
        const hasTitle = /<title>/i.test(content);
        
        // 检查是否有h1
        const hasH1 = /<h1[^>]*>/i.test(content);
        
        return {
            wordCount,
            hasMetaDesc,
            hasTitle,
            hasH1,
            quality: wordCount >= 500 ? 'good' : wordCount >= 200 ? 'fair' : 'poor'
        };
    } catch (error) {
        return {
            error: error.message,
            quality: 'error'
        };
    }
}

// 主函数
function main() {
    console.log('🔍 开始分析未索引页面...\n');
    
    const sitemapContent = readSitemap();
    if (!sitemapContent) {
        return;
    }
    
    const results = {
        inSitemap: [],
        notInSitemap: [],
        fileNotFound: [],
        lowQuality: []
    };
    
    unindexedPages.forEach((url, index) => {
        const filePath = getFilePathFromUrl(url);
        const inSitemap = isUrlInSitemap(url, sitemapContent);
        
        if (!filePath) {
            console.log(`⚠️ 无法解析URL: ${url}`);
            return;
        }
        
        if (fileExists(filePath)) {
            const quality = checkContentQuality(filePath);
            
            if (inSitemap) {
                results.inSitemap.push({ url, filePath, quality });
            } else {
                results.notInSitemap.push({ url, filePath, quality });
            }
            
            if (quality.quality === 'poor' || quality.quality === 'error') {
                results.lowQuality.push({ url, filePath, quality });
            }
        } else {
            results.fileNotFound.push({ url, filePath });
        }
        
        // 显示进度
        if ((index + 1) % 20 === 0) {
            console.log(`📊 已处理 ${index + 1}/${unindexedPages.length} 个页面...`);
        }
    });
    
    // 输出报告
    console.log('\n' + '='.repeat(80));
    console.log('📊 分析结果');
    console.log('='.repeat(80));
    console.log(`\n✅ 在sitemap中: ${results.inSitemap.length} 个`);
    console.log(`❌ 不在sitemap中: ${results.notInSitemap.length} 个`);
    console.log(`⚠️ 文件不存在: ${results.fileNotFound.length} 个`);
    console.log(`📉 内容质量低: ${results.lowQuality.length} 个`);
    
    // 详细报告
    if (results.notInSitemap.length > 0) {
        console.log('\n📋 不在sitemap中的页面（需要添加）:');
        results.notInSitemap.slice(0, 10).forEach(({ url, quality }) => {
            console.log(`   - ${url} (质量: ${quality.quality}, 字数: ${quality.wordCount || 'N/A'})`);
        });
        if (results.notInSitemap.length > 10) {
            console.log(`   ... 还有 ${results.notInSitemap.length - 10} 个`);
        }
    }
    
    if (results.lowQuality.length > 0) {
        console.log('\n📉 内容质量低的页面:');
        results.lowQuality.slice(0, 10).forEach(({ url, quality }) => {
            console.log(`   - ${url} (字数: ${quality.wordCount || 'N/A'})`);
        });
        if (results.lowQuality.length > 10) {
            console.log(`   ... 还有 ${results.lowQuality.length - 10} 个`);
        }
    }
    
    // 生成修复建议
    console.log('\n' + '='.repeat(80));
    console.log('💡 修复建议');
    console.log('='.repeat(80));
    console.log('\n1. 添加缺失页面到sitemap.xml');
    console.log(`   - 需要添加 ${results.notInSitemap.length} 个页面`);
    console.log('\n2. 改善内容质量');
    console.log(`   - ${results.lowQuality.length} 个页面需要更多内容`);
    console.log('\n3. 在Google Search Console中请求重新索引');
    console.log('   - 使用"URL检查"工具逐个提交');
    console.log('\n4. 添加内部链接');
    console.log('   - 从主要页面链接到这些页面');
    
    // 保存详细报告
    const report = {
        timestamp: new Date().toISOString(),
        total: unindexedPages.length,
        inSitemap: results.inSitemap.length,
        notInSitemap: results.notInSitemap.length,
        fileNotFound: results.fileNotFound.length,
        lowQuality: results.lowQuality.length,
        details: {
            notInSitemap: results.notInSitemap.map(({ url }) => url),
            lowQuality: results.lowQuality.map(({ url, quality }) => ({ url, wordCount: quality.wordCount }))
        }
    };
    
    fs.writeFileSync(
        path.join(__dirname, '📊_未索引页面分析报告.json'),
        JSON.stringify(report, null, 2),
        'utf-8'
    );
    
    console.log('\n✅ 详细报告已保存到: 📊_未索引页面分析报告.json');
}

main();
