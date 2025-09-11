from conf_common import *

# 此設定適合使用彩色 LCD 螢幕閱讀

# -- 專案名稱 --
project = 'Laravel-12-Documentationc-zh_TW-color'

# -- 支援的樣式可參考 https://pygments.org/styles/ --
pygments_style = 'monokai'

# -- EPUB 輸出參數，這裡指 EPUB3 + 書本是繁體中文 --
epub_title = "Laravel 12 說明文件-繁體中文彩色高亮版"

epub_author = author

epub_css_files = ['custom.css']

# -- 封面圖檔 --
epub_cover = ('_static/cover-color.png','cover.html')

# EPUB 專用排除設定
epub_exclude_files = [
    'search.html',
    '*.bak',
    '.gitkeep',
    '.doctrees/*',
    '**/.doctrees'
    'cover-grayscale.png',
    '**/cover-grayscale.png'
]

# 排除不需要的檔案和目錄
exclude_patterns = [
    '_build',
    'Thumbs.db', 
    '.DS_Store',
    '*.bak',
    '.gitkeep',
    '.doctrees',
    '**/.doctrees',
    '**/*.doctree',
    'cover-grayscale.png',
    '**/cover-grayscale.png'
]