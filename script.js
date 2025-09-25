// JavaScript文件 - VaultCaddy網站互動功能

document.addEventListener('DOMContentLoaded', function() {
    
    // 初始化導航欄
    if (window.VaultCaddyNavbar) {
        console.log('✅ 導航欄已初始化');
    } else {
        console.warn('⚠️ 導航欄未初始化，嘗試重新初始化...');
        // 確保導航組件存在並初始化
        if (typeof VaultCaddyNavbar !== 'undefined') {
            window.VaultCaddyNavbar = new VaultCaddyNavbar();
        }
    }
    
    // 導航欄切換功能（移動設備）
    const navToggle = document.getElementById('nav-toggle');
    const navMenu = document.getElementById('nav-menu');

    if (navToggle && navMenu) {
        navToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
        });

        // 點擊導航鏈接時關閉菜單
        const navLinks = document.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                navMenu.classList.remove('active');
            });
        });
    }

    // 文件上傳功能
    const uploadArea = document.getElementById('upload-area');
    const fileInput = document.getElementById('file-input');
    const browseBtn = document.querySelector('.browse-btn');

    if (uploadArea && fileInput && browseBtn) {
        // 點擊瀏覽按鈕
        browseBtn.addEventListener('click', function(e) {
            e.preventDefault();
            if (checkAuthBeforeUpload()) {
                fileInput.click();
            }
        });

        // 點擊上傳區域
        uploadArea.addEventListener('click', function() {
            if (checkAuthBeforeUpload()) {
                fileInput.click();
            }
        });

        // 文件拖放功能
        uploadArea.addEventListener('dragover', function(e) {
            e.preventDefault();
            uploadArea.style.background = 'rgba(255, 255, 255, 0.2)';
            uploadArea.style.borderColor = 'rgba(255, 255, 255, 0.6)';
        });

        uploadArea.addEventListener('dragleave', function(e) {
            e.preventDefault();
            uploadArea.style.background = 'rgba(255, 255, 255, 0.1)';
            uploadArea.style.borderColor = 'rgba(255, 255, 255, 0.3)';
        });

        uploadArea.addEventListener('drop', function(e) {
            e.preventDefault();
            uploadArea.style.background = 'rgba(255, 255, 255, 0.1)';
            uploadArea.style.borderColor = 'rgba(255, 255, 255, 0.3)';
            
            const files = e.dataTransfer.files;
            handleFiles(files);
        });

        // 文件選擇處理
        fileInput.addEventListener('change', function(e) {
            const files = e.target.files;
            handleFiles(files);
        });
    }

    // 處理選擇的文件
    function handleFiles(files) {
        if (files.length > 0) {
            const uploadContent = document.querySelector('.upload-content');
            let fileNames = Array.from(files).map(file => file.name).join(', ');
            
            // 創建處理中的UI
            uploadContent.innerHTML = `
                <i class="fas fa-file-pdf" style="color: #ef4444;"></i>
                <p style="margin-top: 1rem;">已選擇: ${fileNames}</p>
                <div style="margin-top: 1rem;">
                    <div style="background: rgba(255,255,255,0.2); height: 4px; border-radius: 2px;">
                        <div class="progress-bar" style="background: #10b981; height: 100%; width: 0%; border-radius: 2px; transition: width 0.3s ease;"></div>
                    </div>
                    <p style="margin-top: 0.5rem; font-size: 0.9rem;">正在處理...</p>
                </div>
                <button class="browse-btn" style="margin-top: 1rem;" onclick="resetUpload()">重新選擇</button>
            `;

            // 模擬進度條
            const progressBar = document.querySelector('.progress-bar');
            let progress = 0;
            const interval = setInterval(() => {
                progress += Math.random() * 15;
                if (progress >= 100) {
                    progress = 100;
                    clearInterval(interval);
                    setTimeout(() => {
                        showCompletionMessage();
                    }, 500);
                }
                progressBar.style.width = progress + '%';
            }, 200);
        }
    }

    // 重置上傳區域
    window.resetUpload = function() {
        const uploadContent = document.querySelector('.upload-content');
        uploadContent.innerHTML = `
            <i class="fas fa-cloud-upload-alt"></i>
            <p>拖放PDF文件到這裡 <span class="or">或</span> <button class="browse-btn">瀏覽</button></p>
            <input type="file" id="file-input" accept=".pdf" multiple>
        `;
        
        // 重新綁定事件
        const newFileInput = document.getElementById('file-input');
        const newBrowseBtn = document.querySelector('.browse-btn');
        
        newBrowseBtn.addEventListener('click', function(e) {
            e.preventDefault();
            newFileInput.click();
        });
        
        newFileInput.addEventListener('change', function(e) {
            const files = e.target.files;
            handleFiles(files);
        });
    };

    // 顯示完成消息
    function showCompletionMessage() {
        const uploadContent = document.querySelector('.upload-content');
        uploadContent.innerHTML = `
            <i class="fas fa-check-circle" style="color: #10b981; font-size: 3rem;"></i>
            <h4 style="margin: 1rem 0; color: #10b981;">處理完成！</h4>
            <p>您的文件已成功轉換並下載到您的電腦。</p>
            <button class="browse-btn" style="margin-top: 1rem;" onclick="resetUpload()">處理更多文件</button>
        `;
    }

    // 價格切換功能
    const toggleBtns = document.querySelectorAll('.toggle-btn');
    const monthlyPrices = document.querySelectorAll('.monthly-price');
    const yearlyPrices = document.querySelectorAll('.yearly-price');

    toggleBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            // 移除所有active類
            toggleBtns.forEach(b => b.classList.remove('active'));
            // 添加active類到當前按鈕
            this.classList.add('active');

            const plan = this.getAttribute('data-plan');
            
            if (plan === 'yearly') {
                monthlyPrices.forEach(price => price.style.display = 'none');
                yearlyPrices.forEach(price => price.style.display = 'inline');
            } else {
                monthlyPrices.forEach(price => price.style.display = 'inline');
                yearlyPrices.forEach(price => price.style.display = 'none');
            }
        });
    });

    // FAQ手風琴功能
    const faqItems = document.querySelectorAll('.faq-item');
    
    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        question.addEventListener('click', function() {
            const isActive = item.classList.contains('active');
            
            // 關閉所有其他項目
            faqItems.forEach(otherItem => {
                if (otherItem !== item) {
                    otherItem.classList.remove('active');
                }
            });
            
            // 切換當前項目
            if (isActive) {
                item.classList.remove('active');
            } else {
                item.classList.add('active');
            }
        });
    });

    // 聊天視窗功能
    const chatWidget = document.getElementById('chat-widget');
    const chatButton = chatWidget.querySelector('.chat-button');

    if (chatButton) {
        chatButton.addEventListener('click', function() {
            // 模擬聊天視窗開啟
            alert('聊天功能即將推出！請通過電子郵件聯絡我們：support@aibankparser.com');
        });
    }

    // 平滑滾動功能
    const navLinks = document.querySelectorAll('a[href^="#"]');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                const offsetTop = targetElement.offsetTop - 80; // 考慮固定導航欄高度
                
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });

    // 滾動時導航欄效果
    window.addEventListener('scroll', function() {
        const navbar = document.querySelector('.navbar');
        
        if (window.scrollY > 100) {
            navbar.style.boxShadow = '0 4px 12px rgba(0,0,0,0.15)';
            navbar.style.backgroundColor = 'rgba(255, 255, 255, 0.95)';
            navbar.style.backdropFilter = 'blur(10px)';
        } else {
            navbar.style.boxShadow = '0 2px 4px rgba(0,0,0,0.1)';
            navbar.style.backgroundColor = '#ffffff';
            navbar.style.backdropFilter = 'none';
        }
    });

    // 元素進入視窗時的動畫
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // 觀察需要動畫的元素
    const animateElements = document.querySelectorAll('.feature-card, .pricing-card, .service-item, .blog-article');
    animateElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });

    // CTA按鈕點擊處理
    const ctaBtns = document.querySelectorAll('.cta-btn');
    
    ctaBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const btnText = this.textContent.trim();
            
            if (btnText === '開始免費使用') {
                alert('免費註冊功能即將推出！請先嘗試上傳您的文件。');
            } else if (btnText === '立即開始') {
                alert('專業方案註冊功能即將推出！請聯絡我們了解更多詳情。');
            } else if (btnText === '聯絡我們') {
                alert('企業方案諮詢\n\n請發送電子郵件至：enterprise@aibankparser.com\n或致電：+1-234-567-8900');
            }
        });
    });

    // 表單驗證和提交處理
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // 獲取表單數據
            const formData = new FormData(this);
            const data = Object.fromEntries(formData);
            
            // 簡單驗證
            let isValid = true;
            const requiredFields = this.querySelectorAll('[required]');
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.style.borderColor = '#ef4444';
                } else {
                    field.style.borderColor = '#d1d5db';
                }
            });
            
            if (isValid) {
                // 模擬提交
                const submitBtn = this.querySelector('button[type="submit"]');
                const originalText = submitBtn.textContent;
                
                submitBtn.textContent = '提交中...';
                submitBtn.disabled = true;
                
                setTimeout(() => {
                    alert('表單提交成功！我們會盡快與您聯絡。');
                    this.reset();
                    submitBtn.textContent = originalText;
                    submitBtn.disabled = false;
                }, 2000);
            } else {
                alert('請填寫所有必填欄位。');
            }
        });
    });

    // 複製到剪貼板功能（如果有代碼示例）
    const copyBtns = document.querySelectorAll('.copy-btn');
    
    copyBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const targetId = this.getAttribute('data-target');
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                const text = targetElement.textContent;
                navigator.clipboard.writeText(text).then(() => {
                    this.textContent = '已複製！';
                    setTimeout(() => {
                        this.textContent = '複製';
                    }, 2000);
                });
            }
        });
    });

    // 工具提示功能
    const tooltips = document.querySelectorAll('[data-tooltip]');
    
    tooltips.forEach(element => {
        element.addEventListener('mouseenter', function() {
            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip';
            tooltip.textContent = this.getAttribute('data-tooltip');
            tooltip.style.cssText = `
                position: absolute;
                background: #1f2937;
                color: white;
                padding: 0.5rem;
                border-radius: 4px;
                font-size: 0.875rem;
                z-index: 1000;
                pointer-events: none;
                white-space: nowrap;
            `;
            
            document.body.appendChild(tooltip);
            
            const rect = this.getBoundingClientRect();
            tooltip.style.left = rect.left + rect.width / 2 - tooltip.offsetWidth / 2 + 'px';
            tooltip.style.top = rect.top - tooltip.offsetHeight - 5 + 'px';
            
            this._tooltip = tooltip;
        });
        
        element.addEventListener('mouseleave', function() {
            if (this._tooltip) {
                document.body.removeChild(this._tooltip);
                this._tooltip = null;
            }
        });
    });

    // 鍵盤導航支持
    document.addEventListener('keydown', function(e) {
        // ESC鍵關閉模態框
        if (e.key === 'Escape') {
            const activeModals = document.querySelectorAll('.modal.active');
            activeModals.forEach(modal => {
                modal.classList.remove('active');
            });
            
            // 關閉移動菜單
            if (navMenu && navMenu.classList.contains('active')) {
                navMenu.classList.remove('active');
            }
        }
    });

    // 性能優化：延遲加載圖片
    const lazyImages = document.querySelectorAll('img[data-src]');
    
    if (lazyImages.length > 0) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        lazyImages.forEach(img => imageObserver.observe(img));
    }

    // 文檔類型選擇器功能
    function initDocumentTypeSelector() {
        const modelCards = document.querySelectorAll('.model-card');
        const selectedModelInput = document.getElementById('selected-model') || createHiddenInput();
        
        modelCards.forEach(card => {
            card.addEventListener('click', function() {
                // 移除所有active狀態
                modelCards.forEach(c => c.classList.remove('active'));
                // 為當前卡片添加active狀態
                this.classList.add('active');
                
                // 更新選中的模型
                const modelType = this.getAttribute('data-model');
                selectedModelInput.value = modelType;
                
                // 更新上傳區域提示文字
                updateUploadAreaText(modelType);
            });
        });
        
        function createHiddenInput() {
            const input = document.createElement('input');
            input.type = 'hidden';
            input.id = 'selected-model';
            input.value = 'bank-statement';
            document.body.appendChild(input);
            return input;
        }
    }
    
    function updateUploadAreaText(modelType) {
        const uploadText = document.querySelector('[data-translate="upload_text"]');
        if (!uploadText) return;
        
        const textMap = {
            'bank-statement': '拖放銀行對帳單PDF文件到這裡',
            'invoice': '拖放發票PDF文件到這裡',
            'receipt': '拖放收據PDF文件到這裡',
            'general': '拖放任何PDF文件到這裡'
        };
        
        const currentLang = window.languageManager?.currentLanguage || 'zh-TW';
        const baseText = textMap[modelType] || textMap['bank-statement'];
        uploadText.innerHTML = `${baseText} <span class="or">或</span> <button class="browse-btn">瀏覽</button>`;
    }
    
    // Credits積分系統
    let userCredits = parseInt(localStorage.getItem('userCredits')) || 10;
    
    function initCreditsSystem() {
        updateCreditsDisplay();
        
        // 監聽文件上傳
        const fileInput = document.getElementById('file-input');
        if (fileInput) {
            fileInput.addEventListener('change', handleFileUpload);
        }
    }
    
    function updateCreditsDisplay() {
        const creditsCount = document.getElementById('credits-count');
        if (creditsCount) {
            creditsCount.textContent = userCredits;
        }
    }
    
    // 檢查登入狀態的函數
    function checkAuthAndRedirect(selectedModel = 'bank-statement') {
        const isLoggedIn = window.VaultCaddyAuth && window.VaultCaddyAuth.isAuthenticated();
        
        if (!isLoggedIn) {
            // 保存要處理的文檔類型到localStorage
            localStorage.setItem('pendingDocumentType', selectedModel);
            // 未登入，跳轉到登入頁面
            window.location.href = 'auth.html';
            return false;
        }
        
        // 已登入，跳轉到統一的儀表板頁面
        window.location.href = `dashboard.html#${selectedModel}`;
        return true;
    }

    function handleFileUpload(event) {
        // 檢查登入狀態
        const isLoggedIn = window.VaultCaddyAuth && window.VaultCaddyAuth.isAuthenticated();
        if (!isLoggedIn) {
            checkAuthAndRedirect();
            return;
        }
        
        const files = event.target.files;
        if (!files.length) return;
        
        // 計算需要的Credits（假設每個文件需要1個Credit）
        let totalCreditsNeeded = 0;
        
        // 這裡應該通過API獲取實際的頁數，暫時模擬
        Array.from(files).forEach(file => {
            // 模擬：每個文件需要1-5個Credits
            totalCreditsNeeded += Math.floor(Math.random() * 5) + 1;
        });
        
        if (userCredits >= totalCreditsNeeded) {
            // 處理文件上傳
            processFileUpload(files, totalCreditsNeeded);
        } else {
            alert(`Credits不足！需要 ${totalCreditsNeeded} Credits，您當前有 ${userCredits} Credits。`);
            event.target.value = ''; // 清空文件選擇
        }
    }
    
    function processFileUpload(files, creditsUsed) {
        // 模擬文件處理
        showProcessingModal();
        
        setTimeout(() => {
            // 扣除Credits
            userCredits -= creditsUsed;
            localStorage.setItem('userCredits', userCredits);
            updateCreditsDisplay();
            
            hideProcessingModal();
            showSuccessMessage(`成功處理 ${files.length} 個文件，使用了 ${creditsUsed} Credits`);
        }, 2000);
    }
    
    function showProcessingModal() {
        // 創建處理中的模態框
        const modal = document.createElement('div');
        modal.id = 'processing-modal';
        modal.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 10000;
        `;
        
        modal.innerHTML = `
            <div style="background: white; padding: 2rem; border-radius: 12px; text-align: center;">
                <div style="width: 40px; height: 40px; border: 4px solid #f3f3f3; border-top: 4px solid #3498db; border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto 1rem;"></div>
                <h3>處理文件中...</h3>
                <p>請稍候，我們正在處理您的文件</p>
            </div>
        `;
        
        document.body.appendChild(modal);
    }
    
    function hideProcessingModal() {
        const modal = document.getElementById('processing-modal');
        if (modal) {
            modal.remove();
        }
    }
    
    function showSuccessMessage(message) {
        const toast = document.createElement('div');
        toast.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #10b981;
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 8px;
            z-index: 10001;
            box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
        `;
        toast.textContent = message;
        
        document.body.appendChild(toast);
        
        setTimeout(() => {
            toast.remove();
        }, 3000);
    }
    
    // 客戶評價滑塊功能
    function initTestimonialsSlider() {
        const track = document.getElementById('testimonial-track');
        const prevBtn = document.getElementById('testimonial-prev');
        const nextBtn = document.getElementById('testimonial-next');
        const dots = document.querySelectorAll('.dot');
        
        if (!track) return;
        
        let currentSlide = 0;
        const totalSlides = 4;
        
        function updateSlider() {
            const translateX = -currentSlide * 25; // 25% per slide
            track.style.transform = `translateX(${translateX}%)`;
            
            // 更新dots
            dots.forEach((dot, index) => {
                dot.classList.toggle('active', index === currentSlide);
            });
            
            // 更新按鈕狀態
            if (prevBtn) prevBtn.disabled = currentSlide === 0;
            if (nextBtn) nextBtn.disabled = currentSlide === totalSlides - 1;
        }
        
        // 前一個按鈕
        if (prevBtn) {
            prevBtn.addEventListener('click', () => {
                if (currentSlide > 0) {
                    currentSlide--;
                    updateSlider();
                }
            });
        }
        
        // 下一個按鈕
        if (nextBtn) {
            nextBtn.addEventListener('click', () => {
                if (currentSlide < totalSlides - 1) {
                    currentSlide++;
                    updateSlider();
                }
            });
        }
        
        // 點擊dots
        dots.forEach((dot, index) => {
            dot.addEventListener('click', () => {
                currentSlide = index;
                updateSlider();
            });
        });
        
        // 自動播放（可選）
        let autoPlayInterval = setInterval(() => {
            if (currentSlide < totalSlides - 1) {
                currentSlide++;
            } else {
                currentSlide = 0;
            }
            updateSlider();
        }, 5000);
        
        // 滑鼠懸停時暫停自動播放
        const testimonials = document.querySelector('.testimonials');
        if (testimonials) {
            testimonials.addEventListener('mouseenter', () => {
                clearInterval(autoPlayInterval);
            });
            
            testimonials.addEventListener('mouseleave', () => {
                autoPlayInterval = setInterval(() => {
                    if (currentSlide < totalSlides - 1) {
                        currentSlide++;
                    } else {
                        currentSlide = 0;
                    }
                    updateSlider();
                }, 5000);
            });
        }
        
        // 初始化
        updateSlider();
    }
    
    // 模擬登入狀態管理
    function initLoginSystem() {
        const loginBtn = document.querySelector('.login-btn');
        const body = document.body;
        
        if (loginBtn) {
            loginBtn.addEventListener('click', function(e) {
                e.preventDefault();
                
                // 切換登入狀態
                if (body.classList.contains('user-logged-in')) {
                    // 登出
                    body.classList.remove('user-logged-in');
                    loginBtn.textContent = '登入 →';
                } else {
                    // 登入
                    body.classList.add('user-logged-in');
                    loginBtn.textContent = '登出 →';
                }
            });
        }
        
        // 檢查是否已登入（從localStorage）
        const isLoggedIn = localStorage.getItem('userLoggedIn') === 'true';
        if (isLoggedIn) {
            body.classList.add('user-logged-in');
            if (loginBtn) loginBtn.textContent = '登出 →';
        }
    }
    
    // 添加拖放和點擊登入檢查
    function addAuthCheckToUpload() {
        const uploadArea = document.querySelector('.upload-area');
        const fileInput = document.getElementById('file-input');
        
        if (uploadArea) {
            // 複寫拖放事件
            const newUploadArea = uploadArea.cloneNode(true);
            uploadArea.parentNode.replaceChild(newUploadArea, uploadArea);
            
            newUploadArea.addEventListener('click', function(e) {
                e.preventDefault();
                const selectedModel = getSelectedModel();
                const isLoggedIn = window.VaultCaddyAuth && window.VaultCaddyAuth.isAuthenticated();
                if (!isLoggedIn) {
                    checkAuthAndRedirect(selectedModel);
                    return;
                }
                fileInput?.click();
            });
            
            newUploadArea.addEventListener('dragover', function(e) {
                e.preventDefault();
                this.classList.add('dragover');
            });
            
            newUploadArea.addEventListener('dragleave', function(e) {
                e.preventDefault();
                this.classList.remove('dragover');
            });
            
            newUploadArea.addEventListener('drop', function(e) {
                e.preventDefault();
                this.classList.remove('dragover');
                
                const selectedModel = getSelectedModel();
                const isLoggedIn = window.VaultCaddyAuth && window.VaultCaddyAuth.isAuthenticated();
                if (!isLoggedIn) {
                    checkAuthAndRedirect(selectedModel);
                    return;
                }
                
                const files = e.dataTransfer.files;
                if (files.length > 0) {
                    handleFileUpload({ target: { files } });
                }
            });
        }
        
        // 瀏覽按鈕點擊處理
        document.addEventListener('click', function(e) {
            if (e.target.classList.contains('browse-btn')) {
                e.preventDefault();
                const selectedModel = getSelectedModel();
                const isLoggedIn = window.VaultCaddyAuth && window.VaultCaddyAuth.isAuthenticated();
                if (!isLoggedIn) {
                    checkAuthAndRedirect(selectedModel);
                    return;
                }
                fileInput?.click();
            }
        });
    }
    
    function getSelectedModel() {
        const activeCard = document.querySelector('.model-card.active');
        return activeCard ? activeCard.dataset.model : 'bank-statement';
    }

    // 初始化新功能
    initDocumentTypeSelector();
    initCreditsSystem();
    initTestimonialsSlider();
    initLoginSystem();
    addAuthCheckToUpload();
    
    console.log('SmartDoc Parser網站已載入完成！');
});

// 全局函數：檢查瀏覽器支持
function checkBrowserSupport() {
    const features = {
        fileAPI: 'FileReader' in window,
        dragDrop: 'draggable' in document.createElement('div'),
        localStorage: 'localStorage' in window,
        fetch: 'fetch' in window
    };
    
    const unsupported = Object.keys(features).filter(key => !features[key]);
    
    if (unsupported.length > 0) {
        console.warn('某些功能在您的瀏覽器中可能無法正常工作：', unsupported);
        
        // 顯示瀏覽器兼容性警告
        const warningBanner = document.createElement('div');
        warningBanner.style.cssText = `
            background: #fbbf24;
            color: #92400e;
            padding: 1rem;
            text-align: center;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            z-index: 9999;
        `;
        warningBanner.innerHTML = `
            <p>您的瀏覽器版本較舊，某些功能可能無法正常工作。建議升級到最新版本的瀏覽器。
            <button onclick="this.parentElement.parentElement.remove()" style="margin-left: 1rem; background: transparent; border: 1px solid #92400e; color: #92400e; padding: 0.25rem 0.5rem; border-radius: 4px; cursor: pointer;">關閉</button>
            </p>
        `;
        
        document.body.insertBefore(warningBanner, document.body.firstChild);
    }
    
    return unsupported.length === 0;
}

// 初始化瀏覽器支持檢查
checkBrowserSupport();

/**
 * 檢查用戶登入狀態，未登入則引導到登入頁面
 */
function checkAuthBeforeUpload() {
    const token = localStorage.getItem('vaultcaddy_token');
    const userData = localStorage.getItem('vaultcaddy_user');
    const isLoggedIn = localStorage.getItem('userLoggedIn') === 'true';
    
    // 檢查是否已登入
    if (!token && !userData && !isLoggedIn) {
        console.log('🔐 用戶未登入，引導到登入頁面...');
        
        // 保存當前頁面，登入後返回
        localStorage.setItem('vaultcaddy_redirect_after_login', window.location.href);
        
        // 顯示提示並跳轉
        alert('請先登入以使用文檔處理功能');
        window.location.href = 'auth.html';
        
        return false;
    }
    
    return true;
}

// 舊的登入功能已移除，現在使用 navbar-component.js 中的統一登入處理
