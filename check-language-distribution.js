/**
 * 检查实际的语言分布
 */

const fs = require('fs');
const path = require('path');

function getAllV2V3Files() {
    const files = [];
    
    // 根目录
    const rootFiles = fs.readdirSync(__dirname)
        .filter(f => (f.endsWith('-v2.html') || f.endsWith('-v3.html')) && 
                     !f.includes('backup') && !f.includes('tmp'))
        .map(f => path.join(__dirname, f));
    files.push(...rootFiles);
    
    // 所有子目录
    const dirs = fs.readdirSync(__dirname)
        .filter(f => {
            const fullPath = path.join(__dirname, f);
            return fs.statSync(fullPath).isDirectory() && 
                   !f.includes('backup') && 
                   !f.includes('node_modules') &&
                   !f.includes('blog') &&
                   !f.includes('solutions');
        });
    
    dirs.forEach(dir => {
        const dirPath = path.join(__dirname, dir);
        const dirFiles = fs.readdirSync(dirPath)
            .filter(f => f.endsWith('-v3.html') && !f.includes('backup') && !f.includes('tmp'))
            .map(f => path.join(dirPath, f));
        files.push(...dirFiles);
    });
    
    return files;
}

function detectLang(filePath) {
    const html = fs.readFileSync(filePath, 'utf8');
    const langMatch = html.match(/<html\s+lang="([^"]*)"/i);
    return langMatch ? langMatch[1] : 'unknown';
}

function main() {
    console.log('='.repeat(80));
    console.log('📊 实际语言分布统计');
    console.log('='.repeat(80));
    console.log('');
    
    const files = getAllV2V3Files();
    console.log(`总文件数: ${files.length}\n`);
    
    // 按语言分组
    const byLang = {};
    const byDir = {};
    
    files.forEach(file => {
        const lang = detectLang(file);
        const relativePath = path.relative(__dirname, file);
        const dir = relativePath.includes('/') ? relativePath.split('/')[0] : '根目录';
        
        if (!byLang[lang]) {
            byLang[lang] = [];
        }
        byLang[lang].push(relativePath);
        
        if (!byDir[dir]) {
            byDir[dir] = { total: 0, langs: {} };
        }
        byDir[dir].total++;
        if (!byDir[dir].langs[lang]) {
            byDir[dir].langs[lang] = 0;
        }
        byDir[dir].langs[lang]++;
    });
    
    // 显示按语言统计
    console.log('📊 按语言统计:');
    console.log('-'.repeat(80));
    Object.keys(byLang).sort().forEach(lang => {
        const count = byLang[lang].length;
        const pct = (count / files.length * 100).toFixed(1);
        console.log(`${lang.padEnd(15)} ${count.toString().padStart(4)} 个 (${pct}%)`);
    });
    
    // 显示按目录统计
    console.log('\n📁 按目录统计:');
    console.log('-'.repeat(80));
    Object.keys(byDir).sort().forEach(dir => {
        const stats = byDir[dir];
        console.log(`\n${dir}: ${stats.total} 个文件`);
        Object.keys(stats.langs).sort().forEach(lang => {
            console.log(`  ${lang.padEnd(15)} ${stats.langs[lang]} 个`);
        });
    });
    
    // 显示示例文件
    console.log('\n📝 各语言示例文件:');
    console.log('-'.repeat(80));
    Object.keys(byLang).sort().forEach(lang => {
        const examples = byLang[lang].slice(0, 3);
        console.log(`\n${lang}:`);
        examples.forEach(file => {
            console.log(`  - ${file}`);
        });
        if (byLang[lang].length > 3) {
            console.log(`  ... 还有 ${byLang[lang].length - 3} 个文件`);
        }
    });
    
    console.log('\n' + '='.repeat(80));
    console.log('✨ 统计完成');
    console.log('='.repeat(80));
}

if (require.main === module) {
    main();
}
