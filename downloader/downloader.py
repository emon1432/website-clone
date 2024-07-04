import os
import requests
from urllib.parse import urljoin, urlparse
from selenium import webdriver
from bs4 import BeautifulSoup
from downloader.link_extractor import get_all_links
from downloader.assets_downloader import download_assets
import time

def start_download(base_url, download_directory, update_progress):
    os.makedirs(download_directory, exist_ok=True)

    chrome_options = webdriver.ChromeOptions()
    prefs = {'download.default_directory': os.path.abspath(download_directory)}
    chrome_options.add_experimental_option('prefs', prefs)
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(options=chrome_options)

    downloaded_assets = set()
    visited = set()
    urls_to_visit = {base_url}

    while urls_to_visit:
        current_url = urls_to_visit.pop()
        if current_url in visited:
            continue
        
        update_progress(f"Opening: {current_url}")
        driver.get(current_url)
        driver.implicitly_wait(2)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        parsed_url = urlparse(current_url)
        html_subdir = os.path.join(download_directory, os.path.dirname(parsed_url.path.lstrip('/')))
        if not html_subdir:
            html_subdir = download_directory
        os.makedirs(html_subdir, exist_ok=True)
        html_filename = os.path.basename(parsed_url.path) if os.path.basename(parsed_url.path) else 'index.html'
        if os.path.isdir(os.path.join(html_subdir, html_filename)):
            html_filename = 'index.html'
        html_filepath = os.path.join(html_subdir, html_filename)
        html_content = "<!DOCTYPE html>\n" + driver.page_source
        with open(html_filepath, "w", encoding="utf-8") as file:
            file.write(html_content)
        
        update_progress(f"Saved HTML: {html_filepath}")
        visited.add(current_url)
        new_links = get_all_links(driver, current_url, visited)
        urls_to_visit.update(new_links)
        update_progress(f"Found {len(new_links)} new links")
        update_progress(f"Total URLs: {len(urls_to_visit) + len(visited)}")
        update_progress(f"Total Visited URLs: {len(visited)}")
        progress = len(visited) / (len(visited) + len(urls_to_visit)) * 100
        update_progress(f"Progress: {progress:.2f}%")
        
        download_assets(soup, current_url, download_directory, downloaded_assets, update_progress)

    driver.quit()
