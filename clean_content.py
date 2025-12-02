import os
import re
from docx import Document

# --- 单个文件处理核心逻辑 (保持 v4.0 的完美逻辑) ---
def process_one_file(file_path, save_path):
    try:
        doc = Document(file_path)
        
        # 1. 关键词
        delete_keywords = ["【答案】", "【解析】", "【知识点】", "【分析】", "【详解】", "【点睛】"]
        
        # 2. 题目识别正则
        question_pattern = re.compile(r'(^[\(（]\d{4})|(^\d+\s*[.．、])')

        # 3. 大标题识别正则
        section_header_pattern = re.compile(r'^[一二三四五六七八九十]+、')
        
        paragraphs_to_delete = [] 
        is_in_delete_zone = False 
        question_count = 0
        
        # 等待大标题后的第一题
        waiting_for_first_question_after_header = False 

        for paragraph in doc.paragraphs:
            text = paragraph.text.strip()
            
            # --- 图片处理 ---
            if not text:
                if is_in_delete_zone:
                    paragraphs_to_delete.append(paragraph)
                continue

            # --- A. 检查大标题 ---
            if section_header_pattern.match(text):
                is_in_delete_zone = False  
                waiting_for_first_question_after_header = True 
                continue 

            # --- B. 检查新题目 ---
            if question_pattern.match(text):
                is_in_delete_zone = False 
                question_count += 1
                
                # 智能加空行逻辑
                if waiting_for_first_question_after_header:
                    # 大标题后第一题 -> 不加空行
                    waiting_for_first_question_after_header = False
                else:
                    # 普通题目 -> 加空行
                    paragraph.insert_paragraph_before("") 
                    paragraph.insert_paragraph_before("") 
                    paragraph.insert_paragraph_before("") 
                
                continue

            # --- C. 检查解析关键词 ---
            for keyword in delete_keywords:
                if text.startswith(keyword):
                    is_in_delete_zone = True
                    break
            
            # --- D. 标记删除 ---
            if is_in_delete_zone:
                paragraphs_to_delete.append(paragraph)

        # --- 执行删除 ---
        for p in paragraphs_to_delete:
            p_element = p._element
            if p_element.getparent() is not None:
                p_element.getparent().remove(p_element)

        doc.save(save_path)
        return True, question_count

    except Exception as e:
        print(f"❌ 出错: {os.path.basename(file_path)} -> {e}")
        return False, 0

# --- 主程序 (✨ 这里更新了自动改名逻辑 ✨) ---
def main():
    current_folder = os.getcwd()
    # 输出文件夹
    output_folder = os.path.join(current_folder, "最终结果")
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 扫描所有 .docx 文件
    all_files = [f for f in os.listdir(current_folder) if f.endswith(".docx") and not f.startswith("~$") and "最终结果" not in f]

    if not all_files:
        print("⚠️  没找到 Word 文档！")
        return

    print(f"🚀 开始处理 {len(all_files)} 个文件...\n")

    total_success = 0
    for filename in all_files:
        input_path = os.path.join(current_folder, filename)
        
        # --- ⭐ 自动改名逻辑在这里 ⭐ ---
        # 1. 把 "_解析" 替换为空
        # 2. 如果还有 "解析" 两个字，也替换为空 (双重保险)
        new_filename = filename.replace("_解析", "").replace("解析", "")
        
        # 确保还是 .docx 结尾 (防止误删后缀)
        if not new_filename.endswith(".docx"):
            new_filename += ".docx"
            
        # 组合新的保存路径
        output_path = os.path.join(output_folder, new_filename)
        
        print(f"处理: {filename} -> 生成: {new_filename} ... ", end="")
        success, count = process_one_file(input_path, output_path)
        
        if success:
            print(f"✅ (题量:{count})")
            total_success += 1

    print("\n" + "="*30)
    print(f"🎉 全部搞定！成功处理 {total_success} 个文件。")
    print(f"📂 请打开【最终结果】文件夹查看，你会发现文件名里的'解析'都不见了！")

if __name__ == "__main__":
    main()