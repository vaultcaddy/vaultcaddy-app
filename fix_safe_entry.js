const fs = require('fs');

const htmlPath = 'src/views/safe-entry.html';
let html = fs.readFileSync(htmlPath, 'utf8');

// The safe-entry.html is missing the companyId in the processReceiptFn call.
// Let's add logic to get companyId from URL params and pass it to the backend.

const newProcessLogic = `        // Call Firebase Cloud Function (Secure Backend OCR)
        async function processReceiptWithAI(file) {
            uploadSection.style.display = 'none';
            loadingOverlay.style.display = 'flex';

            try {
                const base64Image = await fileToBase64(file);
                
                // 從 URL 獲取 companyId (老闆生成的 QR Code 會帶這個參數)
                const urlParams = new URLSearchParams(window.location.search);
                const companyId = urlParams.get('c') || 'demo_company_123'; // 預設給個 demo ID 防呆
                
                // 呼叫 Firebase Cloud Function
                const processReceiptFn = firebase.functions('asia-east1').httpsCallable('processReceipt');
                const response = await processReceiptFn({ 
                    base64Image: base64Image,
                    companyId: companyId
                });
                
                if (!response.data.success) {
                    throw new Error('AI Processing failed on backend');
                }

                currentExtractedData = response.data.data;

                // Update UI
                document.getElementById('valMerchant').textContent = currentExtractedData.merchantName || '未知商戶';
                document.getElementById('valDate').textContent = currentExtractedData.date || new Date().toISOString().split('T')[0];
                document.getElementById('valAmount').textContent = \`HK$ \${(currentExtractedData.amount || 0).toFixed(2)}\`;
                document.getElementById('valCategory').textContent = currentExtractedData.categoryLabel || '未分類';

                loadingOverlay.style.display = 'none';
                resultSection.style.display = 'block';
            } catch (error) {
                console.error('Backend AI Processing Error:', error);
                // 顯示後端回傳的具體錯誤 (例如額度耗盡)
                const errorMsg = error.message || 'AI 辨識失敗，請確保圖片清晰或重試。';
                alert(errorMsg);
                resetUpload();
            }
        }`;

const regex = /\/\/ Call Firebase Cloud Function \(Secure Backend OCR\)[\s\S]*?resetUpload\(\);\n            \}\n        \}/;
html = html.replace(regex, newProcessLogic);

// Also update the submitReceipt to use companyId and the correct collection 'documents' instead of 'expenses' to match the dashboard
const newSubmitLogic = `        // Submit to Firebase (Reusing existing setup)
        async function submitReceipt() {
            if (!currentFile || !currentExtractedData) return;

            resultSection.style.display = 'none';
            loadingOverlay.style.display = 'flex';
            loadingOverlay.querySelector('h3').textContent = '正在加密上傳...';

            try {
                // 1. Upload Image to Firebase Hot Storage
                const storageRef = firebase.storage().ref();
                const fileName = \`receipts_hot/\${Date.now()}_\${currentFile.name}\`;
                const fileRef = storageRef.child(fileName);
                await fileRef.put(currentFile);
                const downloadURL = await fileRef.getDownloadURL();

                // 從 URL 獲取 companyId
                const urlParams = new URLSearchParams(window.location.search);
                const companyId = urlParams.get('c') || 'demo_company_123';

                // 2. Save Data to Firestore with pending_verification status
                // 這裡會自動繼承你在 firebase-config.js 中的配置
                await firebase.firestore().collection('documents').add({
                    companyId: companyId,
                    merchantName: currentExtractedData.merchantName,
                    date: currentExtractedData.date,
                    totalAmount: currentExtractedData.amount,
                    category: currentExtractedData.categoryLabel,
                    imageUrl: downloadURL,
                    status: 'pending_verification', // PRD 要求的狀態流轉起點
                    uploadDate: firebase.firestore.FieldValue.serverTimestamp(),
                    source: 'safe-entry'
                });

                // Clear session data immediately (Stateless Safe-Entry)
                fileInput.value = '';
                previewImage.src = '';
                currentFile = null;
                currentExtractedData = null;
                
                loadingOverlay.style.display = 'none';
                successSection.style.display = 'block';
            } catch (error) {
                console.error('Upload Error:', error);
                alert('上傳失敗，請檢查網絡連線。');
                resetUpload();
            }
        }`;

const regexSubmit = /\/\/ Submit to Firebase \(Reusing existing setup\)[\s\S]*?resetUpload\(\);\n            \}\n        \}/;
html = html.replace(regexSubmit, newSubmitLogic);

// Add image compression before uploading to AI
const compressionLogic = `        // Convert file to Base64 for Qwen-VL API (with Compression)
        function fileToBase64(file) {
            return new Promise((resolve, reject) => {
                const reader = new FileReader();
                reader.readAsDataURL(file);
                reader.onload = (event) => {
                    const img = new Image();
                    img.src = event.target.result;
                    img.onload = () => {
                        const canvas = document.createElement('canvas');
                        const ctx = canvas.getContext('2d');
                        
                        // 限制最大寬高為 1024px (節省 Qwen Token 費用)
                        const MAX_WIDTH = 1024;
                        const MAX_HEIGHT = 1024;
                        let width = img.width;
                        let height = img.height;

                        if (width > height) {
                            if (width > MAX_WIDTH) {
                                height *= MAX_WIDTH / width;
                                width = MAX_WIDTH;
                            }
                        } else {
                            if (height > MAX_HEIGHT) {
                                width *= MAX_HEIGHT / height;
                                height = MAX_HEIGHT;
                            }
                        }

                        canvas.width = width;
                        canvas.height = height;
                        ctx.drawImage(img, 0, 0, width, height);
                        
                        // 壓縮為 JPEG，品質 0.7
                        const compressedBase64 = canvas.toDataURL('image/jpeg', 0.7);
                        resolve(compressedBase64);
                    };
                    img.onerror = error => reject(error);
                };
                reader.onerror = error => reject(error);
            });
        }`;

const regexBase64 = /\/\/ Convert file to Base64 for Qwen-VL API[\s\S]*?\}\);\n        \}/;
html = html.replace(regexBase64, compressionLogic);

fs.writeFileSync(htmlPath, html);
console.log('Updated safe-entry.html API connection and compression');
