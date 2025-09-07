#!/usr/bin/env python3
"""
主程式：協調文件預處理流程

本程式會依序執行以下處理器，轉換 Markdown 文件：
1. 圖片處理 (下載與路徑替換)
2. 內部連結轉換
3. Laravel Doc 特有的 diff 語法轉換
4. 程式碼區塊註解指令處理 (`[tl! add]` 和 `[tl! remove]`)
5. PHP 程式碼區塊標籤修正
6. 程式碼區塊 tab 語法處理

處理邏輯皆已模組化於 `processors` 目錄下。

本程式授權採用 MIT License
Copyright (c) 2025 Pigo Chu
"""

import sys
import os

# 從 processors 模組匯入所有處理函式
from processors.image_handler import process_images
from processors.link_handler import process_links
from processors.diff_handler import process_diff_blocks
from processors.php_tag_handler import process_php_tags
from processors.tab_handler import process_tabs

def convert_content(source_dir: str, output_dir: str) -> None:
    """
    主要處理函式：遍歷檔案並依序執行所有處理器
    """
    print("Starting Laravel documentation content conversion...")
    print(f"Source directory: {source_dir}")
    print(f"Output directory: {output_dir}\n")

    image_output_dir = os.path.join(output_dir, '_static', 'laravel')
    os.makedirs(image_output_dir, exist_ok=True)

    processed_count = 0
    for filename in os.listdir(source_dir):
        if not filename.endswith(".md") or not os.path.isfile(os.path.join(source_dir, filename)):
            continue

        input_file_path = os.path.join(source_dir, filename)
        output_file_path = os.path.join(output_dir, filename)
        
        print(f"Processing: {filename}")

        with open(input_file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # --- 處理流程管道 ---
        # 依序呼叫各個處理器
        content = process_images(content, image_output_dir)
        content = process_links(content)
        content = process_diff_blocks(content)
        content = process_php_tags(content)
        content = process_tabs(content)
        
        # --- 寫入處理後的檔案 ---
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        processed_count += 1

    print("\nConversion completed!")
    print(f"Total files processed: {processed_count}")
    print(f"Output files located at: {output_dir}")

def main() -> None:
    """主函式：解析命令列參數並啟動轉換程序"""
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <source_dir> <output_dir>")
        print("  source_dir: Input directory containing .md files")
        print("  output_dir: Output directory for processed files")
        sys.exit(1)

    source_dir = sys.argv[1]
    output_dir = sys.argv[2]

    if not os.path.isdir(source_dir):
        print(f"Error: Source directory '{source_dir}' does not exist")
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)

    # 修正 sys.path 以便 Python 能找到 `processors` 模組
    # 將 `bin` 目錄的父目錄 (專案根目錄) 加入到 path
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, project_root)

    convert_content(source_dir, output_dir)

if __name__ == "__main__":
    main()
