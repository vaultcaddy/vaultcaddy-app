/**
 * Google Analytics 事件跟踪系统
 * 
 * 本文件自动跟踪用户行为，用于优化转化率和用户体验
 * 
 * 跟踪的关键事件:
 * 1. GIF演示观看
 * 2. PDF上传
 * 3. 转换完成
 * 4. CTA点击
 * 5. 滚动深度
 * 6. Free Trial Banner点击
 * 7. 页面停留时间
 * 
 * @author VaultCaddy Team
 * @version 2.0
 * @date 2025-12-30
 */

(function() {
    'use strict';
    
    console.log('🔍 GA Event Tracking initialized');
    
    // 检查GA是否已加载
    function isGALoaded() {
        return typeof gtag !== 'undefined' || typeof ga !== 'undefined' || typeof window.dataLayer !== 'undefined';
    }
    
    // 发送事件到GA
    function trackEvent(eventName, eventParams = {}) {
        try {
            if (typeof gtag !== 'undefined') {
                // GA4
                gtag('event', eventName, eventParams);
                console.log('✅ GA Event:', eventName, eventParams);
            } else if (typeof ga !== 'undefined') {
                // Universal Analytics (旧版)
                ga('send', 'event', eventParams.event_category || 'engagement', eventName, eventParams.event_label || '');
                console.log('✅ GA Event (UA):', eventName, eventParams);
            } else {
                console.warn('⚠️ Google Analytics未加载');
            }
        } catch (error) {
            console.error('❌ GA跟踪错误:', error);
        }
    }
    
    // ============================================
    // 1. GIF演示观看跟踪 ⭐⭐⭐⭐⭐
    // ============================================
    function trackGIFViews() {
        const gifElements = document.querySelectorAll('img[src*="chase-bank-demo.gif"], img[src*="demo.gif"]');
        
        if (gifElements.length === 0) return;
        
        const gifObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && !entry.target.dataset.tracked) {
                    entry.target.dataset.tracked = 'true';
                    trackEvent('gif_view', {
                        'event_category': 'engagement',
                        'event_label': window.location.pathname,
                        'value': 1
                    });
                }
            });
        }, {
            threshold: 0.5 // 50%可见时触发
        });
        
        gifElements.forEach(gif => {
            gifObserver.observe(gif);
        });
        
        console.log('✅ GIF观看跟踪已启用');
    }
    
    // ============================================
    // 2. PDF上传跟踪 ⭐⭐⭐⭐⭐
    // ============================================
    function trackPDFUploads() {
        // 查找所有可能的文件上传输入框
        const fileInputs = document.querySelectorAll('input[type="file"]');
        
        fileInputs.forEach(input => {
            input.addEventListener('change', function(e) {
                if (e.target.files.length > 0) {
                    const fileCount = e.target.files.length;
                    const firstFile = e.target.files[0];
                    
                    trackEvent('pdf_upload', {
                        'event_category': 'conversion',
                        'event_label': 'file_selected',
                        'value': fileCount,
                        'file_type': firstFile.type,
                        'file_size_mb': (firstFile.size / 1024 / 1024).toFixed(2)
                    });
                }
            });
        });
        
        console.log('✅ PDF上传跟踪已启用');
    }
    
    // ============================================
    // 3. 转换完成跟踪 ⭐⭐⭐⭐⭐
    // ============================================
    window.trackConversionComplete = function(processingTime, pageCount) {
        trackEvent('conversion_complete', {
            'event_category': 'conversion',
            'event_label': 'success',
            'value': pageCount,
            'processing_time_seconds': processingTime
        });
    };
    
    // ============================================
    // 4. CTA点击跟踪 ⭐⭐⭐⭐⭐
    // ============================================
    function trackCTAClicks() {
        // 跟踪注册和登录按钮
        const ctaButtons = document.querySelectorAll(
            'a[href*="signup"], a[href*="register"], ' +
            'a[href*="login"], a[href*="signin"], ' +
            'button[onclick*="signup"], button[onclick*="register"], ' +
            '.btn-primary, .cta-button, .free-trial-button'
        );
        
        ctaButtons.forEach(btn => {
            btn.addEventListener('click', function() {
                const buttonText = this.textContent.trim();
                const buttonHref = this.href || '';
                
                trackEvent('cta_click', {
                    'event_category': 'engagement',
                    'event_label': buttonText,
                    'button_href': buttonHref
                });
            });
        });
        
        console.log(`✅ CTA点击跟踪已启用 (${ctaButtons.length}个按钮)`);
    }
    
    // ============================================
    // 5. Free Trial Banner点击跟踪 ⭐⭐⭐⭐⭐
    // ============================================
    function trackFreeTrialBannerClicks() {
        const banners = document.querySelectorAll('.free-trial-banner-container, [href*="signup"]');
        
        banners.forEach(banner => {
            banner.addEventListener('click', function() {
                trackEvent('free_trial_banner_click', {
                    'event_category': 'conversion',
                    'event_label': 'sticky_banner',
                    'page': window.location.pathname
                });
            });
        });
        
        console.log('✅ Free Trial Banner点击跟踪已启用');
    }
    
    // ============================================
    // 6. 滚动深度跟踪 ⭐⭐⭐⭐
    // ============================================
    function trackScrollDepth() {
        let maxScrollDepth = 0;
        let scrollCheckpoints = [25, 50, 75, 90, 100];
        let trackedCheckpoints = new Set();
        
        function checkScrollDepth() {
            const windowHeight = window.innerHeight;
            const documentHeight = document.documentElement.scrollHeight;
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            
            const scrollPercent = Math.round((scrollTop + windowHeight) / documentHeight * 100);
            
            if (scrollPercent > maxScrollDepth) {
                maxScrollDepth = scrollPercent;
                
                // 检查是否达到checkpoint
                scrollCheckpoints.forEach(checkpoint => {
                    if (scrollPercent >= checkpoint && !trackedCheckpoints.has(checkpoint)) {
                        trackedCheckpoints.add(checkpoint);
                        trackEvent('scroll_depth', {
                            'event_category': 'engagement',
                            'event_label': `${checkpoint}%`,
                            'value': checkpoint
                        });
                    }
                });
            }
        }
        
        // 使用throttle避免频繁触发
        let scrollTimeout;
        window.addEventListener('scroll', function() {
            if (scrollTimeout) {
                clearTimeout(scrollTimeout);
            }
            scrollTimeout = setTimeout(checkScrollDepth, 200);
        }, { passive: true });
        
        console.log('✅ 滚动深度跟踪已启用');
    }
    
    // ============================================
    // 7. 页面停留时间跟踪 ⭐⭐⭐⭐
    // ============================================
    function trackTimeOnPage() {
        const startTime = Date.now();
        
        // 在用户离开前记录停留时间
        window.addEventListener('beforeunload', function() {
            const timeOnPage = Math.round((Date.now() - startTime) / 1000); // 秒
            
            if (timeOnPage > 5) { // 至少5秒才跟踪
                trackEvent('time_on_page', {
                    'event_category': 'engagement',
                    'event_label': window.location.pathname,
                    'value': timeOnPage
                });
            }
        });
        
        console.log('✅ 页面停留时间跟踪已启用');
    }
    
    // ============================================
    // 8. 出站链接点击跟踪 ⭐⭐⭐
    // ============================================
    function trackOutboundLinks() {
        document.addEventListener('click', function(e) {
            const link = e.target.closest('a');
            if (!link) return;
            
            const href = link.href;
            if (href && !href.includes(window.location.hostname)) {
                trackEvent('outbound_click', {
                    'event_category': 'engagement',
                    'event_label': href,
                    'link_text': link.textContent.trim()
                });
            }
        });
        
        console.log('✅ 出站链接跟踪已启用');
    }
    
    // ============================================
    // 9. 表单交互跟踪 ⭐⭐⭐⭐
    // ============================================
    function trackFormInteractions() {
        const forms = document.querySelectorAll('form');
        
        forms.forEach(form => {
            // 表单聚焦
            form.addEventListener('focusin', function(e) {
                if (!form.dataset.focused) {
                    form.dataset.focused = 'true';
                    trackEvent('form_start', {
                        'event_category': 'engagement',
                        'event_label': form.id || form.className || 'unknown_form'
                    });
                }
            }, { once: true });
            
            // 表单提交
            form.addEventListener('submit', function() {
                trackEvent('form_submit', {
                    'event_category': 'conversion',
                    'event_label': form.id || form.className || 'unknown_form'
                });
            });
        });
        
        console.log(`✅ 表单交互跟踪已启用 (${forms.length}个表单)`);
    }
    
    // ============================================
    // 10. 视频播放跟踪 ⭐⭐⭐
    // ============================================
    function trackVideoPlayback() {
        const videos = document.querySelectorAll('video');
        
        videos.forEach(video => {
            video.addEventListener('play', function() {
                trackEvent('video_play', {
                    'event_category': 'engagement',
                    'event_label': video.src || 'demo_video'
                });
            });
            
            video.addEventListener('ended', function() {
                trackEvent('video_complete', {
                    'event_category': 'engagement',
                    'event_label': video.src || 'demo_video'
                });
            });
        });
        
        if (videos.length > 0) {
            console.log(`✅ 视频播放跟踪已启用 (${videos.length}个视频)`);
        }
    }
    
    // ============================================
    // 初始化所有跟踪
    // ============================================
    function initializeTracking() {
        // 等待DOM加载完成
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', initializeTracking);
            return;
        }
        
        // 检查GA是否已加载
        if (!isGALoaded()) {
            console.warn('⚠️ Google Analytics未加载，事件跟踪将不会生效');
            // 继续初始化，以便GA稍后加载时可以工作
        }
        
        // 初始化所有跟踪功能
        setTimeout(() => {
            trackGIFViews();
            trackPDFUploads();
            trackCTAClicks();
            trackFreeTrialBannerClicks();
            trackScrollDepth();
            trackTimeOnPage();
            trackOutboundLinks();
            trackFormInteractions();
            trackVideoPlayback();
            
            console.log('🎉 所有GA事件跟踪已初始化完成');
        }, 500);
    }
    
    // 立即初始化
    initializeTracking();
    
})();

