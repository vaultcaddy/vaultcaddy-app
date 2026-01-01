#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import random

print("🎌 查找日文和韩文版本页面")
print("=" * 80)

base_dir = '/Users/cavlinyeung/ai-bank-parser'

# 日文版
print("\n📘 日文版（ja-JP）：")
ja_dir = os.path.join(base_dir, 'ja-JP')
if os.path.exists(ja_dir):
    ja_files = [f for f in os.listdir(ja_dir) if f.endswith('.html')]
    ja_original = [f for f in ja_files if '-v2' not in f and '-v3' not in f and ('statement' in f or 'accounting' in f)]
    ja_v2 = [f for f in ja_files if '-v2.html' in f]
    ja_v3 = [f for f in ja_files if '-v3.html' in f]
    
    print(f"  原始页面数量: {len(ja_original)}")
    print(f"  V2页面数量: {len(ja_v2)}")
    print(f"  V3页面数量: {len(ja_v3)}")
    
    if ja_original:
        selected_original = random.choice(ja_original)
        print(f"\n  ✅ 选择原始页面: ja-JP/{selected_original}")
    else:
        print(f"\n  ⚠️ 无原始页面")
        selected_original = None
    
    if ja_v2:
        selected_v2 = random.choice(ja_v2)
        print(f"  ✅ 选择V2页面: ja-JP/{selected_v2}")
    else:
        print(f"  ⚠️ 无V2页面")
        selected_v2 = None
    
    if ja_v3:
        selected_v3 = random.choice(ja_v3)
        print(f"  ✅ 选择V3页面: ja-JP/{selected_v3}")
    else:
        print(f"  ⚠️ 无V3页面")
        selected_v3 = None
else:
    print("  ❌ ja-JP目录不存在")
    selected_original = None
    selected_v2 = None
    selected_v3 = None

# 韩文版
print("\n📗 韩文版（ko-KR）：")
kr_dir = os.path.join(base_dir, 'ko-KR')
if os.path.exists(kr_dir):
    kr_files = [f for f in os.listdir(kr_dir) if f.endswith('.html')]
    kr_original = [f for f in kr_files if '-v2' not in f and '-v3' not in f and ('statement' in f or 'accounting' in f)]
    kr_v2 = [f for f in kr_files if '-v2.html' in f]
    kr_v3 = [f for f in kr_files if '-v3.html' in f]
    
    print(f"  原始页面数量: {len(kr_original)}")
    print(f"  V2页面数量: {len(kr_v2)}")
    print(f"  V3页面数量: {len(kr_v3)}")
    
    if kr_original:
        selected_kr_original = random.choice(kr_original)
        print(f"\n  ✅ 选择原始页面: ko-KR/{selected_kr_original}")
    else:
        print(f"\n  ⚠️ 无原始页面")
        selected_kr_original = None
    
    if kr_v2:
        selected_kr_v2 = random.choice(kr_v2)
        print(f"  ✅ 选择V2页面: ko-KR/{selected_kr_v2}")
    else:
        print(f"  ⚠️ 无V2页面")
        selected_kr_v2 = None
    
    if kr_v3:
        selected_kr_v3 = random.choice(kr_v3)
        print(f"  ✅ 选择V3页面: ko-KR/{selected_kr_v3}")
    else:
        print(f"  ⚠️ 无V3页面")
        selected_kr_v3 = None
else:
    print("  ❌ ko-KR目录不存在")
    selected_kr_original = None
    selected_kr_v2 = None
    selected_kr_v3 = None

print("\n" + "=" * 80)
print("📝 总结：")
print(f"\n日文版：")
if selected_original:
    print(f"  - 原始: ja-JP/{selected_original}")
if selected_v2:
    print(f"  - V2: ja-JP/{selected_v2}")
if selected_v3:
    print(f"  - V3: ja-JP/{selected_v3}")
if not selected_original and not selected_v2 and not selected_v3:
    print(f"  - ⚠️ 仅有V3版本")

print(f"\n韩文版：")
if selected_kr_original:
    print(f"  - 原始: ko-KR/{selected_kr_original}")
if selected_kr_v2:
    print(f"  - V2: ko-KR/{selected_kr_v2}")
if selected_kr_v3:
    print(f"  - V3: ko-KR/{selected_kr_v3}")
if not selected_kr_original and not selected_kr_v2 and not selected_kr_v3:
    print(f"  - ⚠️ 仅有V3版本")

print("=" * 80)

# 输出打开命令
print("\n🚀 准备打开的页面：")
pages_to_open = []
if selected_v3:
    pages_to_open.append(f"ja-JP/{selected_v3}")
if selected_kr_v3:
    pages_to_open.append(f"ko-KR/{selected_kr_v3}")

for page in pages_to_open:
    print(f"  - {page}")
