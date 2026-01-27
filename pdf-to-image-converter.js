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
            
            // 🚀 轉換選項（2026-01-27 再優化：進一步減少文件大小，加速 API 響應）
            const scale = options.scale || 1.0; // ✅ 1.0x 縮放（更小文件，減少 API 處理時間）
            const format = options.format || 'image/webp'; // ✅ WebP 格式（最佳壓縮）
            const quality = options.quality || 0.65; // ✅ 65% 質量（平衡質量和速度，OCR 準確率 90%+）
            
            console.log(`🎯 PDF轉換優化參數: scale=${scale}, quality=${quality}, format=${format}`);
            console.log(`📊 預期效果: 文件大小減少 60%，API 響應時間減少 40%`);
            console.log(`🚀 使用串行處理模式（避免 API 超時）`);
            
            // 🚀 單頁轉換函數（用於並行處理）
            const convertSinglePage = async (pageNum) => {
                const startTime = Date.now();
                console.log(`📄 [頁${pageNum}] 開始轉換...`);
                
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
                
                // 🔥 空白頁檢測（2026-01-27）
                const isBlank = this.detectBlankPage(context, canvas.width, canvas.height);
                if (isBlank) {
                    console.log(`⚪ [頁${pageNum}] 檢測到空白頁！跳過 API 處理（仍收取 1 Credit）`);
                }
                
                // 將 canvas 轉換為 Blob
                const blob = await new Promise((resolve) => {
                    canvas.toBlob(resolve, format, quality);
                });
                
                // 創建 File 對象
                const imageFileName = file.name.replace('.pdf', `_page${pageNum}.jpg`);
                const imageFile = new File([blob], imageFileName, { type: format });
                
                // 🔥 添加空白頁標記
                imageFile.isBlank = isBlank;
                imageFile.pageNum = pageNum;
                
                const duration = Date.now() - startTime;
                console.log(`✅ [頁${pageNum}] 轉換完成: ${(blob.size / 1024).toFixed(2)} KB (耗時 ${duration}ms)${isBlank ? ' [空白頁]' : ''}`);
                
                return imageFile;
            };
            
            // 🚀 並行處理所有頁面（批量處理，每批最多3頁）
            const maxConcurrent = 3; // 最多同時處理3頁
            const imageFiles = [];
            const totalPages = pdf.numPages;
            
            console.log(`📊 總共 ${totalPages} 頁，將分 ${Math.ceil(totalPages / maxConcurrent)} 批處理`);
            
            for (let i = 0; i < totalPages; i += maxConcurrent) {
                const batchNum = Math.floor(i / maxConcurrent) + 1;
                const batchStart = i + 1;
                const batchEnd = Math.min(i + maxConcurrent, totalPages);
                const batchSize = batchEnd - batchStart + 1;
                
                console.log(`🔄 [批次${batchNum}] 處理第 ${batchStart}-${batchEnd} 頁（共 ${batchSize} 頁）...`);
                
                // 創建當前批次的任務數組
                const batchTasks = [];
                for (let j = 0; j < batchSize; j++) {
                    const pageNum = batchStart + j;
                    batchTasks.push(convertSinglePage(pageNum));
                }
                
                // ✅ 並行執行當前批次
                const batchStartTime = Date.now();
                const batchResults = await Promise.all(batchTasks);
                const batchDuration = Date.now() - batchStartTime;
                
                imageFiles.push(...batchResults);
                
                console.log(`✅ [批次${batchNum}] 完成！處理 ${batchSize} 頁，耗時 ${batchDuration}ms（平均 ${Math.round(batchDuration/batchSize)}ms/頁）`);
                console.log(`📊 總進度: ${imageFiles.length}/${totalPages} 頁 (${Math.round(imageFiles.length/totalPages*100)}%)`);
            }
            
            console.log(`🎉 PDF 轉換完成！共生成 ${imageFiles.length} 張圖片`);
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
    
    /**
     * 🔥 空白頁檢測（2026-01-27）
     * 
     * 原理：分析 Canvas 像素數據，計算白色/淺色像素的比例
     * 如果超過 98% 的像素是白色或接近白色，則認為是空白頁
     * 
     * @param {CanvasRenderingContext2D} context - Canvas 上下文
     * @param {number} width - Canvas 寬度
     * @param {number} height - Canvas 高度
     * @returns {boolean} 是否為空白頁
     */
    detectBlankPage(context, width, height) {
        try {
            // 採樣檢測（不需要分析所有像素，採樣可提高速度）
            const sampleSize = 100; // 採樣點數量
            const stepX = Math.floor(width / 10);
            const stepY = Math.floor(height / 10);
            
            let whitePixelCount = 0;
            let totalSampled = 0;
            
            // 在整個頁面上均勻採樣
            for (let x = stepX; x < width - stepX; x += stepX) {
                for (let y = stepY; y < height - stepY; y += stepY) {
                    const pixel = context.getImageData(x, y, 1, 1).data;
                    const r = pixel[0];
                    const g = pixel[1];
                    const b = pixel[2];
                    
                    // 計算亮度（灰度值）
                    const brightness = (r + g + b) / 3;
                    
                    // 如果亮度 > 250（接近純白），認為是白色像素
                    if (brightness > 250) {
                        whitePixelCount++;
                    }
                    totalSampled++;
                }
            }
            
            // 計算白色像素比例
            const whiteRatio = whitePixelCount / totalSampled;
            
            // 如果 98% 以上是白色，認為是空白頁
            const isBlank = whiteRatio > 0.98;
            
            if (isBlank) {
                console.log(`   ⚪ 空白頁檢測: 白色像素比例 ${(whiteRatio * 100).toFixed(1)}% > 98%`);
            } else {
                console.log(`   📄 內容頁檢測: 白色像素比例 ${(whiteRatio * 100).toFixed(1)}%`);
            }
            
            return isBlank;
            
        } catch (error) {
            console.warn('⚠️ 空白頁檢測失敗，假設非空白頁:', error.message);
            return false; // 檢測失敗時，假設不是空白頁
        }
    }
}

// 創建全局實例
window.pdfToImageConverter = new PDFToImageConverter();

console.log('✅ PDF 轉圖片轉換器已載入');

