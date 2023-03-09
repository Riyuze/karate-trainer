import tkinter as tk
from tkinter import ttk

import sv_ttk


class Menu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.title_lbl = ttk.Label(self, text="Karate Trainer", font=("Times new roman", 30, "bold"))
        self.title_lbl.pack(pady=5)

        self.start_btn = ttk.Button(self, text="Start", width=40, command=lambda: controller.show_frame(Choice))
        self.start_btn.pack(pady=5)

        self.history_btn = ttk.Button(self, text="History", width=40, command= lambda: controller.show_frame(History))
        self.history_btn.pack(pady=5)

        self.quit_btn = ttk.Button(self, text="Quit", width=40, command=self.quit)
        self.quit_btn.pack(pady=5)

    def close(self):
        win.quit()


class Choice(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.OPTIONS = [
            "Heian Shodan",
        ]

        self.option_var = tk.StringVar(self)

        self.title_lbl = ttk.Label(self, text="Pick Your Training Plan", font=("Times new roman", 30, "bold"))
        self.title_lbl.pack(pady=5)

        self.option_menu = ttk.OptionMenu(self, self.option_var, "Select one...", *self.OPTIONS, command= lambda _: self.button_state())
        self.option_menu.config(width=38)
        self.option_menu.pack(pady=5)

        self.start_btn = ttk.Button(self, text="Start", width=40, command= lambda: self.start())
        self.start_btn.state(["disabled"])
        self.start_btn.pack(pady=5)

        self.back_btn = ttk.Button(self, text="Back", width=40, command= lambda: controller.show_frame(Menu))
        self.back_btn.pack(pady=5)

    def button_state(self):
        self.start_btn.state(["!disabled"])

    def start(self):
        train = self.option_var.get()
        print(f"Train: {train}")


class History(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        
        self.title_lbl = ttk.Label(self, text="History", font=("Times new roman", 30, "bold"))
        self.title_lbl.pack(pady=5)

        self.back_btn = ttk.Button(self, text="Back", width=40, command=lambda: controller.show_frame(Menu))
        self.back_btn.pack(pady=5)
    

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("1080x720")
        self.title("Karate Trainer")
        self.iconbitmap("./assets/karate_trainer.ico")

        sv_ttk.set_theme("dark")

        container = tk.Frame(self)

        container.pack(expand=True)

        self.frames = {}
        for F in (Menu, Choice, History):
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
