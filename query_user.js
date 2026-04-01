const admin = require('firebase-admin');
const serviceAccount = require('./firebase-functions/serviceAccountKey.json');

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount)
});

const db = admin.firestore();

async function queryUser() {
  try {
    const snapshot = await db.collection('users')
      .where('email', '==', 'vaultcaddy@gmail.com')
      .get();
    
    if (snapshot.empty) {
      console.log('❌ 未找到用户: vaultcaddy@gmail.com');
      return;
    }
    
    snapshot.forEach(doc => {
      console.log('✅ 找到用户:', doc.id);
      console.log('📊 用户数据:', JSON.stringify(doc.data(), null, 2));
    });
  } catch (error) {
    console.error('❌ 查询失败:', error);
  }
  
  process.exit(0);
}

queryUser();
