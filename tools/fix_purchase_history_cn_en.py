#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复 Purchase History 加载问题
只修复中文版和英文版（日文版和韩文版正常，不修改）

问题：重复查询 Firebase 导致页面卡住
解决：移除 await loadMonthOptions() 调用，改为从查询结果生成月份选项
"""

import re
import os

def fix_account_file(file_path, lang='zh'):
    """修复 account.html 文件"""
    print(f"\n{'='*70}")
    print(f"🔧 正在修复: {file_path}")
    print(f"{'='*70}")
    
    # 读取文件
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # 语言相关文本
    lang_texts = {
        'zh': {
            'loading_timeout': '⏱️ 加载超时，请检查网络连接',
            'retry': '重试',
            'loading_history': '🔄 开始加载购买历史...',
            'query_complete': '✅ 查询完成，记录数量:',
            'clear_timeout': '✅ 清除超时',
            'generate_options': '✅ 从查询结果生成月份选项',
            'load_failed': '❌ 载入 Credits 历史记录失败:',
            'error_details': '错误详情:',
            'generated_months': '✅ 生成了',
            'months_options': '个月份选项',
            'timeout_warning': '⚠️ 加载超时',
            'comment_removed': '✅ 移除了 await loadMonthOptions() 调用',
            'comment_new': '✅ 改为在查询后从数据中生成月份选项'
        },
        'en': {
            'loading_timeout': '⏱️ Loading timeout, please check network',
            'retry': 'Retry',
            'loading_history': '🔄 Loading purchase history...',
            'query_complete': '✅ Query complete, record count:',
            'clear_timeout': '✅ Clear timeout',
            'generate_options': '✅ Generate month options from query results',
            'load_failed': '❌ Load Credits history failed:',
            'error_details': 'Error details:',
            'generated_months': '✅ Generated',
            'months_options': 'month options',
            'timeout_warning': '⚠️ Loading timeout',
            'comment_removed': '✅ Removed await loadMonthOptions() call',
            'comment_new': '✅ Generate month options from query results instead'
        }
    }
    
    texts = lang_texts[lang]
    
    # 步骤1: 添加新的辅助函数 generateMonthOptionsFromSnapshot
    # 在 loadCreditsHistory 函数之前插入
    helper_function = f'''
        // ✅ 从查询结果生成月份选项（避免重复查询 Firebase）
        function generateMonthOptionsFromSnapshot(historySnapshot) {{
            const select = document.getElementById('history-month-filter');
            if (!select || historySnapshot.empty) {{
                return;
            }}
            
            const months = new Set();
            historySnapshot.forEach(doc => {{
                const record = doc.data();
                if (record.createdAt) {{
                    const date = record.createdAt.toDate();
                    const yearMonth = `${{date.getFullYear()}}-${{String(date.getMonth() + 1).padStart(2, '0')}}`;
                    months.add(yearMonth);
                }}
            }});
            
            const sortedMonths = Array.from(months).sort((a, b) => b.localeCompare(a));
            const currentValue = select.value;
            
            // 保留第一个选项
            const firstOption = select.options[0];
            if (!firstOption) return;
            
            select.innerHTML = '';
            select.appendChild(firstOption.cloneNode(true));
            
            sortedMonths.forEach(yearMonth => {{
                const [year, month] = yearMonth.split('-');
                const option = document.createElement('option');
                option.value = yearMonth;
                option.textContent = `${{parseInt(month)}}/${{year}}`;
                select.appendChild(option);
            }});
            
            if (sortedMonths.includes(currentValue)) {{
                select.value = currentValue;
            }}
            
            console.log(`{texts['generated_months']} ${{sortedMonths.length}} {texts['months_options']}`);
        }}
        
'''
    
    # 查找 async function loadCreditsHistory() 的位置
    pattern = r'([ \t]*)(async function loadCreditsHistory\(\) \{)'
    match = re.search(pattern, content)
    
    if match:
        indent = match.group(1)
        # 在函数定义前插入辅助函数
        insert_pos = match.start()
        content = content[:insert_pos] + helper_function + content[insert_pos:]
        print("✅ 已添加 generateMonthOptionsFromSnapshot() 辅助函数")
    else:
        print("❌ 未找到 loadCreditsHistory 函数定义")
        return False
    
    # 步骤2: 修改 loadCreditsHistory 函数的开始部分
    # 移除 await loadMonthOptions() 调用，添加超时保护
    old_start_pattern = r'''(async function loadCreditsHistory\(\) \{)
            const tbody = document\.getElementById\('credits-history-tbody'\);
            const filter = document\.getElementById\('history-month-filter'\)\.value;
            
            // [^\\n]+
            await loadMonthOptions\(\);
            
            try \{'''
    
    new_start = f'''\\1
            console.log('{texts['loading_history']}');
            const tbody = document.getElementById('credits-history-tbody');
            const filter = document.getElementById('history-month-filter').value;
            
            // {texts['comment_removed']}
            // {texts['comment_new']}
            
            // ✅ 添加超时保护
            const timeoutId = setTimeout(() => {{
                console.warn('{texts['timeout_warning']}');
                tbody.innerHTML = `
                    <tr>
                        <td colspan="3" style="text-align: center; padding: 2rem; color: #f59e0b;">
                            {texts['loading_timeout']}
                            <br>
                            <button onclick="loadCreditsHistory()" 
                                    style="margin-top: 1rem; padding: 0.5rem 1rem; 
                                           background: #3b82f6; color: white; 
                                           border: none; border-radius: 6px; 
                                           cursor: pointer;">
                                {texts['retry']}
                            </button>
                        </td>
                    </tr>
                `;
            }}, 10000); // 10秒超时
            
            try {{'''
    
    content = re.sub(old_start_pattern, new_start, content, flags=re.MULTILINE)
    print("✅ 已修改函数开始部分：移除 await loadMonthOptions()，添加超时保护")
    
    # 步骤3: 在查询后添加调用 generateMonthOptionsFromSnapshot
    old_query_pattern = r'(const historySnapshot = await query\.limit\(50\)\.get\(\);)'
    new_query = f'''\\1
                console.log('{texts['query_complete']}', historySnapshot.size);
                
                // {texts['clear_timeout']}
                clearTimeout(timeoutId);
                
                // {texts['generate_options']}
                generateMonthOptionsFromSnapshot(historySnapshot);'''
    
    content = re.sub(old_query_pattern, new_query, content)
    print("✅ 已在查询后添加 generateMonthOptionsFromSnapshot() 调用")
    
    # 步骤4: 在 catch 块开始添加 clearTimeout
    old_catch_pattern = r'(\} catch \(error\) \{[\s\n]*)(console\.error\([\'"])'
    new_catch = f'''\\1                clearTimeout(timeoutId); // {texts['clear_timeout']}
                \\2'''
    
    content = re.sub(old_catch_pattern, new_catch, content)
    print("✅ 已在 catch 块添加 clearTimeout()")
    
    # 步骤5: 增强错误日志
    old_error_log = r"console\.error\('([^']*载入|[^']*Load)[^']*历史记录失败[^']*:', error\);"
    new_error_log = f"console.error('{texts['load_failed']}', error);\n                console.error('{texts['error_details']}', error.message, error.code);"
    
    content = re.sub(old_error_log, new_error_log, content)
    print("✅ 已增强错误日志")
    
    # 检查是否有修改
    if content == original_content:
        print("⚠️ 警告：文件内容未发生变化，可能已经修复过或模式不匹配")
        return False
    
    # 备份原文件
    backup_path = file_path + '.backup_before_purchase_history_fix'
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(original_content)
    print(f"✅ 已备份原文件到: {backup_path}")
    
    # 写入修改后的内容
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 修复完成: {file_path}")
    return True


def main():
    """主函数"""
    print("╔" + "="*68 + "╗")
    print("║" + " "*15 + "Purchase History 修复脚本" + " "*28 + "║")
    print("╚" + "="*68 + "╝")
    print()
    print("📋 修复范围：")
    print("   ✅ account.html（中文版）")
    print("   ✅ en/account.html（英文版）")
    print("   ⏭️  jp/account.html（日文版 - 跳过，已正常）")
    print("   ⏭️  kr/account.html（韩文版 - 跳过，已正常）")
    print()
    
    # 获取脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 要修复的文件列表
    files_to_fix = [
        ('account.html', 'zh'),           # 中文版
        ('en/account.html', 'en')          # 英文版
    ]
    
    success_count = 0
    total_count = len(files_to_fix)
    
    for file_rel_path, lang in files_to_fix:
        file_path = os.path.join(script_dir, file_rel_path)
        
        if not os.path.exists(file_path):
            print(f"❌ 文件不存在: {file_path}")
            continue
        
        try:
            if fix_account_file(file_path, lang):
                success_count += 1
        except Exception as e:
            print(f"❌ 修复失败: {file_path}")
            print(f"   错误: {str(e)}")
            import traceback
            traceback.print_exc()
    
    # 输出总结
    print("\n" + "="*70)
    print("📊 修复总结")
    print("="*70)
    print(f"✅ 成功修复: {success_count}/{total_count} 个文件")
    
    if success_count == total_count:
        print("\n🎉 所有文件修复成功！")
        print("\n📝 下一步：")
        print("   1. 上传修改后的文件到服务器：")
        print("      • account.html")
        print("      • en/account.html")
        print("   2. 清除浏览器缓存（Ctrl+Shift+R 或 Cmd+Shift+R）")
        print("   3. 测试所有4个版本的 Purchase History 加载")
        print("\n✅ 预期效果：")
        print("   • 所有4个版本都能成功加载")
        print("   • 不再卡在 'Loading...' 状态")
        print("   • 10秒超时保护")
        print("   • 详细的Console日志")
    else:
        print("\n⚠️ 部分文件修复失败，请检查错误信息")
    
    print()


if __name__ == '__main__':
    main()

