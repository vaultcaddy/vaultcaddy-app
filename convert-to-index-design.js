/**
 * 批量将 v2 和 v3 页面转换成 index.html 的设计
 * 保留每个页面的 SEO 元数据，但使用统一的视觉设计
 */

const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');

// 配置
const CONFIG = {
    indexTemplate: path.join(__dirname, 'index.html'),
    outputBackupDir: path.join(__dirname, 'backup_before_conversion_' + Date.now()),
    dryRun: false, // 设置为 true 仅预览不修改
};

/**
 * 读取 index.html 模板
 */
function getIndexTemplate() {
    const html = fs.readFileSync(CONFIG.indexTemplate, 'utf8');
    const dom = new JSDOM(html);
    const doc = dom.window.document;
    
    // 提取主要部分
    const template = {
        fullHTML: html,
        head: doc.head.innerHTML,
        body: doc.body.innerHTML,
        scripts: Array.from(doc.querySelectorAll('script'))
            .map(s => s.outerHTML)
            .join('\n'),
        styles: Array.from(doc.querySelectorAll('style'))
            .map(s => s.outerHTML)
            .join('\n'),
    };
    
    return template;
}

/**
 * 提取页面的 SEO 元数据
 */
function extractSEOMetadata(filePath) {
    const html = fs.readFileSync(filePath, 'utf8');
    const dom = new JSDOM(html);
    const doc = dom.window.document;
    
    const metadata = {
        // 基础 SEO
        title: doc.querySelector('title')?.textContent || '',
        description: doc.querySelector('meta[name="description"]')?.content || '',
        keywords: doc.querySelector('meta[name="keywords"]')?.content || '',
        canonical: doc.querySelector('link[rel="canonical"]')?.href || '',
        
        // Open Graph
        ogTitle: doc.querySelector('meta[property="og:title"]')?.content || '',
        ogDescription: doc.querySelector('meta[property="og:description"]')?.content || '',
        ogImage: doc.querySelector('meta[property="og:image"]')?.content || '',
        ogUrl: doc.querySelector('meta[property="og:url"]')?.content || '',
        
        // Twitter Card
        twitterTitle: doc.querySelector('meta[name="twitter:title"]')?.content || '',
        twitterDescription: doc.querySelector('meta[name="twitter:description"]')?.content || '',
        twitterImage: doc.querySelector('meta[name="twitter:image"]')?.content || '',
        
        // Structured Data
        structuredData: [],
        
        // 语言
        lang: doc.documentElement.lang || 'zh-TW',
    };
    
    // 提取所有 JSON-LD 结构化数据
    const jsonLdScripts = doc.querySelectorAll('script[type="application/ld+json"]');
    jsonLdScripts.forEach(script => {
        try {
            metadata.structuredData.push(JSON.parse(script.textContent));
        } catch (e) {
            console.warn(`无法解析 JSON-LD: ${filePath}`);
        }
    });
    
    return metadata;
}

/**
 * 检测页面类型和关键信息
 */
function detectPageInfo(filePath) {
    const fileName = path.basename(filePath);
    const dirName = path.dirname(filePath);
    
    // 检测语言
    let language = 'zh-TW'; // 默认繁体中文
    if (dirName.includes('en')) language = 'en';
    else if (dirName.includes('zh-HK')) language = 'zh-HK';
    else if (dirName.includes('ja-JP') || dirName.includes('jp')) language = 'ja-JP';
    else if (dirName.includes('ko-KR') || dirName.includes('kr')) language = 'ko-KR';
    
    // 提取银行名称或特性
    const bankMatch = fileName.match(/^([a-z-]+)-bank-statement/i) || 
                     fileName.match(/^([a-z-]+)-statement/i) ||
                     fileName.match(/^([a-z-]+)-accounting/i) ||
                     fileName.match(/^([a-z-]+)-v[23]/i);
    
    const bankName = bankMatch ? bankMatch[1] : 'general';
    
    // 检测版本
    const version = fileName.includes('-v2') ? 'v2' : 
                   fileName.includes('-v3') ? 'v3' : 'v1';
    
    return {
        fileName,
        dirName,
        language,
        bankName,
        version,
        fullPath: filePath,
    };
}

/**
 * 生成新的HTML内容
 */
function generateNewHTML(template, metadata, pageInfo) {
    const dom = new JSDOM(template.fullHTML);
    const doc = dom.window.document;
    
    // 更新语言
    doc.documentElement.lang = metadata.lang || pageInfo.language;
    
    // 更新 SEO 元数据
    if (metadata.title) {
        const titleEl = doc.querySelector('title');
        if (titleEl) titleEl.textContent = metadata.title;
    }
    
    if (metadata.description) {
        let descEl = doc.querySelector('meta[name="description"]');
        if (!descEl) {
            descEl = doc.createElement('meta');
            descEl.name = 'description';
            doc.head.appendChild(descEl);
        }
        descEl.content = metadata.description;
    }
    
    if (metadata.keywords) {
        let keywordsEl = doc.querySelector('meta[name="keywords"]');
        if (!keywordsEl) {
            keywordsEl = doc.createElement('meta');
            keywordsEl.name = 'keywords';
            doc.head.appendChild(keywordsEl);
        }
        keywordsEl.content = metadata.keywords;
    }
    
    // 更新 Canonical URL
    if (metadata.canonical) {
        let canonicalEl = doc.querySelector('link[rel="canonical"]');
        if (!canonicalEl) {
            canonicalEl = doc.createElement('link');
            canonicalEl.rel = 'canonical';
            doc.head.appendChild(canonicalEl);
        }
        canonicalEl.href = metadata.canonical;
    }
    
    // 更新 Open Graph
    const ogMeta = [
        { property: 'og:title', content: metadata.ogTitle },
        { property: 'og:description', content: metadata.ogDescription },
        { property: 'og:image', content: metadata.ogImage },
        { property: 'og:url', content: metadata.ogUrl },
    ];
    
    ogMeta.forEach(({ property, content }) => {
        if (content) {
            let el = doc.querySelector(`meta[property="${property}"]`);
            if (!el) {
                el = doc.createElement('meta');
                el.setAttribute('property', property);
                doc.head.appendChild(el);
            }
            el.content = content;
        }
    });
    
    // 更新 Twitter Card
    const twitterMeta = [
        { name: 'twitter:title', content: metadata.twitterTitle },
        { name: 'twitter:description', content: metadata.twitterDescription },
        { name: 'twitter:image', content: metadata.twitterImage },
    ];
    
    twitterMeta.forEach(({ name, content }) => {
        if (content) {
            let el = doc.querySelector(`meta[name="${name}"]`);
            if (!el) {
                el = doc.createElement('meta');
                el.name = name;
                doc.head.appendChild(el);
            }
            el.content = content;
        }
    });
    
    // 添加 JSON-LD 结构化数据
    // 先删除现有的 JSON-LD
    const existingJsonLd = doc.querySelectorAll('script[type="application/ld+json"]');
    existingJsonLd.forEach(el => el.remove());
    
    // 添加新的 JSON-LD
    metadata.structuredData.forEach(data => {
        const script = doc.createElement('script');
        script.type = 'application/ld+json';
        script.textContent = JSON.stringify(data, null, 2);
        doc.head.appendChild(script);
    });
    
    // 返回最终 HTML
    return '<!DOCTYPE html>\n' + doc.documentElement.outerHTML;
}

/**
 * 处理单个文件
 */
function processFile(filePath) {
    console.log(`\n处理: ${filePath}`);
    
    try {
        // 获取页面信息
        const pageInfo = detectPageInfo(filePath);
        console.log(`  - 语言: ${pageInfo.language}`);
        console.log(`  - 银行/类型: ${pageInfo.bankName}`);
        console.log(`  - 版本: ${pageInfo.version}`);
        
        // 提取 SEO 元数据
        const metadata = extractSEOMetadata(filePath);
        console.log(`  - 标题: ${metadata.title.substring(0, 60)}...`);
        
        // 获取模板
        const template = getIndexTemplate();
        
        // 生成新 HTML
        const newHTML = generateNewHTML(template, metadata, pageInfo);
        
        if (!CONFIG.dryRun) {
            // 备份原文件
            const backupPath = path.join(
                CONFIG.outputBackupDir,
                path.relative(__dirname, filePath)
            );
            const backupDir = path.dirname(backupPath);
            if (!fs.existsSync(backupDir)) {
                fs.mkdirSync(backupDir, { recursive: true });
            }
            fs.copyFileSync(filePath, backupPath);
            
            // 写入新文件
            fs.writeFileSync(filePath, newHTML, 'utf8');
            console.log(`  ✅ 转换完成`);
        } else {
            console.log(`  🔍 [预览模式] 将会转换`);
        }
        
        return { success: true, filePath };
    } catch (error) {
        console.error(`  ❌ 错误: ${error.message}`);
        return { success: false, filePath, error: error.message };
    }
}

/**
 * 获取所有需要转换的文件
 */
function getAllV2V3Files() {
    const files = [];
    
    // 根目录的 v2 文件
    const rootFiles = fs.readdirSync(__dirname)
        .filter(f => f.endsWith('-v2.html') || f.endsWith('-v3.html'))
        .map(f => path.join(__dirname, f));
    files.push(...rootFiles);
    
    // 语言目录的 v3 文件
    const langDirs = ['en', 'zh-HK', 'zh-TW', 'ja-JP', 'jp', 'ko-KR', 'kr'];
    langDirs.forEach(langDir => {
        const dirPath = path.join(__dirname, langDir);
        if (fs.existsSync(dirPath) && fs.statSync(dirPath).isDirectory()) {
            const langFiles = fs.readdirSync(dirPath)
                .filter(f => f.endsWith('-v3.html'))
                .map(f => path.join(dirPath, f));
            files.push(...langFiles);
        }
    });
    
    return files;
}

/**
 * 主函数
 */
async function main() {
    console.log('='.repeat(80));
    console.log('📄 批量转换 v2/v3 页面到 index.html 设计');
    console.log('='.repeat(80));
    console.log(`模式: ${CONFIG.dryRun ? '🔍 预览模式（不会修改文件）' : '✍️  实际转换'}`);
    console.log('');
    
    // 获取所有文件
    const files = getAllV2V3Files();
    console.log(`找到 ${files.length} 个文件需要转换\n`);
    
    if (files.length === 0) {
        console.log('没有找到需要转换的文件');
        return;
    }
    
    // 创建备份目录
    if (!CONFIG.dryRun && !fs.existsSync(CONFIG.outputBackupDir)) {
        fs.mkdirSync(CONFIG.outputBackupDir, { recursive: true });
        console.log(`📦 备份目录: ${CONFIG.outputBackupDir}\n`);
    }
    
    // 处理所有文件
    const results = [];
    for (const file of files) {
        const result = processFile(file);
        results.push(result);
    }
    
    // 统计结果
    console.log('\n' + '='.repeat(80));
    console.log('📊 转换统计');
    console.log('='.repeat(80));
    const successful = results.filter(r => r.success).length;
    const failed = results.filter(r => !r.success).length;
    console.log(`✅ 成功: ${successful}`);
    console.log(`❌ 失败: ${failed}`);
    console.log(`📝 总计: ${results.length}`);
    
    if (failed > 0) {
        console.log('\n失败的文件:');
        results.filter(r => !r.success).forEach(r => {
            console.log(`  - ${r.filePath}: ${r.error}`);
        });
    }
    
    if (!CONFIG.dryRun) {
        console.log(`\n📦 原文件已备份到: ${CONFIG.outputBackupDir}`);
    }
    
    console.log('\n✨ 完成！');
}

// 运行
if (require.main === module) {
    main().catch(console.error);
}

module.exports = { processFile, getAllV2V3Files, extractSEOMetadata };
