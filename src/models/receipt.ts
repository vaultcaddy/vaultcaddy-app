import { TaxMapping } from '../config/tax_taxonomy';

export type ExpenseStatus = 'pending_verification' | 'submitted' | 'processed';

export interface ReceiptImage {
  id: string;
  url: string;           // Hot storage URL
  archiveUrl?: string;   // Glacier Deep Archive URL (if older than 2 years)
  uploadDate: Date;
  fileSize: number;      // Must be optimized
}

export interface ExpenseRecord {
  id: string;
  companyBrNumber: string; // 1 account = 1 BR number
  employeeId?: string;     // If uploaded via Safe-Entry Inbox
  
  // OCR Extracted Data
  merchantName: string;
  date: Date;
  amount: number;
  currency: string;
  category: string;        // e.g., 'Transportation', 'Software_SaaS'
  
  // IRD Mapping
  taxMapping?: TaxMapping;
  
  // Link to the physical/digital receipt
  receiptImage: ReceiptImage;
  
  status: ExpenseStatus;
  
  // Audit Trail
  createdAt: Date;
  updatedAt: Date;
}

// Stateless session for employee uploads (Safe-Entry Inbox)
export interface SafeEntrySession {
  sessionId: string;
  employeeId: string;
  companyBrNumber: string;
  expiresAt: Date;
  currentUploads: Partial<ExpenseRecord>[]; // Only visible during active session
}
