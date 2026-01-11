# 📋 QuickBooks Online API 集成架构说明

**文档目的**: 说明如何建立直接API连接到QuickBooks Online  
**当前状态**: 仅生成QBO文件供用户手动导入  
**目标状态**: 直接通过API推送数据到QuickBooks Online

---

## 🔍 当前实现 vs API集成

### 当前实现（文件导出）

**工作流程**:
```
用户上传PDF → AI提取数据 → 生成QBO文件 → 用户下载 → 手动导入QuickBooks
```

**代码位置**:
- `export-manager.js` - `exportToQBO()` 方法
- 生成OFX/QFX格式的QBO文件
- 用户需要手动下载并导入QuickBooks

**优点**:
- ✅ 简单，无需API认证
- ✅ 用户完全控制数据
- ✅ 支持离线使用

**缺点**:
- ❌ 需要用户手动操作
- ❌ 无法实时同步
- ❌ 用户体验不够流畅

---

## 🚀 API集成需要建立的内容

### 1. Intuit开发者账户和应用程序

#### 1.1 注册开发者账户
- **平台**: https://developer.intuit.com/
- **步骤**:
  1. 创建Intuit开发者账户
  2. 验证邮箱
  3. 完成开发者信息填写

#### 1.2 创建应用程序
- **应用类型**: Accounting (QuickBooks Online)
- **应用名称**: VaultCaddy
- **应用描述**: AI-powered bank statement and invoice processing for QuickBooks Online
- **环境**: 
  - Development (开发环境)
  - Production (生产环境)

#### 1.3 获取应用凭据
- **Client ID** (客户端ID)
- **Client Secret** (客户端密钥)
- **这些凭据用于OAuth 2.0认证**

---

### 2. OAuth 2.0 认证系统

#### 2.1 OAuth 2.0 流程

**步骤1: 授权请求**
```
用户点击"连接QuickBooks" → 
重定向到Intuit授权页面 → 
用户登录并授权 → 
Intuit返回授权码(Authorization Code)
```

**步骤2: 获取访问令牌**
```
使用授权码 + Client ID + Client Secret → 
调用Intuit Token端点 → 
获取Access Token和Refresh Token
```

**步骤3: 存储令牌**
```
Access Token (短期有效，约1小时) → 用于API调用
Refresh Token (长期有效) → 用于刷新Access Token
```

#### 2.2 需要实现的功能

**前端部分**:
```javascript
// 1. 启动OAuth流程
function connectQuickBooks() {
    const clientId = 'YOUR_CLIENT_ID';
    const redirectUri = 'https://vaultcaddy.com/auth/qbo/callback';
    const scope = 'com.intuit.quickbooks.accounting';
    const authUrl = `https://appcenter.intuit.com/connect/oauth2?client_id=${clientId}&scope=${scope}&redirect_uri=${redirectUri}&response_type=code`;
    
    window.location.href = authUrl;
}

// 2. 处理回调
function handleOAuthCallback(code) {
    // 发送code到后端服务器
    fetch('/api/qbo/exchange-token', {
        method: 'POST',
        body: JSON.stringify({ code }),
        headers: { 'Content-Type': 'application/json' }
    });
}
```

**后端部分** (需要新建):
```javascript
// 1. 交换授权码获取令牌
app.post('/api/qbo/exchange-token', async (req, res) => {
    const { code } = req.body;
    
    // 调用Intuit Token端点
    const tokenResponse = await fetch('https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': `Basic ${base64(clientId + ':' + clientSecret)}`
        },
        body: new URLSearchParams({
            grant_type: 'authorization_code',
            code: code,
            redirect_uri: redirectUri
        })
    });
    
    const tokens = await tokenResponse.json();
    // tokens.access_token
    // tokens.refresh_token
    
    // 存储到数据库（关联用户ID）
    await saveTokens(userId, tokens);
});
```

---

### 3. 后端API服务

#### 3.1 需要新建的后端服务

**文件结构**:
```
backend/
├── qbo/
│   ├── auth.js          # OAuth认证处理
│   ├── token-manager.js # 令牌管理和刷新
│   ├── api-client.js    # QuickBooks API客户端
│   └── data-sync.js     # 数据同步逻辑
└── routes/
    └── qbo-routes.js    # API路由
```

#### 3.2 核心功能模块

**A. 令牌管理器 (token-manager.js)**
```javascript
// 作用：
// 1. 存储和检索用户的Access Token和Refresh Token
// 2. 自动刷新过期的Access Token
// 3. 处理令牌过期错误

class QBOTokenManager {
    async getValidToken(userId) {
        // 检查Access Token是否过期
        // 如果过期，使用Refresh Token刷新
        // 返回有效的Access Token
    }
    
    async refreshToken(userId) {
        // 使用Refresh Token获取新的Access Token
    }
}
```

**B. API客户端 (api-client.js)**
```javascript
// 作用：
// 1. 封装QuickBooks API调用
// 2. 处理API错误和重试
// 3. 管理API速率限制

class QBOAPIClient {
    constructor(accessToken, realmId) {
        this.accessToken = accessToken;
        this.realmId = realmId; // 公司ID
        this.baseUrl = 'https://sandbox-quickbooks.api.intuit.com/v3/company';
    }
    
    async createInvoice(invoiceData) {
        // 调用QuickBooks API创建发票
        // POST /v3/company/{realmId}/invoice
    }
    
    async createBankTransaction(transactionData) {
        // 调用QuickBooks API创建银行交易
        // POST /v3/company/{realmId}/deposit
        // 或 POST /v3/company/{realmId}/journalentry
    }
}
```

**C. 数据同步器 (data-sync.js)**
```javascript
// 作用：
// 1. 将VaultCaddy提取的数据转换为QuickBooks格式
// 2. 批量同步数据
// 3. 处理数据冲突和错误

class QBOSyncManager {
    async syncBankStatement(userId, statementData) {
        // 1. 获取用户的QuickBooks连接信息
        // 2. 转换银行对账单数据为QuickBooks格式
        // 3. 调用API创建交易记录
    }
    
    async syncInvoice(userId, invoiceData) {
        // 1. 转换发票数据为QuickBooks格式
        // 2. 创建或更新客户
        // 3. 创建发票
    }
}
```

---

### 4. 数据转换层

#### 4.1 当前QBO文件格式 vs API格式

**当前QBO文件格式** (export-manager.js):
```javascript
// OFX/QFX格式（用于文件导入）
OFXHEADER:100
DATA:OFXSGML
<OFX>
  <INVSTMTMSGSRSV1>
    <INVBANKTRAN>
      <STMTTRN>
        <TRNTYPE>CREDIT</TRNTYPE>
        <DTPOSTED>20260105</DTPOSTED>
        <TRNAMT>1000.00</TRNAMT>
      </STMTTRN>
    </INVBANKTRAN>
  </INVSTMTMSGSRSV1>
</OFX>
```

**API格式** (JSON):
```javascript
// QuickBooks API使用JSON格式
{
  "Deposit": {
    "DepositToAccountRef": {
      "value": "35",  // 银行账户ID
      "name": "Checking"
    },
    "TxnDate": "2026-01-05",
    "Line": [
      {
        "DetailType": "DepositLineDetail",
        "Amount": 1000.00,
        "DepositLineDetail": {
          "EntityRef": {
            "value": "1",
            "name": "Customer Name"
          }
        }
      }
    ]
  }
}
```

#### 4.2 需要建立的数据转换器

```javascript
// qbo/data-converter.js

class QBODataConverter {
    // 将VaultCaddy的银行对账单数据转换为QuickBooks API格式
    convertBankStatementToDeposit(statementData) {
        return {
            Deposit: {
                DepositToAccountRef: {
                    value: this.getAccountId(statementData.accountType),
                    name: statementData.accountName
                },
                TxnDate: statementData.date,
                Line: statementData.transactions.map(tx => ({
                    DetailType: "DepositLineDetail",
                    Amount: tx.amount,
                    DepositLineDetail: {
                        EntityRef: {
                            name: tx.payee || "Unknown"
                        }
                    }
                }))
            }
        };
    }
    
    // 将VaultCaddy的发票数据转换为QuickBooks API格式
    convertInvoiceToQBO(invoiceData) {
        return {
            Invoice: {
                CustomerRef: {
                    name: invoiceData.customerName
                },
                TxnDate: invoiceData.issueDate,
                Line: invoiceData.items.map(item => ({
                    DetailType: "SalesItemLineDetail",
                    Amount: item.amount,
                    SalesItemLineDetail: {
                        ItemRef: {
                            name: item.description
                        },
                        Quantity: item.quantity,
                        UnitPrice: item.unitPrice
                    }
                }))
            }
        };
    }
}
```

---

### 5. 数据库设计

#### 5.1 需要新增的数据表

**qbo_connections 表**:
```sql
CREATE TABLE qbo_connections (
    id VARCHAR(255) PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    realm_id VARCHAR(255) NOT NULL,  -- QuickBooks公司ID
    access_token TEXT NOT NULL,
    refresh_token TEXT NOT NULL,
    token_expires_at TIMESTAMP NOT NULL,
    connected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    disconnected_at TIMESTAMP NULL,
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

**qbo_sync_logs 表**:
```sql
CREATE TABLE qbo_sync_logs (
    id VARCHAR(255) PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    document_id VARCHAR(255) NOT NULL,
    sync_type VARCHAR(50) NOT NULL,  -- 'invoice', 'bank_statement'
    qbo_entity_id VARCHAR(255),      -- QuickBooks中的实体ID
    sync_status VARCHAR(50),         -- 'success', 'failed', 'pending'
    error_message TEXT,
    synced_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (document_id) REFERENCES documents(id)
);
```

---

### 6. 前端UI组件

#### 6.1 需要新增的UI组件

**A. QuickBooks连接按钮**
```html
<!-- 在账户设置页面 -->
<div class="qbo-connection-section">
    <h3>QuickBooks Online 连接</h3>
    <button id="connect-qbo-btn" class="btn-primary">
        <i class="fab fa-quickbooks"></i>
        连接 QuickBooks Online
    </button>
    <div id="qbo-status" class="status-indicator">
        <!-- 显示连接状态 -->
    </div>
</div>
```

**B. 同步选项**
```html
<!-- 在导出菜单中 -->
<div class="export-options">
    <label>
        <input type="radio" name="export-method" value="download">
        下载QBO文件
    </label>
    <label>
        <input type="radio" name="export-method" value="sync" id="sync-to-qbo">
        直接同步到QuickBooks
    </label>
</div>
```

**C. 同步状态显示**
```html
<div id="sync-status" class="sync-status">
    <div class="sync-progress">
        <span>正在同步到QuickBooks...</span>
        <progress value="50" max="100"></progress>
    </div>
    <div class="sync-result">
        <i class="fas fa-check-circle"></i>
        <span>已成功同步3条交易记录</span>
    </div>
</div>
```

---

### 7. 安全考虑

#### 7.1 令牌安全

**存储**:
- ✅ Refresh Token必须加密存储
- ✅ Access Token不应存储在客户端
- ✅ 使用环境变量存储Client Secret

**传输**:
- ✅ 所有API调用使用HTTPS
- ✅ OAuth回调使用state参数防止CSRF攻击

#### 7.2 权限控制

**最小权限原则**:
- ✅ 只请求必要的API权限
- ✅ 定期审查API访问权限
- ✅ 提供用户断开连接的选项

---

### 8. 错误处理和重试机制

#### 8.1 常见错误

**令牌过期**:
```javascript
if (error.code === 401) {
    // 自动刷新令牌并重试
    await refreshToken();
    return retryRequest();
}
```

**速率限制**:
```javascript
if (error.code === 429) {
    // 等待后重试
    await sleep(error.retryAfter);
    return retryRequest();
}
```

**数据验证错误**:
```javascript
if (error.code === 400) {
    // 记录错误，通知用户
    logError(error);
    notifyUser('数据格式错误，请检查数据');
}
```

---

### 9. 测试环境

#### 9.1 Sandbox环境

**用途**:
- 开发和测试API集成
- 不会影响真实QuickBooks数据
- 可以重置测试数据

**配置**:
- 在Intuit开发者门户创建Sandbox应用
- 使用Sandbox API端点: `https://sandbox-quickbooks.api.intuit.com`

#### 9.2 测试账户

**需要**:
- Intuit Sandbox测试账户
- 测试QuickBooks公司
- 测试数据

---

### 10. 实施步骤建议

#### 阶段1: 基础架构（1-2周）
1. ✅ 注册Intuit开发者账户
2. ✅ 创建Sandbox应用
3. ✅ 实现OAuth 2.0认证流程
4. ✅ 建立后端API服务框架

#### 阶段2: 核心功能（2-3周）
1. ✅ 实现令牌管理
2. ✅ 实现API客户端
3. ✅ 实现数据转换器
4. ✅ 实现数据同步逻辑

#### 阶段3: 前端集成（1-2周）
1. ✅ 添加连接UI
2. ✅ 添加同步选项
3. ✅ 添加状态显示
4. ✅ 错误处理UI

#### 阶段4: 测试和优化（1-2周）
1. ✅ 端到端测试
2. ✅ 错误处理测试
3. ✅ 性能优化
4. ✅ 用户体验优化

#### 阶段5: 生产部署（1周）
1. ✅ 创建生产环境应用
2. ✅ 安全审计
3. ✅ 文档编写
4. ✅ 用户培训

---

## 📊 技术栈建议

### 后端
- **Node.js + Express** (或您当前使用的后端框架)
- **axios** (HTTP客户端)
- **jsonwebtoken** (JWT处理，如果需要)
- **crypto** (加密存储)

### 前端
- **现有前端框架** (无需新增)
- **OAuth 2.0客户端库** (可选)

### 数据库
- **现有数据库** (添加新表)

---

## 💰 成本和限制

### API限制
- **免费层**: 500次API调用/分钟
- **付费层**: 根据需求升级

### 开发成本
- **开发者账户**: 免费
- **Sandbox环境**: 免费
- **生产环境**: 可能需要付费（取决于使用量）

---

## 🎯 优势总结

### 用户体验
- ✅ 一键同步，无需手动操作
- ✅ 实时数据同步
- ✅ 减少错误和重复工作

### 商业价值
- ✅ 提升产品竞争力
- ✅ 增加用户粘性
- ✅ 可以作为付费功能

### 技术优势
- ✅ 自动化工作流
- ✅ 减少用户操作步骤
- ✅ 更好的数据一致性

---

## ⚠️ 注意事项

1. **API版本**: QuickBooks API有版本控制，需要关注API版本更新
2. **数据映射**: 不同银行的数据格式需要正确映射到QuickBooks字段
3. **错误处理**: 必须妥善处理各种错误情况
4. **用户隐私**: 确保符合数据保护法规
5. **API变更**: Intuit可能会更新API，需要保持代码更新

---

**文档生成时间**: 2026-01-05  
**状态**: 📋 架构说明文档



