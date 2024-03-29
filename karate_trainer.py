import tkinter as tk
from tkinter import ttk
import sv_ttk
import cv2
import time
from playsound import playsound
import os
from PIL import Image, ImageTk
from datetime import datetime
from person_detector import person_detector
from get_coordinates import get_coordinates
from test_prediction import calculate_similarity, plot
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pygrabber.dshow_graph import FilterGraph
import matplotlib.pyplot as plt


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
        self.train = self.option_var.get()
        if self.train == "Heian Shodan":
            # Change settings according to settings chosen
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

        self.info_txt = "Press Space to start training.\nPress Escape to close camera."

        self.graph = FilterGraph()

        self.devices = enumerate(self.graph.get_input_devices())
        self.devices_list = {item: count for count, item in self.devices}

        self.OPTIONS = self.devices_list

        self.option_var = tk.StringVar(self)

        self.TIMER = 10

        self.index = 0

        self.title_lbl = ttk.Label(self, text="Train", font=("Times new roman", 30, "bold"))
        self.title_lbl.pack(pady=5)

        self.info_lbl = ttk.Label(self, text=self.info_txt, font=("Times new roman", 12, "normal"))
        self.info_lbl.pack(pady=5)

        self.option_menu = ttk.OptionMenu(self, self.option_var, "Select one...", *self.OPTIONS, command= lambda _: self.button_state())
        self.option_menu.config(width=38)
        self.option_menu.pack(pady=5)

        self.camera_btn = ttk.Button(self, text="Show Camera", width=40, command=lambda: self.show_camera())
        self.camera_btn.state(["disabled"])
        self.camera_btn.pack(pady=5)

        self.preview_btn = ttk.Button(self, text="Preview", width=40, command= lambda: controller.show_frame(Preview))
        self.preview_btn.pack(pady=5)

        self.back_btn = ttk.Button(self, text="Back", width=40, command=lambda: controller.show_frame(Choice))
        self.back_btn.pack(pady=5)

    def button_state(self):
        self.camera_btn.state(["!disabled"])

    def show_camera(self):
        self.device = self.option_var.get()

        self.cap = cv2.VideoCapture(self.devices_list[self.device], cv2.CAP_DSHOW)

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
                    
                    cv2.putText(self.img, str(self.TIMER), (0, 25), self.font, 1, (255, 255, 0), 1, cv2.LINE_AA)
                    cv2.imshow("Camera", self.img)
                    cv2.waitKey(1)

                else:
                    _, self.img = self.cap.read()

                    if self.TIMER == 0:
                        cv2.putText(self.img, "Start!", (0, 25), self.font, 1, (255, 255, 0), 1, cv2.LINE_AA)
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

                                cv2.putText(self.img, str(self.TIMER), (0, 25), self.font, 1, (255, 255, 0), 1, cv2.LINE_AA)
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

                            if self.index == 22: #Heian Shodan 22
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
        self.image_txt = tk.StringVar(self)
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

        self.process_btn = ttk.Button(self, text="Process", width=40, command= lambda: self.process(controller))
        self.process_btn.pack(pady=5)
        self.process_btn.state(["disabled"])

        self.back_btn = ttk.Button(self, text="Back", width=40, command=lambda: self.back(controller))
        self.back_btn.pack(pady=5)

    def move(self, delta):
        self.current += delta

        self.image_txt.set(self.text_list[self.current])
        self.image = Image.open(os.path.join('./temp', self.image_list[self.current])).resize((720, 480))
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

        if self.image_list:
            self.image_txt.set(self.text_list[0])
            self.image = Image.open(os.path.join('./temp', self.image_list[0])).resize((720, 480))
            self.tkimage = ImageTk.PhotoImage(self.image)
            self.image_lbl["image"] = self.tkimage

            self.get_image_btn.state(["disabled"])
        else:
            self.image_txt.set("No Images Found")

        if len(self.image_list) > 1:
            self.next_btn.state(["!disabled"])
            self.process_btn.state(["!disabled"])

    def process(self, controller):
        self.time = datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
        self.new_path = os.path.join('./pose', self.time)
        
        if not os.path.exists(self.new_path):
            os.makedirs(self.new_path)
            for items in os.listdir("./temp"):
                os.rename(os.path.join('./temp', items), os.path.join(self.new_path, items))

        person_detector(self.new_path)

        get_coordinates(os.path.join('./cropped_pose', self.time))

        self.image_list = []
        self.text_list = []
        self.image_txt.set("Press Get Image Button.")
        self.tkimage = ""

        self.current = 0

        self.image_lbl["image"] = self.tkimage

        self.get_image_btn.state(["!disabled"])
        self.next_btn.state(["disabled"])
        self.prev_btn.state(["disabled"])
        self.process_btn.state(["disabled"])

        controller.show_frame(History)

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
        self.process_btn.state(["disabled"])

        controller.show_frame(Train)


class History(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.OPTIONS = [dir for dir in os.listdir('./coordinates') if dir not in ['reference', 'reference_front']]
        self.REFERENCE_OPTIONS = ['reference', 'reference_front']

        self.option_var = tk.StringVar(self)
        self.reference_option_var = tk.StringVar(self)

        self.option_state = False
        self.reference_option_state = False

        self.info_txt = "Select an option to review.\nSelect a reference point.\nRED is Reference, BLUE is User."
        
        self.title_lbl = ttk.Label(self, text="History", font=("Times new roman", 30, "bold"))
        self.title_lbl.pack(pady=5)

        self.info_lbl = ttk.Label(self, text=self.info_txt, font=("Times new roman", 12, "normal"))
        self.info_lbl.pack(pady=5)

        self.refresh_btn = ttk.Button(self, text="Refresh", width=40, command=lambda: self.refresh())
        self.refresh_btn.pack(pady=5)

        self.option_menu = ttk.OptionMenu(self, self.option_var, "Select one...", *self.OPTIONS, command= lambda _: self.button_state())
        self.option_menu.config(width=38)
        self.option_menu.pack(pady=5)

        self.reference_option_menu = ttk.OptionMenu(self, self.reference_option_var, "Select one...", *self.REFERENCE_OPTIONS, command= lambda _: self.reference_button_state())
        self.reference_option_menu.config(width=38)
        self.reference_option_menu.pack(pady=5)

        self.start_btn = ttk.Button(self, text="Start", width=40, command=lambda: self.process())
        self.start_btn.state(["disabled"])
        self.start_btn.pack(pady=5)

        self.back_btn = ttk.Button(self, text="Back", width=40, command=lambda: self.back(controller))
        self.back_btn.pack(pady=5)

    def button_state(self):
        self.option_state = True

        if (self.option_state == True and self.reference_option_state == True):
            self.start_btn.state(["!disabled"])

    def reference_button_state(self):
        self.reference_option_state = True

        if (self.option_state == True and self.reference_option_state == True):
            self.start_btn.state(["!disabled"])

    def refresh(self):
        self.menu = self.option_menu['menu']
        self.menu.delete(0, "end")
        self.OPTIONS = [dir for dir in os.listdir('./coordinates') if dir not in ['reference', 'reference_front']]
        for string in self.OPTIONS:
            self.menu.add_command(label=string, command= lambda value=string: self.set_options(value))

    def set_options(self, value):
        self.option_var.set(value)
        self.button_state()

    def back(self, controller):
        controller.show_frame(Menu)
        self.start_btn.state(["disabled"])

    def process(self):
        pose = self.option_var.get()
        reference = self.reference_option_var.get()
        self.pop_up(pose, reference)

    def pop_up(self, pose, reference):
        self.win = tk.Toplevel()
        self.win.wm_title(pose)

        self.HEIAN_SHODAN = [
            "Hidari Gedan Barai", "Migi Chudan Oi Zuki", "Migi Gedan Barai", "Migi Tetsui Uchi", "Hidari Chudan Oi Zuki", 
            "Hidari Gedan Barai", "Miki Jodan Age Uke", "Hidari Age Uke Jodan", "Migi Jodan Age Uke", "Hidari Gedan Barai",
            "Migi Chudan Oi Zuki", "Migi Gedan Barai", "Hidari Chudan Oi Zuki", "Hidari Gedan Barai", "Migi Chudan Oi Zuki",
            "Hidari Chudan Oi Zuki", "Migi Chudan Oi Zuki", "Hidari Chudan Shuto Uke", "Migi Chudan Shuto Uke", "Migi Chudan Shuto Uke",
            "Hidari Chudan Shuto Uke", "Yame Hachiji Dachi"
        ]

        self.current = 0

        self.title_txt = tk.StringVar(self)
        self.title_txt.set(f"{self.HEIAN_SHODAN[self.current]}")

        self.cosine_similarity, self.weighted_similarity = calculate_similarity(os.path.join('./coordinates', pose), os.path.join('./coordinates', reference), self.current, False)

        self.cosine_txt = tk.StringVar(self)
        self.cosine_txt.set(f"Cosine Similarity: {round(self.cosine_similarity, 2)}")

        self.weighted_txt = tk.StringVar(self)
        self.weighted_txt.set(f"Weighted Similarity: {round(self.weighted_similarity, 2)}")

        self.figure = plot(os.path.join('./coordinates', pose), os.path.join('./coordinates', reference), self.current, True)

        self.title_lbl = ttk.Label(self.win, textvariable=self.title_txt, font=("Times new roman", 30, "bold"))
        self.title_lbl.pack(pady=5)

        self.cosine_lbl = ttk.Label(self.win, textvariable=self.cosine_txt, font=("Times new roman", 15, "bold"))
        self.cosine_lbl.pack(pady=5)
        
        self.weighted_lbl = ttk.Label(self.win, textvariable=self.weighted_txt, font=("Times new roman", 15, "bold"))
        self.weighted_lbl.pack(pady=5)

        self.prev_btn = ttk.Button(self.win, text="Previous", width=20, command= lambda: self.move(-1, pose, reference))
        self.prev_btn.pack(padx=5, pady=5, side='left', ipady=20)
        self.prev_btn.state(["disabled"])

        self.next_btn = ttk.Button(self.win, text="Next", width=20, command= lambda: self.move(1, pose, reference))
        self.next_btn.pack(padx=5, pady=5, side='right', ipady=20)
        self.next_btn.state(["!disabled"])

        self.plot = FigureCanvasTkAgg(self.figure, self.win)
        self.plot.get_tk_widget().pack(pady=5)

    def move(self, delta, pose, reference):
        plt.close()
        if self.current <= 21:
            self.current += delta

        if self.current == (len(self.HEIAN_SHODAN) - 1):
            self.next_btn.state(["disabled"])
            self.prev_btn.state(["!disabled"])
        elif self.current == 0:
            self.next_btn.state(["!disabled"])
            self.prev_btn.state(["disabled"])
        else:
            self.next_btn.state(["!disabled"])
            self.prev_btn.state(["!disabled"])

        self.title_txt.set(f"{self.HEIAN_SHODAN[self.current]}")

        self.cosine_similarity, self.weighted_similarity = calculate_similarity(os.path.join('./coordinates', pose), os.path.join('./coordinates', reference), self.current, False)
        self.cosine_txt.set(f"Cosine Similarity: {round(self.cosine_similarity, 2)}")
        self.weighted_txt.set(f"Weighted Similarity: {round(self.weighted_similarity, 2)}")

        self.figure = plot(os.path.join('./coordinates', pose), os.path.join('./coordinates', reference), self.current, True)
        self.plot.get_tk_widget().destroy()
        self.plot = FigureCanvasTkAgg(self.figure, self.win)
        self.plot.get_tk_widget().pack(pady=5)


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
