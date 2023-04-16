import tkinter as tk
from tkinter import ttk
import sv_ttk
import cv2
import time
from playsound import playsound
import os
from PIL import Image, ImageTk


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
            "a_hidari_gedan_barai", "b_migi_chudan_oi_zuki", "c_migi_gedan_barai", "d_migi_tetsui_uchi", "e_hidari_chudan_oi_zuki", 
            "f_hidari_gedan_barai", "g_migi_jodan_age_uke", "h_hidari_age_uke_jodan", "i_migi_jodan_age_uke", "j_hidari_gedan_barai",
            "k_migi_chudan_oi_zuki", "l_migi_gedan_barai", "m_hidari_chudan_oi_zuki", "n_hidari_gedan_barai", "o_migi_chudan_oi_zuki",
            "p_hidari_chudan_oi_zuki", "q_migi_chudan_oi_zuki", "r_hidari_chudan_shuto_uke", "s_migi_chudan_shuto_uke", "t_migi_chudan_shuto_uke",
            "u_hidari_chudan_shuto_uke", "v_yame_hachiji_dachi"
        ]

        self.started = False

        self.TIMER = 10

        self.index = 0

        self.title_lbl = ttk.Label(self, text="Train", font=("Times new roman", 30, "bold"))
        self.title_lbl.pack(pady=5)

        self.camera_btn = ttk.Button(self, text="Show Camera", width=40, command=lambda: self.show_camera())
        self.camera_btn.pack(pady=5)

        self.preview_btn = ttk.Button(self, text="Preview", width=40, command= lambda: controller.show_frame(Preview))
        self.preview_btn.pack(pady=5)

        self.back_btn = ttk.Button(self, text="Back", width=40, command=lambda: controller.show_frame(Choice))
        self.back_btn.pack(pady=5)

    def show_camera(self):
        self.cap = cv2.VideoCapture(0)

        self.width, self.height = 1920, 1080

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        
        self.font = cv2.FONT_HERSHEY_SIMPLEX

        while True:
            _, self.img = self.cap.read()
            cv2.imshow("Camera", self.img)

            self.k = cv2.waitKey(1)

            if self.k == 32:
                playsound("./assets/beep.wav", block=False)
                self.prev = time.time()
                while self.TIMER > 0:
                    _, self.img = self.cap.read()

                    self.current = time.time()
                    if self.current - self.prev >= 1:
                        self.prev = self.current
                        self.TIMER -= 1
                        if self.TIMER > 0:
                            playsound("./assets/beep.wav", block=False)
                    
                    cv2.putText(self.img, str(self.TIMER), (0, 25), self.font, 1, (255, 255, 255), 1, cv2.LINE_AA)
                    cv2.imshow("Camera", self.img)
                    cv2.waitKey(1)

                else:
                    _, self.img = self.cap.read()

                    if self.TIMER == 0:
                        cv2.putText(self.img, "Start!", (0, 25), self.font, 1, (255, 255, 255), 1, cv2.LINE_AA)
                        playsound("./assets/double_beep.wav", block=False)
                        cv2.imshow("Camera", self.img)
                        cv2.waitKey(250)

                        while True:
                            _, self.img = self.cap.read()

                            self.prev = time.time()
                            self.TIMER = 2

                            while self.TIMER > 0:  
                                _, self.img = self.cap.read()
                                self.current = time.time()
                                if self.current - self.prev >= 1:
                                    self.prev = self.current
                                    self.TIMER -= 1

                                cv2.putText(self.img, str(self.TIMER), (0, 25), self.font, 1, (255, 255, 255), 1, cv2.LINE_AA)
                                cv2.imshow("Camera", self.img)
                                cv2.waitKey(1)

                            if self.TIMER == 0:
                                _, self.img = self.cap.read()
                                cv2.imshow("Camera", self.img)
                                cv2.waitKey(1)
                                
                                playsound("./assets/double_beep.wav", block=False)
                                cv2.imwrite(f"temp/{self.HEIAN_SHODAN[self.index]}.png", self.img)
                                self.index += 1
                            
                            else:
                                _, self.img = self.cap.read()
                                cv2.imshow("Camera", self.img)
                                cv2.waitKey(1)

                            if self.index == 2: #Heian Shodan 22
                                self.TIMER = 10
                                self.index = 0
                                playsound("./assets/training_finished.mp3", block=False)
                                break

                    cv2.imshow("Camera", self.img)
                    cv2.waitKey(1)

            elif self.k == 27:
                break

        self.cap.release()

        cv2.destroyAllWindows()


class Preview(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.image_list = []
        self.text_list = []
        self.image_txt = tk.StringVar()
        self.image_txt.set("Press Get Image Button.")
        self.tkimage = ""

        self.current = 0

        self.title_lbl = ttk.Label(self, text="Preview", font=("Times new roman", 30, "bold"))
        self.title_lbl.pack(pady=5)

        self.image_lbl = ttk.Label(self, textvariable=self.image_txt, image=self.tkimage, compound=tk.TOP)
        self.image_lbl.pack(pady=5)

        self.get_image_btn = ttk.Button(self, text="Get Image", width=40, command= lambda: self.get_images())
        self.get_image_btn.pack(pady=5)

        self.prev_btn = ttk.Button(self, text="Previous", width=20, command= lambda: self.move(-1))
        self.prev_btn.pack(pady=5)
        self.prev_btn.state(["disabled"])

        self.next_btn = ttk.Button(self, text="Next", width=20, command= lambda: self.move(1))
        self.next_btn.pack(pady=5)
        self.next_btn.state(["disabled"])

        self.process_btn = ttk.Button(self, text="Process", width=40, command= self.process())
        self.process_btn.pack(pady=5)
        self.process_btn.state(["disabled"])

        self.back_btn = ttk.Button(self, text="Back", width=40, command=lambda: self.back(controller))
        self.back_btn.pack(pady=5)

    def move(self, delta):
        self.current += delta

        self.image_txt.set(self.text_list[self.current])
        self.image = Image.open(f"temp/{self.image_list[self.current]}")
        self.tkimage = ImageTk.PhotoImage(self.image)
        self.image_lbl["image"] = self.tkimage

        if self.current == (len(self.image_list) - 1):
            self.next_btn.state(["disabled"])
            self.prev_btn.state(["!disabled"])
        elif self.current == 0:
            self.next_btn.state(["!disabled"])
            self.prev_btn.state(["disabled"])
        else:
            self.next_btn.state(["!disabled"])
            self.prev_btn.state(["!disabled"])

    def get_images(self):
        self.image_list = os.listdir("./temp")
        self.text_list = [item.removesuffix(".png") for item in self.image_list]

        self.image_txt.set(self.text_list[0])
        self.image = Image.open(f"temp/{self.image_list[0]}")
        self.tkimage = ImageTk.PhotoImage(self.image)
        self.image_lbl["image"] = self.tkimage

        self.get_image_btn.state(["disabled"])

        if len(self.image_list) > 1:
            self.next_btn.state(["!disabled"])
            self.process_btn.state(["!disabled"])

    def process(self):
        print("Process Started!")

    def back(self, controller):
        self.image_list = []
        self.text_list = []
        self.image_txt.set("Press Get Image Button.")
        self.tkimage = ""

        self.current = 0

        self.image_lbl["image"] = self.tkimage

        self.get_image_btn.state(["!disabled"])
        self.next_btn.state(["disabled"])
        self.prev_btn.state(["disabled"])

        controller.show_frame(Train)


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
        for F in (Menu, Choice, History, Train, Preview):
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
