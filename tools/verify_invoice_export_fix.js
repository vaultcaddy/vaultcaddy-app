/**
 * 🔍 Invoice 和 Export 修复验证脚本
 * 
 * 使用方法：
 * 1. 打开任意 document-detail.html 页面
 * 2. 按 F12 打开浏览器控制台
 * 3. 复制整个脚本并粘贴到控制台
 * 4. 按 Enter 执行
 */

(async function verifyInvoiceAndExportFix() {
    console.log('%c🔍 开始验证 Invoice 和 Export 修复...', 'background: #4CAF50; color: white; padding: 10px; font-size: 16px; font-weight: bold;');
    
    const results = {
        passed: [],
        failed: [],
        warnings: []
    };
    
    // ========================================
    // 测试 1: 检查页面语言设置
    // ========================================
    console.log('\n%c📋 测试 1: 检查页面语言设置', 'background: #2196F3; color: white; padding: 5px; font-weight: bold;');
    
    const htmlLang = document.documentElement.lang;
    const currentPath = window.location.pathname;
    
    let expectedLang = 'zh-TW';
    if (currentPath.includes('/en/')) expectedLang = 'en';
    else if (currentPath.includes('/jp/')) expectedLang = 'ja';
    else if (currentPath.includes('/kr/')) expectedLang = 'ko';
    
    if (htmlLang === expectedLang) {
        results.passed.push(`✅ HTML lang 属性正确: ${htmlLang}`);
        console.log(`✅ HTML lang 属性: ${htmlLang} (预期: ${expectedLang})`);
    } else {
        results.failed.push(`❌ HTML lang 不匹配: 实际 ${htmlLang}, 预期 ${expectedLang}`);
        console.log(`❌ HTML lang 不匹配: 实际 ${htmlLang}, 预期 ${expectedLang}`);
    }
    
    // ========================================
    // 测试 2: 检查 Invoice 详情区域的文本
    // ========================================
    console.log('\n%c📋 测试 2: 检查 Invoice 详情文本', 'background: #2196F3; color: white; padding: 5px; font-weight: bold;');
    
    // 等待页面加载
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    const chinesePatterns = [
        '發票詳情',
        '項目明細',
        '發票號碼',
        '供應商',
        '總金額',
        '代碼',
        '描述',
        '數量',
        '單位',
        '單價',
        '金額'
    ];
    
    const pageText = document.body.innerText;
    let foundChinese = [];
    
    chinesePatterns.forEach(pattern => {
        if (pageText.includes(pattern)) {
            foundChinese.push(pattern);
        }
    });
    
    if (foundChinese.length === 0) {
        results.passed.push('✅ Invoice 详情区域无中文文本');
        console.log('✅ Invoice 详情区域无中文文本');
    } else {
        results.failed.push(`❌ 发现中文文本: ${foundChinese.join(', ')}`);
        console.log(`❌ 发现中文文本:`, foundChinese);
    }
    
    // 检查是否有正确的英文标题
    const expectedEnglishTerms = [
        'Invoice Details',
        'Line Items',
        'Invoice Number',
        'Vendor',
        'Total Amount',
        'Code',
        'Description',
        'Quantity',
        'Unit',
        'Unit Price',
        'Amount'
    ];
    
    let foundEnglish = [];
    expectedEnglishTerms.forEach(term => {
        if (pageText.includes(term)) {
            foundEnglish.push(term);
        }
    });
    
    if (foundEnglish.length >= 3) {
        results.passed.push(`✅ 找到英文术语: ${foundEnglish.length} 个`);
        console.log(`✅ 找到英文术语:`, foundEnglish);
    } else if (foundEnglish.length > 0) {
        results.warnings.push(`⚠️  只找到部分英文术语: ${foundEnglish.join(', ')}`);
        console.log(`⚠️  只找到部分英文术语:`, foundEnglish);
    }
    
    // ========================================
    // 测试 3: 检查 Export 按钮功能
    // ========================================
    console.log('\n%c📋 测试 3: 检查 Export 按钮', 'background: #2196F3; color: white; padding: 5px; font-weight: bold;');
    
    const exportBtn = document.querySelector('button[onclick*="toggleExportMenu"]');
    
    if (exportBtn) {
        results.passed.push('✅ 找到 Export 按钮');
        console.log('✅ 找到 Export 按钮');
        
        // 检查 toggleExportMenu 函数是否存在
        if (typeof window.toggleExportMenu === 'function') {
            results.passed.push('✅ toggleExportMenu 函数已定义');
            console.log('✅ toggleExportMenu 函数已定义');
        } else {
            results.failed.push('❌ toggleExportMenu 函数未定义');
            console.log('❌ toggleExportMenu 函数未定义');
        }
        
        // 检查 Export 菜单元素
        const exportMenu = document.getElementById('exportMenu');
        if (exportMenu) {
            results.passed.push('✅ 找到 Export 菜单元素');
            console.log('✅ 找到 Export 菜单元素');
        } else {
            results.failed.push('❌ 未找到 Export 菜单元素');
            console.log('❌ 未找到 Export 菜单元素');
        }
    } else {
        results.failed.push('❌ 未找到 Export 按钮');
        console.log('❌ 未找到 Export 按钮');
    }
    
    // ========================================
    // 测试 4: 检查 currentDocument 对象
    // ========================================
    console.log('\n%c📋 测试 4: 检查 currentDocument 对象', 'background: #2196F3; color: white; padding: 5px; font-weight: bold;');
    
    if (window.currentDocument) {
        results.passed.push('✅ window.currentDocument 已定义');
        console.log('✅ window.currentDocument:', window.currentDocument);
        
        const docType = window.currentDocument.type || window.currentDocument.documentType;
        if (docType && typeof docType === 'string') {
            results.passed.push(`✅ 文档类型正确: ${docType} (${typeof docType})`);
            console.log(`✅ 文档类型: ${docType} (类型: ${typeof docType})`);
        } else if (docType) {
            results.failed.push(`❌ 文档类型异常: ${docType} (${typeof docType})`);
            console.log(`❌ 文档类型异常:`, docType, typeof docType);
        } else {
            results.warnings.push('⚠️  未找到文档类型');
            console.log('⚠️  未找到文档类型');
        }
    } else {
        results.warnings.push('⚠️  window.currentDocument 未定义（可能文档未加载完成）');
        console.log('⚠️  window.currentDocument 未定义');
    }
    
    // ========================================
    // 测试 5: 模拟点击 Export 按钮
    // ========================================
    console.log('\n%c📋 测试 5: 模拟打开 Export 菜单', 'background: #2196F3; color: white; padding: 5px; font-weight: bold;');
    
    if (exportBtn && typeof window.toggleExportMenu === 'function') {
        try {
            // 点击按钮
            exportBtn.click();
            
            // 等待菜单显示
            await new Promise(resolve => setTimeout(resolve, 500));
            
            const exportMenu = document.getElementById('exportMenu');
            if (exportMenu && exportMenu.style.display === 'block') {
                results.passed.push('✅ Export 菜单成功打开');
                console.log('✅ Export 菜单成功打开');
                
                // 检查菜单内容
                const menuContent = exportMenu.innerHTML;
                const hasContent = menuContent.length > 100;
                
                if (hasContent) {
                    results.passed.push('✅ Export 菜单有内容');
                    console.log(`✅ Export 菜单内容长度: ${menuContent.length} 字符`);
                    
                    // 检查是否包含导出选项
                    const hasCSV = menuContent.includes('CSV');
                    const hasQBO = menuContent.includes('QBO');
                    const hasIIF = menuContent.includes('IIF');
                    
                    if (hasCSV || hasQBO || hasIIF) {
                        results.passed.push('✅ 找到导出选项 (CSV/QBO/IIF)');
                        console.log(`✅ 导出选项: CSV=${hasCSV}, QBO=${hasQBO}, IIF=${hasIIF}`);
                    } else {
                        results.warnings.push('⚠️  未找到常见的导出选项');
                        console.log('⚠️  未找到常见的导出选项');
                    }
                } else {
                    results.failed.push('❌ Export 菜单内容为空或过短');
                    console.log(`❌ Export 菜单内容长度: ${menuContent.length} 字符`);
                }
                
                // 关闭菜单
                if (typeof window.closeExportMenu === 'function') {
                    window.closeExportMenu();
                }
            } else {
                results.failed.push('❌ Export 菜单未显示');
                console.log('❌ Export 菜单未显示');
            }
        } catch (error) {
            results.failed.push(`❌ 打开 Export 菜单时出错: ${error.message}`);
            console.error('❌ 打开 Export 菜单时出错:', error);
        }
    } else {
        results.warnings.push('⚠️  跳过 Export 菜单测试（按钮或函数不可用）');
        console.log('⚠️  跳过 Export 菜单测试');
    }
    
    // ========================================
    // 测试 6: 检查控制台错误
    // ========================================
    console.log('\n%c📋 测试 6: 检查 JavaScript 错误', 'background: #2196F3; color: white; padding: 5px; font-weight: bold;');
    
    // 注意：这个测试需要在页面加载时就开始监听错误
    // 这里只能检查当前没有明显的运行时错误
    
    console.log('ℹ️  请检查控制台是否有红色错误信息');
    results.warnings.push('⚠️  请手动检查控制台是否有 JavaScript 错误');
    
    // ========================================
    // 输出测试结果汇总
    // ========================================
    console.log('\n' + '='.repeat(60));
    console.log('%c📊 测试结果汇总', 'background: #FF9800; color: white; padding: 10px; font-size: 16px; font-weight: bold;');
    console.log('='.repeat(60));
    
    console.log(`\n%c✅ 通过: ${results.passed.length} 项`, 'color: green; font-weight: bold;');
    results.passed.forEach(item => console.log(item));
    
    if (results.warnings.length > 0) {
        console.log(`\n%c⚠️  警告: ${results.warnings.length} 项`, 'color: orange; font-weight: bold;');
        results.warnings.forEach(item => console.log(item));
    }
    
    if (results.failed.length > 0) {
        console.log(`\n%c❌ 失败: ${results.failed.length} 项`, 'color: red; font-weight: bold;');
        results.failed.forEach(item => console.log(item));
    }
    
    // 最终判定
    console.log('\n' + '='.repeat(60));
    if (results.failed.length === 0) {
        console.log('%c🎉 恭喜！所有关键测试通过！', 'background: #4CAF50; color: white; padding: 10px; font-size: 16px; font-weight: bold;');
        console.log('%c✅ Invoice 和 Export 修复验证成功', 'color: green; font-weight: bold; font-size: 14px;');
    } else {
        console.log('%c⚠️  发现问题，需要进一步检查', 'background: #f44336; color: white; padding: 10px; font-size: 16px; font-weight: bold;');
        console.log('%c请将上述失败项反馈给开发团队', 'color: red; font-weight: bold; font-size: 14px;');
    }
    console.log('='.repeat(60));
    
    // 返回结果对象（可以在控制台中访问）
    window.verificationResults = {
        passed: results.passed.length,
        warnings: results.warnings.length,
        failed: results.failed.length,
        details: results
    };
    
    console.log('\n💡 提示: 测试结果已保存到 window.verificationResults');
    
    return window.verificationResults;
})();

