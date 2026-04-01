/**
 * 🔧 为相似页面添加Canonical标签
 * 目的：避免被Google识别为门页策略
 */

const fs = require('fs');
const path = require('path');

// 配置
const CONFIG = {
    // 定义主页面（保留独立索引）
    keepIndependent: [
        // Top 30 最重要的银行页面（将来会添加独特内容）
        'chase-bank-statement',
        'bank-of-america-statement',
        'wells-fargo-statement',
        'hsbc-bank-statement',
        'hsbc-hong-kong-statement',
        'hang-seng-bank-statement',
        'boc-hong-kong-statement',
        'citibank-statement',
        'barclays-bank-statement',
        'lloyds-bank-statement',
        'mufg-bank-statement',
        'mizuho-bank-statement',
        'smbc-bank-statement',
        'kb-kookmin-bank-statement',
        'shinhan-bank-statement',
        'hana-bank-statement',
        
        // 主要功能页面
        'bank-statement-to-qbo-converter',
        'bank-statement-to-quickbooks-online',
        'pdf-to-excel-converter',
        'receipt-scanner',
        'invoice-processing',
    ],
    
    // 主页面映射
    canonicalMapping: {
        'default': 'https://vaultcaddy.com/',
        'qbo': 'https://vaultcaddy.com/bank-statement-to-qbo-converter.html',
        'quickbooks': 'https://vaultcaddy.com/bank-statement-to-quickbooks-online.html',
        'excel': 'https://vaultcaddy.com/pdf-to-excel-converter.html',
        'receipt': 'https://vaultcaddy.com/receipt-scanner.html',
        'invoice': 'https://vaultcaddy.com/invoice-processing.html',
    },
    
    backupDir: path.join(__dirname, 'backup_before_canonical_' + Date.now()),
    dryRun: false, // 设置为true仅预览
};

/**
 * 判断文件是否应该保持独立索引
 */
function shouldKeepIndependent(filePath) {
    const fileName = path.basename(filePath, '.html');
    return CONFIG.keepIndependent.some(pattern => fileName.includes(pattern));
}

/**
 * 确定应该使用的canonical URL
 */
function getCanonicalUrl(filePath) {
    const fileName = path.basename(filePath).toLowerCase();
    
    // 如果是保持独立的页面，canonical指向自己
    if (shouldKeepIndependent(filePath)) {
        return null; // 不添加或保持原有canonical
    }
    
    // 根据文件名判断应该指向哪个主页面
    if (fileName.includes('qbo') || fileName.includes('quickbooks')) {
        return CONFIG.canonicalMapping.qbo;
    }
    if (fileName.includes('excel')) {
        return CONFIG.canonicalMapping.excel;
    }
    if (fileName.includes('receipt')) {
        return CONFIG.canonicalMapping.receipt;
    }
    if (fileName.includes('invoice')) {
        return CONFIG.canonicalMapping.invoice;
    }
    
    // 默认指向主页
    return CONFIG.canonicalMapping.default;
}

/**
 * 添加或更新canonical标签
 */
function addCanonicalTag(filePath, canonicalUrl) {
    let html = fs.readFileSync(filePath, 'utf8');
    
    if (!canonicalUrl) {
        // 保持独立索引的页面，不修改
        return { modified: false, reason: 'keep-independent' };
    }
    
    // 检查是否已有canonical
    const hasCanonical = /<link\s+rel="canonical"\s+href="[^"]*"/i.test(html);
    
    if (hasCanonical) {
        // 检查现有canonical是否正确
        const currentCanonical = html.match(/<link\s+rel="canonical"\s+href="([^"]*)"/i);
        if (currentCanonical && currentCanonical[1] === canonicalUrl) {
            return { modified: false, reason: 'already-correct' };
        }
        
        // 更新现有canonical
        html = html.replace(
            /<link\s+rel="canonical"\s+href="[^"]*"/i,
            `<link rel="canonical" href="${canonicalUrl}"`
        );
    } else {
        // 添加新canonical（在</head>前）
        html = html.replace(
            /(<\/head>)/i,
            `    <link rel="canonical" href="${canonicalUrl}">\n    $1`
        );
    }
    
    if (!CONFIG.dryRun) {
        fs.writeFileSync(filePath, html, 'utf8');
    }
    
    return { 
        modified: true, 
        reason: hasCanonical ? 'updated' : 'added',
        canonicalUrl 
    };
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
    const langDirs = ['ja-JP', 'ko-KR', 'zh-HK', 'zh-TW'];
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
    console.log('🔧 添加Canonical标签 - 避免门页策略');
    console.log('='.repeat(80));
    console.log(`模式: ${CONFIG.dryRun ? '🔍 预览模式（不会修改文件）' : '✍️  实际修改'}`);
    console.log('');
    
    // 获取所有文件
    const files = getAllV2V3Files();
    console.log(`找到 ${files.length} 个文件\n`);
    
    // 创建备份目录
    if (!CONFIG.dryRun && !fs.existsSync(CONFIG.backupDir)) {
        fs.mkdirSync(CONFIG.backupDir, { recursive: true });
        console.log(`📦 备份目录: ${CONFIG.backupDir}\n`);
    }
    
    // 统计
    const stats = {
        keepIndependent: 0,
        addedCanonical: 0,
        updatedCanonical: 0,
        alreadyCorrect: 0,
        byCanonical: {},
    };
    
    // 处理每个文件
    console.log('📊 处理文件...\n');
    
    for (const file of files) {
        const relativePath = path.relative(__dirname, file);
        
        // 备份
        if (!CONFIG.dryRun) {
            const backupPath = path.join(CONFIG.backupDir, relativePath);
            const backupDir = path.dirname(backupPath);
            if (!fs.existsSync(backupDir)) {
                fs.mkdirSync(backupDir, { recursive: true });
            }
            fs.copyFileSync(file, backupPath);
        }
        
        // 处理
        const canonicalUrl = getCanonicalUrl(file);
        const result = addCanonicalTag(file, canonicalUrl);
        
        // 统计
        if (result.reason === 'keep-independent') {
            stats.keepIndependent++;
            console.log(`✨ 保持独立: ${relativePath}`);
        } else if (result.reason === 'added') {
            stats.addedCanonical++;
            console.log(`➕ 添加Canonical: ${relativePath} → ${result.canonicalUrl}`);
            
            if (!stats.byCanonical[result.canonicalUrl]) {
                stats.byCanonical[result.canonicalUrl] = 0;
            }
            stats.byCanonical[result.canonicalUrl]++;
        } else if (result.reason === 'updated') {
            stats.updatedCanonical++;
            console.log(`🔄 更新Canonical: ${relativePath} → ${result.canonicalUrl}`);
            
            if (!stats.byCanonical[result.canonicalUrl]) {
                stats.byCanonical[result.canonicalUrl] = 0;
            }
            stats.byCanonical[result.canonicalUrl]++;
        } else if (result.reason === 'already-correct') {
            stats.alreadyCorrect++;
        }
    }
    
    // 显示统计
    console.log('\n' + '='.repeat(80));
    console.log('📊 处理统计');
    console.log('='.repeat(80));
    console.log(`✨ 保持独立索引: ${stats.keepIndependent} 个`);
    console.log(`➕ 添加Canonical: ${stats.addedCanonical} 个`);
    console.log(`🔄 更新Canonical: ${stats.updatedCanonical} 个`);
    console.log(`✅ 已经正确: ${stats.alreadyCorrect} 个`);
    console.log(`📝 总计: ${files.length} 个`);
    
    console.log('\n按Canonical URL统计:');
    console.log('-'.repeat(80));
    Object.keys(stats.byCanonical).sort().forEach(url => {
        const count = stats.byCanonical[url];
        console.log(`${count.toString().padStart(4)} 个页面 → ${url}`);
    });
    
    if (!CONFIG.dryRun) {
        console.log(`\n📦 备份目录: ${CONFIG.backupDir}`);
    }
    
    console.log('\n✨ 完成！');
    
    // 显示建议
    console.log('\n' + '='.repeat(80));
    console.log('💡 下一步建议');
    console.log('='.repeat(80));
    console.log(`
1. 监控Google Search Console
   - 检查索引状态变化
   - 观察是否有"手动操作"警告
   
2. 为保持独立的${stats.keepIndependent}个页面添加独特内容
   - 每个页面至少1000-1500字独特内容
   - 添加银行特定的功能说明
   - 添加真实客户案例
   
3. 2周后评估效果
   - 检查曝光量变化
   - 监控排名变化
   - 分析用户行为数据
    `);
}

if (require.main === module) {
    main().catch(console.error);
}

module.exports = { addCanonicalTag, getCanonicalUrl };
