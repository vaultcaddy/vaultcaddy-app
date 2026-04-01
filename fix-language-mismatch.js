/**
 * 🔧 修复语言不匹配问题
 * 根据页面语言使用对应的index.html模板
 */

const fs = require('fs');
const path = require('path');

// 配置
const CONFIG = {
    templates: {
        'zh-TW': path.join(__dirname, 'index.html'),      // 繁体中文
        'zh-HK': path.join(__dirname, 'index.html'),      // 简体中文（香港）
        'en': path.join(__dirname, 'en/index.html'),      // 英文
        'en-US': path.join(__dirname, 'en/index.html'),   // 英文（美国）
        'en-ja': path.join(__dirname, 'en/index.html'),   // 英文（日本市场）
        'en-so': path.join(__dirname, 'en/index.html'),   // 英文（其他）
        'ja': path.join(__dirname, 'jp/index.html'),      // 日文
        'ja-JP': path.join(__dirname, 'jp/index.html'),   // 日文
        'ko-KR': path.join(__dirname, 'kr/index.html'),   // 韩文
    },
    backupDir: path.join(__dirname, 'backup_before_language_fix_' + Date.now()),
};

/**
 * 检测文件当前使用的语言
 */
function detectCurrentLang(filePath) {
    const html = fs.readFileSync(filePath, 'utf8');
    const langMatch = html.match(/<html\s+lang="([^"]*)"/i);
    return langMatch ? langMatch[1] : 'zh-TW';
}

/**
 * 检测文件应该使用的语言（基于路径和内容）
 */
function detectTargetLang(filePath) {
    const relativePath = path.relative(__dirname, filePath);
    
    // 基于目录判断
    if (relativePath.startsWith('ja-JP/') || relativePath.startsWith('jp/')) {
        return 'ja-JP';
    }
    if (relativePath.startsWith('ko-KR/') || relativePath.startsWith('kr/')) {
        return 'ko-KR';
    }
    if (relativePath.startsWith('zh-HK/')) {
        return 'zh-HK';
    }
    if (relativePath.startsWith('zh-TW/')) {
        return 'zh-TW';
    }
    if (relativePath.startsWith('en/')) {
        return 'en';
    }
    
    // 根目录的v2/v3文件，检查内容中的语言
    const html = fs.readFileSync(filePath, 'utf8');
    const langMatch = html.match(/<html\s+lang="([^"]*)"/i);
    return langMatch ? langMatch[1] : 'zh-TW';
}

/**
 * 简化的转换函数
 */
function convertFile(filePath, templateHTML) {
    const html = fs.readFileSync(filePath, 'utf8');
    
    // 提取SEO元数据
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
    const targetLang = detectTargetLang(filePath);
    
    // 提取JSON-LD
    const jsonLdPattern = /<script\s+type="application\/ld\+json">([\s\S]*?)<\/script>/gi;
    const jsonLdScripts = [];
    let match;
    while ((match = jsonLdPattern.exec(html)) !== null) {
        jsonLdScripts.push(match[1].trim());
    }
    
    // 更新模板
    let newHTML = templateHTML;
    
    // 更新语言
    newHTML = newHTML.replace(/<html\s+lang="[^"]*"/, `<html lang="${targetLang}"`);
    
    // 更新SEO元数据
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
    
    // 添加JSON-LD
    if (jsonLdScripts.length > 0) {
        const jsonLdSection = jsonLdScripts
            .map(script => `<script type="application/ld+json">\n${script}\n</script>`)
            .join('\n    ');
        
        newHTML = newHTML.replace(/<script\s+type="application\/ld\+json">[\s\S]*?<\/script>/gi, '');
        newHTML = newHTML.replace(/(<\/head>)/i, `    ${jsonLdSection}\n    $1`);
    }
    
    return newHTML;
}

/**
 * 获取所有v2/v3文件
 */
function getAllV2V3Files() {
    const files = [];
    
    // 根目录
    const rootFiles = fs.readdirSync(__dirname)
        .filter(f => (f.endsWith('-v2.html') || f.endsWith('-v3.html')) && 
                     !f.includes('backup') && !f.includes('tmp'))
        .map(f => path.join(__dirname, f));
    files.push(...rootFiles);
    
    // 语言目录
    const langDirs = ['en', 'zh-HK', 'zh-TW', 'ja-JP', 'ko-KR'];
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
 * 主函数
 */
async function main() {
    console.log('='.repeat(80));
    console.log('🔧 修复语言不匹配问题');
    console.log('='.repeat(80));
    console.log('');
    
    // 检查模板文件
    console.log('📖 检查模板文件...');
    const missingTemplates = [];
    for (const [lang, templatePath] of Object.entries(CONFIG.templates)) {
        if (!fs.existsSync(templatePath)) {
            missingTemplates.push(`${lang}: ${templatePath}`);
        } else {
            console.log(`  ✅ ${lang}: ${path.relative(__dirname, templatePath)}`);
        }
    }
    
    if (missingTemplates.length > 0) {
        console.log('\n❌ 缺失的模板文件:');
        missingTemplates.forEach(t => console.log(`  - ${t}`));
        return;
    }
    
    // 加载模板
    console.log('\n📖 加载模板...');
    const templates = {};
    for (const [lang, templatePath] of Object.entries(CONFIG.templates)) {
        templates[lang] = fs.readFileSync(templatePath, 'utf8');
    }
    
    // 获取所有文件
    const files = getAllV2V3Files();
    console.log(`\n找到 ${files.length} 个文件\n`);
    
    // 创建备份目录
    if (!fs.existsSync(CONFIG.backupDir)) {
        fs.mkdirSync(CONFIG.backupDir, { recursive: true });
    }
    
    // 分析每个文件
    const analysis = {
        correct: [],
        needsFix: [],
        byLang: {},
    };
    
    console.log('📊 分析文件语言匹配情况...\n');
    
    files.forEach(file => {
        const currentLang = detectCurrentLang(file);
        const targetLang = detectTargetLang(file);
        const relativePath = path.relative(__dirname, file);
        
        if (!analysis.byLang[targetLang]) {
            analysis.byLang[targetLang] = { correct: 0, needsFix: 0 };
        }
        
        if (currentLang === targetLang) {
            analysis.correct.push({ file: relativePath, lang: currentLang });
            analysis.byLang[targetLang].correct++;
        } else {
            analysis.needsFix.push({ 
                file: relativePath, 
                currentLang, 
                targetLang 
            });
            analysis.byLang[targetLang].needsFix++;
        }
    });
    
    // 显示分析结果
    console.log('📊 语言匹配分析:');
    console.log(`  ✅ 正确: ${analysis.correct.length}`);
    console.log(`  ⚠️  需要修复: ${analysis.needsFix.length}`);
    console.log('');
    
    console.log('按语言统计:');
    Object.keys(analysis.byLang).sort().forEach(lang => {
        const stats = analysis.byLang[lang];
        const total = stats.correct + stats.needsFix;
        console.log(`  ${lang.padEnd(10)} 正确: ${stats.correct}  需修复: ${stats.needsFix}  总计: ${total}`);
    });
    
    if (analysis.needsFix.length > 0) {
        console.log('\n⚠️  需要修复的文件示例 (前10个):');
        analysis.needsFix.slice(0, 10).forEach(item => {
            console.log(`  ${item.file}`);
            console.log(`    当前: ${item.currentLang} → 应为: ${item.targetLang}`);
        });
    }
    
    // 询问是否继续
    console.log('\n' + '='.repeat(80));
    console.log('🔧 开始修复...');
    console.log('='.repeat(80));
    console.log('');
    
    let fixed = 0;
    let errors = 0;
    
    for (const item of analysis.needsFix) {
        try {
            const filePath = path.join(__dirname, item.file);
            const template = templates[item.targetLang];
            
            if (!template) {
                console.log(`❌ ${item.file}: 没有找到 ${item.targetLang} 的模板`);
                errors++;
                continue;
            }
            
            // 备份
            const backupPath = path.join(CONFIG.backupDir, item.file);
            const backupDir = path.dirname(backupPath);
            if (!fs.existsSync(backupDir)) {
                fs.mkdirSync(backupDir, { recursive: true });
            }
            fs.copyFileSync(filePath, backupPath);
            
            // 转换
            const newHTML = convertFile(filePath, template);
            
            // 写入
            fs.writeFileSync(filePath, newHTML, 'utf8');
            
            fixed++;
            process.stdout.write(`✅ [${fixed}/${analysis.needsFix.length}] ${item.file} (${item.currentLang} → ${item.targetLang})\r`);
            
        } catch (error) {
            console.log(`\n❌ ${item.file}: ${error.message}`);
            errors++;
        }
    }
    
    console.log('\n\n' + '='.repeat(80));
    console.log('📊 修复完成');
    console.log('='.repeat(80));
    console.log(`✅ 成功修复: ${fixed}`);
    console.log(`❌ 失败: ${errors}`);
    console.log(`📦 备份目录: ${CONFIG.backupDir}`);
    console.log('\n✨ 完成！');
}

if (require.main === module) {
    main().catch(console.error);
}
