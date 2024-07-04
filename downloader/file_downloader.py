import os
import requests
from urllib.parse import urlparse

def download_file(url, directory, downloaded_assets, update_progress):
    if url in downloaded_assets:
        return
    try:
        parsed_url = urlparse(url)
        subdir = os.path.join(directory, os.path.dirname(parsed_url.path.lstrip('/')))
        os.makedirs(subdir, exist_ok=True)
        file_path = os.path.join(subdir, os.path.basename(parsed_url.path))

        if os.path.exists(file_path):
            update_progress(f"Skipped (already exists): {url}")
            downloaded_assets.add(url)
            return

        response = requests.get(url)
        response.raise_for_status()

        with open(file_path, 'wb') as file:
            file.write(response.content)

        update_progress(f"Asset: {url}")
        downloaded_assets.add(url)
    except requests.RequestException as e:
        update_progress(f"Failed to download {url}: {e}")
