import tkinter as tk
from tkinter import ttk

import sv_ttk

import cv2

from PIL import Image, ImageTk

import time


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

        self.start_btn = ttk.Button(self, text="Start", width=40, command= lambda: self.start(controller))
        self.start_btn.state(["disabled"])
        self.start_btn.pack(pady=5)

        self.back_btn = ttk.Button(self, text="Back", width=40, command= lambda: controller.show_frame(Menu))
        self.back_btn.pack(pady=5)

    def button_state(self):
        self.start_btn.state(["!disabled"])

    def start(self, controller):
        train = self.option_var.get()
        if train == "Heian Shodan":
            controller.show_frame(Train)


class Train(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.HEIAN_SHODAN = [
            "a_hidari_gedan_barai", "b_migi_chudan_oi_zuki.png", "c_migi_gedan_barai", "d_migi_tetsui_uchi", "e_hidari_chudan_oi_zuki", 
            "f_hidari_gedan_barai", "g_migi_jodan_age_uke", "h_hidari_age_uke_jodan", "i_migi_jodan_age_uke", "j_hidari_gedan_barai",
            "k_migi_chudan_oi_zuki", "l_migi_gedan_barai", "m_hidari_chudan_oi_zuki", "n_hidari_gedan_barai", "o_migi_chudan_oi_zuki",
            "p_hidari_chudan_oi_zuki", "q_migi_chudan_oi_zuki", "r_hidari_chudan_shuto_uke", "s_migi_chudan_shuto_uke", "t_migi_chudan_shuto_uke",
            "u_hidari_chudan_shuto_uke", "v_yame_hachiji_dachi"
        ]

        self.started = False

        self.TIMER = 10

        self.title_lbl = ttk.Label(self, text="Train", font=("Times new roman", 30, "bold"))
        self.title_lbl.pack(pady=5)

        self.camera_btn = ttk.Button(self, text="Show Camera", width=40, command=lambda: self.show_camera())
        self.camera_btn.pack(pady=5)

        self.back_btn = ttk.Button(self, text="Back", width=40, command=lambda: controller.show_frame(Choice))
        self.back_btn.pack(pady=5)

    def show_camera(self):
        self.cap = cv2.VideoCapture(0)

        self.width, self.height = 1920, 1080

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

        while True:
            _, self.img = self.cap.read()
            cv2.imshow("Camera", self.img)

            self.k = cv2.waitKey(125)

            if self.k == 32:
                self.prev = time.time()
                while self.TIMER >= 0:
                    _, self.img = self.cap.read()

                    self.font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(self.img, str(self.TIMER), (200, 250), self.font, 7, (0, 255, 255), 4, cv2.LINE_AA)

                    cv2.imshow("Camera", self.img)
                    cv2.waitKey(125)

                    self.current = time.time()
                    if self.current - self.prev >= 1:
                        self.prev = self.current
                        self.TIMER -= 1

                else:
                    _, self.img = self.cap.read()

                    cv2.imshow("Camera", self.img)

            elif self.k == 27:
                break

        self.cap.release()

        cv2.destroyAllWindows()


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
        #self.attributes('-fullscreen', True)

        sv_ttk.set_theme("dark")

        container = tk.Frame(self)

        container.pack(expand=True)

        self.frames = {}
        for F in (Menu, Choice, History, Train):
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
