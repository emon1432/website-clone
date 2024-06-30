import os
import requests
from urllib.parse import urljoin, urlparse
from selenium import webdriver
from bs4 import BeautifulSoup
import time

# Base URL to start from
base_url = "https://spruko.com/"

# Directory to save the downloaded files
download_directory = "spruko"

# Ensure the download directory exists
os.makedirs(download_directory, exist_ok=True)

# Configure Chrome options to automatically save files to a directory
chrome_options = webdriver.ChromeOptions()
prefs = {'download.default_directory': os.path.abspath(download_directory)}
chrome_options.add_experimental_option('prefs', prefs)

# Initialize ChromeDriver
driver = webdriver.Chrome(options=chrome_options)

# Function to download a file
def download_file(url, directory):
    try:
        response = requests.get(url)
        response.raise_for_status()
        parsed_url = urlparse(url)
        subdir = os.path.join(directory, os.path.dirname(parsed_url.path.lstrip('/')))
        os.makedirs(subdir, exist_ok=True)
        file_path = os.path.join(subdir, os.path.basename(parsed_url.path))
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded {url} to {file_path}")
    except requests.RequestException as e:
        print(f"Failed to download {url}: {e}")

# Function to get all the page links from the base URL
def get_all_links(base_url, visited):
    driver.get(base_url)
    time.sleep(2)  # Wait for the page to load completely
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    links = set()
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if href.endswith('.html'):
            full_url = urljoin(base_url, href)
            if full_url not in visited:
                links.add(full_url)
    return links

# Function to download assets
def download_assets(soup, base_url, download_directory):
    tags = {'img': 'src', 'link': 'href', 'script': 'src'}
    for tag, attr in tags.items():
        for element in soup.find_all(tag):
            url = element.get(attr)
            if url:
                if not url.startswith(('http', 'https')):
                    url = urljoin(base_url, url)
                download_file(url, download_directory)

# Set of visited URLs to avoid processing the same URL multiple times
visited = set()

# Queue of URLs to process
urls_to_visit = {base_url}

while urls_to_visit:
    current_url = urls_to_visit.pop()
    if current_url in visited:
        continue
    
    print("Opening:", current_url)
    driver.get(current_url)
    time.sleep(2)  # Wait for the page to load completely

    # Parse the page content
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Save the HTML content
    parsed_url = urlparse(current_url)
    html_subdir = os.path.join(download_directory, os.path.dirname(parsed_url.path.lstrip('/')))
    if not html_subdir:  # Ensure we always have a valid subdir
        html_subdir = download_directory
    os.makedirs(html_subdir, exist_ok=True)
    html_filename = os.path.basename(parsed_url.path) if os.path.basename(parsed_url.path) else 'index.html'
    html_filepath = os.path.join(html_subdir, html_filename)
    with open(html_filepath, "w", encoding="utf-8") as file:
        file.write(driver.page_source)

    # Download all assets
    download_assets(soup, current_url, download_directory)

    # Mark the current URL as visited
    visited.add(current_url)

    # Find new links and add them to the queue
    new_links = get_all_links(current_url, visited)
    urls_to_visit.update(new_links)

# Quit the WebDriver session
driver.quit()
