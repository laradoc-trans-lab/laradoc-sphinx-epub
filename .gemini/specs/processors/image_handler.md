# 規格說明：`image_handler.py`

## 1. 處理目標

本處理器專門處理 Markdown 文件中嵌入的圖片。Laravel 的原始文件可能包含指向外部伺服器的圖片 URL。為了將文件製作成離線的 EPUB，需要將這些圖片下載到本地，並更新文件中的圖片路徑。

同時，它也處理 `<img>` HTML 標籤，確保其語法封閉，以符合 XML/XHTML 的嚴格標準。

## 2. 轉換規則

### 規則 1：圖片下載與路徑替換

1.  **偵測目標**：腳本會使用正則表達式 `r'<img[^>]+src="([^"]+)"'` 尋找所有 `<img>` 標籤中的 `src` 屬性。
2.  **篩選條件**：只處理 `src` 中以 `https://` 開頭的 URL。本地相對路徑的圖片會被忽略。
3.  **執行下載**：
    -   為每個唯一的圖片 URL 執行下載。
    -   圖片會被儲存到 `output/_static/laravel/` 目錄下（`output` 是主腳本指定的輸出目錄）。
    -   檔名會沿用 URL 的最後一部分。如果 URL 沒有檔名，則會使用 URL 的 MD5 雜湊值生成一個唯一的檔名。
4.  **路徑替換**：
    -   在成功下載圖片後，原始文件內容中的 `https://...` 長 URL 會被替換成指向本地的新相對路徑，例如 `_static/laravel/image.png`。

### 規則 2：`<img>` 標籤閉合

1.  **偵測目標**：尋找所有未自行閉合的 `<img>` 標籤 (例如 `<img src="...">` 而不是 `<img src="..." />`)。
2.  **執行轉換**：在標籤的結尾 `>` 前加上 ` /`，使其變為自閉合標籤 `<img src="..." />`。

## 3. 範例

### 轉換前 (Before)

```markdown
<img src="https://laravel.com/img/some-diagram.png">
```

### 轉換後 (After)

假設圖片已成功下載到 `output/_static/laravel/some-diagram.png`。

```markdown
<img src="_static/laravel/some-diagram.png" />
```
