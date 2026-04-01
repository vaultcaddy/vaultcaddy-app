/**
 * 继续转换剩余的 v2 和 v3 页面
 * 改进版：更好的错误处理和内存管理
 */

const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');

// 配置
const CONFIG = {
    indexTemplate: path.join(__dirname, 'index.html'),
    backupDir: path.join(__dirname, 'backup_before_conversion_1770702977980'),
    progressFile: path.join(__dirname, 'conversion_progress.json'),
    batchSize: 50, // 每次处理50个文件
};

/**
 * 加载进度
 */
function loadProgress() {
    if (fs.existsSync(CONFIG.progressFile)) {
        return JSON.parse(fs.readFileSync(CONFIG.progressFile, 'utf8'));
    }
    return { completed: [], failed: [], lastIndex: 0 };
}

/**
 * 保存进度
 */
function saveProgress(progress) {
    fs.writeFileSync(CONFIG.progressFile, JSON.stringify(progress, null, 2), 'utf8');
}

/**
 * 检查文件是否已转换
 */
function isAlreadyConverted(filePath, backupDir) {
    const relativePath = path.relative(__dirname, filePath);
    const backupPath = path.join(backupDir, relativePath);
    return fs.existsSync(backupPath);
}

/**
 * 获取所有需要转换的文件
 */
function getAllV2V3Files() {
    const files = [];
    
    // 根目录的 v2/v3 文件
    const rootFiles = fs.readdirSync(__dirname)
        .filter(f => (f.endsWith('-v2.html') || f.endsWith('-v3.html')) && 
                     !f.includes('backup') && !f.includes('tmp'))
        .map(f => path.join(__dirname, f));
    files.push(...rootFiles);
    
    // 语言目录的 v3 文件
    const langDirs = ['en', 'zh-HK', 'zh-TW', 'ja-JP', 'jp', 'ko-KR', 'kr'];
    langDirs.forEach(langDir => {
        const dirPath = path.join(__dirname, langDir);
        if (fs.existsSync(dirPath) && fs.statSync(dirPath).isDirectory()) {
            const langFiles = fs.readdirSync(dirPath)
                .filter(f => f.endsWith('-v3.html') && !f.includes('backup') && !f.includes('tmp'))
                .map(f => path.join(dirPath, f));
            files.push(...langFiles);
        }
    });
    
    return files;
}

/**
 * 简化的转换函数 - 只更新 SEO 元数据
 */
function convertFile(filePath, templateHTML) {
    const html = fs.readFileSync(filePath, 'utf8');
    
    // 使用正则表达式提取和替换 SEO 元数据
    const extractMeta = (html, pattern) => {
        const match = html.match(pattern);
        return match ? match[1] : '';
    };
    
    const title = extractMeta(html, /<title>(.*?)<\/title>/i);
    const description = extractMeta(html, /<meta\s+name="description"\s+content="(.*?)"/i);
    const keywords = extractMeta(html, /<meta\s+name="keywords"\s+content="(.*?)"/i);
    const canonical = extractMeta(html, /<link\s+rel="canonical"\s+href="(.*?)"/i);
    const ogTitle = extractMeta(html, /<meta\s+property="og:title"\s+content="(.*?)"/i);
    const ogDescription = extractMeta(html, /<meta\s+property="og:description"\s+content="(.*?)"/i);
    const ogUrl = extractMeta(html, /<meta\s+property="og:url"\s+content="(.*?)"/i);
    const lang = extractMeta(html, /<html\s+lang="(.*?)"/i) || 'zh-TW';
    
    // 提取所有 JSON-LD 结构化数据
    const jsonLdPattern = /<script\s+type="application\/ld\+json">([\s\S]*?)<\/script>/gi;
    const jsonLdScripts = [];
    let match;
    while ((match = jsonLdPattern.exec(html)) !== null) {
        jsonLdScripts.push(match[1].trim());
    }
    
    // 更新模板
    let newHTML = templateHTML;
    
    // 更新语言
    newHTML = newHTML.replace(/<html\s+lang="[^"]*"/, `<html lang="${lang}"`);
    
    // 更新 SEO 元数据
    if (title) {
        newHTML = newHTML.replace(/<title>.*?<\/title>/i, `<title>${title}</title>`);
    }
    
    if (description) {
        newHTML = newHTML.replace(
            /<meta\s+name="description"\s+content="[^"]*"/i,
            `<meta name="description" content="${description}"`
        );
    }
    
    if (keywords) {
        newHTML = newHTML.replace(
            /<meta\s+name="keywords"\s+content="[^"]*"/i,
            `<meta name="keywords" content="${keywords}"`
        );
    }
    
    if (canonical) {
        newHTML = newHTML.replace(
            /<link\s+rel="canonical"\s+href="[^"]*"/i,
            `<link rel="canonical" href="${canonical}"`
        );
    }
    
    if (ogTitle) {
        newHTML = newHTML.replace(
            /<meta\s+property="og:title"\s+content="[^"]*"/i,
            `<meta property="og:title" content="${ogTitle}"`
        );
    }
    
    if (ogDescription) {
        newHTML = newHTML.replace(
            /<meta\s+property="og:description"\s+content="[^"]*"/i,
            `<meta property="og:description" content="${ogDescription}"`
        );
    }
    
    if (ogUrl) {
        newHTML = newHTML.replace(
            /<meta\s+property="og:url"\s+content="[^"]*"/i,
            `<meta property="og:url" content="${ogUrl}"`
        );
    }
    
    // 添加 JSON-LD 结构化数据（在 head 结束前）
    if (jsonLdScripts.length > 0) {
        const jsonLdSection = jsonLdScripts
            .map(script => `<script type="application/ld+json">\n${script}\n</script>`)
            .join('\n    ');
        
        // 先删除模板中原有的 JSON-LD
        newHTML = newHTML.replace(/<script\s+type="application\/ld\+json">[\s\S]*?<\/script>/gi, '');
        
        // 在 </head> 前添加新的 JSON-LD
        newHTML = newHTML.replace(
            /(<\/head>)/i,
            `    ${jsonLdSection}\n    $1`
        );
    }
    
    return newHTML;
}

/**
 * 处理单个文件
 */
function processFile(filePath, templateHTML) {
    try {
        const relativePath = path.relative(__dirname, filePath);
        
        // 备份
        const backupPath = path.join(CONFIG.backupDir, relativePath);
        const backupDir = path.dirname(backupPath);
        if (!fs.existsSync(backupDir)) {
            fs.mkdirSync(backupDir, { recursive: true });
        }
        
        // 如果还没备份，先备份
        if (!fs.existsSync(backupPath)) {
            fs.copyFileSync(filePath, backupPath);
        }
        
        // 转换
        const newHTML = convertFile(filePath, templateHTML);
        
        // 写入
        fs.writeFileSync(filePath, newHTML, 'utf8');
        
        return { success: true, file: relativePath };
    } catch (error) {
        return { success: false, file: path.relative(__dirname, filePath), error: error.message };
    }
}

/**
 * 主函数
 */
async function main() {
    console.log('='.repeat(80));
    console.log('📄 继续转换剩余的 v2/v3 页面');
    console.log('='.repeat(80));
    console.log('');
    
    // 加载模板
    console.log('📖 加载 index.html 模板...');
    const templateHTML = fs.readFileSync(CONFIG.indexTemplate, 'utf8');
    
    // 获取所有文件
    const allFiles = getAllV2V3Files();
    console.log(`找到 ${allFiles.length} 个 v2/v3 文件\n`);
    
    // 过滤已转换的文件
    const filesToConvert = allFiles.filter(f => {
        const alreadyConverted = isAlreadyConverted(f, CONFIG.backupDir);
        return !alreadyConverted;
    });
    
    console.log(`其中 ${allFiles.length - filesToConvert.length} 个已转换`);
    console.log(`需要转换 ${filesToConvert.length} 个文件\n`);
    
    if (filesToConvert.length === 0) {
        console.log('✨ 所有文件已转换完成！');
        return;
    }
    
    // 加载进度
    const progress = loadProgress();
    
    // 批量处理
    let processedCount = 0;
    const results = { succeeded: 0, failed: 0, errors: [] };
    
    for (let i = 0; i < filesToConvert.length; i++) {
        const file = filesToConvert[i];
        const result = processFile(file, templateHTML);
        
        if (result.success) {
            results.succeeded++;
            progress.completed.push(result.file);
            process.stdout.write(`✅ [${i + 1}/${filesToConvert.length}] ${result.file}\r`);
        } else {
            results.failed++;
            progress.failed.push({ file: result.file, error: result.error });
            console.log(`\n❌ [${i + 1}/${filesToConvert.length}] ${result.file}: ${result.error}`);
        }
        
        processedCount++;
        
        // 每处理50个文件保存一次进度
        if (processedCount % CONFIG.batchSize === 0) {
            saveProgress(progress);
            console.log(`\n💾 已保存进度 (${processedCount}/${filesToConvert.length})`);
            
            // 手动触发垃圾回收（如果可用）
            if (global.gc) {
                global.gc();
            }
        }
    }
    
    // 最后保存进度
    saveProgress(progress);
    
    console.log('\n\n' + '='.repeat(80));
    console.log('📊 转换完成统计');
    console.log('='.repeat(80));
    console.log(`✅ 成功: ${results.succeeded}`);
    console.log(`❌ 失败: ${results.failed}`);
    console.log(`📝 总计: ${filesToConvert.length}`);
    
    if (results.failed > 0) {
        console.log('\n失败的文件:');
        progress.failed.forEach(({ file, error }) => {
            console.log(`  - ${file}: ${error}`);
        });
    }
    
    console.log(`\n📦 备份目录: ${CONFIG.backupDir}`);
    console.log(`📄 进度文件: ${CONFIG.progressFile}`);
    console.log('\n✨ 完成！');
}

// 运行
if (require.main === module) {
    main().catch(console.error);
}
