/**
 * 验证转换后的页面质量
 * 检查 SEO 元数据完整性和设计一致性
 */

const fs = require('fs');
const path = require('path');

function verifyFile(filePath) {
    const html = fs.readFileSync(filePath, 'utf8');
    const relativePath = path.relative(__dirname, filePath);
    
    const checks = {
        file: relativePath,
        hasTitle: /<title>.*?<\/title>/i.test(html),
        hasDescription: /<meta\s+name="description"\s+content=".*?"/i.test(html),
        hasKeywords: /<meta\s+name="keywords"\s+content=".*?"/i.test(html),
        hasCanonical: /<link\s+rel="canonical"\s+href=".*?"/i.test(html),
        hasOgTitle: /<meta\s+property="og:title"\s+content=".*?"/i.test(html),
        hasOgDescription: /<meta\s+property="og:description"\s+content=".*?"/i.test(html),
        hasIndexDesign: /styles\.css/i.test(html) && /pages\.css/i.test(html),
        hasFirebase: /firebase-config\.js/i.test(html),
        hasNavbar: /navbar-component\.js/i.test(html),
        lang: (html.match(/<html\s+lang="([^"]*)"/i) || [])[1] || 'unknown',
    };
    
    // 计算得分
    const requiredChecks = [
        'hasTitle', 'hasDescription', 'hasCanonical', 
        'hasOgTitle', 'hasOgDescription', 'hasIndexDesign'
    ];
    const score = requiredChecks.filter(key => checks[key]).length;
    checks.score = `${score}/${requiredChecks.length}`;
    checks.passed = score === requiredChecks.length;
    
    return checks;
}

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

async function main() {
    console.log('='.repeat(80));
    console.log('🔍 验证转换后的页面质量');
    console.log('='.repeat(80));
    console.log('');
    
    const files = getAllV2V3Files();
    console.log(`检查 ${files.length} 个文件...\n`);
    
    const results = files.map(verifyFile);
    
    // 统计
    const passed = results.filter(r => r.passed).length;
    const failed = results.filter(r => !r.passed).length;
    
    // 按语言分组统计
    const byLang = {};
    results.forEach(r => {
        const lang = r.lang || 'unknown';
        if (!byLang[lang]) {
            byLang[lang] = { total: 0, passed: 0 };
        }
        byLang[lang].total++;
        if (r.passed) byLang[lang].passed++;
    });
    
    console.log('='.repeat(80));
    console.log('📊 验证结果统计');
    console.log('='.repeat(80));
    console.log(`✅ 通过: ${passed} (${(passed/files.length*100).toFixed(1)}%)`);
    console.log(`❌ 失败: ${failed} (${(failed/files.length*100).toFixed(1)}%)`);
    console.log(`📝 总计: ${files.length}`);
    
    console.log('\n按语言统计:');
    Object.keys(byLang).sort().forEach(lang => {
        const stats = byLang[lang];
        const pct = (stats.passed/stats.total*100).toFixed(1);
        console.log(`  ${lang.padEnd(10)} ${stats.passed}/${stats.total} (${pct}%)`);
    });
    
    // 显示失败的文件
    if (failed > 0) {
        console.log('\n❌ 需要修复的文件:');
        results.filter(r => !r.passed).forEach(r => {
            console.log(`  - ${r.file} (得分: ${r.score})`);
            const missing = [];
            if (!r.hasTitle) missing.push('title');
            if (!r.hasDescription) missing.push('description');
            if (!r.hasCanonical) missing.push('canonical');
            if (!r.hasOgTitle) missing.push('og:title');
            if (!r.hasOgDescription) missing.push('og:description');
            if (!r.hasIndexDesign) missing.push('index设计');
            console.log(`    缺失: ${missing.join(', ')}`);
        });
    }
    
    // 随机抽样检查
    console.log('\n🎲 随机抽样检查 (5个文件):');
    const samples = [...results].sort(() => Math.random() - 0.5).slice(0, 5);
    samples.forEach(r => {
        const status = r.passed ? '✅' : '❌';
        console.log(`  ${status} ${r.file} (${r.lang}) - 得分: ${r.score}`);
    });
    
    console.log('\n✨ 验证完成！');
}

if (require.main === module) {
    main().catch(console.error);
}
