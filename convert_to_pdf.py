import os
import win32com.client as win32
from pathlib import Path

def batch_word_to_pdf():
    # ================= 配置区 =================
    OUTPUT_FOLDER_NAME = "PDF导出结果"
    # ========================================

    current_folder = os.getcwd()
    output_path = os.path.join(current_folder, OUTPUT_FOLDER_NAME)

    # 1. 创建输出文件夹
    if not os.path.exists(output_path):
        os.makedirs(output_path)
        print(f"📂 已新建文件夹: {OUTPUT_FOLDER_NAME}")

    # 2. 扫描所有 Word 文件 (.docx 和 .doc)
    files = [f for f in os.listdir(current_folder) 
             if (f.lower().endswith(".docx") or f.lower().endswith(".doc")) 
             and not f.startswith("~$")]

    if not files:
        print("⚠️  当前文件夹里没有找到 Word 文档。")
        return

    print(f"🔍 发现 {len(files)} 个文档，准备开始导出 PDF...\n")
    print("⏳ 正在启动 Word 引擎...")

    try:
        word = win32.gencache.EnsureDispatch('Word.Application')
    except AttributeError:
        word = win32.Dispatch('Word.Application')

    word.Visible = False
    word.DisplayAlerts = 0

    success_count = 0

    for filename in files:
        try:
            # 构造路径
            input_file = os.path.join(current_folder, filename)
            abs_input_path = str(Path(input_file).resolve())
            
            # 构造输出文件名 (把后缀换成 .pdf)
            name_without_ext = os.path.splitext(filename)[0]
            pdf_filename = name_without_ext + ".pdf"
            abs_output_path = str(Path(os.path.join(output_path, pdf_filename)).resolve())

            # 如果 PDF 已存在，跳过
            if os.path.exists(abs_output_path):
                print(f"跳过 (已存在): {pdf_filename}")
                continue

            print(f"导出中: {filename} ... ", end="")

            # 打开文档
            doc = word.Documents.Open(abs_input_path)
            
            # 核心：导出为 PDF
            # 17 = wdExportFormatPDF
            doc.ExportAsFixedFormat(abs_output_path, ExportFormat=17)
            
            doc.Close(SaveChanges=False)
            print("✅ 成功")
            success_count += 1

        except Exception as e:
            print(f"❌ 失败: {e}")
            try:
                doc.Close(SaveChanges=False)
            except:
                pass

    word.Quit()
    print("\n" + "="*30)
    print(f"🎉 全部完成！共生成 {success_count} 个 PDF 文件。")
    print(f"📁 PDF 已保存在: {OUTPUT_FOLDER_NAME}")

if __name__ == "__main__":
    batch_word_to_pdf()