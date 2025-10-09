import os
import re
import base64
import hashlib

def process_base64_images(content: str, image_output_dir: str) -> str:
    """
    Find all <img> tags and markdown images with base64 encoded images,
    save them as files, and replace the src attribute with the path to the new file.
    """
    new_content = content

    # Pattern for markdown: ![alt text](data:...)
    markdown_pattern = re.compile(r'(!\[[^\]]*?\]\()'
                                  r'(data:image/(?:png|jpeg|gif|svg\+xml);base64,([^)]*))'
                                  r'(\))')
    
    # Process markdown images
    # Iterate backwards to not mess up indices of subsequent matches
    for match in reversed(list(markdown_pattern.finditer(new_content))):
        prefix = match.group(1)
        data_uri = match.group(2)
        base64_data = match.group(3)
        suffix = match.group(4)
        
        mime_type_search = re.search(r'data:image/(png|jpeg|gif|svg\+xml)', data_uri)
        if not mime_type_search:
            continue
        mime_type_group = mime_type_search.group(1)

        if mime_type_group == "svg+xml":
            ext = "svg"
        else:
            ext = mime_type_group

        try:
            image_hash = hashlib.md5(base64_data.encode()).hexdigest()
            image_filename = f"{image_hash}.{ext}"
            local_image_path = os.path.join(image_output_dir, image_filename)

            # 這裡因為 sphinx 會自動判斷 _static , 所以不需要 ../
            new_image_src = f"_static/laravel/{image_filename}"

            print(f"  - Found markdown base64 image: {image_hash}")
            print(f"    - Saving to: {new_image_src}")

            image_data = base64.b64decode(base64_data)
            with open(local_image_path, 'wb') as f:
                f.write(image_data)

            # Replace the whole matched part to be safe
            start, end = match.span()
            new_full_string = f"{prefix}{new_image_src}{suffix}"
            new_content = new_content[:start] + new_full_string + new_content[end:]

        except Exception as e:
            print(f"    - Failed to process markdown base64 image: {e}")

    # Pattern for <img> tags: <img src="data:...">
    img_tag_pattern = re.compile(r'(<img[^>]*?src=")'
                                 r'(data:image/(?:png|jpeg|gif|svg\+xml);base64,([^"]*))'
                                 r'(")')

    # Process <img> tags
    # Iterate backwards here as well
    for match in reversed(list(img_tag_pattern.finditer(new_content))):
        prefix = match.group(1)
        data_uri = match.group(2)
        base64_data = match.group(3)
        suffix = match.group(4)

        mime_type_search = re.search(r'data:image/(png|jpeg|gif|svg\+xml)', data_uri)
        if not mime_type_search:
            continue
        mime_type_group = mime_type_search.group(1)

        if mime_type_group == "svg+xml":
            ext = "svg"
        else:
            ext = mime_type_group

        try:
            image_hash = hashlib.md5(base64_data.encode()).hexdigest()
            image_filename = f"{image_hash}.{ext}"
            local_image_path = os.path.join(image_output_dir, image_filename)
            new_image_src = f"../_static/laravel/{image_filename}"

            print(f"  - Found <img> base64 image: {image_hash}")
            print(f"    - Saving to: {new_image_src}")

            image_data = base64.b64decode(base64_data)
            with open(local_image_path, 'wb') as f:
                f.write(image_data)

            # Replace the whole matched part
            start, end = match.span()
            new_full_string = f"{prefix}{new_image_src}{suffix}"
            new_content = new_content[:start] + new_full_string + new_content[end:]

        except Exception as e:
            print(f"    - Failed to process <img> base64 image: {e}")

    return new_content