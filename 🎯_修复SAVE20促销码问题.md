# 🎯 修复 SAVE20 促销码问题 - 完整指南

## 📋 问题分析

**当前情况：**
- ✅ Stripe中已创建优惠券（Coupon）`SAVE20`
- ✅ 代码中已设置 `allow_promotion_codes: true`
- ❌ 客户输入 `SAVE20` 时显示"该促销码无效"

**问题原因：**
您创建的是 **Coupon（优惠券）**，但客户需要的是 **Promotion Code（促销码）**。

在Stripe中：
- **Coupon**: 后台概念，定义折扣规则（20% off, $10 off等）
- **Promotion Code**: 前台概念，客户实际输入的代码（如 SAVE20）

## 🛠️ 解决方案：创建促销码

### 方法1：通过Stripe Dashboard创建（推荐）

1. **进入促销码页面**
   - 登录 Stripe Dashboard
   - 左侧菜单选择 **产品目录** → **优惠**
   - 点击 **促销码** 标签

2. **创建新促销码**
   - 点击右上角 **"+ 创建促销码"** 按钮

3. **配置促销码**
   ```
   促销码：SAVE20
   优惠券：首次8折优惠（选择您已创建的优惠券）
   有效：是
   最大兑换次数：1000（或根据需求设置）
   ```

4. **适用产品（重要！）**
   ```
   选择：适用于所有产品
   或者：选择特定产品
     - VaultCaddy Monthly
     - VaultCaddy Yearly
   ```

5. **保存**
   - 点击 **"创建促销码"**

### 方法2：通过API创建（需要正确的API密钥）

如果您想通过API创建，请在Stripe Dashboard中：

1. 进入 **开发者** → **API密钥**
2. 复制 **生产模式密钥**（以 `sk_live_` 开头）
3. 运行以下命令（替换YOUR_SECRET_KEY）：

```bash
curl https://api.stripe.com/v1/promotion_codes \
  -u "YOUR_SECRET_KEY:" \
  -d "coupon=SAVE20" \
  -d "code=SAVE20" \
  -d "active=true" \
  -d "max_redemptions=1000"
```

## ✅ 验证步骤

创建促销码后，请验证：

1. **在Stripe Dashboard中检查**
   - 产品目录 → 优惠 → 促销码
   - 确认 `SAVE20` 存在且状态为"有效"

2. **测试支付流程**
   - 访问 https://vaultcaddy.com/billing.html
   - 点击 "Get Started"
   - 在支付页面的促销码输入框输入 `SAVE20`
   - 应该显示折扣已应用，金额从 HK$58 变为 HK$46.40

3. **检查折扣计算**
   ```
   原价：HK$58.00
   8折后：HK$58.00 × 0.8 = HK$46.40
   节省：HK$11.60（20% off）
   ```

## 🎯 常见问题

### Q1: 促销码显示"无效"
**解决方案：**
- 检查促销码是否已激活（active: true）
- 检查是否设置了使用次数限制且已用完
- 检查是否设置了适用产品限制

### Q2: 促销码不适用于订阅
**解决方案：**
- 确认优惠券的"持续时间"设置：
  - `once`: 仅首次计费
  - `repeating`: 指定月数
  - `forever`: 永久折扣

### Q3: 客户看不到促销码输入框
**解决方案：**
- 确认代码中设置了 `allow_promotion_codes: true`
- 检查 firebase-functions/index.js 第2264行

## 📝 下一步

完成促销码创建后：

1. ✅ 测试支付流程
2. ✅ 更新营销材料（邮件、社交媒体等）
3. ✅ 监控促销码使用情况
4. ✅ 在Dashboard中查看兑换统计

## 🚀 快速操作

**立即前往Stripe Dashboard创建促销码：**
https://dashboard.stripe.com/coupons/promotions

**需要帮助？**
- Stripe促销码文档：https://stripe.com/docs/billing/subscriptions/coupons
- VaultCaddy支持：检查Firebase Functions日志

---

**创建日期**: 2025-12-20  
**状态**: 待执行  
**优先级**: 🔥 高




