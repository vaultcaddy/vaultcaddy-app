// 安全地隐藏控制台日志
// 不删除代码，只是让console.log不输出
// 保留console.error和console.warn用于错误追踪

(function() {
    'use strict';
    
    // 保存原始console方法
    const originalConsole = {
        log: console.log,
        warn: console.warn,
        error: console.error,
        info: console.info,
        debug: console.debug
    };
    
    // 检测是否在生产环境
    const isProduction = window.location.hostname === 'vaultcaddy.com';
    
    // 检测是否有debug参数（用于临时开启日志）
    const urlParams = new URLSearchParams(window.location.search);
    const debugMode = urlParams.has('debug');
    
    if (false) {  // ✅ 临时禁用日志隐藏，方便调试
        // 🔇 生产环境：隐藏console.log
        console.log = function() {
            // 不输出任何内容
        };
        
        console.info = function() {
            // 不输出任何内容
        };
        
        console.debug = function() {
            // 不输出任何内容
        };
        
        // ⚠️ 保留 console.warn（警告信息）
        // console.warn = originalConsole.warn;
        
        // ❌ 保留 console.error（错误信息，用于追踪问题）
        // console.error = originalConsole.error;
        
        console.log('✅ 控制台日志已隐藏（生产环境）');
        
    } else {
        // 🔊 开发环境或debug模式：保留所有日志
        console.log('🔧 控制台日志已启用（开发环境或debug模式）');
    }
    
    // 暴露原始console方法（用于调试）
    window._originalConsole = originalConsole;
    
    // 提供开启日志的函数
    window.enableConsoleLog = function() {
        console.log = originalConsole.log;
        console.info = originalConsole.info;
        console.debug = originalConsole.debug;
        console.log('✅ 控制台日志已重新启用');
    };
    
    // 提供关闭日志的函数
    window.disableConsoleLog = function() {
        console.log = function() {};
        console.info = function() {};
        console.debug = function() {};
        originalConsole.log('✅ 控制台日志已禁用');
    };
})();

// 使用说明：
// 1. 在页面<head>中引入此脚本（尽可能早）
// 2. 生产环境自动隐藏console.log
// 3. 如需临时查看日志，访问：?debug=1
// 4. 或在控制台执行：enableConsoleLog()

