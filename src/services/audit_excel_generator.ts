import { ExpenseRecord } from '../models/receipt';
import * as XLSX from 'xlsx'; // 需在 package.json 中安裝 xlsx (SheetJS)

/**
 * Audit Excel Generator (4-Way Export 之一)
 * 
 * 專為會計師審計設計的 Excel 導出工具。
 * 核心要求：每一筆開支末尾必須包含該收據影像的「雲端 URL 連結」，
 * 讓會計師可以直接點擊查看原圖，實現 100% 憑證追溯。
 */
export class AuditExcelGenerator {
  
  /**
   * 生成並下載審計專用 Excel
   * @param records 已審核的開支紀錄數組
   * @param companyName 公司名稱 (用於檔案命名)
   */
  public generateAndDownload(records: ExpenseRecord[], companyName: string): void {
    // 1. 定義 Excel 標題列
    const wsData: any[][] = [
      [
        '交易日期 (Date)', 
        '商戶名稱 (Merchant)', 
        '稅務分類 (IRD Category)', 
        'IRD 標籤代碼 (Tax Tag)', 
        '金額 (Amount HKD)', 
        '可否扣稅 (Deductible)', 
        '狀態 (Status)', 
        '收據原圖連結 (Receipt Image URL)' // 審計最關鍵欄位
      ]
    ];

    // 2. 填入數據
    records.forEach(record => {
      wsData.push([
        record.date.toISOString().split('T')[0],
        record.merchantName,
        record.taxMapping?.label_zh || record.category,
        record.taxMapping?.ird_tag || 'N/A',
        record.amount.toFixed(2),
        record.taxMapping?.deductible ? '是 (Yes)' : '否 (No)',
        record.status === 'processed' ? '已入帳' : record.status,
        record.receiptImage.url // Hot Storage URL
      ]);
    });

    // 3. 創建工作表
    const ws = XLSX.utils.aoa_to_sheet(wsData);

    // 4. 為「收據原圖連結」欄位添加超連結樣式 (Hyperlinks)
    // 這樣會計師在 Excel 點擊網址就能直接打開瀏覽器看圖片
    records.forEach((record, index) => {
      const rowIndex = index + 1; // +1 因為第一行是標題
      const cellRef = XLSX.utils.encode_cell({ r: rowIndex, c: 7 }); // 第 8 列 (索引 7) 是 URL
      
      if (!ws[cellRef]) {
        ws[cellRef] = { t: 's', v: record.receiptImage.url };
      }
      
      // 設置超連結屬性與藍色底線樣式
      ws[cellRef].l = { Target: record.receiptImage.url };
      ws[cellRef].s = { 
        font: { color: { rgb: "0000FF" }, underline: true } 
      };
    });

    // 5. 調整欄寬以提升可讀性
    ws['!cols'] = [
      { wch: 15 }, // Date
      { wch: 25 }, // Merchant
      { wch: 20 }, // Category
      { wch: 30 }, // IRD Tag
      { wch: 15 }, // Amount
      { wch: 15 }, // Deductible
      { wch: 15 }, // Status
      { wch: 60 }  // URL (需要較寬)
    ];

    // 6. 創建工作簿並導出
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'Audit_Trail_審計軌跡');

    const fileName = `Audit_Report_${companyName}_${new Date().toISOString().split('T')[0]}.xlsx`;
    
    // 觸發瀏覽器下載
    XLSX.writeFile(wb, fileName);
  }
}
