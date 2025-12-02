import re
from docx import Document
import os

def clean_paper_final():
    input_filename = "input.docx"   
    output_filename = "output_final.docx"

    if not os.path.exists(input_filename):
        print(f"❌ 错误：找不到文件 '{input_filename}'")
        return

    print("正在读取文档...")
    doc = Document(input_filename)
    
    # 1. 关键词
    delete_keywords = ["【答案】", "【解析】", "【知识点】", "【分析】", "【详解】", "【点睛】"]
    
    # 2. 题目识别正则 (v2.0)
    # 匹配 (2007) 或 1. 或 1、
    question_pattern = re.compile(r'(^[\(（]\d{4})|(^\d+\s*[.．、])')

    # 3. ✨ 新增：大标题识别正则 ✨
    # 匹配 "一、" "二、" "三、" 这种中文数字开头的段落
    section_header_pattern = re.compile(r'^[一二三四五六七八九十]+、')
    
    paragraphs_to_delete = [] 
    is_in_delete_zone = False 
    question_count = 0

    # 用于记录上一段是否是大标题
    last_paragraph_was_header = False

    for paragraph in doc.paragraphs:
        text = paragraph.text.strip()
        
        # --- 针对问题2的修复：图片没删掉 ---
        # 即使 text 是空的（只有图片），如果处于删除模式，也要往下走，不能直接 continue
        if not text:
            if is_in_delete_zone:
                paragraphs_to_delete.append(paragraph)
            continue

        # --- A. 检查是否是大标题 (如：一、选择题) ---
        if section_header_pattern.match(text):
            is_in_delete_zone = False  # 保护大标题不被删
            last_paragraph_was_header = True # 标记：刚才经过了大标题
            print(f"👀 发现大标题: {text[:10]}")
            continue # 大标题处理完直接进入下一循环

        # --- B. 检查是否是新题目 ---
        if question_pattern.match(text):
            is_in_delete_zone = False 
            question_count += 1
            
            # --- 针对问题1的修复：智能加空格 ---
            # 只有当上一段不是大标题时，才加空行
            if not last_paragraph_was_header:
                paragraph.insert_paragraph_before("") 
                paragraph.insert_paragraph_before("") 
                paragraph.insert_paragraph_before("") 
            else:
                print(f"   -> 第 {question_count} 题紧跟大标题，不加空格。")

            # 重置标记（因为现在是题目了，不再是大标题）
            last_paragraph_was_header = False
            continue

        # --- C. 检查是否要开始删除 ---
        for keyword in delete_keywords:
            if text.startswith(keyword):
                is_in_delete_zone = True
                break
        
        # --- D. 标记删除 ---
        # 只要在删除区，不管是不是图片，统统标记
        if is_in_delete_zone:
            paragraphs_to_delete.append(paragraph)
            # 这里不需要重置 last_paragraph_was_header，因为解析肯定不是大标题

        # 如果这一行既不是题目也不是标题，也不是要删的（比如题干的第二行），
        # 那么它就是普通内容，我们需要把“上一段是大标题”这个标记洗掉
        # 否则如果大标题下面有两行废话，第三行是题目，空格逻辑就会出错
        if not is_in_delete_zone:
             last_paragraph_was_header = False

    # --- 执行删除 ---
    for p in paragraphs_to_delete:
        p_element = p._element
        if p_element.getparent() is not None:
            p_element.getparent().remove(p_element)

    doc.save(output_filename)
    print("------------------------------------------------")
    print(f"✅ 处理完成！共识别出 {question_count} 道题目。")
    print(f"文件已保存为：{output_filename}")

if __name__ == "__main__":
    clean_paper_final()