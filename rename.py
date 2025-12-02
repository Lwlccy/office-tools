import os
import re

def rename_files_final():
    # ================= 配置区 =================
    # 🔴 安全开关：True = 预览模式； False = 执行改名
    SIMULATE_MODE = False 
    
    # 固定的后缀文字
    FIXED_SUFFIX = "初数真题_解析.docx"
    # ========================================

    current_folder = os.getcwd()
    # 扫描所有 docx 文件，排除临时文件
    files = [f for f in os.listdir(current_folder) if f.endswith(".docx") and not f.startswith("~$")]
    
    print(f"📂 扫描到 {len(files)} 个文件，开始处理...\n")

    count_renamed = 0

    for filename in files:
        # 1. 提取开头的年份 (4位数字)
        year_match = re.match(r'^(\d{4})', filename)
        
        # 如果连年份都找不到，直接跳过
        if not year_match:
            print(f"⚠️ 跳过 (无年份): {filename}")
            continue
        
        year = year_match.group(1)
        
        # 2. 判断是不是 10月
        # 逻辑：年份后面紧跟 分隔符(点/杠/空格) + 10 + 非数字字符
        # 例子：2013.10-xxx, 2012.10xxx
        is_october = re.search(r'^\d{4}[.\- ]*10(\D|$)', filename)
        
        # 3. 构造新名字
        if is_october:
            # 方案：2012.10 初数真题_解析.docx
            new_name = f"{year}.10 {FIXED_SUFFIX}"
        else:
            # 方案：2004 初数真题_解析.docx (包含1月和无月份的情况)
            new_name = f"{year} {FIXED_SUFFIX}"

        # 4. 检查是否需要改名
        if filename == new_name:
            continue # 名字已经符合要求，跳过

        # 5. 执行或预览
        if SIMULATE_MODE:
            # 为了对齐好看，用了 ljust
            print(f"预览: {filename[:25].ljust(30)} --->  ✅ {new_name}")
        else:
            try:
                src = os.path.join(current_folder, filename)
                dst = os.path.join(current_folder, new_name)
                
                if os.path.exists(dst):
                    print(f"❌ 失败 (目标已存在): {new_name}")
                else:
                    os.rename(src, dst)
                    print(f"已重命名: {new_name}")
                    count_renamed += 1
            except Exception as e:
                print(f"❌ 出错: {e}")

    print("\n" + "-" * 40)
    if SIMULATE_MODE:
        print("💡 当前是【预览模式】，文件未变动。")
        print("   请检查上方箭头右侧的名字是否正确。")
        print("   确认无误后，将代码第 6 行改为 False 再运行。")
    else:
        print(f"🎉 处理完成！共重命名 {count_renamed} 个文件。")

if __name__ == "__main__":
    rename_files_final()