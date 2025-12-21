import os
import time
from google import genai
from google.genai import types

# ================= ⚙️ 配置区 =================
API_KEY = "api_key"
API_BASE_URL = "https://api.gptsapi.net"

PROJECT_ROOT = "../Math_Question_Bank"
INPUT_FOLDER = os.path.join(PROJECT_ROOT, "_Work_Bench/PDF_Source")
OUTPUT_FOLDER = os.path.join(PROJECT_ROOT, "_Work_Bench/AI_Output")

# ===================================================

def convert_pdf_pro_max():
    client = genai.Client(
        api_key=API_KEY,
        http_options={
            'base_url': API_BASE_URL,
            'api_version': 'v1beta'
        }
    )

    if not os.path.exists(INPUT_FOLDER):
        print(f"❌ 错误：找不到输入文件夹: {INPUT_FOLDER}")
        return
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    files = [f for f in os.listdir(INPUT_FOLDER) if f.lower().endswith(".pdf")]
    
    print(f"🚀 [Pro增强版] 发现 {len(files)} 个文件，准备启动...\n")

    for i, filename in enumerate(files):
        pdf_path = os.path.join(INPUT_FOLDER, filename)
        md_filename = os.path.splitext(filename)[0] + ".md"
        output_path = os.path.join(OUTPUT_FOLDER, md_filename)

        print(f"[{i+1}/{len(files)}] 🤖 正在读取并发送: {filename} ... ", end="", flush=True)

        try:
            with open(pdf_path, "rb") as f:
                pdf_data = f.read()
            
            # --- 升级版提示词：加入了【范例】，教AI做事 ---
            prompt_text = """
            任务：你是一个严谨的数学题库 OCR 专家。将 PDF 转录为 Markdown。
            
            【核心规则】：
            1. 完整性：必须转录所有题目（通常一套卷子有25道题），绝对不要半途而废！
            2. 纯净性：严禁解题，严禁翻译。不要页眉页脚。
            3. ⚠️ **完整性警告**：必须输出每一道题的【解析】部分！如果解析缺失，视为任务失败。
            
            【格式范例 (请严格模仿)】：
            
            原文："1. 甲乙两地相距..."
            输出：
            ## 第 1 题
            ### 题目
            甲乙两地相距 $100km$，速度比为 $1:2$。（注意：去掉了开头的 1.，标点全角，数字公式化）
            A. $1$ 小时
            B. $2$ 小时
            C. $3$ 小时
            D. $4$ 小时
            E. $5$ 小时
            
            ### 解析
            **【答案】** A
            **【解析内容】** 由题意得...
            
            ---
            
            【标点特别强调】：
            - 中文语境下必须用全角逗号（，）和句号（。）。
            - $公式$ 内部必须用半角符号。
            """

            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=[
                    types.Content(
                        parts=[
                            types.Part.from_bytes(
                                data=pdf_data, 
                                mime_type="application/pdf"
                            ),
                            types.Part.from_text(text=prompt_text)
                        ]
                    )
                ],
                config=types.GenerateContentConfig(
                    temperature=0.0,
                    max_output_tokens=8192  # <--- 拉满输出长度，防止写一半断掉
                )
            )

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            print(f" ✅ 成功！(长度: {len(response.text)} 字符)")

        except Exception as e:
            print(f"\n❌ 出错: {e}")

        # Pro 模型处理慢，且更贵，稍微多休息一下
        time.sleep(5)

    print("\n" + "="*30)
    print("🎉 全部完成！")

if __name__ == "__main__":
    convert_pdf_pro_max()