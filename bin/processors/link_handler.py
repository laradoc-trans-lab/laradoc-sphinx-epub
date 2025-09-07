import re

def process_links(content: str) -> str:
    """處理內部文件連結轉換。"""
    # 轉換包含 #錨點 的連結
    content = re.sub(
        r'\(/docs/\{\{version\}\}/([^)#]+)#([^)]+)\)',
        r'(\1.md#\2)',
        content
    )
    # 轉換一般的連結
    content = re.sub(
        r'\(/docs/\{\{version\}\}/([^)]+)\)',
        r'(\1.md)',
        content
    )
    return content
