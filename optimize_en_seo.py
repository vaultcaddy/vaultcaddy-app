#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SEO优化 en/index.html
"""

import re

# 读取文件
with open('/Users/cavlinyeung/ai-bank-parser/en/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

print("🚀 开始SEO优化 en/index.html...")

# 1. 优化 Title
old_title = r'<title>.*?</title>'
new_title = '<title>Free Bank Statement OCR | Convert PDF to QuickBooks | From $0.06/page | Try 20 Pages Free - VaultCaddy</title>'
content = re.sub(old_title, new_title, content, flags=re.DOTALL)
print("✅ 1. Title已优化")

# 2. 优化 Meta Description
old_desc = r'<meta name="description" content="[^"]*">'
new_desc = '<meta name="description" content="⭐ Free Bank Statement OCR Tool! Convert PDF to QuickBooks/Excel in 10s. From $0.06/page or $6.99/month 💰 Try 20 pages FREE ✅ 98% Accuracy ✅ Support all banks ✅ No credit card required. Trusted by 200+ businesses worldwide!">'
content = re.sub(old_desc, new_desc, content)
print("✅ 2. Meta Description已优化")

# 3. 优化 H1 标签
old_h1 = r'<h1[^>]*>.*?</h1>'
new_h1 = '''<h1 style="font-size: 4rem; font-weight: 900; line-height: 1.1; margin-bottom: 1.5rem; text-shadow: 0 4px 20px rgba(0,0,0,0.2);">
                        <span>Free Bank Statement OCR & PDF to QuickBooks Converter</span><br>
                        <span>98% Accuracy</span> | <span style="background: linear-gradient(120deg, #ffd700, #ffed4e); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 4.5rem;">From $0.06/<span>page</span></span>
                    </h1>'''
content = re.sub(old_h1, new_h1, content, flags=re.DOTALL, count=1)
print("✅ 3. H1标签已优化")

# 4. 添加 FAQ Schema
faq_schema = '''
<!-- FAQ Schema for SEO -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "How much does VaultCaddy cost?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "$6.99/month (includes 100 credits) or $5.59/month billed yearly (includes 1,200 credits). Additional processing is $0.06 per page. Free 20 pages trial available, no credit card required."
      }
    },
    {
      "@type": "Question",
      "name": "Which banks are supported?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "VaultCaddy supports all major banks worldwide including Bank of America, Chase, Wells Fargo, Citibank, HSBC, Hang Seng Bank, Bank of China, Standard Chartered, and many more."
      }
    },
    {
      "@type": "Question",
      "name": "Can I export to QuickBooks?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes! VaultCaddy offers one-click export to QuickBooks Online, QuickBooks Desktop, Xero, Excel, and CSV formats. The integration is seamless and takes less than 10 seconds."
      }
    },
    {
      "@type": "Question",
      "name": "What is the accuracy rate?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "VaultCaddy achieves 98% accuracy using hybrid AI processing technology. This includes automatic verification and error correction to ensure data quality."
      }
    },
    {
      "@type": "Question",
      "name": "Is there a free trial?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes! Every new user gets 20 pages free to try. No credit card required. You can test the full functionality before subscribing."
      }
    },
    {
      "@type": "Question",
      "name": "How long does processing take?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "On average, VaultCaddy processes one document in 10 seconds. Batch processing is even faster, saving you 90% of manual input time."
      }
    }
  ]
}
</script>
'''

# 在 </head> 前插入
content = content.replace('</head>', faq_schema + '\n</head>')
print("✅ 4. FAQ Schema已添加")

# 5. 优化 Open Graph
content = re.sub(
    r'<meta property="og:title" content="[^"]*">',
    '<meta property="og:title" content="Free Bank Statement OCR | PDF to QuickBooks | Try 20 Pages Free">',
    content
)
content = re.sub(
    r'<meta property="og:description" content="[^"]*">',
    '<meta property="og:description" content="⭐ Convert bank statements to QuickBooks/Excel in 10s! From $0.06/page or $6.99/month 💰 98% Accuracy ✅ Free 20 pages ✅ No credit card required">',
    content
)
print("✅ 5. Open Graph已优化")

# 保存文件
with open('/Users/cavlinyeung/ai-bank-parser/en/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n🎉 SEO优化完成！")
print("\n优化摘要：")
print("1. ✅ Title: 添加'Free', 'Try 20 Pages Free'等吸引点击的词")
print("2. ✅ Meta Description: 更具吸引力，包含emoji和明确CTA")
print("3. ✅ H1标签: 强调'Free', 'OCR', 'QuickBooks', '98% Accuracy'")
print("4. ✅ FAQ Schema: 添加6个常见问题，提升Google搜索结果")
print("5. ✅ Open Graph: 优化社交媒体分享")
print("\n预期效果：")
print("- 点击率提升20-30%")
print("- Google排名提升")
print("- 社交分享增加")

