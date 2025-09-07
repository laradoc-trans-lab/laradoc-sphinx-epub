import re

def process_php_tags(content: str) -> str:
    """處理 PHP 程式碼區塊標籤，確保 `<?php` 存在。"""
    def ensure_php_tag(match: re.Match) -> str:
        code_block_content = match.group(1)
        if '<?php' not in code_block_content:
            cleaned_content = code_block_content.lstrip()
            return f"```php-line\n{cleaned_content}```"
        return match.group(0)

    return re.sub(r"```php(.*?)```", ensure_php_tag, content, flags=re.DOTALL)

