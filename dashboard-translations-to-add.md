# Dashboard & Firstproject 需要添加的翻译键

## 需要添加到 translations.js 的翻译键

### Dashboard 页面

```javascript
// 英文 (en)
'dashboard_title': 'Dashboard',
'create_project': 'Create',
'create_new_project': 'Create New Project',
'project_name': 'Project Name',
'project_name_placeholder': 'Enter project name',
'cancel': 'Cancel',  // 已存在
'create': 'Create',
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

// 繁体中文 (zh-TW)
'dashboard_title': '儀表板',
'create_project': '創建',
'create_new_project': '創建新項目',
'project_name': '項目名稱',
'project_name_placeholder': '輸入項目名稱',
'cancel': '取消',  // 已存在
'create': '創建',
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

// 日文 (ja)
'dashboard_title': 'ダッシュボード',
'create_project': '作成',
'create_new_project': '新しいプロジェクトを作成',
'project_name': 'プロジェクト名',
'project_name_placeholder': 'プロジェクト名を入力',
'cancel': 'キャンセル',  // 已存在
'create': '作成',
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

// 韩文 (ko)
'dashboard_title': '대시보드',
'create_project': '생성',
'create_new_project': '새 프로젝트 생성',
'project_name': '프로젝트 이름',
'project_name_placeholder': '프로젝트 이름 입력',
'cancel': '취소',  // 已存在
'create': '생성',
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
```

### Firstproject 页面

```javascript
// 英文 (en)
'select_document_type': 'Select Document Type',
'bank_statement': 'Bank Statement',
'bank_statement_desc': 'Convert bank statements to Excel and CSV format',
'invoice': 'Invoice',
'invoice_desc': 'Extract number, date, project details, price and supplier information',
'drag_drop_files': 'Drag and drop files here or click to upload',
'file_format_support': 'Supports PDF, JPG, PNG formats (Max 10MB) | ✨ Batch upload supported',
'file_upload': 'File Upload',
'ai_analysis': 'AI Analysis',
'data_extraction': 'Data Extraction',
'cloud_storage': 'Cloud Storage',
'processing_progress': 'Processing Progress',
'upload_files': 'Upload files',
'export': 'Export',
'delete': 'Delete',
'date_filter': 'Date Filter',
'date_range': 'Date Range',
'upload_date_range': 'Upload Date Range',
'clear_filter': 'Clear Filter',
'document_name': 'Document Name',
'type': 'Type',
'status': 'Status',
'supplier_source_bank': 'Supplier/Source/Bank',
'amount': 'Amount',
'date': 'Date',
'upload_date': 'Upload Date',
'no_results': 'No results.',
'total_invoices': 'Total',
'invoices': 'invoices',
'rows_per_page': 'Rows per page',
'page': 'Page',
'of': 'of',

// 其他语言类似...
```

## 需要修改的HTML文件

### dashboard.html (所有语言版本)

需要为以下元素添加 `data-translate` 属性：

1. **Modal标题**
   ```html
   <h2 data-translate="create_new_project">Create New Project</h2>
   ```

2. **表单标签**
   ```html
   <label class="form-label" for="projectName" data-translate="project_name">Project Name</label>
   ```

3. **按钮文本**
   ```html
   <button data-translate="cancel">Cancel</button>
   <button data-translate="create">Create</button>
   ```

4. **删除确认对话框**
   ```html
   <h2 data-translate="delete_project">Delete Project</h2>
   <p><span data-translate="delete_project_confirm">Are you sure you want to delete folder</span> '<span id="deleteProjectName"></span>'？</p>
   <p data-translate="delete_warning">This action cannot be undone...</p>
   ```

5. **表格列标题**
   ```html
   <th data-translate="name">Name</th>
   <th data-translate="last_modified">Last modified</th>
   <th data-translate="created">Created</th>
   <th data-translate="actions">Actions</th>
   ```

6. **空状态提示**
   ```html
   <td colspan="4">
     <span data-translate="no_projects_yet">No projects yet</span>
     <span data-translate="create_first_project">Create your first project to get started</span>
   </td>
   ```

### firstproject.html (所有语言版本)

需要为所有界面文本添加 `data-translate` 属性。

## 执行步骤

1. **第一步**：在 translations.js 中添加所有翻译键
2. **第二步**：修改 dashboard.html 和 firstproject.html，为文本添加 data-translate 属性
3. **第三步**：清理混乱的文本（如"YesNoDeleteFile夾"）
4. **第四步**：测试所有语言版本

## 当前问题示例

从网页内容看到的混乱文本：

```html
<!-- ❌ 错误 -->
<h2>DeleteProject</h2>
<p>YesNoDeleteFile夾 ''？<br>DeletebackNonecannot restoreFile夾及WhenmiddleContent。</p>

<!-- ✅ 正确 -->
<h2 data-translate="delete_project">Delete Project</h2>
<p>
  <span data-translate="delete_project_confirm">Are you sure you want to delete folder</span> 
  '<span id="deleteProjectName"></span>'？<br>
  <span data-translate="delete_warning">This action cannot be undone. The folder and all its contents will be permanently deleted.</span>
</p>
```

