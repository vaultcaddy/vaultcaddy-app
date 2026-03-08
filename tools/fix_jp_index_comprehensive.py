#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日文版首页综合翻译：Phase 3-9 一次完成
批量翻译HTML注释、Alt标签、CSS注释、console.log等所有剩余中文
"""

import re

def fix_jp_index_comprehensive():
    """综合翻译：一次性处理所有剩余中文内容"""
    
    file_path = 'jp/index.html'
    
    print("🔍 综合翻译Phase 3-9: 批量翻译所有剩余内容...")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    chinese_chars_before = len(re.findall(r'[一-龥]', content))
    print(f"📊 发现 {chinese_chars_before} 个中文字符")
    
    # ============================================
    # 超大规模翻译字典（中文 -> 日文）
    # ============================================
    print("🔄 开始批量翻译...")
    
    comprehensive_translations = {
        # HTML注释
        '價格區域': '料金セクション',
        '月付和年付並列顯示': '月額プランと年額プランを並べて表示',
        '月付方案': '月額プラン',
        '🔥 標題和價格橫向排列': '🔥 タイトルと価格を横並び配置',
        'CTA 按鈕': 'CTAボタン',
        '年付方案': '年額プラン',
        '客戶評價區域（BankGPT 風格）': 'カスタマーレビューセクション（BankGPTスタイル）',
        '標題': 'タイトル',
        '6張評價卡片 3x2 網格（桌面版）/ 輪播（手機版）': '6件のレビューカード 3x2グリッド（デスクトップ）/ カルーセル（モバイル）',
        '評價卡片 1': 'レビューカード 1',
        '評價卡片 2': 'レビューカード 2',
        '評價卡片 3': 'レビューカード 3',
        '評價卡片 4': 'レビューカード 4',
        '評價卡片 5': 'レビューカード 5',
        '評價卡片 6': 'レビューカード 6',
        'SEO 文章引導區域': 'SEO記事ガイドセクション',
        '文章 1': '記事 1',
        '文章 2': '記事 2',
        'CTA 卡片': 'CTAカード',
        '頁尾': 'フッター',
        'Footer 內容': 'フッターコンテンツ',
        'Logo 和描述': 'ロゴと説明',
        'Footer 底部': 'フッター下部',
        'Footer 鏈接 Hover 效果': 'フッターリンクホバーエフェクト',
        '響應式設計': 'レスポンシブデザイン',
        '手机版Hero区域向上移动消除白色空白': 'モバイル版Heroセクションを上に移動して白い空白を除去',
        '導航欄': 'ナビゲーションバー',
        '顯示漢堡菜單按鈕': 'ハンバーガーメニューボタンを表示',
        '手機版顯示 logo, 隱藏文字': 'モバイル版でロゴを表示、テキストを非表示',
        '✅ 顯示 V 圖標': '✅ Vアイコンを表示',
        '✅ 隱藏 "VaultCaddy" 文字': '✅ "VaultCaddy"テキストを非表示',
        '隱藏導航欄中的文字鏈接': 'ナビゲーションバーのテキストリンクを非表示',
        'User dropdown menu位置': 'ユーザードロップダウンメニュー位置',
        '💡 手機版：確保用戶菜單按鈕和頭像正確顯示': '💡 モバイル版：ユーザーメニューボタンとアバターが正しく表示されることを確認',
        '🔥 通用：減少所有容器的左右內距': '🔥 共通：全コンテナの左右パディングを削減',
        '🔥 功能卡片內距優化': '🔥 機能カードパディング最適化',
        '🔥 智能發票/銀行對賬單徽章置中（提高優先級）': '🔥 スマートインボイス/銀行明細書バッジを中央配置（優先度向上）',
        '🔥 標題也置中（提高優先級）': '🔥 タイトルも中央配置（優先度向上）',
        '🔥 功能區內的所有 flex 容器間距減少': '🔥 機能エリア内の全flexコンテナ間隔を削減',
        '🔥 描述段落間距進一步減少（總共 30pt）': '🔥 説明段落間隔をさらに削減（合計30pt）',
        
        # Alt标签
        'VaultCaddy用戶John M. - 香港會計師 - 使用VaultCaddy處理銀行對帳單': 'VaultCaddyユーザーJohn M. - 会計士 - VaultCaddyで銀行明細書を処理',
        'VaultCaddy用戶Sarah T. - 簿記員 - 推薦VaultCaddy銀行對帳單AI處理工具': 'VaultCaddyユーザーSarah T. - 経理担当 - VaultCaddy銀行明細書AI処理ツールを推薦',
        'VaultCaddy用戶David L. - 公司老闆 - VaultCaddy節省90%記帳時間': 'VaultCaddyユーザーDavid L. - 経営者 - VaultCaddyで記帳時間90%削減',
        'VaultCaddy用戶Emily R. - 財務經理 - VaultCaddy QuickBooks整合專家': 'VaultCaddyユーザーEmily R. - 財務マネージャー - VaultCaddy QuickBooks統合エキスパート',
        'VaultCaddy用戶Michael K. - 自由工作者 - VaultCaddy低成本記帳解決方案': 'VaultCaddyユーザーMichael K. - フリーランス - VaultCaddy低コスト記帳ソリューション',
        'VaultCaddy用戶Sophia W. - 小店老闆 - VaultCaddy自動化對帳單處理': 'VaultCaddyユーザーSophia W. - 小規模事業主 - VaultCaddy自動明細書処理',
        
        # Console.log和JavaScript
        '獲取用戶首字母': 'ユーザーイニシャルを取得',
        '優先使用 displayName 的第一個字母': 'displayNameの最初の文字を優先使用',
        '否則使用 email 的第一個字母': 'そうでなければemailの最初の文字を使用',
        '🔥 漢堡Menu功能（立即執行, 不等待 DOMContentLoaded）': '🔥 ハンバーガーメニュー機能（即座実行、DOMContentLoaded待たない）',
        '🔵 初始化漢堡Menu...': '🔵 ハンバーガーメニューを初期化...',
        'Open側邊欄': 'サイドバーを開く',
        '🔵 openMobileSidebar 被調用': '🔵 openMobileSidebarが呼び出されました',
        '❌ 找不到側邊欄或遮罩元素': '❌ サイドバーまたはオーバーレイ要素が見つかりません',
        'Close側邊欄': 'サイドバーを閉じる',
        '🔵 closeMobileSidebar 被調用': '🔵 closeMobileSidebarが呼び出されました',
        '確保漢堡MenuButton綁定（多重綁定策略）': 'ハンバーガーメニューボタンバインディングを確保（マルチバインディング戦略）',
        '✅ Found漢堡MenuButton, 開始綁定事件': '✅ ハンバーガーメニューボタンを発見、イベントバインディング開始',
        '創建統一的處理函數': '統一処理関数を作成',
        '🔵 MenuButton被Trigger': '🔵 メニューボタンがトリガーされました',
        'Click 事件（滑鼠和一般觸摸）': 'Clickイベント（マウスおよび一般タッチ）',
        'Touchend 事件（iOS Safari 更可靠）': 'Touchendイベント（iOS Safariでより確実）',
        '🔥 3. 只在MobileSettings可見（不影響Desktop）': '🔥 3. モバイル設定表示時のみ（デスクトップに影響なし）',
        'Mobile：漢堡Menu已啟用': 'モバイル：ハンバーガーメニューが有効',
        'Desktop：漢堡Menu保持Hide': 'デスクトップ：ハンバーガーメニューは非表示',
        '✅ 漢堡Menu功能已綁定（click + touchend）': '✅ ハンバーガーメニュー機能をバインド（click + touchend）',
        '⚠️ 找不到漢堡MenuButton': '⚠️ ハンバーガーメニューボタンが見つかりません',
        
        # CSS注释
        '總共上移 60pt': '合計60pt上に移動',
        '內層容器': '内部コンテナ',
        '文字大小適配': 'テキストサイズ適応',
        '✅ PRICING - 使用真實版設計（顯示詳細功能列表）': '✅ PRICING - 実際バージョンデザインを使用（詳細機能リスト表示）',
        '🔥 定價區塊：手機版改為單列, 卡片居中': '🔥 料金セクション：モバイル版を1列に、カードを中央配置',
        '🔥 卡片間距減少': '🔥 カード間隔削減',
        '🔥 定價卡片：收窄並居中, 減少內距': '🔥 料金カード：幅を狭めて中央配置、パディング削減',
        '🔥 內距減少': '🔥 パディング削減',
        '🔥 定價卡片': '🔥 料金カード',
        '🔥 定價卡片Title': '🔥 料金カードタイトル',
        '🔥 價格數字': '🔥 価格数値',
        '🔥 功能列表容器': '🔥 機能リストコンテナ',
        "🔥 What's IncludedTitle - 放大到Title大小": "🔥 What's Includedタイトル - タイトルサイズに拡大",
        '🔥 功能列表：改為 2 列布局': '🔥 機能リスト：2列レイアウトに変更',
        '🔥 功能列表項目 - 放大到Title大小': '🔥 機能リスト項目 - タイトルサイズに拡大',
        '🔥 功能列表勾選圖標 - 放大': '🔥 機能リストチェックマークアイコン - 拡大',
        '🔥 CTA Button：減少內距': '🔥 CTAボタン：パディング削減',
        '🔥 Save 20% 標籤：放大到Title大小': '🔥 20%割引ラベル：タイトルサイズに拡大',
        '🔥 放大到Title大小': '🔥 タイトルサイズに拡大',
        '✅ TESTIMONIALS - 使用真實版設計（Sarah T. 有邊框）': '✅ TESTIMONIALS - 実際バージョンデザインを使用（Sarah T.に枠線）',
        '✅ FEATURES - 使用真實版設計（已在 HTML 中有打勾圖標, 不需要 ::before）': '✅ FEATURES - 実際バージョンデザインを使用（HTMLに既にチェックマークアイコンがあり、::before不要）',
        '🔥 再減半（從 0.35rem → 0.175rem）': '🔥 さらに半分に削減（0.35rem → 0.175rem）',
        '🔥 功能文字段落間空白再減半（從 0.5rem → 0.25rem）': '🔥 機能テキスト段落間隔をさらに半分に（0.5rem → 0.25rem）',
        '🔥 功能Title下方間距再減半': '🔥 機能タイトル下部マージンをさらに半分に',
        '🔥 功能徽章下方間距再減半': '🔥 機能バッジ下部マージンをさらに半分に',
        '🔥 價值卡片（Ultra-Fast Processing/超高準確率/性價比最高）- 強制收窄底部空白': '🔥 価値カード（超高速処理/最高精度/最高コストパフォーマンス）- 下部スペース強制削減',
        '🔥 進一步縮小': '🔥 さらに縮小',
        '🔥 價值卡片Title間距': '🔥 価値カードタイトル間隔',
        '🔥 價值卡片圖標容器間距': '🔥 価値カードアイコンコンテナ間隔',
        '🔥 價值卡片描述最後一行底部間距移除': '🔥 価値カード説明最終行下部マージン削除',
        '🔥 Hero 區域：信任標籤置中': '🔥 Heroエリア：信頼ラベルを中央配置',
        '🔥 Hero 區域：副Title分行顯示': '🔥 Heroエリア：サブタイトル改行表示',
        '🔥 CTA Button向上移 10pt': '🔥 CTAボタンを10pt上に移動',
        '🔥 統計數據向上移 20pt': '🔥 統計データを20pt上に移動',
        '🔥 確保藍色標籤保持圓角膠囊形狀': '🔥 青色ラベルが丸みを帯びたピル形状を維持することを確保',
        '圓角膠囊': '丸みを帯びたピル',
        '🔥 確保圓形圖標容器顯示（圖3/4 - 超高準確率等圖標）': '🔥 円形アイコンコンテナが表示されることを確保（図3/4 - 最高精度アイコン等）',
        '🔥 確保圖標內的 Font Awesome 圖標顯示': '🔥 アイコン内のFont Awesomeアイコンが表示されることを確保',
        '🔥 手機版啟用動畫特效（與電腦版相同）': '🔥 モバイル版でアニメーション効果を有効化（デスクトップ版と同じ）',
        '移除了強制立即顯示的規則, 讓 Intersection Observer 自然觸發動畫': '強制即座表示ルールを削除、Intersection Observerが自然にアニメーションをトリガー',
        '小屏幕手機優化 (iPhone SE 等)': '小画面モバイル最適化（iPhone SE等）',
        
        # 更多JavaScript相关
        '數字滾動動畫腳本': '数値スクロールアニメーションスクリプト',
        '數字滾動動畫函數': '数値スクロールアニメーション関数',
        '使用 easeOutQuart 緩動函數': 'easeOutQuartイージング関数を使用',
        '頁面加載後啟動數字動畫': 'ページ読み込み後に数値アニメーション開始',
        '延遲 300ms 開始動畫': 'アニメーション開始を300ms遅延',
        '🔥 漢堡菜單超級簡單修復方案': '🔥 ハンバーガーメニュー超シンプル修正方法',
        
        # 功能页面相关
        '主要ContentSection': 'メインコンテンツセクション',
        '🎨 全新 Hero Section': '🎨 全く新しいHeroセクション',
        '动态Background装饰': '動的背景装飾',
        'Background裝飾': '背景装飾',
        '主Title': 'メインタイトル',
        '信任標籤（移到Title下方）': '信頼ラベル（タイトル下に移動）',
        '副Title': 'サブタイトル',
        'CTA button組（向move up10pt）': 'CTAボタングループ（10pt上に移動）',
        '關鍵數據': '重要データ',
        '🎨 核心function展示section': '🎨 コア機能ショーケースセクション',
        'function組1：Smart Invoice & Receipt Processing': '機能グループ1：スマートインボイス＆領収書処理',
        '模擬發票 - 茶餐廳（直接复制银行card代码, 只改内容）': 'モック請求書 - レストラン（銀行カードコードを直接コピー、内容のみ変更）',
        'AI 處理label': 'AI処理ラベル',
        'function組2：銀行月結單分析': '機能グループ2：銀行明細書分析',
        '模擬銀行對賬單圖示': 'モック銀行明細書イラスト',
        '價值main張card': '価値メインカード',
        
        # 通用词汇
        '個': '個',
        '張': '枚',
        '份': '件',
        '項': '項目',
        '頁': 'ページ',
        '次': '回',
        '秒': '秒',
        '分鐘': '分',
        '小時': '時間',
        '天': '日',
        '週': '週',
        '月': '月',
        '年': '年',
        
        # 按钮和动作
        '按鈕': 'ボタン',
        '點擊': 'クリック',
        '觸摸': 'タッチ',
        '滑動': 'スライド',
        '滾動': 'スクロール',
        '打開': '開く',
        '關閉': '閉じる',
        '顯示': '表示',
        '隱藏': '非表示',
        '開始': '開始',
        '完成': '完了',
        '成功': '成功',
        '失敗': '失敗',
        '錯誤': 'エラー',
        '警告': '警告',
    }
    
    print(f"🔄 处理 {len(comprehensive_translations)} 个翻译词组...")
    
    # 按长度排序，先替换长的
    sorted_translations = sorted(comprehensive_translations.items(), key=lambda x: len(x[0]), reverse=True)
    
    for chinese, japanese in sorted_translations:
        if japanese:
            content = content.replace(chinese, japanese)
    
    # 统计翻译后的中文字符数
    chinese_chars_after = len(re.findall(r'[一-龥]', content))
    
    print(f"\n📊 综合翻译进度:")
    print(f"  翻译前: {chinese_chars_before} 个中文字符")
    print(f"  翻译后: {chinese_chars_after} 个中文字符")
    print(f"  已翻译: {chinese_chars_before - chinese_chars_after} 个字符")
    print(f"  剩余: {chinese_chars_after} 个字符")
    
    # 保存文件
    print(f"\n💾 保存文件...")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # 计算总体完成度
    total_original = 4572
    completion_rate = ((total_original - chinese_chars_after) / total_original * 100)
    
    print(f"\n{'='*70}")
    print(f"📊 日文版首页翻译总结:")
    print(f"  原始中文字符: {total_original} 个")
    print(f"  剩余中文字符: {chinese_chars_after} 个")
    print(f"  翻译字符数: {total_original - chinese_chars_after} 个")
    print(f"  完成度: {completion_rate:.2f}%")
    print(f"{'='*70}")
    
    if chinese_chars_after <= 100:
        print(f"\n✅✅✅ 日文版首页翻译基本完成！")
    elif chinese_chars_after <= 500:
        print(f"\n✅✅ 日文版首页接近完成！")
    else:
        print(f"\n✅ 日文版首页大部分完成！")
    
    return chinese_chars_after

if __name__ == '__main__':
    remaining = fix_jp_index_comprehensive()
    print(f"\n下一步: {'继续修复韩文版首页' if remaining <= 500 else '需要继续翻译剩余内容'}")

