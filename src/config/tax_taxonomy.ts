// tax_taxonomy.ts - 2026 IRD iXBRL 標籤映射示例

export interface TaxMapping {
  ird_tag: string;
  label_zh: string;
  deductible: boolean;
  alert?: string;
  tax_incentive?: string;
}

export const IRD_MAPPING: Record<string, TaxMapping> = {
  "Transportation": {
    ird_tag: "ird-tc:TravelingExpenses",
    label_zh: "交通費",
    deductible: true
  },
  "Entertainment": {
    ird_tag: "ird-tc:EntertainmentExpenses",
    label_zh: "交際費",
    deductible: true,
    alert: "注意：比例過高可能引起稅局查帳"
  },
  "Meals": {
    ird_tag: "ird-tc:StaffWelfareMeals", // 視乎是員工餐還是交際
    label_zh: "膳食費",
    deductible: true
  },
  "Fine": {
    ird_tag: "ird-tc:NonDeductibleFines",
    label_zh: "罰款",
    deductible: false, // 稅務上不可扣稅
    alert: "警告：政府罰款不可作稅務扣減"
  },
  "Software_SaaS": {
    ird_tag: "ird-tc:DigitalTransformationExpenditure",
    label_zh: "數位轉型開支",
    deductible: true,
    tax_incentive: "300%_deduction" // 2026 政策紅利：加倍扣稅
  }
};
