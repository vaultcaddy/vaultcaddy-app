/**
 * API 配置測試腳本
 * 用於驗證所有API服務是否正確配置
 */

// 載入安全配置
const { getSecureConfig } = require('./config-secure');

async function testAPIConfiguration() {
    console.log('🔍 開始測試 API 配置...\n');

    try {
        const config = getSecureConfig();
        
        // 顯示安全的配置信息（遮蔽敏感數據）
        console.log('📋 當前配置狀態：');
        console.log(JSON.stringify(config.getSafeConfigForLogging(), null, 2));
        console.log('\n');

        // 測試各個服務
        console.log('🔧 服務可用性檢查：');
        
        const services = ['googleCloud', 'azure', 'aws'];
        const availableServices = [];

        for (const service of services) {
            const isAvailable = config.isServiceAvailable(service);
            const status = isAvailable ? '✅' : '❌';
            console.log(`${status} ${service}: ${isAvailable ? '已配置' : '未配置'}`);
            
            if (isAvailable) {
                availableServices.push(service);
            }
        }

        console.log(`\n📊 總計：${availableServices.length}/${services.length} 個服務已配置\n`);

        // 詳細的Google Cloud配置檢查
        if (config.isServiceAvailable('googleCloud')) {
            console.log('🔍 Google Cloud 詳細配置：');
            const gcConfig = config.getGoogleCloudConfig();
            
            console.log(`   項目ID: ${gcConfig.projectId}`);
            console.log(`   認證方式: ${gcConfig.keyFilename ? 'Service Account JSON' : 'API Key'}`);
            console.log(`   處理器配置:`);
            
            const processors = gcConfig.processors || {};
            Object.entries(processors).forEach(([type, id]) => {
                const status = id ? '✅' : '❌';
                console.log(`     ${status} ${type}: ${id ? '已配置' : '未配置'}`);
            });
        }

        // 提供下一步建議
        console.log('\n💡 下一步建議：');
        
        if (availableServices.length === 0) {
            console.log('❌ 沒有任何API服務被配置');
            console.log('   請按照 GOOGLE_CLOUD_SETUP.md 的指引進行設置');
        } else if (availableServices.includes('googleCloud')) {
            console.log('✅ Google Cloud 已配置，可以開始處理文檔');
            console.log('   建議執行: node test-document-processing.js');
        } else {
            console.log('⚠️  部分服務已配置，建議完成 Google Cloud 設置以獲得最佳體驗');
        }

        return {
            success: true,
            availableServices,
            totalServices: services.length
        };

    } catch (error) {
        console.error('❌ 配置測試失敗:', error.message);
        console.log('\n🔧 故障排除建議：');
        console.log('1. 確認 .env 檔案存在且包含必要的環境變數');
        console.log('2. 檢查 Google Cloud 服務帳戶 JSON 檔案路徑');
        console.log('3. 驗證所有 API 密鑰格式正確');
        console.log('4. 參考 GOOGLE_CLOUD_SETUP.md 完整設置指南');
        
        return {
            success: false,
            error: error.message
        };
    }
}

// 如果直接執行此腳本
if (require.main === module) {
    testAPIConfiguration()
        .then(result => {
            if (result.success) {
                console.log(`\n🎉 配置測試完成！${result.availableServices.length}/${result.totalServices} 個服務可用`);
                process.exit(0);
            } else {
                console.log('\n💥 配置測試失敗，請檢查設置');
                process.exit(1);
            }
        })
        .catch(error => {
            console.error('💥 測試腳本執行失敗:', error);
            process.exit(1);
        });
}

module.exports = { testAPIConfiguration };

