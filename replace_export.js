const fs = require('fs');
let content = fs.readFileSync('firstproject.html', 'utf8');

const newExportDocuments = `        window.exportDocuments = async function(format) {
            try {
                // 獲取選中的文檔
                const checkboxes = document.querySelectorAll('.document-checkbox:checked');
                const selectedDocIds = Array.from(checkboxes).map(cb => cb.dataset.docId);
                
                if (selectedDocIds.length === 0) {
                    alert('請先選擇要導出的文檔');
                    return;
                }
                
                // 關閉菜單
                closeExportMenu();
                
                // 顯示加載狀態
                const exportBtn = document.getElementById('export-btn-desktop');
                const originalText = exportBtn ? exportBtn.innerHTML : '';
                if (exportBtn) {
                    exportBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> 導出中...';
                    exportBtn.disabled = true;
                }
                
                // 獲取文檔數據
                const docsToExport = window.allDocuments.filter(doc => selectedDocIds.includes(doc.id));
                
                logger.log(\`📤 開始導出 \${docsToExport.length} 個文檔，格式: \${format}\`);
                
                if (format === 'universal_csv') {
                    const blob = window.exportManager.exportToCSV(docsToExport);
                    const fileName = \`vaultcaddy_export_\${new Date().toISOString().split('T')[0]}.csv\`;
                    window.exportManager.downloadFile(blob, fileName);
                    alert(\`✅ 導出成功！\\n已下載 1 個 CSV 文件\`);
                } else {
                    alert('不支持的導出格式');
                }
                
                // 恢復按鈕狀態
                if (exportBtn) {
                    exportBtn.innerHTML = originalText;
                    exportBtn.disabled = false;
                }
                
                // 取消全選
                const selectAllCheckbox = document.getElementById('select-all-checkbox');
                if (selectAllCheckbox) {
                    selectAllCheckbox.checked = false;
                    toggleAllDocuments(selectAllCheckbox);
                }
                
            } catch (error) {
                console.error('❌ 導出失敗:', error);
                alert('導出失敗: ' + error.message);
                
                // 恢復按鈕狀態
                const exportBtn = document.getElementById('export-btn-desktop');
                if (exportBtn) {
                    exportBtn.innerHTML = '<i class="fas fa-file-export"></i> <span>Export</span>';
                    exportBtn.disabled = false;
                }
            }
        };`;

// Use regex to replace the function
content = content.replace(/window\.exportDocuments = async function\(format\) \{[\s\S]*?catch \(error\) \{[\s\S]*?\}\n        \};/, newExportDocuments);

fs.writeFileSync('firstproject.html', content);
console.log('Replaced exportDocuments');
