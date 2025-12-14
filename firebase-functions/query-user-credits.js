/**
 * 查询用户 Credits 历史的 Cloud Function
 * 
 * 使用方法：
 * 1. 部署此函数
 * 2. 在浏览器控制台调用：
 *    const f = firebase.functions().httpsCallable('queryUserCredits');
 *    const result = await f({ email: 'osclin2002@gmail.com' });
 *    console.log(result.data);
 */

const functions = require('firebase-functions');
const admin = require('firebase-admin');

exports.queryUserCredits = functions.https.onCall(async (data, context) => {
    const { email } = data;
    
    if (!email) {
        throw new functions.https.HttpsError('invalid-argument', '缺少 email 参数');
    }
    
    try {
        // 查找用户
        const usersSnapshot = await admin.firestore().collection('users')
            .where('email', '==', email)
            .limit(1)
            .get();
        
        if (usersSnapshot.empty) {
            throw new functions.https.HttpsError('not-found', '找不到用户');
        }
        
        const userDoc = usersSnapshot.docs[0];
        const userId = userDoc.id;
        const userData = userDoc.data();
        
        // 获取 Credits 历史
        const historySnapshot = await admin.firestore()
            .collection('users')
            .doc(userId)
            .collection('creditsHistory')
            .orderBy('timestamp', 'desc')
            .limit(100)
            .get();
        
        const history = historySnapshot.docs.map(doc => ({
            id: doc.id,
            ...doc.data(),
            timestamp: doc.data().timestamp?.toDate?.()?.toISOString() || null
        }));
        
        // 统计添加的次数
        const addRecords = history.filter(h => h.type === 'add');
        const totalAdded = addRecords.reduce((sum, h) => sum + (h.amount || 0), 0);
        
        return {
            userId,
            email: userData.email,
            currentCredits: userData.credits || 0,
            currentCreditsField: userData.currentCredits || 0,
            planType: userData.planType || 'Free Plan',
            totalAdded,
            addCount: addRecords.length,
            history: history.slice(0, 20) // 只返回前 20 条
        };
        
    } catch (error) {
        console.error('查询失败:', error);
        throw new functions.https.HttpsError('internal', error.message);
    }
});

