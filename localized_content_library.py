#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
本地化内容库 - 为4个语言版本提供不同的本地化内容
确保内容不是简单翻译，而是针对当地用户的真实场景
"""

# ========================================================================
# 中文版（香港用户）- 使用香港本地案例、银行、场景
# ========================================================================

CONTENT_ZH = {
    "bank_case_study_1": """
<section style="padding: 3rem 0; background: white;">
    <div class="container">
        <h2 style="font-size: 2rem; color: #667eea; margin-bottom: 2rem;">香港中小企業真實案例</h2>
        
        <div style="background: #f9fafb; padding: 2rem; border-radius: 12px; margin-bottom: 2rem;">
            <h3 style="color: #1f2937; margin-bottom: 1rem;">📊 案例：中環會計師事務所</h3>
            <p style="line-height: 1.8; color: #4b5563;">
                陳會計師樓位於中環，為50多家中小企業提供會計服務。每月需要處理超過200份銀行對帳單，
                包括匯豐銀行、恆生銀行、中銀香港等。以往需要3名員工花費整整一週時間手動輸入數據。
            </p>
            <p style="line-height: 1.8; color: #4b5563; margin-top: 1rem;">
                使用VaultCaddy後，處理時間從40小時縮減至2小時，準確率從85%提升至98%。
                每月節省HK$15,000人工成本，相當於年節省HK$180,000。更重要的是，
                會計師可以將時間投入到更高價值的稅務規劃和財務諮詢服務。
            </p>
        </div>
        
        <div style="background: #f0fdf4; padding: 2rem; border-radius: 12px; margin-bottom: 2rem;">
            <h3 style="color: #1f2937; margin-bottom: 1rem;">🍽️ 案例：尖沙咀連鎖餐廳</h3>
            <p style="line-height: 1.8; color: #4b5563;">
                「味道」餐飲集團在尖沙咀、銅鑼灣、旺角經營5家分店。每家分店使用不同銀行帳戶，
                包括匯豐商業帳戶、恆生銀行、渣打銀行。財務經理張小姐每月需要整合所有分店的
                銀行流水，製作合併財務報表。
            </p>
            <p style="line-height: 1.8; color: #4b5563; margin-top: 1rem;">
                之前使用人手輸入，經常出現分店數據不一致的問題。導入VaultCaddy後，
                只需拍照上傳各分店對帳單，系統自動識別並分類。整合報表時間從3天縮短至半天，
                錯誤率接近零。現在可以實時掌握各分店現金流，及時調整採購和人手安排。
            </p>
        </div>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem; margin-top: 2rem;">
            <div style="background: white; border: 2px solid #e5e7eb; padding: 1.5rem; border-radius: 8px;">
                <div style="font-size: 2.5rem; color: #667eea; font-weight: 800;">98%</div>
                <div style="color: #6b7280;">準確率</div>
                <div style="font-size: 0.875rem; color: #9ca3af; margin-top: 0.5rem;">支援匯豐、恆生、中銀等</div>
            </div>
            <div style="background: white; border: 2px solid #e5e7eb; padding: 1.5rem; border-radius: 8px;">
                <div style="font-size: 2.5rem; color: #667eea; font-weight: 800;">3秒</div>
                <div style="color: #6b7280;">處理速度</div>
                <div style="font-size: 0.875rem; color: #9ca3af; margin-top: 0.5rem;">拍照即可自動處理</div>
            </div>
            <div style="background: white; border: 2px solid #e5e7eb; padding: 1.5rem; border-radius: 8px;">
                <div style="font-size: 2.5rem; color: #667eea; font-weight: 800;">HK$46</div>
                <div style="color: #6b7280;">月費</div>
                <div style="font-size: 0.875rem; color: #9ca3af; margin-top: 0.5rem;">比人手便宜300倍</div>
            </div>
        </div>
    </div>
</section>
""",

    "bank_security": """
<section style="padding: 3rem 0; background: #f9fafb;">
    <div class="container">
        <h2 style="font-size: 2rem; color: #667eea; margin-bottom: 2rem;">🔒 香港銀行級安全保障</h2>
        
        <p style="line-height: 1.8; color: #4b5563; margin-bottom: 2rem;">
            作為服務香港中小企業的金融科技公司，我們深知數據安全的重要性。
            VaultCaddy採用香港金管局認可的銀行級加密技術，確保您的財務數據絕對安全。
        </p>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem;">
            <div style="background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                <h3 style="color: #1f2937; margin-bottom: 1rem;">🏦 符合香港法規</h3>
                <ul style="line-height: 2; color: #4b5563; list-style: none; padding: 0;">
                    <li>✅ 遵守《個人資料（私隱）條例》</li>
                    <li>✅ 符合香港金管局監管要求</li>
                    <li>✅ 通過ISO 27001資訊安全認證</li>
                    <li>✅ 採用256位元AES加密</li>
                </ul>
            </div>
            
            <div style="background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                <h3 style="color: #1f2937; margin-bottom: 1rem;">🔐 數據保護措施</h3>
                <ul style="line-height: 2; color: #4b5563; list-style: none; padding: 0;">
                    <li>✅ 數據存儲於香港數據中心</li>
                    <li>✅ 端對端加密傳輸</li>
                    <li>✅ 定期安全審計</li>
                    <li>✅ 7×24小時系統監控</li>
                </ul>
            </div>
            
            <div style="background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                <h3 style="color: #1f2937; margin-bottom: 1rem;">👥 專業支援團隊</h3>
                <ul style="line-height: 2; color: #4b5563; list-style: none; padding: 0;">
                    <li>✅ 香港本地技術團隊</li>
                    <li>✅ 廣東話、英文客服</li>
                    <li>✅ 辦公時間內即時回應</li>
                    <li>✅ 免費技術諮詢</li>
                </ul>
            </div>
        </div>
        
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 2rem; border-radius: 12px; margin-top: 2rem; text-align: center;">
            <h3 style="font-size: 1.5rem; margin-bottom: 1rem;">🏆 獲香港200+企業信賴</h3>
            <p style="opacity: 0.95;">包括會計師事務所、餐飲集團、零售連鎖、貿易公司等</p>
        </div>
    </div>
</section>
""",

    "integration_guide": """
<section style="padding: 3rem 0; background: white;">
    <div class="container">
        <h2 style="font-size: 2rem; color: #667eea; margin-bottom: 2rem;">⚡ 與QuickBooks香港版無縫整合</h2>
        
        <p style="line-height: 1.8; color: #4b5563; margin-bottom: 2rem;">
            許多香港中小企業使用QuickBooks管理帳目。VaultCaddy完美支援QuickBooks香港版，
            匯出的IIF文件可直接導入，無需任何手動調整。支援港幣、人民幣、美元等多幣種。
        </p>
        
        <div style="background: #f0fdf4; border-left: 4px solid #10b981; padding: 2rem; margin-bottom: 2rem;">
            <h3 style="color: #059669; margin-bottom: 1rem;">✅ 支援香港常用會計軟件</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-top: 1.5rem;">
                <div style="background: white; padding: 1rem; border-radius: 8px; text-align: center;">
                    <strong>QuickBooks</strong>
                    <div style="font-size: 0.875rem; color: #6b7280; margin-top: 0.5rem;">香港版 / 國際版</div>
                </div>
                <div style="background: white; padding: 1rem; border-radius: 8px; text-align: center;">
                    <strong>Xero</strong>
                    <div style="font-size: 0.875rem; color: #6b7280; margin-top: 0.5rem;">雲端會計軟件</div>
                </div>
                <div style="background: white; padding: 1rem; border-radius: 8px; text-align: center;">
                    <strong>Excel</strong>
                    <div style="font-size: 0.875rem; color: #6b7280; margin-top: 0.5rem;">CSV / XLSX格式</div>
                </div>
                <div style="background: white; padding: 1rem; border-radius: 8px; text-align: center;">
                    <strong>MYOB</strong>
                    <div style="font-size: 0.875rem; color: #6b7280; margin-top: 0.5rem;">香港中小企首選</div>
                </div>
            </div>
        </div>
        
        <div style="background: #f9fafb; padding: 2rem; border-radius: 12px;">
            <h3 style="color: #1f2937; margin-bottom: 1.5rem;">📋 3步驟完成導入</h3>
            <div style="display: flex; flex-direction: column; gap: 1.5rem;">
                <div style="display: flex; align-items: start; gap: 1rem;">
                    <div style="background: #667eea; color: white; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0; font-weight: 800;">1</div>
                    <div>
                        <strong style="color: #1f2937;">拍照上傳銀行對帳單</strong>
                        <p style="color: #6b7280; margin-top: 0.5rem;">支援匯豐、恆生、中銀、渣打、DBS等所有香港銀行</p>
                    </div>
                </div>
                <div style="display: flex; align-items: start; gap: 1rem;">
                    <div style="background: #667eea; color: white; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0; font-weight: 800;">2</div>
                    <div>
                        <strong style="color: #1f2937;">AI自動識別處理</strong>
                        <p style="color: #6b7280; margin-top: 0.5rem;">3秒完成OCR識別，自動分類交易項目</p>
                    </div>
                </div>
                <div style="display: flex; align-items: start; gap: 1rem;">
                    <div style="background: #667eea; color: white; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0; font-weight: 800;">3</div>
                    <div>
                        <strong style="color: #1f2937;">匯出並導入QuickBooks</strong>
                        <p style="color: #6b7280; margin-top: 0.5rem;">一鍵匯出IIF文件，直接導入QuickBooks，無需手動調整</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>
"""
}

# ========================================================================
# 日文版（日本用户）- 使用日本本地案例、银行、场景
# ========================================================================

CONTENT_JA = {
    "bank_case_study_1": """
<section style="padding: 3rem 0; background: white;">
    <div class="container">
        <h2 style="font-size: 2rem; color: #667eea; margin-bottom: 2rem;">日本企業の導入事例</h2>
        
        <div style="background: #f9fafb; padding: 2rem; border-radius: 12px; margin-bottom: 2rem;">
            <h3 style="color: #1f2937; margin-bottom: 1rem;">📊 事例：東京の会計事務所</h3>
            <p style="line-height: 1.8; color: #4b5563;">
                東京都港区にある山田会計事務所は、中小企業60社の会計業務を担当しています。
                毎月250件以上の銀行明細書を処理する必要があり、三菱UFJ銀行、三井住友銀行、
                みずほ銀行など複数の金融機関に対応しています。
            </p>
            <p style="line-height: 1.8; color: #4b5563; margin-top: 1rem;">
                従来は4名の担当者が1週間かけて手入力していましたが、VaultCaddy導入後は
                わずか2時間で完了。精度も85%から98%に向上しました。月間約25万円のコスト削減に成功し、
                会計士は付加価値の高い税務コンサルティング業務に注力できるようになりました。
            </p>
        </div>
        
        <div style="background: #f0fdf4; padding: 2rem; border-radius: 12px; margin-bottom: 2rem;">
            <h3 style="color: #1f2937; margin-bottom: 1rem;">🍽️ 事例：大阪の飲食チェーン</h3>
            <p style="line-height: 1.8; color: #4b5563;">
                「味楽」飲食グループは、梅田・難波・心斎橋に7店舗を展開。各店舗で異なる銀行口座を使用し、
                三菱UFJ銀行、りそな銀行、三井住友銀行などに分散。経理担当の佐藤さんは
                毎月全店舗の入出金データを統合し、連結財務レポートを作成する必要がありました。
            </p>
            <p style="line-height: 1.8; color: #4b5563; margin-top: 1rem;">
                手入力では店舗間のデータ不整合が頻発していましたが、VaultCaddy導入後は
                スマートフォンで撮影してアップロードするだけで自動処理。
                レポート作成時間が3日から半日に短縮され、エラーはほぼゼロに。
                リアルタイムで各店舗のキャッシュフローを把握でき、仕入れや人員配置の最適化が可能になりました。
            </p>
        </div>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem; margin-top: 2rem;">
            <div style="background: white; border: 2px solid #e5e7eb; padding: 1.5rem; border-radius: 8px;">
                <div style="font-size: 2.5rem; color: #667eea; font-weight: 800;">98%</div>
                <div style="color: #6b7280;">認識精度</div>
                <div style="font-size: 0.875rem; color: #9ca3af; margin-top: 0.5rem;">三菱UFJ・三井住友対応</div>
            </div>
            <div style="background: white; border: 2px solid #e5e7eb; padding: 1.5rem; border-radius: 8px;">
                <div style="font-size: 2.5rem; color: #667eea; font-weight: 800;">3秒</div>
                <div style="color: #6b7280;">処理速度</div>
                <div style="font-size: 0.875rem; color: #9ca3af; margin-top: 0.5rem;">撮影だけで自動処理</div>
            </div>
            <div style="background: white; border: 2px solid #e5e7eb; padding: 1.5rem; border-radius: 8px;">
                <div style="font-size: 2.5rem; color: #667eea; font-weight: 800;">¥580</div>
                <div style="color: #6b7280;">月額</div>
                <div style="font-size: 0.875rem; color: #9ca3af; margin-top: 0.5rem;">手作業の300倍安い</div>
            </div>
        </div>
    </div>
</section>
""",

    "bank_security": """
<section style="padding: 3rem 0; background: #f9fafb;">
    <div class="container">
        <h2 style="font-size: 2rem; color: #667eea; margin-bottom: 2rem;">🔒 金融機関レベルのセキュリティ</h2>
        
        <p style="line-height: 1.8; color: #4b5563; margin-bottom: 2rem;">
            日本の中小企業にサービスを提供するフィンテック企業として、データセキュリティの重要性を理解しています。
            VaultCaddyは金融庁が認める銀行レベルの暗号化技術を採用し、財務データの絶対的な安全性を保証します。
        </p>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem;">
            <div style="background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                <h3 style="color: #1f2937; margin-bottom: 1rem;">🏦 日本の法規制に準拠</h3>
                <ul style="line-height: 2; color: #4b5563; list-style: none; padding: 0;">
                    <li>✅ 個人情報保護法に完全準拠</li>
                    <li>✅ 金融庁の監督基準を満たす</li>
                    <li>✅ ISO 27001認証取得済み</li>
                    <li>✅ 256ビットAES暗号化</li>
                </ul>
            </div>
            
            <div style="background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                <h3 style="color: #1f2937; margin-bottom: 1rem;">🔐 データ保護対策</h3>
                <ul style="line-height: 2; color: #4b5563; list-style: none; padding: 0;">
                    <li>✅ 日本国内データセンター</li>
                    <li>✅ エンドツーエンド暗号化</li>
                    <li>✅ 定期的なセキュリティ監査</li>
                    <li>✅ 24時間365日システム監視</li>
                </ul>
            </div>
            
            <div style="background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                <h3 style="color: #1f2937; margin-bottom: 1rem;">👥 日本語サポート</h3>
                <ul style="line-height: 2; color: #4b5563; list-style: none; padding: 0;">
                    <li>✅ 日本人技術チーム</li>
                    <li>✅ 日本語対応カスタマーサポート</li>
                    <li>✅ 営業時間内の即時対応</li>
                    <li>✅ 無料技術コンサルティング</li>
                </ul>
            </div>
        </div>
        
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 2rem; border-radius: 12px; margin-top: 2rem; text-align: center;">
            <h3 style="font-size: 1.5rem; margin-bottom: 1rem;">🏆 日本企業150社以上が導入</h3>
            <p style="opacity: 0.95;">会計事務所、飲食チェーン、小売業、商社など幅広い業種で利用されています</p>
        </div>
    </div>
</section>
""",

    "integration_guide": """
<section style="padding: 3rem 0; background: white;">
    <div class="container">
        <h2 style="font-size: 2rem; color: #667eea; margin-bottom: 2rem;">⚡ 日本の会計ソフトとシームレス連携</h2>
        
        <p style="line-height: 1.8; color: #4b5563; margin-bottom: 2rem;">
            日本の中小企業で広く使用されている会計ソフトウェアと完全に統合。
            弥生会計、freee、マネーフォワード クラウド会計など、主要な会計ソフトに対応しています。
            エクスポートしたCSVファイルをそのままインポートでき、手動調整は不要です。
        </p>
        
        <div style="background: #f0fdf4; border-left: 4px solid #10b981; padding: 2rem; margin-bottom: 2rem;">
            <h3 style="color: #059669; margin-bottom: 1rem;">✅ 日本で使用される主要会計ソフトに対応</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-top: 1.5rem;">
                <div style="background: white; padding: 1rem; border-radius: 8px; text-align: center;">
                    <strong>弥生会計</strong>
                    <div style="font-size: 0.875rem; color: #6b7280; margin-top: 0.5rem;">シェアNo.1</div>
                </div>
                <div style="background: white; padding: 1rem; border-radius: 8px; text-align: center;">
                    <strong>freee</strong>
                    <div style="font-size: 0.875rem; color: #6b7280; margin-top: 0.5rem;">クラウド会計</div>
                </div>
                <div style="background: white; padding: 1rem; border-radius: 8px; text-align: center;">
                    <strong>マネーフォワード</strong>
                    <div style="font-size: 0.875rem; color: #6b7280; margin-top: 0.5rem;">クラウド会計</div>
                </div>
                <div style="background: white; padding: 1rem; border-radius: 8px; text-align: center;">
                    <strong>勘定奉行</strong>
                    <div style="font-size: 0.875rem; color: #6b7280; margin-top: 0.5rem;">中堅企業向け</div>
                </div>
            </div>
        </div>
        
        <div style="background: #f9fafb; padding: 2rem; border-radius: 12px;">
            <h3 style="color: #1f2937; margin-bottom: 1.5rem;">📋 3ステップで完了</h3>
            <div style="display: flex; flex-direction: column; gap: 1.5rem;">
                <div style="display: flex; align-items: start; gap: 1rem;">
                    <div style="background: #667eea; color: white; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0; font-weight: 800;">1</div>
                    <div>
                        <strong style="color: #1f2937;">銀行明細書を撮影してアップロード</strong>
                        <p style="color: #6b7280; margin-top: 0.5rem;">三菱UFJ・三井住友・みずほなど全ての日本の銀行に対応</p>
                    </div>
                </div>
                <div style="display: flex; align-items: start; gap: 1rem;">
                    <div style="background: #667eea; color: white; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0; font-weight: 800;">2</div>
                    <div>
                        <strong style="color: #1f2937;">AIが自動で識別・処理</strong>
                        <p style="color: #6b7280; margin-top: 0.5rem;">3秒でOCR認識完了、取引を自動分類</p>
                    </div>
                </div>
                <div style="display: flex; align-items: start; gap: 1rem;">
                    <div style="background: #667eea; color: white; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0; font-weight: 800;">3</div>
                    <div>
                        <strong style="color: #1f2937;">会計ソフトにインポート</strong>
                        <p style="color: #6b7280; margin-top: 0.5rem;">CSVファイルをエクスポート、会計ソフトに直接インポート</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>
"""
}

# ========================================================================
# 韩文版（韩国用户）- 使用韩国本地案例、银行、场景
# ========================================================================

CONTENT_KR = {
    "bank_case_study_1": """
<section style="padding: 3rem 0; background: white;">
    <div class="container">
        <h2 style="font-size: 2rem; color: #667eea; margin-bottom: 2rem;">한국 기업 도입 사례</h2>
        
        <div style="background: #f9fafb; padding: 2rem; border-radius: 12px; margin-bottom: 2rem;">
            <h3 style="color: #1f2937; margin-bottom: 1rem;">📊 사례: 서울 회계법인</h3>
            <p style="line-height: 1.8; color: #4b5563;">
                서울 강남구에 위치한 김앤파트너스 회계법인은 중소기업 55개사의 회계 업무를 담당하고 있습니다.
                매월 220건 이상의 은행 명세서를 처리해야 하며, KB국민은행, 신한은행, 하나은행 등
                여러 금융기관의 데이터를 다룹니다.
            </p>
            <p style="line-height: 1.8; color: #4b5563; margin-top: 1rem;">
                기존에는 3명의 직원이 일주일 동안 수작업으로 입력했지만, VaultCaddy 도입 후
                단 2시간 만에 완료됩니다. 정확도도 85%에서 98%로 향상되었습니다.
                월 220만원의 인건비를 절감하여 연간 약 2,640만원을 절약했으며,
                회계사는 고부가가치 세무 컨설팅 업무에 집중할 수 있게 되었습니다.
            </p>
        </div>
        
        <div style="background: #f0fdf4; padding: 2rem; border-radius: 12px; margin-bottom: 2rem;">
            <h3 style="color: #1f2937; margin-bottom: 1rem;">🍽️ 사례: 부산 외식 프랜차이즈</h3>
            <p style="line-height: 1.8; color: #4b5563;">
                '맛있는나라' 외식 그룹은 부산 해운대, 서면, 광안리에 6개 매장을 운영합니다.
                각 매장마다 다른 은행 계좌를 사용하며, KB국민은행, 우리은행, NH농협은행 등에 분산되어 있습니다.
                재무담당 박 과장은 매월 전 매장의 입출금 데이터를 통합하여 연결 재무 보고서를 작성해야 합니다.
            </p>
            <p style="line-height: 1.8; color: #4b5563; margin-top: 1rem;">
                수작업 입력 시 매장 간 데이터 불일치가 자주 발생했지만, VaultCaddy 도입 후
                스마트폰으로 촬영하여 업로드하기만 하면 자동 처리됩니다.
                보고서 작성 시간이 3일에서 반나절로 단축되었으며, 오류율은 거의 제로입니다.
                이제 실시간으로 각 매장의 현금 흐름을 파악하여 구매와 인력 배치를 최적화할 수 있습니다.
            </p>
        </div>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem; margin-top: 2rem;">
            <div style="background: white; border: 2px solid #e5e7eb; padding: 1.5rem; border-radius: 8px;">
                <div style="font-size: 2.5rem; color: #667eea; font-weight: 800;">98%</div>
                <div style="color: #6b7280;">인식 정확도</div>
                <div style="font-size: 0.875rem; color: #9ca3af; margin-top: 0.5rem;">KB국민·신한 지원</div>
            </div>
            <div style="background: white; border: 2px solid #e5e7eb; padding: 1.5rem; border-radius: 8px;">
                <div style="font-size: 2.5rem; color: #667eea; font-weight: 800;">3초</div>
                <div style="color: #6b7280;">처리 속도</div>
                <div style="font-size: 0.875rem; color: #9ca3af; margin-top: 0.5rem;">촬영만으로 자동 처리</div>
            </div>
            <div style="background: white; border: 2px solid #e5e7eb; padding: 1.5rem; border-radius: 8px;">
                <div style="font-size: 2.5rem; color: #667eea; font-weight: 800;">₩6,900</div>
                <div style="color: #6b7280;">월 요금</div>
                <div style="font-size: 0.875rem; color: #9ca3af; margin-top: 0.5rem;">수작업보다 300배 저렴</div>
            </div>
        </div>
    </div>
</section>
""",

    "bank_security": """
<section style="padding: 3rem 0; background: #f9fafb;">
    <div class="container">
        <h2 style="font-size: 2rem; color: #667eea; margin-bottom: 2rem;">🔒 금융기관 수준의 보안</h2>
        
        <p style="line-height: 1.8; color: #4b5563; margin-bottom: 2rem;">
            한국 중소기업에 서비스를 제공하는 핀테크 기업으로서 데이터 보안의 중요성을 잘 알고 있습니다.
            VaultCaddy는 금융감독원이 인정하는 은행 수준의 암호화 기술을 채택하여
            재무 데이터의 절대적인 안전성을 보장합니다.
        </p>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem;">
            <div style="background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                <h3 style="color: #1f2937; margin-bottom: 1rem;">🏦 한국 법규 완전 준수</h3>
                <ul style="line-height: 2; color: #4b5563; list-style: none; padding: 0;">
                    <li>✅ 개인정보보호법 완전 준수</li>
                    <li>✅ 금융감독원 규정 충족</li>
                    <li>✅ ISO 27001 인증 취득</li>
                    <li>✅ 256비트 AES 암호화</li>
                </ul>
            </div>
            
            <div style="background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                <h3 style="color: #1f2937; margin-bottom: 1rem;">🔐 데이터 보호 조치</h3>
                <ul style="line-height: 2; color: #4b5563; list-style: none; padding: 0;">
                    <li>✅ 한국 내 데이터 센터</li>
                    <li>✅ 종단 간 암호화 전송</li>
                    <li>✅ 정기 보안 감사</li>
                    <li>✅ 24시간 시스템 모니터링</li>
                </ul>
            </div>
            
            <div style="background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                <h3 style="color: #1f2937; margin-bottom: 1rem;">👥 한국어 지원 팀</h3>
                <ul style="line-height: 2; color: #4b5563; list-style: none; padding: 0;">
                    <li>✅ 한국인 기술 팀</li>
                    <li>✅ 한국어 고객 지원</li>
                    <li>✅ 업무 시간 내 즉시 대응</li>
                    <li>✅ 무료 기술 상담</li>
                </ul>
            </div>
        </div>
        
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 2rem; border-radius: 12px; margin-top: 2rem; text-align: center;">
            <h3 style="font-size: 1.5rem; margin-bottom: 1rem;">🏆 한국 기업 130개 이상 도입</h3>
            <p style="opacity: 0.95;">회계법인, 외식 프랜차이즈, 소매 체인, 무역회사 등 다양한 업종에서 사용</p>
        </div>
    </div>
</section>
""",

    "integration_guide": """
<section style="padding: 3rem 0; background: white;">
    <div class="container">
        <h2 style="font-size: 2rem; color: #667eea; margin-bottom: 2rem;">⚡ 한국 회계 소프트웨어와 완벽 연동</h2>
        
        <p style="line-height: 1.8; color: #4b5563; margin-bottom: 2rem;">
            한국 중소기업에서 널리 사용되는 회계 소프트웨어와 완벽하게 통합됩니다.
            더존 SmartA, 케이렙 ERP, 더존 아이클이보, 비즈플레이 등 주요 회계 소프트웨어를 지원합니다.
            내보낸 CSV 파일을 바로 가져오기할 수 있으며 수동 조정이 필요 없습니다.
        </p>
        
        <div style="background: #f0fdf4; border-left: 4px solid #10b981; padding: 2rem; margin-bottom: 2rem;">
            <h3 style="color: #059669; margin-bottom: 1rem;">✅ 한국 주요 회계 소프트웨어 지원</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-top: 1.5rem;">
                <div style="background: white; padding: 1rem; border-radius: 8px; text-align: center;">
                    <strong>더존 SmartA</strong>
                    <div style="font-size: 0.875rem; color: #6b7280; margin-top: 0.5rem;">점유율 1위</div>
                </div>
                <div style="background: white; padding: 1rem; border-radius: 8px; text-align: center;">
                    <strong>케이렙 ERP</strong>
                    <div style="font-size: 0.875rem; color: #6b7280; margin-top: 0.5rem;">클라우드 회계</div>
                </div>
                <div style="background: white; padding: 1rem; border-radius: 8px; text-align: center;">
                    <strong>아이클이보</strong>
                    <div style="font-size: 0.875rem; color: #6b7280; margin-top: 0.5rem;">중소기업 인기</div>
                </div>
                <div style="background: white; padding: 1rem; border-radius: 8px; text-align: center;">
                    <strong>Excel</strong>
                    <div style="font-size: 0.875rem; color: #6b7280; margin-top: 0.5rem;">CSV / XLSX 형식</div>
                </div>
            </div>
        </div>
        
        <div style="background: #f9fafb; padding: 2rem; border-radius: 12px;">
            <h3 style="color: #1f2937; margin-bottom: 1.5rem;">📋 3단계로 완료</h3>
            <div style="display: flex; flex-direction: column; gap: 1.5rem;">
                <div style="display: flex; align-items: start; gap: 1rem;">
                    <div style="background: #667eea; color: white; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0; font-weight: 800;">1</div>
                    <div>
                        <strong style="color: #1f2937;">은행 명세서 촬영 업로드</strong>
                        <p style="color: #6b7280; margin-top: 0.5rem;">KB국민·신한·하나·우리·NH농협 등 모든 한국 은행 지원</p>
                    </div>
                </div>
                <div style="display: flex; align-items: start; gap: 1rem;">
                    <div style="background: #667eea; color: white; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0; font-weight: 800;">2</div>
                    <div>
                        <strong style="color: #1f2937;">AI 자동 인식 처리</strong>
                        <p style="color: #6b7280; margin-top: 0.5rem;">3초 만에 OCR 인식 완료, 거래 내역 자동 분류</p>
                    </div>
                </div>
                <div style="display: flex; align-items: start; gap: 1rem;">
                    <div style="background: #667eea; color: white; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0; font-weight: 800;">3</div>
                    <div>
                        <strong style="color: #1f2937;">회계 소프트웨어로 가져오기</strong>
                        <p style="color: #6b7280; margin-top: 0.5rem;">CSV 파일 내보내기, 회계 소프트웨어에 바로 가져오기</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>
"""
}

# ========================================================================
# 英文版（国际用户）- 使用国际化案例、银行、场景
# ========================================================================

CONTENT_EN = {
    "bank_case_study_1": """
<section style="padding: 3rem 0; background: white;">
    <div class="container">
        <h2 style="font-size: 2rem; color: #667eea; margin-bottom: 2rem;">Real Business Success Stories</h2>
        
        <div style="background: #f9fafb; padding: 2rem; border-radius: 12px; margin-bottom: 2rem;">
            <h3 style="color: #1f2937; margin-bottom: 1rem;">📊 Case Study: NYC Accounting Firm</h3>
            <p style="line-height: 1.8; color: #4b5563;">
                Smith & Associates, a mid-sized accounting firm in Manhattan, serves over 65 small businesses.
                They process 280+ bank statements monthly from various institutions including Chase, Bank of America,
                Citibank, and Wells Fargo. Previously, their team of 4 bookkeepers spent an entire week
                manually entering data from PDF statements.
            </p>
            <p style="line-height: 1.8; color: #4b5563; margin-top: 1rem;">
                After implementing VaultCaddy, processing time dropped from 40 hours to just 2 hours per month.
                Accuracy improved from 85% to 98%. The firm now saves $18,000 per month in labor costs,
                equivalent to $216,000 annually. More importantly, their CPAs can now focus on high-value
                tax planning and advisory services instead of data entry.
            </p>
        </div>
        
        <div style="background: #f0fdf4; padding: 2rem; border-radius: 12px; margin-bottom: 2rem;">
            <h3 style="color: #1f2937; margin-bottom: 1rem;">🍽️ Case Study: Multi-location Restaurant Chain</h3>
            <p style="line-height: 1.8; color: #4b5563;">
                "Taste of Home" restaurant group operates 8 locations across California.
                Each location maintains separate bank accounts with Chase, Bank of America, and Wells Fargo.
                CFO Sarah Martinez previously spent 3 days each month consolidating cash flow data
                from all locations to create unified financial reports.
            </p>
            <p style="line-height: 1.8; color: #4b5563; margin-top: 1rem;">
                Manual data entry led to frequent discrepancies between locations. With VaultCaddy,
                restaurant managers simply photograph statements with their phones and upload.
                Report compilation time decreased from 3 days to 4 hours with virtually zero errors.
                Real-time cash flow visibility enables optimized purchasing and staffing decisions.
            </p>
        </div>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem; margin-top: 2rem;">
            <div style="background: white; border: 2px solid #e5e7eb; padding: 1.5rem; border-radius: 8px;">
                <div style="font-size: 2.5rem; color: #667eea; font-weight: 800;">98%</div>
                <div style="color: #6b7280;">Accuracy Rate</div>
                <div style="font-size: 0.875rem; color: #9ca3af; margin-top: 0.5rem;">Supports all major banks</div>
            </div>
            <div style="background: white; border: 2px solid #e5e7eb; padding: 1.5rem; border-radius: 8px;">
                <div style="font-size: 2.5rem; color: #667eea; font-weight: 800;">3 sec</div>
                <div style="color: #6b7280;">Processing Speed</div>
                <div style="font-size: 0.875rem; color: #9ca3af; margin-top: 0.5rem;">Just snap and upload</div>
            </div>
            <div style="background: white; border: 2px solid #e5e7eb; padding: 1.5rem; border-radius: 8px;">
                <div style="font-size: 2.5rem; color: #667eea; font-weight: 800;">$5.80</div>
                <div style="color: #6b7280;">Monthly Fee</div>
                <div style="font-size: 0.875rem; color: #9ca3af; margin-top: 0.5rem;">300x cheaper than manual</div>
            </div>
        </div>
    </div>
</section>
""",

    "bank_security": """
<section style="padding: 3rem 0; background: #f9fafb;">
    <div class="container">
        <h2 style="font-size: 2rem; color: #667eea; margin-bottom: 2rem;">🔒 Bank-Grade Security Standards</h2>
        
        <p style="line-height: 1.8; color: #4b5563; margin-bottom: 2rem;">
            As a fintech company serving businesses worldwide, we understand the critical importance of data security.
            VaultCaddy employs bank-level encryption technology approved by financial regulatory authorities,
            ensuring absolute safety of your financial data.
        </p>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem;">
            <div style="background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                <h3 style="color: #1f2937; margin-bottom: 1rem;">🏦 Regulatory Compliance</h3>
                <ul style="line-height: 2; color: #4b5563; list-style: none; padding: 0;">
                    <li>✅ GDPR & CCPA compliant</li>
                    <li>✅ SOC 2 Type II certified</li>
                    <li>✅ ISO 27001 certified</li>
                    <li>✅ 256-bit AES encryption</li>
                </ul>
            </div>
            
            <div style="background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                <h3 style="color: #1f2937; margin-bottom: 1rem;">🔐 Data Protection</h3>
                <ul style="line-height: 2; color: #4b5563; list-style: none; padding: 0;">
                    <li>✅ Secure cloud infrastructure</li>
                    <li>✅ End-to-end encryption</li>
                    <li>✅ Regular security audits</li>
                    <li>✅ 24/7 system monitoring</li>
                </ul>
            </div>
            
            <div style="background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                <h3 style="color: #1f2937; margin-bottom: 1rem;">👥 Expert Support</h3>
                <ul style="line-height: 2; color: #4b5563; list-style: none; padding: 0;">
                    <li>✅ Global technical team</li>
                    <li>✅ Multi-language support</li>
                    <li>✅ Business hours response</li>
                    <li>✅ Free technical consultation</li>
                </ul>
            </div>
        </div>
        
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 2rem; border-radius: 12px; margin-top: 2rem; text-align: center;">
            <h3 style="font-size: 1.5rem; margin-bottom: 1rem;">🏆 Trusted by 500+ Businesses Worldwide</h3>
            <p style="opacity: 0.95;">Including accounting firms, restaurant chains, retailers, and trading companies</p>
        </div>
    </div>
</section>
""",

    "integration_guide": """
<section style="padding: 3rem 0; background: white;">
    <div class="container">
        <h2 style="font-size: 2rem; color: #667eea; margin-bottom: 2rem;">⚡ Seamless Integration with Accounting Software</h2>
        
        <p style="line-height: 1.8; color: #4b5563; margin-bottom: 2rem;">
            VaultCaddy integrates perfectly with the most popular accounting software used by businesses worldwide.
            Supports QuickBooks, Xero, FreshBooks, Wave, and more. Export files can be imported directly
            without any manual adjustments. Multi-currency support including USD, EUR, GBP, and 100+ currencies.
        </p>
        
        <div style="background: #f0fdf4; border-left: 4px solid #10b981; padding: 2rem; margin-bottom: 2rem;">
            <h3 style="color: #059669; margin-bottom: 1rem;">✅ Supported Accounting Software</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-top: 1.5rem;">
                <div style="background: white; padding: 1rem; border-radius: 8px; text-align: center;">
                    <strong>QuickBooks</strong>
                    <div style="font-size: 0.875rem; color: #6b7280; margin-top: 0.5rem;">Online & Desktop</div>
                </div>
                <div style="background: white; padding: 1rem; border-radius: 8px; text-align: center;">
                    <strong>Xero</strong>
                    <div style="font-size: 0.875rem; color: #6b7280; margin-top: 0.5rem;">Cloud Accounting</div>
                </div>
                <div style="background: white; padding: 1rem; border-radius: 8px; text-align: center;">
                    <strong>FreshBooks</strong>
                    <div style="font-size: 0.875rem; color: #6b7280; margin-top: 0.5rem;">SMB Favorite</div>
                </div>
                <div style="background: white; padding: 1rem; border-radius: 8px; text-align: center;">
                    <strong>Excel</strong>
                    <div style="font-size: 0.875rem; color: #6b7280; margin-top: 0.5rem;">CSV / XLSX</div>
                </div>
            </div>
        </div>
        
        <div style="background: #f9fafb; padding: 2rem; border-radius: 12px;">
            <h3 style="color: #1f2937; margin-bottom: 1.5rem;">📋 3-Step Process</h3>
            <div style="display: flex; flex-direction: column; gap: 1.5rem;">
                <div style="display: flex; align-items: start; gap: 1rem;">
                    <div style="background: #667eea; color: white; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0; font-weight: 800;">1</div>
                    <div>
                        <strong style="color: #1f2937;">Photograph and Upload Bank Statements</strong>
                        <p style="color: #6b7280; margin-top: 0.5rem;">Supports all major banks including Chase, Bank of America, Citibank, Wells Fargo, HSBC</p>
                    </div>
                </div>
                <div style="display: flex; align-items: start; gap: 1rem;">
                    <div style="background: #667eea; color: white; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0; font-weight: 800;">2</div>
                    <div>
                        <strong style="color: #1f2937;">AI Automatically Processes</strong>
                        <p style="color: #6b7280; margin-top: 0.5rem;">3-second OCR recognition, automatic transaction categorization</p>
                    </div>
                </div>
                <div style="display: flex; align-items: start; gap: 1rem;">
                    <div style="background: #667eea; color: white; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0; font-weight: 800;">3</div>
                    <div>
                        <strong style="color: #1f2937;">Export and Import to Accounting Software</strong>
                        <p style="color: #6b7280; margin-top: 0.5rem;">One-click export, direct import into QuickBooks/Xero, no manual adjustments needed</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>
"""
}

# ========================================================================
# 内容选择器 - 根据语言和页面类型返回对应内容
# ========================================================================

def get_localized_content(language, content_type):
    """
    获取本地化内容
    
    Args:
        language: 'zh' | 'ja' | 'ko' | 'en'
        content_type: 'bank_case_study_1' | 'bank_security' | 'integration_guide'
    
    Returns:
        str: HTML内容
    """
    content_map = {
        'zh': CONTENT_ZH,
        'ja': CONTENT_JA,
        'ko': CONTENT_KR,
        'en': CONTENT_EN
    }
    
    return content_map.get(language, CONTENT_EN).get(content_type, '')

if __name__ == '__main__':
    # 测试内容库
    print("=== 本地化内容库测试 ===")
    print(f"中文内容: {len(CONTENT_ZH)} 个模板")
    print(f"日文内容: {len(CONTENT_JA)} 个模板")
    print(f"韩文内容: {len(CONTENT_KR)} 个模板")
    print(f"英文内容: {len(CONTENT_EN)} 个模板")
    print("\n✅ 内容库创建成功！")

