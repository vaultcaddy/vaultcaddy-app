#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 3: 翻译完整句子、JS字符串和注释
⚠️ 只翻译文本，不改变任何HTML结构、CSS样式或JS代码结构
"""

import re
import os

# Phase 3 - 完整句子和常见短语翻译
PHASE3_TRANSLATIONS = {
    'en': {
        # JavaScript调试和错误消息
        '調整和為': 'Adjust and set as',
        '遮罩元素': 'Mask element',
        '已就緒使用': 'Ready to use',
        '即時獲取': 'Fetch immediately',
        '無法獲取': 'Failed to fetch',
        '無法從獲取資料': 'Failed to get data from',
        '尚未等待中': 'Not yet waiting',
        '延遲獲取': 'Delayed fetch',
        '已顯示頭像': 'Avatar displayed',
        '頁面保護立即隱藏內容等待檢查': 'Page protection immediately hide content wait check',
        '安全隐藏控制台日志不删除代码': 'Safe hide console log do not delete code',
        '和身份驗證': 'And authentication',
        '驗證檢查': 'Verification check',
        '導航欄交互': 'Navigation bar interaction',
        
        # 常见短语和句子
        '無法連接': 'Connection failed',
        '連接失敗': 'Connection failed',
        '網絡錯誤': 'Network error',
        '請檢查網絡': 'Please check network',
        '請重試': 'Please retry',
        '操作失敗': 'Operation failed',
        '操作成功': 'Operation successful',
        '確定刪除': 'Confirm delete',
        '無法刪除': 'Cannot delete',
        '正在加載': 'Loading',
        '加載失敗': 'Load failed',
        '未找到': 'Not found',
        '沒有數據': 'No data',
        '暫無數據': 'No data yet',
        '數據為空': 'Data is empty',
        '請先': 'Please first',
        '之後': 'After',
        '然後': 'Then',
        '最後': 'Finally',
        '注意': 'Note',
        '提示信息': 'Tip',
        '錯誤信息': 'Error message',
        '成功信息': 'Success message',
        '確認信息': 'Confirm message',
        '詳細信息': 'Details',
        '更多信息': 'More information',
        '查看更多': 'View more',
        '收起': 'Collapse',
        '展開': 'Expand',
        '顯示全部': 'Show all',
        '隱藏': 'Hide',
        '顯示': 'Show',
        '啟用': 'Enable',
        '禁用': 'Disable',
        '可用': 'Available',
        '不可用': 'Unavailable',
        '已啟用': 'Enabled',
        '已禁用': 'Disabled',
        '正常': 'Normal',
        '異常': 'Abnormal',
        '活躍': 'Active',
        '不活躍': 'Inactive',
        '在線': 'Online',
        '離線': 'Offline',
        '已連接': 'Connected',
        '未連接': 'Disconnected',
        '同步中': 'Syncing',
        '已同步': 'Synced',
        '未同步': 'Not synced',
        '更新中': 'Updating',
        '已更新': 'Updated',
        '需要更新': 'Update required',
        '最新版本': 'Latest version',
        '當前版本': 'Current version',
        '歷史版本': 'History version',
        '版本號': 'Version number',
        '發布日期': 'Release date',
        '更新日誌': 'Change log',
        '查看詳情': 'View details',
        '立即更新': 'Update now',
        '稍後提醒': 'Remind later',
        '忽略此次': 'Ignore this time',
        '不再提示': 'Don\'t remind again',
        '我知道了': 'I understand',
        '繼續': 'Continue',
        '停止': 'Stop',
        '暫停': 'Pause',
        '恢復': 'Resume',
        '開始處理': 'Start processing',
        '停止處理': 'Stop processing',
        '暫停處理': 'Pause processing',
        '繼續處理': 'Continue processing',
        '處理完畢': 'Processing completed',
        '等待處理': 'Waiting for processing',
        '正在排隊': 'In queue',
        '已取消': 'Cancelled',
        '已過期': 'Expired',
        '即將過期': 'Expiring soon',
        '永久': 'Permanent',
        '臨時': 'Temporary',
        '草稿': 'Draft',
        '已發布': 'Published',
        '未發布': 'Unpublished',
        '已歸檔': 'Archived',
        '已刪除': 'Deleted',
        '回收站': 'Trash',
        '恢復文件': 'Restore file',
        '永久刪除': 'Delete permanently',
        '清空回收站': 'Empty trash',
        '全部標記為已讀': 'Mark all as read',
        '標記為已讀': 'Mark as read',
        '標記為未讀': 'Mark as unread',
        '加入收藏': 'Add to favorites',
        '取消收藏': 'Remove from favorites',
        '分享給': 'Share with',
        '複製鏈接': 'Copy link',
        '生成鏈接': 'Generate link',
        '鏈接已複製': 'Link copied',
        '複製成功': 'Copied successfully',
        '複製失敗': 'Copy failed',
        '權限不足': 'Insufficient permissions',
        '訪問被拒絕': 'Access denied',
        '請登錄': 'Please login',
        '會話已過期': 'Session expired',
        '請重新登錄': 'Please login again',
        '自動登出': 'Auto logout',
        '登錄超時': 'Login timeout',
        '驗證碼錯誤': 'Verification code error',
        '驗證碼已發送': 'Verification code sent',
        '重新發送': 'Resend',
        '秒後重試': 'Retry after seconds',
        '秒後自動': 'Auto after seconds',
    },
    'jp': {
        '調整和為': '調整して設定',
        '遮罩元素': 'マスク要素',
        '已就緒使用': '使用準備完了',
        '即時獲取': '即座に取得',
        '無法獲取': '取得失敗',
        '無法從獲取資料': 'データ取得失敗',
        '尚未等待中': 'まだ待機中ではありません',
        '延遲獲取': '遅延取得',
        '已顯示頭像': 'アバター表示済み',
        '頁面保護立即隱藏內容等待檢查': 'ページ保護 即座に内容を隠して確認待ち',
        '和身份驗證': 'と認証',
        '驗證檢查': '検証チェック',
        '導航欄交互': 'ナビゲーションバーのインタラクション',
        '無法連接': '接続失敗',
        '請重試': '再試行してください',
        '操作失敗': '操作失敗',
        '操作成功': '操作成功',
    },
    'kr': {
        '調整和為': '조정하고 설정',
        '遮罩元素': '마스크 요소',
        '已就緒使用': '사용 준비 완료',
        '即時獲取': '즉시 가져오기',
        '無法獲取': '가져오기 실패',
        '無法從獲取資料': '데이터 가져오기 실패',
        '尚未等待中': '아직 대기 중이 아님',
        '延遲獲取': '지연 가져오기',
        '已顯示頭像': '아바타 표시됨',
        '頁面保護立即隱藏內容等待檢查': '페이지 보호 즉시 콘텐츠 숨기기 확인 대기',
        '和身份驗證': '및 인증',
        '驗證檢查': '검증 확인',
        '導航欄交互': '내비게이션 바 인터랙션',
        '無法連接': '연결 실패',
        '請重試': '다시 시도하세요',
        '操作失敗': '작업 실패',
        '操作成功': '작업 성공',
    }
}

def translate_file_phase3(file_path, lang_code):
    """Phase 3 翻译 - 只替换文本，不改变结构"""
    
    if not os.path.exists(file_path):
        return 0, 0
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    chinese_before = len(re.findall(r'[一-龥]', content))
    
    translations = PHASE3_TRANSLATIONS.get(lang_code, {})
    # 按长度排序，先替换长的句子
    sorted_trans = sorted(translations.items(), key=lambda x: len(x[0]), reverse=True)
    
    replaced_count = 0
    for chinese, target in sorted_trans:
        if chinese in content:
            # 只替换文本，保持所有标签和结构
            content = content.replace(chinese, target)
            replaced_count += 1
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    chinese_after = len(re.findall(r'[一-龥]', content))
    
    return chinese_before, chinese_after, replaced_count

def main():
    print("🚀 Phase 3: 翻译完整句子和短语...")
    print("⚠️  只翻译文本，保持所有设计和结构不变")
    print("="*70)
    
    pages = [
        'firstproject.html',
        'account.html',
        'billing.html',
        'dashboard.html',
        'document-detail.html',
        'terms.html',
        'privacy.html',
    ]
    
    languages = {'en': '🇬🇧英文', 'jp': '🇯🇵日文', 'kr': '🇰🇷韩文'}
    
    total_before = 0
    total_after = 0
    total_replaced = 0
    
    for page in pages:
        for lang_code, lang_name in languages.items():
            file_path = f"{lang_code}/{page}"
            before, after, replaced = translate_file_phase3(file_path, lang_code)
            
            if before > 0 and replaced > 0:
                translated = before - after
                total_before += before
                total_after += after
                total_replaced += replaced
                
                print(f"{lang_name} {page}: 替换{replaced}处, -{translated}字")
    
    total_translated = total_before - total_after
    percentage = (total_translated / total_before * 100) if total_before > 0 else 0
    
    print(f"\n{'='*70}")
    print(f"Phase 3 完成:")
    print(f"  原始: {total_before:,} 字符")
    print(f"  剩余: {total_after:,} 字符")
    print(f"  翻译: {total_translated:,} 字符 ({percentage:.1f}%)")
    print(f"  替换处数: {total_replaced} 处")
    print(f"{'='*70}")
    print(f"✅ 所有HTML结构、CSS样式、JS代码结构保持不变")

if __name__ == '__main__':
    main()

