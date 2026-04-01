// --- Extracted Script Block 2 ---

        document.addEventListener('DOMContentLoaded', function() {
            // 創建 Intersection Observer
            const observerOptions = {
                threshold: 0.1,
                rootMargin: '0px 0px -50px 0px'
            };
            
            const observer = new IntersectionObserver(function(entries) {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('visible');
                        // 一次性動畫，觀察後即停止
                        observer.unobserve(entry.target);
                    }
                });
            }, observerOptions);
            
            // 為所有需要動畫的元素添加觀察
            setTimeout(() => {
                const animatedElements = document.querySelectorAll('.fade-in-up, .fade-in-left, .fade-in-right, .scale-in');
                animatedElements.forEach(el => observer.observe(el));
            }, 100);
        });
    

// --- Extracted Script Block 3 ---

      window.dataLayer = window.dataLayer | [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-LWPEKNC7RQ');
    

// --- Extracted Script Block 4 ---

    // Scroll Progress Bar
    window.addEventListener('scroll', function() {
        const windowHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        const scrolled = (window.scrollY / windowHeight) * 100;
        const progressBar = document.getElementById('scroll-progress');
        if (progressBar) {
            progressBar.style.width = scrolled + '%';
        }
    });
    

// --- Extracted Script Block 6 ---

        document.addEventListener('DOMContentLoaded', function() {
            console.log('✅ index.html 初始化');
            
            let userCredits = 0;
            let userEmail = '';
            let userDisplayName = '';
            
            // 獲取用戶首字母
            function getUserInitial() {
                // 優先使用 displayName 的第一個字母
                if (userDisplayName && userDisplayName.trim() && userDisplayName !== '0') {
                    return userDisplayName.charAt(0).toUpperCase();
                }
                // 否則使用 email 的第一個字母
                if (userEmail && userEmail.trim()) {
                    return userEmail.charAt(0).toUpperCase();
                }
                return 'U';
            }
            
            // 🔥 漢堡菜單功能（立即執行，不等待 DOMContentLoaded）
            (function() {
                console.log('🔵 初始化漢堡菜單...');
                
                // 打開側邊欄
                window.openMobileSidebar = function() {
                    console.log('🔵 openMobileSidebar 被調用');
                    const sidebar = document.getElementById('mobile-sidebar');
                    const overlay = document.getElementById('mobile-sidebar-overlay');
                    console.log('🔵 sidebar:', sidebar);
                    console.log('🔵 overlay:', overlay);
                    
                    if (sidebar && overlay) {
                        sidebar.style.left = '0';
                        overlay.style.display = 'block';
                        document.body.style.overflow = 'hidden';
                        console.log('✅ 側邊欄已打開');
                    } else {
                        console.error('❌ 找不到側邊欄或遮罩元素');
                    }
                };
                
                // 關閉側邊欄
                window.closeMobileSidebar = function() {
                    console.log('🔵 closeMobileSidebar 被調用');
                    const sidebar = document.getElementById('mobile-sidebar');
                    const overlay = document.getElementById('mobile-sidebar-overlay');
                    
                    if (sidebar && overlay) {
                        sidebar.style.left = '-100%';
                        overlay.style.display = 'none';
                        document.body.style.overflow = 'auto';
                        console.log('✅ 側邊欄已關閉');
                    }
                };
                
                // 確保漢堡菜單按鈕綁定（多重綁定策略）
                const menuBtn = document.getElementById('mobile-menu-btn');
                if (menuBtn) {
                    console.log('✅ 找到漢堡菜單按鈕，開始綁定事件');
                    
                    // 創建統一的處理函數
                    const handleMenuOpen = function(e) {
                        console.log('🔵 菜單按鈕被觸發', e.type);
                        e.preventDefault();
                        e.stopPropagation();
                        window.openMobileSidebar();
                    };
                    
                    // 1. Click 事件（滑鼠和一般觸摸）
                    menuBtn.addEventListener('click', handleMenuOpen, { passive: false });
                    
                    // 2. Removed Touchend event to prevent double firing
                    
                    // 🔥 3. 只在手機版設置可見（不影響桌面版）
                    if (window.innerWidth <= 768) {
                    menuBtn.style.display = 'block';
                    menuBtn.style.visibility = 'visible';
                    menuBtn.style.pointerEvents = 'auto';
                    menuBtn.style.zIndex = '1001';
                        console.log('✅ 手機版：漢堡菜單已啟用');
                    } else {
                        console.log('ℹ️ 桌面版：漢堡菜單保持隱藏');
                    }
                    
                    console.log('✅ 漢堡菜單功能已綁定（click + touchend）');
                } else {
                    console.error('❌ 找不到漢堡菜單按鈕');
                }
            })();
                
                // 手機版自動輪播（僅在手機版啟用）
                if (window.innerWidth <= 768) {
                    // 評價輪播
                    const testimonialsContainer = document.getElementById('testimonials-container');
                    if (testimonialsContainer) {
                        let testimonialIndex = 0;
                        const testimonialCards = testimonialsContainer.children;
                        
                        setInterval(() => {
                            testimonialIndex = (testimonialIndex + 1) % testimonialCards.length;
                            const scrollAmount = testimonialCards[testimonialIndex].offsetLeft - testimonialsContainer.offsetLeft;
                            testimonialsContainer.scrollTo({
                                left: scrollAmount,
                                behavior: 'smooth'
                            });
                        }, 4000); // 每4秒切換
                    }
                    
                    // 學習中心輪播
                    const learningContainer = document.getElementById('learning-center-container');
                    if (learningContainer) {
                        let learningIndex = 0;
                        const learningCards = learningContainer.children;
                        
                        setInterval(() => {
                            learningIndex = (learningIndex + 1) % learningCards.length;
                            const scrollAmount = learningCards[learningIndex].offsetLeft - learningContainer.offsetLeft;
                            learningContainer.scrollTo({
                                left: scrollAmount,
                                behavior: 'smooth'
                            });
                        }, 5000); // 每5秒切換
                    }
                }
            
            // 切換下拉菜單
            async function toggleDropdown() {
                const dropdown = document.getElementById('user-dropdown');
                if (dropdown.style.display === 'none') {
                    dropdown.style.display = 'block';
                    
                    // 🔥 即時從 SimpleDataManager 獲取最新用戶數據
                    let planType = 'Free Plan';
                    if (window.simpleDataManager && window.simpleDataManager.initialized) {
                        try {
                            userCredits = await window.simpleDataManager.getUserCredits();
                            console.log('✅ 即時獲取 Credits:', userCredits);
                            
                            // 獲取套餐類型
                            const currentUser = window.simpleAuth?.getCurrentUser();
                            if (currentUser) {
                                const userDoc = await window.simpleDataManager.db.collection('users').doc(currentUser.uid).get();
                                if (userDoc.exists) {
                                    planType = userDoc.data().planType || 'Free Plan';
                                }
                            }
                        } catch (error) {
                            console.error('❌ 無法獲取用戶數據:', error);
                        }
                    }
                    
                    // ✅ 更新下拉菜單內容（新版）
                    const avatarEl = document.getElementById('dropdown-avatar');
                    const nameEl = document.getElementById('dropdown-name');
                    const emailEl = document.getElementById('dropdown-email');
                    const creditsEl = document.getElementById('dropdown-credits');
                    const planEl = document.getElementById('dropdown-plan');
                    
                    if (avatarEl) avatarEl.textContent = getUserInitial();
                    if (nameEl) nameEl.textContent = userDisplayName || userEmail.split('@')[0] || 'User';
                    if (emailEl) emailEl.textContent = userEmail;
                    if (creditsEl) creditsEl.textContent = userCredits.toLocaleString();
                    if (planEl) planEl.textContent = planType;
                } else {
                    dropdown.style.display = 'none';
                }
            }
            
            // 點擊外部關閉下拉菜單
            document.addEventListener('click', function(event) {
                const dropdown = document.getElementById('user-dropdown');
                const userMenu = document.getElementById('user-menu');
                
                if (dropdown && userMenu && 
                    !dropdown.contains(event.target) && 
                    !userMenu.contains(event.target)) {
                    dropdown.style.display = 'none';
                }
            });
            
            // 登出功能
            window.handleLogout = async function() {
                try {
                    if (window.simpleAuth) {
                        await window.simpleAuth.logout();
                        window.location.href = 'index.html';
                    }
                } catch (error) {
                    console.error('登出失敗:', error);
                    alert('登出失敗，請重試');
                }
            };
            
            // 🔥 與 dashboard.html 完全相同的更新方式
            async function updateUserMenu() {
                const userMenu = document.getElementById('user-menu');
                if (!userMenu) return;
                
                try {
                    const isLoggedIn = window.simpleAuth && window.simpleAuth.isLoggedIn();
                    
                    if (isLoggedIn) {
                        // ✅ 已登入：顯示用戶頭像
                        const currentUser = window.simpleAuth.getCurrentUser();
                        userEmail = currentUser.email || '';
                        userDisplayName = currentUser.displayName || '';
                        
                        // 🔥 從 Firestore 獲取 displayName 和 credits
                        if (window.simpleDataManager && window.simpleDataManager.initialized) {
                            try {
                                const userDoc = await window.simpleDataManager.getUserDocument();
                                if (userDoc) {
                                    userDisplayName = userDoc.displayName || userDisplayName;
                                    userCredits = userDoc.credits || 0;
                                    console.log('✅ index.html 獲取 Credits:', userCredits);
                                }
                            } catch (error) {
                                console.log('⚠️ 無法從 Firestore 獲取用戶資料:', error);
                            }
                        } else {
                            console.log('⏳ SimpleDataManager 尚未初始化，等待中...');
                            // 延遲重試
                            setTimeout(async () => {
                                if (window.simpleDataManager && window.simpleDataManager.initialized) {
                                    try {
                                        userCredits = await window.simpleDataManager.getUserCredits();
                                        console.log('✅ 延遲獲取 Credits:', userCredits);
                                    } catch (error) {
                                        console.error('❌ 延遲獲取失敗:', error);
                                    }
                                }
                            }, 1000);
                        }
                        
                        const userInitial = getUserInitial();
                        console.log(`👤 用戶首字母: "${userInitial}" (displayName: "${userDisplayName}")`);
                        
                        // 🔥 已登入：顯示頭像和下拉菜單
                        userMenu.innerHTML = `
                            <div style="cursor: pointer; padding: 0.5rem; border-radius: 8px; transition: background 0.2s;" onclick="toggleDropdown()">
                                <div id="user-avatar" style="width: 32px; height: 32px; border-radius: 50%; background: #667eea; display: flex; align-items: center; justify-content: center; color: white; font-weight: 600; font-size: 0.875rem;">${userInitial}</div>
                            </div>
                        `;
                        userMenu.style.cursor = 'pointer';
                        console.log('✅ 用戶已登入，顯示頭像');
                    } else {
                        // ✅ 未登入：顯示登入按鈕
                        userMenu.innerHTML = `
                            <button onclick="openAuthModal()" style="padding: 0.5rem 1.5rem; background: #667eea; color: white; border: none; border-radius: 8px; font-weight: 600; cursor: pointer; transition: background 0.2s; font-size: 0.875rem;">
                                登入
                            </button>
                        `;
                        console.log('✅ 用戶未登入，顯示登入按鈕');
                    }
                } catch (e) {
                    console.log('❌ 無法更新用戶菜單:', e);
                }
            }
            
            // ✅ 等待 simpleAuth 初始化後再更新用戶菜單
            async function waitForAuthAndUpdate() {
                if (window.simpleAuth && window.simpleAuth.initialized) {
                    updateUserMenu();
                    return;
                }
                let attempts = 0;
                const checkInterval = setInterval(() => {
                    attempts++;
                    if (window.simpleAuth && window.simpleAuth.initialized) {
                        clearInterval(checkInterval);
                        console.log('✅ simpleAuth 初始化完成，更新用戶菜單');
                        updateUserMenu();
                    } else if (attempts > 50) {
                        clearInterval(checkInterval);
                        console.warn('⚠️ simpleAuth 初始化超時，強制更新用戶菜單');
                        updateUserMenu();
                    }
                }, 100);
            }
            waitForAuthAndUpdate();
            
            // 監聽 Firebase 和 Auth 事件
            window.addEventListener('firebase-ready', updateUserMenu);
            window.addEventListener('user-logged-in', updateUserMenu);
            window.addEventListener('user-logged-out', updateUserMenu);
            window.addEventListener('auth-state-changed', updateUserMenu);
            
            // 暴露 toggleDropdown 到全局
            window.toggleDropdown = toggleDropdown;
            
            // 🔥 手機版強制修改樣式（解決CSS無法覆蓋內聯樣式的問題）
            function forceMobileStyles() {
                // 僅在手機版執行
                if (window.innerWidth > 768) return;
                
                console.log('🔥 強制應用手機版樣式');
                
                // 1. 價值卡片（極速處理、超高準確率、性價比最高）
                const valueCards = document.querySelectorAll('.fade-in-up.delay-1, .fade-in-up.delay-2, .fade-in-up.delay-3');
                valueCards.forEach(card => {
                    card.style.padding = '1rem 1rem 0.5rem 1rem';
                    
                    // 修改圖標容器
                    const iconContainer = card.querySelector('div[style*="width: 80px"]');
                    if (iconContainer) {
                        iconContainer.style.marginBottom = '0.5rem';
                    }
                    
                    // 修改標題
                    const title = card.querySelector('h3');
                    if (title) {
                        title.style.marginBottom = '0.35rem';
                    }
                    
                    // 修改段落
                    const paragraph = card.querySelector('p');
                    if (paragraph) {
                        paragraph.style.marginBottom = '0';
                        paragraph.style.lineHeight = '1.5';
                    }
                });
                
                // 2. 功能組優化（手機版）- 使用更精確的選擇器
                const featureContainers = document.querySelectorAll('div[style*="border-radius: 24px"][style*="padding: 4rem"]');
                console.log(`🔍 找到 ${featureContainers.length} 個功能組容器`);
                
                featureContainers.forEach((container, index) => {
                    // 找到 grid 容器並改為垂直排列
                    const gridContainer = container.querySelector('div[style*="grid-template-columns"]');
                    if (gridContainer) {
                        gridContainer.style.display = 'flex';
                        gridContainer.style.flexDirection = 'column';
                        gridContainer.style.gap = '1rem';
                        console.log(`✅ 功能組 ${index + 1} grid 已改為垂直排列`);
                    }
                    
                    // 徽章置中（找到所有帶有 feature-badge 類的元素）
                    const badges = container.querySelectorAll('.feature-badge');
                    console.log(`  找到 ${badges.length} 個徽章`);
                    badges.forEach(badge => {
                        badge.style.setProperty('display', 'block', 'important');
                        badge.style.setProperty('text-align', 'center', 'important');
                        badge.style.setProperty('margin-left', 'auto', 'important');
                        badge.style.setProperty('margin-right', 'auto', 'important');
                        badge.style.setProperty('margin-bottom', '0.5rem', 'important');
                        badge.style.setProperty('width', 'fit-content', 'important');
                        badge.style.setProperty('font-size', '0.875rem', 'important'); // 恢復原始大小
                        badge.style.setProperty('padding', '0.5rem 1.5rem', 'important'); // 恢復原始內距
                    });
                    
                    // 標題置中
                    const titles = container.querySelectorAll('h2');
                    console.log(`  找到 ${titles.length} 個標題`);
                    titles.forEach(title => {
                        title.style.setProperty('text-align', 'center', 'important');
                        title.style.setProperty('margin-bottom', '0.75rem', 'important');
                    });
                    
                    // 減少所有 flex 容器的間距（OCR、智能分類、即時同步等）
                    const flexDivs = container.querySelectorAll('div[style*="display: flex"][style*="align-items: start"]');
                    console.log(`  找到 ${flexDivs.length} 個描述 flex 容器`);
                    flexDivs.forEach((div, divIndex) => {
                        // 所有描述段落間距都減少 30pt（再減小 10pt）
                        div.style.setProperty('margin-bottom', 'calc(1.5rem - 30pt)', 'important');
                    });
                    
                    console.log(`✅ 功能組 ${index + 1} 已優化完成`);
                });
                
                // 3. 卡片與上方文字間距減少 20pt
                const demoCards = document.querySelectorAll('.fade-in-right, .fade-in-left');
                console.log(`🔍 找到 ${demoCards.length} 個示例卡片`);
                demoCards.forEach((card, index) => {
                    if (card.style.position === 'relative' | card.querySelector('div[style*="position: relative"]')) {
                        card.style.setProperty('margin-top', '-20pt', 'important');
                        console.log(`✅ 卡片 ${index + 1} 已上移 20pt`);
                    }
                });
                
                console.log('✅ 手機版樣式已強制應用');
            }
            
            // 立即執行
            forceMobileStyles();
            
            // 窗口大小改變時重新檢查
            window.addEventListener('resize', forceMobileStyles);
        });
    

// --- Extracted Script Block 7 ---

    

// --- Extracted Script Block 8 ---

        // 數字滾動動畫函數
        function animateNumber(element, start, end, duration, suffix = '') {
            const startTime = performance.now();
            const range = end - start;
            
            function update(currentTime) {
                const elapsed = currentTime - startTime;
                const progress = Math.min(elapsed / duration, 1);
                
                // 使用 easeOutQuart 緩動函數
                const easeProgress = 1 - Math.pow(1 - progress, 4);
                const current = Math.floor(start + (range * easeProgress));
                
                element.textContent = current + suffix;
                
                if (progress < 1) {
                    requestAnimationFrame(update);
                } else {
                    element.textContent = end + suffix;
                }
            }
            
            requestAnimationFrame(update);
        }
        
        // 頁面加載後啟動數字動畫
        window.addEventListener('load', function() {
            setTimeout(() => {
                const speedEl = document.getElementById('stat-speed');
                const accuracyEl = document.getElementById('stat-accuracy');
                const clientsEl = document.getElementById('stat-clients');
                
                if (speedEl) animateNumber(speedEl, 0, 5, 2000);
                if (accuracyEl) animateNumber(accuracyEl, 0, 98, 2000);
                if (clientsEl) animateNumber(clientsEl, 0, 200, 2000);
            }, 300); // 延遲 300ms 開始動畫
        });
    

// --- Extracted Script Block 9 ---

        console.log('🔥 開始初始化漢堡菜單...');
        
        // 打開側邊欄函數
        function openSidebar() {
            console.log('🔵 打開側邊欄');
            const sidebar = document.getElementById('mobile-sidebar');
            const overlay = document.getElementById('mobile-sidebar-overlay');
            
            if (sidebar && overlay) {
                sidebar.style.left = '0';
                overlay.style.display = 'block';
                overlay.style.opacity = '1';
                document.body.style.overflow = 'hidden';
                console.log('✅ 側邊欄已打開');
            }
        }
        
        // 關閉側邊欄函數
        function closeSidebar() {
            console.log('🔵 關閉側邊欄');
            const sidebar = document.getElementById('mobile-sidebar');
            const overlay = document.getElementById('mobile-sidebar-overlay');
            
            if (sidebar && overlay) {
                sidebar.style.left = '-100%';
                overlay.style.opacity = '0';
                setTimeout(() => {
                    overlay.style.display = 'none';
                }, 300); // 等待動畫完成（與 CSS transition 一致）
                document.body.style.overflow = 'auto';
                console.log('✅ 側邊欄已關閉');
            }
        }
        
        // 超級簡單的初始化函數
        function simpleInitMenu() {
            const btn = document.getElementById('mobile-menu-btn');
            const overlay = document.getElementById('mobile-sidebar-overlay');
            
            if (!btn | !overlay) {
                console.log('⏳ 元素未找到，200ms後重試');
                setTimeout(simpleInitMenu, 200);
                return;
            }
            
            console.log('✅ 找到所有元素！');
            
            // 按鈕點擊處理
            btn.addEventListener('click', function() {
                console.log('🔵 按鈕被點擊！');
                openSidebar();
            });
            
            // 觸摸處理
            btn.addEventListener('touchend', function(e) {
                e.preventDefault();
                console.log('🔵 觸摸事件！');
                openSidebar();
            });
            
            // 遮罩點擊關閉
            overlay.addEventListener('click', function() {
                console.log('🔵 點擊遮罩關閉');
                closeSidebar();
            });
            
            // 遮罩觸摸關閉
            overlay.addEventListener('touchend', function(e) {
                e.preventDefault();
                console.log('🔵 觸摸遮罩關閉');
                closeSidebar();
            });
            
            console.log('✅ 所有事件監聽器已綁定');
        }
        
        // 立即嘗試初始化
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', simpleInitMenu);
        } else {
            setTimeout(simpleInitMenu, 100);
        }
        
        // 暴露函數供側邊欄內的連結使用
        window.closeMobileSidebar = closeSidebar;
    

// --- Extracted Script Block 10 ---

    function toggleChat() {
        const chatWindow = document.getElementById('chat-window');
        const button = document.getElementById('chat-button');
        
        if (chatWindow && button) {
            if (chatWindow.style.display === 'none' | !chatWindow.style.display) {
                chatWindow.style.display = 'flex';
                button.textContent = '✕';
                
                if (typeof gtag !== 'undefined') {
                    gtag('event', 'chat_opened', {
                        'event_category': 'engagement'
                    });
                }
            } else {
                chatWindow.style.display = 'none';
                button.textContent = '💬';
            }
        }
    }

    function sendQuickQuestion(question) {
        addUserMessage(question);
        
        setTimeout(() => {
            let answer = '';
            if (question.includes('價格')) {
                answer = '我們提供極具競爭力的價格：\n• 每頁低至：HK$0.3\n• 月付方案：HK$38起\n• 免費試用20頁，無需預約\n\n<a href="#pricing" style="color: #667eea; text-decoration: underline;">查看詳細價格</a>';
            } else if (question.includes('免費試用')) {
                answer = '很簡單！只需3步：\n1. 點擊「立即開始」註冊\n2. Google 登入即送 20 Credits\n3. 上傳文檔開始體驗\n\n<button onclick="openAuthModal()" style="background: #667eea; color: white; padding: 0.5rem 1rem; border: none; border-radius: 6px; cursor: pointer; text-decoration: none; display: inline-block;">立即註冊</button>';
            } else if (question.includes('銀行')) {
                answer = '我們支持所有主要銀行：\n• 香港：匯豐、恆生、中銀、渣打\n• 美國：Bank of America、Chase\n• 日本：三菱UFJ、みずほ\n• 韓國：국민은행、신한은행';
            } else if (question.includes('安全')) {
                answer = '您的數據安全是我們的首要任務：\n✅ 256位SSL加密\n✅ SOC 2認證\n✅ 銀行級安全標準\n✅ 365天數據保留\n\n完全安全可靠！';
            }
            
            addBotMessage(answer);
        }, 1000);
        
        if (typeof gtag !== 'undefined') {
            gtag('event', 'chat_question', {
                'event_category': 'engagement',
                'event_label': question
            });
        }
    }

    function addUserMessage(text) {
        const messages = document.getElementById('chat-messages');
        if (messages) {
            const div = document.createElement('div');
            div.style.cssText = 'margin-bottom: 1rem; display: flex; justify-content: flex-end;';
            div.innerHTML = `
                <div style="background: #667eea; color: white; padding: 0.75rem 1rem; border-radius: 12px; max-width: 70%; font-size: 0.9375rem;">
                    ${text}
                </div>
            `;
            messages.appendChild(div);
            messages.scrollTop = messages.scrollHeight;
        }
    }

    function addBotMessage(text) {
        const messages = document.getElementById('chat-messages');
        if (messages) {
            const div = document.createElement('div');
            div.style.cssText = 'margin-bottom: 1rem;';
            div.innerHTML = `
                <div style="background: white; padding: 1rem; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); font-size: 0.9375rem; color: #1f2937;">
                    ${text.replace(/\n/g, '<br>')}
                </div>
            `;
            messages.appendChild(div);
            messages.scrollTop = messages.scrollHeight;
        }
    }

    function sendChatMessage(e) {
        e.preventDefault();
        const input = document.getElementById('chat-input');
        if (input) {
            const message = input.value.trim();
            
            if (message) {
                addUserMessage(message);
                input.value = '';
                
                setTimeout(() => {
                    addBotMessage('感謝您的提問！我們的客服團隊會盡快回覆。您也可以：\n\n• <button onclick="openAuthModal()" style="background: transparent; color: #667eea; border: none; cursor: pointer; text-decoration: underline; padding: 0;">註冊免費試用</button>\n• <a href="blog/" style="color: #667eea;">查看幫助文檔</a>\n• 發送郵件至 vaultcaddy@gmail.com');
                }, 1000);
            }
        }
    }
    

// --- Extracted Script Block 11 ---

    // Exit Intent Detection
    let exitPopupShown = false;

    document.addEventListener('mouseleave', function(e) {
        // Modify condition to be less sensitive (clientY <= 0 means mouse actually left the top of the viewport)
        if (e.clientY <= 0 && !exitPopupShown && !localStorage.getItem('exitPopupShown')) {
            showExitPopup();
        }
    });

    function showExitPopup() {
        const popup = document.getElementById('exit-popup');
        if (popup) {
            popup.style.display = 'flex';
            exitPopupShown = true;
            localStorage.setItem('exitPopupShown', Date.now());
            
            if (typeof gtag !== 'undefined') {
                gtag('event', 'exit_intent_shown', {
                    'event_category': 'engagement'
                });
            }
        }
    }

    function closeExitPopup() {
        const popup = document.getElementById('exit-popup');
        if (popup) {
            popup.style.display = 'none';
        }
    }

    async function handleExitEmail(e) {
        e.preventDefault();
        const email = document.getElementById('exit-email').value;
        
        document.getElementById('exit-email-form').style.display = 'none';
        document.getElementById('exit-success').style.display = 'block';
        
        if (typeof gtag !== 'undefined') {
            gtag('event', 'exit_email_captured', {
                'event_category': 'lead_generation',
                'event_label': email
            });
        }
        
        if (typeof fbq !== 'undefined') {
            fbq('track', 'Lead');
        }
        
        setTimeout(() => {
            closeExitPopup();
            window.location.href = 'auth.html?discount=EXIT20';
        }, 3000);
    }

    const popupTime = localStorage.getItem('exitPopupShown');
    if (popupTime && (Date.now() - popupTime > 24 * 60 * 60 * 1000)) {
        localStorage.removeItem('exitPopupShown');
    }
    

// --- Extracted Script Block 12 ---

        // 增强滚动动画效果
        document.addEventListener('DOMContentLoaded', function() {
            // 数字计数动画
            const animateNumbers = () => {
                const stats = [
                    { id: 'stat-speed', target: 5, suffix: '' },
                    { id: 'stat-accuracy', target: 98, suffix: '' },
                    { id: 'stat-clients', target: 200, suffix: '' }
                ];
                
                stats.forEach(stat => {
                    const element = document.getElementById(stat.id);
                    if (!element) return;
                    
                    let current = 0;
                    const increment = stat.target / 50;
                    const timer = setInterval(() => {
                        current += increment;
                        if (current >= stat.target) {
                            current = stat.target;
                            clearInterval(timer);
                        }
                        element.textContent = Math.floor(current);
                    }, 30);
                });
            };
            
            // 检查元素是否在视口中
            const isInViewport = (element) => {
                const rect = element.getBoundingClientRect();
                return rect.top < window.innerHeight && rect.bottom > 0;
            };
            
            // 当滚动到统计数字时触发动画
            let numbersAnimated = false;
            window.addEventListener('scroll', () => {
                const heroSection = document.querySelector('main section');
                if (!numbersAnimated && heroSection && isInViewport(heroSection)) {
                    animateNumbers();
                    numbersAnimated = true;
                }
            });
            
            // 頁面加载时如果已经在视口中，立即触发
            const heroSection = document.querySelector('main section');
            if (heroSection && isInViewport(heroSection)) {
                animateNumbers();
                numbersAnimated = true;
            }
        });
    

// --- Extracted Script Block 13 ---

        // 全局變量：當前選擇的文檔類型
        let selectedDocType = 'statement'; // 默認為銀行對帳單
        
        // 選擇文檔類型
        window.selectDocType = function(type) {
            selectedDocType = type;
            console.log('✅ 選擇文檔類型:', type);
            
            // 更新按鈕樣式
            const statementBtn = document.getElementById('doc-type-statement');
            const invoiceBtn = document.getElementById('doc-type-invoice');
            
            if (type === 'statement') {
                // 銀行對帳單按鈕變為激活狀態
                statementBtn.style.background = '#667eea';
                statementBtn.style.color = 'white';
                invoiceBtn.style.background = 'white';
                invoiceBtn.style.color = '#667eea';
            } else {
                // 發票按鈕變為激活狀態
                invoiceBtn.style.background = '#667eea';
                invoiceBtn.style.color = 'white';
                statementBtn.style.background = 'white';
                statementBtn.style.color = '#667eea';
            }
        };
        
        // ============================================
        // 📦 IndexedDB 文件存儲（用於跨頁面傳遞文件）
        // ============================================
        const FileStorage = {
            dbName: 'VaultCaddyFiles',
            storeName: 'pendingFiles',
            db: null,
            
            // 初始化數據庫
            async init() {
                return new Promise((resolve, reject) => {
                    const request = indexedDB.open(this.dbName, 1);
                    
                    request.onerror = () => reject(request.error);
                    request.onsuccess = () => {
                        this.db = request.result;
                        resolve(this.db);
                    };
                    
                    request.onupgradeneeded = (event) => {
                        const db = event.target.result;
                        if (!db.objectStoreNames.contains(this.storeName)) {
                            db.createObjectStore(this.storeName);
                        }
                    };
                });
            },
            
            // 保存文件
            async saveFiles(files) {
                if (!this.db) await this.init();
                
                return new Promise((resolve, reject) => {
                    const transaction = this.db.transaction([this.storeName], 'readwrite');
                    const store = transaction.objectStore(this.storeName);
                    
                    // 保存文件數組
                    const request = store.put(Array.from(files), 'pendingFiles');
                    
                    request.onsuccess = () => {
                        console.log('✅ 文件已保存到 IndexedDB');
                        resolve();
                    };
                    request.onerror = () => reject(request.error);
                });
            },
            
            // 獲取文件
            async getFiles() {
                if (!this.db) await this.init();
                
                return new Promise((resolve, reject) => {
                    const transaction = this.db.transaction([this.storeName], 'readonly');
                    const store = transaction.objectStore(this.storeName);
                    const request = store.get('pendingFiles');
                    
                    request.onsuccess = () => {
                        resolve(request.result || []);
                    };
                    request.onerror = () => reject(request.error);
                });
            },
            
            // 清除文件
            async clearFiles() {
                if (!this.db) await this.init();
                
                return new Promise((resolve, reject) => {
                    const transaction = this.db.transaction([this.storeName], 'readwrite');
                    const store = transaction.objectStore(this.storeName);
                    const request = store.delete('pendingFiles');
                    
                    request.onsuccess = () => {
                        console.log('✅ 文件已從 IndexedDB 清除');
                        resolve();
                    };
                    request.onerror = () => reject(request.error);
                });
            }
        };
        
        // 初始化上傳區域
        (function() {
            const dropzone = document.getElementById('dropzone');
            const fileInput = document.getElementById('file-input');
            
            if (!dropzone || !fileInput) {
                console.log('⏭️ 上傳區域未找到，跳過初始化');
                return;
            }
            
            console.log('✅ 初始化首頁上傳功能');
            
            // 點擊上傳
            dropzone.addEventListener('click', () => {
                fileInput.click();
            });
            
            // 文件選擇
            fileInput.addEventListener('change', (e) => {
                handleFiles(e.target.files);
            });
            
            // 拖放事件
            dropzone.addEventListener('dragover', (e) => {
                e.preventDefault();
                dropzone.style.borderColor = '#764ba2';
                dropzone.style.background = 'rgba(102, 126, 234, 0.15)';
                dropzone.style.transform = 'scale(1.02)';
            });
            
            dropzone.addEventListener('dragleave', (e) => {
                e.preventDefault();
                dropzone.style.borderColor = '#667eea';
                dropzone.style.background = 'rgba(102, 126, 234, 0.05)';
                dropzone.style.transform = 'scale(1)';
            });
            
            dropzone.addEventListener('drop', (e) => {
                e.preventDefault();
                dropzone.style.borderColor = '#667eea';
                dropzone.style.background = 'rgba(102, 126, 234, 0.05)';
                dropzone.style.transform = 'scale(1)';
                handleFiles(e.dataTransfer.files);
            });
            
            // 處理文件
            function handleFiles(files) {
                if (!files || files.length === 0) return;
                
                console.log(`📁 用戶拖入 ${files.length} 個文件`);
                console.log(`📋 文檔類型: ${selectedDocType === 'statement' ? '銀行對帳單' : '發票'}`);
                
                // ✅ 檢查文件大小（20MB限制）
                const MAX_FILE_SIZE = 20 * 1024 * 1024; // 20MB
                const filesArray = Array.from(files);
                const oversizedFiles = filesArray.filter(f => f.size > MAX_FILE_SIZE);
                
                if (oversizedFiles.length > 0) {
                    const fileNames = oversizedFiles.map(f => `${f.name} (${(f.size / 1024 / 1024).toFixed(2)}MB)`).join('\n');
                    showToast(`以下文件超過 20MB 限制：\n${fileNames}`);
                    console.error('❌ 文件大小超過限制:', oversizedFiles);
                    return;
                }
                
                // 檢查用戶是否已登入
                const isLoggedIn = window.simpleAuth && window.simpleAuth.isLoggedIn();
                
                if (!isLoggedIn) {
                    // 未登入：保存文件到 IndexedDB 和文檔類型
                    FileStorage.saveFiles(filesArray).then(() => {
                        localStorage.setItem('pendingFileCount', files.length);
                        localStorage.setItem('pendingDocType', selectedDocType); // 保存文檔類型
                        localStorage.setItem('hasPendingFiles', 'true'); // 標記有待處理文件
                        
                        console.log('ℹ️ 用戶未登入，保存文件到 IndexedDB');
                        
                        // 顯示提示
                        const docTypeName = selectedDocType === 'statement' ? '銀行對帳單' : '發票';
                        showToast(`已選擇 ${files.length} 個${docTypeName}文件，請先登入以開始處理`);
                        
                        // 彈出登入框
                        setTimeout(() => {
                            if (typeof openAuthModal === 'function') {
                                openAuthModal();
                            } else {
                                console.error('❌ openAuthModal 函數未定義');
                                window.location.href = 'auth.html';
                            }
                        }, 300);
                    }).catch(error => {
                        console.error('❌ 保存文件失敗:', error);
                        showToast('保存文件失敗，請重試');
                    });
                } else {
                    // 已登入：保存文件到 IndexedDB 並跳轉
                    console.log('✅ 用戶已登入，準備查找或創建 First_Project');
                    
                    FileStorage.saveFiles(filesArray).then(() => {
                        localStorage.setItem('hasPendingFiles', 'true'); // 標記有待處理文件
                        findOrCreateFirstProject();
                    }).catch(error => {
                        console.error('❌ 保存文件失敗:', error);
                        showToast('保存文件失敗，請重試');
                    });
                }
            }
            
            // ✅ 查找或創建 First_Project 文件夾
            async function findOrCreateFirstProject() {
                try {
                    showToast('正在準備項目...');
                    
                    // 獲取所有項目
                    const projects = await window.simpleDataManager.getProjects();
                    console.log('📂 獲取到項目列表:', projects);
                    
                    // 查找 First_Project
                    let firstProject = projects.find(p => p.name === 'First_Project');
                    
                    if (firstProject) {
                        console.log('✅ 找到現有的 First_Project:', firstProject.id);
                    } else {
                        // 創建新的 First_Project
                        console.log('📁 創建新的 First_Project');
                        firstProject = await window.simpleDataManager.createProject('First_Project');
                        console.log('✅ First_Project 創建成功:', firstProject.id);
                    }
                    
                    // 保存文檔類型和提示信息
                    const docTypeName = selectedDocType === 'statement' ? '銀行對帳單' : '發票';
                    sessionStorage.setItem('uploadHint', `請在此頁面上傳您的${docTypeName}文件`);
                    sessionStorage.setItem('selectedDocType', selectedDocType);
                    sessionStorage.setItem('autoUpload', 'true'); // 標記需要自動觸發上傳
                    
                    // 跳轉到 First_Project
                    showToast('項目準備完成！正在跳轉...');
                    setTimeout(() => {
                        window.location.href = `firstproject.html?project=${firstProject.id}`;
                    }, 500);
                    
                } catch (error) {
                    console.error('❌ 查找或創建 First_Project 失敗:', error);
                    showToast(`錯誤：${error.message || '無法創建項目'}`);
                }
            }
            
            // Toast 提示
            function showToast(message) {
                const toast = document.createElement('div');
                toast.textContent = message;
                toast.style.cssText = 'position: fixed; bottom: 2rem; left: 50%; transform: translateX(-50%); background: #1f2937; color: white; padding: 1rem 2rem; border-radius: 8px; z-index: 10000; box-shadow: 0 4px 12px rgba(0,0,0,0.3); font-size: 0.95rem; max-width: 90%; text-align: center;';
                document.body.appendChild(toast);
                setTimeout(() => {
                    toast.style.opacity = '0';
                    toast.style.transition = 'opacity 0.3s ease';
                    setTimeout(() => toast.remove(), 300);
                }, 3000);
            }
            
            // 處理待上傳文件的函數（統一邏輯）
            async function processPendingFiles() {
                const hasPendingFiles = localStorage.getItem('hasPendingFiles');
                const pendingCount = localStorage.getItem('pendingFileCount');
                const pendingDocType = localStorage.getItem('pendingDocType');
                
                if (!hasPendingFiles || !pendingCount || !pendingDocType) {
                    console.log('⏭️ 沒有待處理的文件');
                    return false;
                }
                
                // 檢查用戶是否已登入
                const isLoggedIn = window.simpleAuth && window.simpleAuth.isLoggedIn();
                if (!isLoggedIn) {
                    console.log('⏳ 有待處理文件，但用戶尚未登入');
                    return false;
                }
                
                const docTypeName = pendingDocType === 'statement' ? '銀行對帳單' : '發票';
                console.log(`✅ 檢測到 ${pendingCount} 個待處理的${docTypeName}文件`);
                
                // 保存文檔類型到 sessionStorage
                sessionStorage.setItem('selectedDocType', pendingDocType);
                selectedDocType = pendingDocType;
                
                // 顯示提示
                showToast('正在準備項目...');
                
                // 調用查找或創建 First_Project
                setTimeout(() => {
                    findOrCreateFirstProject();
                }, 500);
                
                return true;
            }
            
            // 監聽登入成功事件
            window.addEventListener('user-logged-in', async () => {
                console.log('🔔 收到 user-logged-in 事件');
                await processPendingFiles();
            });
            
            // ✅ 頁面加載時檢查是否有待處理文件（用戶可能刷新了頁面）
            window.addEventListener('DOMContentLoaded', async () => {
                // 等待 simpleAuth 初始化
                setTimeout(async () => {
                    const processed = await processPendingFiles();
                    if (processed) {
                        console.log('✅ 頁面加載時處理了待上傳文件');
                    }
                }, 1000);
            });
            
            // ✅ 如果頁面已經加載完成，立即檢查
            if (document.readyState === 'complete' || document.readyState === 'interactive') {
                setTimeout(async () => {
                    const processed = await processPendingFiles();
                    if (processed) {
                        console.log('✅ 立即處理了待上傳文件');
                    }
                }, 1000);
            }
        })();
    

// --- Extracted Script Block 14 ---

        // 打開登入彈窗
        function openAuthModal() {
            const modal = document.getElementById('auth-modal');
            if (modal) {
                modal.style.display = 'flex';
                document.body.style.overflow = 'hidden'; // 防止背景滾動
                
                // Google Analytics 追蹤
                if (typeof gtag !== 'undefined') {
                    gtag('event', 'open_auth_modal', {
                        event_category: 'engagement',
                        event_label: 'Auth Modal Opened'
                    });
                }
            }
        }
        
        // 關閉登入彈窗
        function closeAuthModal() {
            const modal = document.getElementById('auth-modal');
            if (modal) {
                modal.style.display = 'none';
                document.body.style.overflow = ''; // 恢復背景滾動
            }
        }
        
        // 點擊背景關閉彈窗
        document.getElementById('auth-modal')?.addEventListener('click', function(e) {
            if (e.target === this) {
                closeAuthModal();
            }
        });
        
        // ESC 鍵關閉彈窗
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                closeAuthModal();
            }
        });
        
        // Google 登入（彈窗版本）
        async function signInWithGoogleModal() {
            const btn = document.getElementById('modal-google-signin-btn');
            if (!btn) return;
            
            // 顯示載入狀態
            const originalText = btn.innerHTML;
            btn.disabled = true;
            btn.style.opacity = '0.6';
            btn.innerHTML = '<span style="display: inline-block; width: 20px; height: 20px; border: 3px solid rgba(255,255,255,0.3); border-top-color: white; border-radius: 50%; animation: spin 0.6s linear infinite;"></span> 登入中...';
            
            try {
                // 檢查 Firebase 和 simpleAuth 是否已載入
                if (typeof firebase === 'undefined' || !window.simpleAuth) {
                    throw new Error('Firebase 尚未載入，請稍後再試');
                }
                
                // 調用 simpleAuth 的 Google 登入（正確的方法名是 loginWithGoogle）
                await window.simpleAuth.loginWithGoogle();
                
                // 登入成功，關閉彈窗
                closeAuthModal();
                
                // ✅ 不刷新頁面，讓 user-logged-in 事件自然觸發
                // 如果有待處理的文件，會自動跳轉
                console.log('✅ 登入成功，等待 user-logged-in 事件處理待上傳文件...');
                
            } catch (error) {
                console.error('❌ Google 登入失敗:', error);
                
                // 顯示錯誤提示
                alert('登入失敗：' + (error.message || '未知錯誤'));
                
                // 恢復按鈕狀態
                btn.disabled = false;
                btn.style.opacity = '1';
                btn.innerHTML = originalText;
            }
        }
        
        // 添加旋轉動畫
        const style = document.createElement('style');
        style.textContent = '@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }';
        document.head.appendChild(style);
    

