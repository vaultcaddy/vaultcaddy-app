/**
 * 更新特定用戶的 Credits
 * 使用方法：node update-user-credits.js
 */

const admin = require('firebase-admin');
const serviceAccount = require('./serviceAccountKey.json'); // 需要 Firebase Admin SDK 密鑰

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount)
});

const db = admin.firestore();

async function updateUserCredits(email, credits) {
    try {
        // 查找用戶
        const usersSnapshot = await db.collection('users')
            .where('email', '==', email)
            .limit(1)
            .get();
        
        if (usersSnapshot.empty) {
            console.log(`❌ 找不到用戶: ${email}`);
            return;
        }
        
        const userDoc = usersSnapshot.docs[0];
        const userId = userDoc.id;
        
        // 更新 Credits
        await db.collection('users').doc(userId).update({
            currentCredits: credits,
            updatedAt: admin.firestore.FieldValue.serverTimestamp()
        });
        
        // 記錄 Credits 歷史
        await db.collection('users').doc(userId).collection('creditsHistory').add({
            type: 'admin_adjustment',
            amount: credits,
            description: '管理員手動調整 Credits',
            createdAt: admin.firestore.FieldValue.serverTimestamp(),
            balanceAfter: credits
        });
        
        console.log(`✅ 成功更新用戶 ${email} 的 Credits 為 ${credits}`);
        
    } catch (error) {
        console.error('❌ 更新失敗:', error);
    }
}

// 更新 osclin2002@gmail.com 的 Credits 為 80000
updateUserCredits('osclin2002@gmail.com', 80000)
    .then(() => {
        console.log('✅ 操作完成');
        process.exit(0);
    })
    .catch(error => {
        console.error('❌ 操作失敗:', error);
        process.exit(1);
    });
