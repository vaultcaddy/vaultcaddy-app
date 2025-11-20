/**
 * ============================================
 * 👤 VaultCaddy 用戶資料管理器
 * ============================================
 * 作用：統一管理用戶頭像和個人資料
 * 
 * 功能：
 * 1. 從 Firestore 讀取/更新 displayName
 * 2. 自動計算 userInitial（首字母）
 * 3. 統一更新所有頁面的用戶頭像
 * 4. 監聽用戶登入/登出事件
 * 
 * 使用方式：
 * - 自動初始化：頁面載入時自動執行
 * - 手動更新：window.userProfileManager.updateProfile({ displayName: 'Yeung Cavlin' })
 * - 獲取資料：window.userProfileManager.getUserProfile()
 * ============================================
 */

class UserProfileManager {
    constructor() {
        this.currentProfile = {
            displayName: '',
            userInitial: 'U',
            email: '',
            photoURL: null
        };
        
        this.initialized = false;
        console.log('👤 UserProfileManager 構造函數執行');
    }
    
    /**
     * 初始化用戶資料管理器
     */
    async init() {
        try {
            console.log('👤 開始初始化 UserProfileManager...');
            
            // 等待 SimpleAuth 初始化
            await this.waitForSimpleAuth();
            
            // 加載用戶資料
            await this.loadUserProfile();
            
            // 監聽用戶狀態變化
            this.setupListeners();
            
            this.initialized = true;
            console.log('✅ UserProfileManager 已初始化');
            console.log('   當前資料:', this.currentProfile);
            
        } catch (error) {
            console.error('❌ UserProfileManager 初始化失敗:', error);
        }
    }
    
    /**
     * 等待 SimpleAuth 就緒
     */
    waitForSimpleAuth() {
        return new Promise((resolve) => {
            if (window.simpleAuth && window.simpleAuth.initialized) {
                resolve();
            } else {
                const checkInterval = setInterval(() => {
                    if (window.simpleAuth && window.simpleAuth.initialized) {
                        clearInterval(checkInterval);
                        resolve();
                    }
                }, 100);
                
                setTimeout(() => {
                    clearInterval(checkInterval);
                    console.warn('⚠️ SimpleAuth 初始化超時');
                    resolve();
                }, 10000);
            }
        });
    }
    
    /**
     * 從 Firestore 加載用戶資料
     */
    async loadUserProfile() {
        try {
            const user = window.simpleAuth?.currentUser;
            
            if (!user) {
                console.log('📭 用戶未登入，使用默認資料');
                this.currentProfile = {
                    displayName: '',
                    userInitial: 'U',
                    email: '',
                    photoURL: null
                };
                return;
            }
            
            console.log('📥 加載用戶資料:', user.email);
            
            // 從 Firestore 獲取用戶資料
            const userDoc = await firebase.firestore()
                .collection('users')
                .doc(user.uid)
                .get();
            
            let displayName = '';
            let photoURL = null;
            
            if (userDoc.exists) {
                const userData = userDoc.data();
                displayName = userData.displayName || '';
                photoURL = userData.photoURL || null;
                console.log('   Firestore 資料:', { displayName, photoURL });
            }
            
            // 如果 Firestore 沒有，使用 Firebase Auth 的資料
            if (!displayName) {
                displayName = user.displayName || user.email?.split('@')[0] || '';
                console.log('   使用 Firebase Auth 資料:', displayName);
            }
            
            // 計算首字母
            const userInitial = this.calculateInitial(displayName || user.email);
            
            this.currentProfile = {
                displayName: displayName,
                userInitial: userInitial,
                email: user.email || '',
                photoURL: photoURL
            };
            
            console.log('✅ 用戶資料已加載:', this.currentProfile);
            
            // 觸發自定義事件，通知其他組件
            window.dispatchEvent(new CustomEvent('user-profile-loaded', { 
                detail: this.currentProfile 
            }));
            
        } catch (error) {
            console.error('❌ 加載用戶資料失敗:', error);
        }
    }
    
    /**
     * 計算用戶名稱首字母
     */
    calculateInitial(name) {
        if (!name) return 'U';
        
        // 移除空格和特殊字符，取第一個有效字符
        const cleanName = name.trim();
        if (cleanName.length === 0) return 'U';
        
        // 取第一個字符並轉大寫
        const initial = cleanName.charAt(0).toUpperCase();
        
        console.log(`   計算首字母: "${name}" -> "${initial}"`);
        return initial;
    }
    
    /**
     * 更新用戶資料（保存到 Firestore）
     */
    async updateProfile(updates) {
        try {
            const user = window.simpleAuth?.currentUser;
            
            if (!user) {
                console.error('❌ 用戶未登入，無法更新資料');
                return false;
            }
            
            console.log('📝 更新用戶資料:', updates);
            
            // 更新 Firestore
            await firebase.firestore()
                .collection('users')
                .doc(user.uid)
                .set(updates, { merge: true });
            
            // 更新本地資料
            if (updates.displayName) {
                this.currentProfile.displayName = updates.displayName;
                this.currentProfile.userInitial = this.calculateInitial(updates.displayName);
            }
            
            if (updates.photoURL !== undefined) {
                this.currentProfile.photoURL = updates.photoURL;
            }
            
            console.log('✅ 用戶資料已更新:', this.currentProfile);
            
            // 觸發自定義事件
            window.dispatchEvent(new CustomEvent('user-profile-updated', { 
                detail: this.currentProfile 
            }));
            
            // 刷新所有頭像
            this.refreshAllAvatars();
            
            return true;
            
        } catch (error) {
            console.error('❌ 更新用戶資料失敗:', error);
            return false;
        }
    }
    
    /**
     * 獲取當前用戶資料
     */
    getUserProfile() {
        return { ...this.currentProfile };
    }
    
    /**
     * 獲取用戶首字母
     */
    getUserInitial() {
        return this.currentProfile.userInitial;
    }
    
    /**
     * 刷新所有頁面的用戶頭像
     */
    refreshAllAvatars() {
        console.log('🔄 刷新所有用戶頭像...');
        
        const { userInitial, photoURL } = this.currentProfile;
        
        // 1. 更新導航欄頭像
        const navbarAvatar = document.querySelector('.navbar-user div, .navbar-user img');
        if (navbarAvatar) {
            if (photoURL) {
                // 使用圖片
                navbarAvatar.innerHTML = `<img src="${photoURL}" alt="User" style="width: 32px; height: 32px; border-radius: 50%; object-fit: cover;">`;
            } else {
                // 使用首字母
                navbarAvatar.textContent = userInitial;
            }
            console.log('   ✅ 導航欄頭像已更新');
        }
        
        // 2. 更新個人資料頁面頭像
        const profileAvatar = document.getElementById('user-avatar');
        if (profileAvatar) {
            profileAvatar.textContent = userInitial;
            console.log('   ✅ 個人資料頭像已更新');
        }
        
        // 3. 更新所有其他頭像元素
        const allAvatars = document.querySelectorAll('[data-user-avatar]');
        allAvatars.forEach(avatar => {
            avatar.textContent = userInitial;
        });
        
        if (allAvatars.length > 0) {
            console.log(`   ✅ 已更新 ${allAvatars.length} 個額外頭像`);
        }
    }
    
    /**
     * 設置事件監聽器
     */
    setupListeners() {
        // 監聽用戶登入
        window.addEventListener('user-logged-in', async () => {
            console.log('🔔 用戶登入事件，重新加載資料');
            await this.loadUserProfile();
            this.refreshAllAvatars();
        });
        
        // 監聽用戶登出
        window.addEventListener('user-logged-out', () => {
            console.log('🔔 用戶登出事件，清空資料');
            this.currentProfile = {
                displayName: '',
                userInitial: 'U',
                email: '',
                photoURL: null
            };
            this.refreshAllAvatars();
        });
        
        // 監聽 Firebase 就緒
        window.addEventListener('firebase-ready', async () => {
            console.log('🔔 Firebase 就緒事件');
            if (!this.initialized) {
                await this.init();
            }
        });
    }
}

// 創建全局實例
window.userProfileManager = new UserProfileManager();

// 自動初始化
(async function() {
    try {
        // 等待 DOM 就緒
        if (document.readyState === 'loading') {
            await new Promise(resolve => {
                document.addEventListener('DOMContentLoaded', resolve);
            });
        }
        
        // 初始化
        await window.userProfileManager.init();
        
    } catch (error) {
        console.error('❌ UserProfileManager 自動初始化失敗:', error);
    }
})();

console.log('✅ user-profile-manager.js 已載入');

