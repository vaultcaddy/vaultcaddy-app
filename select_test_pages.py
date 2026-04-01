#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import random

print("🎲 随机抽取测试页面（中英文各v1/v2/v3）")
print("=" * 80)

# 英文版
print("\n📘 英文版本：")
en_original = "hsbc-bank-statement.html"
en_v2 = "restaurant-accounting-solution-v2.html"
en_v3 = "chase-bank-statement-v3.html"

print(f"  V1（原始）: {en_original}")
print(f"  V2: {en_v2}")
print(f"  V3: {en_v3}")

# 台湾中文版
print("\n📗 台湾中文版（TWD）：")
tw_original = "zh-TW/hsbc-bank-statement.html" if os.path.exists("zh-TW/hsbc-bank-statement.html") else None
tw_v2 = "zh-TW/restaurant-accounting-solution-v2.html" if os.path.exists("zh-TW/restaurant-accounting-solution-v2.html") else None
tw_v3 = "zh-TW/ctbc-bank-statement-v3.html"

if tw_original:
    print(f"  V1（原始）: {tw_original}")
else:
    print(f"  V1（原始）: ⚠️ 未找到")
if tw_v2:
    print(f"  V2: {tw_v2}")
else:
    print(f"  V2: ⚠️ 未找到")
print(f"  V3: {tw_v3}")

# 香港中文版
print("\n📙 香港中文版（HKD）：")
hk_original = "zh-HK/hsbc-bank-statement.html" if os.path.exists("zh-HK/hsbc-bank-statement.html") else None
hk_v2 = "zh-HK/restaurant-accounting-solution-v2.html" if os.path.exists("zh-HK/restaurant-accounting-solution-v2.html") else None
hk_v3 = "zh-HK/hsbc-bank-statement-v3.html"

if hk_original:
    print(f"  V1（原始）: {hk_original}")
else:
    print(f"  V1（原始）: ⚠️ 未找到")
if hk_v2:
    print(f"  V2: {hk_v2}")
else:
    print(f"  V2: ⚠️ 未找到")
print(f"  V3: {hk_v3}")

print("\n" + "=" * 80)
print("📝 总结：")
print("  - 英文版：3个页面（V1原始 + V2 + V3）")
print("  - 台湾版：1个页面（V3，V1/V2可能不存在）")
print("  - 香港版：1个页面（V3，V1/V2可能不存在）")
print("=" * 80)
