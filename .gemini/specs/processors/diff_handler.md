# 規格說明：`diff_handler.py`

## 1. 處理目標

本處理器旨在解決 Laravel 原始文件中一種特殊的程式碼差異 (diff) 標示法。在 Laravel 文件中，程式碼的新增與刪除是透過 HTML 註解 `<!-- [tl! add] -->` 和 `<!-- [tl! remove] -->` 來標示的，且整個區塊被包在 ````html ... ````` 程式碼區塊中。

這種格式無法被 Sphinx 的 `myst-parser` 正確解析為 `diff` 語法。本處理器的工作就是將其轉換為標準的 `diff` 程式碼區塊。

## 2. 轉換規則

1.  **偵測目標**：腳本會搜尋所有標記為 `html` 的程式碼區塊 (````html ... ````)。
2.  **判斷條件**：只有當 `html` 程式碼區塊內部同時包含 `+` 或 `-` 開頭的行，**並且**該行包含 `<!-- [tl! add] -->` 或 `<!-- [tl! remove] -->` 註解時，才會觸發轉換。
3.  **執行轉換**：
    -   將程式碼區塊的語言標示從 `html` 改為 `diff`。
    -   移除所有 `<!-- [tl! add] -->` 和 `<!-- [tl! remove] -->` 的 HTML 註解標籤。
    -   保留原始的 `+` 和 `-` 符號。

## 3. 範例

### 轉換前 (Before)

    ```html
    - use App\Http\Controllers\PostController;
    + use App\Http\Controllers\ArticleController; <!-- [tl! add] -->
    ```

### 轉換後 (After)

    ```diff
    - use App\Http\Controllers\PostController;
    + use App\Http\Controllers\ArticleController;
    ```

如果一個 `html` 區塊內沒有 `[tl! ...]` 標籤，即使有 `+` 或 `-`，它也**不會**被轉換，以避免錯誤地修改了非 `diff` 用途的程式碼。
