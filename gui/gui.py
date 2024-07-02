import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import threading
from gui.start_download import download_thread

def start_gui():
    def start_download():
        base_url = url_entry.get()
        download_directory = filedialog.askdirectory()
        if not download_directory:
            return
        progress_text.delete(1.0, tk.END)  # Clear previous progress
        threading.Thread(target=download_thread, args=(base_url, download_directory, update_progress)).start()
        root.withdraw()  # Hide the main window
        progress_window.deiconify()  # Show the progress window

    def update_progress(message):
        progress_text.insert(tk.END, message + "\n")
        progress_text.see(tk.END)

    root = tk.Tk()
    root.title("Website Downloader")

    tk.Label(root, text="Base URL:").pack(pady=10)
    url_entry = tk.Entry(root, width=50)
    url_entry.pack(pady=5)

    tk.Button(root, text="Download", command=start_download).pack(pady=20)

    progress_window = tk.Toplevel(root)
    progress_window.title("Download Progress")
    progress_window.geometry("500x400")
    progress_window.withdraw()  # Hide initially

    progress_text = tk.Text(progress_window)
    progress_text.pack(expand=True, fill=tk.BOTH)

    root.mainloop()
