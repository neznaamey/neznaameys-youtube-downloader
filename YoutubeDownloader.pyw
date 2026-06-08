import customtkinter as ctk
from tkinter import filedialog, messagebox
import yt_dlp
import threading
import os
import re
import sys

def resource_path(relative_path):
    """Získá cestu k souborům, když je program zabalený v .exe"""
    try:
        # PyInstaller ukládá soubory do této dočasné složky
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Nastavení vzhledu
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class DownloaderApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("neznaamey's yt downloader")
        self.geometry("500x560")
        
        # Načtení ikonky i uvnitř .exe
        try:
            self.iconbitmap(resource_path("icon.ico"))
        except:
            pass
            
        self.myth_green = "#2ecc71" 
        self.bg_dark = "#1a1a1a"   
        self.configure(fg_color=self.bg_dark)

        # UI Prvky
        self.url_entry = ctk.CTkEntry(self, placeholder_text="Vlož URL adresu YouTube videa", width=400, border_color=self.myth_green)
        self.url_entry.pack(pady=20)

        self.format_menu = ctk.CTkOptionMenu(self, values=["MP4 (Video)", "MP3 (Audio)"],
                                            fg_color=self.bg_dark, button_color=self.myth_green,
                                            command=self.update_quality_menu)
        self.format_menu.pack(pady=10)

        self.quality_menu = ctk.CTkOptionMenu(self, values=["Nejlepší", "4K (2160p)", "1440p", "1080p", "720p", "480p"],
                                            fg_color=self.bg_dark, button_color=self.myth_green)
        self.quality_menu.pack(pady=10)

        self.btn_path = ctk.CTkButton(self, text="Vybrat složku pro uložení", fg_color=self.myth_green, hover_color="#27ae60", command=self.select_path)
        self.btn_path.pack(pady=10)
        
        self.path_label = ctk.CTkLabel(self, text="Cesta: Nezvolena", text_color="gray", font=("Arial", 11))
        self.path_label.pack()
        
        self.progress_bar = ctk.CTkProgressBar(self, width=400, progress_color=self.myth_green)
        self.progress_bar.pack(pady=20)
        self.progress_bar.set(0)

        self.btn_download = ctk.CTkButton(self, text="STÁHNOUT", fg_color=self.myth_green, hover_color="#27ae60", command=self.start_download_thread)
        self.btn_download.pack(pady=20)
        self.download_path = ""

    def update_quality_menu(self, choice):
        if "MP4" in choice:
            self.quality_menu.configure(values=["Nejlepší", "4K (2160p)", "1440p", "1080p", "720p", "480p"])
        else:
            self.quality_menu.configure(values=["320kbps", "192kbps", "128kbps"])

    def select_path(self):
        self.download_path = filedialog.askdirectory()
        if self.download_path:
            self.path_label.configure(text=f"Ukládám do: {self.download_path}", text_color="white")

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            try:
                p = d.get('_percent_str', '0%').replace('%', '')
                self.progress_bar.set(float(p) / 100)
            except: pass

    def start_download_thread(self):
        url = self.url_entry.get()
        if not re.search(r'(youtube\.com|youtu\.be)', url):
            messagebox.showerror("Chyba", "Kámo, tohle ale není YouTube.")
            return
            
        if not self.download_path:
            messagebox.showwarning("Pozor", "Nejdříve vyber složku!")
            return
        threading.Thread(target=self.download_video, daemon=True).start()

    def download_video(self):
        url = self.url_entry.get()
        fmt = self.format_menu.get()
        qual = self.quality_menu.get()
        
        class QuietLogger:
            def debug(self, msg): pass
            def warning(self, msg): pass
            def error(self, msg): pass

        ydl_opts = {
            'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),
            'progress_hooks': [self.progress_hook],
            'ffmpeg_location': r"C:\ffmpeg\bin",
            'logger': QuietLogger(),
        }

        if "MP3" in fmt:
            bitrate = re.findall(r'\d+', qual)[0]
            ydl_opts.update({'format': 'bestaudio/best', 'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': bitrate}]})
        else:
            if qual == "Nejlepší":
                ydl_opts['format'] = 'best'
            else:
                res = re.findall(r'\d+', qual)[0]
                ydl_opts['format'] = f'bestvideo[height<={res}]+bestaudio/best'

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl: ydl.download([url])
            messagebox.showinfo("Hotovo", "Staženo!")
            self.progress_bar.set(0)
        except Exception:
            # Záchranná brzda - stahování bez FFmpeg
            try:
                with yt_dlp.YoutubeDL({'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'), 'logger': QuietLogger()}) as ydl:
                    ydl.download([url])
                messagebox.showinfo("Hotovo", "Staženo v nejlepší dostupné kvalitě (bez FFmpeg).")
                self.progress_bar.set(0)
            except:
                messagebox.showerror("Chyba", "Stahování selhalo. Zkontroluj odkaz.")

if __name__ == "__main__":
    app = DownloaderApp()
    app.mainloop()