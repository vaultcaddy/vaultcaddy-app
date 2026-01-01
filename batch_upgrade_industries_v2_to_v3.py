#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量升级17个行业页面 v2→v3
为每个行业定制痛点和解决方案
"""

import os
import re
from pathlib import Path

class IndustryPageUpgrader:
    def __init__(self, root_dir):
        self.root_dir = Path(root_dir)
        self.upgraded_count = 0
        self.template = None
        
        # 行业数据（名称、痛点、解决方案、专属功能）
        self.industries = {
            'ecommerce': {
                'name': 'E-commerce',
                'title': 'E-commerce Accounting Solution | Automate Order & Payment Processing',
                'description': 'AI-powered e-commerce accounting solution. Automate Shopify/Amazon orders, payment gateway reconciliation, and inventory tracking. Save 8+ hours/week.',
                'pain_points': [
                    ('🛒', 'Multi-channel Order Reconciliation', 'Manually matching orders from Shopify, Amazon, eBay (2-4 hours daily)'),
                    ('💳', 'Payment Gateway Tracking', 'Reconciling PayPal, Stripe, Square across multiple platforms'),
                    ('📦', 'Inventory Cost Calculation', 'Tracking COGS across multiple warehouses and fulfillment centers'),
                    ('💰', 'Refund & Chargeback Management', 'Manual adjustment tracking and dispute resolution')
                ],
                'solutions': [
                    ('E-commerce Platform Integration', 'Instant import from Shopify, Amazon, WooCommerce, Etsy'),
                    ('Payment Gateway Auto-match', 'Automatic reconciliation with bank deposits'),
                    ('Inventory COGS Tracking', 'Real-time cost calculation and profit margins'),
                    ('Refund Processing', 'Automated refund and chargeback accounting')
                ],
                'features': [
                    ('Shopify/Amazon/eBay Orders', 'Direct platform integration'),
                    ('PayPal/Stripe/Square', 'Payment gateway reconciliation'),
                    ('Inventory Tracking', 'Multi-warehouse COGS'),
                    ('Sales Tax Calculation', 'Multi-state tax compliance'),
                    ('Profit Margin Analysis', 'Real-time profitability'),
                    ('Refund Management', 'Automated adjustments')
                ]
            },
            'construction': {
                'name': 'Construction',
                'title': 'Construction Accounting Solution | Job Costing & Subcontractor Payment Automation',
                'description': 'AI-powered construction accounting solution. Automate job costing, subcontractor invoices, and material tracking. Save 12+ hours/week.',
                'pain_points': [
                    ('🏗️', 'Job Cost Tracking', 'Manual allocation of expenses to specific projects (3-5 hours weekly)'),
                    ('👷', 'Subcontractor Invoice Processing', 'Processing dozens of subcontractor invoices monthly'),
                    ('🧱', 'Material Cost Reconciliation', 'Matching supplier deliveries with invoices and projects'),
                    ('💰', 'Progress Billing', 'Calculating percentage completion and billing amounts')
                ],
                'solutions': [
                    ('Automated Job Costing', 'AI assigns expenses to correct job codes in 3 seconds'),
                    ('Subcontractor Invoice AI', 'Instant extraction and categorization by project'),
                    ('Material Cost Matching', 'Auto-match delivery receipts with invoices'),
                    ('Progress Billing Calculator', 'Automated percentage completion tracking')
                ],
                'features': [
                    ('Job Cost Reports', 'Real-time project profitability'),
                    ('Subcontractor Payments', 'Invoice tracking and 1099 ready'),
                    ('Material Tracking', 'By project and job code'),
                    ('Equipment Cost Allocation', 'Depreciation and usage'),
                    ('Change Order Management', 'Budget impact tracking'),
                    ('Certified Payroll', 'Davis-Bacon compliance')
                ]
            },
            'healthcare-practice': {
                'name': 'Healthcare Practice',
                'title': 'Healthcare Practice Accounting | Medical Billing & Insurance Reconciliation Automation',
                'description': 'AI-powered healthcare accounting solution. Automate insurance EOB processing, patient payments, and medical supply tracking. Save 10+ hours/week.',
                'pain_points': [
                    ('🏥', 'Insurance EOB Processing', 'Manually entering dozens of insurance payments daily (2-4 hours)'),
                    ('💊', 'Medical Supply Tracking', 'Reconciling inventory from multiple suppliers'),
                    ('👨‍⚕️', 'Patient Payment Matching', 'Matching partial payments to invoices and insurance'),
                    ('💰', 'Revenue Cycle Management', 'Tracking AR aging and denied claims')
                ],
                'solutions': [
                    ('EOB Auto-processing', 'AI extracts insurance payments and adjustments in 3 seconds'),
                    ('Supply Cost Tracking', 'Automated medical supply reconciliation'),
                    ('Patient Payment Matching', 'Intelligent matching to open invoices'),
                    ('AR Aging Dashboard', 'Real-time aging and denial tracking')
                ],
                'features': [
                    ('Insurance EOB Import', 'All major carriers'),
                    ('Patient Payment Portal', 'Online payment tracking'),
                    ('Medical Supply Costs', 'By procedure and department'),
                    ('Revenue Cycle Reports', 'Days in AR and collection rate'),
                    ('Payroll for Clinical Staff', 'Hourly and salary tracking'),
                    ('HIPAA Compliance', 'Secure document storage')
                ]
            },
            'law-firm': {
                'name': 'Law Firm',
                'title': 'Law Firm Accounting Solution | Trust Accounting & Client Billing Automation',
                'description': 'AI-powered law firm accounting solution. Automate IOLTA trust accounting, client billing, and case expense tracking. Save 8+ hours/week.',
                'pain_points': [
                    ('⚖️', 'Trust Account Reconciliation', 'Monthly IOLTA reconciliation (4-6 hours monthly)'),
                    ('💼', 'Client Cost Allocation', 'Tracking expenses by case and client'),
                    ('📄', 'Retainer Management', 'Monitoring retainer balances and replenishment'),
                    ('💰', 'Multi-entity Accounting', 'Managing multiple partnerships and LLCs')
                ],
                'solutions': [
                    ('IOLTA Auto-reconciliation', '3-second trust account matching and reporting'),
                    ('Case Expense Tracking', 'AI assigns costs to correct case numbers'),
                    ('Retainer Monitoring', 'Automated low-balance alerts'),
                    ('Multi-entity Dashboard', 'Consolidated and separate entity reporting')
                ],
                'features': [
                    ('IOLTA Trust Accounting', 'Bar association compliant'),
                    ('Client Matter Reports', 'Real-time profitability by case'),
                    ('Retainer Tracking', 'Balance monitoring and invoicing'),
                    ('Expense Allocation', 'By client, matter, attorney'),
                    ('1099 for Expert Witnesses', 'Automated vendor reporting'),
                    ('Multi-entity Support', 'Partnership and LLC accounting')
                ]
            },
            'real-estate': {
                'name': 'Real Estate',
                'title': 'Real Estate Accounting Solution | Rental Income & Property Expense Tracking',
                'description': 'AI-powered real estate accounting solution. Automate rent collection, property maintenance tracking, and tenant deposits. Save 6+ hours/week.',
                'pain_points': [
                    ('🏡', 'Multi-property Tracking', 'Managing income/expenses across multiple properties (2-3 hours weekly)'),
                    ('💰', 'Rent Collection Reconciliation', 'Matching tenant payments to units and leases'),
                    ('🔧', 'Maintenance Cost Allocation', 'Tracking repairs and improvements by property'),
                    ('💵', 'Security Deposit Management', 'Monitoring tenant deposits and refunds')
                ],
                'solutions': [
                    ('Property-level Tracking', 'AI categorizes transactions by property automatically'),
                    ('Rent Auto-matching', 'Instant matching of payments to tenant accounts'),
                    ('Maintenance Cost Reports', 'Real-time expense tracking by property'),
                    ('Deposit Liability Tracking', 'Automated security deposit accounting')
                ],
                'features': [
                    ('Property Income/Expense', 'Separate P&L per property'),
                    ('Tenant Rent Tracking', 'Late fee calculation'),
                    ('Maintenance Costs', 'By property and unit'),
                    ('Security Deposit Ledger', 'State compliance reporting'),
                    ('Property Tax Tracking', 'Payment reminders'),
                    ('Capital Improvements', 'Depreciation scheduling')
                ]
            },
            'manufacturing': {
                'name': 'Manufacturing',
                'title': 'Manufacturing Accounting Solution | Production Costing & Inventory Management',
                'description': 'AI-powered manufacturing accounting solution. Automate production costing, raw material tracking, and work-in-process accounting. Save 15+ hours/week.',
                'pain_points': [
                    ('🏭', 'Production Cost Allocation', 'Manual calculation of direct/indirect costs (4-6 hours weekly)'),
                    ('📦', 'Raw Material Tracking', 'Reconciling inventory from multiple suppliers'),
                    ('⚙️', 'Work-in-Process Accounting', 'Tracking costs through production stages'),
                    ('💰', 'Overhead Allocation', 'Distributing factory overhead to products')
                ],
                'solutions': [
                    ('Automated Cost Allocation', 'AI calculates production costs in real-time'),
                    ('Material Cost Tracking', 'Instant reconciliation with purchase orders'),
                    ('WIP Dashboard', 'Real-time production stage tracking'),
                    ('Overhead Distribution', 'Automated absorption costing')
                ],
                'features': [
                    ('Production Cost Reports', 'By product line and batch'),
                    ('Raw Material Inventory', 'FIFO/LIFO/Average costing'),
                    ('WIP Tracking', 'By production order'),
                    ('Finished Goods Costing', 'Landed cost calculation'),
                    ('Overhead Allocation', 'Machine hour or labor hour basis'),
                    ('Variance Analysis', 'Standard vs. actual costs')
                ]
            },
            'logistics-shipping': {
                'name': 'Logistics & Shipping',
                'title': 'Logistics Accounting Solution | Freight Invoice & Fuel Cost Automation',
                'description': 'AI-powered logistics accounting solution. Automate freight invoices, fuel card reconciliation, and carrier payments. Save 12+ hours/week.',
                'pain_points': [
                    ('🚚', 'Freight Invoice Processing', 'Processing hundreds of carrier invoices monthly (3-5 hours weekly)'),
                    ('⛽', 'Fuel Card Reconciliation', 'Matching fuel purchases to trips and drivers'),
                    ('💼', 'Load Profitability Tracking', 'Calculating margin by shipment and route'),
                    ('💰', 'Carrier Payment Management', '1099 tracking for owner-operators')
                ],
                'solutions': [
                    ('Freight Invoice AI', '3-second extraction and shipment matching'),
                    ('Fuel Auto-reconciliation', 'Instant matching to trips and drivers'),
                    ('Load Profit Calculator', 'Real-time margin analysis by route'),
                    ('Carrier Payment Automation', 'Automated 1099 preparation')
                ],
                'features': [
                    ('Freight Invoice Import', 'All major carriers'),
                    ('Fuel Card Integration', 'By driver and vehicle'),
                    ('Load Profitability', 'Revenue minus all costs'),
                    ('Carrier Payments', '1099 and COI tracking'),
                    ('Equipment Costs', 'Maintenance and depreciation'),
                    ('Route Analysis', 'Most profitable lanes')
                ]
            },
            'consulting-firm': {
                'name': 'Consulting Firm',
                'title': 'Consulting Firm Accounting | Project Billing & Expense Tracking Automation',
                'description': 'AI-powered consulting accounting solution. Automate project billing, client expense tracking, and consultant payouts. Save 8+ hours/week.',
                'pain_points': [
                    ('💼', 'Project Cost Tracking', 'Manual allocation of time and expenses to projects (3-4 hours weekly)'),
                    ('✈️', 'Client Expense Reimbursement', 'Processing consultant expense reports'),
                    ('📊', 'Retainer Management', 'Tracking consulting retainers and billing'),
                    ('💰', 'Contractor Payment', 'Managing payments to independent consultants')
                ],
                'solutions': [
                    ('Project Cost Automation', 'AI assigns expenses to correct client projects'),
                    ('Expense Report Processing', '3-second extraction and categorization'),
                    ('Retainer Dashboard', 'Real-time balance and usage tracking'),
                    ('Contractor Payments', 'Automated 1099 preparation')
                ],
                'features': [
                    ('Project P&L Reports', 'Real-time profitability by client'),
                    ('Consultant Expenses', 'Travel, meals, and other costs'),
                    ('Retainer Tracking', 'Hours and dollar balance monitoring'),
                    ('Contractor Payments', '1099 compliance'),
                    ('Time & Billing Integration', 'Hours to accounting sync'),
                    ('Multi-client Dashboard', 'All projects in one view')
                ]
            },
            'freelancer': {
                'name': 'Freelancer',
                'title': 'Freelancer Accounting Solution | Income Tracking & Expense Management',
                'description': 'AI-powered freelancer accounting solution. Automate client invoice tracking, business expense categorization, and quarterly tax prep. Save 5+ hours/week.',
                'pain_points': [
                    ('💼', 'Multiple Income Sources', 'Tracking payments from various clients and platforms (2-3 hours weekly)'),
                    ('📄', 'Expense Categorization', 'Manually sorting business vs. personal expenses'),
                    ('💰', 'Quarterly Tax Calculation', 'Estimating self-employment tax and estimated payments'),
                    ('🏦', 'Client Invoice Tracking', 'Following up on late payments and AR aging')
                ],
                'solutions': [
                    ('Multi-platform Income Tracking', 'Auto-import from PayPal, Stripe, Upwork, Fiverr'),
                    ('Smart Expense Categorization', 'AI sorts business expenses in 3 seconds'),
                    ('Quarterly Tax Calculator', 'Real-time tax liability estimation'),
                    ('AR Aging Dashboard', 'Automated late payment reminders')
                ],
                'features': [
                    ('Multi-platform Income', 'PayPal, Venmo, Stripe, Zelle'),
                    ('Business Expense Tracking', 'IRS Schedule C categories'),
                    ('Mileage Tracking', 'Business trip documentation'),
                    ('Quarterly Tax Estimates', 'Form 1040-ES calculations'),
                    ('Client Invoice Status', 'Paid, pending, overdue'),
                    ('1099-K Reconciliation', 'Platform income matching')
                ]
            },
            'small-business': {
                'name': 'Small Business',
                'title': 'Small Business Accounting Solution | All-in-One Financial Management',
                'description': 'AI-powered small business accounting solution. Automate bookkeeping, expense tracking, and financial reporting. Save 10+ hours/week.',
                'pain_points': [
                    ('📊', 'Manual Bookkeeping', 'Spending hours on data entry every week (3-5 hours)'),
                    ('💼', 'Expense Management', 'Sorting business receipts and categorizing'),
                    ('💰', 'Cash Flow Monitoring', 'Not knowing cash position in real-time'),
                    ('📄', 'Tax Preparation', 'Scrambling for documents at year-end')
                ],
                'solutions': [
                    ('Automated Bookkeeping', 'AI does all data entry in 3 seconds'),
                    ('Smart Expense Sorting', 'Automatic categorization and tax classification'),
                    ('Real-time Cash Dashboard', 'Live cash position and forecasting'),
                    ('Tax-ready Reports', 'Always audit-ready documentation')
                ],
                'features': [
                    ('Bank/Credit Card Sync', 'All major financial institutions'),
                    ('Expense Categorization', 'AI-powered smart sorting'),
                    ('Invoice & Bill Management', 'AP and AR tracking'),
                    ('Financial Reports', 'P&L, Balance Sheet, Cash Flow'),
                    ('Tax Preparation Export', 'QuickBooks, Excel, CPA ready'),
                    ('Multi-user Access', 'Accountant and bookkeeper sharing')
                ]
            },
            'nonprofit-organization': {
                'name': 'Nonprofit Organization',
                'title': 'Nonprofit Accounting Solution | Fund Accounting & Grant Tracking',
                'description': 'AI-powered nonprofit accounting solution. Automate fund accounting, grant expense tracking, and donor reporting. Save 8+ hours/week.',
                'pain_points': [
                    ('💼', 'Fund Accounting', 'Manual tracking of restricted vs. unrestricted funds (3-4 hours weekly)'),
                    ('💰', 'Grant Expense Tracking', 'Ensuring expenses comply with grant requirements'),
                    ('📊', 'Donor Reporting', 'Creating custom reports for different donor requirements'),
                    ('📄', 'IRS Form 990 Preparation', 'Gathering data for annual filing')
                ],
                'solutions': [
                    ('Automated Fund Accounting', 'AI assigns transactions to correct funds'),
                    ('Grant Compliance Tracking', 'Real-time budget vs. actual by grant'),
                    ('Custom Donor Reports', 'One-click donor impact statements'),
                    ('990-ready Documentation', 'Always prepared for annual filing')
                ],
                'features': [
                    ('Fund Accounting', 'Restricted, unrestricted, endowment'),
                    ('Grant Tracking', 'Budget vs. actual by grant'),
                    ('Donor Reporting', 'Custom donor impact reports'),
                    ('IRS Form 990 Export', 'Schedule-ready data'),
                    ('In-kind Donations', 'Non-cash contribution tracking'),
                    ('Program Expense Allocation', 'Functional expense reporting')
                ]
            },
            'professional-services': {
                'name': 'Professional Services',
                'title': 'Professional Services Accounting | Time Billing & Project Management',
                'description': 'AI-powered professional services accounting. Automate time billing, project expenses, and client invoicing. Save 8+ hours/week.',
                'pain_points': [
                    ('⏱️', 'Time & Billing', 'Manual timekeeping and invoice generation (2-3 hours weekly)'),
                    ('💼', 'Project Expense Allocation', 'Tracking billable vs. non-billable costs'),
                    ('📊', 'Utilization Reporting', 'Calculating staff utilization rates'),
                    ('💰', 'Retainer Management', 'Monitoring client retainer balances')
                ],
                'solutions': [
                    ('Automated Time Billing', 'AI generates invoices from timesheets'),
                    ('Smart Expense Allocation', 'Automatic billable expense tagging'),
                    ('Utilization Dashboard', 'Real-time staff utilization tracking'),
                    ('Retainer Automation', 'Auto-alerts for low balances')
                ],
                'features': [
                    ('Time & Billing Integration', 'Connect with time tracking tools'),
                    ('Project P&L', 'Real-time profitability by client'),
                    ('Billable Expense Tracking', 'Client reimbursable costs'),
                    ('Utilization Reports', 'Staff efficiency analysis'),
                    ('Retainer Management', 'Balance and usage monitoring'),
                    ('WIP Reports', 'Work in progress tracking')
                ]
            },
            'retail-store': {
                'name': 'Retail Store',
                'title': 'Retail Accounting Solution | Point of Sale & Inventory Management',
                'description': 'AI-powered retail accounting solution. Automate POS reconciliation, inventory costing, and multi-location tracking. Save 8+ hours/week.',
                'pain_points': [
                    ('🏪', 'POS System Reconciliation', 'Daily reconciliation of cash, credit, and gift cards (1-2 hours daily)'),
                    ('📦', 'Inventory Costing', 'Tracking COGS across multiple locations'),
                    ('💰', 'Multi-location Tracking', 'Separate accounting for each store location'),
                    ('📊', 'Sales Tax Compliance', 'Multi-state sales tax collection and remittance')
                ],
                'solutions': [
                    ('POS Auto-reconciliation', 'Instant matching of POS to bank deposits'),
                    ('Inventory COGS Tracking', 'Real-time cost of goods sold calculation'),
                    ('Multi-location Dashboard', 'Consolidated and separate store reporting'),
                    ('Sales Tax Automation', 'Automatic calculation and filing prep')
                ],
                'features': [
                    ('POS Integration', 'Square, Clover, Shopify POS'),
                    ('Inventory Management', 'FIFO, LIFO, average cost'),
                    ('Multi-location Reports', 'By store and consolidated'),
                    ('Sales Tax Tracking', 'By state and jurisdiction'),
                    ('Gift Card Liability', 'Outstanding balance tracking'),
                    ('Employee Discount Tracking', 'Staff purchase monitoring')
                ]
            },
            'travel-agency': {
                'name': 'Travel Agency',
                'title': 'Travel Agency Accounting | Commission Tracking & Client Payment Management',
                'description': 'AI-powered travel agency accounting. Automate commission reconciliation, client payment tracking, and vendor payouts. Save 6+ hours/week.',
                'pain_points': [
                    ('✈️', 'Commission Reconciliation', 'Tracking commissions from airlines, hotels, cruise lines (2-3 hours weekly)'),
                    ('💼', 'Client Payment Tracking', 'Managing deposits, final payments, and refunds'),
                    ('🏨', 'Vendor Payment Management', 'Paying suppliers on behalf of clients'),
                    ('💰', 'Multi-currency Transactions', 'Handling foreign currency bookings and payments')
                ],
                'solutions': [
                    ('Commission Auto-matching', 'AI matches supplier payments to bookings'),
                    ('Client Payment Automation', 'Automated payment reminders and tracking'),
                    ('Vendor Payment Dashboard', 'Real-time supplier payment status'),
                    ('Multi-currency Tracking', 'Automatic foreign exchange conversion')
                ],
                'features': [
                    ('Commission Tracking', 'By supplier and booking'),
                    ('Client Payment Status', 'Deposit, balance, paid'),
                    ('Vendor Payments', 'Supplier payment reconciliation'),
                    ('Multi-currency Support', 'Foreign exchange tracking'),
                    ('Refund Management', 'Client refund processing'),
                    ('Booking Profitability', 'Commission minus costs')
                ]
            },
            'insurance-agency': {
                'name': 'Insurance Agency',
                'title': 'Insurance Agency Accounting | Commission Tracking & Carrier Reconciliation',
                'description': 'AI-powered insurance agency accounting. Automate commission reconciliation, carrier statement processing, and agent payouts. Save 10+ hours/week.',
                'pain_points': [
                    ('💼', 'Commission Reconciliation', 'Matching carrier commissions to policies sold (3-5 hours weekly)'),
                    ('📄', 'Carrier Statement Processing', 'Processing statements from multiple carriers'),
                    ('💰', 'Agent Commission Splits', 'Calculating agent payouts and overrides'),
                    ('📊', 'Policy Revenue Tracking', 'Monitoring renewals and cancellations')
                ],
                'solutions': [
                    ('Commission Auto-matching', 'AI matches carrier payments to policies'),
                    ('Carrier Statement AI', '3-second extraction and categorization'),
                    ('Agent Payout Automation', 'Automatic split calculations'),
                    ('Revenue Dashboard', 'Real-time policy revenue tracking')
                ],
                'features': [
                    ('Commission Tracking', 'By carrier and policy type'),
                    ('Carrier Reconciliation', 'Statement-to-payment matching'),
                    ('Agent Splits', 'Multi-level commission structure'),
                    ('Policy Revenue', 'New, renewal, cancellation tracking'),
                    ('1099 for Agents', 'Independent agent reporting'),
                    ('E&O Insurance Tracking', 'Coverage monitoring')
                ]
            },
            'agriculture-farming': {
                'name': 'Agriculture & Farming',
                'title': 'Agriculture Accounting Solution | Crop Cost & Equipment Expense Tracking',
                'description': 'AI-powered agriculture accounting solution. Automate crop production costing, equipment expense tracking, and government subsidy management. Save 8+ hours/week.',
                'pain_points': [
                    ('🌾', 'Crop Production Costing', 'Tracking costs by field and crop type (3-4 hours weekly)'),
                    ('🚜', 'Equipment Expense Allocation', 'Distributing equipment costs across fields'),
                    ('💰', 'Government Subsidy Tracking', 'Monitoring USDA payments and requirements'),
                    ('📊', 'Livestock Cost Accounting', 'Tracking feed, veterinary, and other livestock costs')
                ],
                'solutions': [
                    ('Automated Crop Costing', 'AI assigns costs to correct fields and crops'),
                    ('Equipment Cost Allocation', 'Automatic distribution by field usage'),
                    ('Subsidy Dashboard', 'Real-time USDA payment tracking'),
                    ('Livestock Cost Tracking', 'Per-head cost calculation')
                ],
                'features': [
                    ('Crop Production Reports', 'Cost per acre and per bushel'),
                    ('Equipment Costs', 'Depreciation and maintenance'),
                    ('Government Subsidy Tracking', 'USDA payment monitoring'),
                    ('Livestock Accounting', 'Feed, veterinary, breeding costs'),
                    ('Land Improvement Tracking', 'Capital vs. operating expenses'),
                    ('Harvest Revenue', 'By crop and field')
                ]
            }
        }
    
    def load_template(self):
        """加载v3模板"""
        template_path = self.root_dir / 'restaurant-accounting-v3-test.html'
        if not template_path.exists():
            print(f"❌ 找不到模板: {template_path}")
            return False
        
        with open(template_path, 'r', encoding='utf-8') as f:
            self.template = f.read()
        
        print("✅ 模板加载成功")
        return True
    
    def extract_industry_key(self, filename):
        """从文件名提取行业key"""
        return filename.replace('-accounting-v2.html', '')
    
    def customize_template(self, industry_key):
        """自定义模板"""
        if industry_key not in self.industries:
            print(f"⚠️ 未找到行业数据: {industry_key}")
            return None
        
        industry = self.industries[industry_key]
        content = self.template
        
        # 1. 替换标题和描述
        content = re.sub(
            r'<title>.*?</title>',
            f'<title>{industry["title"]}</title>',
            content,
            flags=re.DOTALL
        )
        
        content = re.sub(
            r'<meta name="description" content=".*?">',
            f'<meta name="description" content="{industry["description"]}">',
            content
        )
        
        # 2. 替换行业名称
        content = content.replace('Restaurant', industry['name'])
        content = content.replace('restaurant', industry['name'].lower())
        
        # 3. 替换痛点部分
        pain_points_html = ''
        for emoji, title, desc in industry['pain_points']:
            pain_points_html += f'''                <div class="pain-card">
                    <div class="pain-icon">{emoji}</div>
                    <h3>{title}</h3>
                    <p>{desc}</p>
                </div>\n'''
        
        content = re.sub(
            r'<!-- Pain Points Section -->.*?</section>',
            f'''<!-- Pain Points Section -->
    <section style="padding: 80px 24px; background: white;">
        <div style="max-width: 1200px; margin: 0 auto;">
            <h2 style="text-align: center; font-size: 42px; font-weight: 800; margin-bottom: 60px; color: #1a202c;">
                Common {industry['name']} Accounting Challenges
            </h2>
            <div class="pain-points">
{pain_points_html}            </div>
        </div>
    </section>''',
            content,
            flags=re.DOTALL
        )
        
        # 4. 替换解决方案部分
        solutions_html = ''
        for title, desc in industry['solutions']:
            solutions_html += f'''                <div class="solution-card">
                    <div class="solution-badge">✓</div>
                    <h3>{title}</h3>
                    <p>{desc}</p>
                </div>\n'''
        
        content = re.sub(
            r'<!-- Solutions Section -->.*?</section>',
            f'''<!-- Solutions Section -->
    <section style="padding: 80px 24px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
        <div style="max-width: 1200px; margin: 0 auto;">
            <h2 style="text-align: center; font-size: 42px; font-weight: 800; margin-bottom: 20px; color: white;">
                How VaultCaddy Solves These Problems
            </h2>
            <p style="text-align: center; font-size: 20px; color: rgba(255,255,255,0.9); margin-bottom: 60px; max-width: 800px; margin-left: auto; margin-right: auto;">
                AI-powered automation designed specifically for {industry['name'].lower()} businesses
            </p>
            <div class="solutions">
{solutions_html}            </div>
        </div>
    </section>''',
            content,
            flags=re.DOTALL
        )
        
        # 5. 替换专属功能部分
        features_html = ''
        for title, desc in industry['features']:
            features_html += f'''                <div class="feature-card">
                    <div class="feature-icon">✓</div>
                    <h3>{title}</h3>
                    <p>{desc}</p>
                </div>\n'''
        
        content = re.sub(
            r'<!-- Exclusive Features -->.*?</section>',
            f'''<!-- Exclusive Features -->
    <section style="padding: 80px 24px; background: #f8fafc;">
        <div style="max-width: 1200px; margin: 0 auto;">
            <h2 style="text-align: center; font-size: 42px; font-weight: 800; margin-bottom: 60px; color: #1a202c;">
                {industry['name']}-Specific Features
            </h2>
            <div class="features">
{features_html}            </div>
        </div>
    </section>''',
            content,
            flags=re.DOTALL
        )
        
        return content
    
    def upgrade_file(self, file_path):
        """升级单个行业页面"""
        try:
            print(f"\n🔧 处理: {file_path.name}")
            
            # 提取行业key
            industry_key = self.extract_industry_key(file_path.name)
            print(f"  🏢 行业: {self.industries.get(industry_key, {}).get('name', industry_key)}")
            
            # 自定义模板
            new_content = self.customize_template(industry_key)
            if not new_content:
                return False
            
            # 创建新文件名
            new_filename = file_path.name.replace('-v2.html', '-v3.html')
            new_file_path = file_path.parent / new_filename
            
            # 写入新文件
            with open(new_file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"  ✅ 创建: {new_filename}")
            self.upgraded_count += 1
            return True
            
        except Exception as e:
            print(f"  ❌ 失败: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def upgrade_all(self):
        """升级所有行业页面"""
        print("🚀 开始批量升级行业页面...")
        print("=" * 80)
        
        # 加载模板
        if not self.load_template():
            return
        
        # 查找所有行业accounting页面
        industry_files = list(self.root_dir.glob('*-accounting-v2.html'))
        
        print(f"\n📊 找到 {len(industry_files)} 个行业页面")
        print("=" * 80)
        
        # 升级每个文件
        for file_path in industry_files:
            if 'backup' in file_path.name:
                continue
            self.upgrade_file(file_path)
        
        print("\n" + "=" * 80)
        print("🎉 Phase 2: 行业页面升级完成！")
        print("=" * 80)
        print(f"\n📊 总计:")
        print(f"   - 找到 {len(industry_files)} 个行业页面")
        print(f"   - 成功升级 {self.upgraded_count} 个页面")
        print(f"\n✅ 所有新v3文件已创建")
        print(f"💾 原v2文件保持不变")

def main():
    root_dir = '/Users/cavlinyeung/ai-bank-parser'
    
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║              🏢 Phase 2: 批量升级行业页面 v2→v3                               ║
║                                                                              ║
║  升级内容:                                                                    ║
║    ✓ 使用restaurant-accounting-v3-test.html模板                              ║
║    ✓ 为每个行业定制痛点和解决方案                                            ║
║    ✓ 纯英文内容                                                              ║
║    ✓ 正确定价（$5.59/月，$7/月）                                              ║
║    ✓ 正确链接（/en/auth.html）                                                ║
║    ✓ 包含GIF演示部分                                                          ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    upgrader = IndustryPageUpgrader(root_dir)
    upgrader.upgrade_all()
    
    print("\n" + "=" * 80)
    print("✅ Phase 2 完成！")
    print("=" * 80)
    print("\n下一步: Phase 3 - 升级5个功能页面")

if __name__ == '__main__':
    main()

