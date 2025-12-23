#!/usr/bin/env python3
"""
完整修复Dashboard和Firstproject的翻译问题

作用：
1. 在translations.js中添加缺失的dashboard相关翻译键
2. 修复dashboard.html中的混乱文本
3. 为关键元素添加data-translate属性
"""

import os
import re

# Dashboard相关的翻译键
DASHBOARD_TRANSLATIONS = {
    'en': {
        'dashboard_title': 'Dashboard',
        'create_project': 'Create',
        'create_new_project': 'Create New Project',
        'project_name': 'Project Name',
        'project_name_placeholder': 'Enter project name to create a new document project',
        'delete_project': 'Delete Project',
        'delete_project_confirm': 'Are you sure you want to delete folder',
        'delete_warning': 'This action cannot be undone. The folder and all its contents will be permanently deleted.',
        'delete_confirmation_prompt': 'Please enter the project name to confirm deletion',
        'yes': 'Yes',
        'no_projects_yet': 'No projects yet',
        'create_first_project': 'Create your first project to get started',
        'name': 'Name',
        'last_modified': 'Last modified',
        'created': 'Created',
        'actions': 'Actions',
        'upload_files': 'Upload files',
        'export': 'Export',
        'delete': 'Delete',
    },
    'zh-TW': {
        'dashboard_title': '儀表板',
        'create_project': '創建',
        'create_new_project': '創建新項目',
        'project_name': '項目名稱',
        'project_name_placeholder': '輸入項目名稱以創建新的文檔項目',
        'delete_project': '刪除項目',
        'delete_project_confirm': '您確定要刪除文件夾',
        'delete_warning': '刪除後無法復原文件夾及當中內容。',
        'delete_confirmation_prompt': '請輸入項目名稱以確認刪除',
        'yes': '是',
        'no_projects_yet': '暫無項目',
        'create_first_project': '創建您的第一個項目以開始',
        'name': '名稱',
        'last_modified': '最後修改',
        'created': '創建時間',
        'actions': '操作',
        'upload_files': '上傳文件',
        'export': '導出',
        'delete': '刪除',
    },
    'ja': {
        'dashboard_title': 'ダッシュボード',
        'create_project': '作成',
        'create_new_project': '新しいプロジェクトを作成',
        'project_name': 'プロジェクト名',
        'project_name_placeholder': 'プロジェクト名を入力して新しいドキュメントプロジェクトを作成',
        'delete_project': 'プロジェクトを削除',
        'delete_project_confirm': 'フォルダを削除してもよろしいですか',
        'delete_warning': '削除後は復元できません。フォルダとその中のすべてのコンテンツが完全に削除されます。',
        'delete_confirmation_prompt': '削除を確認するには、プロジェクト名を入力してください',
        'yes': 'はい',
        'no_projects_yet': 'プロジェクトはまだありません',
        'create_first_project': '最初のプロジェクトを作成して始めましょう',
        'name': '名前',
        'last_modified': '最終更新',
        'created': '作成日',
        'actions': '操作',
        'upload_files': 'ファイルをアップロード',
        'export': 'エクスポート',
        'delete': '削除',
    },
    'ko': {
        'dashboard_title': '대시보드',
        'create_project': '생성',
        'create_new_project': '새 프로젝트 생성',
        'project_name': '프로젝트 이름',
        'project_name_placeholder': '프로젝트 이름을 입력하여 새 문서 프로젝트 생성',
        'delete_project': '프로젝트 삭제',
        'delete_project_confirm': '폴더를 삭제하시겠습니까',
        'delete_warning': '삭제 후 복원할 수 없습니다. 폴더 및 모든 내용이 영구적으로 삭제됩니다.',
        'delete_confirmation_prompt': '삭제를 확인하려면 프로젝트 이름을 입력하세요',
        'yes': '예',
        'no_projects_yet': '프로젝트가 아직 없습니다',
        'create_first_project': '첫 번째 프로젝트를 만들어 시작하세요',
        'name': '이름',
        'last_modified': '마지막 수정',
        'created': '생성됨',
        'actions': '작업',
        'upload_files': '파일 업로드',
        'export': '내보내기',
        'delete': '삭제',
    }
}

def add_translations_to_js(file_path):
    """在translations.js中添加dashboard翻译键"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 为每个语言添加翻译键
        for lang_code, translations in DASHBOARD_TRANSLATIONS.items():
            # 找到该语言的TRANSLATIONS对象
            pattern = rf"('{lang_code}':\s*\{{[^}}]*?)(\s*\}})"
            
            # 检查是否已经存在dashboard_title
            if f"'dashboard_title':" in content and lang_code in content:
                print(f"  ⏭️  {lang_code}: 翻译键已存在")
                continue
            
            # 构建要添加的翻译文本
            trans_lines = []
            for key, value in translations.items():
                # 转义单引号
                escaped_value = value.replace("'", "\\'")
                trans_lines.append(f"        '{key}': '{escaped_value}'")
            
            trans_text = ',\n' + ',\n'.join(trans_lines)
            
            # 在语言对象的最后一个属性后添加（在closing brace之前）
            def replacer(match):
                return match.group(1) + trans_text + match.group(2)
            
            content = re.sub(pattern, replacer, content, count=1, flags=re.DOTALL)
            print(f"  ✅ {lang_code}: 已添加 {len(translations)} 个翻译键")
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
        
    except Exception as e:
        print(f"  ❌ 错误: {e}")
        return False

def fix_dashboard_html(file_path, lang_code):
    """修复dashboard.html中的混乱文本并添加data-translate"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 1. 修复"Create New Project"标题
        content = re.sub(
            r'<h2>Create New Project</h2>',
            '<h2 data-translate="create_new_project">Create New Project</h2>',
            content
        )
        
        # 2. 修复"Project Name"标签
        content = re.sub(
            r'<label class="form-label" for="projectName">Project Name</label>',
            '<label class="form-label" for="projectName" data-translate="project_name">Project Name</label>',
            content
        )
        
        # 3. 修复混乱的"DeleteProject"标题
        content = re.sub(
            r'<h2[^>]*>DeleteProject</h2>',
            '<h2 style="font-size: 1.25rem; font-weight: 600; color: #1f2937; margin: 0 0 0.5rem 0;" data-translate="delete_project">Delete Project</h2>',
            content
        )
        
        # 4. 修复混乱的删除确认文本
        messy_text_pattern = r'YesNoDeleteFile夾.*?WhenmiddleContent。'
        if re.search(messy_text_pattern, content, re.DOTALL):
            # 替换整个混乱的段落
            replacement = '''<span data-translate="delete_project_confirm">Are you sure you want to delete folder</span> '<span id="deleteProjectName" style="font-weight: 600; color: #1f2937;"></span>'？<br>
                        <span data-translate="delete_warning">This action cannot be undone. The folder and all its contents will be permanently deleted.</span>'''
            
            content = re.sub(
                r'YesNoDeleteFile夾[^<]*<span id="deleteProjectName"[^>]*></span>[^<]*<br>\s*DeletebackNonecannot restoreFile夾及WhenmiddleContent。',
                replacement,
                content
            )
        
        # 5. 修复"Please enter Project Name"提示
        content = re.sub(
            r'Please enterProjectNametoConfirmDelete',
            '<span data-translate="delete_confirmation_prompt">Please enter the project name to confirm deletion</span>',
            content
        )
        
        # 6. 修复按钮文本
        content = re.sub(
            r'(<button[^>]*onclick="closeCreateProjectModal\(\)"[^>]*>)\s*Cancel\s*(</button>)',
            r'\1<span data-translate="cancel">Cancel</span>\2',
            content
        )
        
        content = re.sub(
            r'(<button[^>]*onclick="createProjectFromModal\(\)"[^>]*>)\s*Create\s*(</button>)',
            r'\1<span data-translate="create_project">Create</span>\2',
            content
        )
        
        content = re.sub(
            r'(<button[^>]*onclick="closeDeleteProjectModal\(\)"[^>]*>)\s*Cancel\s*(</button>)',
            r'\1<span data-translate="cancel">Cancel</span>\2',
            content
        )
        
        content = re.sub(
            r'(<button[^>]*id="confirmDeleteBtn"[^>]*>)\s*Yes\s*(</button>)',
            r'\1<span data-translate="yes">Yes</span>\2',
            content
        )
        
        # 只在有实际修改时才写回
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"  ❌ 错误: {e}")
        return False

def main():
    print("🔧 开始完整修复Dashboard翻译问题...")
    print("=" * 60)
    
    # 第一步：添加翻译键到translations.js
    print("\n📝 步骤1: 添加翻译键到translations.js")
    print("-" * 60)
    
    if os.path.exists('translations.js'):
        add_translations_to_js('translations.js')
    else:
        print("  ❌ translations.js 不存在")
    
    # 第二步：修复dashboard.html文件
    print("\n📝 步骤2: 修复dashboard.html文件")
    print("-" * 60)
    
    files_to_fix = [
        ('dashboard.html', ''),
        ('en/dashboard.html', 'en'),
        ('jp/dashboard.html', 'jp'),
        ('kr/dashboard.html', 'kr'),
    ]
    
    fixed_count = 0
    
    for file_path, lang_code in files_to_fix:
        if not os.path.exists(file_path):
            print(f"⏭️  跳过: {file_path} (不存在)")
            continue
        
        print(f"\n📄 处理: {file_path}")
        
        was_fixed = fix_dashboard_html(file_path, lang_code)
        
        if was_fixed:
            print(f"   ✅ 已修复混乱文本并添加data-translate属性")
            fixed_count += 1
        else:
            print(f"   ⏭️  无需修改")
    
    # 总结
    print(f"\n\n{'=' * 60}")
    print(f"📊 修复完成")
    print(f"{'=' * 60}")
    print(f"✅ translations.js: 已添加dashboard翻译键")
    print(f"✅ 修复的dashboard.html文件: {fixed_count}/4")
    print(f"{'=' * 60}")
    
    print(f"\n💡 下一步:")
    print(f"1. 测试各语言版本: https://vaultcaddy.com/en/dashboard.html")
    print(f"2. 检查删除对话框是否正确显示")
    print(f"3. 测试手机版响应式设计")
    print(f"\n🔍 已知问题:")
    print(f"- Firstproject页面还需要类似的修复")
    print(f"- 某些动态生成的文本可能需要在JS中处理")

if __name__ == '__main__':
    main()

