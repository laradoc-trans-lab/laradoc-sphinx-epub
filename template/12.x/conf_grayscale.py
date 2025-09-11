from conf_common import *

# 此設定適合使用彩色 LCD 螢幕閱讀

# -- 專案名稱 --
project = 'Laravel-12-Documentationc-zh_TW-grayscale'

# -- 支援的樣式可參考 https://pygments.org/styles/ --
pygments_style = 'friendly_grayscale'


# -- EPUB 輸出參數，這裡指 EPUB3 + 書本是繁體中文 --
epub_title = "Laravel 12 說明文件-繁體中文黑白高亮版"

epub_author = author

# 原本的 grayscale 並非真正灰階，修正為符合 eink 螢幕特性使字形能以 300PPI 呈現
epub_css_files = ['custom.css' , 'grayscale-eink.css']

# -- 封面圖檔 --
epub_cover = ('_static/cover-grayscale.png','cover.html')

# EPUB 專用排除設定
epub_exclude_files = [
    'search.html',
    '*.bak',
    '.gitkeep',
    '.doctrees/*',
    '**/.doctrees/*'
    'cover-color.png',
    '**/cover-color.png'
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
    'cover-color.png',
    '**/cover-color.png'
]