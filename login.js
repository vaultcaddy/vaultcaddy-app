// 登入頁面JavaScript功能

document.addEventListener('DOMContentLoaded', function() {
    
    // 語言翻譯擴展（登入頁面專用）
    const loginTranslations = {
        'en': {
            'login_title': 'Sign in to your account',
            'google_signin': 'Continue with Google',
            'or': 'OR',
            'email_label': 'Email address',
            'email_placeholder': 'Enter your email',
            'password_label': 'Password',
            'password_placeholder': 'Enter your password',
            'remember_me': 'Remember me',
            'forgot_password': 'Forgot password?',
            'signin_btn': 'Sign in',
            'not_member': 'Not a member?',
            'signup_link': 'Sign up',
            'welcome_back': 'Welcome back!',
            'login_welcome_text': 'Access your AI Bank Parser dashboard to manage your document conversions and view your conversion history.',
            'feature_highlight_1': 'Convert PDF bank statements instantly',
            'feature_highlight_2': 'Download in multiple formats',
            'feature_highlight_3': 'Secure and confidential processing',
            'feature_highlight_4': 'Access conversion history',
            'forgot_password_title': 'Reset your password',
            'forgot_password_text': 'Enter your email address and we\'ll send you a link to reset your password.',
            'send_reset_link': 'Send reset link',
            'signup_title': 'Create your account',
            'name_label': 'Full name',
            'name_placeholder': 'Enter your full name',
            'create_password_placeholder': 'Create a password',
            'password_requirements': 'Password must be at least 8 characters long',
            'terms_agreement': 'I agree to the <a href="#terms">Terms of Service</a> and <a href="#privacy">Privacy Policy</a>',
            'create_account_btn': 'Create account'
        },
        'zh-TW': {
            'login_title': '登入您的帳戶',
            'google_signin': '使用Google繼續',
            'or': '或',
            'email_label': '電子郵件地址',
            'email_placeholder': '輸入您的電子郵件',
            'password_label': '密碼',
            'password_placeholder': '輸入您的密碼',
            'remember_me': '記住我',
            'forgot_password': '忘記密碼？',
            'signin_btn': '登入',
            'not_member': '還不是會員？',
            'signup_link': '註冊',
            'welcome_back': '歡迎回來！',
            'login_welcome_text': '存取您的AI Bank Parser儀表板，管理您的文件轉換並查看轉換歷史記錄。',
            'feature_highlight_1': '即時轉換PDF銀行對帳單',
            'feature_highlight_2': '下載多種格式',
            'feature_highlight_3': '安全且保密的處理',
            'feature_highlight_4': '存取轉換歷史記錄',
            'forgot_password_title': '重設您的密碼',
            'forgot_password_text': '輸入您的電子郵件地址，我們將向您發送重設密碼的鏈接。',
            'send_reset_link': '發送重設鏈接',
            'signup_title': '創建您的帳戶',
            'name_label': '全名',
            'name_placeholder': '輸入您的全名',
            'create_password_placeholder': '創建密碼',
            'password_requirements': '密碼必須至少8個字符',
            'terms_agreement': '我同意<a href="#terms">服務條款</a>和<a href="#privacy">隱私政策</a>',
            'create_account_btn': '創建帳戶'
        },
        'zh-CN': {
            'login_title': '登录您的账户',
            'google_signin': '使用Google继续',
            'or': '或',
            'email_label': '电子邮件地址',
            'email_placeholder': '输入您的电子邮件',
            'password_label': '密码',
            'password_placeholder': '输入您的密码',
            'remember_me': '记住我',
            'forgot_password': '忘记密码？',
            'signin_btn': '登录',
            'not_member': '还不是会员？',
            'signup_link': '注册',
            'welcome_back': '欢迎回来！',
            'login_welcome_text': '访问您的AI Bank Parser仪表板，管理您的文档转换并查看转换历史记录。',
            'feature_highlight_1': '即时转换PDF银行对账单',
            'feature_highlight_2': '下载多种格式',
            'feature_highlight_3': '安全且保密的处理',
            'feature_highlight_4': '访问转换历史记录',
            'forgot_password_title': '重置您的密码',
            'forgot_password_text': '输入您的电子邮件地址，我们将向您发送重置密码的链接。',
            'send_reset_link': '发送重置链接',
            'signup_title': '创建您的账户',
            'name_label': '全名',
            'name_placeholder': '输入您的全名',
            'create_password_placeholder': '创建密码',
            'password_requirements': '密码必须至少8个字符',
            'terms_agreement': '我同意<a href="#terms">服务条款</a>和<a href="#privacy">隐私政策</a>',
            'create_account_btn': '创建账户'
        }
    };

    // 擴展翻譯
    Object.keys(loginTranslations).forEach(lang => {
        if (translations[lang]) {
            Object.assign(translations[lang], loginTranslations[lang]);
        }
    });

    // 表單元素
    const loginForm = document.getElementById('login-form');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const passwordToggle = document.getElementById('password-toggle');
    const signinBtn = document.getElementById('signin-btn');
    const googleSigninBtn = document.getElementById('google-signin');

    // 模態框元素
    const forgotPasswordModal = document.getElementById('forgot-password-modal');
    const signupModal = document.getElementById('signup-modal');
    const forgotPasswordLink = document.querySelector('.forgot-password');
    const signupLink = document.querySelector('.signup-link a');

    // 關閉按鈕
    const closeForgotModal = document.getElementById('close-forgot-modal');
    const closeSignupModal = document.getElementById('close-signup-modal');

    // 密碼顯示/隱藏切換
    if (passwordToggle) {
        passwordToggle.addEventListener('click', function() {
            const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInput.setAttribute('type', type);
            
            const icon = this.querySelector('i');
            if (type === 'text') {
                icon.className = 'fas fa-eye-slash';
            } else {
                icon.className = 'fas fa-eye';
            }
        });
    }

    // 註冊表單密碼切換
    const signupPasswordToggle = document.getElementById('signup-password-toggle');
    const signupPasswordInput = document.getElementById('signup-password');
    
    if (signupPasswordToggle) {
        signupPasswordToggle.addEventListener('click', function() {
            const type = signupPasswordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            signupPasswordInput.setAttribute('type', type);
            
            const icon = this.querySelector('i');
            if (type === 'text') {
                icon.className = 'fas fa-eye-slash';
            } else {
                icon.className = 'fas fa-eye';
            }
        });
    }

    // 表單驗證
    function validateEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    function validatePassword(password) {
        return password.length >= 8;
    }

    function showError(input, message) {
        input.classList.add('error');
        const errorElement = input.parentNode.querySelector('.error-message');
        if (errorElement) {
            errorElement.textContent = message;
        }
    }

    function clearError(input) {
        input.classList.remove('error');
        const errorElement = input.parentNode.querySelector('.error-message');
        if (errorElement) {
            errorElement.textContent = '';
        }
    }

    function showSuccess(input) {
        input.classList.add('valid');
        input.classList.remove('error');
    }

    // 即時驗證
    if (emailInput) {
        emailInput.addEventListener('blur', function() {
            if (this.value && !validateEmail(this.value)) {
                showError(this, '請輸入有效的電子郵件地址');
            } else if (this.value && validateEmail(this.value)) {
                clearError(this);
                showSuccess(this);
            }
        });

        emailInput.addEventListener('input', function() {
            if (this.classList.contains('error') && validateEmail(this.value)) {
                clearError(this);
                showSuccess(this);
            }
        });
    }

    if (passwordInput) {
        passwordInput.addEventListener('blur', function() {
            if (this.value && !validatePassword(this.value)) {
                showError(this, '密碼必須至少8個字符');
            } else if (this.value && validatePassword(this.value)) {
                clearError(this);
                showSuccess(this);
            }
        });
    }

    // 登入表單提交
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            let isValid = true;
            
            // 驗證電子郵件
            if (!emailInput.value) {
                showError(emailInput, '請輸入電子郵件地址');
                isValid = false;
            } else if (!validateEmail(emailInput.value)) {
                showError(emailInput, '請輸入有效的電子郵件地址');
                isValid = false;
            }
            
            // 驗證密碼
            if (!passwordInput.value) {
                showError(passwordInput, '請輸入密碼');
                isValid = false;
            }
            
            if (isValid) {
                // 顯示載入狀態
                signinBtn.classList.add('loading');
                signinBtn.disabled = true;
                
                // 模擬登入請求
                setTimeout(() => {
                    alert('登入功能正在開發中！\n\n電子郵件: ' + emailInput.value);
                    signinBtn.classList.remove('loading');
                    signinBtn.disabled = false;
                }, 2000);
            }
        });
    }

    // Google登入
    if (googleSigninBtn) {
        googleSigninBtn.addEventListener('click', function() {
            alert('Google登入功能即將推出！');
        });
    }

    // 模態框功能
    function openModal(modal) {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    function closeModal(modal) {
        modal.classList.remove('active');
        document.body.style.overflow = 'auto';
    }

    // 忘記密碼
    if (forgotPasswordLink) {
        forgotPasswordLink.addEventListener('click', function(e) {
            e.preventDefault();
            openModal(forgotPasswordModal);
        });
    }

    // 註冊
    if (signupLink) {
        signupLink.addEventListener('click', function(e) {
            e.preventDefault();
            openModal(signupModal);
        });
    }

    // 關閉模態框
    if (closeForgotModal) {
        closeForgotModal.addEventListener('click', function() {
            closeModal(forgotPasswordModal);
        });
    }

    if (closeSignupModal) {
        closeSignupModal.addEventListener('click', function() {
            closeModal(signupModal);
        });
    }

    // 點擊模態框外部關閉
    [forgotPasswordModal, signupModal].forEach(modal => {
        if (modal) {
            modal.addEventListener('click', function(e) {
                if (e.target === this || e.target.classList.contains('modal-overlay')) {
                    closeModal(this);
                }
            });
        }
    });

    // ESC鍵關閉模態框
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            [forgotPasswordModal, signupModal].forEach(modal => {
                if (modal && modal.classList.contains('active')) {
                    closeModal(modal);
                }
            });
        }
    });

    // 忘記密碼表單
    const forgotPasswordForm = document.getElementById('forgot-password-form');
    if (forgotPasswordForm) {
        forgotPasswordForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const forgotEmail = document.getElementById('forgot-email').value;
            
            if (!forgotEmail) {
                alert('請輸入電子郵件地址');
                return;
            }
            
            if (!validateEmail(forgotEmail)) {
                alert('請輸入有效的電子郵件地址');
                return;
            }
            
            // 模擬發送重設鏈接
            alert('重設密碼鏈接已發送到: ' + forgotEmail);
            closeModal(forgotPasswordModal);
            forgotPasswordForm.reset();
        });
    }

    // 註冊表單
    const signupForm = document.getElementById('signup-form');
    if (signupForm) {
        signupForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const name = document.getElementById('signup-name').value;
            const email = document.getElementById('signup-email').value;
            const password = document.getElementById('signup-password').value;
            const terms = document.getElementById('terms-agreement').checked;
            
            let isValid = true;
            
            if (!name.trim()) {
                alert('請輸入您的全名');
                isValid = false;
            }
            
            if (!email) {
                alert('請輸入電子郵件地址');
                isValid = false;
            } else if (!validateEmail(email)) {
                alert('請輸入有效的電子郵件地址');
                isValid = false;
            }
            
            if (!password) {
                alert('請輸入密碼');
                isValid = false;
            } else if (!validatePassword(password)) {
                alert('密碼必須至少8個字符');
                isValid = false;
            }
            
            if (!terms) {
                alert('請同意服務條款和隱私政策');
                isValid = false;
            }
            
            if (isValid) {
                // 模擬註冊
                alert('註冊功能正在開發中！\n\n姓名: ' + name + '\n電子郵件: ' + email);
                closeModal(signupModal);
                signupForm.reset();
            }
        });
    }

    // 自動填充測試數據（開發用）
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
        const fillTestDataBtn = document.createElement('button');
        fillTestDataBtn.textContent = '填充測試數據';
        fillTestDataBtn.style.cssText = `
            position: fixed;
            bottom: 20px;
            left: 20px;
            background: #10b981;
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.875rem;
            z-index: 1000;
        `;
        
        fillTestDataBtn.addEventListener('click', function() {
            if (emailInput) emailInput.value = 'test@example.com';
            if (passwordInput) passwordInput.value = 'password123';
        });
        
        document.body.appendChild(fillTestDataBtn);
    }

    // 鍵盤導航支持
    document.addEventListener('keydown', function(e) {
        // Tab鍵焦點管理
        if (e.key === 'Tab') {
            const focusableElements = document.querySelectorAll(
                'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
            );
            
            const firstElement = focusableElements[0];
            const lastElement = focusableElements[focusableElements.length - 1];
            
            if (e.shiftKey) {
                if (document.activeElement === firstElement) {
                    lastElement.focus();
                    e.preventDefault();
                }
            } else {
                if (document.activeElement === lastElement) {
                    firstElement.focus();
                    e.preventDefault();
                }
            }
        }
        
        // Enter鍵提交表單
        if (e.key === 'Enter' && e.target.tagName === 'INPUT') {
            const form = e.target.closest('form');
            if (form) {
                const submitBtn = form.querySelector('button[type="submit"]');
                if (submitBtn) {
                    submitBtn.click();
                }
            }
        }
    });

    // 表單自動儲存到localStorage
    function saveFormData(formId, data) {
        localStorage.setItem('formData_' + formId, JSON.stringify(data));
    }

    function loadFormData(formId) {
        const data = localStorage.getItem('formData_' + formId);
        return data ? JSON.parse(data) : null;
    }

    // 載入已儲存的表單數據
    const savedLoginData = loadFormData('login-form');
    if (savedLoginData && emailInput) {
        emailInput.value = savedLoginData.email || '';
        const rememberCheckbox = document.getElementById('remember-me');
        if (rememberCheckbox && savedLoginData.remember) {
            rememberCheckbox.checked = true;
        }
    }

    // 儲存表單數據
    if (loginForm) {
        loginForm.addEventListener('input', function() {
            const rememberCheckbox = document.getElementById('remember-me');
            if (rememberCheckbox && rememberCheckbox.checked) {
                saveFormData('login-form', {
                    email: emailInput.value,
                    remember: true
                });
            }
        });
    }

    // 安全性：清除密碼輸入框的自動完成
    document.querySelectorAll('input[type="password"]').forEach(input => {
        input.setAttribute('autocomplete', 'current-password');
    });

    console.log('登入頁面載入完成！');
});

// 全域函數：驗證表單
window.validateLoginForm = function(email, password) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    
    if (!email || !emailRegex.test(email)) {
        return { valid: false, message: '請輸入有效的電子郵件地址' };
    }
    
    if (!password || password.length < 8) {
        return { valid: false, message: '密碼必須至少8個字符' };
    }
    
    return { valid: true };
};

// 全域函數：模擬登入API
window.simulateLogin = async function(email, password, remember = false) {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            // 模擬不同的登入結果
            if (email === 'admin@aibankparser.com' && password === 'admin123') {
                resolve({
                    success: true,
                    user: {
                        id: 1,
                        email: email,
                        name: 'Admin User',
                        role: 'admin'
                    },
                    token: 'mock_jwt_token_' + Date.now()
                });
            } else if (email === 'user@example.com' && password === 'password123') {
                resolve({
                    success: true,
                    user: {
                        id: 2,
                        email: email,
                        name: 'Test User',
                        role: 'user'
                    },
                    token: 'mock_jwt_token_' + Date.now()
                });
            } else {
                reject({
                    success: false,
                    message: '電子郵件或密碼錯誤'
                });
            }
        }, 1500); // 模擬網絡延遲
    });
};
