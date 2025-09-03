/**
 * Google Cloud API 配置
 * 包含所有Google Cloud服務的配置信息
 */

// Google Cloud Vision API 配置
const GOOGLE_CLOUD_CONFIG = {
    // OAuth Client ID
    CLIENT_ID: '672279750239-u41ov9g2no1l2vh5j9h1679phggq0gko.apps.googleusercontent.com',
    
    // API 端點
    ENDPOINTS: {
        VISION_API: 'https://vision.googleapis.com/v1',
        DOCUMENT_AI: 'https://documentai.googleapis.com/v1',
        TRANSLATION: 'https://translation.googleapis.com/language/translate/v2'
    },
    
    // 授權範圍
    SCOPES: [
        'https://www.googleapis.com/auth/cloud-platform',
        'https://www.googleapis.com/auth/cloud-vision'
    ],
    
    // 重定向URI
    REDIRECT_URIS: [
        'https://vaultcaddy.com/auth/callback',
        'https://www.vaultcaddy.com/auth/callback',
        'https://vaultcaddy.github.io/vaultcaddy-app/auth/callback'
    ],
    
    // 授權的JavaScript來源
    AUTHORIZED_ORIGINS: [
        'https://vaultcaddy.com',
        'https://www.vaultcaddy.com',
        'https://vaultcaddy.github.io'
    ]
};

// 初始化Google API
function initializeGoogleAPI() {
    return new Promise((resolve, reject) => {
        // 檢查是否已載入gapi
        if (typeof gapi !== 'undefined') {
            gapi.load('auth2', () => {
                gapi.auth2.init({
                    client_id: GOOGLE_CLOUD_CONFIG.CLIENT_ID,
                    scope: GOOGLE_CLOUD_CONFIG.SCOPES.join(' ')
                }).then(() => {
                    console.log('✅ Google API 初始化成功');
                    resolve();
                }).catch(reject);
            });
        } else {
            // 動態載入Google API
            const script = document.createElement('script');
            script.src = 'https://apis.google.com/js/api.js';
            script.onload = () => {
                initializeGoogleAPI().then(resolve).catch(reject);
            };
            script.onerror = reject;
            document.head.appendChild(script);
        }
    });
}

// 處理OAuth認證
async function authenticateWithGoogle() {
    try {
        const authInstance = gapi.auth2.getAuthInstance();
        const user = await authInstance.signIn();
        const accessToken = user.getAuthResponse().access_token;
        
        // 存儲認證信息
        localStorage.setItem('google_access_token', accessToken);
        localStorage.setItem('google_user_info', JSON.stringify(user.getBasicProfile()));
        
        console.log('✅ Google 認證成功');
        return { user, accessToken };
    } catch (error) {
        console.error('❌ Google 認證失敗:', error);
        throw error;
    }
}

// 檢查認證狀態
function isGoogleAuthenticated() {
    const token = localStorage.getItem('google_access_token');
    return !!token;
}

// 取得存儲的access token
function getGoogleAccessToken() {
    return localStorage.getItem('google_access_token');
}

// 全局導出
window.GOOGLE_CLOUD_CONFIG = GOOGLE_CLOUD_CONFIG;
window.initializeGoogleAPI = initializeGoogleAPI;
window.authenticateWithGoogle = authenticateWithGoogle;
window.isGoogleAuthenticated = isGoogleAuthenticated;
window.getGoogleAccessToken = getGoogleAccessToken;

console.log('📋 Google Cloud 配置已載入');
console.log('🔑 Client ID:', GOOGLE_CLOUD_CONFIG.CLIENT_ID.substring(0, 20) + '...');
