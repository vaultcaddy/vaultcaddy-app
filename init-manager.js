/**
 * 初始化管理器 (Initialization Manager)
 * 作用: 统一管理异步初始化，避免多次 setTimeout 重试
 * 版本: 1.0.0
 * 日期: 2026-01-23
 * 
 * 功能:
 *   - Promise 基础的等待机制
 *   - 避免重复初始化
 *   - 超时控制
 * 
 * 使用示例:
 *   await window.initManager.waitFor('simpleAuth', 
 *     () => window.simpleAuth && window.simpleAuth.isReady
 *   );
 */

class InitializationManager {
    constructor() {
        this.promises = new Map();
        this.initialized = new Set();
        logger.log('初始化管理器已创建');
    }
    
    /**
     * 等待某个条件满足
     * @param {string} key - 唯一标识
     * @param {Function} checkFn - 检查函数，返回 true 表示已就绪
     * @param {number} timeout - 超时时间（毫秒），默认 5000ms
     * @param {number} interval - 检查间隔（毫秒），默认 100ms
     * @returns {Promise} 
     */
    async waitFor(key, checkFn, timeout = 5000, interval = 100) {
        // 如果已经初始化过，直接返回
        if (this.initialized.has(key)) {
            logger.log(`${key} 已初始化，立即返回`);
            return Promise.resolve();
        }
        
        // 如果正在等待，返回现有的 Promise
        if (this.promises.has(key)) {
            logger.log(`${key} 正在等待中，返回现有 Promise`);
            return this.promises.get(key);
        }
        
        // 创建新的等待 Promise
        const promise = new Promise((resolve, reject) => {
            const startTime = Date.now();
            
            const check = () => {
                try {
                    if (checkFn()) {
                        this.initialized.add(key);
                        this.promises.delete(key);
                        logger.log(`${key} 已就绪`);
                        resolve();
                    } else if (Date.now() - startTime > timeout) {
                        this.promises.delete(key);
                        logger.error(`等待 ${key} 超时`);
                        reject(new Error(`Timeout waiting for ${key}`));
                    } else {
                        setTimeout(check, interval);
                    }
                } catch (error) {
                    this.promises.delete(key);
                    logger.error(`检查 ${key} 时出错:`, error);
                    reject(error);
                }
            };
            
            logger.log(`开始等待 ${key}`);
            check();
        });
        
        this.promises.set(key, promise);
        return promise;
    }
    
    /**
     * 手动标记为已初始化
     * @param {string} key - 唯一标识
     */
    markInitialized(key) {
        this.initialized.add(key);
        logger.log(`${key} 被手动标记为已初始化`);
    }
    
    /**
     * 检查是否已初始化
     * @param {string} key - 唯一标识
     * @returns {boolean}
     */
    isInitialized(key) {
        return this.initialized.has(key);
    }
    
    /**
     * 重置初始化状态（用于测试或重新初始化）
     * @param {string} key - 唯一标识
     */
    reset(key) {
        this.initialized.delete(key);
        this.promises.delete(key);
        logger.log(`${key} 已重置`);
    }
    
    /**
     * 重置所有
     */
    resetAll() {
        this.initialized.clear();
        this.promises.clear();
        logger.log('所有初始化状态已重置');
    }
}

// 创建全局实例
window.initManager = new InitializationManager();

logger.log('初始化管理器已加载');
