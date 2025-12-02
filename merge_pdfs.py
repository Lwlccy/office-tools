import os
from PyPDF2 import PdfMerger

def merge_pdfs_with_bookmarks():
    # ================= 配置区 =================
    # 合并后的文件名
    OUTPUT_FILENAME = "合并后的完整版(带目录).pdf"
    # ========================================

    current_folder = os.getcwd()
    merger = PdfMerger()

    # 1. 扫描 PDF 文件
    # 排除掉脚本自己生成的结果文件，防止递归
    files = [f for f in os.listdir(current_folder) 
             if f.lower().endswith(".pdf") and f != OUTPUT_FILENAME]
    
    # 2. 排序 (非常重要！)
    # 电脑默认排序是 1, 10, 2。
    # 如果你的文件名是 "1.第一章", "2.第二章"，建议改为 "01.第一章", "02.第二章"
    files.sort()

    if not files:
        print("⚠️  没找到 PDF 文件。")
        return

    print(f"🔍 发现 {len(files)} 个文件，开始合并并生成目录...\n")

    for filename in files:
        file_path = os.path.join(current_folder, filename)
        
        # 3. 制作目录标题
        # 去掉后缀名 (.pdf)
        bookmark_name = os.path.splitext(filename)[0]
        
        # (可选) 如果你文件名里有 "01. ", "2020- " 这种前缀想去掉，可以用 replace
        # bookmark_name = bookmark_name.replace("初数真题", "") 

        print(f"📖 添加章节: [{bookmark_name}]")
        
        # 4. 核心步骤：合并的同时添加书签
        # outline_item 参数就是侧边栏显示的目录名字
        merger.append(file_path, outline_item=bookmark_name)

    # 5. 保存
    output_path = os.path.join(current_folder, OUTPUT_FILENAME)
    merger.write(output_path)
    merger.close()

    print("\n" + "="*30)
    print(f"🎉 成功！文件已生成: {OUTPUT_FILENAME}")
    print("👉 打开 PDF 后，请点击软件左侧的【书签/目录】图标查看效果。")

if __name__ == "__main__":
    merge_pdfs_with_bookmarks()