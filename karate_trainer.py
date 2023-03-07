import tkinter as tk

import sv_ttk

def start():
    print("Hello!")

def main():
    root = tk.Tk()
    root.title("Karate Trainer")
    root.geometry("1080x720")
    root.iconbitmap("./assets/karate_trainer.ico")

    title_lbl = tk.Label(root, text="Karate Trainer", font=("Arial Bold", 30))
    title_lbl.pack()

    start_btn = tk.Button(root, text="Start", width=40, command=start)
    start_btn.pack()

    sv_ttk.set_theme("dark")

    try:  
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    finally:
        root.mainloop()

if __name__ == "__main__":
    main()