const admin = require('firebase-admin');

admin.initializeApp();

const db = admin.firestore();

async function queryUser() {
  try {
    const snapshot = await db.collection('users')
      .where('email', '==', 'vaultcaddy@gmail.com')
      .get();
    
    if (snapshot.empty) {
      console.log('❌ 未找到用户: vaultcaddy@gmail.com');
      console.log('\n让我列出所有用户...\n');
      
      const allUsers = await db.collection('users').get();
      console.log(`总用户数: ${allUsers.size}`);
      allUsers.forEach(doc => {
        const data = doc.data();
        console.log(`\n用户 ID: ${doc.id}`);
        console.log(`Email: ${data.email}`);
        console.log(`Credits: ${data.credits || data.currentCredits || 0}`);
      });
      return;
    }
    
    snapshot.forEach(doc => {
      console.log('\n✅ 找到用户 ID:', doc.id);
      console.log('📊 用户数据:', JSON.stringify(doc.data(), null, 2));
    });
  } catch (error) {
    console.error('❌ 查询失败:', error);
  }
  
  process.exit(0);
}

queryUser();
