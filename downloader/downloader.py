import os
import requests
from urllib.parse import urljoin, urlparse
from selenium import webdriver
from bs4 import BeautifulSoup
from downloader.link_extractor import get_all_links
from downloader.assets_downloader import download_assets
import time

def start_download(base_url, download_directory, update_progress):
    # Ensure the download directory exists
    os.makedirs(download_directory, exist_ok=True)

    # Configure Chrome options to automatically save files to a directory
    chrome_options = webdriver.ChromeOptions()
    prefs = {'download.default_directory': os.path.abspath(download_directory)}
    chrome_options.add_experimental_option('prefs', prefs)
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode

    # Initialize ChromeDriver
    driver = webdriver.Chrome(options=chrome_options)

    # Set to keep track of downloaded asset URLs
    downloaded_assets = set()

    # Set of visited URLs to avoid processing the same URL multiple times
    visited = set()

    # Queue of URLs to process
    urls_to_visit = {base_url}

    while urls_to_visit:
        current_url = urls_to_visit.pop()
        if current_url in visited:
            continue
        
        update_progress(f"Opening: {current_url}")
        driver.get(current_url)
        driver.implicitly_wait(2)  # Wait for the page to load completely

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
        
        update_progress(f"Saved HTML: {html_filepath}")

        # Mark the current URL as visited
        visited.add(current_url)

        # Find new links and add them to the queue
        new_links = get_all_links(driver, current_url, visited)
        urls_to_visit.update(new_links)
        update_progress(f"Found {len(new_links)} new links")
        update_progress(f"Total URLs: {len(urls_to_visit) + len(visited)}")
        update_progress(f"Total Visited URLs: {len(visited)}")
        progress = len(visited) / (len(visited) + len(urls_to_visit)) * 100
        update_progress(f"Progress: {progress:.2f}%")
        
        # Download all assets
        download_assets(soup, current_url, download_directory, downloaded_assets, update_progress)

    # Quit the WebDriver session
    driver.quit()
