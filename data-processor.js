/**
 * 文檔數據處理器
 * 使用JavaScript實現類似pandas的數據處理功能
 */

class DocumentDataProcessor {
    constructor() {
        this.supportedFormats = ['csv', 'json', 'excel'];
        console.log('📊 文檔數據處理器已初始化');
    }
    
    /**
     * 處理銀行對帳單數據
     */
    async processBankStatementData(extractedData) {
        console.log('📊 處理銀行對帳單數據');
        
        const { transactions, accountInfo, statementPeriod, financialPosition } = extractedData;
        
        if (!transactions || transactions.length === 0) {
            throw new Error('沒有找到交易記錄');
        }
        
        // 數據清理和標準化
        const cleanedTransactions = this.cleanTransactionData(transactions);
        
        // 計算統計信息
        const statistics = this.calculateStatistics(cleanedTransactions);
        
        // 分類分析
        const categoryAnalysis = this.categorizeTransactions(cleanedTransactions);
        
        // 時間序列分析
        const timeSeriesAnalysis = this.analyzeTimeSeriesData(cleanedTransactions);
        
        // 生成洞察
        const insights = this.generateBankStatementInsights(cleanedTransactions, statistics);
        
        return {
            processedTransactions: cleanedTransactions,
            statistics: statistics,
            categoryAnalysis: categoryAnalysis,
            timeSeriesAnalysis: timeSeriesAnalysis,
            insights: insights,
            metadata: {
                accountInfo: accountInfo,
                statementPeriod: statementPeriod,
                financialPosition: financialPosition,
                processedAt: new Date().toISOString()
            }
        };
    }
    
    /**
     * 處理收據數據
     */
    async processReceiptData(extractedData) {
        console.log('📊 處理收據數據');
        
        const { items, totalAmount, merchant, date } = extractedData;
        
        if (!items || items.length === 0) {
            console.warn('沒有找到商品項目，使用總金額創建單一項目');
            return this.createSingleItemReceipt(extractedData);
        }
        
        // 數據清理和標準化
        const cleanedItems = this.cleanReceiptItems(items);
        
        // 計算統計信息
        const statistics = this.calculateReceiptStatistics(cleanedItems, totalAmount);
        
        // 商品分類
        const itemCategories = this.categorizeReceiptItems(cleanedItems);
        
        // 生成洞察
        const insights = this.generateReceiptInsights(cleanedItems, statistics);
        
        return {
            processedItems: cleanedItems,
            statistics: statistics,
            itemCategories: itemCategories,
            insights: insights,
            metadata: {
                merchant: merchant,
                date: date,
                totalAmount: totalAmount,
                processedAt: new Date().toISOString()
            }
        };
    }
    
    /**
     * 處理發票數據
     */
    async processInvoiceData(extractedData) {
        console.log('📊 處理發票數據');
        
        const { lineItems, totalAmount, vendor, customer } = extractedData;
        
        // 數據清理和標準化
        const cleanedLineItems = this.cleanInvoiceItems(lineItems || []);
        
        // 計算統計信息
        const statistics = this.calculateInvoiceStatistics(cleanedLineItems, totalAmount);
        
        // 生成洞察
        const insights = this.generateInvoiceInsights(cleanedLineItems, statistics);
        
        return {
            processedLineItems: cleanedLineItems,
            statistics: statistics,
            insights: insights,
            metadata: {
                vendor: vendor,
                customer: customer,
                totalAmount: totalAmount,
                processedAt: new Date().toISOString()
            }
        };
    }
    
    /**
     * 清理交易數據
     */
    cleanTransactionData(transactions) {
        return transactions
            .filter(transaction => transaction && transaction.date && transaction.amount !== undefined)
            .map(transaction => ({
                date: this.standardizeDate(transaction.date),
                description: this.cleanDescription(transaction.description),
                amount: this.parseAmount(transaction.amount),
                balance: this.parseAmount(transaction.balance),
                type: transaction.amount >= 0 ? 'credit' : 'debit',
                category: this.categorizeTransaction(transaction.description)
            }))
            .sort((a, b) => new Date(a.date) - new Date(b.date));
    }
    
    /**
     * 清理收據商品數據
     */
    cleanReceiptItems(items) {
        return items
            .filter(item => item && item.name && item.amount !== undefined)
            .map(item => ({
                name: this.cleanItemName(item.name),
                amount: this.parseAmount(item.amount),
                quantity: item.quantity || 1,
                unitPrice: this.parseAmount(item.amount) / (item.quantity || 1),
                category: this.categorizeReceiptItem(item.name)
            }));
    }
    
    /**
     * 清理發票項目數據
     */
    cleanInvoiceItems(lineItems) {
        return lineItems
            .filter(item => item && item.description && item.amount !== undefined)
            .map(item => ({
                description: this.cleanDescription(item.description),
                quantity: item.quantity || 1,
                unitPrice: this.parseAmount(item.unitPrice || item.amount),
                amount: this.parseAmount(item.amount),
                category: this.categorizeInvoiceItem(item.description)
            }));
    }
    
    /**
     * 計算統計信息
     */
    calculateStatistics(transactions) {
        const amounts = transactions.map(t => t.amount);
        const credits = transactions.filter(t => t.amount > 0);
        const debits = transactions.filter(t => t.amount < 0);
        
        return {
            totalTransactions: transactions.length,
            totalCredits: credits.reduce((sum, t) => sum + t.amount, 0),
            totalDebits: Math.abs(debits.reduce((sum, t) => sum + t.amount, 0)),
            averageTransaction: this.calculateMean(amounts),
            medianTransaction: this.calculateMedian(amounts),
            largestCredit: Math.max(...credits.map(t => t.amount), 0),
            largestDebit: Math.abs(Math.min(...debits.map(t => t.amount), 0)),
            dateRange: {
                start: transactions[0]?.date,
                end: transactions[transactions.length - 1]?.date
            },
            creditCount: credits.length,
            debitCount: debits.length
        };
    }
    
    /**
     * 計算收據統計信息
     */
    calculateReceiptStatistics(items, totalAmount) {
        const amounts = items.map(item => item.amount);
        
        return {
            totalItems: items.length,
            totalAmount: totalAmount || items.reduce((sum, item) => sum + item.amount, 0),
            averageItemPrice: this.calculateMean(amounts),
            medianItemPrice: this.calculateMedian(amounts),
            mostExpensiveItem: Math.max(...amounts, 0),
            leastExpensiveItem: Math.min(...amounts.filter(a => a > 0), 0),
            totalQuantity: items.reduce((sum, item) => sum + item.quantity, 0)
        };
    }
    
    /**
     * 計算發票統計信息
     */
    calculateInvoiceStatistics(lineItems, totalAmount) {
        const amounts = lineItems.map(item => item.amount);
        
        return {
            totalLineItems: lineItems.length,
            totalAmount: totalAmount || lineItems.reduce((sum, item) => sum + item.amount, 0),
            averageLineAmount: this.calculateMean(amounts),
            totalQuantity: lineItems.reduce((sum, item) => sum + item.quantity, 0)
        };
    }
    
    /**
     * 交易分類
     */
    categorizeTransactions(transactions) {
        const categories = {};
        
        transactions.forEach(transaction => {
            const category = transaction.category;
            if (!categories[category]) {
                categories[category] = {
                    count: 0,
                    totalAmount: 0,
                    transactions: []
                };
            }
            
            categories[category].count++;
            categories[category].totalAmount += Math.abs(transaction.amount);
            categories[category].transactions.push(transaction);
        });
        
        // 按金額排序
        return Object.entries(categories)
            .map(([name, data]) => ({
                category: name,
                ...data,
                averageAmount: data.totalAmount / data.count,
                percentage: (data.totalAmount / transactions.reduce((sum, t) => sum + Math.abs(t.amount), 0)) * 100
            }))
            .sort((a, b) => b.totalAmount - a.totalAmount);
    }
    
    /**
     * 收據商品分類
     */
    categorizeReceiptItems(items) {
        const categories = {};
        
        items.forEach(item => {
            const category = item.category;
            if (!categories[category]) {
                categories[category] = {
                    count: 0,
                    totalAmount: 0,
                    items: []
                };
            }
            
            categories[category].count++;
            categories[category].totalAmount += item.amount;
            categories[category].items.push(item);
        });
        
        return Object.entries(categories)
            .map(([name, data]) => ({
                category: name,
                ...data,
                averageAmount: data.totalAmount / data.count,
                percentage: (data.totalAmount / items.reduce((sum, item) => sum + item.amount, 0)) * 100
            }))
            .sort((a, b) => b.totalAmount - a.totalAmount);
    }
    
    /**
     * 時間序列分析
     */
    analyzeTimeSeriesData(transactions) {
        const dailyData = {};
        const monthlyData = {};
        
        transactions.forEach(transaction => {
            const date = transaction.date;
            const month = date.substring(0, 7); // YYYY-MM
            
            // 日數據
            if (!dailyData[date]) {
                dailyData[date] = { credits: 0, debits: 0, balance: 0 };
            }
            
            if (transaction.amount > 0) {
                dailyData[date].credits += transaction.amount;
            } else {
                dailyData[date].debits += Math.abs(transaction.amount);
            }
            
            dailyData[date].balance = transaction.balance;
            
            // 月數據
            if (!monthlyData[month]) {
                monthlyData[month] = { credits: 0, debits: 0, netFlow: 0 };
            }
            
            if (transaction.amount > 0) {
                monthlyData[month].credits += transaction.amount;
            } else {
                monthlyData[month].debits += Math.abs(transaction.amount);
            }
            
            monthlyData[month].netFlow = monthlyData[month].credits - monthlyData[month].debits;
        });
        
        return {
            dailyData: dailyData,
            monthlyData: monthlyData,
            trends: this.calculateTrends(Object.values(monthlyData))
        };
    }
    
    /**
     * 生成銀行對帳單洞察
     */
    generateBankStatementInsights(transactions, statistics) {
        const insights = [];
        
        // 現金流洞察
        if (statistics.totalCredits > statistics.totalDebits) {
            insights.push({
                type: 'positive',
                title: '正現金流',
                message: `本期收入 $${statistics.totalCredits.toFixed(2)} 超過支出 $${statistics.totalDebits.toFixed(2)}`
            });
        } else {
            insights.push({
                type: 'warning',
                title: '負現金流',
                message: `本期支出 $${statistics.totalDebits.toFixed(2)} 超過收入 $${statistics.totalCredits.toFixed(2)}`
            });
        }
        
        // 交易頻率洞察
        const avgTransactionsPerDay = statistics.totalTransactions / this.calculateDaysBetween(
            statistics.dateRange.start, 
            statistics.dateRange.end
        );
        
        insights.push({
            type: 'info',
            title: '交易頻率',
            message: `平均每日 ${avgTransactionsPerDay.toFixed(1)} 筆交易`
        });
        
        // 大額交易洞察
        if (statistics.largestDebit > statistics.averageTransaction * 5) {
            insights.push({
                type: 'warning',
                title: '大額支出',
                message: `發現大額支出 $${statistics.largestDebit.toFixed(2)}，為平均交易金額的 ${(statistics.largestDebit / Math.abs(statistics.averageTransaction)).toFixed(1)} 倍`
            });
        }
        
        return insights;
    }
    
    /**
     * 生成收據洞察
     */
    generateReceiptInsights(items, statistics) {
        const insights = [];
        
        // 商品數量洞察
        insights.push({
            type: 'info',
            title: '購買概況',
            message: `共購買 ${statistics.totalItems} 種商品，總金額 $${statistics.totalAmount.toFixed(2)}`
        });
        
        // 價格分析
        if (statistics.mostExpensiveItem > statistics.averageItemPrice * 3) {
            insights.push({
                type: 'warning',
                title: '高價商品',
                message: `最貴商品 $${statistics.mostExpensiveItem.toFixed(2)} 為平均價格的 ${(statistics.mostExpensiveItem / statistics.averageItemPrice).toFixed(1)} 倍`
            });
        }
        
        return insights;
    }
    
    /**
     * 生成發票洞察
     */
    generateInvoiceInsights(lineItems, statistics) {
        const insights = [];
        
        insights.push({
            type: 'info',
            title: '發票概況',
            message: `共 ${statistics.totalLineItems} 個項目，總金額 $${statistics.totalAmount.toFixed(2)}`
        });
        
        return insights;
    }
    
    /**
     * 導出為CSV格式
     */
    exportToCSV(data, type = 'transactions') {
        let headers, rows;
        
        switch (type) {
            case 'transactions':
                headers = ['日期', '描述', '金額', '餘額', '類型', '類別'];
                rows = data.map(t => [
                    t.date,
                    t.description,
                    t.amount,
                    t.balance,
                    t.type,
                    t.category
                ]);
                break;
                
            case 'receipt-items':
                headers = ['商品名稱', '數量', '單價', '金額', '類別'];
                rows = data.map(item => [
                    item.name,
                    item.quantity,
                    item.unitPrice,
                    item.amount,
                    item.category
                ]);
                break;
                
            case 'invoice-items':
                headers = ['描述', '數量', '單價', '金額', '類別'];
                rows = data.map(item => [
                    item.description,
                    item.quantity,
                    item.unitPrice,
                    item.amount,
                    item.category
                ]);
                break;
                
            default:
                throw new Error(`不支援的導出類型: ${type}`);
        }
        
        const csvContent = [headers, ...rows]
            .map(row => row.map(field => `"${field}"`).join(','))
            .join('\n');
            
        return csvContent;
    }
    
    /**
     * 導出為JSON格式
     */
    exportToJSON(data) {
        return JSON.stringify(data, null, 2);
    }
    
    /**
     * 導出為Excel格式（使用SheetJS）
     */
    async exportToExcel(data, type = 'transactions') {
        if (typeof XLSX === 'undefined') {
            throw new Error('SheetJS (XLSX) 庫未載入');
        }
        
        let worksheetData;
        
        switch (type) {
            case 'transactions':
                worksheetData = data.map(t => ({
                    '日期': t.date,
                    '描述': t.description,
                    '金額': t.amount,
                    '餘額': t.balance,
                    '類型': t.type,
                    '類別': t.category
                }));
                break;
                
            case 'receipt-items':
                worksheetData = data.map(item => ({
                    '商品名稱': item.name,
                    '數量': item.quantity,
                    '單價': item.unitPrice,
                    '金額': item.amount,
                    '類別': item.category
                }));
                break;
                
            case 'invoice-items':
                worksheetData = data.map(item => ({
                    '描述': item.description,
                    '數量': item.quantity,
                    '單價': item.unitPrice,
                    '金額': item.amount,
                    '類別': item.category
                }));
                break;
        }
        
        const ws = XLSX.utils.json_to_sheet(worksheetData);
        const wb = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(wb, ws, "數據");
        
        return XLSX.write(wb, { bookType: 'xlsx', type: 'array' });
    }
    
    // ==================== 輔助方法 ====================
    
    /**
     * 標準化日期格式
     */
    standardizeDate(dateString) {
        if (!dateString) return null;
        
        // 嘗試解析各種日期格式
        const date = new Date(dateString.replace(/[-\/]/g, '/'));
        
        if (isNaN(date.getTime())) {
            console.warn(`無法解析日期: ${dateString}`);
            return dateString;
        }
        
        return date.toISOString().split('T')[0]; // YYYY-MM-DD
    }
    
    /**
     * 清理描述文字
     */
    cleanDescription(description) {
        if (!description) return '';
        
        return description
            .trim()
            .replace(/\s+/g, ' ') // 合併多個空格
            .replace(/[^\w\s\u4e00-\u9fff]/g, '') // 移除特殊字符，保留中文
            .substring(0, 100); // 限制長度
    }
    
    /**
     * 清理商品名稱
     */
    cleanItemName(name) {
        if (!name) return '';
        
        return name
            .trim()
            .replace(/\s+/g, ' ')
            .substring(0, 50);
    }
    
    /**
     * 解析金額
     */
    parseAmount(amount) {
        if (typeof amount === 'number') return amount;
        if (!amount) return 0;
        
        // 移除貨幣符號和逗號
        const cleaned = amount.toString().replace(/[$,\s]/g, '');
        const parsed = parseFloat(cleaned);
        
        return isNaN(parsed) ? 0 : parsed;
    }
    
    /**
     * 交易分類
     */
    categorizeTransaction(description) {
        if (!description) return 'other';
        
        const desc = description.toLowerCase();
        
        if (desc.includes('atm') || desc.includes('cash')) return 'cash';
        if (desc.includes('transfer') || desc.includes('轉帳')) return 'transfer';
        if (desc.includes('salary') || desc.includes('薪資')) return 'salary';
        if (desc.includes('interest') || desc.includes('利息')) return 'interest';
        if (desc.includes('fee') || desc.includes('手續費')) return 'fee';
        if (desc.includes('payment') || desc.includes('付款')) return 'payment';
        
        return 'other';
    }
    
    /**
     * 收據商品分類
     */
    categorizeReceiptItem(name) {
        if (!name) return 'other';
        
        const itemName = name.toLowerCase();
        
        if (itemName.includes('food') || itemName.includes('餐')) return 'food';
        if (itemName.includes('drink') || itemName.includes('飲')) return 'beverage';
        if (itemName.includes('tax') || itemName.includes('稅')) return 'tax';
        
        return 'other';
    }
    
    /**
     * 發票項目分類
     */
    categorizeInvoiceItem(description) {
        if (!description) return 'other';
        
        const desc = description.toLowerCase();
        
        if (desc.includes('service') || desc.includes('服務')) return 'service';
        if (desc.includes('product') || desc.includes('產品')) return 'product';
        if (desc.includes('tax') || desc.includes('稅')) return 'tax';
        
        return 'other';
    }
    
    /**
     * 計算平均值
     */
    calculateMean(numbers) {
        if (!numbers || numbers.length === 0) return 0;
        return numbers.reduce((sum, num) => sum + num, 0) / numbers.length;
    }
    
    /**
     * 計算中位數
     */
    calculateMedian(numbers) {
        if (!numbers || numbers.length === 0) return 0;
        
        const sorted = [...numbers].sort((a, b) => a - b);
        const mid = Math.floor(sorted.length / 2);
        
        return sorted.length % 2 === 0
            ? (sorted[mid - 1] + sorted[mid]) / 2
            : sorted[mid];
    }
    
    /**
     * 計算兩個日期之間的天數
     */
    calculateDaysBetween(startDate, endDate) {
        const start = new Date(startDate);
        const end = new Date(endDate);
        const diffTime = Math.abs(end - start);
        return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    }
    
    /**
     * 計算趨勢
     */
    calculateTrends(monthlyData) {
        if (monthlyData.length < 2) return { trend: 'insufficient_data' };
        
        const netFlows = monthlyData.map(data => data.netFlow);
        const trend = netFlows[netFlows.length - 1] > netFlows[0] ? 'increasing' : 'decreasing';
        
        return {
            trend: trend,
            change: netFlows[netFlows.length - 1] - netFlows[0],
            changePercentage: ((netFlows[netFlows.length - 1] - netFlows[0]) / Math.abs(netFlows[0])) * 100
        };
    }
    
    /**
     * 創建單一項目收據（當無法解析商品項目時）
     */
    createSingleItemReceipt(extractedData) {
        const { totalAmount, merchant, date } = extractedData;
        
        const singleItem = {
            name: merchant || '未知商品',
            amount: totalAmount || 0,
            quantity: 1,
            unitPrice: totalAmount || 0,
            category: 'other'
        };
        
        return {
            processedItems: [singleItem],
            statistics: this.calculateReceiptStatistics([singleItem], totalAmount),
            itemCategories: this.categorizeReceiptItems([singleItem]),
            insights: [{
                type: 'warning',
                title: '數據有限',
                message: '無法解析詳細商品項目，僅顯示總金額'
            }],
            metadata: {
                merchant: merchant,
                date: date,
                totalAmount: totalAmount,
                processedAt: new Date().toISOString()
            }
        };
    }
}

// 全局實例
window.DocumentDataProcessor = DocumentDataProcessor;

console.log('✅ 文檔數據處理器已載入');
