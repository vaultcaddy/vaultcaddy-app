#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量将所有50个v3页面转换为新设计
基于 chase-bank-statement-v3-redesign.html 模板
"""

import os
import re

# 所有50个银行页面的配置
BANKS = [
    # 美国银行 (10个) - USD $5.59/month
    {
        "file": "chase-bank-statement-v3.html",
        "bank_name": "Chase Bank",
        "country": "USA",
        "currency": "USD",
        "monthly_price": "$7",
        "annual_price": "$5.59",
        "annual_total": "$67",
        "per_page": "$0.06",
        "title": "Chase Bank USA Statement Converter | PDF to Excel/QuickBooks | 98% Accuracy",
        "description": "AI-powered Chase Bank USA statement converter. Convert PDF to Excel/QuickBooks/Xero in 3 seconds with 98% accuracy. From $5.59/month | 500+ businesses trust us",
        "h1": "Convert Chase Bank<br>Statements in Seconds",
        "hero_text": "AI-powered PDF to Excel/QuickBooks converter with 98% accuracy.<br>No manual data entry. No templates. Just fast, accurate results.",
        "features_subtitle": "Built specifically for Chase Bank statements",
        "account_types": "Chase Total Checking, Chase Savings, Chase Business Complete Banking, Chase Credit Cards (Sapphire, Freedom, Ink), Chase Private Client accounts, and Chase First Banking"
    },
    {
        "file": "bank-of-america-statement-v3.html",
        "bank_name": "Bank of America",
        "country": "USA",
        "currency": "USD",
        "monthly_price": "$7",
        "annual_price": "$5.59",
        "annual_total": "$67",
        "per_page": "$0.06",
        "title": "Bank of America Statement Converter | PDF to Excel/QuickBooks | 98% Accuracy",
        "description": "AI-powered Bank of America statement converter. Convert PDF to Excel/QuickBooks/Xero in 3 seconds with 98% accuracy. From $5.59/month",
        "h1": "Convert Bank of America<br>Statements in Seconds",
        "hero_text": "AI-powered PDF to Excel/QuickBooks converter with 98% accuracy.<br>No manual data entry. No templates. Just fast, accurate results.",
        "features_subtitle": "Built specifically for Bank of America statements",
        "account_types": "Bank of America Advantage Banking, Savings Accounts, Business Advantage accounts, BofA Credit Cards (Cash Rewards, Travel Rewards, Premium Rewards), Merrill Edge accounts"
    },
    {
        "file": "wells-fargo-statement-v3.html",
        "bank_name": "Wells Fargo",
        "country": "USA",
        "currency": "USD",
        "monthly_price": "$7",
        "annual_price": "$5.59",
        "annual_total": "$67",
        "per_page": "$0.06",
        "title": "Wells Fargo Statement Converter | PDF to Excel/QuickBooks | 98% Accuracy",
        "description": "AI-powered Wells Fargo statement converter. Convert PDF to Excel/QuickBooks/Xero in 3 seconds with 98% accuracy. From $5.59/month",
        "h1": "Convert Wells Fargo<br>Statements in Seconds",
        "hero_text": "AI-powered PDF to Excel/QuickBooks converter with 98% accuracy.<br>No manual data entry. No templates. Just fast, accurate results.",
        "features_subtitle": "Built specifically for Wells Fargo statements",
        "account_types": "Wells Fargo Everyday Checking, Way2Save Savings, Business Checking, Wells Fargo Credit Cards (Active Cash, Autograph, Reflect), Propel Card"
    },
    {
        "file": "citibank-statement-v3.html",
        "bank_name": "Citibank",
        "country": "USA",
        "currency": "USD",
        "monthly_price": "$7",
        "annual_price": "$5.59",
        "annual_total": "$67",
        "per_page": "$0.06",
        "title": "Citibank USA Statement Converter | PDF to Excel/QuickBooks | 98% Accuracy",
        "description": "AI-powered Citibank USA statement converter. Convert PDF to Excel/QuickBooks/Xero in 3 seconds with 98% accuracy. From $5.59/month",
        "h1": "Convert Citibank<br>Statements in Seconds",
        "hero_text": "AI-powered PDF to Excel/QuickBooks converter with 98% accuracy.<br>No manual data entry. No templates. Just fast, accurate results.",
        "features_subtitle": "Built specifically for Citibank statements",
        "account_types": "Citi Basic Banking, Citi Priority accounts, Citi Business accounts, Citi Credit Cards (Double Cash, Premier, Custom Cash), Citi ThankYou Rewards"
    },
    {
        "file": "capital-one-statement-v3.html",
        "bank_name": "Capital One",
        "country": "USA",
        "currency": "USD",
        "monthly_price": "$7",
        "annual_price": "$5.59",
        "annual_total": "$67",
        "per_page": "$0.06",
        "title": "Capital One Statement Converter | PDF to Excel/QuickBooks | 98% Accuracy",
        "description": "AI-powered Capital One statement converter. Convert PDF to Excel/QuickBooks/Xero in 3 seconds with 98% accuracy. From $5.59/month",
        "h1": "Convert Capital One<br>Statements in Seconds",
        "hero_text": "AI-powered PDF to Excel/QuickBooks converter with 98% accuracy.<br>No manual data entry. No templates. Just fast, accurate results.",
        "features_subtitle": "Built specifically for Capital One statements",
        "account_types": "Capital One 360 Checking, 360 Savings, Spark Business accounts, Capital One Credit Cards (Venture, SavorOne, Quicksilver), 360 Performance Savings"
    },
    {
        "file": "us-bank-statement-v3.html",
        "bank_name": "U.S. Bank",
        "country": "USA",
        "currency": "USD",
        "monthly_price": "$7",
        "annual_price": "$5.59",
        "annual_total": "$67",
        "per_page": "$0.06",
        "title": "U.S. Bank Statement Converter | PDF to Excel/QuickBooks | 98% Accuracy",
        "description": "AI-powered U.S. Bank statement converter. Convert PDF to Excel/QuickBooks/Xero in 3 seconds with 98% accuracy. From $5.59/month",
        "h1": "Convert U.S. Bank<br>Statements in Seconds",
        "hero_text": "AI-powered PDF to Excel/QuickBooks converter with 98% accuracy.<br>No manual data entry. No templates. Just fast, accurate results.",
        "features_subtitle": "Built specifically for U.S. Bank statements",
        "account_types": "U.S. Bank Smartly Checking, Elite Money Market, Silver Business Checking, U.S. Bank Credit Cards (Altitude Go, Cash+, Shopper Cash Rewards)"
    },
    {
        "file": "pnc-bank-statement-v3.html",
        "bank_name": "PNC Bank",
        "country": "USA",
        "currency": "USD",
        "monthly_price": "$7",
        "annual_price": "$5.59",
        "annual_total": "$67",
        "per_page": "$0.06",
        "title": "PNC Bank Statement Converter | PDF to Excel/QuickBooks | 98% Accuracy",
        "description": "AI-powered PNC Bank statement converter. Convert PDF to Excel/QuickBooks/Xero in 3 seconds with 98% accuracy. From $5.59/month",
        "h1": "Convert PNC Bank<br>Statements in Seconds",
        "hero_text": "AI-powered PDF to Excel/QuickBooks converter with 98% accuracy.<br>No manual data entry. No templates. Just fast, accurate results.",
        "features_subtitle": "Built specifically for PNC Bank statements",
        "account_types": "PNC Virtual Wallet, PNC Savings accounts, PNC Business Checking, PNC Credit Cards (Cash Rewards, Points, Core)"
    },
    {
        "file": "td-bank-statement-v3.html",
        "bank_name": "TD Bank",
        "country": "USA",
        "currency": "USD",
        "monthly_price": "$7",
        "annual_price": "$5.59",
        "annual_total": "$67",
        "per_page": "$0.06",
        "title": "TD Bank USA Statement Converter | PDF to Excel/QuickBooks | 98% Accuracy",
        "description": "AI-powered TD Bank USA statement converter. Convert PDF to Excel/QuickBooks/Xero in 3 seconds with 98% accuracy. From $5.59/month",
        "h1": "Convert TD Bank<br>Statements in Seconds",
        "hero_text": "AI-powered PDF to Excel/QuickBooks converter with 98% accuracy.<br>No manual data entry. No templates. Just fast, accurate results.",
        "features_subtitle": "Built specifically for TD Bank statements",
        "account_types": "TD Convenience Checking, TD Beyond Savings, TD Business Checking, TD Credit Cards (Cash, Double Up, Travel)"
    },
    {
        "file": "truist-bank-statement-v3.html",
        "bank_name": "Truist Bank",
        "country": "USA",
        "currency": "USD",
        "monthly_price": "$7",
        "annual_price": "$5.59",
        "annual_total": "$67",
        "per_page": "$0.06",
        "title": "Truist Bank Statement Converter | PDF to Excel/QuickBooks | 98% Accuracy",
        "description": "AI-powered Truist Bank statement converter. Convert PDF to Excel/QuickBooks/Xero in 3 seconds with 98% accuracy. From $5.59/month",
        "h1": "Convert Truist Bank<br>Statements in Seconds",
        "hero_text": "AI-powered PDF to Excel/QuickBooks converter with 98% accuracy.<br>No manual data entry. No templates. Just fast, accurate results.",
        "features_subtitle": "Built specifically for Truist Bank statements",
        "account_types": "Truist One Banking, Truist Confidence accounts, Truist Business Checking, Truist Credit Cards (Enjoy Cash, Enjoy Travel, Enjoy Beyond)"
    },
    {
        "file": "ally-bank-statement-v3.html",
        "bank_name": "Ally Bank",
        "country": "USA",
        "currency": "USD",
        "monthly_price": "$7",
        "annual_price": "$5.59",
        "annual_total": "$67",
        "per_page": "$0.06",
        "title": "Ally Bank Statement Converter | PDF to Excel/QuickBooks | 98% Accuracy",
        "description": "AI-powered Ally Bank statement converter. Convert PDF to Excel/QuickBooks/Xero in 3 seconds with 98% accuracy. From $5.59/month",
        "h1": "Convert Ally Bank<br>Statements in Seconds",
        "hero_text": "AI-powered PDF to Excel/QuickBooks converter with 98% accuracy.<br>No manual data entry. No templates. Just fast, accurate results.",
        "features_subtitle": "Built specifically for Ally Bank statements",
        "account_types": "Ally Interest Checking, Online Savings Account, Money Market Account, Ally Credit Card (Cashback)"
    },
    
    # 英国银行 (5个) - GBP £4.59/month
    {
        "file": "hsbc-uk-bank-statement-v3.html",
        "bank_name": "HSBC UK",
        "country": "United Kingdom",
        "currency": "GBP",
        "monthly_price": "£5.75",
        "annual_price": "£4.59",
        "annual_total": "£55",
        "per_page": "£0.05",
        "title": "HSBC UK Statement Converter | PDF to Excel/QuickBooks | 98% Accuracy",
        "description": "AI-powered HSBC UK statement converter. Convert PDF to Excel/QuickBooks/Xero in 3 seconds with 98% accuracy. From £4.59/month",
        "h1": "Convert HSBC UK<br>Statements in Seconds",
        "hero_text": "AI-powered PDF to Excel/QuickBooks converter with 98% accuracy.<br>No manual data entry. No templates. Just fast, accurate results.",
        "features_subtitle": "Built specifically for HSBC UK statements",
        "account_types": "HSBC Bank Account, HSBC Advance, HSBC Premier, HSBC Business Banking, HSBC Credit Cards"
    },
    {
        "file": "barclays-bank-statement-v3.html",
        "bank_name": "Barclays Bank",
        "country": "United Kingdom",
        "currency": "GBP",
        "monthly_price": "£5.75",
        "annual_price": "£4.59",
        "annual_total": "£55",
        "per_page": "£0.05",
        "title": "Barclays Bank Statement Converter | PDF to Excel/QuickBooks | 98% Accuracy",
        "description": "AI-powered Barclays Bank statement converter. Convert PDF to Excel/QuickBooks/Xero in 3 seconds with 98% accuracy. From £4.59/month",
        "h1": "Convert Barclays Bank<br>Statements in Seconds",
        "hero_text": "AI-powered PDF to Excel/QuickBooks converter with 98% accuracy.<br>No manual data entry. No templates. Just fast, accurate results.",
        "features_subtitle": "Built specifically for Barclays Bank statements",
        "account_types": "Barclays Bank Account, Barclays Premier, Barclays Business Banking, Barclaycard Credit Cards"
    },
    {
        "file": "lloyds-bank-statement-v3.html",
        "bank_name": "Lloyds Bank",
        "country": "United Kingdom",
        "currency": "GBP",
        "monthly_price": "£5.75",
        "annual_price": "£4.59",
        "annual_total": "£55",
        "per_page": "£0.05",
        "title": "Lloyds Bank Statement Converter | PDF to Excel/QuickBooks | 98% Accuracy",
        "description": "AI-powered Lloyds Bank statement converter. Convert PDF to Excel/QuickBooks/Xero in 3 seconds with 98% accuracy. From £4.59/month",
        "h1": "Convert Lloyds Bank<br>Statements in Seconds",
        "hero_text": "AI-powered PDF to Excel/QuickBooks converter with 98% accuracy.<br>No manual data entry. No templates. Just fast, accurate results.",
        "features_subtitle": "Built specifically for Lloyds Bank statements",
        "account_types": "Lloyds Classic Account, Lloyds Club, Lloyds Premier, Lloyds Business Banking"
    },
    {
        "file": "natwest-bank-statement-v3.html",
        "bank_name": "NatWest",
        "country": "United Kingdom",
        "currency": "GBP",
        "monthly_price": "£5.75",
        "annual_price": "£4.59",
        "annual_total": "£55",
        "per_page": "£0.05",
        "title": "NatWest Statement Converter | PDF to Excel/QuickBooks | 98% Accuracy",
        "description": "AI-powered NatWest statement converter. Convert PDF to Excel/QuickBooks/Xero in 3 seconds with 98% accuracy. From £4.59/month",
        "h1": "Convert NatWest<br>Statements in Seconds",
        "hero_text": "AI-powered PDF to Excel/QuickBooks converter with 98% accuracy.<br>No manual data entry. No templates. Just fast, accurate results.",
        "features_subtitle": "Built specifically for NatWest statements",
        "account_types": "NatWest Select Account, NatWest Reward, NatWest Premier, NatWest Business Banking"
    },
    {
        "file": "santander-uk-statement-v3.html",
        "bank_name": "Santander UK",
        "country": "United Kingdom",
        "currency": "GBP",
        "monthly_price": "£5.75",
        "annual_price": "£4.59",
        "annual_total": "£55",
        "per_page": "£0.05",
        "title": "Santander UK Statement Converter | PDF to Excel/QuickBooks | 98% Accuracy",
        "description": "AI-powered Santander UK statement converter. Convert PDF to Excel/QuickBooks/Xero in 3 seconds with 98% accuracy. From £4.59/month",
        "h1": "Convert Santander UK<br>Statements in Seconds",
        "hero_text": "AI-powered PDF to Excel/QuickBooks converter with 98% accuracy.<br>No manual data entry. No templates. Just fast, accurate results.",
        "features_subtitle": "Built specifically for Santander UK statements",
        "account_types": "Santander Edge, Santander 123, Santander Select, Santander Business Banking"
    },
    
    # 加拿大银行 (5个) - CAD C$7.59/month
    {
        "file": "rbc-bank-statement-v3.html",
        "bank_name": "RBC Royal Bank",
        "country": "Canada",
        "currency": "CAD",
        "monthly_price": "C$9.50",
        "annual_price": "C$7.59",
        "annual_total": "C$91",
        "per_page": "C$0.08",
        "title": "RBC Royal Bank Statement Converter | PDF to Excel/QuickBooks | 98% Accuracy",
        "description": "AI-powered RBC statement converter. Convert PDF to Excel/QuickBooks/Xero in 3 seconds with 98% accuracy. From C$7.59/month",
        "h1": "Convert RBC Royal Bank<br>Statements in Seconds",
        "hero_text": "AI-powered PDF to Excel/QuickBooks converter with 98% accuracy.<br>No manual data entry. No templates. Just fast, accurate results.",
        "features_subtitle": "Built specifically for RBC Royal Bank statements",
        "account_types": "RBC Day to Day Banking, RBC High Interest eSavings, RBC Business accounts, RBC Credit Cards"
    },
    {
        "file": "td-canada-trust-statement-v3.html",
        "bank_name": "TD Canada Trust",
        "country": "Canada",
        "currency": "CAD",
        "monthly_price": "C$9.50",
        "annual_price": "C$7.59",
        "annual_total": "C$91",
        "per_page": "C$0.08",
        "title": "TD Canada Trust Statement Converter | PDF to Excel/QuickBooks | 98% Accuracy",
        "description": "AI-powered TD Canada Trust statement converter. Convert PDF to Excel/QuickBooks/Xero in 3 seconds with 98% accuracy. From C$7.59/month",
        "h1": "Convert TD Canada Trust<br>Statements in Seconds",
        "hero_text": "AI-powered PDF to Excel/QuickBooks converter with 98% accuracy.<br>No manual data entry. No templates. Just fast, accurate results.",
        "features_subtitle": "Built specifically for TD Canada Trust statements",
        "account_types": "TD Everyday Chequing, TD High Interest Savings, TD Business Banking, TD Credit Cards"
    },
    {
        "file": "scotiabank-statement-v3.html",
        "bank_name": "Scotiabank",
        "country": "Canada",
        "currency": "CAD",
        "monthly_price": "C$9.50",
        "annual_price": "C$7.59",
        "annual_total": "C$91",
        "per_page": "C$0.08",
        "title": "Scotiabank Statement Converter | PDF to Excel/QuickBooks | 98% Accuracy",
        "description": "AI-powered Scotiabank statement converter. Convert PDF to Excel/QuickBooks/Xero in 3 seconds with 98% accuracy. From C$7.59/month",
        "h1": "Convert Scotiabank<br>Statements in Seconds",
        "hero_text": "AI-powered PDF to Excel/QuickBooks converter with 98% accuracy.<br>No manual data entry. No templates. Just fast, accurate results.",
        "features_subtitle": "Built specifically for Scotiabank statements",
        "account_types": "Scotiabank Basic Banking, Preferred Package, Scotia Business accounts, Scotia Credit Cards"
    },
    {
        "file": "bmo-bank-statement-v3.html",
        "bank_name": "BMO Bank of Montreal",
        "country": "Canada",
        "currency": "CAD",
        "monthly_price": "C$9.50",
        "annual_price": "C$7.59",
        "annual_total": "C$91",
        "per_page": "C$0.08",
        "title": "BMO Bank of Montreal Statement Converter | PDF to Excel/QuickBooks | 98% Accuracy",
        "description": "AI-powered BMO statement converter. Convert PDF to Excel/QuickBooks/Xero in 3 seconds with 98% accuracy. From C$7.59/month",
        "h1": "Convert BMO<br>Statements in Seconds",
        "hero_text": "AI-powered PDF to Excel/QuickBooks converter with 98% accuracy.<br>No manual data entry. No templates. Just fast, accurate results.",
        "features_subtitle": "Built specifically for BMO statements",
        "account_types": "BMO Practical Plan, BMO Premium Plan, BMO Business Banking, BMO Credit Cards"
    },
    {
        "file": "cibc-bank-statement-v3.html",
        "bank_name": "CIBC",
        "country": "Canada",
        "currency": "CAD",
        "monthly_price": "C$9.50",
        "annual_price": "C$7.59",
        "annual_total": "C$91",
        "per_page": "C$0.08",
        "title": "CIBC Statement Converter | PDF to Excel/QuickBooks | 98% Accuracy",
        "description": "AI-powered CIBC statement converter. Convert PDF to Excel/QuickBooks/Xero in 3 seconds with 98% accuracy. From C$7.59/month",
        "h1": "Convert CIBC<br>Statements in Seconds",
        "hero_text": "AI-powered PDF to Excel/QuickBooks converter with 98% accuracy.<br>No manual data entry. No templates. Just fast, accurate results.",
        "features_subtitle": "Built specifically for CIBC statements",
        "account_types": "CIBC Smart Account, CIBC Imperial Service, CIBC Business accounts, CIBC Credit Cards"
    },
    
    # 澳洲银行 (4个) - AUD A$8.59/month
    {
        "file": "commbank-statement-v3.html",
        "bank_name": "CommBank Australia",
        "country": "Australia",
        "currency": "AUD",
        "monthly_price": "A$10.75",
        "annual_price": "A$8.59",
        "annual_total": "A$103",
        "per_page": "A$0.09",
        "title": "CommBank Statement Converter | PDF to Excel/QuickBooks | 98% Accuracy",
        "description": "AI-powered CommBank statement converter. Convert PDF to Excel/QuickBooks/Xero in 3 seconds with 98% accuracy. From A$8.59/month",
        "h1": "Convert CommBank<br>Statements in Seconds",
        "hero_text": "AI-powered PDF to Excel/QuickBooks converter with 98% accuracy.<br>No manual data entry. No templates. Just fast, accurate results.",
        "features_subtitle": "Built specifically for CommBank statements",
        "account_types": "CommBank Smart Access, NetBank Saver, CommBank Business accounts, CommBank Credit Cards"
    },
    {
        "file": "westpac-australia-statement-v3.html",
        "bank_name": "Westpac Australia",
        "country": "Australia",
        "currency": "AUD",
        "monthly_price": "A$10.75",
        "annual_price": "A$8.59",
        "annual_total": "A$103",
        "per_page": "A$0.09",
        "title": "Westpac Australia Statement Converter | PDF to Excel/QuickBooks | 98% Accuracy",
        "description": "AI-powered Westpac statement converter. Convert PDF to Excel/QuickBooks/Xero in 3 seconds with 98% accuracy. From A$8.59/month",
        "h1": "Convert Westpac<br>Statements in Seconds",
        "hero_text": "AI-powered PDF to Excel/QuickBooks converter with 98% accuracy.<br>No manual data entry. No templates. Just fast, accurate results.",
        "features_subtitle": "Built specifically for Westpac statements",
        "account_types": "Westpac Choice, Westpac eSaver, Westpac Business accounts, Westpac Credit Cards"
    },
    {
        "file": "anz-australia-statement-v3.html",
        "bank_name": "ANZ Australia",
        "country": "Australia",
        "currency": "AUD",
        "monthly_price": "A$10.75",
        "annual_price": "A$8.59",
        "annual_total": "A$103",
        "per_page": "A$0.09",
        "title": "ANZ Australia Statement Converter | PDF to Excel/QuickBooks | 98% Accuracy",
        "description": "AI-powered ANZ statement converter. Convert PDF to Excel/QuickBooks/Xero in 3 seconds with 98% accuracy. From A$8.59/month",
        "h1": "Convert ANZ<br>Statements in Seconds",
        "hero_text": "AI-powered PDF to Excel/QuickBooks converter with 98% accuracy.<br>No manual data entry. No templates. Just fast, accurate results.",
        "features_subtitle": "Built specifically for ANZ statements",
        "account_types": "ANZ Access Advantage, ANZ Online Saver, ANZ Business accounts, ANZ Credit Cards"
    },
    {
        "file": "nab-statement-v3.html",
        "bank_name": "NAB",
        "country": "Australia",
        "currency": "AUD",
        "monthly_price": "A$10.75",
        "annual_price": "A$8.59",
        "annual_total": "A$103",
        "per_page": "A$0.09",
        "title": "NAB Statement Converter | PDF to Excel/QuickBooks | 98% Accuracy",
        "description": "AI-powered NAB statement converter. Convert PDF to Excel/QuickBooks/Xero in 3 seconds with 98% accuracy. From A$8.59/month",
        "h1": "Convert NAB<br>Statements in Seconds",
        "hero_text": "AI-powered PDF to Excel/QuickBooks converter with 98% accuracy.<br>No manual data entry. No templates. Just fast, accurate results.",
        "features_subtitle": "Built specifically for NAB statements",
        "account_types": "NAB Classic Banking, NAB iSaver, NAB Business accounts, NAB Credit Cards"
    },
    
    # 新西兰银行 (4个) - NZD NZ$9.29/month
    {
        "file": "anz-new-zealand-statement-v3.html",
        "bank_name": "ANZ New Zealand",
        "country": "New Zealand",
        "currency": "NZD",
        "monthly_price": "NZ$11.60",
        "annual_price": "NZ$9.29",
        "annual_total": "NZ$111",
        "per_page": "NZ$0.10",
        "title": "ANZ NZ Statement Converter | PDF to Excel/QuickBooks | 98% Accuracy",
        "description": "AI-powered ANZ NZ statement converter. Convert PDF to Excel/QuickBooks/Xero in 3 seconds with 98% accuracy. From NZ$9.29/month",
        "h1": "Convert ANZ NZ<br>Statements in Seconds",
        "hero_text": "AI-powered PDF to Excel/QuickBooks converter with 98% accuracy.<br>No manual data entry. No templates. Just fast, accurate results.",
        "features_subtitle": "Built specifically for ANZ NZ statements",
        "account_types": "ANZ Access, ANZ Serious Saver, ANZ Business accounts, ANZ Credit Cards"
    },
    {
        "file": "asb-bank-statement-v3.html",
        "bank_name": "ASB Bank",
        "country": "New Zealand",
        "currency": "NZD",
        "monthly_price": "NZ$11.60",
        "annual_price": "NZ$9.29",
        "annual_total": "NZ$111",
        "per_page": "NZ$0.10",
        "title": "ASB Bank Statement Converter | PDF to Excel/QuickBooks | 98% Accuracy",
        "description": "AI-powered ASB Bank statement converter. Convert PDF to Excel/QuickBooks/Xero in 3 seconds with 98% accuracy. From NZ$9.29/month",
        "h1": "Convert ASB Bank<br>Statements in Seconds",
        "hero_text": "AI-powered PDF to Excel/QuickBooks converter with 98% accuracy.<br>No manual data entry. No templates. Just fast, accurate results.",
        "features_subtitle": "Built specifically for ASB Bank statements",
        "account_types": "ASB Everyday, ASB Savings Plus, ASB Business accounts, ASB Credit Cards"
    },
    {
        "file": "westpac-new-zealand-statement-v3.html",
        "bank_name": "Westpac New Zealand",
        "country": "New Zealand",
        "currency": "NZD",
        "monthly_price": "NZ$11.60",
        "annual_price": "NZ$9.29",
        "annual_total": "NZ$111",
        "per_page": "NZ$0.10",
        "title": "Westpac NZ Statement Converter | PDF to Excel/QuickBooks | 98% Accuracy",
        "description": "AI-powered Westpac NZ statement converter. Convert PDF to Excel/QuickBooks/Xero in 3 seconds with 98% accuracy. From NZ$9.29/month",
        "h1": "Convert Westpac NZ<br>Statements in Seconds",
        "hero_text": "AI-powered PDF to Excel/QuickBooks converter with 98% accuracy.<br>No manual data entry. No templates. Just fast, accurate results.",
        "features_subtitle": "Built specifically for Westpac NZ statements",
        "account_types": "Westpac Choice, Westpac eSaver, Westpac Business accounts, Westpac Credit Cards"
    },
    {
        "file": "bnz-statement-v3.html",
        "bank_name": "BNZ",
        "country": "New Zealand",
        "currency": "NZD",
        "monthly_price": "NZ$11.60",
        "annual_price": "NZ$9.29",
        "annual_total": "NZ$111",
        "per_page": "NZ$0.10",
        "title": "BNZ Statement Converter | PDF to Excel/QuickBooks | 98% Accuracy",
        "description": "AI-powered BNZ statement converter. Convert PDF to Excel/QuickBooks/Xero in 3 seconds with 98% accuracy. From NZ$9.29/month",
        "h1": "Convert BNZ<br>Statements in Seconds",
        "hero_text": "AI-powered PDF to Excel/QuickBooks converter with 98% accuracy.<br>No manual data entry. No templates. Just fast, accurate results.",
        "features_subtitle": "Built specifically for BNZ statements",
        "account_types": "BNZ Rapid Save, BNZ Savings, BNZ Business accounts, BNZ Credit Cards"
    },
    
    # 新加坡银行 (3个) - SGD S$7.59/month
    {
        "file": "dbs-bank-statement-v3.html",
        "bank_name": "DBS Bank",
        "country": "Singapore",
        "currency": "SGD",
        "monthly_price": "S$9.50",
        "annual_price": "S$7.59",
        "annual_total": "S$91",
        "per_page": "S$0.08",
        "title": "DBS Bank Statement Converter | PDF to Excel/QuickBooks | 98% Accuracy",
        "description": "AI-powered DBS Bank statement converter. Convert PDF to Excel/QuickBooks/Xero in 3 seconds with 98% accuracy. From S$7.59/month",
        "h1": "Convert DBS Bank<br>Statements in Seconds",
        "hero_text": "AI-powered PDF to Excel/QuickBooks converter with 98% accuracy.<br>No manual data entry. No templates. Just fast, accurate results.",
        "features_subtitle": "Built specifically for DBS Bank statements",
        "account_types": "DBS Multiplier, DBS eSavings, DBS Business accounts, DBS Credit Cards"
    },
    {
        "file": "ocbc-bank-statement-v3.html",
        "bank_name": "OCBC Bank",
        "country": "Singapore",
        "currency": "SGD",
        "monthly_price": "S$9.50",
        "annual_price": "S$7.59",
        "annual_total": "S$91",
        "per_page": "S$0.08",
        "title": "OCBC Bank Statement Converter | PDF to Excel/QuickBooks | 98% Accuracy",
        "description": "AI-powered OCBC Bank statement converter. Convert PDF to Excel/QuickBooks/Xero in 3 seconds with 98% accuracy. From S$7.59/month",
        "h1": "Convert OCBC Bank<br>Statements in Seconds",
        "hero_text": "AI-powered PDF to Excel/QuickBooks converter with 98% accuracy.<br>No manual data entry. No templates. Just fast, accurate results.",
        "features_subtitle": "Built specifically for OCBC Bank statements",
        "account_types": "OCBC 360 Account, OCBC Savings, OCBC Business accounts, OCBC Credit Cards"
    },
    {
        "file": "uob-statement-v3.html",
        "bank_name": "UOB",
        "country": "Singapore",
        "currency": "SGD",
        "monthly_price": "S$9.50",
        "annual_price": "S$7.59",
        "annual_total": "S$91",
        "per_page": "S$0.08",
        "title": "UOB Statement Converter | PDF to Excel/QuickBooks | 98% Accuracy",
        "description": "AI-powered UOB statement converter. Convert PDF to Excel/QuickBooks/Xero in 3 seconds with 98% accuracy. From S$7.59/month",
        "h1": "Convert UOB<br>Statements in Seconds",
        "hero_text": "AI-powered PDF to Excel/QuickBooks converter with 98% accuracy.<br>No manual data entry. No templates. Just fast, accurate results.",
        "features_subtitle": "Built specifically for UOB statements",
        "account_types": "UOB One Account, UOB Stash Account, UOB Business accounts, UOB Credit Cards"
    },
    
    # 日本银行 (3个) - JPY ¥926/month
    {
        "file": "mufg-bank-statement-v3.html",
        "bank_name": "Mitsubishi UFJ (MUFG)",
        "country": "Japan",
        "currency": "JPY",
        "monthly_price": "¥1,158",
        "annual_price": "¥926",
        "annual_total": "¥11,116",
        "per_page": "¥10",
        "title": "MUFG Bank Statement Converter | PDF to Excel/QuickBooks | 98% Accuracy",
        "description": "AI-powered MUFG Bank statement converter. Convert PDF to Excel/QuickBooks/Xero in 3 seconds with 98% accuracy. From ¥926/month",
        "h1": "Convert MUFG Bank<br>Statements in Seconds",
        "hero_text": "AI-powered PDF to Excel/QuickBooks converter with 98% accuracy.<br>No manual data entry. No templates. Just fast, accurate results.",
        "features_subtitle": "Built specifically for MUFG Bank statements",
        "account_types": "MUFG Ordinary Deposit, MUFG Savings, MUFG Business accounts, MUFG Credit Cards"
    },
    {
        "file": "smbc-bank-statement-v3.html",
        "bank_name": "Sumitomo Mitsui (SMBC)",
        "country": "Japan",
        "currency": "JPY",
        "monthly_price": "¥1,158",
        "annual_price": "¥926",
        "annual_total": "¥11,116",
        "per_page": "¥10",
        "title": "SMBC Statement Converter | PDF to Excel/QuickBooks | 98% Accuracy",
        "description": "AI-powered SMBC statement converter. Convert PDF to Excel/QuickBooks/Xero in 3 seconds with 98% accuracy. From ¥926/month",
        "h1": "Convert SMBC<br>Statements in Seconds",
        "hero_text": "AI-powered PDF to Excel/QuickBooks converter with 98% accuracy.<br>No manual data entry. No templates. Just fast, accurate results.",
        "features_subtitle": "Built specifically for SMBC statements",
        "account_types": "SMBC Ordinary Deposit, SMBC Time Deposit, SMBC Business accounts, SMBC Credit Cards"
    },
    {
        "file": "mizuho-bank-statement-v3.html",
        "bank_name": "Mizuho Bank",
        "country": "Japan",
        "currency": "JPY",
        "monthly_price": "¥1,158",
        "annual_price": "¥926",
        "annual_total": "¥11,116",
        "per_page": "¥10",
        "title": "Mizuho Bank Statement Converter | PDF to Excel/QuickBooks | 98% Accuracy",
        "description": "AI-powered Mizuho Bank statement converter. Convert PDF to Excel/QuickBooks/Xero in 3 seconds with 98% accuracy. From ¥926/month",
        "h1": "Convert Mizuho Bank<br>Statements in Seconds",
        "hero_text": "AI-powered PDF to Excel/QuickBooks converter with 98% accuracy.<br>No manual data entry. No templates. Just fast, accurate results.",
        "features_subtitle": "Built specifically for Mizuho Bank statements",
        "account_types": "Mizuho Ordinary Deposit, Mizuho Savings, Mizuho Business accounts, Mizuho Credit Cards"
    },
    
    # 韩国银行 (4个) - KRW ₩7998/month
    {
        "file": "kb-kookmin-bank-statement-v3.html",
        "bank_name": "KB Kookmin Bank",
        "country": "South Korea",
        "currency": "KRW",
        "monthly_price": "₩9,998",
        "annual_price": "₩7,998",
        "annual_total": "₩95,976",
        "per_page": "₩80",
        "title": "KB Kookmin Bank Statement Converter | PDF to Excel/QuickBooks | 98% Accuracy",
        "description": "AI-powered KB Kookmin Bank statement converter. Convert PDF to Excel/QuickBooks/Xero in 3 seconds with 98% accuracy. From ₩7,998/month",
        "h1": "Convert KB Kookmin Bank<br>Statements in Seconds",
        "hero_text": "AI-powered PDF to Excel/QuickBooks converter with 98% accuracy.<br>No manual data entry. No templates. Just fast, accurate results.",
        "features_subtitle": "Built specifically for KB Kookmin Bank statements",
        "account_types": "KB Star Banking, KB My Savings, KB Business accounts, KB Credit Cards"
    },
    {
        "file": "shinhan-bank-statement-v3.html",
        "bank_name": "Shinhan Bank",
        "country": "South Korea",
        "currency": "KRW",
        "monthly_price": "₩9,998",
        "annual_price": "₩7,998",
        "annual_total": "₩95,976",
        "per_page": "₩80",
        "title": "Shinhan Bank Statement Converter | PDF to Excel/QuickBooks | 98% Accuracy",
        "description": "AI-powered Shinhan Bank statement converter. Convert PDF to Excel/QuickBooks/Xero in 3 seconds with 98% accuracy. From ₩7,998/month",
        "h1": "Convert Shinhan Bank<br>Statements in Seconds",
        "hero_text": "AI-powered PDF to Excel/QuickBooks converter with 98% accuracy.<br>No manual data entry. No templates. Just fast, accurate results.",
        "features_subtitle": "Built specifically for Shinhan Bank statements",
        "account_types": "Shinhan Sol Banking, Shinhan Savings, Shinhan Business accounts, Shinhan Credit Cards"
    },
    {
        "file": "hana-bank-statement-v3.html",
        "bank_name": "Hana Bank",
        "country": "South Korea",
        "currency": "KRW",
        "monthly_price": "₩9,998",
        "annual_price": "₩7,998",
        "annual_total": "₩95,976",
        "per_page": "₩80",
        "title": "Hana Bank Statement Converter | PDF to Excel/QuickBooks | 98% Accuracy",
        "description": "AI-powered Hana Bank statement converter. Convert PDF to Excel/QuickBooks/Xero in 3 seconds with 98% accuracy. From ₩7,998/month",
        "h1": "Convert Hana Bank<br>Statements in Seconds",
        "hero_text": "AI-powered PDF to Excel/QuickBooks converter with 98% accuracy.<br>No manual data entry. No templates. Just fast, accurate results.",
        "features_subtitle": "Built specifically for Hana Bank statements",
        "account_types": "Hana 1Q Banking, Hana Savings, Hana Business accounts, Hana Credit Cards"
    },
    {
        "file": "woori-bank-statement-v3.html",
        "bank_name": "Woori Bank",
        "country": "South Korea",
        "currency": "KRW",
        "monthly_price": "₩9,998",
        "annual_price": "₩7,998",
        "annual_total": "₩95,976",
        "per_page": "₩80",
        "title": "Woori Bank Statement Converter | PDF to Excel/QuickBooks | 98% Accuracy",
        "description": "AI-powered Woori Bank statement converter. Convert PDF to Excel/QuickBooks/Xero in 3 seconds with 98% accuracy. From ₩7,998/month",
        "h1": "Convert Woori Bank<br>Statements in Seconds",
        "hero_text": "AI-powered PDF to Excel/QuickBooks converter with 98% accuracy.<br>No manual data entry. No templates. Just fast, accurate results.",
        "features_subtitle": "Built specifically for Woori Bank statements",
        "account_types": "Woori WON Banking, Woori Savings Plus, Woori Business accounts, Woori Credit Cards"
    },
    
    # 台湾银行 (3个) - TWD NT$188/month
    {
        "file": "bank-of-taiwan-statement-v3.html",
        "bank_name": "Bank of Taiwan",
        "country": "Taiwan",
        "currency": "TWD",
        "monthly_price": "NT$235",
        "annual_price": "NT$188",
        "annual_total": "NT$2,256",
        "per_page": "NT$2",
        "title": "Bank of Taiwan Statement Converter | PDF to Excel/QuickBooks | 98% Accuracy",
        "description": "AI-powered Bank of Taiwan statement converter. Convert PDF to Excel/QuickBooks/Xero in 3 seconds with 98% accuracy. From NT$188/month",
        "h1": "Convert Bank of Taiwan<br>Statements in Seconds",
        "hero_text": "AI-powered PDF to Excel/QuickBooks converter with 98% accuracy.<br>No manual data entry. No templates. Just fast, accurate results.",
        "features_subtitle": "Built specifically for Bank of Taiwan statements",
        "account_types": "BOT Checking Account, BOT Savings, BOT Business accounts, BOT Credit Cards"
    },
    {
        "file": "ctbc-bank-statement-v3.html",
        "bank_name": "CTBC Bank",
        "country": "Taiwan",
        "currency": "TWD",
        "monthly_price": "NT$235",
        "annual_price": "NT$188",
        "annual_total": "NT$2,256",
        "per_page": "NT$2",
        "title": "CTBC Bank Statement Converter | PDF to Excel/QuickBooks | 98% Accuracy",
        "description": "AI-powered CTBC Bank statement converter. Convert PDF to Excel/QuickBooks/Xero in 3 seconds with 98% accuracy. From NT$188/month",
        "h1": "Convert CTBC Bank<br>Statements in Seconds",
        "hero_text": "AI-powered PDF to Excel/QuickBooks converter with 98% accuracy.<br>No manual data entry. No templates. Just fast, accurate results.",
        "features_subtitle": "Built specifically for CTBC Bank statements",
        "account_types": "CTBC Digital Account, CTBC Savings Plus, CTBC Business accounts, CTBC Credit Cards"
    },
    {
        "file": "cathay-bank-statement-v3.html",
        "bank_name": "Cathay Bank",
        "country": "Taiwan",
        "currency": "TWD",
        "monthly_price": "NT$235",
        "annual_price": "NT$188",
        "annual_total": "NT$2,256",
        "per_page": "NT$2",
        "title": "Cathay Bank Statement Converter | PDF to Excel/QuickBooks | 98% Accuracy",
        "description": "AI-powered Cathay Bank statement converter. Convert PDF to Excel/QuickBooks/Xero in 3 seconds with 98% accuracy. From NT$188/month",
        "h1": "Convert Cathay Bank<br>Statements in Seconds",
        "hero_text": "AI-powered PDF to Excel/QuickBooks converter with 98% accuracy.<br>No manual data entry. No templates. Just fast, accurate results.",
        "features_subtitle": "Built specifically for Cathay Bank statements",
        "account_types": "Cathay KOKO Account, Cathay Savings, Cathay Business accounts, Cathay Credit Cards"
    },
    
    # 香港银行 (3个) - HKD HK$46/month
    {
        "file": "hsbc-hong-kong-statement-v3.html",
        "bank_name": "HSBC Hong Kong",
        "country": "Hong Kong",
        "currency": "HKD",
        "monthly_price": "HK$58",
        "annual_price": "HK$46",
        "annual_total": "HK$552",
        "per_page": "HK$0.5",
        "title": "HSBC Hong Kong Statement Converter | PDF to Excel/QuickBooks | 98% Accuracy",
        "description": "AI-powered HSBC Hong Kong statement converter. Convert PDF to Excel/QuickBooks/Xero in 3 seconds with 98% accuracy. From HK$46/month",
        "h1": "Convert HSBC Hong Kong<br>Statements in Seconds",
        "hero_text": "AI-powered PDF to Excel/QuickBooks converter with 98% accuracy.<br>No manual data entry. No templates. Just fast, accurate results.",
        "features_subtitle": "Built specifically for HSBC Hong Kong statements",
        "account_types": "HSBC Personal Integrated Account, HSBC Premier, HSBC Business Banking, HSBC Credit Cards"
    },
    {
        "file": "hang-seng-bank-statement-v3.html",
        "bank_name": "Hang Seng Bank",
        "country": "Hong Kong",
        "currency": "HKD",
        "monthly_price": "HK$58",
        "annual_price": "HK$46",
        "annual_total": "HK$552",
        "per_page": "HK$0.5",
        "title": "Hang Seng Bank Statement Converter | PDF to Excel/QuickBooks | 98% Accuracy",
        "description": "AI-powered Hang Seng Bank statement converter. Convert PDF to Excel/QuickBooks/Xero in 3 seconds with 98% accuracy. From HK$46/month",
        "h1": "Convert Hang Seng Bank<br>Statements in Seconds",
        "hero_text": "AI-powered PDF to Excel/QuickBooks converter with 98% accuracy.<br>No manual data entry. No templates. Just fast, accurate results.",
        "features_subtitle": "Built specifically for Hang Seng Bank statements",
        "account_types": "Hang Seng Integrated Account, Hang Seng Prestige Banking, Hang Seng Business accounts, Hang Seng Credit Cards"
    },
    {
        "file": "boc-hong-kong-statement-v3.html",
        "bank_name": "BOC Hong Kong",
        "country": "Hong Kong",
        "currency": "HKD",
        "monthly_price": "HK$58",
        "annual_price": "HK$46",
        "annual_total": "HK$552",
        "per_page": "HK$0.5",
        "title": "BOC Hong Kong Statement Converter | PDF to Excel/QuickBooks | 98% Accuracy",
        "description": "AI-powered BOC Hong Kong statement converter. Convert PDF to Excel/QuickBooks/Xero in 3 seconds with 98% accuracy. From HK$46/month",
        "h1": "Convert BOC Hong Kong<br>Statements in Seconds",
        "hero_text": "AI-powered PDF to Excel/QuickBooks converter with 98% accuracy.<br>No manual data entry. No templates. Just fast, accurate results.",
        "features_subtitle": "Built specifically for BOC Hong Kong statements",
        "account_types": "BOC Integrated Account, BOC i-Banking, BOC Business accounts, BOC Credit Cards"
    },
    
    # 欧洲银行 (6个) - EUR €5.29/month
    {
        "file": "deutsche-bank-statement-v3.html",
        "bank_name": "Deutsche Bank",
        "country": "Germany",
        "currency": "EUR",
        "monthly_price": "€6.60",
        "annual_price": "€5.29",
        "annual_total": "€63",
        "per_page": "€0.06",
        "title": "Deutsche Bank Statement Converter | PDF to Excel/QuickBooks | 98% Accuracy",
        "description": "AI-powered Deutsche Bank statement converter. Convert PDF to Excel/QuickBooks/Xero in 3 seconds with 98% accuracy. From €5.29/month",
        "h1": "Convert Deutsche Bank<br>Statements in Seconds",
        "hero_text": "AI-powered PDF to Excel/QuickBooks converter with 98% accuracy.<br>No manual data entry. No templates. Just fast, accurate results.",
        "features_subtitle": "Built specifically for Deutsche Bank statements",
        "account_types": "Deutsche Bank Girokonto, Savings accounts, Business Banking, Deutsche Bank Credit Cards"
    },
    {
        "file": "ing-bank-statement-v3.html",
        "bank_name": "ING Bank",
        "country": "Netherlands",
        "currency": "EUR",
        "monthly_price": "€6.60",
        "annual_price": "€5.29",
        "annual_total": "€63",
        "per_page": "€0.06",
        "title": "ING Bank Statement Converter | PDF to Excel/QuickBooks | 98% Accuracy",
        "description": "AI-powered ING Bank statement converter. Convert PDF to Excel/QuickBooks/Xero in 3 seconds with 98% accuracy. From €5.29/month",
        "h1": "Convert ING Bank<br>Statements in Seconds",
        "hero_text": "AI-powered PDF to Excel/QuickBooks converter with 98% accuracy.<br>No manual data entry. No templates. Just fast, accurate results.",
        "features_subtitle": "Built specifically for ING Bank statements",
        "account_types": "ING Betaalrekening, ING Sparen, ING Business accounts, ING Credit Cards"
    },
    {
        "file": "commerzbank-statement-v3.html",
        "bank_name": "Commerzbank",
        "country": "Germany",
        "currency": "EUR",
        "monthly_price": "€6.60",
        "annual_price": "€5.29",
        "annual_total": "€63",
        "per_page": "€0.06",
        "title": "Commerzbank Statement Converter | PDF to Excel/QuickBooks | 98% Accuracy",
        "description": "AI-powered Commerzbank statement converter. Convert PDF to Excel/QuickBooks/Xero in 3 seconds with 98% accuracy. From €5.29/month",
        "h1": "Convert Commerzbank<br>Statements in Seconds",
        "hero_text": "AI-powered PDF to Excel/QuickBooks converter with 98% accuracy.<br>No manual data entry. No templates. Just fast, accurate results.",
        "features_subtitle": "Built specifically for Commerzbank statements",
        "account_types": "Commerzbank Girokonto, Savings accounts, Business Banking, Commerzbank Credit Cards"
    },
    {
        "file": "rabobank-statement-v3.html",
        "bank_name": "Rabobank",
        "country": "Netherlands",
        "currency": "EUR",
        "monthly_price": "€6.60",
        "annual_price": "€5.29",
        "annual_total": "€63",
        "per_page": "€0.06",
        "title": "Rabobank Statement Converter | PDF to Excel/QuickBooks | 98% Accuracy",
        "description": "AI-powered Rabobank statement converter. Convert PDF to Excel/QuickBooks/Xero in 3 seconds with 98% accuracy. From €5.29/month",
        "h1": "Convert Rabobank<br>Statements in Seconds",
        "hero_text": "AI-powered PDF to Excel/QuickBooks converter with 98% accuracy.<br>No manual data entry. No templates. Just fast, accurate results.",
        "features_subtitle": "Built specifically for Rabobank statements",
        "account_types": "Rabobank Betaalrekening, Rabobank Sparen, Rabobank Business accounts, Rabobank Credit Cards"
    },
    {
        "file": "abn-amro-statement-v3.html",
        "bank_name": "ABN AMRO",
        "country": "Netherlands",
        "currency": "EUR",
        "monthly_price": "€6.60",
        "annual_price": "€5.29",
        "annual_total": "€63",
        "per_page": "€0.06",
        "title": "ABN AMRO Statement Converter | PDF to Excel/QuickBooks | 98% Accuracy",
        "description": "AI-powered ABN AMRO statement converter. Convert PDF to Excel/QuickBooks/Xero in 3 seconds with 98% accuracy. From €5.29/month",
        "h1": "Convert ABN AMRO<br>Statements in Seconds",
        "hero_text": "AI-powered PDF to Excel/QuickBooks converter with 98% accuracy.<br>No manual data entry. No templates. Just fast, accurate results.",
        "features_subtitle": "Built specifically for ABN AMRO statements",
        "account_types": "ABN AMRO Basis Pakket, ABN AMRO Sparen, ABN AMRO Business accounts, ABN AMRO Credit Cards"
    },
    {
        "file": "dz-bank-statement-v3.html",
        "bank_name": "DZ Bank",
        "country": "Germany",
        "currency": "EUR",
        "monthly_price": "€6.60",
        "annual_price": "€5.29",
        "annual_total": "€63",
        "per_page": "€0.06",
        "title": "DZ Bank Statement Converter | PDF to Excel/QuickBooks | 98% Accuracy",
        "description": "AI-powered DZ Bank statement converter. Convert PDF to Excel/QuickBooks/Xero in 3 seconds with 98% accuracy. From €5.29/month",
        "h1": "Convert DZ Bank<br>Statements in Seconds",
        "hero_text": "AI-powered PDF to Excel/QuickBooks converter with 98% accuracy.<br>No manual data entry. No templates. Just fast, accurate results.",
        "features_subtitle": "Built specifically for DZ Bank statements",
        "account_types": "DZ Bank Girokonto, Savings accounts, Business Banking, DZ Bank Credit Cards"
    },
]

# 读取模板文件
def read_template():
    with open('chase-bank-statement-v3-redesign.html', 'r', encoding='utf-8') as f:
        return f.read()

# 生成单个银行页面
def generate_bank_page(template, bank):
    content = template
    
    # 替换基本信息
    content = content.replace('Chase Bank USA Statement Converter | PDF to Excel/QuickBooks | 98% Accuracy', bank['title'])
    content = content.replace('AI-powered Chase Bank USA statement converter. Convert PDF to Excel/QuickBooks/Xero in 3 seconds with 98% accuracy. From $5.59/month | 500+ businesses trust us', bank['description'])
    
    # 替换Hero区
    content = content.replace('Convert Chase Bank<br>\n                Statements in Seconds', bank['h1'])
    content = content.replace('AI-powered PDF to Excel/QuickBooks converter with 98% accuracy.<br>\n                No manual data entry. No templates. Just fast, accurate results.', bank['hero_text'])
    
    # 替换定价
    content = content.replace('$5.59', bank['annual_price'])
    content = content.replace('$7', bank['monthly_price'])
    content = content.replace('$67', bank['annual_total']) if 'annual_total' in bank else content
    content = content.replace('$0.06', bank['per_page'])
    
    # 替换银行名称
    content = re.sub(r'Chase Bank(?!\'s)', bank['bank_name'], content)
    content = re.sub(r'Chase(?! )', bank['bank_name'], content)
    
    # 替换Features标题
    content = content.replace('Built specifically for Chase Bank statements', bank['features_subtitle'])
    
    # 替换账户类型
    if 'account_types' in bank:
        content = re.sub(
            r'Chase Total Checking.*?Chase First Banking',
            bank['account_types'],
            content,
            flags=re.DOTALL
        )
    
    # 替换FAQ中的银行名称
    content = content.replace('Chase Bank statements', f"{bank['bank_name']} statements")
    content = content.replace('Chase Bank account', f"{bank['bank_name']} account")
    content = content.replace('Chase statements', f"{bank['bank_name']} statements")
    content = content.replace('your Chase', f"your {bank['bank_name']}")
    content = content.replace('Chase PDF', f"{bank['bank_name']} PDF")
    
    return content

# 批量生成所有页面
def batch_generate():
    print("🚀 开始批量转换50个v3页面...")
    print("=" * 60)
    
    template = read_template()
    success_count = 0
    
    for i, bank in enumerate(BANKS, 1):
        try:
            content = generate_bank_page(template, bank)
            
            # 保存文件
            with open(bank['file'], 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ {i}/50 - {bank['bank_name']} ({bank['country']}) - {bank['file']}")
            success_count += 1
            
        except Exception as e:
            print(f"❌ {i}/50 - {bank['bank_name']} - 错误: {str(e)}")
    
    print("=" * 60)
    print(f"\n🎉 转换完成！")
    print(f"✅ 成功: {success_count}/50")
    print(f"❌ 失败: {50 - success_count}/50")

if __name__ == '__main__':
    batch_generate()

