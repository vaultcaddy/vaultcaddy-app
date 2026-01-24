/**
 * 日志工具 (Logger Utility)
 * 作用: 条件化调试日志，生产环境不输出，减少控制台噪音
 * 版本: 1.0.0
 * 日期: 2026-01-23
 * 
 * 使用方法:
 *   logger.log('调试信息');   // 只在 DEBUG_MODE = true 时输出
 *   logger.error('错误信息'); // 始终输出（重要）
 *   logger.warn('警告信息');  // 只在 DEBUG_MODE = true 时输出
 * 
 * 配置:
 *   生产环境: window.DEBUG_MODE = false;
 *   开发环境: window.DEBUG_MODE = true;
 */

(function() {
    'use strict';
    
    // 生产环境设置为 false，开发环境设置为 true
    window.DEBUG_MODE = false;
    
    window.logger = {
        /**
         * 普通日志 - 只在开发模式下输出
         */
        log: function(...args) {
            if (window.DEBUG_MODE) {
                console.log(...args);
            }
        },
        
        /**
         * 错误日志 - 始终输出（生产环境也需要）
         */
        error: function(...args) {
            console.error(...args);
        },
        
        /**
         * 警告日志 - 只在开发模式下输出
         */
        warn: function(...args) {
            if (window.DEBUG_MODE) {
                console.warn(...args);
            }
        },
        
        /**
         * 信息日志 - 只在开发模式下输出
         */
        info: function(...args) {
            if (window.DEBUG_MODE) {
                console.info(...args);
            }
        },
        
        /**
         * 分组开始 - 只在开发模式下输出
         */
        group: function(title) {
            if (window.DEBUG_MODE) {
                console.group(title);
            }
        },
        
        /**
         * 分组结束 - 只在开发模式下输出
         */
        groupEnd: function() {
            if (window.DEBUG_MODE) {
                console.groupEnd();
            }
        },
        
        /**
         * 表格输出 - 只在开发模式下输出
         */
        table: function(data) {
            if (window.DEBUG_MODE) {
                console.table(data);
            }
        }
    };
    
    // 开发模式提示
    if (window.DEBUG_MODE) {
        console.log('%c🔧 Debug Mode Enabled', 'color: #10b981; font-weight: bold; font-size: 14px');
    }
})();

