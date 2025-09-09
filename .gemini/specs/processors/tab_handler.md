# 規格說明：`tab_handler.py`

## 1. 處理目標

本處理器用於轉換 Laravel 文件中一種用於建立分頁選項卡 (Tabs) 的非標準 Markdown 語法。在原始文件中，它使用 `tab=` 屬性來定義一個程式碼區塊屬於哪個選項卡。

這種語法不是標準 Markdown 或 `myst-parser` 的一部分，因此需要轉換成一種更通用、更易於後續處理的格式。

## 2. 轉換規則

1.  **偵測目標**：腳本會逐行讀取文件，並尋找以 ````<language> tab=<title>```` 開頭的程式碼區塊標示。
    -   `<language>` 是程式碼語言 (如 `bash`, `php`)。
    -   `<title>` 是該選項卡的標題。
2.  **執行轉換**：
    -   當偵測到符合格式的行時，腳本會將該行替換為兩部分：
        1.  一個 Markdown 的粗體標題，內容為 `**<title>**`。
        2.  一個標準的程式碼區塊起始標籤 ````<language>````。
    -   原始程式碼區塊的內容和結束標籤 ```` ` 會保持不變。

## 3. 範例

### 轉換前 (Before)

    ```bash tab=macOS
    brew install mysql
    ```

    ```bash tab=Windows
    choco install mysql
    ```

### 轉換後 (After)

    **macOS**

    ```bash
    brew install mysql
    ```

    **Windows**

    ```bash
    choco install mysql
    ```

這樣的轉換結果雖然失去了原生的 Tab UI，但保留了內容的結構和上下文，使其在轉換後的 EPUB 中依然清晰可讀。每個選項卡的內容現在都有一個明確的標題。
