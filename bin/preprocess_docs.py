#!/usr/bin/env python3
"""
程式用途
1. 下載文件中含有 `<img src=\"\">` 標籤所包含的圖片並儲存於 `book/_source/_static/laravel` 資料夾，
   並將連結改為本地路徑。
2. 將文件中出現 `/docs/{{version}}/{{chapter}}` 的連結轉換為 `{{chapter}}.md`。
3. 將文件中出現 "```php" 區塊中內的程式碼檢查整段是否有出現 `<?php` , 如果沒有出現，則插入一行 `<?php` 於區塊的第一行。
4. 將文件中出現 "```shell tab=Linux" 的語法修正，會將 tab 後面提取出來增加一行粗體敘述於程式碼前。
5. 最後將 Markdown 文件儲存到指定的輸出目錄 `book/_source`。

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
        # 1. 使用正規表示式尋找所有 <img> 標籤中的 src 網址
        img_urls = re.findall(r'<img[^>]+src=\"([^\"]+)\"', content)

        # 2. 如果有找到圖片，才修正未閉合的 img 標籤
        if img_urls:
            content = re.sub(r'(<img[^>]*)(?<!/)>', r'\1 />', content)
        
        # 3. 遍歷所有找到的圖片網址 (使用 set 避免在同一個檔案中重複下載相同的圖片)
        for url in set(img_urls):
            # 只處理 https 開頭的外部圖片
            if not url.startswith(('https://')):
                continue

            try:
                # 3. 從網址中解析出原始檔名
                image_filename = os.path.basename(urlparse(url).path)
                if not image_filename:
                    # 如果網址中沒有檔名 (例如 /images/show/123)，則用 hash 值建立一個
                    image_filename = "img_" + hashlib.md5(url.encode()).hexdigest()[:10]

                local_image_path = os.path.join(image_output_dir, image_filename)
                new_image_src = f"_static/laravel/{image_filename}"
                
                print(f"  - Found image: {url}")
                print(f"    - Downloading to: {new_image_src}")
                
                # 4. 重新下載圖片以確保獲取最新版本
                if download_image(url, local_image_path):
                    # 5. 如果下載成功，則替換內容中的網址為本地路徑
                    content = content.replace(url, new_image_src)

            except Exception as e:
                print(f"    - Failed to process image URL {url}: {e}")

        # --- 階段二：處理內部文件連結 ---
        # 6. 轉換包含 #錨點 的連結 (例如 /docs/{{version}}/chapter#header -> chapter.md#header)
        content = re.sub(
            r'\(/docs/\{\{version\}\}/([^)#]+)#([^)]+)\)',
            r'(\1.md#\2)',
            content
        )
        # 7. 轉換一般的連結 (例如 /docs/{{version}}/chapter -> chapter.md)
        content = re.sub(
            r'\(/docs/\{\{version\}\}/([^)]+)\)',
            r'(\1.md)',
            content
        )


        # --- 新增階段：修正 PHP 程式碼區塊標籤 ---
        # 3. 將文件中出現 "```php" 區塊中內的程式碼檢查整段是否有出現 `<?php` , 如果沒有出現，則插入一行 `<?php` 於區塊的第一行。
        def ensure_php_tag(match):
            # group(1) is the content between ```php and ```
            code_block_content = match.group(1)

            if '<?php' not in code_block_content:
                # Strip leading whitespace/newlines from the original content
                # to avoid extra blank lines.
                cleaned_content = code_block_content.lstrip()
                # Reconstruct the block with the tag on its own line.
                return f"```php\n<?php\n{cleaned_content}```"
            
            # If the tag exists, return the original block to avoid any changes.
            return match.group(0)

        content = re.sub(r"```php(.*?)```", ensure_php_tag, content, flags=re.DOTALL)
        
        # --- 階段三：處理程式碼區塊 tab ---
        new_content_lines = []
        for line in content.splitlines(keepends=True):
            match = re.match(r"^\s*```(\w+)\s+tab=(.*)", line)
            if match:
                language = match.group(1)
                title = match.group(2).strip()
                # 修正：移除星號與文字間的空格，並在標題後新增一個空行
                new_content_lines.append(f"**{title}**\n\n")
                new_content_lines.append(f"```{language}\n")
            else:
                new_content_lines.append(line)
        content = "".join(new_content_lines)
        
        # --- 階段四：寫入處理後的檔案 ---
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        processed_count += 1

    print("\nConversion completed!")
    print(f"Total files processed: {processed_count}")
    print(f"Output files located at: {output_dir}")

def main():
    """主函式：解析命令列參數並啟動轉換程序"""
    # 檢查命令列參數數量是否正確
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <source_dir> <output_dir>")
        print("  source_dir: Input directory containing .md files")
        print("  output_dir: Output directory for processed files")
        sys.exit(1)

    source_dir = sys.argv[1]
    output_dir = sys.argv[2]

    # 檢查來源目錄是否存在
    if not os.path.isdir(source_dir):
        print(f"Error: Source directory '{source_dir}' does not exist")
        sys.exit(1)

    # 建立輸出目錄 (如果不存在的話)
    os.makedirs(output_dir, exist_ok=True)

    # 呼叫核心處理函式
    convert_content(source_dir, output_dir)

if __name__ == "__main__":
    main()
