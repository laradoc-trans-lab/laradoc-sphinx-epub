# 規格說明：`preprocess_docs.py`

## 1. 總體目標

本腳本的主要目標是作為一個預處理工具，將從 Laravel 官方文件庫 (`laravel/docs`) 直接複製過來的 Markdown 檔案，轉換成與 Sphinx (搭配 `myst-parser`) 相容的格式。最終目的是為了順利將 Laravel 文件編譯成 EPUB 電子書。

它扮演一個協調者的角色，依序調用一系列的「處理器」(processors)，形成一個處理管道 (pipeline)。

## 2. 執行方式

透過終端機執行，需要提供兩個參數：

```bash
./bin/preprocess_docs.py <source_dir> <output_dir>
```

-   `source_dir`: 包含原始 Laravel Markdown 文件的目錄。
-   `output_dir`: 用於存放處理後文件的目錄。

腳本會遍歷 `source_dir` 中的所有 `.md` 檔案，執行處理後，將同名檔案儲存於 `output_dir`。

## 3. 處理管道 (Processing Pipeline)

對於每一個 Markdown 檔案，腳本會讀取其內容，並依序通過以下處理器進行轉換。每個處理器的輸出，都會成為下一個處理器的輸入。

處理順序如下：

1.  **[`process_images`](processors/image_handler.md)**:
    -   **目的**: 處理文件中的圖片。
    -   **執行內容**: 尋找 `<img>` 標籤，下載外部圖片並存放到本地 `_static/laravel/` 目錄下，然後將圖片路徑替換為本地相對路徑。

2.  **[`process_links`](processors/link_handler.md)**:
    -   **目的**: 修正內部文件連結。
    -   **執行內容**: 將 Laravel 文件特有的 `{{version}}` 變數和 `.md` 結尾的連結，轉換成 Sphinx 能識別的相對路徑格式。

3.  **[`process_diff_blocks`](processors/diff_handler.md)**:
    -   **目的**: 轉換程式碼差異區塊。
    -   **執行內容**: 將 Laravel 文件中用 `<!-- [tl! add] -->` 和 `<!-- [tl! remove] -->` 標注的 HTML 程式碼區塊，轉換成標準的 `diff` 程式碼區塊語法。

4.  **[`process_php_tags`](processors/php_tag_handler.md)**:
    -   **目的**: 確保 PHP 程式碼區塊的格式正確。
    -   **執行內容**: 檢查 `php` 程式碼區塊，如果內容中缺少 `<?php` 開頭標籤，會自動補上，以確保語法高亮和程式碼的完整性。

5.  **[`process_tabs`](processors/tab_handler.md)**:
    -   **目的**: 轉換分頁標籤語法。
    -   **執行內容**: 將 Laravel 文件中特有的 `tab=` 語法，轉換成易於閱讀的標題和標準程式碼區塊，以便後續處理或直接閱讀。

詳細的轉換邏輯，請點擊上方各處理器連結，參考其獨立規格文件。
