#!/usr/bin/env python3
"""
🔥 恢复到15:00版本（15:13）

只恢复，不删除任何内容
"""

import subprocess

def restore_to_1500():
    """恢复到15:00版本"""
    
    files = [
        'en/document-detail.html',
        'jp/document-detail.html',
        'kr/document-detail.html',
        'document-detail.html'
    ]
    
    # 使用15:13的 commit
    commit_hash = 'b096f9a5b2324df7bc0f1b3d959286301e8ccea5'
    
    print(f"恢复到 commit: {commit_hash}")
    print(f"时间: 2026-01-03 15:13:19")
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
    print("🔥 恢复到今天15:00版本\n")
    print("=" * 60)
    restore_to_1500()
    print("=" * 60)
    print("\n✅ 恢复完成！")
    print("\n🚀 请刷新页面测试！")

if __name__ == '__main__':
    main()

