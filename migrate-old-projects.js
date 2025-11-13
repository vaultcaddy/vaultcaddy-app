/**
 * 遷移舊項目數據到新路徑
 * 
 * 舊路徑: projects/{projectId}
 * 新路徑: users/{userId}/projects/{projectId}
 * 
 * 使用方法：
 * 1. 在 Firebase Console 的 Firestore 中打開這個腳本
 * 2. 或在本地運行：node migrate-old-projects.js
 */

// 如果在 Node.js 環境運行
const admin = require('firebase-admin');

// 初始化 Firebase Admin（如果還沒初始化）
if (!admin.apps.length) {
    admin.initializeApp({
        // 您可以使用服務帳戶金鑰，或在 Firebase Console 中運行
    });
}

const db = admin.firestore();

async function migrateOldProjects() {
    console.log('🔄 開始遷移舊項目數據...');
    
    try {
        // 1. 獲取所有舊項目（直接在 projects collection 中）
        const oldProjectsSnapshot = await db.collection('projects').get();
        
        if (oldProjectsSnapshot.empty) {
            console.log('✅ 沒有需要遷移的舊項目');
            return;
        }
        
        console.log(`📦 找到 ${oldProjectsSnapshot.size} 個舊項目`);
        
        let successCount = 0;
        let failCount = 0;
        
        // 2. 遍歷每個舊項目
        for (const projectDoc of oldProjectsSnapshot.docs) {
            const projectId = projectDoc.id;
            const projectData = projectDoc.data();
            
            console.log(`\n處理項目: ${projectId}`);
            console.log(`  名稱: ${projectData.name}`);
            console.log(`  用戶ID: ${projectData.userId}`);
            
            // 檢查是否有 userId
            if (!projectData.userId) {
                console.warn(`  ⚠️  跳過：缺少 userId`);
                failCount++;
                continue;
            }
            
            try {
                // 3. 創建新路徑的項目
                const newProjectRef = db.collection('users')
                    .doc(projectData.userId)
                    .collection('projects')
                    .doc(projectId);
                
                // 複製項目數據（移除 userId 因為它現在在路徑中）
                const { userId, ...newProjectData } = projectData;
                await newProjectRef.set(newProjectData);
                
                console.log(`  ✅ 項目已複製到新路徑`);
                
                // 4. 遷移項目下的文檔（如果有）
                const oldDocumentsSnapshot = await db.collection('documents')
                    .where('projectId', '==', projectId)
                    .get();
                
                if (!oldDocumentsSnapshot.empty) {
                    console.log(`  📄 找到 ${oldDocumentsSnapshot.size} 個文檔，開始遷移...`);
                    
                    for (const docDoc of oldDocumentsSnapshot.docs) {
                        const docId = docDoc.id;
                        const docData = docDoc.data();
                        
                        // 創建新路徑的文檔
                        const newDocRef = db.collection('users')
                            .doc(projectData.userId)
                            .collection('projects')
                            .doc(projectId)
                            .collection('documents')
                            .doc(docId);
                        
                        // 複製文檔數據（移除 projectId）
                        const { projectId: _, ...newDocData } = docData;
                        await newDocRef.set(newDocData);
                        
                        console.log(`    ✅ 文檔已遷移: ${docData.fileName || docId}`);
                    }
                }
                
                // 5. 刪除舊項目（可選，建議先確認新數據正確後再刪除）
                // await projectDoc.ref.delete();
                // console.log(`  🗑️  舊項目已刪除`);
                
                successCount++;
                console.log(`  🎉 項目遷移完成！`);
                
            } catch (error) {
                console.error(`  ❌ 遷移失敗:`, error);
                failCount++;
            }
        }
        
        console.log('\n' + '='.repeat(50));
        console.log('📊 遷移統計：');
        console.log(`  ✅ 成功: ${successCount} 個項目`);
        console.log(`  ❌ 失敗: ${failCount} 個項目`);
        console.log('='.repeat(50));
        
        if (successCount > 0) {
            console.log('\n⚠️  重要提示：');
            console.log('1. 請在 Dashboard 上確認新數據是否正確顯示');
            console.log('2. 確認無誤後，可以手動刪除舊的 projects 和 documents collection');
            console.log('3. 前往 Firebase Console > Firestore > projects > 刪除');
        }
        
    } catch (error) {
        console.error('❌ 遷移過程發生錯誤:', error);
    }
}

// 執行遷移
migrateOldProjects();

// 如果需要清理舊數據（在確認新數據正確後才執行）
async function cleanupOldData() {
    console.log('🧹 開始清理舊數據...');
    
    const confirm = prompt('⚠️  確定要刪除舊數據嗎？這個操作無法撤銷！(yes/no)');
    
    if (confirm !== 'yes') {
        console.log('❌ 取消清理');
        return;
    }
    
    try {
        // 刪除舊 projects collection
        const projectsSnapshot = await db.collection('projects').get();
        for (const doc of projectsSnapshot.docs) {
            await doc.ref.delete();
        }
        console.log('✅ projects collection 已刪除');
        
        // 刪除舊 documents collection
        const documentsSnapshot = await db.collection('documents').get();
        for (const doc of documentsSnapshot.docs) {
            await doc.ref.delete();
        }
        console.log('✅ documents collection 已刪除');
        
        console.log('🎉 清理完成！');
        
    } catch (error) {
        console.error('❌ 清理失敗:', error);
    }
}

// 導出函數以便在其他地方使用
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        migrateOldProjects,
        cleanupOldData
    };
}

