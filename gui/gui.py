import tkinter as tk
from tkinter import filedialog
import threading
from gui.start_download import download_thread

def start_gui():
    def start_download():
        base_url = url_entry.get()
        download_directory = filedialog.askdirectory()
        if not download_directory:
            return
        progress_text.delete(1.0, tk.END)
        threading.Thread(target=download_thread, args=(base_url, download_directory, update_progress)).start()
        root.withdraw()
        progress_window.deiconify()

    def update_progress(message):
        progress_text.insert(tk.END, message + "\n")
        progress_text.see(tk.END)

        if message.startswith("Opening:"):
            current_url_label.config(text=message.split("Opening: ")[-1])
        elif message.startswith("Asset:"):
            asset_url_label.config(text=message.split("Asset: ")[-1])
        elif message.startswith("Total Visited URLs:"):
            total_visited_label.config(text=message.split("Total Visited URLs: ")[-1])
        elif message.startswith("Total URLs:"):
            total_urls_label.config(text=message.split("Total URLs: ")[-1])
        elif message.startswith("Progress:"):
            progress = message.split("Progress: ")[-1]
            progress_label.config(text=progress)

    root = tk.Tk()
    root.title("Website Downloader")
    
    tk.Label(root, text="Base URL:").pack(pady=10)
    url_entry = tk.Entry(root, width=50)
    url_entry.pack(pady=5)

    tk.Button(root, text="Download", command=start_download).pack(pady=20)

    progress_window = tk.Toplevel(root)
    progress_window.title("Download Progress")
    progress_window.geometry("800x1000")
    progress_window.withdraw()

    progress_frame = tk.Frame(progress_window, padx=20, pady=20)
    progress_frame.pack(expand=True, fill=tk.BOTH)

    tk.Label(progress_frame, text="Website Downloader", font=("Arial", 16, "bold")).pack(pady=10)
    
    tk.Label(progress_frame, text="Total URLs: ", font=("Arial", 12, "bold", "underline")).pack(pady=5)
    total_urls_label = tk.Label(progress_frame, text="Calculating...")
    total_urls_label.pack(pady=5)
    
    tk.Label(progress_frame, text="Total Visited: ", font=("Arial", 12, "bold", "underline")).pack(pady=5)
    total_visited_label = tk.Label(progress_frame, text="Calculating...")
    total_visited_label.pack(pady=5)

    tk.Label(progress_frame, text="Current URL : ", font=("Arial", 12, "bold", "underline")).pack(pady=5)
    current_url_label = tk.Label(progress_frame, text="")
    current_url_label.pack(pady=5)
    
    tk.Label(progress_frame, text="Assets Downloaded: ", font=("Arial", 12, "bold", "underline")).pack(pady=5)
    asset_url_label = tk.Label(progress_frame, text="Fetching...")
    asset_url_label.pack(pady=5)
    
    tk.Label(progress_frame, text="Progress: ", font=("Arial", 12, "bold", "underline")).pack(pady=5)
    progress_label = tk.Label(progress_frame, text="Calculating...")
    progress_label.pack(pady=5)
    
    progress_text = tk.Text(progress_frame)
    progress_text.pack(expand=True, fill=tk.BOTH)

    def close_progress_window():
        progress_window.withdraw()
        root.deiconify()

    tk.Button(progress_frame, text="Close", command=close_progress_window).pack(pady=10)

    root.mainloop()
