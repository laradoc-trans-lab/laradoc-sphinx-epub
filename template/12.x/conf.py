# 這是基礎設定檔，conf-color.py 與 conf-bw.py 會引用此檔案並覆寫部分設定

# conf.py
# 詳細參考 https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------

copyright = "2025, Laravel Contributors; translated by laradoc-trans-lab"
author = '2025, Laravel contributors; translated by laradoc-trans-lab'
version = '12.x'
release = '12.x-20250829'

# -- General configuration ---------------------------------------------------
# Using myst_parser for modern Markdown support in Sphinx
extensions = [
    'myst_parser',
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




# -- EPUB 輸出參數，這裡指 EPUB3 + 書本是繁體中文 --
epub_title = "Laravel 12 文件繁體中文版"
epub_version = 3.0
epub_language = 'zh-TW'
# 將內文中有外部 URL 以註腳方式顯示
epub_show_urls = 'footnote'

# -- 修正不支援的 Highlighting --
from pygments.lexers.web import PhpLexer
from pygments.lexers.configs import IniLexer
from sphinx.highlighting import lexers

# -- blade 語法改為 PHP 語法 --
lexers['blade'] = PhpLexer(startinline=True)

# -- env 檔案語法改為 ini 語法 --
lexers['env'] = IniLexer()

# -- Path setup --------------------------------------------------------------
# Path to custom static files (CSS, images, etc.)
html_static_path = ['_source/_static']

epub_tocdepth = 2



# 根據環境變數決定載入哪個設定檔以覆蓋基本設定
import sys
import os


config_type = os.environ.get('SPHINX_CUSTOM_CONFIG', 'default')

if config_type in ['grayscale', 'color']:
    config_file = f'conf_{config_type}.py'
    config_path = os.path.join(os.path.dirname(__file__), config_file)
    
    print(f"嘗試載入配置: {config_path}")
    
    if os.path.exists(config_path):
        print(f"載入配置檔案: {config_file}")
        with open(config_path, 'r', encoding='utf-8') as f:
            exec(f.read())
    else:
        print(f"警告: 找不到配置檔案 {config_file}")
        print(f"當前目錄檔案: {os.listdir(os.path.dirname(__file__))}")
