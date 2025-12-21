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
            
            // 🔧 先強制刷新用戶狀態（確保獲取最新的 emailVerified）
            await user.reload();
            
            // ✅ 直接使用 Firebase Auth 的 emailVerified 屬性（最准確）
            const isVerified = user.emailVerified;
            
            console.log(`📧 Email 驗證狀態: ${isVerified ? '已驗證 ✅' : '未驗證 ❌'}`);
            console.log(`   用戶: ${user.email}`);
            console.log(`   emailVerified: ${user.emailVerified}`);
            
            return isVerified;
            
        } catch (error) {
            console.error('❌ 檢查驗證狀態失敗:', error);
            // 發生錯誤時，假設未驗證（安全起見）
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
                <span style="font-size: 1.5rem;">🎁</span>
                <span style="font-weight: 600;">Verify your email now and get 20 Credits free trial!</span>
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
                    Verify Now
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
        
        // 🔧 統一調整頁面佈局（支持所有頁面）
        const adjustPageLayout = () => {
            const isMobile = window.innerWidth <= 768;
            const bannerHeight = 60; // 橫幅高度
            const navbarHeight = 60; // 導航欄高度
            
            console.log(`📱 調整頁面佈局 - ${isMobile ? '手機版' : '桌面版'}`);
            
            // ✅ 手機版：調整所有可能的容器
            if (isMobile) {
                // 1. 調整 dashboard-container
                const dashboardContainer = document.querySelector('.dashboard-container');
                if (dashboardContainer) {
                    dashboardContainer.style.paddingTop = `${navbarHeight + bannerHeight + 20}px`; // 額外20px間距
                    console.log('✅ dashboard-container paddingTop:', dashboardContainer.style.paddingTop);
                }
                
                // 2. 調整 account-container（billing.html）
                const accountContainer = document.querySelector('.account-container');
                if (accountContainer) {
                    accountContainer.style.paddingTop = `${navbarHeight + bannerHeight + 20}px`;
                    console.log('✅ account-container 已調整');
                }
                
                // 3. 調整 main-content
                const mainContent = document.querySelector('.main-content');
                if (mainContent) {
                    const currentPadding = parseInt(mainContent.style.paddingTop || '0');
                    if (currentPadding < bannerHeight) {
                        mainContent.style.paddingTop = `${bannerHeight + 20}px`;
                        console.log('✅ main-content 已調整');
                    }
                }
                
                // 4. 調整 settings-container（account.html）
                const settingsContainer = document.querySelector('.settings-container');
                if (settingsContainer) {
                    settingsContainer.style.marginTop = `${bannerHeight}px`;
                    console.log('✅ settings-container 已調整');
                }
                
                // 5. 調整 pricing-container（billing.html）
                const pricingContainer = document.querySelector('.pricing-container');
                if (pricingContainer) {
                    pricingContainer.style.marginTop = `${bannerHeight}px`;
                    console.log('✅ pricing-container 已調整');
                }
                
                // 6. 如果都沒有，調整 body
                if (!dashboardContainer && !accountContainer && !mainContent) {
                    document.body.style.paddingTop = `${navbarHeight + bannerHeight + 20}px`;
                    console.log('✅ body paddingTop 已調整');
                }
            } else {
                // 桌面版：正常調整
                const dashboardContainer = document.querySelector('.dashboard-container');
                if (dashboardContainer) {
                    dashboardContainer.style.paddingTop = `${navbarHeight + bannerHeight}px`;
                }
                
                const accountContainer = document.querySelector('.account-container');
                if (accountContainer) {
                    accountContainer.style.paddingTop = `${navbarHeight + bannerHeight}px`;
                }
            }
        };
        
        // 延遲調整，確保 DOM 完全加載
        setTimeout(adjustPageLayout, 100);
        setTimeout(adjustPageLayout, 500); // 再次調整，以防首次失敗
        
        // ✅ 調整左側欄位置（當驗證 banner 出現時，sidebar 需要向下移動）
        const adjustSidebar = () => {
            const sidebar = document.querySelector('.sidebar') || document.querySelector('aside.sidebar');
            if (sidebar) {
                // 驗證 banner 高度約 60px，sidebar 原本 top: 60px（navbar 高度）
                // 需要調整為 top: 120px（navbar + banner）
                sidebar.style.top = '120px';
                sidebar.style.height = 'calc(100vh - 120px)';
                console.log('✅ 左側欄位置已調整：top: 120px');
            } else {
                console.log('⚠️ 找不到左側欄元素');
                // 延遲重試
                setTimeout(adjustSidebar, 100);
            }
        };
        
        // 檢查並調整左側欄（延遲執行確保 DOM 已載入）
        setTimeout(adjustSidebar, 100);
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
    blockFeature(message = 'Please verify your email to use this feature') {
        alert(message);
        this.goToVerification();
    },
    
    /**
     * 主檢查函數（在頁面載入時調用）
     * @param {Object} options 配置選項
     * @param {boolean} options.showNotice 是否顯示提示橫幅（默認 true）
     * @param {boolean} options.blockPage 是否阻止頁面使用（默認 false，已廢棄）
     * @returns {Promise<boolean>} 是否已驗證
     */
    async init(options = {}) {
        const {
            showNotice = true,
            blockPage = false  // 已廢棄，不再阻擋功能
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
                console.log('🎁 Email 未驗證，顯示獎勵提示');
                
                if (showNotice) {
                    this.showUnverifiedNotice();
                }
                
                // 不再阻擋功能，只要有足夠 Credits 即可使用
                
                return false;
            } else {
                console.log('✅ Email 已驗證');
                return true;
            }
            
        } catch (error) {
            console.error('❌ Email 驗證檢查失敗:', error);
            // 發生錯誤時也不阻擋功能
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

