# 📝 Billing Meter 配置信息

## 测试模式

### Billing Meter
- **Meter ID**: `mtr_test_61TnAddrAuQxlRy7p41JmiQ31C`
- **Event Name**: `vaultcaddy_credit_usage`
- **Display Name**: VaultCaddy Credits 使用量
- **状态**: 激活
- **创建时间**: 2025/12/13 下午2:51

### API 测试命令
```bash
curl https://api.stripe.com/v1/billing/meter_events \
  -u "sk_test_51S6Qv3JmiQ31C0GTbiGaoNjEugsCskHfhma2MAZChrenTpiag7WEsxkbjwPmLwEamsWdYdUGr05uagoLVEnq9g5N00RQU4012q:" \
  -d event_name=vaultcaddy_credit_usage \
  -d timestamp=1765976378 \
  -d "payload[stripe_customer_id]"="cus_TcZTukSbC3QlVh" \
  -d "payload[value]"=1
```

---

## 生产模式

### Billing Meter
- **Meter ID**: `待创建`
- **Event Name**: `vaultcaddy_credit_usage`（必须与测试模式一致）
- **Display Name**: VaultCaddy Credits 使用量
- **状态**: 待创建

⚠️ **提醒**: 测试完成后，需要在生产模式中创建相同配置的 Meter

---

## 下一步

1. ✅ 创建 Billing Meter - **已完成**
2. 🔄 创建新的价格配置（关联到这个 Meter） - **进行中**
3. ⏳ 修改 Firebase Functions 代码
4. ⏳ 测试新系统
5. ⏳ 部署到生产环境





