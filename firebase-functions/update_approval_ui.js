const fs = require('fs');

const jsPath = 'document-detail-new.js';
let js = fs.readFileSync(jsPath, 'utf8');

// Add an approval button to the invoice details card
const approvalButtonHTML = `
                <div style="grid-column: 1 / -1; margin-top: 1rem; display: flex; justify-content: flex-end;">
                    <button onclick="approveDocument()" id="approveBtn" style="background: #10b981; color: white; border: none; padding: 0.75rem 1.5rem; border-radius: 6px; font-weight: 600; cursor: pointer; display: \${docStatus === 'pending_verification' ? 'block' : 'none'}; box-shadow: 0 4px 6px -1px rgba(16, 185, 129, 0.2);">
                        <i class="fas fa-check-circle" style="margin-right: 0.5rem;"></i> 審核通過 (Approve)
                    </button>
                    <div id="approvedBadge" style="background: #ecfdf5; color: #059669; padding: 0.75rem 1.5rem; border-radius: 6px; font-weight: 600; border: 1px solid #10b981; display: \${docStatus !== 'pending_verification' ? 'block' : 'none'};">
                        <i class="fas fa-check-double" style="margin-right: 0.5rem;"></i> 已入帳 (Processed)
                    </div>
                </div>
`;

// Insert the button before the closing div of the invoice-details-grid
js = js.replace('</div>\n            <style>', approvalButtonHTML + '            </div>\n            <style>');

// Add the approveDocument function
const approveFunction = `
// ============================================
// 審核通過功能 (Approve Document)
// ============================================
window.approveDocument = async function() {
    if (!currentDocument || !currentDocument.id) return;
    
    const btn = document.getElementById('approveBtn');
    const badge = document.getElementById('approvedBadge');
    
    try {
        btn.innerHTML = '<i class="fas fa-spinner fa-spin" style="margin-right: 0.5rem;"></i> 處理中...';
        btn.disabled = true;
        
        // 這裡應該呼叫 Firebase Firestore 更新狀態
        const db = firebase.firestore();
        await db.collection('documents').doc(currentDocument.id).update({
            status: 'processed',
            approvedAt: firebase.firestore.FieldValue.serverTimestamp()
        });
        
        // 更新本地狀態
        currentDocument.status = 'processed';
        
        // 切換 UI
        btn.style.display = 'none';
        badge.style.display = 'block';
        
        // 顯示成功提示
        const toast = document.createElement('div');
        toast.style.cssText = 'position: fixed; bottom: 20px; right: 20px; background: #10b981; color: white; padding: 1rem 2rem; border-radius: 8px; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); z-index: 9999; font-weight: 600;';
        toast.innerHTML = '<i class="fas fa-check-circle" style="margin-right: 0.5rem;"></i> 單據已成功入帳！';
        document.body.appendChild(toast);
        
        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transition = 'opacity 0.5s ease';
            setTimeout(() => document.body.removeChild(toast), 500);
        }, 3000);
        
    } catch (error) {
        console.error('審核失敗:', error);
        alert('審核失敗: ' + error.message);
        btn.innerHTML = '<i class="fas fa-check-circle" style="margin-right: 0.5rem;"></i> 審核通過 (Approve)';
        btn.disabled = false;
    }
};
`;

// Append the function to the end of the file
if (!js.includes('window.approveDocument')) {
    js += '\n' + approveFunction;
}

fs.writeFileSync(jsPath, js);
console.log('Added approval UI and logic to document-detail-new.js');
