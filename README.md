# 🛠️ 自动化题库处理工具 (Office Automation Tools)

这是一个基于 Python 的办公自动化工具集，专门用于批量处理 Word 题库文档。
它可以帮助你从文件名清洗、自动编号固化，到最终的内容解析删除与排版，实现全流程自动化。

## 🚀 功能列表

本项目包含三个核心脚本：

1.  **`rename.py`** (Mac/Windows)
    *   **功能**：批量重命名混乱的文件。
    *   **逻辑**：将 `2013.10-修改版.docx` 统一格式化为 `2013.10 初数真题_解析.docx`。
    *   **特点**：支持正则提取年份月份，带安全预览模式。

2.  **`convert_numbers.py`** (Windows Only)
    *   **功能**：解决 Word 自动编号无法被 Python 读取的问题。
    *   **逻辑**：调用 Word 原生 COM 接口，将自动编号列表转换为纯文本数字。
    *   **注意**：需要在 Windows 环境下运行，依赖 Office Word 软件。

3.  **`final_tools.py`** (Mac/Windows)
    *   **功能**：深度清理与排版。
    *   **逻辑**：
        *   删除【解析】、【答案】等特定段落。
        *   智能保留题目与大标题。
        *   自动处理题目间的空行排版。
        *   **自动改名**：处理完成后，自动移除文件名中的“_解析”字样。

## 📦 环境要求

*   Python 3.x
*   依赖库：
    ```bash
    pip install python-docx
    pip install pywin32  # 仅 Windows 端需要
    ```

## 📖 使用流程 (SOP)

建议按照以下顺序操作以获得最佳效果：

### 第 1 步：文件重命名 (Mac)
将所有原始 Word 文档放入文件夹，运行：
```bash
python rename.py
```

### 第 2 步：固化编号 (Windows)
将重命名后的文件复制到 Windows 环境，运行：
```Bash
python convert_numbers.py
```

### 第 3 步：清理与排版 (Mac)
将处理好的文件放回 Mac，运行：
```Bash
python final_tools.py
```

最终结果将生成在 最终结果 文件夹中。