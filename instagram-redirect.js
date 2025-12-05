// Instagram/Facebook WebView 自动检测和引导脚本
// 当检测到社交媒体内置浏览器时，显示友好提示引导用户在浏览器中打开

(function() {
    'use strict';
    
    // 检测 Instagram/Facebook/其他社交媒体 WebView
    const userAgent = navigator.userAgent || navigator.vendor || window.opera;
    const isInstagram = userAgent.indexOf('Instagram') > -1;
    const isFacebook = userAgent.indexOf('FBAN') > -1 || userAgent.indexOf('FBAV') > -1;
    const isWeChat = userAgent.indexOf('MicroMessenger') > -1;
    const isLine = userAgent.indexOf('Line') > -1;
    const isSocialWebView = isInstagram || isFacebook || isWeChat || isLine;
    
    console.log('🔍 浏览器检测:', {
        userAgent: userAgent,
        isInstagram: isInstagram,
        isFacebook: isFacebook,
        isWeChat: isWeChat,
        isSocialWebView: isSocialWebView
    });
    
    if (isSocialWebView) {
        console.log('📱 检测到社交媒体浏览器，显示引导提示');
        
        // 创建底部浮动提示条（不遮挡页面内容）
        const banner = document.createElement('div');
        banner.id = 'social-browser-banner';
        banner.style.cssText = `
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            z-index: 999999;
            padding: 15px 20px;
            box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.2);
            animation: slideInUp 0.5s ease-out;
            transform: translateY(0);
        `;
        
        // 底部横幅内容
        let platformName = 'App';
        if (isInstagram) platformName = 'Instagram';
        else if (isFacebook) platformName = 'Facebook';
        else if (isWeChat) platformName = '微信';
        else if (isLine) platformName = 'Line';
        
        banner.innerHTML = `
            <style>
                @keyframes slideInUp {
                    from {
                        transform: translateY(100%);
                    }
                    to {
                        transform: translateY(0);
                    }
                }
                
                @keyframes bounce {
                    0%, 100% { transform: translateY(0); }
                    50% { transform: translateY(-5px); }
                }
                
                .banner-btn {
                    transition: all 0.2s ease;
                }
                
                .banner-btn:active {
                    transform: scale(0.95);
                }
            </style>
            
            <div style="display: flex; align-items: center; justify-content: space-between; gap: 15px;">
                <div style="flex: 1;">
                    <div style="font-weight: 700; font-size: 1rem; margin-bottom: 5px; display: flex; align-items: center; gap: 8px;">
                        <span style="animation: bounce 2s infinite;">🌐</span>
                        <span>在瀏覽器中打開以獲得最佳體驗</span>
                    </div>
                    <div style="font-size: 0.875rem; opacity: 0.95;">
                        點擊右上角 <strong>⋯</strong> → 選擇「在瀏覽器中打開」
                    </div>
                </div>
                
                <div style="display: flex; gap: 10px; flex-shrink: 0;">
                    <button onclick="tryOpenInBrowser()" class="banner-btn" style="
                        background: white;
                        color: #667eea;
                        border: none;
                        padding: 12px 20px;
                        border-radius: 8px;
                        font-weight: 600;
                        font-size: 0.9rem;
                        cursor: pointer;
                        white-space: nowrap;
                        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
                    ">
                        🚀 立即打開
                    </button>
                    
                    <button onclick="closeBanner()" style="
                        background: rgba(255, 255, 255, 0.2);
                        color: white;
                        border: 1px solid rgba(255, 255, 255, 0.3);
                        padding: 10px;
                        border-radius: 8px;
                        font-size: 1.2rem;
                        cursor: pointer;
                        width: 40px;
                        height: 40px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                    ">
                        ✕
                    </button>
                </div>
            </div>
        `;
        
        // 添加到页面
        if (document.body) {
            document.body.appendChild(banner);
            // 调整body padding，避免内容被横幅遮挡
            document.body.style.paddingBottom = '80px';
        } else {
            document.addEventListener('DOMContentLoaded', function() {
                document.body.appendChild(banner);
                document.body.style.paddingBottom = '80px';
            });
        }
        
        // 尝试在浏览器中打开（多种方式）
        window.tryOpenInBrowser = function() {
            const url = window.location.href;
            
            // 方法1: 尝试打开默认浏览器
            try {
                // 对于iOS Safari
                if (/iPhone|iPad|iPod/.test(navigator.userAgent)) {
                    // 尝试Safari scheme
                    window.location.href = 'x-safari-' + url;
                    
                    // 延迟提示
                    setTimeout(function() {
                        // 如果没有跳转成功，复制链接
                        if (navigator.clipboard && navigator.clipboard.writeText) {
                            navigator.clipboard.writeText(url).then(function() {
                                alert('✅ 網址已複製！\n\n請在 Safari 中粘貼打開。\n\n提示：點擊右上角 ⋯ → 在 Safari 中打開');
                            }).catch(function() {
                                showManualCopyAlert(url);
                            });
                        } else {
                            showManualCopyAlert(url);
                        }
                    }, 1000);
                } else {
                    // Android: 尝试打开Chrome
                    window.location.href = 'googlechrome://navigate?url=' + encodeURIComponent(url);
                    
                    setTimeout(function() {
                        // 备用：复制链接
                        if (navigator.clipboard && navigator.clipboard.writeText) {
                            navigator.clipboard.writeText(url).then(function() {
                                alert('✅ 網址已複製！\n\n請在 Chrome 或其他瀏覽器中粘貼打開。');
                            }).catch(function() {
                                showManualCopyAlert(url);
                            });
                        } else {
                            showManualCopyAlert(url);
                        }
                    }, 1000);
                }
            } catch (err) {
                console.error('打开浏览器失败:', err);
                showManualCopyAlert(url);
            }
        };
        
        // 显示手动复制提示
        function showManualCopyAlert(url) {
            alert('請按照以下步驟操作：\n\n1. 點擊右上角 ⋯ (三個點)\n2. 選擇「在 Safari/Chrome 中打開」\n\n或複製此網址：\n' + url);
        }
        
        // 关闭横幅
        window.closeBanner = function() {
            const banner = document.getElementById('social-browser-banner');
            if (banner) {
                banner.style.transform = 'translateY(100%)';
                setTimeout(function() {
                    banner.remove();
                    document.body.style.paddingBottom = '0';
                }, 300);
            }
        };
    }
})();

