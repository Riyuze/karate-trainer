import tkinter as tk
from tkinter import ttk

import sv_ttk


class Menu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.title_lbl = ttk.Label(self, text="Karate Trainer", font=("Times new roman", 30, "bold")).pack(pady=5)

        self.start_btn = ttk.Button(self, text="Start", width=40).pack(pady=5)
        self.history_btn = ttk.Button(self, text="History", width=40, command= lambda: controller.show_frame(History)).pack(pady=5)
        self.quit_btn = ttk.Button(self, text="Quit", width=40, command=self.quit).pack(pady=5)

    def close(self):
        win.quit()

class History(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.title_lbl = ttk.Label(self, text="History", font=("Times new roman", 30, "bold")).pack(pady=5)

        self.back_btn = ttk.Button(self, text="Back", width=40, command=lambda: controller.show_frame(Menu)).pack(pady=5)
    

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.geometry("1080x720")
        self.title("Karate Trainer")
        self.iconbitmap("./assets/karate_trainer.ico")

        sv_ttk.set_theme("dark")

        container = tk.Frame(self)

        container.pack(expand=True)

        self.frames = {}
        for F in (Menu, History):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Menu)

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()

if __name__ == "__main__":
    try:  
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    finally:
        app = App()
        app.mainloop()
