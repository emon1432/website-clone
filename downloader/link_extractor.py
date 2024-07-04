import time
from urllib.parse import urljoin
from bs4 import BeautifulSoup

def get_all_links(driver, base_url, visited):
    driver.get(base_url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    links = set()
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if href.endswith('.html'):
            full_url = urljoin(base_url, href)
            if full_url not in visited:
                links.add(full_url)
    return links
