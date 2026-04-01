# VaultCaddy 總顧問指導文件（2026-03-31）

> **文件作用說明**：
> 本文件作為一人團隊的最高決策指導，幫助AI（Cursor/Grok/Claude）及創辦人快速對齊商業優先級。
> 所有未來功能開發、營銷行動、Prompt修改、文件更新，**必須先參考本文件**。
> 作用：避免重複討論「要不要轉做Grant Hunter/BizGuard」，聚焦「先把現有VaultCaddy做到月收HK$20k+」。

## 1. 核心定位（不可動搖）
- **產品名稱**：VaultCaddy - 香港小店扣稅神器
- **核心價值**：解決「收據鞋盒地獄 + IRD扣稅判斷難」痛點
- **目標客戶**：
  1. 香港實體小店老闆（餐飲、零售、美容、髮型屋）
  2. 中小型執業會計師 / 公司秘書（最重要渠道）
- **定價**：HK$78/月（維持極致性價比），未來加Pro版HK$298
- **差異化**：比Dext便宜70%，專為香港小店+IRD扣稅優化，AI自動給tax_deductibility評級

## 2. 對之前對話的總顧問裁決
之前多次討論轉向「Grant Hunter AI」（資助申請）或「BizGuard AI」（全合規守護），**我的最終意見**：
- **VaultCaddy不是7.5分產品，而是正確的起點**。
- **不要現在從零做新SaaS**：已有OCR、銀行對賬、QBO匯出、香港銀行支援等真實功能，重新開始會浪費已投入時間。
- **正確路徑**：**先衝宣傳 + 優化現有產品（Roadmap Phase 1）** → 收入穩定後再自然演進到BizGuard（Phase 2）。
- 原因：宣傳難度 > 建立產品。會計師渠道一旦打通，獲客成本極低且churn低。

## 3. 當前最優先三大行動（必須按順序執行）
### A. 內容自動化 + 會計師/公司秘書渠道聯盟（最高優先）
這是天才級杠杆。會計師最痛「客戶年底才拎一鞋盒單據」。

- 使用 `CONTENT_PROMPT_VAULTCADDY.md` 自動生成所有 FB/LinkedIn/微信內容
- **即將提供的Cold Email模板**（見下方）

### B. 優化 Landing Page + SEO
- 強化 `hk-shop-landing.html` 的會計師賣點與 SEO
- 加入明顯 CTA 引導小店老闆推薦給會計師

### C. 優化核心Prompt與匯出 + 裂變機制
- 確保`qwen-vl-max-processor.js`已使用`PROMPT_HK_SHOP_IRD.md`中的最新Prompt。
- `export-manager.js`必須包含`expense_category`和`tax_deductibility`欄位。
- 每週發3-5篇內容 + 加入「推薦1個朋友，雙方免1個月月費」。

## 4. 產品演進路線圖（已確認）
**Phase 1 (現在-下個月)**: 完善收據核心 + 渠道獲客
**Phase 2 (收入穩定後)**: 加入周年申報、稅表到期WhatsApp警報 → 命名為「BizGuard模組」
**Phase 3**: 整合政府資助推薦（Grant Hunter功能）

**絕不**：同時開發多個大功能。每次只加1個高價值功能。

## 5. 技術與文件規範
- 所有新Prompt文件必須在開頭加「**文件作用說明**」。
- 修改JS/HTML時，先Read現有文件，再用StrReplace精準編輯。
- 著陸頁必須強調「會計師最愛的扣稅評級」和「5秒上傳」。

---

**下一步建議**（請按此順序執行）：
1. 使用 `CONTENT_PROMPT_VAULTCADDY.md` 自動生成內容（已完成）
2. 優化 `hk-shop-landing.html` + SEO（下一步）
3. 撰寫會計師 Cold Email 模板
4. 建立內容發佈日曆與裂變機制
5. 檢查核心 Prompt 與匯出功能

作為你的總顧問，我會確保每一步都**文件化 + 可被AI後續使用**，讓一人團隊效率最大化。

你現在想從哪一步開始？（請回覆「開始寫Cold Email」或指定其他）
