# 🚀 Micro-SaaS 戰略與產品定位 (VaultCaddy HK)

**建立日期**: 2026-04-01
**文件作用**: 記錄我們作為一人團隊的「Micro-SaaS 矩陣」戰略，以及 VaultCaddy 在香港市場的精確產品定位。此文件將幫助未來的 AI 助理理解我們的商業模式（快速變現、低維護、轉戰下一個專案），並確保開發聚焦於「能讓用戶掏錢的核心功能」，避免過度工程化（Over-engineering）。

## 1. 商業目標與模式 (Business Objective)
*   **目標**: 在 1 個月內達到 20,000（預設為 HKD）的營收/MRR。
*   **模式**: Micro-SaaS Studio（微型 SaaS 工作室）。達成目標並穩定運行後，即進入「低維護/自動化」狀態，創辦人轉移精力開發下一個 SaaS。
*   **核心要求**: 產品必須具備「零接觸上手 (Zero-touch onboarding)」、「極低客服需求」與「高自動化」特性。

## 2. 目標受眾與痛點 (Target Audience & Pain Points)
*   **目標客戶**: 香港的小微企業老闆、一人公司 (Solo-preneurs)、Freelancers。
*   **非目標客戶**: 會計師樓 (CPA Firms) - 我們不賣給他們，我們是幫客戶對付他們的高昂收費。
*   **核心痛點 (The "Shoebox" Problem)**: 
    *   香港公司每年必須審計。如果年底將一堆亂七八糟的紙本收據（鞋盒）丟給會計師，會計師會收取高昂的「入帳費 / 整理費 (Bookkeeping / Messy Records Surcharge)」。
    *   老闆想隨時知道公司花了多少錢，但不想學複雜的會計軟體 (如 Xero)。

## 3. 核心產品工作流 (Core Workflow)
1.  **極簡輸入 (Frictionless Input)**: 員工/老闆無需下載 App，直接掃描 QR Code 即可拍照上傳收據。
2.  **AI 自動整理 (Auto-Organization)**: 系統自動辨識日期、金額、商戶，並按月份（如 2026年4月）自動歸檔到雲端資料夾。
3.  **老闆儀表板 (Boss Dashboard)**: 提供極簡的支出視覺化，讓老闆一眼看出錢花在哪。
4.  **CPA 友善匯出 (CPA-Ready Export) [付費關鍵]**: 一鍵匯出會計師能直接使用的 Excel/CSV 報表，附帶收據圖片連結。

## 4. AI 開發指導原則 (AI Development Guidelines)
*   **不做大而全**: 拒絕開發複雜的資產負債表、複式簿記 (Double-entry bookkeeping) 功能。
*   **專注 OCR 準確度**: 香港收據常中英夾雜、字體模糊，這是技術核心。
*   **極致的行動端體驗**: QR Code 掃描後的 Web App 介面必須在 3 秒內完成上傳。