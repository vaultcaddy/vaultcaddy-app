const fs = require('fs');
const path = './simple-auth.js';
let code = fs.readFileSync(path, 'utf8');

// Replace init()
code = code.replace(
    /this\.auth = firebase\.auth\(\);\s+console\.log\('⏳ 等待第一次 Auth 狀態回調\.\.\.'\);/,
    `this.auth = firebase.auth();
            
            // 處理 Redirect 登入結果
            try {
                const redirectResult = await this.auth.getRedirectResult();
                if (redirectResult && redirectResult.user) {
                    console.log('✅ 處理 Redirect 登入成功');
                    await this.handleUserFirstLogin(redirectResult.user);
                }
            } catch (redirectError) {
                console.error('❌ Redirect 登入處理失敗:', redirectError);
            }
            
            console.log('⏳ 等待第一次 Auth 狀態回調...');`
);

// Replace loginWithGoogle
const loginWithGoogleRegex = /async loginWithGoogle\(\) \{[\s\S]*?return result;\n        \} catch \(error\) \{/m;

const newLoginWithGoogle = `async loginWithGoogle() {
        try {
            console.log('🔐 正在使用 Google 登入...');
            const provider = new firebase.auth.GoogleAuthProvider();
            provider.setCustomParameters({ prompt: 'select_account' });
            
            // 使用 signInWithRedirect 解決部分瀏覽器（如無痕模式）卡死問題
            await this.auth.signInWithRedirect(provider);
            
            // signInWithRedirect 會重新載入頁面，所以後續代碼移至 handleUserFirstLogin
            return { user: null }; // 佔位返回
        } catch (error) {`;

code = code.replace(loginWithGoogleRegex, newLoginWithGoogle);

// Add handleUserFirstLogin before loginWithGoogle
const handleUserFirstLoginCode = `
    // 處理用戶首次登入（創建 Firestore 文檔）
    async handleUserFirstLogin(user) {
        if (!user) return;
        
        try {
            const db = firebase.firestore();
            const userRef = db.collection('users').doc(user.uid);
            const userDoc = await userRef.get();
            
            if (!userDoc.exists) {
                console.log('📝 首次 Google 登入，創建 Firestore 用戶文檔...');
                const normalizedEmail = user.email.toLowerCase().trim();
                
                const userData = {
                    email: normalizedEmail,
                    displayName: user.displayName || '',
                    company: '',
                    credits: 20,
                    currentCredits: 20,
                    emailVerified: user.emailVerified,
                    planType: 'Free Plan',
                    photoURL: user.photoURL || '',
                    provider: 'google',
                    createdAt: firebase.firestore.FieldValue.serverTimestamp(),
                    updatedAt: firebase.firestore.FieldValue.serverTimestamp()
                };
                
                await userRef.set(userData);
                console.log('✅ Firestore 用戶文檔已創建（Google）');
                
                // 🎁 添加 Credits 歷史記錄
                try {
                    const historyRef = userRef.collection('creditsHistory').doc();
                    await historyRef.set({
                        type: 'bonus',
                        amount: 20,
                        reason: 'registration_bonus',
                        description: 'Google 註冊獎勵',
                        createdAt: firebase.firestore.FieldValue.serverTimestamp(),
                        balanceAfter: 20
                    });
                } catch (historyError) {
                    console.error('⚠️ 添加 Credits 歷史記錄失敗:', historyError);
                }
                
                // 🎯 Google Ads 轉化跟蹤
                try {
                    if (window.dataLayer) {
                        window.dataLayer.push({
                            'event': 'manual_event_PURCHASE',
                            'event_category': 'conversion',
                            'event_label': 'google_signup',
                            'value': 50,
                            'currency': 'HKD'
                        });
                        window.dataLayer.push({
                            'event': 'sign_up',
                            'method': 'google',
                            'value': 50,
                            'currency': 'HKD'
                        });
                    }
                } catch (e) {
                    console.error('轉化追蹤錯誤:', e);
                }
            } else {
                console.log('ℹ️ 用戶文檔已存在，更新最後登入時間...');
                await userRef.update({
                    updatedAt: firebase.firestore.FieldValue.serverTimestamp()
                });
            }
        } catch (error) {
            console.error('❌ 處理用戶首次登入失敗:', error);
        }
    }

    async loginWithGoogle`;

code = code.replace('async loginWithGoogle', handleUserFirstLoginCode);

fs.writeFileSync(path, code);
console.log('Patched simple-auth.js');
