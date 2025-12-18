import os
import time
from google import genai
from google.genai import types

# ================= 🌐 网络通行证 =================
os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"

# ================= ⚙️ 配置区 =================
API_KEY = "AIzaSyCxUqmWepe5UxSfGeCaS7Hf99ttsj6Otwo"  # <--- 别忘了检查这里

PROJECT_ROOT = "../Math_Question_Bank"
INPUT_FOLDER = os.path.join(PROJECT_ROOT, "_Work_Bench/PDF_Source")
OUTPUT_FOLDER = os.path.join(PROJECT_ROOT, "_Work_Bench/AI_Output")

# ===================================================

def convert_pdf_with_new_sdk():
    client = genai.Client(api_key=API_KEY)

    if not os.path.exists(INPUT_FOLDER):
        print(f"❌ 错误：找不到输入文件夹: {INPUT_FOLDER}")
        return
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    files = [f for f in os.listdir(INPUT_FOLDER) if f.lower().endswith(".pdf")]
    if not files:
        print("⚠️  没有找到 PDF 文件。")
        return

    print(f"🚀 [新版引擎] 发现 {len(files)} 个文件，准备启动...\n")

    for filename in files:
        pdf_path = os.path.join(INPUT_FOLDER, filename)
        md_filename = os.path.splitext(filename)[0] + ".md"
        output_path = os.path.join(OUTPUT_FOLDER, md_filename)

        print(f"🤖 正在上传: {filename} ... ", end="", flush=True)

        try:
            # --- 核心修改：指定 mime_type ---
            with open(pdf_path, "rb") as f:
                file_ref = client.files.upload(
                    file=f,
                    config=types.UploadFileConfig(
                        display_name="temp_pdf_upload",
                        mime_type="application/pdf"  # 告诉AI这是PDF
                    )
                )
            print("✅ 上传成功 | 正在思考...", end="", flush=True)
            # --------------------------------

            prompt = """
            任务：你是一个专业的数学题库录入员（OCR模式）。将PDF转录为Markdown。
            
            【红线规则】：
            1. 🚫 严禁解题、严禁翻译、严禁废话。
            2. 🚫 去除题号（如 "1. "），提取答案。
            
            【格式要求】：
            1. 结构：
               ## 第 X 题
               ### 题目
               (题干 + 选项列表)
               ### 解析
               **【答案】** X
               **【解析内容】** ...
               ---
            2. 公式：全部使用 LaTeX ($...$)。
            3. 标点：中文用全角，公式内用半角。
            4. 图片：> ![待截图](assets/占位.png)
            """

            response = client.models.generate_content(
                model='gemini-2.0-flash', 
                contents=[file_ref, prompt],
                config=types.GenerateContentConfig(
                    temperature=0.0
                )
            )

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            print(f" ✅ 转换完成！")

        except Exception as e:
            print(f"\n❌ 出错: {e}")

    print("\n" + "="*30)
    print("🎉 全部完成！")

if __name__ == "__main__":
    convert_pdf_with_new_sdk()