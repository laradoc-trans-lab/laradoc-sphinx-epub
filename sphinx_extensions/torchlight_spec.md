# `torchlight.py` Sphinx 擴充套件規格書

## 1. 總覽

本文件旨在闡明 `torchlight.py` 這支 Sphinx 擴充套件的功能。其主要目的是解析程式碼區塊中自訂的語法高亮標籤，並將它們轉換為特定的 HTML `<span>` class，以便在最終輸出（例如 EPUB 檔案）中應用對應的樣式。

此擴充套件透過在 Sphinx 初始化設定階段，將預設的 `PygmentsBridge.html_formatter` 替換為自訂的 `TorchlightHtmlFormatter` 類別來達成目的。

## 2. 核心機制

核心邏輯實作於 `TorchlightHtmlFormatter.wrap()` 方法中，該方法會逐行處理由 Pygments 產生的程式碼區塊。

### 2.1. 狀態管理

格式化工具（Formatter）會維護兩個布林（boolean）狀態旗標，用以追蹤目前的程式碼行是否處於一個多行高亮區塊之內：

- `self.in_add_block`: 當格式化工具進入 `[tl! add:start]` ... `[tl! add:end]` 區塊時，此旗標為 `True`。
- `self.in_remove_block`: 當格式化工具進入 `[tl! remove:start]` ... `[tl! remove:end]` 區塊時，此旗標為 `True`。

這兩個旗標在初始化時都被設定為 `False`。

### 2.2. 標籤偵測

程式使用單一的正規表示式（Regular Expression）來偵測每一行中的高亮標籤：

```python
r'(?P<prefix>//\s*)?\[tl!\s*(?P<type>add|remove)(?::(?P<subtype>start|end))?\]'
```

這個模式（pattern）會捕捉三個關鍵資訊：

- `prefix`: 一個可選的 `// ` 註解前綴。
- `type`: 標籤的類型，必須是 `add` 或 `remove`。
- `subtype`: 標籤的子類型，可以是 `start`、`end`，或者 `None`（當它是一個單行標籤時）。

## 3. 標籤處理邏輯

當在某一行偵測到標籤時，腳本會執行相應的操作。在所有情況下，標籤本身（例如 `// [tl! add]`）都會從最終輸出的 HTML 中被移除。

### 3.1. `add` 標籤

- **關聯 CSS Class:** `hll`
- **處理邏輯:**
    - **`// [tl! add]` (單行標籤):**
        - 目前的程式碼行會被 `<span class="hll">` 包裹。
    - **`// [tl! add:start]`:**
        - `in_add_block` 旗標被設為 `True`。
        - 目前的程式碼行會被 `<span class="hll">` 包裹。
    - **`// [tl! add:end]`:**
        - 如果 `in_add_block` 當前為 `True`，則目前的程式碼行會被 `<span class="hll">` 包裹。
        - `in_add_block` 旗標被設為 `False`。

### 3.2. `remove` 標籤

- **關聯 CSS Class:** `dll`
- **處理邏輯:**
    - **`// [tl! remove]` (單行標籤):**
        - 目前的程式碼行會被 `<span class="dll">` 包裹。
    - **`// [tl! remove:start]`:**
        - `in_remove_block` 旗標被設為 `True`。
        - 目前的程式碼行會被 `<span class="dll">` 包裹。
    - **`// [tl! remove:end]`:**
        - 如果 `in_remove_block` 當前為 `True`，則目前的程式碼行會被 `<span class="dll">` 包裹。
        - `in_remove_block` 旗標被設為 `False`。

## 4. 無標籤時的程式碼行處理

如果一行程式碼不包含任何標籤，腳本會檢查狀態旗標：

- 如果 `in_add_block` 為 `True`，該行會被 `<span class="hll">` 包裹。
- 如果 `in_remove_block` 為 `True`，該行會被 `<span class="dll">` 包裹。
- 如果兩個旗標都為 `False`，則該行會被直接輸出，不做任何修改。

## 5. 後期處理

在標籤被處理並從程式碼行中移除後，腳本會執行一個額外的清理步驟，用以移除 Pygments 可能留下的空註解 `<span>`。這個清理是透過正規表示式 `r'<span class="c[0-9]">\s*</span>'` 來完成的。

## 6. 範例

以下範例展示了原始碼在經過 `TorchlightHtmlFormatter` 處理後的預期 HTML 輸出。為求簡潔，HTML 中的語法高亮 `<span>` 已被簡化。

### 範例 1：單行 `add` 與 `remove`

**原始內容 (`.md`):**

````markdown
```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel([
            'resources/css/app.css', // [tl! remove]
            'resources/js/app.js',
        ]),
    ],
});
```

```js
import './bootstrap';
import '../css/app.css'; // [tl! add]
```
````

**預期輸出 (`.xhtml`):**

```html
<!-- 範例 1A -->
<pre>
<span>...</span>
<span>...</span>
<span>...</span>
<span class="dll"><span>            'resources/css/app.css', </span></span>
<span>            'resources/js/app.js',</span>
<span>...</span>
</pre>

<!-- 範例 1B -->
<pre>
<span>import './bootstrap';</span>
<span class="hll"><span>import '../css/app.css'; </span></span>
</pre>
```

### 範例 2：`add` 區塊

**原始內容 (`.md`):**

````markdown
```php
abstract class TestCase extends BaseTestCase
{
    protected function setUp(): void// [tl! add:start]
    {
        parent::setUp();

        $this->withoutVite();
    }// [tl! add:end]
}
```
````

**預期輸出 (`.xhtml`):**

```html
<pre>
<span>abstract class TestCase extends BaseTestCase</span>
<span>{</span>
<span class="hll"><span>    protected function setUp(): void</span></span>
<span class="hll"><span>    {</span></span>
<span class="hll"><span>        parent::setUp();</span></span>
<span class="hll"><span></span></span>
<span class="hll"><span>        $this->withoutVite();</span></span>
<span class="hll"><span>    }</span></span>
<span>}</span>
</pre>
```

### 範例 3：相鄰的 `remove` 與 `add`

**原始內容 (`.md`):**

````markdown
```json
"scripts": {
     "dev": "vite",
     "build": "vite build" // [tl! remove]
     "build": "vite build && vite build --ssr" // [tl! add]
}
```
````

**預期輸出 (`.xhtml`):**

```html
<pre>
<span>"scripts": {</span>
<span>     "dev": "vite",</span>
<span class="dll"><span>     "build": "vite build" </span></span>
<span class="hll"><span>     "build": "vite build && vite build --ssr" </span></span>
<span>}</span>
</pre>
```
