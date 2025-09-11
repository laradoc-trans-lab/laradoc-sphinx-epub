import os
import sys
from pathlib import Path

# 確保 conf_common.py 等模組可以被找到
sys.path.insert(0, str(Path(__file__).parent))

# ----------------------------------------------------------------------------
# 為了讓 VSCode 等靜態分析器能預先識別變數，先從基礎設定檔匯入
# 執行時，這些變數會被下方 `from ... import *` 的值覆寫
# ----------------------------------------------------------------------------
try:
    from conf_common import *
except ImportError as e:
    print(f"警告: 無法從 conf_common 預先載入變數. {e}")
    # 定義一個最小集合以防萬一
    project, author, epub_author,epub_title, version, release,epub_build_date,epub_contributor,epub_contributor_url = [''] * 9


# ----------------------------------------------------------------------------
# 根據環境變數，從對應的版本設定檔中匯入所有設定 (*)
# 這會覆寫上面從 conf_common 匯入的預設值
# ----------------------------------------------------------------------------
config_type = os.environ.get('SPHINX_CUSTOM_CONFIG', 'color')
print(f"正在為 '{config_type}' 版本載入設定...")

if config_type == 'grayscale':
    try:
        from conf_grayscale import *
    except ImportError as e:
        print(f"錯誤: 無法從 conf_grayscale.py 匯入設定. {e}")
else:
    try:
        from conf_color import *
    except ImportError as e:
        print(f"錯誤: 無法從 conf_color.py 匯入設定. {e}")


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
    'book_title': project,
    'book_version': version,
    'book_release': release,
}