"""
Admonition 處理器

此模組負責將 Markdown 文件中的 `[!NOTE]` 和 `[!WARNING]` 語法
轉換為嵌入 Base64 編碼的 SVG 圖片的 HTML `<img>` 標籤。

主要功能：
- 為 NOTE 和 WARNING 產生對應的 SVG 圖示。
- 使用 Base64 將 SVG 編碼，以便直接嵌入 HTML。
- 提供文繞圖效果，並保持與文字的適當間距。

本程式授權採用 MIT License
Copyright (c) 2025 Pigo Chu
"""

import base64

# --- SVG 圖示定義 ---

SVG_NOTE = """
<svg width="20" height="20" viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg">
  <title>Note</title>
  <circle cx="8" cy="8" r="7.5" fill="#3B82F6" stroke="white" stroke-width="1"/>
  <text x="8" y="12" font-family="sans-serif" font-size="10" font-weight="bold" fill="white" text-anchor="middle">i</text>
</svg>
""".strip()

SVG_WARNING = """
<svg width="20" height="20" viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg">
  <title>Warning</title>
  <path d="M8 1 L0.5 15 L15.5 15 Z" fill="#FBBF24" stroke="white" stroke-width="1"/>
  <text x="8" y="13" font-family="sans-serif" font-size="12" font-weight="bold" fill="black" text-anchor="middle">!</text>
</svg>
""".strip()

# --- 輔助函式 ---

def _create_image_tag(svg_content: str, alt_text: str) -> str:
    """
    將 SVG 字串轉換為 Base64 編碼的 <img> 標籤。

    Args:
        svg_content: 原始的 SVG 程式碼字串。
        alt_text: <img> 標籤的替代文字。

    Returns:
        完整的 HTML <img> 標籤字串。
    """
    encoded_svg = base64.b64encode(svg_content.encode('utf-8')).decode('utf-8')
    return (
        f'<img src="data:image/svg+xml;base64,{encoded_svg}" '
        f'alt="{alt_text}" align="left" '
        f'style="margin: 0 16px 0 0" />'
    )

# --- 主要處理函式 ---

def process_admonitions(content: str) -> str:
    """
    在給定的內容中，將 `[!NOTE]` 和 `[!WARNING]` 替換為 SVG 圖片標籤。

    Args:
        content: 原始的 Markdown 文件內容。

    Returns:
        經過替換處理後的文件內容。
    """
    # 產生一次性的 <img> 標籤
    note_img_tag = _create_image_tag(SVG_NOTE, "NOTE")
    warning_img_tag = _create_image_tag(SVG_WARNING, "WARNING")

    # 執行替換
    content = content.replace("[!NOTE]", note_img_tag)
    content = content.replace("[!WARNING]", warning_img_tag)

    return content
