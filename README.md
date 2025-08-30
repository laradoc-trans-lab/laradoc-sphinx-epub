# 使用 Sphinx 將 Laravel 文件轉成 epub

Laravel 官方文件的寫法若直接用 Sphinx 轉換成 EPUB 會遇到很多問題，如

1. "```shell tab=Linux " 這種標籤效果，好像各轉換工具沒辦法直接處理好。
2. 文件中 Markdown 使用 `<img>` 引用外部圖片，需下載回來包在 epub。
3. 文件中 Markdown 使用 `<img>` 沒有正確的結束語法，因此無法通過 XHTML 驗證。
3. 程式碼區塊使用的語言不被認得，例如 `blade` , 這都要額外設定修正。

為了解決上述問題，這邊提供了修正程式來解決這問題，且將轉換過程需要的設定都撰寫成樣板，方便日後使用。

## 專案目錄結構介紹

* `bin/preprocess_docs.py` : 可用來修復 Markdown 內的各種問題，包含自動下載圖片存放於本地端。
* `bin/build.sh` : 簡單的 bash 以執行 `preprocess_docs.py` 與 `sphinx-build` 建立 epub 檔案。
* `template` : 現成的樣板，目前只提供 `template/12.x` 可直接用於轉換 `Laravel 12.x` 說明文件，以後會陸續增加其他版本，目前的樣板有設定好可以轉換為兩種 epub 版本，分別為彩色高亮版與灰階高亮版。
* `source` : 空目錄，轉換前需要準備好所有 Markdown 未修復的原始檔案。
* `book` : 用於準備好要轉換的檔案所需檔案，包含修正好的 Markdown file , 本地端圖片，Sphinx 相關設定檔。
* `build` : 輸出為 epub 時，會將所有檔案儲存於此。

## 環境需求

如果系統能跑 `docker`，可以跳過本段說明，使用 `docker` 跑比較簡單，若沒辦法跑 `docker` , 需要準備好以下必備軟體

- Linux : 目前提供的 shell , py 都只有在 Linux 測過，也許 Mac 也行吧。
- Python3
- Sphinx
- `requirements.txt` 內有 PIP 所需套件都要安裝。

以下簡單介紹 Sphinx 的安裝方式 , 假設你已經 clone 本專案了，就直接於本專案的根目錄下操作即可

```bash
python3 -m venv .venv
chmod +x .venv/bin/activate
.venv/bin/activate
source .venv/bin/activate
pip install sphinx sphinx-rtd-theme recommonmark
```
這樣就會於本專案建立 venv 的虛擬環境，所安裝的軟體只能在專案內使用。不會影響到全域 Python。

## 使用現成的樣板以 Sphinx 轉換為 EPUB

一開始要先準備 Laravel 原始的 Markdown , [這裡有提供](https://github.com/laradoc-trans-lab/laravel_docs-zh_TW)，其實本專案其實也可以用來轉換 Laravel 官方的英文版本啦，接下來就依照步驟將轉換的環境建置好:

1. 將文件的所有 Markdown 檔案 \(*.md\) 複製到 `source` 目錄下。
2. 將 `template/12.x` 內的檔案複製到 `book` 目錄下。
3. 如有需要可以修改 `book` 下的 `conf.py` ,`conf_color.py` , `conf_graysacle.py`，設定檔都有中文註解了。

接下來就可以進行轉換了

若環境有 `docker` 執行以下命令:

```bash
docker compose run -u $UID:$GID --rm builder
```

環境沒有 `docker` 執行以下命令:

```bash
bin/build.sh
```

就這麼簡單，所有 Markdwon 修正與轉換為 epub 都會依照現有的目錄結構自動完成，轉換過程會有一些紅字 WARNING 不用館，如果轉換成功結束，應該可以看到幾個變化

* `book/_source` 目錄會有所有修正好的 Markdown 檔案。
* `build` 目錄會有 `color` 與 `grayscale` 分別是轉成兩種類型的 epub ，你要的 epub 檔案就在裡面。

## Author

Pigo Chu <pigochu@gmail.com>

## Lincense

本專案提供的工具與教學步驟使用 MIT 授權。