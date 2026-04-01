#!/usr/bin/env python3
"""
🔥 只恢复到16:00版本，不删除任何内容

只做恢复操作，不修改任何代码
"""

import subprocess

def restore_to_1600_only():
    """只恢复到16:00版本"""
    
    files = [
        'en/document-detail.html',
        'jp/document-detail.html',
        'kr/document-detail.html',
        'document-detail.html'
    ]
    
    # 使用今天16:23的 commit
    commit_hash = '543c43f276fbabba15397aab35e0c4a2b42012e5'
    
    print(f"恢复到 commit: {commit_hash}")
    print(f"时间: 2026-01-03 16:23:00")
    print("=" * 60)
    
    for file in files:
        try:
            cmd = f'git show {commit_hash}:{file}'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                with open(file, 'w', encoding='utf-8') as f:
                    f.write(result.stdout)
                print(f"✅ 已恢复 {file}")
            else:
                print(f"⚠️ 未找到 {file} 在该版本")
        except Exception as e:
            print(f"❌ 恢复 {file} 失败: {e}")

def main():
    print("🔥 恢复到今天16:00版本（不删除任何内容）\n")
    print("=" * 60)
    restore_to_1600_only()
    print("=" * 60)
    print("\n✅ 恢复完成！")
    print("\n🚀 请刷新页面测试！")
    print("• 页面应该恢复到16:00的状态")
    print("• 所有功能应该正常工作")

if __name__ == '__main__':
    main()

