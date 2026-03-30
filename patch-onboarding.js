const fs = require('fs');
const path = './simple-auth.js';
let code = fs.readFileSync(path, 'utf8');

const replacement = `                await userRef.set(userData);
                console.log('✅ Firestore 用戶文檔已創建（Google）');
                
                // 🚀 Onboarding: 自動創建當前月份資料夾
                try {
                    const now = new Date();
                    const currentMonthName = \`\${now.getFullYear()}-\${(now.getMonth() + 1).toString().padStart(2, '0')}\`;
                    const projectRef = userRef.collection('projects').doc();
                    await projectRef.set({
                        name: currentMonthName,
                        createdAt: firebase.firestore.FieldValue.serverTimestamp()
                    });
                    console.log('✅ 自動創建當前月份資料夾:', currentMonthName);
                } catch (err) {
                    console.error('⚠️ 自動創建月份資料夾失敗:', err);
                }
                
                // 🎁 添加 Credits 歷史記錄`;

code = code.replace(/                await userRef\.set\(userData\);\n                console\.log\('✅ Firestore 用戶文檔已創建（Google）'\);\n                \n                \/\/ 🎁 添加 Credits 歷史記錄/, replacement);

fs.writeFileSync(path, code);
console.log('Patched simple-auth.js for onboarding');
