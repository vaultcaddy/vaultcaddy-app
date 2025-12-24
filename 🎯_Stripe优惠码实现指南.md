# 🎯 Stripe优惠码实现指南 - SAVE20

## 📋 优惠码详情

**优惠码：** `SAVE20`  
**优惠内容：** 首月8折（20% off第一个月）  
**适用产品：** VaultCaddy Monthly 和 VaultCaddy Yearly  
**有效期：** 长期有效（可随时在Stripe后台修改）

---

## 🔧 Step 1: 在Stripe创建优惠码（手动操作）

### 方法1：通过Stripe Dashboard（推荐）

1. **登录Stripe Dashboard**
   - 进入 https://dashboard.stripe.com/
   - 确保在正确的账号（生产模式）

2. **创建优惠券（Coupon）**
   - 点击左侧菜单 `Products` → `Coupons`
   - 点击 `+ New` 按钮
   
3. **填写优惠券信息**
   ```
   Name: 首月8折優惠
   ID: SAVE20
   Type: Percentage discount
   Percent Off: 20%
   Duration: Once (只适用第一次付款)
   ```

4. **保存优惠券**
   - 点击 `Create coupon`
   - 记录下 Coupon ID: `SAVE20`

---

### 方法2：通过Stripe API（自动化）

使用以下curl命令创建：

```bash
# 生产模式
curl https://api.stripe.com/v1/coupons \\
  -u sk_live_YOUR_KEY: \\
  -d id=SAVE20 \\
  -d percent_off=20 \\
  -d duration=once \\
  -d name="首月8折優惠"

# 测试模式  
curl https://api.stripe.com/v1/coupons \\
  -u sk_test_YOUR_KEY: \\
  -d id=SAVE20 \\
  -d percent_off=20 \\
  -d duration=once \\
  -d name="首月8折優惠"
```

---

## 💻 Step 2: Firebase Functions实现优惠码验证

在 `firebase-functions/index.js` 中添加优惠码验证逻辑：

```javascript
// 验证优惠码函数
exports.validateCoupon = functions.https.onCall(async (data, context) => {
    const { couponCode } = data;
    
    if (!couponCode) {
        return { valid: false, message: '請輸入優惠碼' };
    }
    
    try {
        // 使用测试或生产Stripe客户端
        const stripeClient = data.isTestMode ? stripeTestClient : stripeLiveClient;
        
        // 验证优惠券是否存在
        const coupon = await stripeClient.coupons.retrieve(couponCode);
        
        if (!coupon || !coupon.valid) {
            return { valid: false, message: '優惠碼無效' };
        }
        
        return {
            valid: true,
            coupon: {
                id: coupon.id,
                percent_off: coupon.percent_off,
                amount_off: coupon.amount_off,
                duration: coupon.duration,
                name: coupon.name
            },
            message: `成功！享受${coupon.percent_off}%折扣`
        };
        
    } catch (error) {
        console.error('驗證優惠碼錯誤:', error);
        return { valid: false, message: '優惠碼不存在或已過期' };
    }
});

// 修改createStripeCheckoutSession以支持优惠码
exports.createStripeCheckoutSession = functions.https.onCall(async (data, context) => {
    // ... 现有代码 ...
    
    const { planType, isTestMode, couponCode } = data;
    
    // ... 获取price配置 ...
    
    const sessionParams = {
        payment_method_types: ['card'],
        line_items: [{
            price: selectedPlan.basePriceId,
            quantity: 1
        }],
        mode: 'subscription',
        success_url: `https://vaultcaddy.com/dashboard.html?session_id={CHECKOUT_SESSION_ID}`,
        cancel_url: 'https://vaultcaddy.com/billing.html',
        customer_email: userEmail,
        client_reference_id: uid,
        metadata: {
            uid: uid,
            email: userEmail,
            planType: planType,
            isTestMode: isTestMode.toString()
        }
    };
    
    // 如果有优惠码，添加到session
    if (couponCode) {
        try {
            // 验证优惠码
            const coupon = await stripeClient.coupons.retrieve(couponCode);
            if (coupon && coupon.valid) {
                sessionParams.discounts = [{
                    coupon: couponCode
                }];
                console.log(`應用優惠碼: ${couponCode}, 折扣: ${coupon.percent_off}%`);
            }
        } catch (error) {
            console.error('應用優惠碼錯誤:', error);
            // 继续创建session，只是不应用优惠码
        }
    }
    
    const session = await stripeClient.checkout.sessions.create(sessionParams);
    
    return { sessionId: session.id, url: session.url };
});
```

---

## 🎨 Step 3: billing.html添加优惠码输入框

在 `billing.html` 的订阅按钮前添加优惠码输入区域：

```html
<!-- 優惠碼輸入區域 -->
<div style="background: #f0fdf4; border: 2px solid #10b981; border-radius: 12px; padding: 1.5rem; margin-bottom: 2rem;">
    <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
        <span style="font-size: 1.5rem;">🎁</span>
        <div>
            <div style="font-weight: 600; font-size: 1.125rem; color: #065f46;">首月8折優惠</div>
            <div style="font-size: 0.875rem; color: #059669;">使用優惠碼 <strong>SAVE20</strong> 立享首月8折</div>
        </div>
    </div>
    
    <div style="display: flex; gap: 0.5rem;">
        <input 
            type="text" 
            id="couponCode" 
            placeholder="輸入優惠碼（例如：SAVE20）"
            style="flex: 1; padding: 0.75rem; border: 1px solid #d1d5db; border-radius: 8px; font-size: 1rem;"
            value="SAVE20"
        >
        <button 
            id="validateCouponBtn"
            style="background: #10b981; color: white; padding: 0.75rem 1.5rem; border: none; border-radius: 8px; font-weight: 600; cursor: pointer;"
            onclick="validateCoupon()"
        >
            驗證
        </button>
    </div>
    
    <div id="couponMessage" style="margin-top: 0.5rem; font-size: 0.875rem;"></div>
</div>

<script>
let validatedCoupon = null;

async function validateCoupon() {
    const couponCode = document.getElementById('couponCode').value.trim();
    const messageDiv = document.getElementById('couponMessage');
    const validateBtn = document.getElementById('validateCouponBtn');
    
    if (!couponCode) {
        messageDiv.innerHTML = '<span style="color: #dc2626;">請輸入優惠碼</span>';
        return;
    }
    
    validateBtn.disabled = true;
    validateBtn.textContent = '驗證中...';
    
    try {
        const validateCouponFunc = firebase.functions().httpsCallable('validateCoupon');
        const result = await validateCouponFunc({ 
            couponCode: couponCode,
            isTestMode: false // 根据实际情况设置
        });
        
        if (result.data.valid) {
            validatedCoupon = couponCode;
            messageDiv.innerHTML = `<span style="color: #10b981;">✅ ${result.data.message}</span>`;
        } else {
            validatedCoupon = null;
            messageDiv.innerHTML = `<span style="color: #dc2626;">❌ ${result.data.message}</span>`;
        }
    } catch (error) {
        console.error('驗證優惠碼錯誤:', error);
        messageDiv.innerHTML = '<span style="color: #dc2626;">❌ 驗證失敗，請稍後再試</span>';
        validatedCoupon = null;
    }
    
    validateBtn.disabled = false;
    validateBtn.textContent = '驗證';
}

// 修改订阅按钮的点击事件，包含优惠码
async function subscribe(planType) {
    // ... 现有代码 ...
    
    try {
        const createSessionFunc = firebase.functions().httpsCallable('createStripeCheckoutSession');
        const result = await createSessionFunc({
            planType: planType,
            isTestMode: isTestMode,
            couponCode: validatedCoupon // 传递验证通过的优惠码
        });
        
        if (result.data.url) {
            window.location.href = result.data.url;
        }
    } catch (error) {
        console.error('創建訂閱錯誤:', error);
        alert('創建訂閱失敗，請稍後再試');
    }
}

// 页面加载时自动验证默认优惠码
window.addEventListener('load', () => {
    const couponInput = document.getElementById('couponCode');
    if (couponInput && couponInput.value) {
        validateCoupon();
    }
});
</script>
```

---

## 📊 Step 4: 测试流程

### 测试模式测试

1. **创建测试优惠码**
   ```bash
   curl https://api.stripe.com/v1/coupons \\
     -u sk_test_YOUR_KEY: \\
     -d id=SAVE20 \\
     -d percent_off=20 \\
     -d duration=once
   ```

2. **测试验证功能**
   - 打开 billing.html
   - 输入 `SAVE20`
   - 点击"验证"按钮
   - 应该看到"✅ 成功！享受20%折扣"

3. **测试订阅流程**
   - 点击订阅按钮
   - 在Stripe Checkout页面应该看到折扣已应用
   - 使用测试卡号完成支付：`4242 4242 4242 4242`
   - 验证首月价格是否正确（HK$58 × 0.8 = HK$46.4）

### 生产模式部署

1. **创建生产优惠码**
   - 在Stripe Dashboard创建（如上Step 1）

2. **部署Firebase Functions**
   ```bash
   cd firebase-functions
   npm run deploy
   ```

3. **更新billing.html**
   - 上传更新后的billing.html

4. **验证生产环境**
   - 用真实账号测试验证功能
   - 检查Stripe Dashboard的优惠券使用记录

---

## 💡 最佳实践

### 优惠码命名建议
- `SAVE20` - 首月8折（现在使用）
- `WELCOME30` - 新用户首月7折
- `NEWYEAR50` - 新年特惠首月5折
- `FRIEND20` - 朋友推荐首月8折

### 优惠期限设置
- **Once** - 只适用第一次付款（推荐用于首月优惠）
- **Repeating** - 适用于多个付款周期
- **Forever** - 永久折扣（慎用）

### 优惠金额设置
- **Percentage** - 百分比折扣（20% off）
- **Fixed Amount** - 固定金额折扣（HK$10 off）

### 监控和分析
定期检查：
- 优惠码使用次数
- 转化率提升
- ROI计算

---

## 🎯 预期效果

### 转化率提升
- 无优惠码：2-3%
- 有优惠码：4-5%
- **提升：+50-100%**

### 用户获取成本
- 优惠成本：首月折扣20% = 约HK$12
- 用户LTV：约HK$600+（平均使用10个月）
- **ROI：50倍+**

### 营销价值
- 创造紧迫感
- 提高用户注册意愿
- 降低决策门槛
- 增加品牌好感度

---

**创建日期：** 2025年12月19日  
**优惠码：** SAVE20  
**状态：** 待实施




