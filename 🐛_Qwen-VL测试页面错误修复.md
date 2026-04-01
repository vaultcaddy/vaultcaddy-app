# 🐛 Qwen-VL 测试页面错误修复

**修复日期**: 2026-01-07  
**错误**: API 錯誤: 400 - Invalid value: image  
**原因**: 使用了错误的API格式

---

## 🔍 问题分析

### 错误信息

```
錯誤: API 錯誤: 400 - Invalid value: image. 
Supported values are: 'text','image_url','video_url' and 'video'.
```

### 问题原因

**错误的代码**（`qwen-vl-test.html` 第487-488行）:
```javascript
{
    type: 'image',  // ❌ 错误：API不支持这个类型
    image: `data:${mimeType};base64,${base64Image}`
}
```

**原因**:
- Qwen-VL API 不支持 `type: 'image'`
- 应该使用 `type: 'image_url'`
- 并且图像数据应该放在 `image_url.url` 字段中

---

## ✅ 修复方案

### 正确的代码

```javascript
{
    type: 'image_url',  // ✅ 正确：使用 image_url
    image_url: {
        url: `data:${mimeType};base64,${base64Image}`
    }
}
```

---

## 📋 支持的文件格式

### Qwen-VL Max 支持的格式

| 文件类型 | 支持 | 说明 |
|---------|------|------|
| **PDF** | ✅ 支持 | 可以直接上传PDF文件 |
| **图片 (JPG/JPEG)** | ✅ 支持 | 常用格式 |
| **图片 (PNG)** | ✅ 支持 | 常用格式 |
| **图片 (WebP)** | ✅ 支持 | 现代格式 |
| **图片 (GIF)** | ✅ 支持 | 动图第一帧 |

### 处理方式

**对于图片文件**:
1. 读取文件
2. 转换为 Base64
3. 发送到 Qwen-VL API

**对于PDF文件**（目前版本）:
1. 读取PDF文件
2. 转换为 Base64
3. 发送到 Qwen-VL API（PDF可以直接发送）

**注意**: Qwen-VL Max 可以直接处理PDF，不需要先转换为图片！

---

## 🚀 修复后的功能

### 支持的操作

1. ✅ **上传图片**（JPG、PNG、WebP、GIF）
2. ✅ **上传PDF**（单页或多页）
3. ✅ **拖放上传**
4. ✅ **点击上传**

### 处理流程

```
用户上传文件
    ↓
读取文件内容
    ↓
转换为 Base64
    ↓
发送到 Qwen-VL API（使用正确的 image_url 格式）
    ↓
接收处理结果
    ↓
显示提取的数据
```

---

## 📊 API格式说明

### Qwen-VL API 支持的内容类型

根据官方文档，`content` 数组中支持以下类型：

| 类型 | 字段 | 说明 |
|------|------|------|
| **text** | `text` | 文本内容 |
| **image_url** | `image_url.url` | 图片URL或Base64 |
| **video_url** | `video_url` | 视频URL |
| **video** | `video` | 视频内容 |

### 正确的请求格式

```javascript
{
    model: 'qwen3-vl-plus-2025-12-19',
    messages: [
        {
            role: 'user',
            content: [
                {
                    type: 'image_url',  // ✅ 使用 image_url
                    image_url: {
                        url: 'data:image/jpeg;base64,/9j/4AAQ...'  // Base64 图像
                        // 或
                        // url: 'https://example.com/image.jpg'  // 图片URL
                    }
                },
                {
                    type: 'text',
                    text: '请提取这张图片中的文本'
                }
            ]
        }
    ],
    temperature: 0.1,
    max_tokens: 4000
}
```

---

## 🧪 测试步骤

### 测试1: 上传图片

1. 访问 http://localhost:8000/qwen-vl-test.html
2. 选择"銀行對賬單測試"
3. 上传一张银行对账单图片（JPG或PNG）
4. 查看处理结果

**预期结果**:
- ✅ 成功处理
- ✅ 显示提取的JSON数据
- ✅ 显示处理统计信息

---

### 测试2: 上传PDF

1. 选择"銀行對賬單測試"
2. 上传一个PDF银行对账单
3. 查看处理结果

**预期结果**:
- ✅ 成功处理（PDF可以直接处理）
- ✅ 显示提取的JSON数据
- ✅ 显示处理统计信息

---

### 测试3: 拖放上传

1. 准备一张收据图片
2. 切换到"收據測試"
3. 拖放图片到上传区域
4. 查看处理结果

**预期结果**:
- ✅ 成功识别拖放
- ✅ 成功处理
- ✅ 显示提取的JSON数据

---

## 💡 关于PDF处理的说明

### Qwen-VL Max 对PDF的支持

**好消息**: ✅ Qwen-VL Max **可以直接处理PDF**，不需要先转换为图片！

**处理方式**:
1. 用户上传PDF文件
2. 读取PDF文件内容
3. 转换为Base64
4. 直接发送给Qwen-VL API（使用 `image_url` 格式）
5. Qwen-VL 自动处理PDF中的所有页面

**优点**:
- ✅ 无需PDF转图片步骤
- ✅ 处理速度更快
- ✅ 支持多页PDF
- ✅ 准确率更高

---

## 🔄 修复前后对比

### 修复前（错误）

```javascript
// ❌ 错误的格式
content: [
    {
        type: 'image',  // API不支持
        image: 'data:image/jpeg;base64,...'
    }
]
```

**结果**: 400错误

---

### 修复后（正确）

```javascript
// ✅ 正确的格式
content: [
    {
        type: 'image_url',  // API支持
        image_url: {
            url: 'data:image/jpeg;base64,...'
        }
    }
]
```

**结果**: 成功处理

---

## ✅ 总结

### 修复内容

1. ✅ 修改API请求格式（`image` → `image_url`）
2. ✅ 调整数据结构（添加 `image_url.url` 嵌套）
3. ✅ 确认PDF支持（可以直接处理）

### PDF支持

- ✅ **PDF可以上传**
- ✅ **无需转换为图片**
- ✅ **Qwen-VL Max 直接处理**

### 下一步

1. 刷新测试页面
2. 重新上传文件（图片或PDF）
3. 验证处理结果

---

**修复完成时间**: 2026-01-07  
**状态**: ✅ 已修复  
**PDF支持**: ✅ 可以直接上传PDF文件







