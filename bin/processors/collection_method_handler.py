import re

def process_collection_methods(content: str) -> str:
    """
    移除 Markdown 內容中的 {.collection-method} 和 {.collection-method .first-collection-method} 標記。
    """
    # 移除 {.collection-method .first-collection-method}
    content = re.sub(r' \{\.collection-method \.first-collection-method\}', '', content)
    # 移除 {.collection-method}
    content = re.sub(r' \{\.collection-method\}', '', content)
    return content
