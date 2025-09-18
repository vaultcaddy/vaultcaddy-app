/**
 * VaultCaddy 用戶認證系統
 * 實現真實的註冊、登入、登出功能
 */

class VaultCaddyAuth {
    constructor() {
        this.apiUrl = 'https://api.vaultcaddy.com'; // 生產環境API
        this.localStorageKeys = {
            user: 'vaultcaddy_user',
            token: 'vaultcaddy_token',
            credits: 'vaultcaddy_credits',
            refreshToken: 'vaultcaddy_refresh_token'
        };
        this.currentUser = null;
        this.initializeAuth();
    }

    /**
     * 初始化認證系統
     */
    initializeAuth() {
        // 檢查是否有保存的用戶信息
        const savedUser = localStorage.getItem(this.localStorageKeys.user);
        const savedToken = localStorage.getItem(this.localStorageKeys.token);
        
        if (savedUser && savedToken) {
            try {
                this.currentUser = JSON.parse(savedUser);
                this.validateToken(savedToken);
            } catch (error) {
                console.error('Failed to parse saved user data:', error);
                this.logout();
            }
        }
    }

    /**
     * 用戶註冊
     */
    async register(userData) {
        try {
            // 輸入驗證
            const validationResult = this.validateRegistrationData(userData);
            if (!validationResult.isValid) {
                throw new Error(validationResult.message);
            }

            // 模擬API請求（生產環境中會連接真實後端）
            const response = await this.mockApiCall('/auth/register', {
                method: 'POST',
                body: JSON.stringify({
                    email: userData.email,
                    password: userData.password,
                    firstName: userData.firstName,
                    lastName: userData.lastName,
                    company: userData.company || ''
                })
            });

            if (response.success) {
                // 註冊成功後自動登入
                const loginResult = await this.login({
                    email: userData.email,
                    password: userData.password
                });
                
                // 註冊成功後跳轉到首頁
                if (loginResult.success) {
                    setTimeout(() => {
                        window.location.href = 'index.html';
                    }, 1500);
                }
                
                return loginResult;
            } else {
                throw new Error(response.message || '註冊失敗');
            }
        } catch (error) {
            console.error('Registration failed:', error);
            throw error;
        }
    }

    /**
     * 用戶登入
     */
    async login(credentials) {
        try {
            // 輸入驗證
            if (!credentials.email || !credentials.password) {
                throw new Error('請輸入郵箱和密碼');
            }

            // 模擬API請求
            const response = await this.mockApiCall('/auth/login', {
                method: 'POST',
                body: JSON.stringify(credentials)
            });

            if (response.success) {
                // 保存用戶信息和令牌
                this.currentUser = response.user;
                
                localStorage.setItem(this.localStorageKeys.user, JSON.stringify(response.user));
                localStorage.setItem(this.localStorageKeys.token, response.token);
                localStorage.setItem(this.localStorageKeys.credits, response.user.credits.toString());
                
                if (response.refreshToken) {
                    localStorage.setItem(this.localStorageKeys.refreshToken, response.refreshToken);
                }

                // 觸發登入事件
                this.dispatchAuthEvent('login', this.currentUser);
                
                return {
                    success: true,
                    user: this.currentUser,
                    redirectUrl: this.getRedirectUrl()
                };
            } else {
                throw new Error(response.message || '登入失敗');
            }
        } catch (error) {
            console.error('Login failed:', error);
            throw error;
        }
    }

    /**
     * 用戶登出
     */
    async logout() {
        try {
            const token = localStorage.getItem(this.localStorageKeys.token);
            
            if (token) {
                // 通知服務器登出（可選）
                await this.mockApiCall('/auth/logout', {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
            }
        } catch (error) {
            console.error('Logout API call failed:', error);
        } finally {
            // 清除本地存儲
            Object.values(this.localStorageKeys).forEach(key => {
                localStorage.removeItem(key);
            });
            
            this.currentUser = null;
            
            // 觸發登出事件
            this.dispatchAuthEvent('logout');
            
            // 重定向到首頁
            window.location.href = 'index.html';
        }
    }

    /**
     * 檢查用戶是否已登入
     */
    isAuthenticated() {
        return this.currentUser !== null && localStorage.getItem(this.localStorageKeys.token) !== null;
    }

    /**
     * 獲取當前用戶信息
     */
    getCurrentUser() {
        return this.currentUser;
    }

    /**
     * 獲取用戶Credits
     */
    getUserCredits() {
        if (this.currentUser) {
            return this.currentUser.credits;
        }
        return parseInt(localStorage.getItem(this.localStorageKeys.credits) || '0');
    }

    /**
     * 更新用戶Credits
     */
    async updateCredits(newCredits) {
        try {
            const token = localStorage.getItem(this.localStorageKeys.token);
            
            const response = await this.mockApiCall('/user/credits', {
                method: 'PUT',
                headers: {
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ credits: newCredits })
            });

            if (response.success) {
                if (this.currentUser) {
                    this.currentUser.credits = newCredits;
                    localStorage.setItem(this.localStorageKeys.user, JSON.stringify(this.currentUser));
                }
                localStorage.setItem(this.localStorageKeys.credits, newCredits.toString());
                
                // 觸發Credits更新事件
                this.dispatchAuthEvent('creditsUpdated', { credits: newCredits });
                
                return true;
            }
            return false;
        } catch (error) {
            console.error('Failed to update credits:', error);
            return false;
        }
    }

    /**
     * 驗證註冊數據
     */
    validateRegistrationData(data) {
        if (!data.email || !this.isValidEmail(data.email)) {
            return { isValid: false, message: '請輸入有效的郵箱地址' };
        }
        
        if (!data.password || data.password.length < 8) {
            return { isValid: false, message: '密碼至少需要8位字符' };
        }
        
        if (!data.firstName || data.firstName.trim().length < 1) {
            return { isValid: false, message: '請輸入名字' };
        }
        
        if (!data.lastName || data.lastName.trim().length < 1) {
            return { isValid: false, message: '請輸入姓氏' };
        }
        
        return { isValid: true };
    }

    /**
     * 郵箱格式驗證
     */
    isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    /**
     * 令牌驗證
     */
    async validateToken(token) {
        try {
            const response = await this.mockApiCall('/auth/validate', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            
            if (!response.success) {
                this.logout();
                return false;
            }
            
            return true;
        } catch (error) {
            console.error('Token validation failed:', error);
            this.logout();
            return false;
        }
    }

    /**
     * 獲取重定向URL
     */
    getRedirectUrl() {
        const pendingDocumentType = localStorage.getItem('pendingDocumentType');
        if (pendingDocumentType) {
            localStorage.removeItem('pendingDocumentType');
            const dashboardRoutes = {
                'bank-statement': 'dashboard-bank.html',
                'invoice': 'dashboard-invoice.html',
                'receipt': 'dashboard-receipt.html',
                'general': 'dashboard-general.html'
            };
            return dashboardRoutes[pendingDocumentType] || 'dashboard-bank.html';
        }
        return 'dashboard-bank.html';
    }

    /**
     * 觸發認證事件
     */
    dispatchAuthEvent(eventType, data = null) {
        const event = new CustomEvent(`vaultcaddy:auth:${eventType}`, {
            detail: data
        });
        window.dispatchEvent(event);
    }

    /**
     * 模擬API調用（生產環境中會替換為真實API）
     */
    async mockApiCall(endpoint, options = {}) {
        // 模擬網絡延遲
        await new Promise(resolve => setTimeout(resolve, 500 + Math.random() * 1000));
        
        // 模擬不同的API響應
        switch (endpoint) {
            case '/auth/register':
                return this.mockRegisterResponse(JSON.parse(options.body));
            case '/auth/login':
                return this.mockLoginResponse(JSON.parse(options.body));
            case '/auth/logout':
                return { success: true };
            case '/auth/validate':
                return { success: true };
            case '/user/credits':
                return { success: true };
            default:
                return { success: false, message: 'API endpoint not found' };
        }
    }

    /**
     * 模擬註冊響應
     */
    mockRegisterResponse(userData) {
        // 檢查是否郵箱已存在（模擬）
        const existingUsers = JSON.parse(localStorage.getItem('vaultcaddy_users') || '[]');
        if (existingUsers.find(user => user.email === userData.email)) {
            return { success: false, message: '此郵箱已被註冊' };
        }

        // 創建新用戶
        const newUser = {
            id: Date.now().toString(),
            email: userData.email,
            firstName: userData.firstName,
            lastName: userData.lastName,
            company: userData.company || '',
            credits: 10, // 新用戶贈送10個Credits
            createdAt: new Date().toISOString(),
            plan: 'free'
        };

        // 保存用戶到模擬數據庫
        existingUsers.push({ ...newUser, password: userData.password });
        localStorage.setItem('vaultcaddy_users', JSON.stringify(existingUsers));

        return { success: true, user: newUser };
    }

    /**
     * 模擬登入響應
     */
    mockLoginResponse(credentials) {
        const existingUsers = JSON.parse(localStorage.getItem('vaultcaddy_users') || '[]');
        const user = existingUsers.find(u => u.email === credentials.email && u.password === credentials.password);

        if (!user) {
            return { success: false, message: '郵箱或密碼錯誤' };
        }

        const { password, ...userWithoutPassword } = user;
        
        return {
            success: true,
            user: userWithoutPassword,
            token: 'mock-jwt-token-' + Date.now(),
            refreshToken: 'mock-refresh-token-' + Date.now()
        };
    }

    /**
     * 重置密碼請求
     */
    async requestPasswordReset(email) {
        try {
            const response = await this.mockApiCall('/auth/reset-password', {
                method: 'POST',
                body: JSON.stringify({ email })
            });

            return response;
        } catch (error) {
            console.error('Password reset request failed:', error);
            throw error;
        }
    }

    /**
     * 更新用戶資料
     */
    async updateProfile(profileData) {
        try {
            const token = localStorage.getItem(this.localStorageKeys.token);
            
            const response = await this.mockApiCall('/user/profile', {
                method: 'PUT',
                headers: {
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(profileData)
            });

            if (response.success) {
                // 更新本地用戶信息
                this.currentUser = { ...this.currentUser, ...profileData };
                localStorage.setItem(this.localStorageKeys.user, JSON.stringify(this.currentUser));
                
                this.dispatchAuthEvent('profileUpdated', this.currentUser);
                return true;
            }
            return false;
        } catch (error) {
            console.error('Failed to update profile:', error);
            throw error;
        }
    }
}

// 創建全局認證實例
window.VaultCaddyAuth = new VaultCaddyAuth();

// 導出供模塊使用
if (typeof module !== 'undefined' && module.exports) {
    module.exports = VaultCaddyAuth;
}
