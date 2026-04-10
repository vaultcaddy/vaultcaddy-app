# 🚀 VaultCaddy 2026 衝刺精華與總顧問交接文檔

> **給下一個 Cursor AI Session 的重要訊息**：
> 這是我們之前在 `ai-bank-parser-local` 專案中討論與開發的「精華總結」。我們已經將所有新開發的代碼遷移到了這個正式的 GitHub 專案 (`vaultcaddy-app`)。請你（AI）在開始任何新任務前，**務必閱讀此文檔**，以確保你完全理解我們的商業目標、技術架構與開發進度。

---

## 1. 我們的商業目標與定價死鎖
*   **目標**：在定價死鎖於 **HK$78/月** 的前提下，實現 **HK$100,000/月** 的經常性收入 (MRR)。
*   **用戶數目標**：約 1,282 個付費訂閱用戶（佔香港中小企 0.37%）。
*   **核心策略**：極低的獲客成本 (CAC)、極強的「自傳播性 (Viral Loop)」、以及「零客服 (Zero-touch)」體驗。
*   **總顧問的 To-B 策略**：不只針對老闆 (To-C)，更要主打中小型會計師樓 (CPA Firms)。我們不搶會計師的蛋糕，而是幫他們做最髒最累的 Data Entry，讓他們利潤翻倍。

## 2. 已經完成的核心開發 (已遷移至此專案)
我們已經根據 `REQUIREMENTS.md` (PRD) 完成了以下核心功能的底層開發，並存放在 `src/` 與 `firebase-functions/` 目錄下：

### A. 隔離式員工錄入系統 (Safe-Entry)
*   **`src/views/safe-entry.html`**：一個無狀態 (Stateless) 的手機端上傳頁面。員工掃描 QR Code 進入，拍照 -> AI 辨識 -> 提交。提交後圖片與數據立即從前端清空，員工無法查看歷史紀錄。
*   **`src/views/qr-generator.html`**：老闆專屬的控制面板。老闆可以一鍵生成帶有公司專屬連結的「實體 QR Code 海報」，印出來貼在收銀機旁。

### B. 安全的 AI 呼叫 (總顧問否決了前端直呼 API)
*   **`firebase-functions/index.js`**：我們創建了 `processReceipt` 雲端函數。前端將圖片轉為 Base64 後，呼叫此函數。由後端安全地呼叫 **Qwen3-VL-Plus (DashScope)** 進行 OCR 辨識，提取商戶、日期、金額，並自動歸類到香港 IRD 稅務分類。

### C. 4-Way Export (四大導出矩陣)
*   **`src/services/ixbrl_generator.ts`**：嚴格對標香港稅務局 (IRD) 2025/26 Taxonomy，將開支數據轉換為 e-Filing 專用的 iXBRL (XHTML) 格式。
*   **`src/services/accounting_export.ts`**：完美對接 Xero (包含 Tracking Category) 與 QuickBooks (3 欄式) 的 CSV 導出引擎，實現「0 修改直接 Import」。
*   **`src/services/audit_excel_generator.ts`**：專為會計師審計設計的 Excel 導出。每一筆開支末尾都帶有 Firebase Hot Storage 的「收據原圖超連結」，實現 100% 憑證追溯。

## 3. 下一步衝刺任務 (Next Steps)
我們現在已經具備了「安全、極易落地、會計師愛用」的三大特質。接下來的任務是將這些 TypeScript 服務整合到現有的系統中，準備正式 Promo：

1.  **編譯與整合**：將 `src/services/` 下的 TypeScript 導出引擎編譯為 JavaScript，並整合到老闆後台的 `document-detail-new.js` (或新的 Dashboard) 中。
2.  **Firebase 部署**：將 `firebase-functions/index.js` 部署到 Firebase，並配置 DashScope API Key。
3.  **UI/UX 串接**：確保老闆在後台可以看到員工透過 `safe-entry.html` 上傳的 `pending_verification` 狀態的單據，並進行審核入帳。
4.  **母子帳戶 (暫緩)**：我們討論過「會計師帳號綁定多個 BR 子帳戶」的功能，但決定**先用現有版本去跑市場 Promo**，等有會計師主動來談合作時，再把這個功能當作「Pro / Partner 方案」開發。

> **AI，你現在的任務是：**
> 根據上述精華，協助 User 進行下一步的整合與部署工作。請隨時保持「總顧問」的思維，在確保 HK$78/月 利潤空間的前提下，提供最優的技術與商業建議。
