import tkinter as tk
from tkinter import ttk

import sv_ttk

def start(text):
    print(text)

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("1080x720")
        self.title("Karate Trainer")
        self.iconbitmap("./assets/karate_trainer.ico")

        self.create_widgets()
    
    def create_widgets(self):
        title_lbl = ttk.Label(self, text="Karate Trainer", font=("Arial Bold", 30)).pack(pady=5)

        start_btn = ttk.Button(self, text="Start", width=40, command=lambda: start("Test")).pack(pady=5)
        quit_btn = ttk.Button(self, text="Quit", width=40).pack(pady=5)

        sv_ttk.set_theme("dark")

if __name__ == "__main__":
    try:  
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    finally:
        app = App()
        app.mainloop()
    