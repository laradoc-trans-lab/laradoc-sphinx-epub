"""
建置的設定檔

前半部大多是一些簡單程式主要配置共用目錄，參考的目錄，擴充模組等等設定
後半部則可以視情況調整各變數改變 EPUB 檔案資訊
"""


import os
import sys
import datetime
from pathlib import Path


env_build_version = os.environ.get('SPHINX_BUILD_VERSION','')
parts = env_build_version.split(',')

laravel_version = parts[0]
book_style = parts[1]


# 定義路徑，讓 Sphinx 可以找到自訂的擴充模組與樣式
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / '..' / 'sphinx_extensions'))
sys.path.insert(0, str(Path(__file__).parent / '..' / 'pygments_styles'))

# 載入擴充模組
extensions = [
    'myst_parser', # Markdown 支援
    'torchlight', # 自訂程式碼高亮擴充模組，位於 ../sphinx_extensions 目錄
]

# 定義來源檔案格式，支援 reStructuredText 與 Markdown
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

# 定義樣板目錄，封面 HTML 樣板會放在這裡
templates_path = ['common/_templates']

# 靜態檔案目錄 , image , css 放於此
html_static_path = [f'preprocess/{laravel_version}/docs/_static' , 'common/_static', f'common/cover/{laravel_version}/{book_style}'] 


# 定義目錄索引的檔案
master_doc = 'index'

# 排除不需要的檔案和目錄
exclude_patterns = [
    '_build',
    'Thumbs.db', 
    '.DS_Store',
    '*.bak',
    '.gitkeep',
    '.doctrees',
    '**/.doctrees',
    '**/*.doctree'
]


# -- 修正不支援的 Highlighting --
from pygments.lexers.templates import PhpLexer,HtmlPhpLexer
from pygments.lexers.configs import IniLexer,BashLexer
from sphinx.highlighting import lexers

# -- blade 語法改為 PHP 語法 --
lexers['blade'] = HtmlPhpLexer(linenos=True)
# -- env 檔案語法改為 ini 語法 --
lexers['env'] = IniLexer(linenos=True)
# -- shell 語法改為 bash 語法 --
lexers['shell'] = BashLexer(linenos=True)
lexers['php-line'] = PhpLexer(startinline=True,linenos=True)



# -------- 後半部可以視情況調整 --------

# -- 專案資訊 : 以下都是 Sphinx 需要的變數
language='zh_TW'
copyright = "2025, Laravel Contributors"
author = 'Laravel contributors'
version = laravel_version

# 動態生成 release (格式：12.x-%Y%m%d%H%M)
release = f"{version}-{datetime.datetime.now().strftime('%Y%m%d%H%M')}"
tmp_version = laravel_version.replace('.x','') # 把版本的 .x 移除
project = f'Laravel-{tmp_version}-Documentationc-zh_TW-{book_style}' # 轉換後的檔名

# -- EPUB 書本資訊 : 以下都是 EPUB 需要的變數
epub_author = author
epub_title = f'Laravel {tmp_version} 非官方說明文件'
if book_style == 'color':
    epub_subtitle = '繁體中文彩色高亮版'
    epub_css_files = ['custom-color.css']
    # -- 封面圖檔 --
    epub_cover = (f'cover-color.png','cover.html')
    pygments_style = 'xcode'

else:
    epub_subtitle = '繁體中文黑白高亮版'
    epub_css_files = ['custom-grayscale.css']
    # -- 封面圖檔 --
    epub_cover = (f'cover-grayscale.png','cover.html')
    pygments_style = 'grayscale.GrayscaleStyle'

epub_version = 3.0
epub_language = 'zh-TW'
epub_show_urls = 'footnote' # 外部連結以註腳顯示
epub_publisher = 'laradoc-trans-lab'
epub_contributor = 'laradoc-trans-lab'
epub_contributor_url = 'https://github.com/laradoc-trans-lab'
epub_tocdepth = 2
epub_build_date = f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}" # 建置日期


# ----------------------------------------------------------------------------
# 此為封面頁所需要的樣板變數
# ----------------------------------------------------------------------------
html_context = {
    'author': author,
    'epub_author': epub_author,
    'epub_title': epub_title,
    'epub_build_date': epub_build_date,
    'epub_contributor': epub_contributor,
    'epub_contributor_url' : epub_contributor_url,
    'epub_title': epub_title,
    'epub_subtitle': epub_subtitle,
    'book_version': version,
    'book_release': release,
    'book_style': book_style,
}