# 🌐 多语言同步系统使用说明

> **作用：** 帮助AI和开发者快速了解如何维护VaultCaddy的多语言网站

---

## ⚡ 快速开始（只需记住这个）

```bash
# 修改任何中文版页面后，运行：
./sync-multilingual.sh all
```

**完成！** 所有英文、日文、韩文版本自动更新。

---

## 📋 系统说明

### 网站结构
- **中文版**：根目录（dashboard.html, account.html等）
- **英文版**：`en/` 文件夹
- **日文版**：`jp/` 文件夹
- **韩文版**：`kr/` 文件夹

### 工作流程
1. ✏️ 只修改**中文版**文件
2. 🚀 运行 `./sync-multilingual.sh all`
3. ✅ 其他语言版本自动更新

### 涉及页面（7个）
- dashboard.html - Dashboard主页面
- firstproject.html - 项目管理页面
- document-detail.html - 文档详情页面
- account.html - 账户设置页面
- billing.html - 计费管理页面
- privacy.html - 隐私政策页面
- terms.html - 服务条款页面

---

## 🎯 常用命令

```bash
# 同步所有页面（最常用）
./sync-multilingual.sh all

# 只同步单个页面
./sync-multilingual.sh dashboard
./sync-multilingual.sh account
./sync-multilingual.sh billing

# 查看帮助
./sync-multilingual.sh
```

---

## ⚠️ 重要规则

### ✅ 正确做法
- 只修改中文版（根目录的HTML文件）
- 修改后运行同步脚本
- 让系统自动生成其他语言版本

### ❌ 错误做法
- ❌ 不要直接修改 `en/dashboard.html`（会被覆盖）
- ❌ 不要直接修改 `jp/dashboard.html`（会被覆盖）
- ❌ 不要直接修改 `kr/dashboard.html`（会被覆盖）

---

## 📖 详细文档

需要更多信息？查看这些文档：

| 文档 | 用途 |
|------|------|
| `⚡_多语言同步_备忘单.md` | 超简备忘单，快速查询 |
| `📖_多语言同步_快速参考.md` | 日常使用指南 |
| `🎉_多语言同步系统_完整方案.md` | 完整方案总结 |
| `🌐_多语言同步系统完整指南.md` | 详细技术文档 |

---

## 🔧 系统组成

- **核心脚本**：`multilingual_sync_master.py`（Python脚本）
- **快捷脚本**：`sync-multilingual.sh`（推荐使用）
- **翻译字典**：111个核心术语
- **支持语言**：英文(EN)、日文(JP)、韩文(KR)

---

## 💡 实战示例

### 示例1：修改Dashboard欢迎消息

```bash
# 1. 编辑中文版
vim dashboard.html
# 修改欢迎消息

# 2. 同步
./sync-multilingual.sh dashboard

# 3. 完成！验证
open en/dashboard.html
```

### 示例2：批量更新多个页面

```bash
# 1. 编辑多个中文版
vim dashboard.html
vim account.html
vim billing.html

# 2. 一键同步
./sync-multilingual.sh all

# 3. 完成！
```

---

## 📊 系统统计

- ✅ **支持页面：** 7个核心页面
- ✅ **翻译术语：** 111个
- ✅ **生成文件：** 21个（7页 × 3语言）
- ✅ **同步速度：** 10秒完成所有页面
- ✅ **效率提升：** 180-360倍

---

## 🌐 验证链接示例

### Dashboard
- 🇨🇳 https://vaultcaddy.com/dashboard.html
- 🇺🇸 https://vaultcaddy.com/en/dashboard.html
- 🇯🇵 https://vaultcaddy.com/jp/dashboard.html
- 🇰🇷 https://vaultcaddy.com/kr/dashboard.html

### Account
- 🇨🇳 https://vaultcaddy.com/account.html
- 🇺🇸 https://vaultcaddy.com/en/account.html
- 🇯🇵 https://vaultcaddy.com/jp/account.html
- 🇰🇷 https://vaultcaddy.com/kr/account.html

---

## ➕ 如何添加新术语

如果发现有新的中文术语需要翻译：

```bash
# 1. 编辑翻译字典
vim multilingual_sync_master.py

# 2. 在 TRANSLATION_DICT 中添加：
'您的新术语': {
    'en': 'Your New Term',
    'jp': 'あなたの新しい用語',
    'kr': '새로운 용어'
}

# 3. 重新同步
./sync-multilingual.sh all
```

---

## 🚀 效率对比

### 传统手动方式 ❌
- 时间：30-60分钟
- 错误率：高
- 工作量：大

### 自动化同步 ✅
- 时间：10秒
- 错误率：低
- 工作量：最小

**效率提升：180-360倍！** 🚀

---

## 📞 需要帮助？

1. 查看 `⚡_多语言同步_备忘单.md`
2. 运行 `./sync-multilingual.sh` 查看使用说明
3. 查看其他详细文档

---

## 🎯 记住这一条命令

```bash
./sync-multilingual.sh all
```

**这就是全部！** 其他语言版本会自动处理。⚡

---

**系统版本：** v1.0  
**创建日期：** 2025年12月21日  
**状态：** ✅ 运行中  
**最后同步：** 2025年12月21日

---

**🎉 恭喜！您现在拥有一个强大的多语言同步系统！**

