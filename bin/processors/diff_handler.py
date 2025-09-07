import re

def process_diff_blocks(content: str) -> str:
    """轉換 Laravel Doc 特有的 HTML diff 語法為標準 diff 語法。"""
    def replacer(match: re.Match) -> str:
        block_content = match.group(1)

        should_convert = False
        for line in block_content.splitlines():
            stripped_line = line.strip()
            if (stripped_line.startswith('+') or stripped_line.startswith('-')) and \
               ('<!-- [tl! add] -->' in stripped_line or '<!-- [tl! remove] -->' in stripped_line):
                should_convert = True
                break

        if should_convert:
            modified_content = block_content.replace('<!-- [tl! remove] -->', '')
            modified_content = modified_content.replace('<!-- [tl! add] -->', '')
            return f"```diff{modified_content}```"
        
        return match.group(0)

    return re.sub(r"```html(.*?)```", replacer, content, flags=re.DOTALL)

