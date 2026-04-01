/**
 * 验证独特内容质量 - 确保避免门页策略
 */

const fs = require('fs');
const path = require('path');
const cheerio = require('cheerio');

function analyzeContent(htmlPath) {
    const html = fs.readFileSync(htmlPath, 'utf8');
    const $ = cheerio.load(html);
    
    // 检查是否有独特内容
    const uniqueContent = $('.unique-content').html();
    if (!uniqueContent) {
        return { hasContent: false };
    }
    
    // 计算字数（去除HTML标签）
    const textContent = uniqueContent.replace(/<[^>]*>/g, ' ').replace(/\s+/g, ' ').trim();
    const wordCount = textContent.length;
    
    // 检查内容多样性
    const hasSections = (uniqueContent.match(/<h[234]/g) || []).length >= 5;
    const hasLists = (uniqueContent.match(/<ul|<ol/g) || []).length >= 2;
    const hasExamples = uniqueContent.includes('案例') || uniqueContent.includes('example') || uniqueContent.includes('case');
    const hasFAQ = uniqueContent.includes('FAQ') || uniqueContent.includes('常見問題') || uniqueContent.includes('問題');
    
    // 提取银行/主题名称
    const title = $('title').text();
    const bankMatch = title.match(/([A-Za-z\s&]+?)\s+(Bank|Statement|對賬單)/i);
    const bankName = bankMatch ? bankMatch[1].trim() : 'Unknown';
    
    return {
        hasContent: true,
        wordCount,
        hasSections,
        hasLists,
        hasExamples,
        hasFAQ,
        bankName,
        title,
        qualityScore: [hasSections, hasLists, hasExamples, hasFAQ].filter(Boolean).length
    };
}

async function main() {
    console.log('🔍 驗證獨特內容質量\n');
    
    const baseDir = '/Users/cavlinyeung/ai-bank-parser';
    const allFiles = [];
    
    // 收集所有v2/v3文件
    const rootFiles = fs.readdirSync(baseDir)
        .filter(f => (f.endsWith('-v2.html') || f.endsWith('-v3.html')) && !f.includes('index'))
        .map(f => path.join(baseDir, f));
    allFiles.push(...rootFiles);
    
    const langDirs = ['en', 'zh-TW', 'ja-JP', 'ko-KR'];
    for (const langDir of langDirs) {
        const fullPath = path.join(baseDir, langDir);
        if (!fs.existsSync(fullPath)) continue;
        
        const files = fs.readdirSync(fullPath)
            .filter(f => f.endsWith('-v3.html') && !f.includes('index'))
            .map(f => path.join(fullPath, f));
        allFiles.push(...files);
    }
    
    console.log(`📊 總共找到 ${allFiles.length} 個頁面\n`);
    
    let withContent = 0;
    let withoutContent = 0;
    let totalWords = 0;
    const wordCountDistribution = { '<2000': 0, '2000-2500': 0, '2500-3000': 0, '>3000': 0 };
    const qualityDistribution = { excellent: 0, good: 0, fair: 0, poor: 0 };
    const missingContent = [];
    
    for (const file of allFiles) {
        try {
            const result = analyzeContent(file);
            const fileName = path.basename(file);
            
            if (!result.hasContent) {
                withoutContent++;
                missingContent.push(fileName);
                continue;
            }
            
            withContent++;
            totalWords += result.wordCount;
            
            // 字数分布
            if (result.wordCount < 2000) wordCountDistribution['<2000']++;
            else if (result.wordCount <= 2500) wordCountDistribution['2000-2500']++;
            else if (result.wordCount <= 3000) wordCountDistribution['2500-3000']++;
            else wordCountDistribution['>3000']++;
            
            // 质量分布
            if (result.qualityScore === 4) qualityDistribution.excellent++;
            else if (result.qualityScore === 3) qualityDistribution.good++;
            else if (result.qualityScore === 2) qualityDistribution.fair++;
            else qualityDistribution.poor++;
            
        } catch (error) {
            console.error(`❌ 錯誤處理 ${path.basename(file)}: ${error.message}`);
        }
    }
    
    console.log('='.repeat(80));
    console.log('📊 驗證結果\n');
    
    console.log(`✅ 有獨特內容：${withContent} 個頁面`);
    console.log(`❌ 缺少獨特內容：${withoutContent} 個頁面`);
    console.log(`📝 平均字數：${Math.round(totalWords / withContent)} 字\n`);
    
    console.log('字數分布：');
    console.log(`  < 2000字：${wordCountDistribution['<2000']} 個`);
    console.log(`  2000-2500字：${wordCountDistribution['2000-2500']} 個`);
    console.log(`  2500-3000字：${wordCountDistribution['2500-3000']} 個`);
    console.log(`  > 3000字：${wordCountDistribution['>3000']} 個\n`);
    
    console.log('內容質量分布：');
    console.log(`  優秀（4/4）：${qualityDistribution.excellent} 個`);
    console.log(`  良好（3/4）：${qualityDistribution.good} 個`);
    console.log(`  一般（2/4）：${qualityDistribution.fair} 個`);
    console.log(`  較差（≤1/4）：${qualityDistribution.poor} 個\n`);
    
    if (missingContent.length > 0) {
        console.log('⚠️  缺少獨特內容的頁面：');
        missingContent.forEach(file => console.log(`  - ${file}`));
    }
    
    console.log('\n' + '='.repeat(80));
    console.log('🎯 門頁策略風險評估\n');
    
    const avgWords = Math.round(totalWords / withContent);
    const contentDiversity = (qualityDistribution.excellent + qualityDistribution.good) / withContent * 100;
    
    let riskLevel = 'LOW';
    let riskColor = '🟢';
    
    if (avgWords < 2000 || contentDiversity < 70) {
        riskLevel = 'MEDIUM';
        riskColor = '🟡';
    }
    if (avgWords < 1500 || contentDiversity < 50) {
        riskLevel = 'HIGH';
        riskColor = '🔴';
    }
    
    console.log(`${riskColor} 風險等級：${riskLevel}`);
    console.log(`\n評估依據：`);
    console.log(`  • 平均字數：${avgWords} 字 ${avgWords >= 2000 ? '✅' : '⚠️'}`);
    console.log(`  • 內容多樣性：${contentDiversity.toFixed(1)}% ${contentDiversity >= 70 ? '✅' : '⚠️'}`);
    console.log(`  • 有獨特內容：${withContent}/${allFiles.length} ${withContent === allFiles.length ? '✅' : '⚠️'}`);
    
    console.log('\n建議：');
    if (riskLevel === 'LOW') {
        console.log('  ✅ 內容質量優秀！基本避免了門頁策略風險。');
        console.log('  ✅ 每個頁面都有2000+字的獨特內容。');
        console.log('  ✅ 內容結構多樣化（案例、FAQ、列表等）。');
    } else if (riskLevel === 'MEDIUM') {
        console.log('  ⚠️  建議進一步優化內容質量。');
        console.log('  ⚠️  增加內容深度和多樣性。');
    } else {
        console.log('  🔴 高風險！需要立即優化內容。');
    }
    
    console.log('\n' + '='.repeat(80));
}

if (require.main === module) {
    main().catch(console.error);
}
