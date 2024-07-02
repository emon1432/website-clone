from urllib.parse import urljoin
from bs4 import BeautifulSoup
from downloader.file_downloader import download_file

def download_assets(soup, base_url, download_directory, downloaded_assets, update_progress):
    tags = {'img': 'src', 'link': 'href', 'script': 'src'}
    for tag, attr in tags.items():
        for element in soup.find_all(tag):
            url = element.get(attr)
            if url:
                if not url.startswith(('http', 'https')):
                    url = urljoin(base_url, url)
                download_file(url, download_directory, downloaded_assets, update_progress)
