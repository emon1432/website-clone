from downloader.downloader import start_download

def download_thread(base_url, download_directory, update_progress):
    try:
        start_download(base_url, download_directory, update_progress)
        update_progress("Download completed!")
    except Exception as e:
        update_progress(f"Error: {e}")
