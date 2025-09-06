#!/usr/bin/env python3
"""
程式用途
1. 下載文件中含有 `<img src="">` 標籤所包含的圖片並儲存於 `book/_source/_static/laravel` 資料夾，
   並將連結改為本地路徑。
2. 將文件中出現 `/docs/{{version}}/{{chapter}}` 的連結轉換為 `{{chapter}}.md`。
3. 將 Laravel Doc 特有的 diff 語法轉換為 Sphinx 的 diff 語法。
4. 將文件中出現 "```php" 區塊中內的程式碼檢查整段是否有出現 `<?php` , 如果沒有出現，則改為 `<?php-inline`。
5. 將文件中出現 "```shell tab=Linux" 的語法修正，會將 tab 後面提取出來增加一行粗體敘述於程式碼前。
6. 最後將 Markdown 文件儲存到指定的輸出目錄 `book/_source`。

本程式授權採用 MIT License
Copyright (c) 2025 Pigo Chu
"""

import sys
import os
import re
import requests
import hashlib
from urllib.parse import urlparse

def download_image(url, save_path):
    # -- 下載指定 URL 的圖片並儲存到指定路徑 --
    try:
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()  # 如果請求失敗 (例如 404)，則會拋出例外
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    except requests.exceptions.RequestException as e:
        print(f"    - Error downloading {url}: {e}")
        return False

def process_laravel_diff_blocks(content):
    """轉換 Laravel Doc 特有的 HTML diff 語法為標準 diff 語法。"""
    def replacer(match):
        # group(1) 是 ```html 與 ``` 之間的內容
        block_content = match.group(1)
        # 檢查區塊內是否含有目標註解
        if '<!-- [tl! remove] -->' in block_content or '<!-- [tl! add] -->' in block_content:
            # 移除註解
            modified_content = block_content.replace('<!-- [tl! remove] -->', '')
            modified_content = modified_content.replace('<!-- [tl! add] -->', '')
            # 將 ```html 改為 ```diff
            return f"```diff{modified_content}```"
        # 如果沒有找到標記，回傳原來的區塊
        return match.group(0)

    # 使用 re.DOTALL 讓 `.` 可以匹配換行符
    return re.sub(r"```html(.*?)```", replacer, content, flags=re.DOTALL)

def convert_content(source_dir, output_dir):
    """
    主要處理函式：轉換文件連結、下載圖片，並儲存到輸出目錄
    """
    print("Starting Laravel documentation content conversion...")
    print(f"Source directory: {source_dir}")
    print(f"Output directory: {output_dir}\n")

    # 在輸出目錄中建立一個名為 _statics/laravel 的資料夾來存放圖片
    image_output_dir = os.path.join(output_dir, '_static' , 'laravel')
    os.makedirs(image_output_dir, exist_ok=True)

    processed_count = 0
    # 遍歷來源目錄中的所有檔案
    for filename in os.listdir(source_dir):
        # 只處理 .md 結尾的檔案
        if not filename.endswith(".md") or not os.path.isfile(os.path.join(source_dir, filename)):
            continue

        input_file_path = os.path.join(source_dir, filename)
        output_file_path = os.path.join(output_dir, filename)
        
        print(f"Processing: {filename}")

        with open(input_file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # --- 階段一：處理圖片 ---
        img_urls = re.findall(r'<img[^>]+src="([^"]+)"', content)
        if img_urls:
            content = re.sub(r'(<img[^>]*)(?<!/)>', r'\1 />', content)
        
        for url in set(img_urls):
            if not url.startswith(('https://')):
                continue
            try:
                image_filename = os.path.basename(urlparse(url).path)
                if not image_filename:
                    image_filename = "img_" + hashlib.md5(url.encode()).hexdigest()[:10]
                local_image_path = os.path.join(image_output_dir, image_filename)
                new_image_src = f"_static/laravel/{image_filename}"
                print(f"  - Found image: {url}")
                print(f"    - Downloading to: {new_image_src}")
                if download_image(url, local_image_path):
                    content = content.replace(url, new_image_src)
            except Exception as e:
                print(f"    - Failed to process image URL {url}: {e}")

        # --- 階段二：處理內部文件連結 ---
        content = re.sub(r'\(/docs/\{\{version\}\}/([^)#]+)#([^)]+)\)', r'(\1.md#\2)', content)
        content = re.sub(r'\(/docs/\{\{version\}\}/([^)]+)\)', r'(\1.md)', content)

        # --- 階段三：處理 Laravel Doc 特有的 diff 語法 ---
        content = process_laravel_diff_blocks(content)

        # --- 階段四：修正 PHP 程式碼區塊標籤 ---
        def ensure_php_tag(match):
            code_block_content = match.group(1)
            if '<?php' not in code_block_content:
                cleaned_content = code_block_content.lstrip()
                return f"```php-line\n{cleaned_content}```"
            return match.group(0)

        content = re.sub(r"```php(.*?)```", ensure_php_tag, content, flags=re.DOTALL)
        
        # --- 階段五：處理程式碼區塊 tab ---
        new_content_lines = []
        for line in content.splitlines(keepends=True):
            match = re.match(r"^\s*```(\w+)\s+tab=(.*)", line)
            if match:
                language = match.group(1)
                title = match.group(2).strip()
                new_content_lines.append(f"**{title}**\n\n")
                new_content_lines.append(f"```{language}\n")
            else:
                new_content_lines.append(line)
        content = "".join(new_content_lines)
        
        # --- 階段六：寫入處理後的檔案 ---
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(content)

    print("\nConversion completed!")
    print(f"Total files processed: {processed_count}")
    print(f"Output files located at: {output_dir}")

def main():
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
    convert_content(source_dir, output_dir)

if __name__ == "__main__":
    main()