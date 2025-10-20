/**
 * VaultCaddy 智能對賬引擎
 * 
 * 核心功能:
 * 1. 自動匹配發票/收據與銀行交易
 * 2. 多維度匹配算法（金額、日期、對手方）
 * 3. 模糊匹配和智能建議
 * 4. 批量對賬處理
 * 
 * @version 1.0.0
 */

class SmartReconciliationEngine {
    constructor() {
        this.version = '1.0.0';
        this.matchingRules = this.initializeMatchingRules();
        this.matchHistory = [];
    }
    
    /**
     * 初始化匹配規則
     */
    initializeMatchingRules() {
        return {
            // 完全匹配規則（高信心度）
            exact: {
                amountTolerance: 0.01,      // 金額誤差容忍度（HKD）
                dateTolerance: 0,            // 日期誤差容忍度（天）
                nameMatchThreshold: 0.95,    // 名稱匹配閾值
                confidenceScore: 95          // 信心分數
            },
            
            // 強匹配規則（中高信心度）
            strong: {
                amountTolerance: 1.00,       // 金額誤差容忍度
                dateTolerance: 3,            // 日期誤差容忍度（±3天）
                nameMatchThreshold: 0.85,    // 名稱匹配閾值
                confidenceScore: 85          // 信心分數
            },
            
            // 可能匹配規則（中信心度）
            possible: {
                amountTolerance: 5.00,       // 金額誤差容忍度
                dateTolerance: 7,            // 日期誤差容忍度（±7天）
                nameMatchThreshold: 0.70,    // 名稱匹配閾值
                confidenceScore: 70          // 信心分數
            },
            
            // 弱匹配規則（低信心度）
            weak: {
                amountTolerance: 10.00,      // 金額誤差容忍度
                dateTolerance: 14,           // 日期誤差容忍度（±14天）
                nameMatchThreshold: 0.60,    // 名稱匹配閾值
                confidenceScore: 60          // 信心分數
            }
        };
    }
    
    /**
     * 主要對賬方法：自動匹配發票和銀行交易
     * 
     * @param {Array} invoices - 發票列表
     * @param {Array} bankTransactions - 銀行交易列表
     * @returns {Object} 對賬結果
     */
    async reconcile(invoices, bankTransactions) {
        console.log('🔄 開始智能對賬...');
        console.log(`   發票數量: ${invoices.length}`);
        console.log(`   銀行交易數量: ${bankTransactions.length}`);
        
        const startTime = Date.now();
        const results = {
            matched: [],           // 已匹配
            unmatched: {
                invoices: [],      // 未匹配的發票
                transactions: []   // 未匹配的交易
            },
            suggestions: [],       // 匹配建議
            summary: {
                totalInvoices: invoices.length,
                totalTransactions: bankTransactions.length,
                matchedCount: 0,
                unmatchedInvoicesCount: 0,
                unmatchedTransactionsCount: 0,
                matchRate: 0,
                processingTime: 0
            }
        };
        
        // 創建交易副本以追蹤已匹配的項目
        const remainingTransactions = [...bankTransactions];
        const remainingInvoices = [...invoices];
        
        // 第一輪：完全匹配（最高優先級）
        console.log('🎯 第一輪: 完全匹配...');
        const exactMatches = this.findExactMatches(remainingInvoices, remainingTransactions);
        results.matched.push(...exactMatches);
        this.removeMatchedItems(remainingInvoices, remainingTransactions, exactMatches);
        console.log(`   完全匹配: ${exactMatches.length} 對`);
        
        // 第二輪：強匹配
        console.log('🎯 第二輪: 強匹配...');
        const strongMatches = this.findStrongMatches(remainingInvoices, remainingTransactions);
        results.matched.push(...strongMatches);
        this.removeMatchedItems(remainingInvoices, remainingTransactions, strongMatches);
        console.log(`   強匹配: ${strongMatches.length} 對`);
        
        // 第三輪：可能匹配（作為建議）
        console.log('💡 第三輪: 生成匹配建議...');
        const possibleMatches = this.findPossibleMatches(remainingInvoices, remainingTransactions);
        results.suggestions = possibleMatches;
        console.log(`   匹配建議: ${possibleMatches.length} 對`);
        
        // 整理未匹配項目
        results.unmatched.invoices = remainingInvoices;
        results.unmatched.transactions = remainingTransactions;
        
        // 計算統計數據
        results.summary.matchedCount = results.matched.length;
        results.summary.unmatchedInvoicesCount = remainingInvoices.length;
        results.summary.unmatchedTransactionsCount = remainingTransactions.length;
        results.summary.matchRate = invoices.length > 0 
            ? Math.round((results.matched.length / invoices.length) * 100) 
            : 0;
        results.summary.processingTime = Date.now() - startTime;
        
        console.log('✅ 對賬完成！');
        console.log(`   匹配成功: ${results.matched.length} 對`);
        console.log(`   未匹配發票: ${results.unmatched.invoices.length}`);
        console.log(`   未匹配交易: ${results.unmatched.transactions.length}`);
        console.log(`   匹配率: ${results.summary.matchRate}%`);
        console.log(`   處理時間: ${results.summary.processingTime}ms`);
        
        return results;
    }
    
    /**
     * 查找完全匹配
     */
    findExactMatches(invoices, transactions) {
        const matches = [];
        const rule = this.matchingRules.exact;
        
        for (const invoice of invoices) {
            for (const transaction of transactions) {
                const match = this.evaluateMatch(invoice, transaction, rule);
                
                if (match.isMatch && match.confidenceScore >= rule.confidenceScore) {
                    matches.push({
                        invoice: invoice,
                        transaction: transaction,
                        matchType: 'exact',
                        confidenceScore: match.confidenceScore,
                        matchDetails: match.details,
                        matchedAt: new Date().toISOString()
                    });
                    break; // 找到匹配後停止搜索此發票
                }
            }
        }
        
        return matches;
    }
    
    /**
     * 查找強匹配
     */
    findStrongMatches(invoices, transactions) {
        const matches = [];
        const rule = this.matchingRules.strong;
        
        for (const invoice of invoices) {
            for (const transaction of transactions) {
                const match = this.evaluateMatch(invoice, transaction, rule);
                
                if (match.isMatch && match.confidenceScore >= rule.confidenceScore) {
                    matches.push({
                        invoice: invoice,
                        transaction: transaction,
                        matchType: 'strong',
                        confidenceScore: match.confidenceScore,
                        matchDetails: match.details,
                        matchedAt: new Date().toISOString()
                    });
                    break;
                }
            }
        }
        
        return matches;
    }
    
    /**
     * 查找可能匹配（作為建議）
     */
    findPossibleMatches(invoices, transactions) {
        const suggestions = [];
        const rule = this.matchingRules.possible;
        
        for (const invoice of invoices) {
            const candidateMatches = [];
            
            for (const transaction of transactions) {
                const match = this.evaluateMatch(invoice, transaction, rule);
                
                if (match.isMatch && match.confidenceScore >= rule.confidenceScore) {
                    candidateMatches.push({
                        invoice: invoice,
                        transaction: transaction,
                        matchType: 'possible',
                        confidenceScore: match.confidenceScore,
                        matchDetails: match.details
                    });
                }
            }
            
            // 按信心分數排序，只保留前3個建議
            if (candidateMatches.length > 0) {
                candidateMatches.sort((a, b) => b.confidenceScore - a.confidenceScore);
                suggestions.push({
                    invoice: invoice,
                    suggestedMatches: candidateMatches.slice(0, 3)
                });
            }
        }
        
        return suggestions;
    }
    
    /**
     * 評估發票和交易的匹配程度
     */
    evaluateMatch(invoice, transaction, rule) {
        const result = {
            isMatch: false,
            confidenceScore: 0,
            details: {
                amountMatch: false,
                dateMatch: false,
                nameMatch: false,
                amountDifference: 0,
                dateDifference: 0,
                nameSimilarity: 0
            }
        };
        
        // 1. 金額匹配檢查
        const invoiceAmount = this.extractAmount(invoice);
        const transactionAmount = Math.abs(transaction.debit || transaction.credit || transaction.amount || 0);
        const amountDiff = Math.abs(invoiceAmount - transactionAmount);
        result.details.amountDifference = amountDiff;
        result.details.amountMatch = amountDiff <= rule.amountTolerance;
        
        if (!result.details.amountMatch) {
            return result; // 金額不匹配，直接返回
        }
        
        // 2. 日期匹配檢查
        const invoiceDate = this.parseDate(invoice.issueDate || invoice.date);
        const transactionDate = this.parseDate(transaction.date);
        
        if (invoiceDate && transactionDate) {
            const dateDiff = Math.abs(this.getDaysDifference(invoiceDate, transactionDate));
            result.details.dateDifference = dateDiff;
            result.details.dateMatch = dateDiff <= rule.dateTolerance;
        }
        
        // 3. 名稱/對手方匹配檢查
        const invoiceName = this.extractName(invoice);
        const transactionName = this.extractTransactionName(transaction);
        
        if (invoiceName && transactionName) {
            const similarity = this.calculateStringSimilarity(invoiceName, transactionName);
            result.details.nameSimilarity = similarity;
            result.details.nameMatch = similarity >= rule.nameMatchThreshold;
        }
        
        // 4. 計算總體信心分數
        let score = 0;
        let maxScore = 0;
        
        // 金額匹配（40分）
        maxScore += 40;
        if (result.details.amountMatch) {
            if (amountDiff === 0) {
                score += 40;
            } else {
                score += 40 * (1 - amountDiff / rule.amountTolerance);
            }
        }
        
        // 日期匹配（30分）
        maxScore += 30;
        if (result.details.dateMatch) {
            if (result.details.dateDifference === 0) {
                score += 30;
            } else {
                score += 30 * (1 - result.details.dateDifference / rule.dateTolerance);
            }
        }
        
        // 名稱匹配（30分）
        maxScore += 30;
        if (result.details.nameMatch) {
            score += 30 * result.details.nameSimilarity;
        }
        
        result.confidenceScore = Math.round((score / maxScore) * 100);
        result.isMatch = result.confidenceScore >= rule.confidenceScore;
        
        return result;
    }
    
    /**
     * 從發票中提取金額
     */
    extractAmount(invoice) {
        return parseFloat(
            invoice.totalAmount || 
            invoice.processedData?.totalAmount || 
            invoice.amount || 
            0
        );
    }
    
    /**
     * 從發票中提取名稱（供應商或客戶）
     */
    extractName(invoice) {
        const vendor = invoice.vendor?.name || invoice.processedData?.vendor?.name || '';
        const customer = invoice.customer?.name || invoice.processedData?.customer?.name || '';
        return (vendor || customer).toLowerCase().trim();
    }
    
    /**
     * 從交易中提取對手方名稱
     */
    extractTransactionName(transaction) {
        return (transaction.description || transaction.counterparty || '').toLowerCase().trim();
    }
    
    /**
     * 解析日期字符串
     */
    parseDate(dateString) {
        if (!dateString) return null;
        const date = new Date(dateString);
        return isNaN(date.getTime()) ? null : date;
    }
    
    /**
     * 計算兩個日期之間的天數差
     */
    getDaysDifference(date1, date2) {
        const diffTime = Math.abs(date2 - date1);
        return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    }
    
    /**
     * 計算字符串相似度（使用 Levenshtein 距離）
     */
    calculateStringSimilarity(str1, str2) {
        if (!str1 || !str2) return 0;
        
        // 預處理：移除空格、轉小寫
        str1 = str1.replace(/\s+/g, '').toLowerCase();
        str2 = str2.replace(/\s+/g, '').toLowerCase();
        
        if (str1 === str2) return 1.0;
        
        // 計算 Levenshtein 距離
        const matrix = [];
        const len1 = str1.length;
        const len2 = str2.length;
        
        for (let i = 0; i <= len1; i++) {
            matrix[i] = [i];
        }
        
        for (let j = 0; j <= len2; j++) {
            matrix[0][j] = j;
        }
        
        for (let i = 1; i <= len1; i++) {
            for (let j = 1; j <= len2; j++) {
                const cost = str1[i - 1] === str2[j - 1] ? 0 : 1;
                matrix[i][j] = Math.min(
                    matrix[i - 1][j] + 1,      // 刪除
                    matrix[i][j - 1] + 1,      // 插入
                    matrix[i - 1][j - 1] + cost // 替換
                );
            }
        }
        
        const distance = matrix[len1][len2];
        const maxLen = Math.max(len1, len2);
        
        return maxLen === 0 ? 1.0 : 1.0 - (distance / maxLen);
    }
    
    /**
     * 從列表中移除已匹配的項目
     */
    removeMatchedItems(invoices, transactions, matches) {
        for (const match of matches) {
            const invoiceIndex = invoices.findIndex(inv => inv.id === match.invoice.id);
            if (invoiceIndex !== -1) {
                invoices.splice(invoiceIndex, 1);
            }
            
            const transactionIndex = transactions.findIndex(txn => txn.id === match.transaction.id);
            if (transactionIndex !== -1) {
                transactions.splice(transactionIndex, 1);
            }
        }
    }
    
    /**
     * 手動匹配（用戶確認匹配）
     */
    manualMatch(invoice, transaction, userId = null) {
        console.log('👤 手動匹配確認...');
        
        const match = {
            invoice: invoice,
            transaction: transaction,
            matchType: 'manual',
            confidenceScore: 100,
            matchDetails: {
                manuallyMatched: true,
                matchedBy: userId,
                matchedAt: new Date().toISOString()
            }
        };
        
        this.matchHistory.push(match);
        
        console.log('✅ 手動匹配已記錄');
        return match;
    }
    
    /**
     * 取消匹配
     */
    unmatch(matchId) {
        console.log('🔓 取消匹配...');
        
        const matchIndex = this.matchHistory.findIndex(m => m.id === matchId);
        if (matchIndex !== -1) {
            this.matchHistory.splice(matchIndex, 1);
            console.log('✅ 匹配已取消');
            return true;
        }
        
        console.log('⚠️ 未找到匹配記錄');
        return false;
    }
    
    /**
     * 獲取對賬統計
     */
    getReconciliationStats(matches) {
        const stats = {
            total: matches.length,
            byType: {
                exact: 0,
                strong: 0,
                possible: 0,
                manual: 0
            },
            byConfidence: {
                high: 0,    // >= 90
                medium: 0,  // 70-89
                low: 0      // < 70
            },
            totalAmount: 0,
            averageConfidence: 0
        };
        
        let totalConfidence = 0;
        
        for (const match of matches) {
            // 按類型統計
            stats.byType[match.matchType] = (stats.byType[match.matchType] || 0) + 1;
            
            // 按信心度統計
            if (match.confidenceScore >= 90) {
                stats.byConfidence.high++;
            } else if (match.confidenceScore >= 70) {
                stats.byConfidence.medium++;
            } else {
                stats.byConfidence.low++;
            }
            
            // 總金額
            stats.totalAmount += this.extractAmount(match.invoice);
            
            // 總信心度
            totalConfidence += match.confidenceScore;
        }
        
        stats.averageConfidence = matches.length > 0 
            ? Math.round(totalConfidence / matches.length) 
            : 0;
        
        return stats;
    }
}

// 導出為全局變量
if (typeof window !== 'undefined') {
    window.SmartReconciliationEngine = SmartReconciliationEngine;
    window.smartReconciliationEngine = new SmartReconciliationEngine();
    console.log('✅ 智能對賬引擎已加載');
}

// Node.js 環境導出
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SmartReconciliationEngine;
}

