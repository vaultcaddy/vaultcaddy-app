const fs = require('fs');

const htmlPath = 'document-detail.html';
let html = fs.readFileSync(htmlPath, 'utf8');

// Replace the openVaultcaddyExportMenuInternal function
const newMenuFunc = `    function openVaultcaddyExportMenuInternal() {
        const menu = document.getElementById('vaultcaddyExportMenu');
        const overlay = document.getElementById('vaultcaddyExportOverlay');
        const btn = document.getElementById('vaultcaddyExportBtn');
        
        if (!menu) return;
        
        const doc = window.currentDocument;
        const docType = doc?.type || doc?.documentType || '';
        
        let menuHTML = '<div style="padding: 0.5rem 0; background: #ffffff;">';
        
        menuHTML += \`
            <div style="padding: 0.5rem 1rem; font-size: 0.75rem; font-weight: 600; color: #6b7280; text-transform: uppercase; letter-spacing: 0.05em;">Hong Kong Tax & Audit</div>
            
            <button onclick="vaultcaddyExportDocument('ixbrl')" class="export-menu-item" style="width: 100%; text-align: left; padding: 0.75rem 1rem; border: none; background: transparent; cursor: pointer; display: flex; align-items: center; gap: 0.75rem; color: #374151; transition: background 0.2s; background: linear-gradient(90deg, rgba(16,185,129,0.05) 0%, transparent 100%);">
                <i class="fas fa-file-code" style="color: #10b981; width: 20px;"></i>
                <div>
                    <div style="font-weight: 600;">🇭🇰 iXBRL (IRD e-Filing)</div>
                    <div style="font-size: 0.75rem; color: #059669; font-weight: 500;">Taxonomy 2025/26 Compliant</div>
                </div>
            </button>
            
            <button onclick="vaultcaddyExportDocument('audit_excel')" class="export-menu-item" style="width: 100%; text-align: left; padding: 0.75rem 1rem; border: none; background: transparent; cursor: pointer; display: flex; align-items: center; gap: 0.75rem; color: #374151; transition: background 0.2s;">
                <i class="fas fa-file-excel" style="color: #059669; width: 20px;"></i>
                <div>
                    <div style="font-weight: 500;">📊 Audit Excel</div>
                    <div style="font-size: 0.75rem; color: #6b7280;">Includes Receipt Image Links</div>
                </div>
            </button>
            
            <div style="padding: 0.5rem 1rem; font-size: 0.75rem; font-weight: 600; color: #6b7280; text-transform: uppercase; letter-spacing: 0.05em; margin-top: 0.5rem;">Accounting Software</div>
            
            <button onclick="vaultcaddyExportDocument('xero_csv')" class="export-menu-item" style="width: 100%; text-align: left; padding: 0.75rem 1rem; border: none; background: transparent; cursor: pointer; display: flex; align-items: center; gap: 0.75rem; color: #374151; transition: background 0.2s;">
                <i class="fas fa-file-csv" style="color: #0ea5e9; width: 20px;"></i>
                <div>
                    <div style="font-weight: 500;">Xero CSV</div>
                    <div style="font-size: 0.75rem; color: #6b7280;">Ready to Import</div>
                </div>
            </button>
            
            <button onclick="vaultcaddyExportDocument('qbo_csv')" class="export-menu-item" style="width: 100%; text-align: left; padding: 0.75rem 1rem; border: none; background: transparent; cursor: pointer; display: flex; align-items: center; gap: 0.75rem; color: #374151; transition: background 0.2s;">
                <i class="fas fa-file-csv" style="color: #2ca01c; width: 20px;"></i>
                <div>
                    <div style="font-weight: 500;">QuickBooks CSV</div>
                    <div style="font-size: 0.75rem; color: #6b7280;">3-Column Format</div>
                </div>
            </button>
        \`;
        
        menuHTML += '</div>';
        menu.innerHTML = menuHTML;
        
        menu.style.display = 'block';
        overlay.style.display = 'block';
        
        // ... (rest of the positioning logic remains same, we will just regex replace the innerHTML part)
`;

// It's safer to use regex to replace the function body
const regex = /function openVaultcaddyExportMenuInternal\(\) \{[\s\S]*?menu\.innerHTML = menuHTML;/;
html = html.replace(regex, newMenuFunc + '\n        menu.innerHTML = menuHTML;');

fs.writeFileSync(htmlPath, html);
console.log('Updated document-detail.html export menu UI');
