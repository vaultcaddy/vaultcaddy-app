/**
 * Email 驗證檢查模組
 * 
 * 功能：
 * 1. 檢查用戶 email 是否已驗證
 * 2. 未驗證用戶顯示提示並阻止功能使用
 * 3. 提供跳轉到驗證頁面的功能
 * 
 * 使用方法：
 * 在需要驗證的頁面引入此腳本，然後調用：
 * await checkEmailVerification();
 */

window.emailVerificationChecker = {
    /**
     * 檢查當前用戶的 email 是否已驗證
     * @returns {Promise<boolean>} 是否已驗證
     */
    async checkVerification() {
        try {
            const user = firebase.auth().currentUser;
            
            if (!user) {
                console.log('❌ 用戶未登入');
                return false;
            }
            
            // 檢查 Firestore 中的驗證狀態
            const functions = firebase.functions();
            const checkFunc = functions.httpsCallable('checkEmailVerified');
            const result = await checkFunc({ email: user.email });
            
            return result.data.verified || false;
            
        } catch (error) {
            console.error('❌ 檢查驗證狀態失敗:', error);
            return false;
        }
    },
    
    /**
     * 顯示未驗證提示
     */
    showUnverifiedNotice() {
        const user = firebase.auth().currentUser;
        if (!user) return;
        
        // 創建提示橫幅（放在頂部欄下方）
        const notice = document.createElement('div');
        notice.id = 'email-verification-notice';
        notice.style.cssText = `
            position: fixed;
            top: 60px;
            left: 0;
            right: 0;
            background: linear-gradient(135deg, #f59e0b 0%, #ef4444 100%);
            color: white;
            padding: 1rem;
            text-align: center;
            z-index: 999;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            animation: slideDown 0.3s ease-out;
        `;
        
        notice.innerHTML = `
            <div style="max-width: 1200px; margin: 0 auto; display: flex; align-items: center; justify-content: center; gap: 1rem; flex-wrap: wrap;">
                <span style="font-size: 1.5rem;">⚠️</span>
                <span style="font-weight: 600;">您的電子郵件尚未驗證</span>
                <span style="opacity: 0.9;">請先驗證您的 email 才能使用完整功能</span>
                <button onclick="emailVerificationChecker.goToVerification()" style="
                    background: white;
                    color: #ef4444;
                    border: none;
                    padding: 0.5rem 1.5rem;
                    border-radius: 6px;
                    font-weight: 600;
                    cursor: pointer;
                    transition: transform 0.2s;
                ">
                    立即驗證
                </button>
            </div>
        `;
        
        // 添加動畫
        const style = document.createElement('style');
        style.textContent = `
            @keyframes slideDown {
                from {
                    transform: translateY(-100%);
                    opacity: 0;
                }
                to {
                    transform: translateY(0);
                    opacity: 1;
                }
            }
        `;
        document.head.appendChild(style);
        
        // 插入到頁面頂部
        document.body.insertBefore(notice, document.body.firstChild);
        
        // 調整頁面內容位置（避免被橫幅遮擋，考慮頂部欄高度）
        const mainContent = document.querySelector('main') || document.querySelector('.container') || document.body;
        if (mainContent && mainContent !== document.body) {
            mainContent.style.marginTop = '60px';
        } else {
            document.body.style.paddingTop = '120px'; // 60px (navbar) + 60px (notice)
        }
    },
    
    /**
     * 跳轉到驗證頁面
     */
    goToVerification() {
        const user = firebase.auth().currentUser;
        if (user) {
            window.location.href = `verify-email.html?email=${encodeURIComponent(user.email)}`;
        }
    },
    
    /**
     * 阻止功能使用並顯示提示
     */
    blockFeature(message = '請先驗證您的 email 才能使用此功能') {
        alert(message);
        this.goToVerification();
    },
    
    /**
     * 主檢查函數（在頁面載入時調用）
     * @param {Object} options 配置選項
     * @param {boolean} options.showNotice 是否顯示提示橫幅（默認 true）
     * @param {boolean} options.blockPage 是否阻止頁面使用（默認 false）
     * @returns {Promise<boolean>} 是否已驗證
     */
    async init(options = {}) {
        const {
            showNotice = true,
            blockPage = false
        } = options;
        
        try {
            // 等待 Firebase Auth 初始化
            await new Promise((resolve) => {
                firebase.auth().onAuthStateChanged((user) => {
                    resolve(user);
                });
            });
            
            const user = firebase.auth().currentUser;
            
            // 未登入用戶不需要檢查
            if (!user) {
                return true;
            }
            
            // 檢查驗證狀態
            const isVerified = await this.checkVerification();
            
            if (!isVerified) {
                console.log('⚠️ Email 未驗證');
                
                if (showNotice) {
                    this.showUnverifiedNotice();
                }
                
                if (blockPage) {
                    // 阻止頁面功能
                    this.blockAllFeatures();
                }
                
                return false;
            } else {
                console.log('✅ Email 已驗證');
                return true;
            }
            
        } catch (error) {
            console.error('❌ Email 驗證檢查失敗:', error);
            return false;
        }
    },
    
    /**
     * 阻止所有頁面功能
     */
    blockAllFeatures() {
        // 禁用所有按鈕
        const buttons = document.querySelectorAll('button:not(#email-verification-notice button)');
        buttons.forEach(btn => {
            btn.disabled = true;
            btn.style.opacity = '0.5';
            btn.style.cursor = 'not-allowed';
        });
        
        // 禁用所有輸入
        const inputs = document.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            input.disabled = true;
            input.style.opacity = '0.5';
        });
        
        // 添加點擊攔截
        document.addEventListener('click', (e) => {
            if (!e.target.closest('#email-verification-notice')) {
                e.preventDefault();
                e.stopPropagation();
                this.blockFeature();
            }
        }, true);
    }
};

// 導出全局函數以便在頁面中使用
window.checkEmailVerification = async (options) => {
    return await window.emailVerificationChecker.init(options);
};

console.log('✅ Email 驗證檢查模組已載入');

