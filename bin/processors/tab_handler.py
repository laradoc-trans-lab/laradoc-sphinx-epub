import re

def process_tabs(content: str) -> str:
    """處理程式碼區塊的 `tab=` 語法。"""
    new_content_lines = []
    for line in content.splitlines(keepends=True):
        match = re.match(r"^\s*```(\w+)\s+tab=(.*)", line)
        if match:
            language = match.group(1)
            title = match.group(2).strip()
            new_content_lines.append(f"**{title}**\n\n")
            new_content_lines.append(f"```{language}\n")
        else:
            new_content_lines.append(line)
    return "".join(new_content_lines)

