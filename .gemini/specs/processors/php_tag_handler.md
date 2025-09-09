# 規格說明：`php_tag_handler.py`

## 1. 處理目標

本處理器用於規範 `php` 程式碼區塊的內容。在某些情況下，從 Laravel 文件複製的 PHP 程式碼片段可能不包含開頭的 `<?php` 標籤。這會導致 Sphinx 的語法高亮器 (`pygments`) 無法正確識別程式碼，或在某些情況下導致解析錯誤。

此處理器的任務是確保所有標記為 `php` 的程式碼區塊都包含 `<?php` 標籤。

## 2. 轉換規則

1.  **偵測目標**：腳本會搜尋所有標記為 `php` 的程式碼區塊 (````php ... ````)。
2.  **判斷條件**：檢查區塊內的程式碼是否包含 `<?php` 字串。
3.  **執行轉換**：
    -   如果程式碼**不包含** `<?php`，腳本會將程式碼區塊的語言標示從 `php` 改為 `php-line`。
    -   `php-line` 是一個自訂的標示，暗示這段程式碼在邏輯上是 PHP，但可能不是一個完整的檔案。在 Sphinx 的設定中，它可以被對應回 `php` 語法高亮，但這樣的修改提供了一個明確的標記，指出內容經過了自動處理。
    -   如果程式碼**已包含** `<?php`，則不做任何變更。

## 3. 範例

### 轉換前 (Before)

    ```php
    use Illuminate\Support\Facades\Route;

    Route::get('/', function () {
        return view('welcome');
    });
    ```

### 轉換後 (After)

    ```php-line
    use Illuminate\Support\Facades\Route;

    Route::get('/', function () {
        return view('welcome');
    });
    ```
