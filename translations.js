// 多語言翻譯文件
const translations = {
    'en': {
        // 導航
        'nav_features': 'Features',
        'nav_pricing': 'Pricing', 
        'nav_dashboard': 'Dashboard',
        'nav_api': 'API',
        'nav_credits': 'Credits:',
        'nav_login': 'Log in →',
        
        // Hero區域
        'hero_title': 'Process Financial Documents in <span class="gradient-text">10-30 Seconds</span><br>Let AI Handle the Tedious Work, You Focus on Growth',
        'hero_subtitle': 'Auto-convert bank statements, invoices, receipts to Excel/CSV/QuickBooks format<br><strong>98% Accuracy</strong> • <strong>Save 90% Time</strong> • <strong>Zero Human Errors</strong>',
        'upload_title': 'Select Document Type and Upload Files',
        'select_model': 'Choose Conversion Mode',
        'model_bank_title': 'Bank Statement Converter',
        'model_bank_desc': 'Extract bank statement data automatically',
        'model_invoice_title': 'Invoice Converter',
        'model_invoice_desc': 'AI invoice data recognition',
        'model_receipt_title': 'Receipt Converter',
        'model_receipt_desc': 'AI receipt data scanning',
        'model_general_title': 'General Document Converter',
        'model_general_desc': 'Universal document processor',
        'upload_text': 'Drop PDF file here <span class="or">Or</span> <button class="browse-btn">Browse</button>',
        'browse_btn': 'Browse',
        
        // 節省時間區域
        'time_saving_title': 'Modernize Your Bookkeeping',
        'time_saving_subtitle': 'Automate financial document processing with AI and focus on what truly matters - growing your business',
        
        // 功能特色
        'feature_easy_title': 'Automated Data Extraction',
        'feature_easy_desc': 'Our AI system accurately extracts key financial data from various document types, saving you hours of manual data entry.',
        'feature_secure_title': 'Accounting Software Integration',
        'feature_secure_desc': 'Our tools are designed to work seamlessly with popular accounting software like QuickBooks, Xero, and more.',
        'feature_flexible_title': 'Enhanced Security',
        'feature_flexible_desc': 'Bank-level encryption and secure cloud storage ensure your sensitive financial documents are always protected.',
        'feature_quick_title': 'Streamlined Workflow',
        'feature_quick_desc': 'Let our proprietary software handle the heavy lifting and reduce your bookkeeping time by up to 80%.',
        'feature_batch_title': 'Multi-Format Conversion',
        'feature_batch_desc': 'Easily convert bank statements, invoices, and receipts to Excel, JSON, CSV, and QuickBooks Online formats.',
        'feature_error_title': 'AI-Powered Accuracy',
        'feature_error_desc': 'Our advanced AI ensures high-precision data extraction and conversion, minimizing errors and saving you valuable time.',
        
        // 價格區域
        'pricing_badge': 'FAIR AND AFFORDABLE PRICING',
        'pricing_title': 'Easy Bank Statement Processing',
        'pricing_subtitle': 'Join thousands of businesses saving time on financial data entry. No hidden fees, cancel anytime.',
        'pricing_monthly': 'Monthly bill',
        'pricing_yearly': 'Yearly bill (SAVE 20%)',
        'plan_free': 'Free Plan',
        'plan_pro': 'Professional Plan',
        'plan_enterprise': 'Enterprise Plan',
        'popular_badge': 'Most Popular',
        'free_feature_1': 'Up to 3 pages per day',
        'free_feature_2': 'Basic conversion features',
        'free_feature_3': 'CSV format output',
        'pro_feature_1': 'Unlimited pages',
        'pro_feature_2': 'All format outputs',
        'pro_feature_3': 'Batch processing',
        'pro_feature_4': 'Priority support',
        'enterprise_feature_1': 'Unlimited processing',
        'enterprise_feature_2': 'API access',
        'enterprise_feature_3': 'Dedicated support',
        'enterprise_feature_4': 'Custom integration',
        'cta_free': 'Start Free Trial',
        'cta_pro': 'Get Started',
        'cta_enterprise': 'Contact Us',
        
        // FAQ
        'faq_title': 'Frequently Asked Questions',
        'faq_subtitle': 'Our comprehensive AI BANK PARSER FAQ dives deep into everything you need to know.',
        'faq_q1': 'What is AI Bank Parser Converter?',
        'faq_a1': 'AI Bank Parser is specialized software designed to convert your PDF bank statements into CSV, EXCEL, QBO, or JSON formats. It detects and extracts transaction data stored in tables and generates a new file quickly and accurately.',
        'faq_q2': 'How does it work?',
        'faq_a2': 'Upload your PDF bank statements, and our software will detect tables, extract their contents, and convert them into the format you need. The processed file will be automatically downloaded to your computer.',
        'faq_q3': 'Is my data secure?',
        'faq_a3': 'Absolutely. We prioritize your data privacy and security throughout the conversion process.',
        'faq_q4': 'How much does it cost?',
        'faq_a4': 'We offer a range of subscription plans to suit your needs. Try it for free, then choose a plan that works best for you.',
        'faq_q5': 'Can I use it for free?',
        'faq_a5': 'Yes! You can convert up to 3 pages per day for free. We also offer paid subscriptions for higher conversion needs.',
        'faq_q6': 'How long does the conversion take?',
        'faq_a6': 'The conversion process can take seconds or minutes, depending on the size of your file, saving you hours of manual data entry.',
        'faq_q7': 'Who can benefit from using VaultCaddy?',
        'faq_a7_accountant': 'Accountants:',
        'faq_a7_accountant_desc': 'Speed up working with client bank statements.',
        'faq_a7_finance': 'Finance Specialists:',
        'faq_a7_finance_desc': 'Enhance efficiency in analysis and reporting.',
        'faq_a7_business': 'Business Owners:',
        'faq_a7_business_desc': 'Gain better financial insight for budgeting and planning.',
        'faq_q8': 'What if it doesn\'t work with my bank?',
        'faq_a8': 'If our software doesn\'t work with your bank, contact us through the chat widget at the bottom right of the page. Provide your email, and we\'ll adjust our script to accommodate your needs.',
        'faq_contact': 'Have more questions? Reach out through our chat widget or email us directly. customer support team.',
        
        // 部落格
        'blog_title': 'Why Use AI Bank Parser to Convert PDF Bank Statements into CSV?',
        'blog_intro': 'In today\'s fast-paced financial world, efficiency and accuracy are paramount. Converting PDF bank statements into CSV format can be a tedious and error-prone task if done manually. Enter the AI Bank Parser, a powerful tool designed to automate this process, saving you time and reducing errors. In this blog post, we\'ll explore why using an AI Bank Parser is beneficial for converting your bank statements into CSV format.',
        
        // 頁尾
        'footer_privacy': 'Privacy Policy',
        'footer_terms': 'Terms & Conditions',
        'footer_gdpr': 'GDPR',
        'footer_copyright': '© 2025 Made with VaultCaddy 版權所有',
        
        // 上傳狀態
        'upload_processing': 'Processing...',
        'upload_complete': 'Processing Complete!',
        'upload_success_msg': 'Your file has been successfully converted and downloaded to your computer.',
        'upload_more': 'Process More Files',
        'upload_selected': 'Selected: ',
        'upload_reset': 'Select Again',
        
        // Dashboard 專用
        'dashboard_title': 'Dashboard',
        'sidebar_bank_statements': 'Bank Statements',
        'sidebar_invoices': 'Invoices', 
        'sidebar_receipts': 'Receipts',
        'sidebar_general': 'General Documents',
        'page_title_dashboard': 'Dashboard - VaultCaddy',
        'bank_statement_processor': 'Bank Statement Processor',
        'invoice_processor': 'Invoice Processor',
        'receipt_processor': 'Receipt Processor',
        'general_processor': 'General Document Processor',
        'manage_view_documents': 'Manage and view your documents',
        'bank_statement_details': 'Bank Statement Details & Notes',
        'models': 'Models',
        'configurations': 'CONFIGURATIONS',
        'account': 'Account',
        'billing': 'Billing',
        'filter_document_name': 'Filter document name...',
        'upload_files': 'Upload files',
        'export': 'Export',
        'view': 'View',
        'document': 'Document',
        'invoice_date': 'Invoice Date',
        'items_count': 'Items',
        'balance_info': 'Balance Info',
        'status': 'Status',
        'review_status': 'Review Status',
        'notes': 'Notes',
        'date_uploaded': 'Date Uploaded',
        'actions': 'Actions',
        'back_to_dashboard': 'Back to dashboard',
        'reconciliation_status': 'Reconciliation Status',
        'remaining_credits': 'Remaining Credits',
        'transactions': 'transactions',
        'in_progress': 'In Progress',
        'row_s_selected': 'row(s) selected',
        'rows_per_page': 'Rows per page',
        'page_of': 'Page',
        'of': 'of',
        'transactions_reconciled': 'transactions reconciled',
        'complete': 'Complete',
        'transactions_title': 'Transactions',
        'showing_transactions': 'Showing',
        'to': 'to',
        'average_processing_time': 'Average Processing Time',
        'processing_success_rate': 'Processing Success Rate',
        
        // Account 页面
        'account_settings': 'Account Settings',
        'manage_account_info': 'Manage your account info.',
        'profile': 'Profile',
        'security': 'Security',
        'profile_details': 'Profile details',
        'update_profile': 'Update profile',
        'email_addresses': 'Email addresses',
        'primary': 'Primary',
        'add_email_address': 'Add email address',
        'connected_accounts': 'Connected accounts',
        'connect_account': 'Connect account',
        'cancel': 'Cancel',
        'save': 'Save',
        
        // Billing 页面
        'billing_credits': 'Billing & Credits',
        'manage_billing_subscription': 'Manage your billing, subscription, and credits',
        'current_plan': 'Current plan:',
        'manage_current_subscription': 'Manage your current subscription plan',
        'manage': 'Manage',
        'add_credits': 'Add credits',
        'add_credits_description': 'Add credits to your account to convert more documents.',
        'subscription_plans': 'Subscription plans',
        'monthly': 'Monthly',
        'yearly': 'Yearly (Save 20%)',
        'basic': 'Basic',
        'pro': 'Pro',
        'business': 'Business',
        'perfect_for_individuals': 'Perfect for individuals and freelancers.',
        'small_businesses_accounting': 'Small businesses and accounting firms.',
        'growing_businesses_high_volume': 'Growing businesses with high volume needs.',
        'month': '/month',
        'pages_included': 'pages included',
        'page_conversions_per': 'page conversions per',
        'save_annual_billing': 'Save 20% with annual billing',
        'everything_in': 'Everything in',
        'plus': 'plus:',
        'batch_processing': 'Batch processing up to',
        'files': 'files',
        'get_started': 'Get started',
        'need_help': 'Need Help?',
        
        // 方案功能描述
        'pages_included_text': 'pages included',
        'page_conversions_per_month': 'page conversions per month',
        'convert_all_files_one_click': 'Convert all files with one click',
        'excel_csv_export': 'Excel & CSV export formats',
        'quickbooks_integration': 'QuickBooks integration',
        'ai_powered_ocr': 'AI-powered OCR processing',
        'day_data_retention': 'day data retention',
        'email_support': 'Email support',
        'secure_file_upload': 'Secure file upload',
        'everything_in_basic_plus': 'Everything in Basic, plus:',
        'batch_processing_files': 'Batch processing up to 20 files',
        'faster_processing_times': 'Faster processing times',
        'data_accuracy_validation': 'Data accuracy validation',
        'multiple_export_formats': 'Multiple export formats',
        'api_access_coming_soon': 'API access (coming soon)',
        'priority_email_support': 'Priority email support',
        'everything_in_pro_plus': 'Everything in Pro, plus:',
        'team_collaboration_features': 'Team collaboration features',
        'advanced_analytics_dashboard': 'Advanced analytics dashboard',
        'white_label_options': 'White-label options',
        'dedicated_account_manager': 'Dedicated account manager',
        'phone_video_support': 'Phone & video support',
        
        // 側邊欄
        'models': 'Models',
        'sidebar_invoices': 'Invoices',
        'sidebar_receipts': 'Receipts',
        'sidebar_general': 'General Documents',
        'processed_documents_count': 'Processed Documents',
        'remaining_credits': 'Remaining Credits'
    },
    
    'zh-TW': {
        // 導航
        'nav_features': '功能',
        'nav_pricing': '價格',
        'nav_dashboard': '儀表板',
        'nav_api': 'API',
        'nav_credits': 'Credits:',
        'nav_login': '登入 →',
        
        // Hero區域
        'hero_title': '<span class="gradient-text">10-30 秒</span>完成財務文檔處理<br>讓 AI 處理繁瑣工作，您專注業務成長',
        'hero_subtitle': '自動轉換銀行對帳單、發票、收據為 Excel/CSV/QuickBooks 格式<br><strong>準確率 98%</strong> • <strong>節省 90% 時間</strong> • <strong>零人為錯誤</strong>',
        'upload_title': '選擇文檔類型並上傳文件',
        'select_model': '選擇轉換模式',
        'model_bank_title': '銀行對帳單轉換器',
        'model_bank_desc': '自動提取銀行對帳單數據',
        'model_invoice_title': '發票轉換器',
        'model_invoice_desc': 'AI發票數據識別',
        'model_receipt_title': '收據轉換器',
        'model_receipt_desc': 'AI收據數據掃描',
        'model_general_title': '通用文檔轉換器',
        'model_general_desc': '通用文檔處理器',
        'upload_text': '拖放PDF文件到這裡 <span class="or">或</span> <button class="browse-btn">瀏覽</button>',
        'browse_btn': '瀏覽',
        
        // 節省時間區域
        'time_saving_title': '現代化您的記帳工作',
        'time_saving_subtitle': '利用AI自動化財務文檔處理，專注於真正重要的事情 - 發展您的業務',
        
        // 功能特色
        'feature_easy_title': '自動化資料提取',
        'feature_easy_desc': '我們的AI系統能從各種文檔類型中準確提取關鍵財務資料，為您節省數小時的手動資料輸入。',
        'feature_secure_title': '與會計軟體整合',
        'feature_secure_desc': '我們的工具設計為與QuickBooks、Xero等流行會計軟體無縫配合。',
        'feature_flexible_title': '增強安全性',
        'feature_flexible_desc': '銀行級加密和安全雲端儲存，確保您的敏感財務文檔始終受到保護。',
        'feature_quick_title': '流線化工作流程',
        'feature_quick_desc': '讓我們的專有軟體處理繁重的任務，您可以減少記帳時間多達80%。',
        'feature_batch_title': '多格式轉換',
        'feature_batch_desc': '輕鬆將銀行對帳單、發票和收據轉換為Excel、JSON、CSV和QuickBooks Online格式。',
        'feature_error_title': 'AI驅動的準確性',
        'feature_error_desc': '我們的先進AI確保高精度的資料提取和轉換，最大限度減少錯誤，節省您的寶貴時間。',
        
        // 價格區域
        'pricing_badge': '合理且實惠的價格',
        'pricing_title': '輕鬆處理銀行對帳單',
        'pricing_subtitle': '與數千家企業一起，節省財務數據錄入的時間。無隱藏費用，隨時取消。',
        'pricing_monthly': '月費',
        'pricing_yearly': '年費 (節省20%)',
        'plan_basic': '基礎方案',
        'basic_pages': '2,400頁/年',
        'basic_feature_1': '2,400頁轉換/年',
        'basic_feature_2': 'Excel & CSV導出',
        'basic_feature_3': 'QuickBooks整合',
        'basic_feature_4': 'AI OCR處理',
        'basic_feature_5': '30天數據保留',
        'cta_basic': '開始使用',
        
        'plan_pro': '專業方案',
        'pro_pages': '6,000頁/年',
        'pro_feature_1': '6,000頁轉換/年',
        'pro_feature_2': '批次處理20個文件',
        'pro_feature_3': '數據準確性驗證',
        'pro_feature_4': '多種導出格式',
        'pro_feature_5': 'API訪問(即將推出)',
        'pro_feature_6': '優先郵件支援',
        'cta_pro': '立即開始',
        
        'plan_business': '商業方案',
        'business_pages': '14,400頁/年',
        'business_feature_1': '14,400頁轉換/年',
        'business_feature_2': '團隊協作功能',
        'business_feature_3': '高級分析儀表板',
        'business_feature_4': '白標選項',
        'business_feature_5': '365天數據保留',
        'business_feature_6': '專屬客戶經理',
        'cta_enterprise': '聯絡我們',
        'popular_badge': '最受歡迎',
        
        // 統一服務
        'service_unified_title': '全方位AI文檔處理平台',
        'service_unified_desc': '我們的AI驅動平台能夠處理銀行對帳單、發票、收據和一般文檔，自動轉換為Excel、CSV、JSON和QuickBooks格式。一個平台，解決所有財務文檔處理需求。',
        'feature_tag_ai': 'AI智能識別',
        'feature_tag_multi': '多格式輸出',
        'feature_tag_fast': '快速處理',
        'feature_tag_secure': '安全可靠',
        
        // 客戶評價
        'testimonials_title': '聽聽我們客戶的評價',
        'testimonials_subtitle': '超過200+企業的信賴選擇',
        'testimonial_1_text': '"太棒了，效果非常好！我印象深刻。"',
        'testimonial_1_name': 'Jamie',
        'testimonial_1_title': 'Orient CEO',
        'testimonial_2_text': '"完全符合我的需求。我對結果非常滿意。"',
        'testimonial_2_name': 'Jose',
        'testimonial_2_title': 'Stealth Startup',
        'testimonial_3_text': '"最準確的處理軟體，價格合理。"',
        'testimonial_3_name': 'Sara',
        'testimonial_3_title': 'Verifax CFO',
        'testimonial_4_text': '"非常有幫助。讓我的工作變得輕鬆多了！"',
        'testimonial_4_name': 'Dan',
        'testimonial_4_title': '會計專業人士',
        
        // FAQ
        'faq_title': '常見問題',
        'faq_subtitle': '我們全面的AI BANK PARSER常見問題深入探討您需要了解的一切。',
        'faq_q1': '什麼是AI Bank Parser轉換器？',
        'faq_a1': 'AI Bank Parser是專門設計用於將您的PDF銀行對帳單轉換為CSV、EXCEL、QBO或JSON格式的軟體。它可以檢測並提取儲存在表格中的交易資料，快速且準確地生成新文件。',
        'faq_q2': '它是如何運作的？',
        'faq_a2': '上傳您的PDF銀行對帳單，我們的軟體將檢測表格、提取其內容，並將其轉換為您需要的格式。處理後的文件將自動下載到您的電腦。',
        'faq_q3': '我的資料安全嗎？',
        'faq_a3': '絕對安全。我們在整個轉換過程中優先考慮您的資料隱私和安全。',
        'faq_q4': '費用是多少？',
        'faq_a4': '我們提供一系列訂閱方案以滿足您的需求。免費試用，然後選擇最適合您的方案。',
        'faq_q5': '我可以免費使用嗎？',
        'faq_a5': '是的！您每天可以免費轉換最多3頁。我們也提供付費訂閱以滿足更高的轉換需求。',
        'faq_q6': '轉換需要多長時間？',
        'faq_a6': '轉換過程可能需要幾秒鐘或幾分鐘，取決於您文件的大小，為您節省數小時的手動資料輸入時間。',
        'faq_q7': '誰可以從使用VaultCaddy中受益？',
        'faq_a7_accountant': '會計師：',
        'faq_a7_accountant_desc': '加快處理客戶銀行對帳單的工作。',
        'faq_a7_finance': '財務專家：',
        'faq_a7_finance_desc': '提高分析和報告的效率。',
        'faq_a7_business': '企業主：',
        'faq_a7_business_desc': '獲得更好的財務洞察，用於預算編制和規劃。',
        'faq_q8': '如果它不適用於我的銀行怎麼辦？',
        'faq_a8': '如果我們的軟體不適用於您的銀行，請通過頁面右下角的聊天視窗聯絡我們。提供您的電子郵件，我們將調整我們的腳本以滿足您的需求。',
        'faq_contact': '還有更多問題？通過我們的聊天視窗聯絡我們或直接發送電子郵件給我們的客戶支援團隊。',
        
        // 部落格
        'blog_title': '為什麼使用AI Bank Parser將PDF銀行對帳單轉換為CSV？',
        'blog_intro': '在當今快節奏的金融世界中，效率和準確性至關重要。如果手動完成，將PDF銀行對帳單轉換為CSV格式可能是一項繁瑣且容易出錯的任務。AI Bank Parser是一個強大的工具，旨在自動化這一過程，為您節省時間並減少錯誤。在這篇文章中，我們將探討為什麼使用AI Bank Parser將您的銀行對帳單轉換為CSV格式是有益的。',
        
        // 頁尾
        'footer_privacy': '隱私政策',
        'footer_terms': '條款與條件',
        'footer_gdpr': 'GDPR',
        'footer_copyright': '© 2025 Made with VaultCaddy 版權所有',
        
        // 上傳狀態
        'upload_processing': '正在處理...',
        'upload_complete': '處理完成！',
        'upload_success_msg': '您的文件已成功轉換並下載到您的電腦。',
        'upload_more': '處理更多文件',
        'upload_selected': '已選擇: ',
        'upload_reset': '重新選擇',
        
        // Dashboard 專用
        'dashboard_title': '儀表板',
        'sidebar_bank_statements': '銀行對帳單',
        'sidebar_invoices': '發票', 
        'sidebar_receipts': '收據',
        'sidebar_general': '一般文檔',
        'page_title_dashboard': '儀表板 - VaultCaddy',
        'bank_statement_processor': '銀行對帳單處理器',
        'invoice_processor': '發票處理器',
        'receipt_processor': '收據處理器',
        'general_processor': '一般文檔處理器',
        'manage_view_documents': '管理和查看您的文檔',
        'bank_statement_details': '銀行對帳單詳細信息與備註',
        'models': '模型',
        'configurations': '配置',
        'account': '帳戶',
        'billing': '計費',
        'filter_document_name': '篩選文檔名稱...',
        'upload_files': '上傳文件',
        'export': '匯出',
        'view': '檢視',
        'document': '文檔',
        'invoice_date': '帳單日期',
        'items_count': '商品',
        'balance_info': '餘額信息',
        'status': '狀態',
        'review_status': '審核狀態',
        'notes': '備註',
        'date_uploaded': '上傳日期',
        'actions': '操作',
        'back_to_dashboard': '返回儀表板',
        'reconciliation_status': '對帳狀態',
        'remaining_credits': '剩餘積分',
        'transactions': '筆交易',
        'in_progress': '進行中',
        'row_s_selected': '行已選擇',
        'rows_per_page': '每頁行數',
        'page_of': '第',
        'of': '共',
        'transactions_reconciled': '筆交易已對帳',
        'complete': '完成',
        'transactions_title': '交易記錄',
        'showing_transactions': '顯示第',
        'to': '至',
        'average_processing_time': '平均處理時間',
        'processing_success_rate': '處理成功率',
        
        // Account 頁面
        'account_settings': '帳戶設定',
        'manage_account_info': '管理您的帳戶資訊。',
        'profile': '個人檔案',
        'security': '安全性',
        'profile_details': '個人檔案詳情',
        'update_profile': '更新個人檔案',
        'email_addresses': '電子郵件地址',
        'primary': '主要',
        'add_email_address': '新增電子郵件地址',
        'connected_accounts': '已連接帳戶',
        'connect_account': '連接帳戶',
        'cancel': '取消',
        'save': '儲存',
        
        // Billing 頁面
        'billing_credits': '計費與積分',
        'manage_billing_subscription': '管理您的計費、訂閱和積分',
        'current_plan': '目前方案：',
        'manage_current_subscription': '管理您目前的訂閱方案',
        'manage': '管理',
        'add_credits': '新增積分',
        'add_credits_description': '向您的帳戶新增積分以轉換更多文檔。',
        'subscription_plans': '訂閱方案',
        'monthly': '月費',
        'yearly': '年費 (節省20%)',
        'basic': '基礎',
        'pro': '專業',
        'business': '商業',
        'perfect_for_individuals': '完美適合個人和自由工作者。',
        'small_businesses_accounting': '小型企業和會計事務所。',
        'growing_businesses_high_volume': '成長中的企業，有大量需求。',
        'month': '/月',
        'pages_included': '頁面包含',
        'page_conversions_per': '頁面轉換每',
        'save_annual_billing': '年度計費節省20%',
        'everything_in': '包含',
        'plus': '的所有功能，還有：',
        'batch_processing': '批次處理最多',
        'files': '個文件',
        'get_started': '開始使用',
        'need_help': '需要幫助？',
        
        // 方案功能描述
        'pages_included_text': '頁面包含',
        'page_conversions_per_month': '頁面轉換每月',
        'convert_all_files_one_click': '一鍵轉換所有文件',
        'excel_csv_export': 'Excel 和 CSV 匯出格式',
        'quickbooks_integration': 'QuickBooks 整合',
        'ai_powered_ocr': 'AI 驅動的 OCR 處理',
        'day_data_retention': '天數據保留',
        'email_support': '電子郵件支援',
        'secure_file_upload': '安全文件上傳',
        'everything_in_basic_plus': '包含基礎版所有功能，還有：',
        'batch_processing_files': '批次處理最多20個文件',
        'faster_processing_times': '更快的處理時間',
        'data_accuracy_validation': '數據準確性驗證',
        'multiple_export_formats': '多種匯出格式',
        'api_access_coming_soon': 'API 存取（即將推出）',
        'priority_email_support': '優先電子郵件支援',
        'everything_in_pro_plus': '包含專業版所有功能，還有：',
        'team_collaboration_features': '團隊協作功能',
        'advanced_analytics_dashboard': '進階分析儀表板',
        'white_label_options': '白標選項',
        'dedicated_account_manager': '專屬客戶經理',
        'phone_video_support': '電話和視訊支援',
        
        // 側邊欄
        'models': '模型',
        'sidebar_invoices': '發票',
        'sidebar_receipts': '收據',
        'sidebar_general': '一般文檔',
        'processed_documents_count': '處理文檔總數',
        'remaining_credits': '剩餘積分'
    },
    
    'zh-CN': {
        // 导航
        'nav_features': '功能',
        'nav_pricing': '定价',
        'nav_api': 'API',
        'nav_login': '登录 →',
        
        // Hero区域
        'hero_title': '将任何PDF银行对账单<br>转换为CSV、EXCEL、QBO或JSON格式',
        'hero_subtitle': '使用我们先进的银行对账单提取软件，简化您的财务数据处理。',
        'upload_title': '上传银行对账单PDF文件',
        'upload_text': '将PDF文件拖放到这里 <span class="or">或</span> <button class="browse-btn">浏览</button>',
        'browse_btn': '浏览',
        
        // 节省时间区域
        'time_saving_title': '节省数小时的手动数据输入',
        'time_saving_subtitle': '使用AI BANK PARSER将PDF银行对账单转换为CSV、EXCEL、QBO或JSON格式',
        
        // 功能特色
        'feature_easy_title': '易于使用',
        'feature_easy_desc': '只需上传您的PDF文件，转换后的文件将自动下载。',
        'feature_secure_title': '安全且保密',
        'feature_secure_desc': '您的数据隐私是我们的首要任务。我们确保所有转换都以安全方式进行，以保护您的敏感信息。',
        'feature_flexible_title': '灵活的输出格式',
        'feature_flexible_desc': '选择多种输出格式，如CSV、EXCEL、QBO或JSON，以满足您的特定需求。',
        'feature_quick_title': '快速且高效',
        'feature_quick_desc': '根据文件大小，在几秒钟或几分钟内转换您的文件，为您节省宝贵时间。',
        'feature_batch_title': '批量处理',
        'feature_batch_desc': '一次处理多个文件，并将所有交易合并到单一结果文件中。',
        'feature_error_title': '减少人为错误',
        'feature_error_desc': '自动化数据提取，最大程度减少手动输入造成的错误。',
        
        // Dashboard 专用
        'dashboard_title': '仪表板',
        'sidebar_bank_statements': '银行对账单',
        'sidebar_invoices': '发票',
        'sidebar_receipts': '收据',
        'sidebar_general': '一般文档',
        'processed_documents_count': '已处理文档数',
        'remaining_credits': '剩余积分',
        'models': '模型',
        'configurations': '配置',
        'account': '账户',
        'billing': '计费',
        'account_settings': '账户设置',
        'manage_account_info': '管理您的账户信息。',
        'billing_credits': '计费与积分',
        'manage_billing_subscription': '管理您的计费、订阅和积分',
        
        // 定价区域
        'pricing_title': '合理且实惠的定价',
        'pricing_subtitle': '人人都能负担得起',
        'pricing_monthly': '月费',
        'pricing_yearly': '年费 (节省20%)',
        'plan_free': '免费方案',
        'plan_pro': '专业方案',
        'plan_enterprise': '企业方案',
        'popular_badge': '最受欢迎',
        'free_feature_1': '每日最多3页',
        'free_feature_2': '基本转换功能',
        'free_feature_3': 'CSV格式输出',
        'pro_feature_1': '无限制页数',
        'pro_feature_2': '所有格式输出',
        'pro_feature_3': '批量处理',
        'pro_feature_4': '优先支持',
        'enterprise_feature_1': '无限制处理',
        'enterprise_feature_2': 'API访问',
        'enterprise_feature_3': '专属支持',
        'enterprise_feature_4': '自定义集成',
        'cta_free': '开始免费使用',
        'cta_pro': '立即开始',
        'cta_enterprise': '联系我们'
    },
    
    'ja': {
        // ナビゲーション
        'nav_features': '機能',
        'nav_pricing': '料金',
        'nav_api': 'API',
        'nav_credits': 'クレジット:',
        'nav_login': 'ログイン →',
        
        // ヒーローエリア
        'hero_title': 'AIで任意の財務文書を処理<br>銀行明細書、請求書、レシートを一括処理',
        'hero_subtitle': '会計士と簿記担当者向けに設計された業界最先端のAI文書コンバーター。PDF銀行明細書、請求書、レシートなどの文書からデータを抽出します。',
        'upload_title': '文書タイプを選択してファイルをアップロード',
        'select_model': '変換モードを選択',
        'model_bank_title': '銀行明細書コンバーター',
        'model_bank_desc': '銀行明細書データの自動抽出',
        'model_invoice_title': '請求書コンバーター',
        'model_invoice_desc': 'AI請求書データ認識',
        'model_receipt_title': 'レシートコンバーター',
        'model_receipt_desc': 'AIレシートデータスキャン',
        'model_general_title': '汎用文書コンバーター',
        'model_general_desc': '汎用文書プロセッサー',
        'upload_text': 'PDFファイルをここにドロップ <span class="or">または</span> <button class="browse-btn">参照</button>',
        'browse_btn': '参照',
        
        // 時間節約エリア
        'time_saving_title': '記帳業務をモダン化',
        'time_saving_subtitle': 'AIによる財務文書処理の自動化で、本当に重要なこと - ビジネスの成長に集中しましょう',
        
        // 機能特徴
        'feature_easy_title': '自動化データ抽出',
        'feature_easy_desc': '当社のAIシステムは様々な文書タイプから重要な財務データを正確に抽出し、手作業による数時間のデータ入力を節約します。',
        'feature_secure_title': '会計ソフトとの統合',
        'feature_secure_desc': '当社のツールはQuickBooks、Xeroなどの人気の会計ソフトとシームレスに連携するよう設計されています。',
        'feature_flexible_title': '強化されたセキュリティ',
        'feature_flexible_desc': '銀行レベルの暗号化と安全なクラウドストレージにより、機密の財務文書を常に保護します。',
        'feature_quick_title': '合理化されたワークフロー',
        'feature_quick_desc': '当社の独自ソフトウェアに重労働を任せ、記帳時間を最大80%削減できます。',
        'feature_batch_title': 'マルチフォーマット変換',
        'feature_batch_desc': '銀行明細書、請求書、レシートをExcel、JSON、CSV、QuickBooks Online形式に簡単に変換できます。',
        'feature_error_title': 'AI駆動の精度',
        'feature_error_desc': '当社の先進AIが高精度のデータ抽出と変換を保証し、エラーを最小限に抑えて貴重な時間を節約します。',
        
        // 統一サービス
        'service_unified_title': '包括的AIドキュメント処理プラットフォーム',
        'service_unified_desc': '当社のAI駆動プラットフォームは、銀行明細書、請求書、レシート、一般文書を処理し、Excel、CSV、JSON、QuickBooks形式に自動変換します。一つのプラットフォームで、すべての財務文書処理ニーズを解決します。',
        'feature_tag_ai': 'AI スマート認識',
        'feature_tag_multi': 'マルチフォーマット出力', 
        'feature_tag_fast': '高速処理',
        'feature_tag_secure': '安全で信頼性',
        
        // 定価エリア
        'pricing_badge': '合理でお手頃な料金',
        'pricing_title': '簡単な銀行取引明細書処理',
        'pricing_subtitle': '数千社の企業と共に、財務データ入力の時間を節約。隠れた費用なし、いつでもキャンセル可能。',
        'pricing_monthly': '月額料金',
        'pricing_yearly': '年額料金 (20%節約)',
        'plan_basic': '基礎プラン',
        'plan_pro': 'プロフェッショナルプラン',
        'basic_pages': '2,400ページ/年',
        'basic_feature_1': 'Excel & CSV出力',
        'basic_feature_2': 'QuickBooks統合',
        'basic_feature_3': '30日データ保持',
        'basic_feature_4': 'AI OCR処理',
        'basic_feature_5': 'メールサポート',
        'cta_basic': '利用開始',
        'pro_pages': '6,000ページ/年',
        'pro_feature_1': '無制限ページ',
        'pro_feature_2': '全フォーマット出力',
        'pro_feature_3': 'バッチ処理',
        'pro_feature_4': '優先サポート',
        'pro_feature_5': 'API アクセス（近日公開）',
        'pro_feature_6': '優先メール支援',
        'cta_pro': '開始',
        'popular_badge': '最も人気',
        
        // よくある質問
        'faq_title': 'よくある質問',
        'faq_subtitle': '包括的なAI BANK PARSER FAQで、知っておくべきすべてを詳しく説明します。',
        'faq_q1': 'AI Bank Parser Converterとは何ですか？',
        'faq_a1': 'AI Bank Parser ConverterはPDF銀行明細書をCSV、Excel、JSON、QBO形式に変換する先進的なツールです。',
        'faq_q2': 'どのように動作しますか？',
        'faq_a2': 'AI技術を使用してPDFファイルを分析し、取引データを抽出して選択した形式に変換します。',
        'faq_q3': 'データは安全ですか？',
        'faq_a3': 'はい、すべてのデータは暗号化され、処理後に安全に削除されます。',
        'faq_q4': '料金はいくらですか？',
        'faq_a4': '基本プランは月額24ドルから始まり、年額プランでは20%割引となります。',
        'faq_q5': '無料で使用できますか？',
        'faq_a5': 'はい、登録時に10クレジットが提供され、機能をテストできます。',
        'faq_q6': '変換にはどのくらい時間がかかりますか？',
        'faq_a6': 'ほとんどの変換は数秒から数分で完了します。',
        'faq_contact': 'さらにご質問がありますか？チャットウィジェットを通じてお問い合わせいただくか、カスタマーサポートチームまで直接メールでご連絡ください。',
        
        // ブログエリア  
        'blog_title': 'AI Bank Parserを使用してPDF銀行明細書をCSVに変換する理由',
        'blog_intro': '今日のペースの速い金融世界では、効率性と正確性が最も重要です。PDF銀行明細書をCSV形式に変換することは、手作業で行うと時間がかかり、エラーが起こりやすい作業です。AI Bank Parserは、このプロセスを自動化し、時間を節約し、エラーを削減するために設計された強力なツールです。このブログ投稿では、AI Bank Parserを使用して銀行明細書をCSV形式に変換することが有益である理由を探ります。',
        'blog_time_title': '時間節約並提高効率',
        'blog_time_desc': '手動でPDF銀行明細書をCSVに変換するには数時間かかる場合があります。特に大量の取引がある場合は特にそうです。AI Bank Parserはこのプロセスを自動化し、数秒または数分で変換を完了します。この効率性により、より重要なタスクに集中でき、全体的な生産性が向上します。',
        'blog_error_title': '人為的エラーの削減',
        'blog_error_desc': '手動データ入力はエラーが起こりやすく、財務記録に重大な問題を引き起こす可能性があります。AI Bank ParserはPDF銀行明細書からデータを正確に抽出し、高精度でCSV形式に変換することで、これらのリスクを最小限に抑えます。これにより、財務データが信頼性が高く正確であることが保証されます。',
        'blog_data_title': '大量データの処理',
        'blog_data_desc': '会計士、財務アナリスト、企業主のいずれであっても、大量の銀行取引の処理は困難です。AI Bank Parserは複数のファイルを同時に処理し、取引を単一の整理されたCSVファイルにマージするように設計されています。この機能は、大量の財務データを管理する専門家にとって特に有用です。',
        'blog_ease_title': '使いやすさ',
        'blog_ease_desc': 'AI Bank Parserはユーザーフレンドリーなインターフェースを備えており、あらゆる技術レベルのユーザーが簡単に使用できます。PDF銀行明細書をアップロードするだけで、ツールが残りを処理し、迅速かつ正確にCSVファイルを提供します。',
        'blog_cost_title': '経済的なソリューション',
        'blog_cost_desc': 'データ入力タスクの外注は高額になる可能性があります。AI Bank Parserは、手動データ入力サービスの必要性を減らす、より手頃な代替手段を提供します。このツールに投資することで、時間の経過とともに大幅なコスト削減を実現できます。',
        'blog_security_title': '安全且保密',
        'blog_security_desc': '機密の財務情報を扱う際、データセキュリティは最優先事項です。AI Bank Parserは、変換プロセス全体を通じてデータが安全に処理され、機密性と完整性を維持することを保証します。',
        'blog_conclusion_title': 'PDFから電子表格への画期的変化',
        'blog_conclusion_desc': 'AI Bank Parserは、PDF銀行明細書をCSV形式に変換する必要がある人にとって画期的です。このプロセスを自動化することで、時間を節約し、エラーを削減し、効率性を向上させます。財務専門家でも企業主でも、このツールはワークフローを簡素化し、財務データの正確性を向上させることができます。今すぐAI Bank Parserを試して、自動化された銀行明細書変換の利点を自分で体験してください！',
        
        // 追加サービス
        'service_excel_title': '銀行明細書をExcelに変換',
        'service_excel_desc': 'ユーザーフレンドリーなツールを使用して、PDF銀行明細書をExcel形式に簡単に変換できます。自動化されたデータ抽出により時間を節約し、エラーを削減します。',
        'service_extraction_title': '銀行明細書抽出ソフトウェア',
        'service_extraction_desc': '先進技術を活用して、PDF銀行明細書から取引データを精密かつ迅速に抽出します。会計士や財務専門家に最適です。',
        'service_csv_title': 'PDF銀行明細書をCSVに変換',
        'service_csv_desc': '数回のクリックでPDF銀行明細書をCSV形式に変換できます。信頼性の高いツールでワークフローを簡素化し、データの正確性を向上させます。',
        
        // Dashboard 専用
        'dashboard_title': 'ダッシュボード',
        'sidebar_bank_statements': '銀行明細書',
        'sidebar_invoices': '請求書', 
        'sidebar_receipts': 'レシート',
        'sidebar_general': '一般文書',
        'page_title_dashboard': 'ダッシュボード - VaultCaddy',
        'bank_statement_processor': '銀行明細書プロセッサー',
        'invoice_processor': '請求書プロセッサー',
        'receipt_processor': 'レシートプロセッサー',
        'general_processor': '一般文書プロセッサー',
        'manage_view_documents': '文書の管理と表示',
        'bank_statement_details': '銀行明細書の詳細とメモ',
        'models': 'モデル',
        'configurations': '設定',
        'account': 'アカウント',
        'billing': '請求',
        'filter_document_name': '文書名をフィルター...',
        'upload_files': 'ファイルをアップロード',
        'view': 'ビュー',
        'document': '文書',
        'statement_period': '明細書期間',
        'reconciliation': '照合',
        'balance_info': '残高情報',
        'status': 'ステータス',
        'actions': 'アクション',
        'back_to_dashboard': 'ダッシュボードに戻る',
        'reconciliation_status': '照合ステータス',
        'remaining_credits': '残りクレジット',
        'transactions': '件の取引',
        'in_progress': '進行中',
        'row_s_selected': '行が選択されています',
        'rows_per_page': '1ページあたりの行数',
        'page_of': 'ページ',
        'of': '/',
        'transactions_reconciled': '件の取引が照合済み',
        'complete': '完了',
        'transactions_title': '取引',
        'showing_transactions': '表示中',
        'to': 'から',
        'average_processing_time': '平均処理時間',
        'processing_success_rate': '処理成功率',
        
        // Account ページ
        'account_settings': 'アカウント設定',
        'manage_account_info': 'アカウント情報を管理する。',
        'profile': 'プロフィール',
        'security': 'セキュリティ',
        'profile_details': 'プロフィール詳細',
        'update_profile': 'プロフィールを更新',
        'email_addresses': 'メールアドレス',
        'primary': 'プライマリ',
        'add_email_address': 'メールアドレスを追加',
        'connected_accounts': '連携アカウント',
        'connect_account': 'アカウントを連携',
        'cancel': 'キャンセル',
        'save': '保存',
        
        // Billing ページ
        'billing_credits': '請求とクレジット',
        'manage_billing_subscription': '請求、サブスクリプション、クレジットを管理',
        'current_plan': '現在のプラン：',
        'manage_current_subscription': '現在のサブスクリプションプランを管理',
        'manage': '管理',
        'add_credits': 'クレジットを追加',
        'add_credits_description': 'より多くの文書を変換するためにアカウントにクレジットを追加します。',
        'subscription_plans': 'サブスクリプションプラン',
        'monthly': '月額',
        'yearly': '年額 (20%節約)',
        'basic': 'ベーシック',
        'pro': 'プロ',
        'business': 'ビジネス',
        'perfect_for_individuals': '個人やフリーランサーに最適。',
        'small_businesses_accounting': '中小企業や会計事務所。',
        'growing_businesses_high_volume': '大量処理が必要な成長企業。',
        'month': '/月',
        'pages_included': 'ページ含む',
        'page_conversions_per': 'ページ変換毎',
        'save_annual_billing': '年間請求で20%節約',
        'everything_in': 'すべて含む',
        'plus': 'に加えて：',
        'batch_processing': 'バッチ処理最大',
        'files': 'ファイル',
        'get_started': '開始する',
        'need_help': 'ヘルプが必要ですか？',
        
        // 方案功能描述
        'pages_included_text': 'ページ含む',
        'page_conversions_per_month': 'ページ変換毎月',
        'convert_all_files_one_click': 'ワンクリックで全ファイル変換',
        'excel_csv_export': 'ExcelとCSVエクスポート形式',
        'quickbooks_integration': 'QuickBooks統合',
        'ai_powered_ocr': 'AI搭載OCR処理',
        'day_data_retention': '日間データ保持',
        'email_support': 'メールサポート',
        'secure_file_upload': 'セキュアファイルアップロード',
        'everything_in_basic_plus': 'ベーシックの全機能に加えて：',
        'batch_processing_files': 'バッチ処理最大20ファイル',
        'faster_processing_times': '高速処理時間',
        'data_accuracy_validation': 'データ精度検証',
        'multiple_export_formats': '複数エクスポート形式',
        'api_access_coming_soon': 'APIアクセス（近日公開）',
        'priority_email_support': '優先メールサポート',
        'everything_in_pro_plus': 'プロの全機能に加えて：',
        'team_collaboration_features': 'チーム連携機能',
        'advanced_analytics_dashboard': '高度分析ダッシュボード',
        'white_label_options': 'ホワイトラベルオプション',
        'dedicated_account_manager': '専任アカウントマネージャー',
        'phone_video_support': '電話・ビデオサポート',
        
        // 側邊欄
        'models': 'モデル',
        'sidebar_invoices': '請求書',
        'sidebar_receipts': 'レシート',
        'sidebar_general': '一般文書',
        'processed_documents_count': '処理済み文書数',
        'remaining_credits': '残りクレジット'
    },
    
    'ko': {
        // 내비게이션
        'nav_features': '기능',
        'nav_pricing': '가격',
        'nav_api': 'API',
        'nav_credits': '크레딧:',
        'nav_login': '로그인 →',
        
        // 히어로 영역
        'hero_title': 'AI로 모든 재무 문서 처리<br>은행 명세서, 송장, 영수증 일괄 처리',
        'hero_subtitle': '회계사와 부기 담당자를 위해 설계된 업계 최고의 AI 문서 변환기. PDF 은행 명세서, 송장, 영수증 등의 문서에서 데이터를 추출합니다.',
        'upload_title': '문서 유형을 선택하고 파일 업로드',
        'select_model': '변환 모드 선택',
        'model_bank_title': '은행 명세서 변환기',
        'model_bank_desc': '은행 명세서 데이터 자동 추출',
        'model_invoice_title': '송장 변환기',
        'model_invoice_desc': 'AI 송장 데이터 인식',
        'model_receipt_title': '영수증 변환기',
        'model_receipt_desc': 'AI 영수증 데이터 스캔',
        'model_general_title': '범용 문서 변환기',
        'model_general_desc': '범용 문서 프로세서',
        'upload_text': 'PDF 파일을 여기에 드롭 <span class="or">또는</span> <button class="browse-btn">찾아보기</button>',
        'browse_btn': '찾아보기',
        
        // 시간 절약 영역
        'time_saving_title': '부기 업무 현대화',
        'time_saving_subtitle': 'AI를 통한 재무 문서 처리 자동화로 정말 중요한 일 - 비즈니스 성장에 집중하세요',
        
        // 기능 특징
        'feature_easy_title': '자동화된 데이터 추출',
        'feature_easy_desc': '당사의 AI 시스템은 다양한 문서 유형에서 중요한 재무 데이터를 정확하게 추출하여 수 시간의 수동 데이터 입력을 절약합니다.',
        'feature_secure_title': '회계 소프트웨어 통합',
        'feature_secure_desc': '당사의 도구는 QuickBooks, Xero 등 인기 있는 회계 소프트웨어와 원활하게 작동하도록 설계되었습니다.',
        'feature_flexible_title': '향상된 보안',
        'feature_flexible_desc': '은행급 암호화와 안전한 클라우드 저장소로 민감한 재무 문서를 항상 보호합니다.',
        'feature_quick_title': '간소화된 워크플로',
        'feature_quick_desc': '당사의 독점 소프트웨어가 무거운 작업을 처리하여 부기 시간을 최대 80% 단축할 수 있습니다.',
        'feature_batch_title': '다중 형식 변환',
        'feature_batch_desc': '은행 명세서, 송장, 영수증을 Excel, JSON, CSV, QuickBooks Online 형식으로 쉽게 변환할 수 있습니다.',
        'feature_error_title': 'AI 기반 정확성',
        'feature_error_desc': '당사의 고급 AI가 높은 정확도의 데이터 추출과 변환을 보장하여 오류를 최소화하고 소중한 시간을 절약합니다.',
        
        // 가격 영역
        'pricing_badge': '합리적이고 저렴한 요금',
        'pricing_title': '간편한 은행 명세서 처리',
        'pricing_subtitle': '수천 개 기업과 함께 재무 데이터 입력 시간을 절약하세요. 숨겨진 요금 없음, 언제든 취소 가능.',
        'pricing_monthly': '월 요금제',
        'pricing_yearly': '연 요금제 (20% 절약)',
        'plan_free': '무료 플랜',
        'plan_pro': '전문 플랜',
        'plan_enterprise': '기업 플랜',
        'popular_badge': '가장 인기',
        'free_feature_1': '일일 최대 3페이지',
        'free_feature_2': '기본 변환 기능',
        'free_feature_3': 'CSV 형식 출력',
        'pro_feature_1': '무제한 페이지',
        'pro_feature_2': '모든 형식 출력',
        'pro_feature_3': '일괄 처리',
        'pro_feature_4': '우선 지원',
        'enterprise_feature_1': '무제한 처리',
        'enterprise_feature_2': 'API 액세스',
        'enterprise_feature_3': '전용 지원',
        'enterprise_feature_4': '맞춤 통합',
        'cta_free': '무료로 시작하기',
        'cta_pro': '지금 시작하기',
        'cta_enterprise': '문의하기',
        
        // 통합 서비스
        'service_unified_title': '포괄적인 AI 문서 처리 플랫폼',
        'service_unified_desc': '당사의 AI 기반 플랫폼은 은행 명세서, 송장, 영수증, 일반 문서를 처리하여 Excel, CSV, JSON, QuickBooks 형식으로 자동 변환합니다. 하나의 플랫폼으로 모든 재무 문서 처리 요구사항을 해결합니다.',
        'feature_tag_ai': 'AI 스마트 인식',
        'feature_tag_multi': '다중 형식 출력',
        'feature_tag_fast': '빠른 처리',
        'feature_tag_secure': '안전하고 신뢰할 수 있음',
        
        // Dashboard 전용
        'dashboard_title': '대시보드',
        'sidebar_bank_statements': '은행 명세서',
        'sidebar_invoices': '송장', 
        'sidebar_receipts': '영수증',
        'sidebar_general': '일반 문서',
        'processed_documents_count': '처리된 문서 수',
        'remaining_credits': '남은 크레딧',
        
        // Account 페이지
        'account_settings': '계정 설정',
        'manage_account_info': '계정 정보를 관리합니다.',
        'profile': '프로필',
        'security': '보안',
        'profile_details': '프로필 세부사항',
        'update_profile': '프로필 업데이트',
        'email_addresses': '이메일 주소',
        'primary': '기본',
        'add_email_address': '이메일 주소 추가',
        'connected_accounts': '연결된 계정',
        'connect_account': '계정 연결',
        'cancel': '취소',
        'save': '저장',
        
        // Billing 페이지
        'billing_credits': '결제 및 크레딧',
        'manage_billing_subscription': '결제, 구독 및 크레딧 관리',
        'current_plan': '현재 플랜:',
        'manage_current_subscription': '현재 구독 플랜 관리',
        'manage': '관리',
        'add_credits': '크레딧 추가',
        'add_credits_description': '더 많은 문서를 변환하기 위해 계정에 크레딧을 추가합니다.',
        'subscription_plans': '구독 플랜',
        'monthly': '월간',
        'yearly': '연간 (20% 절약)',
        'basic': '기본',
        'pro': '프로',
        'business': '비즈니스',
        'perfect_for_individuals': '개인 및 프리랜서에게 완벽합니다.',
        'small_businesses_accounting': '중소기업 및 회계 사무소.',
        'growing_businesses_high_volume': '대용량이 필요한 성장하는 기업.',
        'month': '/월',
        'pages_included': '페이지 포함',
        'page_conversions_per': '페이지 변환 매',
        'save_annual_billing': '연간 결제로 20% 절약',
        'everything_in': '모든 것 포함',
        'plus': '추가:',
        'batch_processing': '배치 처리 최대',
        'files': '파일',
        'get_started': '시작하기',
        'need_help': '도움이 필요하세요?',
        'pages_included_text': '페이지 포함',
        'page_conversions_per_month': '월간 페이지 변환',
        'convert_all_files_one_click': '원클릭으로 모든 파일 변환',
        'excel_csv_export': 'Excel 및 CSV 내보내기 형식',
        'quickbooks_integration': 'QuickBooks 통합',
        'ai_powered_ocr': 'AI 기반 OCR 처리',
        'day_data_retention': '일 데이터 보관',
        'email_support': '이메일 지원',
        'secure_file_upload': '안전한 파일 업로드',
        'everything_in_basic_plus': '기본의 모든 기능에 추가:',
        'batch_processing_files': '배치 처리 최대 20개 파일',
        'faster_processing_times': '더 빠른 처리 시간',
        'data_accuracy_validation': '데이터 정확성 검증',
        'multiple_export_formats': '다중 내보내기 형식',
        'api_access_coming_soon': 'API 액세스 (곧 출시)',
        'priority_email_support': '우선 이메일 지원',
        'everything_in_pro_plus': '프로의 모든 기능에 추가:',
        'team_collaboration_features': '팀 협업 기능',
        'advanced_analytics_dashboard': '고급 분석 대시보드',
        'white_label_options': '화이트 라벨 옵션',
        'dedicated_account_manager': '전담 계정 관리자',
        'phone_video_support': '전화 및 비디오 지원',
        'page_title_dashboard': '대시보드 - VaultCaddy',
        'bank_statement_processor': '은행 명세서 프로세서',
        'invoice_processor': '송장 프로세서',
        'receipt_processor': '영수증 프로세서',
        'general_processor': '일반 문서 프로세서',
        'manage_view_documents': '문서 관리 및 보기',
        'bank_statement_details': '은행 명세서 세부사항 및 메모',
        'models': '모델',
        'configurations': '설정',
        'account': '계정',
        'billing': '청구',
        'filter_document_name': '문서명 필터...',
        'upload_files': '파일 업로드',
        'view': '보기',
        'document': '문서',
        'statement_period': '명세서 기간',
        'reconciliation': '조정',
        'balance_info': '잔액 정보',
        'status': '상태',
        'actions': '작업',
        'back_to_dashboard': '대시보드로 돌아가기',
        'reconciliation_status': '조정 상태',
        'remaining_credits': '남은 크레딧',
        'transactions': '건의 거래',
        'in_progress': '진행 중',
        'row_s_selected': '행이 선택됨',
        'rows_per_page': '페이지당 행 수',
        'page_of': '페이지',
        'of': '/',
        'transactions_reconciled': '건의 거래가 조정됨',
        'complete': '완료',
        'transactions_title': '거래',
        'showing_transactions': '표시 중',
        'to': '~',
        'average_processing_time': '평균 처리 시간',
        'processing_success_rate': '처리 성공률',
        
        // 정가 영역
        'pricing_badge': '합리적이고 저렴한 요금',
        'pricing_title': '간편한 은행 명세서 처리',
        'pricing_subtitle': '수천 개 기업과 함께 재무 데이터 입력 시간을 절약하세요. 숨겨진 요금 없음, 언제든 취소 가능.',
        'pricing_monthly': '월 요금제',
        'pricing_yearly': '연 요금제 (20% 절약)',
        'plan_basic': '기본 플랜',
        'plan_pro': '프로페셔널 플랜',
        'basic_pages': '2,400페이지/년',
        'basic_feature_1': 'Excel & CSV 출력',
        'basic_feature_2': 'QuickBooks 통합',
        'basic_feature_3': '30일 데이터 보관',
        'basic_feature_4': 'AI OCR 처리',
        'basic_feature_5': '이메일 지원',
        'cta_basic': '시작하기',
        'pro_pages': '6,000페이지/년',
        'pro_feature_1': '무제한 페이지',
        'pro_feature_2': '모든 형식 출력',
        'pro_feature_3': '일괄 처리',
        'pro_feature_4': '우선 지원',
        'pro_feature_5': 'API 액세스 (곧 출시)',
        'pro_feature_6': '우선 이메일 지원',
        'cta_pro': '시작',
        'popular_badge': '가장 인기',
        
        // FAQ
        'faq_title': '자주 묻는 질문',
        'faq_subtitle': '포괄적인 AI BANK PARSER FAQ에서 알아야 할 모든 것을 자세히 설명합니다.',
        'faq_q1': 'AI Bank Parser Converter란 무엇입니까?',
        'faq_a1': 'AI Bank Parser Converter는 PDF 은행 명세서를 CSV, Excel, JSON, QBO 형식으로 변환하는 고급 도구입니다.',
        'faq_q2': '어떻게 작동하나요?',
        'faq_a2': 'AI 기술을 사용하여 PDF 파일을 분석하고 거래 데이터를 추출하여 선택한 형식으로 변환합니다.',
        'faq_q3': '데이터가 안전한가요?',
        'faq_a3': '예, 모든 데이터는 암호화되고 처리 후 안전하게 삭제됩니다.',
        'faq_q4': '비용은 얼마인가요?',
        'faq_a4': '기본 플랜은 월 $24부터 시작하며, 연간 플랜에서는 20% 할인됩니다.',
        'faq_q5': '무료로 사용할 수 있나요?',
        'faq_a5': '예, 가입 시 10크레딧이 제공되어 기능을 테스트할 수 있습니다.',
        'faq_q6': '변환에 얼마나 걸리나요?',
        'faq_a6': '대부분의 변환은 몇 초에서 몇 분 내에 완료됩니다.',
        'faq_contact': '더 궁금한 점이 있으신가요? 채팅 위젯을 통해 문의하거나 고객 지원팀에 직접 이메일을 보내주세요.',
        
        // 블로그 영역
        'blog_title': 'AI Bank Parser를 사용하여 PDF 은행 명세서를 CSV로 변환하는 이유',
        'blog_intro': '오늘날의 빠른 금융 세계에서 효율성과 정확성이 가장 중요합니다. PDF 은행 명세서를 CSV 형식으로 변환하는 것은 수동으로 할 경우 시간이 많이 걸리고 오류가 발생하기 쉬운 작업입니다. AI Bank Parser는 이 과정을 자동화하여 시간을 절약하고 오류를 줄이기 위해 설계된 강력한 도구입니다.',
        'blog_time_title': '시간 절약 및 효율성 향상',
        'blog_time_desc': 'PDF 은행 명세서를 수동으로 CSV로 변환하는 데는 몇 시간이 걸릴 수 있습니다. 특히 많은 거래가 있는 경우 더욱 그렇습니다. AI Bank Parser는 이 과정을 자동화하여 몇 초 또는 몇 분 내에 변환을 완료합니다.',
        'blog_error_title': '인적 오류 감소',
        'blog_error_desc': '수동 데이터 입력은 오류가 발생하기 쉬우며 재무 기록에 심각한 문제를 일으킬 수 있습니다. AI Bank Parser는 PDF 은행 명세서에서 데이터를 정확하게 추출하여 높은 정확도로 CSV 형식으로 변환함으로써 이러한 위험을 최소화합니다.',
        'blog_data_title': '대량 데이터 처리',
        'blog_data_desc': '회계사, 재무 분석가 또는 사업주든 관계없이 대량의 은행 거래를 처리하는 것은 어려울 수 있습니다. AI Bank Parser는 여러 파일을 동시에 처리하고 거래를 단일하고 정리된 CSV 파일로 병합하도록 설계되었습니다.',
        'blog_ease_title': '사용 편의성',
        'blog_ease_desc': 'AI Bank Parser는 사용자 친화적인 인터페이스를 갖추고 있어 모든 기술 수준의 사용자가 쉽게 사용할 수 있습니다. PDF 은행 명세서를 업로드하기만 하면 도구가 나머지를 처리하여 빠르고 정확하게 CSV 파일을 제공합니다.',
        'blog_cost_title': '경제적인 솔루션',
        'blog_cost_desc': '데이터 입력 작업을 외주화하는 것은 비용이 많이 들 수 있습니다. AI Bank Parser는 수동 데이터 입력 서비스의 필요성을 줄이는 더 저렴한 대안을 제공합니다.',
        'blog_security_title': '안전하고 기밀',
        'blog_security_desc': '민감한 재무 정보를 처리할 때 데이터 보안이 최우선입니다. AI Bank Parser는 변환 과정 전반에 걸쳐 데이터가 안전하게 처리되어 기밀성과 무결성을 유지함을 보장합니다.',
        'blog_conclusion_title': 'PDF에서 스프레드시트로의 게임 체인저',
        'blog_conclusion_desc': 'AI Bank Parser는 PDF 은행 명세서를 CSV 형식으로 변환해야 하는 모든 사람에게 게임 체인저입니다. 이 과정을 자동화함으로써 시간을 절약하고 오류를 줄이며 효율성을 향상시킵니다.',
        
        // FAQ
        'faq_title': '자주 묻는 질문',
        'faq_subtitle': '포괄적인 VaultCaddy FAQ에서 알아야 할 모든 것을 자세히 살펴보세요.',
        'faq_q1': 'VaultCaddy 변환기란 무엇인가요?',
        'faq_a1': 'VaultCaddy는 PDF 은행 명세서를 CSV, EXCEL, QBO 또는 JSON 형식으로 변환하도록 특별히 설계된 소프트웨어입니다. 표에 저장된 거래 데이터를 감지하고 추출하여 빠르고 정확하게 새 파일을 생성합니다.',
        'faq_q2': '어떻게 작동하나요?',
        'faq_a2': 'PDF 은행 명세서를 업로드하면 소프트웨어가 표를 감지하고 내용을 추출한 후 필요한 형식으로 변환합니다. 처리된 파일은 자동으로 컴퓨터에 다운로드됩니다.',
        'faq_q3': '내 데이터가 안전한가요?',
        'faq_a3': '절대적으로 안전합니다. 전체 변환 과정에서 데이터 개인정보 보호와 보안을 최우선으로 합니다.',
        'faq_q4': '비용은 얼마인가요?',
        'faq_a4': '귀하의 요구사항에 맞는 다양한 구독 플랜을 제공합니다. 무료로 체험해 보신 후 가장 적합한 플랜을 선택하세요.',
        'faq_q5': '무료로 사용할 수 있나요?',
        'faq_a5': '네! 매일 최대 3페이지까지 무료로 변환할 수 있습니다. 더 많은 변환이 필요한 경우 유료 구독도 제공합니다.',
        'faq_q6': '변환에 얼마나 걸리나요?',
        'faq_a6': '파일 크기에 따라 변환 과정은 몇 초에서 몇 분이 걸리며, 수 시간의 수동 데이터 입력 시간을 절약해 줍니다.',
        'faq_q7': 'VaultCaddy를 사용하면 누가 혜택을 받을 수 있나요?',
        'faq_a7': '<ul><li><strong>회계사:</strong> 고객 은행 명세서 작업 속도 향상</li><li><strong>재무 전문가:</strong> 분석 및 보고 효율성 향상</li><li><strong>사업주:</strong> 예산 편성 및 계획을 위한 더 나은 재무 통찰력 확보</li></ul>',
        'faq_q8': '내 은행에서 작동하지 않으면 어떻게 하나요?',
        'faq_a8': '소프트웨어가 귀하의 은행에서 작동하지 않는 경우, 페이지 오른쪽 하단의 채팅 위젯을 통해 문의하십시오. 이메일을 제공해 주시면 귀하의 요구사항에 맞게 스크립트를 조정해 드리겠습니다.',
        'faq_contact': '더 궁금한 점이 있으신가요? 채팅 위젯을 통해 문의하거나 고객 지원팀에 직접 이메일을 보내주세요.',
        
        // 부트스트랩
        'blog_title': 'PDF 은행 명세서를 CSV로 변환하는데 VaultCaddy를 사용하는 이유는?',
        'blog_intro': '오늘날 빠르게 변화하는 금융 세계에서 효율성과 정확성이 무엇보다 중요합니다. PDF 은행 명세서를 CSV 형식으로 변환하는 것은 수동으로 할 경우 지루하고 오류가 발생하기 쉬운 작업일 수 있습니다. VaultCaddy는 이 과정을 자동화하여 시간을 절약하고 오류를 줄이도록 설계된 강력한 도구입니다.',
        
        // 페이지 하단
        'footer_privacy': '개인정보 처리방침',
        'footer_terms': '이용약관',
        'footer_gdpr': 'GDPR',
        'footer_copyright': '© 2024 VaultCaddy Inc. 모든 권리 보유.'
    },
    
    'es': {
        // Navegación
        'nav_features': 'Características',
        'nav_pricing': 'Precios',
        'nav_api': 'API',
        'nav_login': 'Iniciar sesión →',
        
        // Área Hero
        'hero_title': 'Convierte cualquier estado de cuenta bancario PDF<br>a formato CSV, EXCEL, QBO o JSON',
        'hero_subtitle': 'Simplifica el procesamiento de datos financieros con nuestro software avanzado de extracción de estados de cuenta bancarios.',
        'upload_title': 'Subir archivo PDF de estado de cuenta bancario',
        'upload_text': 'Arrastra el archivo PDF aquí <span class="or">o</span> <button class="browse-btn">Explorar</button>',
        'browse_btn': 'Explorar',
        
        // Área de ahorro de tiempo
        'time_saving_title': 'Ahorra horas de entrada manual de datos',
        'time_saving_subtitle': 'Usa AI BANK PARSER para convertir estados de cuenta bancarios PDF a CSV, EXCEL, QBO o JSON',
        
        // Características
        'feature_easy_title': 'Fácil de usar',
        'feature_easy_desc': 'Simplemente sube tus archivos PDF y los archivos convertidos se descargarán automáticamente.',
        'feature_secure_title': 'Seguro y confidencial',
        'feature_secure_desc': 'Tu privacidad de datos es nuestra máxima prioridad. Aseguramos que todas las conversiones se realicen de forma segura para proteger tu información sensible.',
        'feature_flexible_title': 'Formatos de salida flexibles',
        'feature_flexible_desc': 'Elige entre varios formatos de salida como CSV, EXCEL, QBO o JSON para satisfacer tus necesidades específicas.',
        'feature_quick_title': 'Rápido y eficiente',
        'feature_quick_desc': 'Convierte tus archivos en segundos o minutos, dependiendo de su tamaño, ahorrándote tiempo valioso.',
        'feature_batch_title': 'Procesamiento en lotes',
        'feature_batch_desc': 'Maneja múltiples archivos a la vez y fusiona todas las transacciones en un solo archivo de resultado.',
        'feature_error_title': 'Reduce errores humanos',
        'feature_error_desc': 'Automatiza la extracción de datos para minimizar errores de entrada manual.',
        
        // Dashboard 専用
        'dashboard_title': 'Panel de control',
        'sidebar_bank_statements': 'Estados bancarios',
        'sidebar_invoices': 'Facturas', 
        'sidebar_receipts': 'Recibos',
        'sidebar_general': 'Documentos generales',
        'processed_documents_count': 'Documentos procesados',
        'remaining_credits': 'Créditos restantes',
        
        // Account 页面
        'account_settings': 'Configuración de cuenta',
        'manage_account_info': 'Gestionar la información de su cuenta.',
        'profile': 'Perfil',
        'security': 'Seguridad',
        'profile_details': 'Detalles del perfil',
        'update_profile': 'Actualizar perfil',
        'email_addresses': 'Direcciones de correo',
        'primary': 'Principal',
        'add_email_address': 'Agregar dirección de correo',
        'connected_accounts': 'Cuentas conectadas',
        'connect_account': 'Conectar cuenta',
        'cancel': 'Cancelar',
        'save': 'Guardar',
        
        // Billing 页面
        'billing_credits': 'Facturación y créditos',
        'manage_billing_subscription': 'Gestionar facturación, suscripción y créditos',
        'current_plan': 'Plan actual:',
        'manage_current_subscription': 'Gestionar su plan de suscripción actual',
        'manage': 'Gestionar',
        'add_credits': 'Agregar créditos',
        'add_credits_description': 'Agregue créditos a su cuenta para convertir más documentos.',
        'subscription_plans': 'Planes de suscripción',
        'monthly': 'Mensual',
        'yearly': 'Anual (Ahorrar 20%)',
        'basic': 'Básico',
        'pro': 'Pro',
        'business': 'Empresarial',
        'perfect_for_individuals': 'Perfecto para individuos y freelancers.',
        'small_businesses_accounting': 'Pequeñas empresas y firmas contables.',
        'growing_businesses_high_volume': 'Empresas en crecimiento con necesidades de alto volumen.',
        'models': 'Modelos',
        'configurations': 'CONFIGURACIONES',
        'account': 'Cuenta',
        'billing': 'Facturación',
        'remaining_credits': 'Créditos restantes',
        'transactions': 'transacciones',
        'in_progress': 'En progreso',
        'row_s_selected': 'fila(s) seleccionada(s)',
        'rows_per_page': 'Filas por página',
        'page_of': 'Página',
        'of': 'de',
        'transactions_reconciled': 'transacciones conciliadas',
        'complete': 'Completo',
        'transactions_title': 'Transacciones',
        'showing_transactions': 'Mostrando',
        'to': 'a',
        'average_processing_time': 'Tiempo promedio de procesamiento',
        'processing_success_rate': 'Tasa de éxito de procesamiento'
    },
    
    'fr': {
        // Navigation
        'nav_features': 'Fonctionnalités',
        'nav_pricing': 'Tarifs',
        'nav_api': 'API',
        'nav_login': 'Se connecter →',
        
        // Zone Hero
        'hero_title': 'Convertissez tout relevé bancaire PDF<br>en format CSV, EXCEL, QBO ou JSON',
        'hero_subtitle': 'Simplifiez le traitement de vos données financières avec notre logiciel avancé d\'extraction de relevés bancaires.',
        'upload_title': 'Télécharger un fichier PDF de relevé bancaire',
        'upload_text': 'Déposez le fichier PDF ici <span class="or">ou</span> <button class="browse-btn">Parcourir</button>',
        'browse_btn': 'Parcourir',
        
        // Zone d\'économie de temps
        'time_saving_title': 'Économisez des heures de saisie manuelle',
        'time_saving_subtitle': 'Utilisez AI BANK PARSER pour convertir les relevés bancaires PDF en CSV, EXCEL, QBO ou JSON',
        
        // Caractéristiques
        'feature_easy_title': 'Facile à utiliser',
        'feature_easy_desc': 'Téléchargez simplement vos fichiers PDF et les fichiers convertis seront automatiquement téléchargés.',
        'feature_secure_title': 'Sécurisé et confidentiel',
        'feature_secure_desc': 'Votre confidentialité des données est notre priorité absolue. Nous nous assurons que toutes les conversions sont effectuées en toute sécurité pour protéger vos informations sensibles.',
        'feature_flexible_title': 'Formats de sortie flexibles',
        'feature_flexible_desc': 'Choisissez parmi différents formats de sortie tels que CSV, EXCEL, QBO ou JSON pour répondre à vos besoins spécifiques.',
        'feature_quick_title': 'Rapide et efficace',
        'feature_quick_desc': 'Convertissez vos fichiers en quelques secondes ou minutes, selon leur taille, vous faisant économiser un temps précieux.',
        'feature_batch_title': 'Traitement par lots',
        'feature_batch_desc': 'Gérez plusieurs fichiers à la fois et fusionnez toutes les transactions dans un seul fichier de résultat.',
        'feature_error_title': 'Réduire les erreurs humaines',
        'feature_error_desc': 'Automatisez l\'extraction de données pour minimiser les erreurs de saisie manuelle.',
        
        // Dashboard 専用
        'dashboard_title': 'Tableau de bord',
        'sidebar_bank_statements': 'Relevés bancaires',
        'sidebar_invoices': 'Factures', 
        'sidebar_receipts': 'Reçus',
        'sidebar_general': 'Documents généraux',
        'processed_documents_count': 'Documents traités',
        'remaining_credits': 'Crédits restants',
        
        // Account 页面
        'account_settings': 'Paramètres du compte',
        'manage_account_info': 'Gérer les informations de votre compte.',
        'profile': 'Profil',
        'security': 'Sécurité',
        'profile_details': 'Détails du profil',
        'update_profile': 'Mettre à jour le profil',
        'email_addresses': 'Adresses e-mail',
        'primary': 'Principal',
        'add_email_address': 'Ajouter une adresse e-mail',
        'connected_accounts': 'Comptes connectés',
        'connect_account': 'Connecter un compte',
        'cancel': 'Annuler',
        'save': 'Enregistrer',
        
        // Billing 页面
        'billing_credits': 'Facturation et crédits',
        'manage_billing_subscription': 'Gérer la facturation, l\'abonnement et les crédits',
        'current_plan': 'Plan actuel:',
        'manage_current_subscription': 'Gérer votre plan d\'abonnement actuel',
        'manage': 'Gérer',
        'add_credits': 'Ajouter des crédits',
        'add_credits_description': 'Ajoutez des crédits à votre compte pour convertir plus de documents.',
        'subscription_plans': 'Plans d\'abonnement',
        'monthly': 'Mensuel',
        'yearly': 'Annuel (Économiser 20%)',
        'basic': 'Basique',
        'pro': 'Pro',
        'business': 'Entreprise',
        'perfect_for_individuals': 'Parfait pour les particuliers et freelances.',
        'small_businesses_accounting': 'Petites entreprises et cabinets comptables.',
        'growing_businesses_high_volume': 'Entreprises en croissance avec des besoins de gros volume.',
        'models': 'Modèles',
        'configurations': 'CONFIGURATIONS',
        'account': 'Compte',
        'billing': 'Facturation',
        'remaining_credits': 'Crédits restants',
        'transactions': 'transactions',
        'in_progress': 'En cours',
        'row_s_selected': 'ligne(s) sélectionnée(s)',
        'rows_per_page': 'Lignes par page',
        'page_of': 'Page',
        'of': 'de',
        'transactions_reconciled': 'transactions rapprochées',
        'complete': 'Terminé',
        'transactions_title': 'Transactions',
        'showing_transactions': 'Affichage',
        'to': 'à',
        'average_processing_time': 'Temps de traitement moyen',
        'processing_success_rate': 'Taux de réussite du traitement'
    },
    
    'de': {
        // Navigation
        'nav_features': 'Funktionen',
        'nav_pricing': 'Preise',
        'nav_api': 'API',
        'nav_login': 'Anmelden →',
        
        // Hero-Bereich
        'hero_title': 'Konvertieren Sie beliebige PDF-Kontoauszüge<br>in CSV-, EXCEL-, QBO- oder JSON-Format',
        'hero_subtitle': 'Optimieren Sie Ihre Finanzdatenverarbeitung mit unserer fortschrittlichen Kontoauszug-Extraktionssoftware.',
        'upload_title': 'Kontoauszug-PDF-Datei hochladen',
        'upload_text': 'PDF-Datei hier ablegen <span class="or">oder</span> <button class="browse-btn">Durchsuchen</button>',
        'browse_btn': 'Durchsuchen',
        
        // Zeitersparnis-Bereich
        'time_saving_title': 'Sparen Sie Stunden manueller Dateneingabe',
        'time_saving_subtitle': 'Verwenden Sie AI BANK PARSER, um PDF-Kontoauszüge in CSV, EXCEL, QBO oder JSON zu konvertieren',
        
        // Funktionen
        'feature_easy_title': 'Einfach zu verwenden',
        'feature_easy_desc': 'Laden Sie einfach Ihre PDF-Dateien hoch und die konvertierten Dateien werden automatisch heruntergeladen.',
        'feature_secure_title': 'Sicher und vertraulich',
        'feature_secure_desc': 'Ihr Datenschutz hat oberste Priorität. Wir stellen sicher, dass alle Konvertierungen sicher durchgeführt werden, um Ihre sensiblen Informationen zu schützen.',
        'feature_flexible_title': 'Flexible Ausgabeformate',
        'feature_flexible_desc': 'Wählen Sie aus verschiedenen Ausgabeformaten wie CSV, EXCEL, QBO oder JSON, um Ihre spezifischen Anforderungen zu erfüllen.',
        'feature_quick_title': 'Schnell und effizient',
        'feature_quick_desc': 'Konvertieren Sie Ihre Dateien in Sekunden oder Minuten, je nach Größe, und sparen Sie wertvolle Zeit.',
        'feature_batch_title': 'Stapelverarbeitung',
        'feature_batch_desc': 'Bearbeiten Sie mehrere Dateien gleichzeitig und führen Sie alle Transaktionen in einer einzigen Ergebnisdatei zusammen.',
        'feature_error_title': 'Menschliche Fehler reduzieren',
        'feature_error_desc': 'Automatisieren Sie die Datenextraktion, um Fehler bei der manuellen Eingabe zu minimieren.',
        
        // Dashboard 專用
        'dashboard_title': 'Dashboard',
        'sidebar_bank_statements': 'Kontoauszüge',
        'sidebar_invoices': 'Rechnungen',
        'sidebar_receipts': 'Belege',
        'sidebar_general': 'Allgemeine Dokumente',
        'processed_documents_count': 'Verarbeitete Dokumente',
        'remaining_credits': 'Verbleibende Credits',
        
        // Account 页面
        'account_settings': 'Kontoeinstellungen',
        'manage_account_info': 'Verwalten Sie Ihre Kontoinformationen.',
        'profile': 'Profil',
        'security': 'Sicherheit',
        'profile_details': 'Profildetails',
        'update_profile': 'Profil aktualisieren',
        'email_addresses': 'E-Mail-Adressen',
        'primary': 'Primär',
        'add_email_address': 'E-Mail-Adresse hinzufügen',
        'connected_accounts': 'Verbundene Konten',
        'connect_account': 'Konto verbinden',
        'cancel': 'Abbrechen',
        'save': 'Speichern',
        
        // Billing 页面
        'billing_credits': 'Abrechnung und Credits',
        'manage_billing_subscription': 'Abrechnung, Abonnement und Credits verwalten',
        'current_plan': 'Aktueller Plan:',
        'manage_current_subscription': 'Verwalten Sie Ihren aktuellen Abonnementplan',
        'manage': 'Verwalten',
        'add_credits': 'Credits hinzufügen',
        'add_credits_description': 'Fügen Sie Credits zu Ihrem Konto hinzu, um mehr Dokumente zu konvertieren.',
        'subscription_plans': 'Abonnementpläne',
        'monthly': 'Monatlich',
        'yearly': 'Jährlich (20% sparen)',
        'basic': 'Basic',
        'pro': 'Pro',
        'business': 'Business',
        'perfect_for_individuals': 'Perfekt für Einzelpersonen und Freelancer.',
        'small_businesses_accounting': 'Kleine Unternehmen und Buchhaltungsfirmen.',
        'growing_businesses_high_volume': 'Wachsende Unternehmen mit hohem Volumen.',
        'models': 'Modelle',
        'configurations': 'KONFIGURATIONEN',
        'account': 'Konto',
        'billing': 'Abrechnung',
        'remaining_credits': 'Verbleibende Credits',
        'transactions': 'Transaktionen',
        'in_progress': 'In Bearbeitung',
        'row_s_selected': 'Zeile(n) ausgewählt',
        'rows_per_page': 'Zeilen pro Seite',
        'page_of': 'Seite',
        'of': 'von',
        'transactions_reconciled': 'Transaktionen abgeglichen',
        'complete': 'Vollständig',
        'transactions_title': 'Transaktionen',
        'showing_transactions': 'Anzeige',
        'to': 'bis',
        'average_processing_time': 'Durchschnittliche Verarbeitungszeit',
        'processing_success_rate': 'Verarbeitungserfolgsrate'
    }
};

// 統一語言管理器
class LanguageManager {
    constructor() {
        this.currentLanguage = this.detectUserLanguage();
        this.translations = translations;
        this.init();
    }
    
    detectUserLanguage() {
        // 首先檢查localStorage中保存的語言偏好
        const savedLanguage = localStorage.getItem('language') || localStorage.getItem('preferred_language');
        if (savedLanguage && translations[savedLanguage]) {
            return savedLanguage;
        }
        
        // 獲取瀏覽器語言設置
        const browserLang = navigator.language || navigator.userLanguage;
        
        // 語言映射表
        const languageMap = {
            'zh-TW': 'zh-TW',
            'zh-CN': 'zh-CN', 
            'zh-HK': 'zh-TW', // 香港使用繁體中文
            'zh-MO': 'zh-TW', // 澳門使用繁體中文
            'zh': 'zh-CN',     // 默認中文使用簡體
            'ja': 'ja',
            'ja-JP': 'ja',
            'ko': 'ko',
            'ko-KR': 'ko',
            'es': 'es',
            'es-ES': 'es',
            'es-MX': 'es',
            'es-AR': 'es',
            'fr': 'fr',
            'fr-FR': 'fr',
            'fr-CA': 'fr',
            'de': 'de',
            'de-DE': 'de',
            'de-AT': 'de',
            'de-CH': 'de',
            'en': 'en',
            'en-US': 'en',
            'en-GB': 'en',
            'en-CA': 'en',
            'en-AU': 'en'
        };
        
        // 精確匹配
        if (languageMap[browserLang]) {
            return languageMap[browserLang];
        }
        
        // 模糊匹配（只匹配語言代碼前兩位）
        const langCode = browserLang.substring(0, 2);
        if (languageMap[langCode]) {
            return languageMap[langCode];
        }
        
        // 默認返回繁體中文
        return 'zh-TW';
    }
    
    init() {
        // 不創建語言選擇器，讓導航欄組件處理
        this.loadLanguage(this.currentLanguage);
        
        // 監聽語言變更事件
        window.addEventListener('languageChanged', (e) => {
            if (e.detail && e.detail.language) {
                this.currentLanguage = e.detail.language;
            }
        });
    }
    
    changeLanguage(lang) {
        this.currentLanguage = lang;
        localStorage.setItem('language', lang);
        localStorage.setItem('preferred_language', lang); // 兼容導航欄組件
        this.loadLanguage(lang);
        
        // 更新HTML lang屬性
        document.documentElement.lang = lang;
        
        // 觸發語言變更事件
        window.dispatchEvent(new CustomEvent('languageChanged', { 
            detail: { language: lang, translations: this.translations[lang] || this.translations['en'] } 
        }));
    }
    
    loadLanguage(lang) {
        const translation = this.translations[lang] || this.translations['en'];
        
        // 更新所有帶有 data-translate 屬性的元素
        document.querySelectorAll('[data-translate]').forEach(element => {
            const key = element.getAttribute('data-translate');
            if (translation[key]) {
                // 檢查是否包含HTML標籤
                if (translation[key].includes('<')) {
                    element.innerHTML = translation[key];
                } else {
                    element.textContent = translation[key];
                }
            }
        });
        
        // 更新具有 data-translate-placeholder 屬性的input元素
        document.querySelectorAll('[data-translate-placeholder]').forEach(element => {
            const key = element.getAttribute('data-translate-placeholder');
            if (translation[key]) {
                element.placeholder = translation[key];
            }
        });
        
        // 更新頁面標題
        if (translation['page_title']) {
            document.title = translation['page_title'];
        }
        
        // 更新HTML lang屬性
        document.documentElement.lang = lang;
        
        console.log('✅ 語言已更新為:', lang);
    }
    
    getLanguageName(lang) {
        const names = {
            'en': 'English',
            'zh-TW': '繁體中文',
            'zh-CN': '简体中文',
            'ja': '日本語',
            'ko': '한국어',
            'es': 'Español',
            'fr': 'Français',
            'de': 'Deutsch'
        };
        return names[lang] || 'English';
    }
    
    // 兼容外部調用的 switchLanguage 方法
    switchLanguage(lang) {
        this.changeLanguage(lang);
    }
}

// 初始化語言管理器
document.addEventListener('DOMContentLoaded', () => {
    // 確保在DOM完全載入後初始化語言管理器
    setTimeout(() => {
        const languageManager = new LanguageManager();
        
        // 調試信息
        console.log('Language Manager initialized');
        console.log('Detected language:', languageManager.currentLanguage);
        console.log('Browser language:', navigator.language);
        
        // 將語言管理器實例添加到window對象以便調試
        window.languageManager = languageManager;
    }, 100);
});
