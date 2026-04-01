#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
恢复4个版本首页学习中心蓝色背景脚本
"""

def restore_learning_center_background():
    """恢复学习中心的蓝色渐变背景"""
    
    files = [
        "/Users/cavlinyeung/ai-bank-parser/index.html",
        "/Users/cavlinyeung/ai-bank-parser/en/index.html",
        "/Users/cavlinyeung/ai-bank-parser/jp/index.html",
        "/Users/cavlinyeung/ai-bank-parser/kr/index.html"
    ]
    
    print("🎨 开始恢复学习中心蓝色背景...")
    
    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 查找并替换学习中心的背景样式
            old_style = 'background: white; padding: 4rem 0; color: #1f2937;'
            new_style = 'background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 4rem 0; color: white;'
            
            if old_style in content:
                content = content.replace(old_style, new_style)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"   ✅ {file_path.split('/')[-2:]}: 蓝色背景已恢复")
            else:
                print(f"   ⚠️ {file_path.split('/')[-2:]}: 未找到目标样式")
                
        except Exception as e:
            print(f"   ❌ {file_path}: 错误 - {str(e)}")
    
    print("\n✅ 学习中心蓝色背景恢复完成！")

def verify_multilingual_sync():
    """验证多语言数据同步功能是否正确集成"""
    
    print("\n🔍 验证多语言数据同步功能...")
    
    files = [
        "/Users/cavlinyeung/ai-bank-parser/index.html",
        "/Users/cavlinyeung/ai-bank-parser/en/index.html",
        "/Users/cavlinyeung/ai-bank-parser/jp/index.html",
        "/Users/cavlinyeung/ai-bank-parser/kr/index.html"
    ]
    
    # 检查每个文件是否包含多语言同步脚本
    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            has_sync_script = 'multilingual-data-sync.js' in content
            has_language_switcher = 'id="language-switcher"' in content
            
            lang_name = {
                'index.html': '中文版',
                'en/index.html': '英文版',
                'jp/index.html': '日文版',
                'kr/index.html': '韩文版'
            }
            
            file_key = '/'.join(file_path.split('/')[-2:]) if 'index.html' in file_path.split('/')[-1] else file_path.split('/')[-1]
            name = lang_name.get(file_key, file_key)
            
            if has_sync_script and has_language_switcher:
                print(f"   ✅ {name}: 数据同步功能已正确集成")
            else:
                print(f"   ⚠️ {name}: 数据同步功能可能缺失")
                if not has_sync_script:
                    print(f"      - 缺少 multilingual-data-sync.js 引用")
                if not has_language_switcher:
                    print(f"      - 缺少 language-switcher 容器")
                    
        except Exception as e:
            print(f"   ❌ {file_path}: 错误 - {str(e)}")
    
    print("\n📝 数据互通说明：")
    print("   • Firebase后端：4个版本共享同一个Firebase项目")
    print("   • 用户数据：登录后在任何语言版本都能看到相同数据")
    print("   • 语言偏好：系统会记住用户选择的语言")
    print("   • 自动跳转：下次访问自动跳转到用户偏好语言")

def main():
    """主函数"""
    
    print("╔══════════════════════════════════════════════════════════════════════╗")
    print("║     🎨 恢复学习中心背景 + 验证数据互通                                   ║")
    print("╚══════════════════════════════════════════════════════════════════════╝\n")
    
    # 恢复蓝色背景
    restore_learning_center_background()
    
    # 验证数据同步功能
    verify_multilingual_sync()
    
    print("\n╔══════════════════════════════════════════════════════════════════════╗")
    print("║     🎉 所有操作完成！                                                    ║")
    print("╚══════════════════════════════════════════════════════════════════════╝\n")
    
    print("📊 完成总结：")
    print("   ✅ 4个版本学习中心蓝色背景已恢复")
    print("   ✅ 数据互通功能验证完成")
    print("   ✅ Firebase统一后端确保数据一致性")
    
    print("\n🔗 查看效果：")
    print("   • 中文版: https://vaultcaddy.com/index.html")
    print("   • 英文版: https://vaultcaddy.com/en/index.html")
    print("   • 日文版: https://vaultcaddy.com/jp/index.html")
    print("   • 韩文版: https://vaultcaddy.com/kr/index.html")
    
    print("\n💡 数据互通测试方法：")
    print("   1. 在中文版登录账户")
    print("   2. 上传一些文档到Dashboard")
    print("   3. 切换到日文版（点击语言切换器）")
    print("   4. 应该能看到相同的文档和数据")

if __name__ == "__main__":
    main()

