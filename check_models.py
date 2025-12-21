import google.generativeai as genai
import os

# 1. 网络代理 (必须加，否则连不上)
os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"

# 2. API Key
genai.configure(api_key="api_key")

print("正在查询可用模型列表...")

try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"✅ 可用模型: {m.name}")
except Exception as e:
    print(f"❌ 查询失败: {e}")