# 規格說明：`link_handler.py`

## 1. 處理目標

本處理器旨在修正 Markdown 文件中指向其他文件的內部連結。Laravel 官方文件的連結格式包含 `{{version}}` 變數，且通常不包含 `.md` 副檔名，這種格式無法被 Sphinx 直接用於建立文件間的交叉引用。

本處理器的任務是將這些連結轉換為 Sphinx (`myst-parser`) 能夠識別的標準相對路徑格式。

## 2. 轉換規則

腳本會偵測兩種主要的連結格式並進行替換。

### 規則 1：一般內部連結

-   **偵測目標**: 尋找符合 `(/docs/{{version}}/path/to/document)` 格式的連結。
-   **執行轉換**: 將其轉換為 `(path/to/document.md)`。本質上是移除 `/docs/{{version}}/` 前綴，並在結尾添加 `.md` 副檔名。

### 規則 2：包含錨點的內部連結

-   **偵測目標**: 尋找符合 `(/docs/{{version}}/path/to/document#section-anchor)` 格式的連結。
-   **執行轉換**: 將其轉換為 `(path/to/document.md#section-anchor)`。處理方式與規則 1 類似，但會保留結尾的 `#` 錨點。

## 3. 範例

### 範例 1：一般連結

#### 轉換前 (Before)

```markdown
[installation guide](/docs/{{version}}/installation)
```

#### 轉換後 (After)

```markdown
[installation guide](installation.md)
```

### 範例 2：帶錨點的連結

#### 轉換前 (Before)

```markdown
[configuration options](/docs/{{version}}/configuration#application-settings)
```

#### 轉換後 (After)

```markdown
[configuration options](configuration.md#application-settings)
```
