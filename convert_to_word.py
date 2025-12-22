import os
import re
import subprocess

def export_md_to_docx():
    # ================= ⚙️ 配置区 =================
    # 1. 输入文件 (你的 Markdown 讲义/试卷)
    INPUT_FILE = "Math_Question_Bank/_Work_Bench/2026 初数真题解析_纯净版.md"
    
    # 2. 输出文件
    OUTPUT_FILE = "Math_Question_Bank/_Work_Bench/2026 初数真题解析_Word版.docx"
    # ========================================

    if not os.path.exists(INPUT_FILE):
        print(f"❌ 找不到文件: {INPUT_FILE}")
        return

    print(f"📖 正在读取: {os.path.basename(INPUT_FILE)} ...")
    
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # --- 步骤 1: 清洗数据 (Word 不认识 CSS/HTML) ---
    
    # 1. 删除 <style>...</style> 块
    content = re.sub(r'<style>[\s\S]*?</style>', '', content)
    
    # 2. 删除 HTML 表头 (<div class="paper-header">...</div>)
    # 并尝试提取标题文字，还原成 Markdown 标题
    # (这里做一个简单的处理：直接删掉 HTML 标签，提取里面的中文)
    def restore_header(match):
        html_block = match.group(0)
        # 简单提取 h1 内容
        h1_match = re.search(r'<h1>(.*?)</h1>', html_block)
        if h1_match:
            return f"# {h1_match.group(1)}\n\n" # 变回 Markdown 一级标题
        return ""

    content = re.sub(r'<div class="paper-header">[\s\S]*?</div>', restore_header, content)

    # 3. 删除其他 HTML 标签 (如 <br>)，Word 会自动处理换行
    content = content.replace('<br>', '\n')
    content = content.replace('&nbsp;', ' ')

    # --- 步骤 2: 生成临时文件 ---
    temp_md = "temp_for_word.md"
    with open(temp_md, 'w', encoding='utf-8') as f:
        f.write(content)

    # --- 步骤 3: 调用 Pandoc 转换 ---
    # 核心命令：pandoc input.md -o output.docx
    print("🔄 正在召唤 Pandoc 进行转换...")
    
    try:
        # 检查是否安装了 pandoc
        subprocess.run(["pandoc", "--version"], check=True, stdout=subprocess.PIPE)
        
        # 执行转换
        subprocess.run([
            "pandoc", 
            temp_md, 
            "-o", OUTPUT_FILE
        ], check=True)
        
        print(f"✅ Word 文档已生成: {OUTPUT_FILE}")
        print("👉 提示：公式已自动转为 Word 原生格式，你可以直接编辑！")

    except FileNotFoundError:
        print("❌ 错误：你的电脑没装 Pandoc！请先去下载安装。")
    except Exception as e:
        print(f"❌ 转换出错: {e}")
    finally:
        # 清理临时文件
        if os.path.exists(temp_md):
            os.remove(temp_md)

if __name__ == "__main__":
    export_md_to_docx()