from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from downloader.file_downloader import download_file

def download_assets(soup, base_url, download_directory, downloaded_assets, update_progress):
    tags = {'img': 'src', 'link': 'href', 'script': 'src'}
    base_domain = urlparse(base_url).netloc
    for tag, attr in tags.items():
        for element in soup.find_all(tag):
            url = element.get(attr)
            if url:
                full_url = urljoin(base_url, url)
                if urlparse(full_url).netloc == base_domain:
                    download_file(full_url, download_directory, downloaded_assets, update_progress)
