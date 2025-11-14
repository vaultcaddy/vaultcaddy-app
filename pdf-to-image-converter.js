/**
 * PDF 轉圖片轉換器
 * 作用：將 PDF 文件轉換為圖片，以便 Vision API 處理
 * 幫助：Vision API 只支持圖片格式，此模塊將 PDF 轉換為 JPG
 * 
 * 使用 PDF.js 庫（Mozilla 開發）
 */

class PDFToImageConverter {
    constructor() {
        this.pdfjsLib = null;
        this.initialized = false;
        console.log('📄 PDF 轉圖片轉換器初始化中...');
        this.loadPDFJS();
    }
    
    /**
     * 載入 PDF.js 庫
     */
    async loadPDFJS() {
        if (window.pdfjsLib) {
            this.pdfjsLib = window.pdfjsLib;
            this.pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';
            this.initialized = true;
            console.log('✅ PDF.js 已載入');
            return;
        }
        
        try {
            // 動態載入 PDF.js
            const script = document.createElement('script');
            script.src = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js';
            script.onload = () => {
                this.pdfjsLib = window.pdfjsLib;
                this.pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';
                this.initialized = true;
                console.log('✅ PDF.js 動態載入成功');
            };
            script.onerror = () => {
                console.error('❌ PDF.js 載入失敗');
            };
            document.head.appendChild(script);
        } catch (error) {
            console.error('❌ PDF.js 載入錯誤:', error);
        }
    }
    
    /**
     * 等待 PDF.js 初始化
     */
    async waitForInit() {
        if (this.initialized) return true;
        
        return new Promise((resolve) => {
            const checkInterval = setInterval(() => {
                if (this.initialized) {
                    clearInterval(checkInterval);
                    resolve(true);
                }
            }, 100);
            
            // 10 秒超時
            setTimeout(() => {
                clearInterval(checkInterval);
                resolve(false);
            }, 10000);
        });
    }
    
    /**
     * 將 PDF 文件轉換為圖片數組
     * @param {File} file - PDF 文件
     * @param {Object} options - 轉換選項
     * @returns {Promise<Array<File>>} 圖片文件數組
     */
    async convertPDFToImages(file, options = {}) {
        console.log(`📄 開始轉換 PDF: ${file.name}`);
        
        // 等待初始化
        const initialized = await this.waitForInit();
        if (!initialized) {
            throw new Error('PDF.js 未能初始化，請刷新頁面重試');
        }
        
        try {
            // 讀取 PDF 文件
            const arrayBuffer = await file.arrayBuffer();
            
            // 載入 PDF 文檔
            const loadingTask = this.pdfjsLib.getDocument({
                data: arrayBuffer,
                cMapUrl: 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/cmaps/',
                cMapPacked: true,
            });
            
            const pdf = await loadingTask.promise;
            console.log(`✅ PDF 載入成功，共 ${pdf.numPages} 頁`);
            
            // 轉換選項
            const scale = options.scale || 2.0; // 2x 縮放以提高清晰度
            const format = options.format || 'image/jpeg'; // JPG 格式
            const quality = options.quality || 0.95; // 95% 質量
            
            // 轉換每一頁
            const imageFiles = [];
            
            for (let pageNum = 1; pageNum <= pdf.numPages; pageNum++) {
                console.log(`📄 正在轉換第 ${pageNum}/${pdf.numPages} 頁...`);
                
                const page = await pdf.getPage(pageNum);
                const viewport = page.getViewport({ scale });
                
                // 創建 canvas
                const canvas = document.createElement('canvas');
                const context = canvas.getContext('2d');
                canvas.width = viewport.width;
                canvas.height = viewport.height;
                
                // 渲染 PDF 頁面到 canvas
                await page.render({
                    canvasContext: context,
                    viewport: viewport
                }).promise;
                
                // 將 canvas 轉換為 Blob
                const blob = await new Promise((resolve) => {
                    canvas.toBlob(resolve, format, quality);
                });
                
                // 創建 File 對象
                const imageFileName = file.name.replace('.pdf', `_page${pageNum}.jpg`);
                const imageFile = new File([blob], imageFileName, { type: format });
                
                imageFiles.push(imageFile);
                console.log(`✅ 第 ${pageNum} 頁轉換完成: ${imageFileName} (${(blob.size / 1024).toFixed(2)} KB)`);
            }
            
            console.log(`🎉 PDF 轉換完成，共生成 ${imageFiles.length} 張圖片`);
            return imageFiles;
            
        } catch (error) {
            console.error('❌ PDF 轉換失敗:', error);
            throw new Error(`PDF 轉換失敗: ${error.message}`);
        }
    }
    
    /**
     * 檢查文件是否為 PDF
     */
    isPDF(file) {
        return file.type === 'application/pdf' || file.name.toLowerCase().endsWith('.pdf');
    }
}

// 創建全局實例
window.pdfToImageConverter = new PDFToImageConverter();

console.log('✅ PDF 轉圖片轉換器已載入');

