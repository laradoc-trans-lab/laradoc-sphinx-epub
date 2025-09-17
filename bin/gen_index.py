#!/usr/bin/env python3

import sys
import os
import re
from markdown_it import MarkdownIt

def parse_documentation_md(md_content):
    """
    解析 documentation.md 內容，提取 H2 標題及其下的連結。
    返回一個列表，每個元素是一個字典，包含 'caption' 和 'entries'。
    """
    md = MarkdownIt()
    tokens = md.parse(md_content)

    sections = []
    current_section = None

    for i, token in enumerate(tokens):
        if token.type == 'heading_open' and token.tag == 'h2':
            if current_section:
                sections.append(current_section)
            
            caption = "Untitled Section"
            if i + 1 < len(tokens) and tokens[i+1].type == 'inline':
                caption = tokens[i+1].content.strip()
            
            current_section = {'caption': caption, 'entries': []}
            continue
        
        if token.type == 'inline' and token.children and current_section:
            for child_token in token.children:
                if child_token.type == 'link_open':
                    href = child_token.attrs.get('href')
                    if href:
                        link_match = re.match(r'^/docs/(?:%7B%7Bversion%7D%7D|{{version}})/(.*?)$', str(href))
                        if link_match:
                            filename = os.path.basename(link_match.group(1))
                            current_section['entries'].append(filename)
    
    if current_section:
        sections.append(current_section)
    
    return sections

def generate_sub_index_md_file(output_file_path, section_data):
    """
    生成一個 index-N.md 文件，包含 Markdown 標題和 MyST toctree 指令。
    """
    md_content = []

    # 添加 Markdown 標題
    md_content.append(f"# {section_data['caption']}")
    md_content.append("")

    if section_data['entries']:
        # 添加 MyST toctree 指令
        md_content.append("```{toctree}") 
        md_content.append(":maxdepth: 1")
        md_content.append("")
        for entry in section_data['entries']:
            md_content.append(f"docs/{entry}") 
        # 移除最後的 ``` 關閉標籤，因為它是文件中的最後一個內容
        # md_content.append("```") # Removed
        # md_content.append("") # Removed

    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(md_content))
    print(f"Generated Sphinx sub-index file: {output_file_path}")

def generate_main_index_md_file(output_dir, sub_index_file_names):
    """
    生成主 index.md 文件，連結到子索引文件。
    """
    output_file_path = os.path.join(output_dir, "index.md")
    md_content = []

    # 添加頂級文件標題
    md_content.append("# 目錄")
    md_content.append("")

    # 添加 MyST toctree 指令
    md_content.append("```{toctree}") 
    md_content.append(":maxdepth: 2")
    md_content.append("")
    for sub_file in sub_index_file_names:
        md_content.append(f"{sub_file}")
    # 移除最後的 ``` 關閉標籤，因為它是文件中的最後一個內容
    # md_content.append("```") # Removed
    # md_content.append("") # Removed

    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(md_content))
    print(f"Generated Sphinx main index file: {output_file_path}")

def main():
    if len(sys.argv) != 2:
        print("Usage: bin/gen_index.py <version>", file=sys.stderr)
        sys.exit(1)
    
    version = sys.argv[1]
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir) # Go up one level from 'bin'

    source_dir = os.path.join(project_root, "workspace", "source")
    documentation_md_path = os.path.join(source_dir, "documentation.md")
    output_dir = os.path.join(project_root, "workspace", "preprocess", version)

    if not os.path.exists(documentation_md_path):
        print(f"Error: {documentation_md_path} not found.", file=sys.stderr)
        sys.exit(1)
    
    os.makedirs(output_dir, exist_ok=True)

    with open(documentation_md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    all_sections = parse_documentation_md(md_content)

    sub_index_file_names = []
    for i, section in enumerate(all_sections):
        # 處理 "API 說明文件" 這個特殊的 H2，它是一個外部連結，不應該被包含在 toctree 中
        if section['caption'] == 'API 說明文件' and not section['entries']:
            continue

        sub_file_name = f"index-{i+1}"
        sub_index_file_path = os.path.join(output_dir, f"{sub_file_name}.md")
        generate_sub_index_md_file(sub_index_file_path, section)
        sub_index_file_names.append(sub_file_name)

    generate_main_index_md_file(output_dir, sub_index_file_names)

if __name__ == "__main__":
    main()
