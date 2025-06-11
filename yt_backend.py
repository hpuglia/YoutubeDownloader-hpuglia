from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import threading
import os
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox
import re
import webbrowser

app = Flask(__name__)
CORS(app)

# Pasta padrão ~/Downloads/YouTube
output_folder = str(Path.home() / "Downloads" / "YouTube")
os.makedirs(output_folder, exist_ok=True)

download_status = {}
download_titles = {}

class DownloadUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("YouTube Downloader - HPuglia")
        self.root.geometry("700x480")

        # Frame lateral para botões de links
        side_frame = tk.Frame(self.root)
        side_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        self.create_side_button(side_frame, "📥 Instalar TamperMonkey", "https://www.tampermonkey.net/")
        self.create_side_button(side_frame, "⚙️ Instalar Script", "https://raw.githubusercontent.com/hpuglia/YoutubeDownloader-hpuglia/main/youtube-dl.user.js")

        # Frame principal
        main_frame = tk.Frame(self.root)
        main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.status_list = tk.Listbox(main_frame, width=80, height=20)
        self.status_list.pack(pady=10)

        btn_frame = tk.Frame(main_frame)
        btn_frame.pack()

        self.open_button = tk.Button(btn_frame, text="📂 Abrir pasta de saída", command=self.open_folder)
        self.open_button.grid(row=0, column=0, padx=5)

        self.change_button = tk.Button(btn_frame, text="🛠 Alterar pasta de saída", command=self.change_folder)
        self.change_button.grid(row=0, column=1, padx=5)

        self.clear_button = tk.Button(btn_frame, text="🧹 Limpar status", command=self.clear_status)
        self.clear_button.grid(row=0, column=2, padx=5)

        self.folder_label = tk.Label(main_frame, text=f"Pasta atual: {output_folder}", fg="blue")
        self.folder_label.pack(pady=5)

        # Botão Doação
        self.donate_button = tk.Button(
            main_frame,
            text="💖 Doação",
            command=self.open_donation_link,
            font=("Arial", 14, "bold"),
            fg="white",
            bg="#E91E63",
            activebackground="#AD1457",
            relief=tk.RAISED,
            bd=3,
            padx=15,
            pady=5
        )
        self.donate_button.pack(pady=10)
        self.animate_blink()

    def create_side_button(self, frame, text, url):
        btn = tk.Button(frame, text=text, width=22, command=lambda: webbrowser.open(url), anchor="w", relief=tk.RAISED)
        btn.pack(pady=2)

    def animate_blink(self):
        current_color = self.donate_button.cget("bg")
        new_color = "#F48FB1" if current_color == "#E91E63" else "#E91E63"
        self.donate_button.config(bg=new_color)
        self.root.after(700, self.animate_blink)

    def update_status(self, msg, download_id=None):
        if download_id:
            found = False
            for i in range(self.status_list.size()):
                line = self.status_list.get(i)
                if line.startswith(download_titles.get(download_id, download_id)):
                    self.status_list.delete(i)
                    self.status_list.insert(i, msg)
                    found = True
                    break
            if not found:
                self.status_list.insert(tk.END, msg)
        else:
            self.status_list.insert(tk.END, msg)
        self.status_list.yview_moveto(1)

    def clear_status(self):
        self.status_list.delete(0, tk.END)
        download_status.clear()
        download_titles.clear()

    def change_folder(self):
        global output_folder
        new_folder = filedialog.askdirectory()
        if new_folder:
            output_folder = new_folder
            self.folder_label.config(text=f"Pasta atual: {output_folder}")
            os.makedirs(output_folder, exist_ok=True)

    def open_folder(self):
        try:
            os.startfile(output_folder)
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir a pasta:\n{str(e)}")

    def open_donation_link(self):
        webbrowser.open("https://nubank.com.br/cobrar/na7j5/6847d4fc-4652-4c8c-9949-d499d2338b2a")

    def popup_complete(self, title):
        popup = tk.Toplevel(self.root)
        popup.title("Download concluído")
        tk.Label(popup, text=f"Download de '{title}' finalizado com sucesso!").pack(pady=10)
        tk.Button(popup, text="📂 Abrir pasta", command=self.open_folder, bg="green", fg="white").pack(pady=10)
        tk.Button(popup, text="Fechar", command=popup.destroy).pack(pady=5)

ui = DownloadUI()

def get_video_title(yt_dlp_path, url):
    try:
        result = subprocess.run(
            [yt_dlp_path, "--get-title", url],
            capture_output=True,
            text=True,
            check=True
        )
        title = result.stdout.strip()
        return re.sub(r'[\\/:"*?<>|]+', '_', title)
    except Exception:
        return url

def download_video(url, download_id):
    yt_dlp_path = "E:/Documents/yt-dlp.exe"
    title = get_video_title(yt_dlp_path, url)
    download_titles[download_id] = title

    download_status[download_id] = "⏳ Iniciando..."
    ui.update_status(f"{title} → ⏳ Iniciando...", download_id)

    process = subprocess.Popen(
        [yt_dlp_path, "-P", output_folder, "--newline", "--progress", "--print", "%(progress._percent_str)s", url],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    for line in process.stdout:
        line = line.strip()
        if "%" in line:
            download_status[download_id] = line
            ui.update_status(f"{title} → {line}", download_id)

    download_status[download_id] = "✅ Concluído"
    ui.update_status(f"{title} → ✅ Concluído ✅", download_id)
    ui.root.after(0, lambda: ui.popup_complete(title))

@app.route('/download')
def download():
    url = request.args.get('url')
    if url:
        download_id = url
        download_status[download_id] = "⏳ Iniciando..."
        ui.update_status(f"Iniciando download...", download_id)
        threading.Thread(target=download_video, args=(url, download_id), daemon=True).start()
        return jsonify({"id": download_id, "status": download_status[download_id]})
    return "URL inválida", 400

@app.route('/status')
def status():
    download_id = request.args.get('id')
    if download_id in download_status:
        return jsonify({"status": download_status[download_id]})
    return "ID inválida", 404

def start_flask():
    print("🚀 Backend YouTube Downloader com Interface iniciado!")
    app.run(host="127.0.0.1", port=5000)

if __name__ == "__main__":
    flask_thread = threading.Thread(target=start_flask, daemon=True)
    flask_thread.start()
    ui.root.mainloop()
