import os
import requests
from urllib.parse import urlparse

def download_file(url, directory, downloaded_assets, update_progress):
    if url in downloaded_assets:
        return  # Skip if already downloaded
    try:
        response = requests.get(url)
        response.raise_for_status()
        parsed_url = urlparse(url)
        subdir = os.path.join(directory, os.path.dirname(parsed_url.path.lstrip('/')))
        os.makedirs(subdir, exist_ok=True)
        file_path = os.path.join(subdir, os.path.basename(parsed_url.path))
        with open(file_path, 'wb') as file:
            file.write(response.content)
        update_progress(f"Downloaded {url} to {file_path}")
        downloaded_assets.add(url)  # Add to the set of downloaded assets
    except requests.RequestException as e:
        update_progress(f"Failed to download {url}: {e}")
