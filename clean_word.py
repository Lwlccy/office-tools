import re
from docx import Document
import os

def clean_paper_universal():
    input_filename = "input.docx"   
    output_filename = "output_universal.docx"

    if not os.path.exists(input_filename):
        print(f"❌ 错误：找不到文件 '{input_filename}'")
        return

    print("正在读取文档...")
    doc = Document(input_filename)
    
    # 1. 删除关键词 (你可以随时在这里添加新的)
    delete_keywords = ["【答案】", "【解析】", "【知识点】", "【分析】"]
    
    # 2. 🤖 超级正则表达式 🤖
    # 这个 pattern 用了 "|" (或) 符号，把多种情况组合在一起
    # 含义：
    #   ^[\(（]\d{4}      --> 匹配 "(2007" 或 "（2008"
    #   |                --> 或者
    #   ^\d+\s*[.．、]    --> 匹配 "数字" + "点/顿号" (如 1. 或 1、 或 10．)
    pattern_string = r'(^[\(（]\d{4})|(^\d+\s*[.．、])'
    new_question_pattern = re.compile(pattern_string)
    
    paragraphs_to_delete = [] 
    is_in_delete_zone = False 
    question_count = 0

    for paragraph in doc.paragraphs:
        text = paragraph.text.strip()
        
        if not text:
            continue

        # --- A. 检查是否是新题目 ---
        if new_question_pattern.match(text):
            is_in_delete_zone = False 
            question_count += 1
            
            # 打印前15个字符，方便你检查它识别了什么
            print(f"识别到第 {question_count} 题: {text[:15]}...") 
            
            # 加空行
            paragraph.insert_paragraph_before("") 
            paragraph.insert_paragraph_before("") 
            paragraph.insert_paragraph_before("") 
            continue

        # --- B. 检查是否要开始删除 ---
        for keyword in delete_keywords:
            if text.startswith(keyword):
                is_in_delete_zone = True
                break
        
        # --- C. 标记删除 ---
        if is_in_delete_zone:
            paragraphs_to_delete.append(paragraph)

    # --- D. 执行删除 ---
    for p in paragraphs_to_delete:
        p_element = p._element
        if p_element.getparent() is not None:
            p_element.getparent().remove(p_element)

    doc.save(output_filename)
    print("------------------------------------------------")
    print(f"✅ 处理完成！共识别出 {question_count} 道题目。")
    print(f"文件已保存为：{output_filename}")

if __name__ == "__main__":
    clean_paper_universal()