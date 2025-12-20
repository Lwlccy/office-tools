import os
import base64
import fitz  # PyMuPDF
import httpx # 引入底层网络库
from openai import OpenAI

# ================= ⚙️ 配置区 =================
API_KEY = "sk-iSs9beacc5a664f4a0e9d7572971082efb6ad603d56bVpeQ"
API_BASE_URL = "https://api.gptsapi.net/v1" 
MODEL_NAME = "gpt-4o"

# 🔴 网络模式开关 (关键修改)
# 如果是 False：强制直连 (中转站通常用这个)
# 如果是 True ：强制走梯子 (如果直连卡死，改成 True 试试)
USE_PROXY = False 
PROXY_URL = "http://127.0.0.1:7890"

PROJECT_ROOT = "../Math_Question_Bank"
INPUT_FOLDER = os.path.join(PROJECT_ROOT, "_Work_Bench/PDF_Source")
OUTPUT_FOLDER = os.path.join(PROJECT_ROOT, "_Work_Bench/AI_Output")
# ============================================

def encode_image(image_bytes):
    return base64.b64encode(image_bytes).decode('utf-8')

def convert_with_gpt():
    # --- 核心修改：适配 httpx 新版语法 ---
    if USE_PROXY:
        print("🌐 网络模式：强制使用本地代理 (7890)")
        # 新版 httpx 参数名变成了 'proxy' (单数)
        http_client = httpx.Client(proxy=PROXY_URL)
    else:
        print("🌐 网络模式：强制直连 (不走代理)")
        # trust_env=False 意思是：完全忽略系统环境变量里的代理设置，强制直连
        http_client = httpx.Client(trust_env=False)

    # 初始化 OpenAI ... (下面保持不变)
    client = OpenAI(
        api_key=API_KEY,
        base_url=API_BASE_URL,
        http_client=http_client
    )
    # ----------------------------------

    # 初始化 OpenAI，注入自定义的 http_client
    client = OpenAI(
        api_key=API_KEY,
        base_url=API_BASE_URL,
        http_client=http_client  # <--- 注入点
    )
    # -------------------------------

    if not os.path.exists(INPUT_FOLDER):
        print(f"❌ 找不到输入文件夹: {INPUT_FOLDER}")
        return
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    files = [f for f in os.listdir(INPUT_FOLDER) if f.lower().endswith(".pdf")]
    print(f"🚀 [GPT-4o 引擎] 发现 {len(files)} 个文件，准备启动...\n")

    for filename in files:
        pdf_path = os.path.join(INPUT_FOLDER, filename)
        md_filename = os.path.splitext(filename)[0] + ".md"
        output_path = os.path.join(OUTPUT_FOLDER, md_filename)
        
        print(f"📘 正在处理: {filename}")
        
        doc = fitz.open(pdf_path)
        full_text = ""

        for page_num, page in enumerate(doc):
            print(f"   -> 正在识别第 {page_num + 1}/{len(doc)} 页...", end="", flush=True)
            
            try:
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                img_bytes = pix.tobytes("png")
                base64_image = encode_image(img_bytes)

                prompt = """
                你是一个数学题库录入员。请将这张图片里的内容转录为 Markdown。
                要求：
                1. 题目结构：## 第 X 题... ### 解析...
                2. 公式：LaTeX ($...$)。
                3. 标点：中文全角。
                4. 排除页眉页脚。
                """

                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/png;base64,{base64_image}",
                                        "detail": "high"
                                    },
                                },
                            ],
                        }
                    ],
                    temperature=0.0,
                )
                
                page_content = response.choices[0].message.content
                full_text += page_content + "\n\n"
                print(" ✅ 完成")

            except Exception as e:
                print(f" ❌ 出错: {e}")
                # 如果直连报错，提示用户去改代码
                if "ConnectError" in str(e) or "Timeout" in str(e):
                    print("💡 提示：连接超时。请尝试将脚本开头的 USE_PROXY 改为 True 再试。")

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(full_text)
        
        print(f"🎉 文件已保存: {output_path}\n")

if __name__ == "__main__":
    convert_with_gpt()