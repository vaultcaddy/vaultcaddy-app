#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import random

# 英文版root目录
root_files = [f for f in os.listdir('.') if f.endswith('.html') and not f.startswith('index')]

# 分类页面
original_pages = [f for f in root_files if '-v2' not in f and '-v3' not in f and ('statement' in f or 'accounting' in f or 'solution' in f)]
v2_pages = [f for f in root_files if '-v2.html' in f]
v3_pages = [f for f in root_files if '-v3.html' in f]

print("=" * 80)
print("🎲 随机抽取英文版页面")
print("=" * 80)

if original_pages:
    en_original = random.choice(original_pages)
    print(f"\n📄 英文原始页面: {en_original}")
else:
    print("\n⚠️ 未找到英文原始页面")

if v2_pages:
    en_v2 = random.choice(v2_pages)
    print(f"📄 英文V2页面: {en_v2}")
else:
    print("⚠️ 未找到英文V2页面")

if v3_pages:
    en_v3 = random.choice(v3_pages)
    print(f"📄 英文V3页面: {en_v3}")
else:
    print("⚠️ 未找到英文V3页面")

# 中文版（台湾）
print("\n" + "=" * 80)
print("🎲 随机抽取中文台湾版页面")
print("=" * 80)

tw_dir = 'zh-TW'
if os.path.exists(tw_dir):
    tw_files = [f for f in os.listdir(tw_dir) if f.endswith('.html')]
    tw_original = [f for f in tw_files if '-v2' not in f and '-v3' not in f and ('statement' in f or 'accounting' in f or 'solution' in f)]
    tw_v2 = [f for f in tw_files if '-v2.html' in f]
    tw_v3 = [f for f in tw_files if '-v3.html' in f]
    
    if tw_original:
        print(f"\n📄 台湾原始页面: zh-TW/{random.choice(tw_original)}")
    if tw_v2:
        print(f"📄 台湾V2页面: zh-TW/{random.choice(tw_v2)}")
    if tw_v3:
        print(f"📄 台湾V3页面: zh-TW/{random.choice(tw_v3)}")

# 中文版（香港）
print("\n" + "=" * 80)
print("🎲 随机抽取中文香港版页面")
print("=" * 80)

hk_dir = 'zh-HK'
if os.path.exists(hk_dir):
    hk_files = [f for f in os.listdir(hk_dir) if f.endswith('.html')]
    hk_original = [f for f in hk_files if '-v2' not in f and '-v3' not in f and ('statement' in f or 'accounting' in f or 'solution' in f)]
    hk_v2 = [f for f in hk_files if '-v2.html' in f]
    hk_v3 = [f for f in hk_files if '-v3.html' in f]
    
    if hk_original:
        print(f"\n📄 香港原始页面: zh-HK/{random.choice(hk_original)}")
    if hk_v2:
        print(f"📄 香港V2页面: zh-HK/{random.choice(hk_v2)}")
    if hk_v3:
        print(f"📄 香港V3页面: zh-HK/{random.choice(hk_v3)}")

print("\n" + "=" * 80)
