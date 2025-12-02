import os
import win32com.client as win32
from pathlib import Path

def batch_convert_numbers_to_text():
    # 1. 获取当前脚本所在的文件夹
    current_folder = os.getcwd()
    
    # 2. 启动 Word 应用程序 (在后台运行，你看不到界面)
    print("⏳ 正在启动 Word 引擎...")
    try:
        word = win32.gencache.EnsureDispatch('Word.Application')
    except AttributeError:
        # 如果缓存出错，强制使用动态调度
        word = win32.Dispatch('Word.Application')
        
    word.Visible = False # 不显示 Word 界面，后台静默处理
    word.DisplayAlerts = 0 # 不弹窗警告

    # 3. 扫描文件夹里的 docx 文件
    files = [f for f in os.listdir(current_folder) if f.endswith(".docx") and not f.startswith("~$")]
    
    if not files:
        print("❌ 当前文件夹里没有 Word 文档！")
        return

    print(f"🔍 发现 {len(files)} 个文件，准备开始“编号固化”处理...\n")

    count = 0
    for filename in files:
        file_path = os.path.join(current_folder, filename)
        abs_path = str(Path(file_path).resolve()) # Word 需要绝对路径
        
        try:
            print(f"正在处理: {filename} ...", end="")
            
            # 打开文档
            doc = word.Documents.Open(abs_path)
            
            # ⭐ 核心核心核心：调用 Word 的原生功能 ⭐
            # 这行代码等同于你在 Word 里运行 VBA: ActiveDocument.ConvertNumbersToText
            doc.ConvertNumbersToText()
            
            # 保存并关闭
            doc.Save()
            doc.Close()
            
            print(" ✅ 完成")
            count += 1
            
        except Exception as e:
            print(f" ❌ 失败! 原因: {e}")
            # 如果出错，尝试强行关闭当前文档，以免卡住
            try:
                doc.Close(SaveChanges=False)
            except:
                pass

    # 4. 退出 Word
    word.Quit()
    print("\n" + "="*30)
    print(f"🎉 全部搞定！共处理 {count} 个文件。")
    print("现在这些文件里的编号都已经变成纯文本了，可以用之前的 Mac 脚本去清理了！")

if __name__ == "__main__":
    batch_convert_numbers_to_text()
