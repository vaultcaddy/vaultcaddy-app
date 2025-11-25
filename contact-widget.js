/**
 * 右下角對話按鈕組件
 * 功能：快速 email 聯繫 VaultCaddy 團隊
 * 作用：提供用戶便捷的聯繫方式，提升用戶體驗
 */

(function() {
    'use strict';
    
    // 創建對話按鈕
    function createContactWidget() {
        // 按鈕容器
        const widget = document.createElement('div');
        widget.id = 'contact-widget';
        widget.style.cssText = `
            position: fixed;
            bottom: 30px;
            right: 30px;
            z-index: 9999;
        `;
        
        // 對話按鈕
        const button = document.createElement('button');
        button.id = 'contact-button';
        button.innerHTML = '<i class="fas fa-comment-dots"></i>';
        button.style.cssText = `
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
            font-size: 24px;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s ease;
        `;
        
        // Hover 效果
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.1)';
            this.style.boxShadow = '0 6px 20px rgba(102, 126, 234, 0.6)';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
            this.style.boxShadow = '0 4px 12px rgba(102, 126, 234, 0.4)';
        });
        
        // 對話框
        const dialog = document.createElement('div');
        dialog.id = 'contact-dialog';
        dialog.style.cssText = `
            position: fixed;
            bottom: 100px;
            right: 30px;
            width: 360px;
            max-width: calc(100vw - 60px);
            background: white;
            border-radius: 16px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
            display: none;
            flex-direction: column;
            overflow: hidden;
            z-index: 10000;
        `;
        
        dialog.innerHTML = `
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; color: white;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h3 style="margin: 0; font-size: 1.25rem;">聯繫我們</h3>
                    <button id="close-dialog" style="background: none; border: none; color: white; font-size: 24px; cursor: pointer; padding: 0; width: 30px; height: 30px; display: flex; align-items: center; justify-content: center;">
                        ×
                    </button>
                </div>
                <p style="margin: 8px 0 0; font-size: 0.875rem; opacity: 0.9;">有任何問題或建議？我們很樂意聽取您的意見！</p>
            </div>
            
            <form id="contact-form" style="padding: 20px;">
                <div style="margin-bottom: 15px;">
                    <label style="display: block; font-size: 0.875rem; font-weight: 600; color: #374151; margin-bottom: 5px;">您的姓名</label>
                    <input type="text" id="contact-name" required style="width: 100%; padding: 10px; border: 2px solid #e5e7eb; border-radius: 8px; font-size: 0.9375rem; transition: border-color 0.2s;" placeholder="請輸入您的姓名">
                </div>
                
                <div style="margin-bottom: 15px;">
                    <label style="display: block; font-size: 0.875rem; font-weight: 600; color: #374151; margin-bottom: 5px;">您的 Email</label>
                    <input type="email" id="contact-email" required style="width: 100%; padding: 10px; border: 2px solid #e5e7eb; border-radius: 8px; font-size: 0.9375rem; transition: border-color 0.2s;" placeholder="your@email.com">
                </div>
                
                <div style="margin-bottom: 15px;">
                    <label style="display: block; font-size: 0.875rem; font-weight: 600; color: #374151; margin-bottom: 5px;">主題</label>
                    <input type="text" id="contact-subject" required style="width: 100%; padding: 10px; border: 2px solid #e5e7eb; border-radius: 8px; font-size: 0.9375rem; transition: border-color 0.2s;" placeholder="請簡述您的問題">
                </div>
                
                <div style="margin-bottom: 15px;">
                    <label style="display: block; font-size: 0.875rem; font-weight: 600; color: #374151; margin-bottom: 5px;">訊息內容</label>
                    <textarea id="contact-message" required rows="4" style="width: 100%; padding: 10px; border: 2px solid #e5e7eb; border-radius: 8px; font-size: 0.9375rem; resize: vertical; transition: border-color 0.2s; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;" placeholder="請詳細描述您的問題或建議..."></textarea>
                </div>
                
                <button type="submit" style="width: 100%; padding: 12px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 8px; font-size: 1rem; font-weight: 600; cursor: pointer; transition: transform 0.2s;">
                    發送訊息
                </button>
                
                <p style="margin-top: 12px; font-size: 0.75rem; color: #6b7280; text-align: center;">
                    或直接發送郵件至<br>
                    <a href="mailto:vaultcaddy@gmail.com" style="color: #667eea; text-decoration: none; font-weight: 600;">vaultcaddy@gmail.com</a>
                </p>
            </form>
            
            <div id="contact-success" style="display: none; padding: 20px; text-align: center;">
                <div style="width: 60px; height: 60px; background: #10b981; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 15px; color: white; font-size: 30px;">
                    ✓
                </div>
                <h4 style="margin: 0 0 10px; color: #1f2937; font-size: 1.125rem;">訊息已發送！</h4>
                <p style="margin: 0; color: #6b7280; font-size: 0.875rem;">我們會盡快回覆您的郵件。</p>
            </div>
        `;
        
        widget.appendChild(button);
        widget.appendChild(dialog);
        document.body.appendChild(widget);
        
        // 事件監聽器
        button.addEventListener('click', function() {
            const isVisible = dialog.style.display === 'flex';
            dialog.style.display = isVisible ? 'none' : 'flex';
            if (!isVisible) {
                dialog.style.animation = 'slideInUp 0.3s ease-out';
            }
        });
        
        document.getElementById('close-dialog').addEventListener('click', function() {
            dialog.style.display = 'none';
        });
        
        // 表單提交
        document.getElementById('contact-form').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const name = document.getElementById('contact-name').value;
            const email = document.getElementById('contact-email').value;
            const subject = document.getElementById('contact-subject').value;
            const message = document.getElementById('contact-message').value;
            
            // 構建 mailto 鏈接
            const mailtoLink = `mailto:vaultcaddy@gmail.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(
                `姓名: ${name}\nEmail: ${email}\n\n訊息:\n${message}`
            )}`;
            
            // 打開郵件客戶端
            window.location.href = mailtoLink;
            
            // 顯示成功訊息
            document.getElementById('contact-form').style.display = 'none';
            document.getElementById('contact-success').style.display = 'block';
            
            // 3 秒後關閉對話框並重置
            setTimeout(function() {
                dialog.style.display = 'none';
                document.getElementById('contact-form').style.display = 'block';
                document.getElementById('contact-success').style.display = 'none';
                document.getElementById('contact-form').reset();
            }, 3000);
        });
        
        // 點擊外部關閉對話框
        document.addEventListener('click', function(e) {
            if (!widget.contains(e.target)) {
                dialog.style.display = 'none';
            }
        });
        
        // Focus 效果
        const inputs = dialog.querySelectorAll('input, textarea');
        inputs.forEach(input => {
            input.addEventListener('focus', function() {
                this.style.borderColor = '#667eea';
            });
            
            input.addEventListener('blur', function() {
                this.style.borderColor = '#e5e7eb';
            });
        });
    }
    
    // 添加動畫 CSS
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        #contact-button:active {
            transform: scale(0.95) !important;
        }
        
        @media (max-width: 640px) {
            #contact-dialog {
                bottom: 100px;
                right: 15px;
                left: 15px;
                width: auto !important;
            }
            
            #contact-widget {
                bottom: 20px;
                right: 20px;
            }
        }
    `;
    document.head.appendChild(style);
    
    // 頁面載入完成後初始化
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', createContactWidget);
    } else {
        createContactWidget();
    }
})();

