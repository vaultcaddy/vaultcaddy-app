/**
 * ============================================
 * 🌐 VaultCaddy 多语言数据互通系统
 * ============================================
 * 作用：
 * 1. 保存和同步用户的语言偏好到 Firebase
 * 2. 自动跳转到用户偏好的语言版本
 * 3. 提供语言切换功能
 * 4. 确保所有语言版本访问相同的数据
 * 
 * 使用方法：
 * 1. 在所有页面的 <head> 中引入此脚本
 * 2. 在页面中添加语言切换器容器：<div id="language-switcher"></div>
 * 
 * @version 1.0.0
 * @date 2025-12-21
 * ============================================
 */

(function() {
    'use strict';
    
    console.log('🌐 multilingual-data-sync.js 加載');
    
    // ============================================
    // 语言配置
    // ============================================
    const LANGUAGES = {
        'zh': {
            code: 'zh',
            name: '中文',
            nativeName: '中文',
            flag: '🇨🇳',
            path: '/',
            domain: 'vaultcaddy.com'
        },
        'en': {
            code: 'en',
            name: 'English',
            nativeName: 'English',
            flag: '🇺🇸',
            path: '/en/',
            domain: 'vaultcaddy.com/en'
        },
        'jp': {
            code: 'jp',
            name: 'Japanese',
            nativeName: '日本語',
            flag: '🇯🇵',
            path: '/jp/',
            domain: 'vaultcaddy.com/jp'
        },
        'kr': {
            code: 'kr',
            name: 'Korean',
            nativeName: '한국어',
            flag: '🇰🇷',
            path: '/kr/',
            domain: 'vaultcaddy.com/kr'
        }
    };
    
    // ============================================
    // 核心功能类
    // ============================================
    class MultilingualDataSync {
        constructor() {
            this.currentLang = this.detectCurrentLanguage();
            this.initialized = false;
            console.log('🌐 当前语言:', this.currentLang);
        }
        
        /**
         * 检测当前页面的语言
         */
        detectCurrentLanguage() {
            const path = window.location.pathname;
            
            if (path.startsWith('/en/')) return 'en';
            if (path.startsWith('/jp/')) return 'jp';
            if (path.startsWith('/kr/')) return 'kr';
            return 'zh';
        }
        
        /**
         * 获取用户的语言偏好
         * 优先级: Firebase > LocalStorage > 浏览器语言 > 默认中文
         */
        async getUserLanguagePreference() {
            try {
                // 1. 尝试从 Firebase 获取
                if (window.simpleAuth && window.simpleAuth.isLoggedIn()) {
                    const db = window.getFirestore();
                    if (db) {
                        const user = window.simpleAuth.getCurrentUser();
                        const userDoc = await db.collection('users').doc(user.uid).get();
                        
                        if (userDoc.exists && userDoc.data().preferredLanguage) {
                            const lang = userDoc.data().preferredLanguage;
                            console.log('✅ 从 Firebase 获取语言偏好:', lang);
                            return lang;
                        }
                    }
                }
                
                // 2. 尝试从 LocalStorage 获取
                const localLang = localStorage.getItem('vaultcaddy_language');
                if (localLang && LANGUAGES[localLang]) {
                    console.log('✅ 从 LocalStorage 获取语言偏好:', localLang);
                    return localLang;
                }
                
                // 3. 尝试从浏览器语言检测
                const browserLang = navigator.language || navigator.userLanguage;
                if (browserLang.startsWith('zh')) return 'zh';
                if (browserLang.startsWith('en')) return 'en';
                if (browserLang.startsWith('ja')) return 'jp';
                if (browserLang.startsWith('ko')) return 'kr';
                
                // 4. 默认返回中文
                return 'zh';
            } catch (error) {
                console.warn('⚠️ 获取语言偏好失败:', error);
                return 'zh';
            }
        }
        
        /**
         * 保存用户的语言偏好
         */
        async saveLanguagePreference(lang) {
            try {
                // 1. 保存到 LocalStorage
                localStorage.setItem('vaultcaddy_language', lang);
                console.log('✅ 保存语言偏好到 LocalStorage:', lang);
                
                // 2. 如果用户已登录，保存到 Firebase
                if (window.simpleAuth && window.simpleAuth.isLoggedIn()) {
                    const db = window.getFirestore();
                    if (db) {
                        const user = window.simpleAuth.getCurrentUser();
                        await db.collection('users').doc(user.uid).update({
                            preferredLanguage: lang,
                            languageUpdatedAt: firebase.firestore.FieldValue.serverTimestamp()
                        });
                        console.log('✅ 保存语言偏好到 Firebase:', lang);
                    }
                }
                
                return true;
            } catch (error) {
                console.error('❌ 保存语言偏好失败:', error);
                return false;
            }
        }
        
        /**
         * 切换到指定语言
         */
        async switchLanguage(targetLang) {
            if (!LANGUAGES[targetLang]) {
                console.error('❌ 不支持的语言:', targetLang);
                return;
            }
            
            // 保存语言偏好
            await this.saveLanguagePreference(targetLang);
            
            // 构建目标URL
            const currentPath = window.location.pathname;
            const currentSearch = window.location.search;
            const currentHash = window.location.hash;
            
            // 移除当前语言前缀
            let cleanPath = currentPath;
            for (const lang in LANGUAGES) {
                if (currentPath.startsWith(LANGUAGES[lang].path) && lang !== 'zh') {
                    cleanPath = currentPath.substring(LANGUAGES[lang].path.length - 1);
                    break;
                }
            }
            
            // 添加目标语言前缀
            let targetPath;
            if (targetLang === 'zh') {
                targetPath = cleanPath;
            } else {
                targetPath = LANGUAGES[targetLang].path + cleanPath.substring(1);
            }
            
            // 跳转
            const targetUrl = targetPath + currentSearch + currentHash;
            console.log('🌐 切换语言到:', targetLang, '目标URL:', targetUrl);
            window.location.href = targetUrl;
        }
        
        /**
         * 获取当前页面在其他语言版本的URL
         */
        getUrlForLanguage(lang) {
            if (!LANGUAGES[lang]) return null;
            
            const currentPath = window.location.pathname;
            const currentSearch = window.location.search;
            const currentHash = window.location.hash;
            
            // 移除当前语言前缀
            let cleanPath = currentPath;
            for (const l in LANGUAGES) {
                if (currentPath.startsWith(LANGUAGES[l].path) && l !== 'zh') {
                    cleanPath = currentPath.substring(LANGUAGES[l].path.length - 1);
                    break;
                }
            }
            
            // 添加目标语言前缀
            let targetPath;
            if (lang === 'zh') {
                targetPath = cleanPath;
            } else {
                targetPath = LANGUAGES[lang].path + cleanPath.substring(1);
            }
            
            return targetPath + currentSearch + currentHash;
        }
        
        /**
         * 创建语言切换器UI
         */
        createLanguageSwitcher() {
            const container = document.getElementById('language-switcher');
            if (!container) {
                console.warn('⚠️ 找不到 language-switcher 容器');
                return;
            }
            
            // 创建下拉菜单
            const currentLangConfig = LANGUAGES[this.currentLang];
            
            container.innerHTML = `
                <div style="position: relative; display: inline-block;">
                    <button id="lang-button" onclick="window.multilingualSync.toggleLanguageDropdown()" 
                            style="display: flex; align-items: center; gap: 0.5rem; padding: 0.375rem 0.875rem; 
                                   background: white; border: 1px solid #e5e7eb; border-radius: 6px; 
                                   cursor: pointer; font-size: 0.875rem; transition: all 0.2s;
                                   box-shadow: 0 1px 3px rgba(0,0,0,0.1);"
                            onmouseover="this.style.borderColor='#8b5cf6'; this.style.boxShadow='0 2px 6px rgba(139,92,246,0.2)'"
                            onmouseout="this.style.borderColor='#e5e7eb'; this.style.boxShadow='0 1px 3px rgba(0,0,0,0.1)'">
                        <span style="font-weight: 500; color: #374151;">${currentLangConfig.nativeName}</span>
                        <svg style="width: 1rem; height: 1rem; color: #6b7280;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                        </svg>
                    </button>
                    
                    <div id="lang-dropdown" 
                         style="display: none; position: absolute; top: calc(100% + 0.5rem); right: 0; 
                                background: white; border: 1px solid #e5e7eb; border-radius: 8px; 
                                box-shadow: 0 4px 12px rgba(0,0,0,0.15); min-width: 180px; z-index: 1000;
                                overflow: hidden;">
                        ${Object.entries(LANGUAGES).map(([code, config]) => `
                            <a href="#" onclick="event.preventDefault(); window.multilingualSync.switchLanguage('${code}')"
                               style="display: flex; align-items: center; padding: 0.625rem 1rem; 
                                      color: ${code === this.currentLang ? '#8b5cf6' : '#374151'}; 
                                      background: ${code === this.currentLang ? '#f5f3ff' : 'white'};
                                      text-decoration: none; transition: background 0.2s;
                                      border-left: 3px solid ${code === this.currentLang ? '#8b5cf6' : 'transparent'};"
                               onmouseover="if ('${code}' !== '${this.currentLang}') this.style.background='#f9fafb'"
                               onmouseout="if ('${code}' !== '${this.currentLang}') this.style.background='white'">
                                <div style="flex: 1;">
                                    <div style="font-weight: ${code === this.currentLang ? '600' : '500'};">
                                        ${config.nativeName}
                                    </div>
                                    <div style="font-size: 0.75rem; color: #6b7280;">
                                        ${config.name}
                                    </div>
                                </div>
                                ${code === this.currentLang ? '<span style="color: #8b5cf6;">✓</span>' : ''}
                            </a>
                        `).join('')}
                    </div>
                </div>
            `;
            
            // 点击外部关闭下拉菜单
            document.addEventListener('click', (event) => {
                const langButton = document.getElementById('lang-button');
                const langDropdown = document.getElementById('lang-dropdown');
                
                if (langButton && langDropdown) {
                    if (!langButton.contains(event.target) && !langDropdown.contains(event.target)) {
                        langDropdown.style.display = 'none';
                    }
                }
            });
            
            console.log('✅ 语言切换器已创建');
        }
        
        /**
         * 切换语言下拉菜单
         */
        toggleLanguageDropdown() {
            const dropdown = document.getElementById('lang-dropdown');
            if (dropdown) {
                dropdown.style.display = dropdown.style.display === 'none' ? 'block' : 'none';
            }
        }
        
        /**
         * 自动跳转到用户偏好的语言版本（仅在首页）
         */
        async autoRedirectToPreferredLanguage() {
            // 只在根路径（首页）执行自动跳转
            if (window.location.pathname !== '/' && window.location.pathname !== '/index.html') {
                return;
            }
            
            // 检查是否有明确的语言选择（URL参数）
            const urlParams = new URLSearchParams(window.location.search);
            if (urlParams.has('lang')) {
                const lang = urlParams.get('lang');
                if (LANGUAGES[lang]) {
                    await this.saveLanguagePreference(lang);
                    return;
                }
            }
            
            // 获取用户偏好语言
            const preferredLang = await this.getUserLanguagePreference();
            
            // 如果偏好语言与当前语言不同，执行跳转
            if (preferredLang !== this.currentLang && preferredLang !== 'zh') {
                console.log('🌐 自动跳转到偏好语言:', preferredLang);
                const targetUrl = LANGUAGES[preferredLang].path + 'index.html';
                window.location.href = targetUrl;
            }
        }
        
        /**
         * 初始化
         */
        async initialize() {
            if (this.initialized) return;
            
            console.log('🌐 初始化多语言数据互通系统...');
            
            // 创建语言切换器
            this.createLanguageSwitcher();
            
            // 在首页执行自动跳转（可选，根据需求开启）
            // await this.autoRedirectToPreferredLanguage();
            
            this.initialized = true;
            console.log('✅ 多语言数据互通系统初始化完成');
            
            // 触发自定义事件
            window.dispatchEvent(new CustomEvent('multilingual-ready', {
                detail: { currentLang: this.currentLang }
            }));
        }
    }
    
    // ============================================
    // 全局暴露
    // ============================================
    window.MultilingualDataSync = MultilingualDataSync;
    window.multilingualSync = new MultilingualDataSync();
    window.LANGUAGES = LANGUAGES;
    
    // ============================================
    // 自动初始化
    // ============================================
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            window.multilingualSync.initialize();
        });
    } else {
        window.multilingualSync.initialize();
    }
    
    console.log('✅ multilingual-data-sync.js 加载完成');
})();

