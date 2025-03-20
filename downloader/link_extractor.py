from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

def get_all_links(driver, base_url, visited):
    driver.get(base_url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    base_domain = urlparse(base_url).netloc  # Get the base domain
    links = set()
    
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        full_url = urljoin(base_url, href)
        parsed_url = urlparse(full_url)

        # Only add links that belong to the same domain
        if parsed_url.netloc == base_domain and full_url not in visited:
            links.add(full_url)

    return links
