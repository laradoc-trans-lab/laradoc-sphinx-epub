import os
import re
import requests
import hashlib
from urllib.parse import urlparse

def _download_image(url: str, save_path: str) -> bool:
    """下載指定 URL 的圖片並儲存到指定路徑。"""
    try:
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    except requests.exceptions.RequestException as e:
        print(f"    - Error downloading {url}: {e}")
        return False

def process_images(content: str, image_output_dir: str) -> str:
    """處理 Markdown 內容中的圖片，下載並替換路徑。"""
    img_urls = re.findall(r'<img[^>]+src="([^"]+)"', content)
    if not img_urls:
        return content

    content = re.sub(r'(<img[^>]*)(?<!/)>', r'\1 />', content)

    for url in set(img_urls):
        if not url.startswith('https://'):
            continue

        try:
            image_filename = os.path.basename(urlparse(url).path)
            if not image_filename:
                image_filename = "img_" + hashlib.md5(url.encode()).hexdigest()[:10]

            local_image_path = os.path.join(image_output_dir, image_filename)
            new_image_src = f"_static/laravel/{image_filename}"
            
            print(f"  - Found image: {url}")
            print(f"    - Downloading to: {new_image_src}")
            
            if _download_image(url, local_image_path):
                content = content.replace(url, new_image_src)

        except Exception as e:
            print(f"    - Failed to process image URL {url}: {e}")
            
    return content
