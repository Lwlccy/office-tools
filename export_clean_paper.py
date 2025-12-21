import os
import re

def export_no_yaml():
    # ================= ⚙️ 配置区 =================
    # 1. 输入文件
    # 注意中间多了一层目录
    INPUT_FILE = "../Math_Question_Bank/01_Real_Exams/2026 初数真题_解析.md"
    
    # 2. 输出文件
    # 同样需要加上中间这一层目录
    OUTPUT_FILE = "../Math_Question_Bank/_Work_Bench/2026_真题_纯净版.md"
    
    # 3. 是否删除解析？ (True=试卷, False=讲义)
    REMOVE_ANALYSIS = False 
    # ========================================

    if not os.path.exists(INPUT_FILE):
        print(f"❌ 找不到文件: {INPUT_FILE}")
        return

    print(f"🧹 正在清洗文件: {os.path.basename(INPUT_FILE)} ...")

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # --- 核心修改：删除 ``` 包裹的元数据块 ---
    # 解释：
    # ^```      -> 匹配行首的 ```
    # [\w]*     -> 匹配可能存在的语言标记 (比如 ```yaml)
    # [\s\S]*?  -> 吃掉中间所有内容 (非贪婪模式)
    # ^```      -> 直到遇到行首的 ``` 结束
    yaml_pattern = re.compile(r'^```[\w]*[\s\S]*?^```', re.MULTILINE)
    content = yaml_pattern.sub('', content)

    # --- 删除解析 (保留题目) ---
    if REMOVE_ANALYSIS:
        # 匹配 "### 解析" 及其后面的内容
        analysis_pattern = re.compile(r'###\s*解析[\s\S]*?(?=(## 第|$))', re.DOTALL)
        content = analysis_pattern.sub('\n<br><br>\n', content)

    # --- 清理多余空行 ---
    content = re.sub(r'\n{3,}', '\n\n', content)

    # --- 注入 CSS 样式 ---
    style = """<style>
    body { font-family: "Songti SC", serif; font-size: 16px; line-height: 1.6; margin: 2cm; }
    h1 { text-align: center; }
    img { max-width: 60%; display: block; margin: 10px auto; }
    li { margin-bottom: 12px; }
</style>

"""
    final_content = style + content.strip()

    # 保存
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(final_content)

    print(f"✅ 成功！纯净版已生成: {OUTPUT_FILE}")

if __name__ == "__main__":
    export_no_yaml()