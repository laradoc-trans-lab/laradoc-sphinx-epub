import os
import sys
import datetime
from pathlib import Path

# Add the project root to sys.path to find sphinx_extensions
sys.path.insert(0, str(Path(__file__).parent / '..' / 'sphinx_extensions'))

# 這是基礎設定檔，conf-color.py 與 conf-bw.py 會引用此檔案並覆寫部分設定

# conf.py
# 詳細參考 https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------

copyright = "2025, Laravel Contributors"
author = 'Laravel contributors'
version = '12.x'
# 動態生成 release (格式：12.x-%Y%m%d%H%M)
release = f"{version}-{datetime.datetime.now().strftime('%Y%m%d%H%M')}"

# 為專案和作者提供預設值，主要為了讓靜態分析工具能夠識別
# 這些值會被 conf_color.py / conf_grayscale.py 中的定義所覆寫
project = 'Laravel'
epub_author = author

# -- General configuration ---------------------------------------------------
# Using myst_parser for modern Markdown support in Sphinx
extensions = [
    'myst_parser',
    'torchlight',
]


# Define source file suffixes, including Markdown
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

# 定義目錄索引的檔案
master_doc = '_index'

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




# ---- EPUB 輸出參數 ----
epub_title = "Laravel 12 文件繁體中文版"
epub_version = 3.0
epub_language = 'zh-TW'
epub_show_urls = 'footnote' # 外部連結以註腳顯示
epub_publisher = 'laradoc-trans-lab'
epub_contributor = 'laradoc-trans-lab'
epub_contributor_url = 'https://github.com/laradoc-trans-lab'
epub_tocdepth = 2
epub_build_date = f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}" # 建置日期


# -- 修正不支援的 Highlighting --
from pygments.lexers.templates import PhpLexer
from pygments.lexers.templates import HtmlPhpLexer
from pygments.lexers.configs import IniLexer
from pygments.lexers.configs import BashLexer
from sphinx.highlighting import lexers

# -- blade 語法改為 PHP 語法 --
lexers['blade'] = HtmlPhpLexer(linenos=True)
# -- env 檔案語法改為 ini 語法 --
lexers['env'] = IniLexer(linenos=True)
# -- shell 語法改為 bash 語法 --
lexers['shell'] = BashLexer(linenos=True)

lexers['php-line'] = PhpLexer(startinline=True)


# ---- 目錄設定 ----
# 樣板目錄 , 封面 html 放於此
templates_path = ['_templates']

# 靜態檔案目錄 , image , css 放於此
html_static_path = ['_source/_static']
html_codeblock_linenos_style = 'inline'






