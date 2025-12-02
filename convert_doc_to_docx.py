import os
import win32com.client as win32
from pathlib import Path

def batch_convert_doc_to_docx():
    current_folder = os.getcwd()
    
    # 1. 扫描所有 .doc 文件 (排除已经是 .docx 的，也排除临时文件)
    # 注意：endswith(".doc") 会匹配 .docx，所以要特判
    files = [f for f in os.listdir(current_folder) 
             if f.lower().endswith(".doc") 
             and not f.lower().endswith(".docx") 
             and not f.startswith("~$")]

    if not files:
        print("⚠️  当前文件夹里没有找到 .doc 文件。")
        return

    print(f"🔍 发现 {len(files)} 个 .doc 文件，准备开始转换...\n")
    print("⏳ 正在启动 Word 引擎...")

    try:
        # 启动 Word
        word = win32.gencache.EnsureDispatch('Word.Application')
    except AttributeError:
        word = win32.Dispatch('Word.Application')

    word.Visible = False
    word.DisplayAlerts = 0

    success_count = 0

    for filename in files:
        # 获取绝对路径 (Windows COM 需要绝对路径)
        doc_path = os.path.join(current_folder, filename)
        abs_doc_path = str(Path(doc_path).resolve())
        
        # 构造输出路径 (.doc -> .docx)
        docx_filename = filename + "x" 
        abs_docx_path = str(Path(os.path.join(current_folder, docx_filename)).resolve())

        # 如果目标文件已存在，跳过
        if os.path.exists(abs_docx_path):
            print(f"跳过 (已存在): {docx_filename}")
            continue

        try:
            print(f"转换中: {filename} ... ", end="")
            
            # 打开 .doc
            doc = word.Documents.Open(abs_doc_path)
            
            # 另存为 .docx
            # FileFormat=12 代表 wdFormatXMLDocument (即 .docx 格式)
            doc.SaveAs2(abs_docx_path, FileFormat=12)
            
            doc.Close()
            print("✅ 成功")
            success_count += 1
            
            # (可选) 转换成功后删除原文件，想保留原文件就把下面这行注释掉
            # os.remove(abs_doc_path) 

        except Exception as e:
            print(f"❌ 失败: {e}")
            try:
                doc.Close(SaveChanges=False)
            except:
                pass

    word.Quit()
    print("\n" + "="*30)
    print(f"🎉 转换完成！共生成 {success_count} 个 .docx 文件。")

if __name__ == "__main__":
    batch_convert_doc_to_docx()