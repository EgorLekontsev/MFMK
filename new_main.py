import tkinter as tk
from tkinter import PhotoImage, Canvas
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageTk
from platform import system
from re import sub
from subprocess import check_output
from socket import socket, AF_INET, SOCK_DGRAM
import wmi
import psutil

'''def check_os():
    os = system()
    if os == "Windows":
        print("This is Windows operating system.")
    elif os == "Linux":
        print("This is Linux operating system.")
    else:
        print("Unknown operating system.")
check_os()'''

'''
Keypad - кейпад
Frame1 - Главный экран - 1 2 3 4 фреймы индикаторов
Frame2 - Планировщик уставок
Frame3 - Мониторинг(Тренды онлайн)
Frame4 - Мониторинг(Тренды истории)
Frame5 - Мониторинг(Наработки насосов)
Frame6 - Журнал(Текущие события)
Frame7 - Журнал(Журнал история)
Frame8 - Журнал(Журнал изменений)
Frame9 - Настройки станции(Параметры двигателей)
Frame10 - Настройки станции(Настройки датчиков)
Frame11 - Настройки станции(Параметры насосов общ.)
Frame12 - Настройки станции(вкл. доп. насосов)
Frame13 - Настройки станции(откл. доп. насосов)
Frame14 - Настройки станции(Опции)
Frame15 - Настройки станции(Аварийные режимы)
Frame16 - Инженерное меню(Настройки ПИД-рег.)
Frame17 - Инженерное меню(PLC)
Frame18 - Инженерное меню(Бэкап)
Frame19 - Настройки панели
Frame20 - Контакты
'''
class App(tk.Tk): # Основной класс с характеристиками окна
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("Главный экран")  # Изначальное название окна

        self.geometry("800x480")
        self.resizable(width=False, height=False)
        self.configure(background='black')

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        '''
        При добавлении фрейма, обновить кортеж снизу!!!
        Так же не забыть создать класс для нового фрейма, по аналогии!!!
        '''
        for F in (Frame1_1, Frame1_2, Frame1_3, Frame1_4, Frame2, Frame3, Frame4, Frame5, Frame6, Frame7, Frame8, Frame9, Frame10, Frame11, Frame12, Frame13, Frame14, Frame15, Frame16, Frame17, Frame18, Frame19, Frame20):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Frame1_1")
        self.update_clock()

    def show_frame(self, page_name): # Смена фреймов
        frame = self.frames[page_name]
        frame.tkraise()

        match page_name: # Смена названий окна
            case "Frame1_1":
                self.title("Главный экран")
            case "Frame1_2":
                self.title("Главный экран")
            case "Frame1_3":
                self.title("Главный экран")
            case "Frame1_4":
                self.title("Главный экран")
            case "Frame2":
                self.title("Планировщик уставок")
            case "Frame3":
                self.title("Мониторинг(Тренды онлайн)")
            case "Frame4":
                self.title("Мониторинг(Тренды истории)")
            case "Frame5":
                self.title("Мониторинг(Наработки насосов)")
            case "Frame6":
                self.title("Журнал(Текущие события)")
            case "Frame7":
                self.title("Журнал(Журнал история)")
            case "Frame8":
                self.title("Журнал(Журнал изменений)")
            case "Frame9":
                self.title("Настройки станции(Параметры двигателей)")
            case "Frame10":
                self.title("Настройки станции(Настройки датчиков)")
            case "Frame11":
                self.title("Настройки станции(Параметры насосов общ.)")
            case "Frame12":
                self.title("Настройки станции(вкл. доп. насосов)")
            case "Frame13":
                self.title("Настройки станции(откл. доп. насосов)")
            case "Frame14":
                self.title("Настройки станции(Опции)")
            case "Frame15":
                self.title("Настройки станции(Аварийные режимы)")
            case "Frame16":
                self.title("Инженерное меню(Настройки ПИД-рег.)")
            case "Frame17":
                self.title("Инженерное меню(PLC)")
            case "Frame18":
                self.title("Инженерное меню(Бэкап)")
            case "Frame19":
                self.title("Настройки панели")
            case "Frame20":
                self.title("Контакты")
            case _:
                self.title("ERROR 404")



    def update_clock(self): # Часики
        current_time = datetime.now().strftime('%d/%m/%y %H:%M')
        for frame_name in self.frames:
            self.frames[frame_name].update_clock(current_time)
        self.after(1000, self.update_clock) # Тик-так

class Keypad(tk.Toplevel):
    def __init__(self, NameFrame, master=None, ):
        super().__init__(master)
        self.title("Главный экран")
        self.geometry("300x400")
        self.resizable(width=False, height=False)
        self.canvas = tk.Canvas(
            self,
            height=400,
            width=300,
            bd=0,
            highlightthickness=0,
            relief="ridge")
        self.canvas.place(x=0, y=0)

        self.password = "123"
        self.enter_password = ""
        self.NameFrame = NameFrame

        self.entry_label = tk.Label(self.canvas, text="", fg='white', bg='black', font=('Roboto Bold', 16), width=20, anchor='e')
        self.entry_label.place(x=35, y=65)
        self.interfacekp_img = PhotoImage(file=r"images\Keypad\InterfaceKP.png")
        self.interfacekp = self.canvas.create_image(150, 200, image=self.interfacekp_img)
        self.comma_img = PhotoImage(file=r"images\Keypad\Comma.png")
        self.comma_button = self.canvas.create_image(45, 355, image=self.comma_img)
        self.zero_img = PhotoImage(file=r"images\Keypad\0.png")
        self.zero_button = self.canvas.create_image(115, 355, image=self.zero_img)
        self.canvas.tag_bind(self.zero_button, "<Button-1>", self.zero_func)
        self.one_img = PhotoImage(file=r"images\Keypad\1.png")
        self.one_button = self.canvas.create_image(45, 285, image=self.one_img)
        self.canvas.tag_bind(self.one_button, "<Button-1>", self.one_func)
        self.two_img = PhotoImage(file=r"images\Keypad\2.png")
        self.two_button = self.canvas.create_image(115, 285, image=self.two_img)
        self.canvas.tag_bind(self.two_button, "<Button-1>", self.two_func)
        self.three_img = PhotoImage(file=r"images\Keypad\3.png")
        self.three_button = self.canvas.create_image(185, 285, image=self.three_img)
        self.canvas.tag_bind(self.three_button, "<Button-1>", self.three_func)
        self.four_img = PhotoImage(file=r"images\Keypad\4.png")
        self.four_button = self.canvas.create_image(45, 215, image=self.four_img)
        self.canvas.tag_bind(self.four_button, "<Button-1>", self.four_func)
        self.five_img = PhotoImage(file=r"images\Keypad\5.png")
        self.five_button = self.canvas.create_image(115, 215, image=self.five_img)
        self.canvas.tag_bind(self.five_button, "<Button-1>", self.five_func)
        self.six_img = PhotoImage(file=r"images\Keypad\6.png")
        self.six_button = self.canvas.create_image(185, 215, image=self.six_img)
        self.canvas.tag_bind(self.six_button, "<Button-1>", self.six_func)
        self.seven_img = PhotoImage(file=r"images\Keypad\7.png")
        self.seven_button = self.canvas.create_image(45, 145, image=self.seven_img)
        self.canvas.tag_bind(self.seven_button, "<Button-1>", self.seven_func)
        self.eight_img = PhotoImage(file=r"images\Keypad\8.png")
        self.eight_button = self.canvas.create_image(115, 145, image=self.eight_img)
        self.canvas.tag_bind(self.eight_button, "<Button-1>", self.eight_func)
        self.nine_img = PhotoImage(file=r"images\Keypad\9.png")
        self.nine_button = self.canvas.create_image(185, 145, image=self.nine_img)
        self.canvas.tag_bind(self.nine_button, "<Button-1>", self.nine_func)
        self.clear_all_img = PhotoImage(file=r"images\Keypad\C.png")
        self.clear_all_button = self.canvas.create_image(255, 145, image=self.clear_all_img)
        self.canvas.tag_bind(self.clear_all_button, "<Button-1>", self.clear_all_button_func)
        self.clear_img = PhotoImage(file=r"images\Keypad\Arrow.png")
        self.clear_button = self.canvas.create_image(255, 215, image=self.clear_img)
        self.canvas.tag_bind(self.clear_button, "<Button-1>", self.clear_button_func)
        self.esc_img = PhotoImage(file=r"images\Keypad\Esc.png")
        self.esc_button = self.canvas.create_image(255, 285, image=self.esc_img)
        self.canvas.tag_bind(self.esc_button, "<Button-1>", self.escape_button_func)
        self.enter_img = PhotoImage(file=r"images\Keypad\Enter.png")
        self.enter_button = self.canvas.create_image(220, 355, image=self.enter_img)
        self.canvas.tag_bind(self.enter_button, "<Button-1>", self.enter_button_func)




    ''' ЗАПЯТАЯ 
    def cammo_func(self, event):
        self.clock_label.config(text=self.clock_label.cget('text')+",")
    '''
    def zero_func(self, event):
        if len(self.enter_password) != 8:
            self.enter_password = self.enter_password + "0"
            self.entry_label.config(text=self.entry_label.cget('text')+"*")
    def one_func(self, event):
        if len(self.enter_password) != 8:
            self.enter_password = self.enter_password + "1"
            self.entry_label.config(text=self.entry_label.cget('text')+"*")
    def two_func(self, event):
        if len(self.enter_password) != 8:
            self.enter_password = self.enter_password + "2"
            self.entry_label.config(text=self.entry_label.cget('text')+"*")
    def three_func(self, event):
        if len(self.enter_password) != 8:
            self.enter_password = self.enter_password + "3"
            self.entry_label.config(text=self.entry_label.cget('text')+"*")
    def four_func(self, event):
        if len(self.enter_password) != 8:
            self.enter_password = self.enter_password + "4"
            self.entry_label.config(text=self.entry_label.cget('text')+"*")
    def five_func(self, event):
        if len(self.enter_password) != 8:
            self.enter_password = self.enter_password + "5"
            self.entry_label.config(text=self.entry_label.cget('text')+"*")
    def six_func(self, event):
        if len(self.enter_password) != 8:
            self.enter_password = self.enter_password + "6"
            self.entry_label.config(text=self.entry_label.cget('text')+"*")
    def seven_func(self, event):
        if len(self.enter_password) != 8:
            self.enter_password = self.enter_password + "7"
            self.entry_label.config(text=self.entry_label.cget('text')+"*")
    def eight_func(self, event):
        if len(self.enter_password) != 8:
            self.enter_password = self.enter_password + "8"
            self.entry_label.config(text=self.entry_label.cget('text')+"*")
    def nine_func(self, event):
        if len(self.enter_password) != 8:
            self.enter_password = self.enter_password + "9"
            self.entry_label.config(text=self.entry_label.cget('text')+"*")
    def clear_all_button_func(self, event):
        self.enter_password = ""
        self.entry_label.config(text="")
    def clear_button_func(self, event):
        past_text = self.entry_label.cget('text')
        new_text = past_text[:-1]
        self.enter_password = self.enter_password[:-1]
        self.entry_label.config(text=new_text)
    def enter_button_func(self, event):
        if self.enter_password == self.password:
            self.enter_password = ""
            self.entry_label.config(text="")
            print("Успешный вход!")
            self.destroy()
        else:
            print(self.enter_password)
            print("Неудачная попытка!")

    def escape_button_func(self, event):
        self.destroy()



class Frame1_1(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.canvas = Canvas(
            self,
            bg="black",
            height=480,
            width=800,
            bd=0,
            highlightthickness=0,
            relief="ridge")
        self.canvas.place(x=0, y=0)
        button = tk.Button(self, text="Настройки", fg='white', bg='black', font=('Roboto Bold', 14), activebackground="black", activeforeground="white",
                           relief="groove", command=lambda: controller.show_frame("Frame2"))
        button.place(x=0, y=0, width=135, height=37)
        self.indicators_img = PhotoImage(file=r"images\MainScreen\indicator_0.png")
        self.indicators_button = self.canvas.create_image(195, 20, image=self.indicators_img)
        self.canvas.tag_bind(self.indicators_button, "<Button-1>", lambda event: controller.show_frame("Frame1_2"))
        self.background_img = PhotoImage(file=r"images\MainScreen\stop_icon.png")
        self.canvas.create_image(655, 20, image=self.background_img)
        self.clock_label = tk.Label(self.canvas, text="", fg='white', bg='black', font=('Roboto Bold', 12))
        self.clock_label.place(x=680, y=5)
        self.right_img = PhotoImage(file=r"images\MainScreen\red.png")
        self.right_button = self.canvas.create_image(770, 180, image=self.right_img)
        self.canvas.tag_bind(self.right_button, "<Button-1>", self.update_right)
        self.Pumps_img = PhotoImage(file=r"images\MainScreen\SystemPump.png")
        self.Pumps = self.canvas.create_image(380,400, image=self.Pumps_img)
        self.Info_img = PhotoImage(file=r"images\MainScreen\Info.png")
        self.Info = self.canvas.create_image(90, 400, image=self.Info_img)

    def update_right(self, event):
        if self.right_img.cget("file") == r"images\MainScreen\red.png":
            self.right_img = PhotoImage(file=r"images\MainScreen\blue.png")
        elif self.right_img.cget("file") == r"images\MainScreen\blue.png":
            self.right_img = PhotoImage(file=r"images\MainScreen\green.png")
        elif self.right_img.cget("file") == r"images\MainScreen\green.png":
            self.right_img = PhotoImage(file=r"images\MainScreen\pink.png")
        elif self.right_img.cget("file") == r"images\MainScreen\pink.png":
            self.right_img = PhotoImage(file=r"images\MainScreen\orange.png")
        elif self.right_img.cget("file") == r"images\MainScreen\orange.png":
            self.right_img = PhotoImage(file=r"images\MainScreen\yellow.png")
        elif self.right_img.cget("file") == r"images\MainScreen\yellow.png":
            self.right_img = PhotoImage(file=r"images\MainScreen\red.png")
        self.right_button = self.canvas.create_image(770, 180, image=self.right_img)
        self.canvas.tag_bind(self.right_button, "<Button-1>", self.update_right)
    def update_clock(self, current_time):
        self.clock_label.config(text=current_time)

class Frame1_2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.canvas = Canvas(
            self,
            bg="black",
            height=480,
            width=800,
            bd=0,
            highlightthickness=0,
            relief="ridge")
        self.canvas.place(x=0, y=0)
        button = tk.Button(self, text="Настройки", fg='white', bg='black', font=('Roboto Bold', 14), activebackground="black", activeforeground="white",
                           relief="groove", command=lambda: controller.show_frame("Frame2"))
        button.place(x=0, y=0, width=135, height=37)
        self.indicators_img = PhotoImage(file=r"images\MainScreen\indicator_1.png")
        self.indicators_button = self.canvas.create_image(195, 20, image=self.indicators_img)
        self.canvas.tag_bind(self.indicators_button, "<Button-1>", lambda event: controller.show_frame("Frame1_3"))
        self.background_img = PhotoImage(file=r"images\MainScreen\stop_icon.png")
        background = self.canvas.create_image(655, 20, image=self.background_img)
        self.clock_label = tk.Label(self.canvas, text="", fg='white', bg='black', font=('Roboto Bold', 12))
        self.clock_label.place(x=680, y=5)
        self.Pumps_img = PhotoImage(file=r"images\MainScreen\SystemPump.png")
        self.Pumps = self.canvas.create_image(380, 400, image=self.Pumps_img)
        self.Info_img = PhotoImage(file=r"images\MainScreen\Info.png")
        self.Info = self.canvas.create_image(90, 400, image=self.Info_img)

    def update_clock(self, current_time):
        self.clock_label.config(text=current_time)

class Frame1_3(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.canvas = Canvas(
            self,
            bg="black",
            height=480,
            width=800,
            bd=0,
            highlightthickness=0,
            relief="ridge")
        self.canvas.place(x=0, y=0)
        button = tk.Button(self, text="Настройки", fg='white', bg='black', font=('Roboto Bold', 14), activebackground="black", activeforeground="white",
                           relief="groove", command=lambda: controller.show_frame("Frame2"))
        button.place(x=0, y=0, width=135, height=37)
        self.indicators_img = PhotoImage(file=r"images\MainScreen\indicator_1.png")
        self.indicators_button = self.canvas.create_image(195, 20, image=self.indicators_img)
        self.canvas.tag_bind(self.indicators_button, "<Button-1>", lambda event: controller.show_frame("Frame1_4"))
        self.background_img = PhotoImage(file=r"images\MainScreen\stop_icon.png")
        self.canvas.create_image(655, 20, image=self.background_img)
        self.clock_label = tk.Label(self.canvas, text="", fg='white', bg='black', font=('Roboto Bold', 12))
        self.clock_label.place(x=680, y=5)
        self.Pumps_img = PhotoImage(file=r"images\MainScreen\SystemPump.png")
        self.Pumps = self.canvas.create_image(380, 400, image=self.Pumps_img)
        self.Info_img = PhotoImage(file=r"images\MainScreen\Info.png")
        self.Info = self.canvas.create_image(90, 400, image=self.Info_img)

        self.button1_img = PhotoImage(file=r"images\MainScreen\ON.png")
        self.button1_button = self.canvas.create_image(235, 200, image=self.button1_img)
        self.canvas.tag_bind(self.button1_button, "<Button-1>", self.update_button1)
        self.button2_img = PhotoImage(file=r"images\MainScreen\ON.png")
        self.button2_button = self.canvas.create_image(330, 200, image=self.button2_img)
        self.canvas.tag_bind(self.button2_button, "<Button-1>", self.update_button2)
        self.button3_img = PhotoImage(file=r"images\MainScreen\ON.png")
        self.button3_button = self.canvas.create_image(425, 200, image=self.button3_img)
        self.canvas.tag_bind(self.button3_button, "<Button-1>", self.update_button3)
        self.button4_img = PhotoImage(file=r"images\MainScreen\ON.png")
        self.button4_button = self.canvas.create_image(520, 200, image=self.button4_img)
        self.canvas.tag_bind(self.button4_button, "<Button-1>", self.update_button4)
        self.button5_img = PhotoImage(file=r"images\MainScreen\ON.png")
        self.button5_button = self.canvas.create_image(615, 200, image=self.button5_img)
        self.canvas.tag_bind(self.button5_button, "<Button-1>", self.update_button5)
        self.button6_img = PhotoImage(file=r"images\MainScreen\ON.png")
        self.button6_button = self.canvas.create_image(710, 200, image=self.button6_img)
        self.canvas.tag_bind(self.button6_button, "<Button-1>", self.update_button6)
    def update_button1(self, event):
        if self.button1_img.cget("file") == r"images\MainScreen\OFF.png":
            self.button1_img = PhotoImage(file=r"images\MainScreen\ON.png")
        elif self.button1_img.cget("file") == r"images\MainScreen\ON.png":
            self.button1_img = PhotoImage(file=r"images\MainScreen\OFF.png")
        self.button1_button = self.canvas.create_image(235, 200, image=self.button1_img)
        self.canvas.tag_bind(self.button1_button, "<Button-1>", self.update_button1)

    def update_button2(self, event):
        if self.button2_img.cget("file") == r"images\MainScreen\OFF.png":
            self.button2_img = PhotoImage(file=r"images\MainScreen\ON.png")
        elif self.button2_img.cget("file") == r"images\MainScreen\ON.png":
            self.button2_img = PhotoImage(file=r"images\MainScreen\OFF.png")
        self.button2_button = self.canvas.create_image(330, 200, image=self.button2_img)
        self.canvas.tag_bind(self.button2_button, "<Button-1>", self.update_button2)

    def update_button3(self, event):
        if self.button3_img.cget("file") == r"images\MainScreen\OFF.png":
            self.button3_img = PhotoImage(file=r"images\MainScreen\ON.png")
        elif self.button3_img.cget("file") == r"images\MainScreen\ON.png":
            self.button3_img = PhotoImage(file=r"images\MainScreen\OFF.png")
        self.button3_button = self.canvas.create_image(425, 200, image=self.button3_img)
        self.canvas.tag_bind(self.button3_button, "<Button-1>", self.update_button3)
    def update_button4(self, event):
        if self.button4_img.cget("file") == r"images\MainScreen\OFF.png":
            self.button4_img = PhotoImage(file=r"images\MainScreen\ON.png")
        elif self.button4_img.cget("file") == r"images\MainScreen\ON.png":
            self.button4_img = PhotoImage(file=r"images\MainScreen\OFF.png")
        self.button4_button = self.canvas.create_image(520, 200, image=self.button4_img)
        self.canvas.tag_bind(self.button4_button, "<Button-1>", self.update_button4)

    def update_button5(self, event):
        if self.button5_img.cget("file") == r"images\MainScreen\OFF.png":
            self.button5_img = PhotoImage(file=r"images\MainScreen\ON.png")
        elif self.button5_img.cget("file") == r"images\MainScreen\ON.png":
            self.button5_img = PhotoImage(file=r"images\MainScreen\OFF.png")
        self.button5_button = self.canvas.create_image(615, 200, image=self.button5_img)
        self.canvas.tag_bind(self.button5_button, "<Button-1>", self.update_button5)

    def update_button6(self, event):
        if self.button6_img.cget("file") == r"images\MainScreen\OFF.png":
            self.button6_img = PhotoImage(file=r"images\MainScreen\ON.png")
        elif self.button6_img.cget("file") == r"images\MainScreen\ON.png":
            self.button6_img = PhotoImage(file=r"images\MainScreen\OFF.png")
        self.button6_button = self.canvas.create_image(710, 200, image=self.button6_img)
        self.canvas.tag_bind(self.button6_button, "<Button-1>", self.update_button6)


    def update_clock(self, current_time):
        self.clock_label.config(text=current_time)

class Frame1_4(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.canvas = Canvas(
            self,
            bg="black",
            height=480,
            width=800,
            bd=0,
            highlightthickness=0,
            relief="ridge")
        self.canvas.place(x=0, y=0)
        button = tk.Button(self, text="Настройки", fg='white', bg='black', font=('Roboto Bold', 14), activebackground="black", activeforeground="white",
                           relief="groove", command=lambda: controller.show_frame("Frame2"))
        button.place(x=0, y=0, width=135, height=37)
        self.indicators_img = PhotoImage(file=r"images\MainScreen\indicator_2.png")
        self.indicators_button = self.canvas.create_image(195, 20, image=self.indicators_img)
        self.canvas.tag_bind(self.indicators_button, "<Button-1>", lambda event: controller.show_frame("Frame1_1"))
        self.background_img = PhotoImage(file=r"images\MainScreen\stop_icon.png")
        background = self.canvas.create_image(655, 20, image=self.background_img)
        self.clock_label = tk.Label(self.canvas, text="", fg='white', bg='black', font=('Roboto Bold', 12))
        self.clock_label.place(x=680, y=5)
        self.Pumps_img = PhotoImage(file=r"images\MainScreen\SystemPump.png")
        self.Pumps = self.canvas.create_image(380, 400, image=self.Pumps_img)
        self.Info_img = PhotoImage(file=r"images\MainScreen\Info.png")
        self.Info = self.canvas.create_image(90, 400, image=self.Info_img)

    def update_clock(self, current_time):
        self.clock_label.config(text=current_time)

class Frame2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='black')
        self.canvas = Canvas(
            self,
            bg="black",
            height=480,
            width=800,
            bd=0,
            highlightthickness=0,
            relief="ridge")
        self.canvas.place(x=0, y=0)

        button_day1 = tk.Button(self, text='ПН', font=('Roboto Bold', 12), bg='#0F91DA', fg='white', relief="groove", activebackground="#0F91DA", activeforeground="white")
        button_day1.place(x=510, y=107, width=35, height=35)
        button_day2 = tk.Button(self, text='ВТ', font=('Roboto Bold', 12), bg='#0F91DA', fg='white', relief="groove",
                                activebackground="#0F91DA", activeforeground="white")
        button_day2.place(x=550, y=107, width=35, height=35)
        button_day3 = tk.Button(self, text='СР', font=('Roboto Bold', 12), bg='#0F91DA', fg='white', relief="groove",
                                activebackground="#0F91DA", activeforeground="white")
        button_day3.place(x=590, y=107, width=35, height=35)
        button_day4 = tk.Button(self, text='ЧТ', font=('Roboto Bold', 12), bg='#0F91DA', fg='white', relief="groove",
                                activebackground="#0F91DA", activeforeground="white")
        button_day4.place(x=630, y=107, width=35, height=35)
        button_day5 = tk.Button(self, text='ПТ', font=('Roboto Bold', 12), bg='#0F91DA', fg='white', relief="groove",
                                activebackground="#0F91DA", activeforeground="white")
        button_day5.place(x=670, y=107, width=35, height=35)
        button_day6 = tk.Button(self, text='СБ', font=('Roboto Bold', 12), bg='#871212', fg='white', relief="groove",
                                activebackground="#871212", activeforeground="white")
        button_day6.place(x=710, y=107, width=35, height=35)
        button_day7 = tk.Button(self, text='ВС', font=('Roboto Bold', 12), bg='#871212', fg='white', relief="groove",
                                activebackground="#871212", activeforeground="white")
        button_day7.place(x=750, y=107, width=35, height=35)

        self.img_share = PhotoImage(file=r"new_images\share.png")
        self.img_user = PhotoImage(file=r"new_images\user.png")
        self.img_cal = PhotoImage(file=r"new_images\calendar.png")
        self.img_day = PhotoImage(file=r"new_images\day.png")
        self.img_eye = PhotoImage(file=r"new_images\eye.png")
        self.img_shield = PhotoImage(file=r"new_images\shield.png")
        self.img_field_l = PhotoImage(file=r"new_images\field_long.png")
        self.img_field_s = PhotoImage(file=r"new_images\field_short.png")

        self.canvas.create_image(231, 30, image=self.img_share)
        self.canvas.create_image(231, 78, image=self.img_user)
        self.canvas.create_image(231, 226, image=self.img_day)
        self.canvas.create_image(231, 271, image=self.img_day)
        self.canvas.create_image(231, 316, image=self.img_day)
        self.canvas.create_image(231, 361, image=self.img_day)
        self.canvas.create_image(594, 77, image=self.img_shield)
        self.canvas.create_image(491, 122, image=self.img_shield)
        self.canvas.create_image(354, 227, image=self.img_shield)
        self.canvas.create_image(354, 273, image=self.img_shield)
        self.canvas.create_image(354, 318, image=self.img_shield)
        self.canvas.create_image(354, 363, image=self.img_shield)

        self.canvas.create_line(210, 50, 790, 50, fill="gray", width=1)
        self.canvas.create_line(210, 100, 790, 100, fill="gray", width=1)
        self.canvas.create_line(210, 150, 790, 150, fill="gray", width=1)
        self.canvas.create_line(210, 400, 790, 400, fill="gray", width=1)

        self.canvas.create_image(231, 424, image=self.img_eye)
        self.canvas.create_image(231, 454, image=self.img_eye)
        self.canvas.create_image(231, 125, image=self.img_cal)

        self.label1 = tk.Label(self.canvas, text="Источник уставки", fg='white', bg='black', font=('Roboto Bold', 12))
        self.label1.place(x=260, y=19)
        self.label2 = tk.Label(self.canvas, text="Уставка пользователя", fg='white', bg='black', font=('Roboto Bold', 12))
        self.label2.place(x=260, y=67)
        self.label3 = tk.Label(self.canvas, text="Настройка дней недели", fg='white', bg='black', font=('Roboto Bold', 12))
        self.label3.place(x=260, y=116)
        self.label4 = tk.Label(self.canvas, text="Планировщик", fg='gray', bg='black',
                               font=('Roboto Bold', 10))
        self.label4.place(x=208, y=155)
        self.label5 = tk.Label(self.canvas, text="Время перехода:", fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label5.place(x=231, y=179)
        self.label6 = tk.Label(self.canvas, text="Будни", fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label6.place(x=372, y=179)
        self.label7 = tk.Label(self.canvas, text="Выходные", fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label7.place(x=474, y=179)
        self.label8 = tk.Label(self.canvas, text="Уставка:", fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label8.place(x=572, y=179)
        self.label9 = tk.Label(self.canvas, text="Будни", fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label9.place(x=644, y=179)
        self.label10 = tk.Label(self.canvas, text="Выходные", fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label10.place(x=707, y=179)
        self.label11 = tk.Label(self.canvas, text="Утро", fg='white', bg='black',
                                font=('Roboto Bold', 12))
        self.label11.place(x=260, y=217)
        self.label12 = tk.Label(self.canvas, text="День", fg='white', bg='black',
                                font=('Roboto Bold', 12))
        self.label12.place(x=260, y=261)
        self.label13 = tk.Label(self.canvas, text="Вечер", fg='white', bg='black',
                                font=('Roboto Bold', 12))
        self.label13.place(x=260, y=305)
        self.label14 = tk.Label(self.canvas, text="Ночь", fg='white', bg='black',
                                font=('Roboto Bold', 12))
        self.label14.place(x=260, y=349)
        self.label15 = tk.Label(self.canvas, text="Текущий день", fg='white', bg='black',
                                font=('Roboto Bold', 12))
        self.label15.place(x=252, y=414)
        self.label16 = tk.Label(self.canvas, text="Тип уставки", fg='white', bg='black',
                                font=('Roboto Bold', 12))
        self.label16.place(x=252, y=444)
        self.label17 = tk.Label(self.canvas, text="Тип дня", fg='white', bg='black',
                                font=('Roboto Bold', 12))
        self.label17.place(x=553, y=414)
        self.label18 = tk.Label(self.canvas, text="Текущая уставка", fg='white', bg='black',
                                font=('Roboto Bold', 12))
        self.label18.place(x=519, y=444)
        self.label19 = tk.Label(self.canvas, text="Бар", fg='white', bg='black',
                                font=('Roboto Bold', 12))
        self.label19.place(x=744, y=445)

        self.canvas.create_image(423, 226, image=self.img_field_s)
        self.canvas.create_image(423, 274, image=self.img_field_s)
        self.canvas.create_image(423, 316, image=self.img_field_s)
        self.canvas.create_image(423, 361, image=self.img_field_s)
        self.canvas.create_image(528, 226, image=self.img_field_s)
        self.canvas.create_image(528, 274, image=self.img_field_s)
        self.canvas.create_image(528, 316, image=self.img_field_s)
        self.canvas.create_image(528, 361, image=self.img_field_s)


        self.label20 = tk.Label(self.canvas, text=":", fg='white', bg='black',
                                font=('Roboto Bold', 12))
        self.label20.place(x=420, y=215, width=5, height=19)
        self.label21 = tk.Label(self.canvas, text=":", fg='white', bg='black',
                                font=('Roboto Bold', 12))
        self.label21.place(x=420, y=264, width=5, height=19)
        self.label22 = tk.Label(self.canvas, text=":", fg='white', bg='black',
                                font=('Roboto Bold', 12))
        self.label22.place(x=420, y=306, width=5, height=19)
        self.label23 = tk.Label(self.canvas, text=":", fg='white', bg='black',
                                font=('Roboto Bold', 12))
        self.label23.place(x=420, y=349, width=5, height=19)
        self.label24 = tk.Label(self.canvas, text=":", fg='white', bg='black',
                                font=('Roboto Bold', 12))
        self.label24.place(x=525, y=215, width=5, height=19)
        self.label25 = tk.Label(self.canvas, text=":", fg='white', bg='black',
                                font=('Roboto Bold', 12))
        self.label25.place(x=525, y=264, width=5, height=19)
        self.label26 = tk.Label(self.canvas, text=":", fg='white', bg='black',
                                font=('Roboto Bold', 12))
        self.label26.place(x=525, y=306, width=5, height=19)
        self.label27 = tk.Label(self.canvas, text=":", fg='white', bg='black',
                                font=('Roboto Bold', 12))
        self.label27.place(x=525, y=349, width=5, height=19)

        #Кликабельная зона
        self.setpoint = self.canvas.create_image(703, 76, image=self.img_field_l)
        self.canvas.tag_bind(self.setpoint, "<Button-1>", lambda event: print(1))
        self.label28 = tk.Label(self.canvas, text="Бар", fg='white', bg='black',
                                font=('Roboto Bold', 12))
        self.label28.place(x=750, y=66, width=28, height=19)
        self.label28.bind("<Button-1>", lambda event: print(1))
        self.setpoint_value = tk.Label(self.canvas, text="3.00", fg='white', bg='black',
                                font=('Roboto Bold', 12))
        self.setpoint_value.place(x=644, y=67, width=33, height=19)
        self.setpoint_value.bind("<Button-1>", lambda event: print(1))

        self.weekdays_morning_h = tk.Label(self.canvas, text="05", fg='white', bg='black',
                                font=('Roboto Bold', 12))
        self.weekdays_morning_h.place(x=388, y=216, width=19, height=19)
        self.weekdays_afternoon_h = tk.Label(self.canvas, text="10", fg='white', bg='black',
                                           font=('Roboto Bold', 12))
        self.weekdays_afternoon_h.place(x=388, y=265, width=19, height=19)
        self.weekdays_evening_h = tk.Label(self.canvas, text="17", fg='white', bg='black',
                                             font=('Roboto Bold', 12))
        self.weekdays_evening_h.place(x=388, y=307, width=19, height=19)
        self.weekdays_night_h = tk.Label(self.canvas, text="22", fg='white', bg='black',
                                             font=('Roboto Bold', 12))
        self.weekdays_night_h.place(x=388, y=350, width=19, height=19)

        self.weekdays_morning_m = tk.Label(self.canvas, text="00", fg='white', bg='black',
                                           font=('Roboto Bold', 12))
        self.weekdays_morning_m.place(x=440, y=216, width=19, height=19)
        self.weekdays_afternoon_m = tk.Label(self.canvas, text="00", fg='white', bg='black',
                                             font=('Roboto Bold', 12))
        self.weekdays_afternoon_m.place(x=440, y=265, width=19, height=19)
        self.weekdays_evening_m = tk.Label(self.canvas, text="00", fg='white', bg='black',
                                           font=('Roboto Bold', 12))
        self.weekdays_evening_m.place(x=440, y=307, width=19, height=19)
        self.weekdays_night_m = tk.Label(self.canvas, text="00", fg='white', bg='black',
                                         font=('Roboto Bold', 12))
        self.weekdays_night_m.place(x=440, y=350, width=19, height=19)

        self.weekends_morning_h = tk.Label(self.canvas, text="05", fg='white', bg='black',
                                           font=('Roboto Bold', 12))
        self.weekends_morning_h.place(x=492, y=216, width=19, height=19)
        self.weekends_afternoon_h = tk.Label(self.canvas, text="10", fg='white', bg='black',
                                             font=('Roboto Bold', 12))
        self.weekends_afternoon_h.place(x=492, y=265, width=19, height=19)
        self.weekends_evening_h = tk.Label(self.canvas, text="17", fg='white', bg='black',
                                           font=('Roboto Bold', 12))
        self.weekends_evening_h.place(x=492, y=307, width=19, height=19)
        self.weekends_night_h = tk.Label(self.canvas, text="22", fg='white', bg='black',
                                         font=('Roboto Bold', 12))
        self.weekends_night_h.place(x=492, y=350, width=19, height=19)

        self.weekends_morning_m = tk.Label(self.canvas, text="00", fg='white', bg='black',
                                           font=('Roboto Bold', 12))
        self.weekends_morning_m.place(x=544, y=216, width=19, height=19)
        self.weekends_afternoon_m = tk.Label(self.canvas, text="00", fg='white', bg='black',
                                             font=('Roboto Bold', 12))
        self.weekends_afternoon_m.place(x=544, y=265, width=19, height=19)
        self.weekends_evening_m = tk.Label(self.canvas, text="00", fg='white', bg='black',
                                           font=('Roboto Bold', 12))
        self.weekends_evening_m.place(x=544, y=307, width=19, height=19)
        self.weekends_night_m = tk.Label(self.canvas, text="00", fg='white', bg='black',
                                         font=('Roboto Bold', 12))
        self.weekends_night_m.place(x=544, y=350, width=19, height=19)

        self.weekdays_morning_field = self.canvas.create_image(636, 226, image=self.img_field_s)
        self.weekdays_afternoon_field = self.canvas.create_image(636, 274, image=self.img_field_s)
        self.weekdays_evening_field = self.canvas.create_image(636, 316, image=self.img_field_s)
        self.weekdays_night_field = self.canvas.create_image(636, 361, image=self.img_field_s)
        self.weekends_morning_field = self.canvas.create_image(741, 226, image=self.img_field_s)
        self.weekends_afternoon_field = self.canvas.create_image(741, 274, image=self.img_field_s)
        self.weekends_evening_field = self.canvas.create_image(741, 316, image=self.img_field_s)
        self.weekends_night_field = self.canvas.create_image(741, 361, image=self.img_field_s)

        self.weekdays_morning_value = tk.Label(self.canvas, text="3.00", fg='white', bg='black',
                                       font=('Roboto Bold', 12))
        self.weekdays_morning_value.place(x=599, y=216, width=42, height=19)
        self.label29 = tk.Label(self.canvas, text="Бар", fg='white', bg='black',
                                font=('Roboto Bold', 12))
        self.label29.place(x=653, y=215, width=28, height=19)
        self.weekdays_afternoon_value = tk.Label(self.canvas, text="3.00", fg='white', bg='black',
                                               font=('Roboto Bold', 12))
        self.weekdays_afternoon_value.place(x=599, y=265, width=42, height=19)
        self.label30 = tk.Label(self.canvas, text="Бар", fg='white', bg='black',
                                font=('Roboto Bold', 12))
        self.label30.place(x=653, y=264, width=28, height=19)
        self.weekdays_evening_value = tk.Label(self.canvas, text="3.00", fg='white', bg='black',
                                               font=('Roboto Bold', 12))
        self.weekdays_evening_value.place(x=599, y=307, width=42, height=19)
        self.label31 = tk.Label(self.canvas, text="Бар", fg='white', bg='black',
                                font=('Roboto Bold', 12))
        self.label31.place(x=653, y=306, width=28, height=19)
        self.weekdays_night_value = tk.Label(self.canvas, text="3.00", fg='white', bg='black',
                                               font=('Roboto Bold', 12))
        self.weekdays_night_value.place(x=599, y=350, width=42, height=19)
        self.label32 = tk.Label(self.canvas, text="Бар", fg='white', bg='black',
                                font=('Roboto Bold', 12))
        self.label32.place(x=653, y=351, width=28, height=19)


        self.weekends_morning_value = tk.Label(self.canvas, text="3.00", fg='white', bg='black',
                                               font=('Roboto Bold', 12))
        self.weekends_morning_value.place(x=704, y=216, width=42, height=19)
        self.label33 = tk.Label(self.canvas, text="Бар", fg='white', bg='black',
                                font=('Roboto Bold', 12))
        self.label33.place(x=757, y=215, width=28, height=19)
        self.weekends_afternoon_value = tk.Label(self.canvas, text="3.00", fg='white', bg='black',
                                                 font=('Roboto Bold', 12))
        self.weekends_afternoon_value.place(x=704, y=265, width=42, height=19)
        self.label34 = tk.Label(self.canvas, text="Бар", fg='white', bg='black',
                                font=('Roboto Bold', 12))
        self.label34.place(x=757, y=265, width=28, height=19)
        self.weekends_evening_value = tk.Label(self.canvas, text="3.00", fg='white', bg='black',
                                               font=('Roboto Bold', 12))
        self.weekends_evening_value.place(x=704, y=307, width=42, height=19)
        self.label35 = tk.Label(self.canvas, text="Бар", fg='white', bg='black',
                                font=('Roboto Bold', 12))
        self.label35.place(x=757, y=306, width=28, height=19)
        self.weekends_night_value = tk.Label(self.canvas, text="3.00", fg='white', bg='black',
                                             font=('Roboto Bold', 12))
        self.weekends_night_value.place(x=704, y=350, width=42, height=19)
        self.label36 = tk.Label(self.canvas, text="Бар", fg='white', bg='black',
                                font=('Roboto Bold', 12))
        self.label36.place(x=757, y=350, width=28, height=19)
        # Кликабельная зона

        self.day = tk.Label(self.canvas, text="", fg='white', bg='black',
                                font=('Roboto Bold', 12))
        self.current_day = datetime.now()
        self.weekday = self.current_day.weekday() + 1
        match (self.weekday):
            case 1:
                self.day.config(text = "Понедельник")
            case 2:
                self.day.config(text="Вторник")
            case 3:
                self.day.config(text="Среда")
            case 4:
                self.day.config(text="Четверг")
            case 5:
                self.day.config(text="Пятница")
            case 6:
                self.day.config(text="Суббота")
            case 7:
                self.day.config(text="Воскресенье")
        self.day.place(x=375, y=414)

        self.type_setpoint = tk.Label(self.canvas, text="Пользователь", fg='white', bg='black',
                            font=('Roboto Bold', 12))
        self.type_setpoint.place(x=354, y=444)

        self.type_day = tk.Label(self.canvas, text="Не определен", fg='white', bg='black',
                                      font=('Roboto Bold', 12))
        self.type_day.place(x=625, y=414)

        self.current_setpoint = tk.Label(self.canvas, text="", fg='white', bg='black',
                                 font=('Roboto Bold', 12))
        self.current_setpoint.config(text="3.00")
        self.current_setpoint.place(x=675, y=444)


        self.clock_label = tk.Label(self.canvas, text="", fg='white', bg='black', font=('Roboto Bold', 12))
        self.clock_label.place(x=680, y=5)

        self.font = ImageFont.truetype("Roboto-Bold.ttf", 18)
        self.img_screen = Image.open(r"new_images\screen.png")
        self.img_calendar = Image.open(r"new_images\calendar.png")
        self.img_peak = Image.open(r"new_images\peak.png")
        self.img_tablet = Image.open(r"new_images\tablet.png")
        self.img_gear_wheel = Image.open(r"new_images\gear_wheel.png")
        self.img_wrench = Image.open(r"new_images\wrench.png")
        self.img_gear_wheel_bg = Image.open(r"new_images\gear_wheel_bg.png")
        self.img_phone = Image.open(r"new_images\phone.png")
        self.img_right = Image.open(r"new_images\right.png")
        self.img_triangle = Image.open(r"new_images\triangle.png")

        self.combined_img1 = Image.new("RGB", (200, 60), "black")
        self.draw1 = ImageDraw.Draw(self.combined_img1)
        self.combined_img1.paste(self.img_screen, (15, 20))
        self.draw1.text((50, 20), "Главный экран", fill="white", font=self.font)
        self.combined_photo1 = ImageTk.PhotoImage(self.combined_img1)

        self.combined_img2 = Image.new("RGB", (200, 60), "black")
        self.draw2 = ImageDraw.Draw(self.combined_img2)
        self.combined_img2.paste(self.img_calendar, (10, 15))
        self.combined_img2.paste(self.img_triangle, (180, 13))
        self.draw2.text((50, 10), "Планировщик\nуставок", fill="white", font=self.font)
        self.combined_photo2 = ImageTk.PhotoImage(self.combined_img2)

        self.combined_img3 = Image.new("RGB", (200, 60), "black")
        self.draw3 = ImageDraw.Draw(self.combined_img3)
        self.combined_img3.paste(self.img_peak, (10, 15))
        self.combined_img3.paste(self.img_right, (170, 15))
        self.draw3.text((50, 20), "Мониторинг", fill="white", font=self.font)
        self.combined_photo3 = ImageTk.PhotoImage(self.combined_img3)

        self.combined_img4 = Image.new("RGB", (200, 60), "black")
        self.draw4 = ImageDraw.Draw(self.combined_img4)
        self.combined_img4.paste(self.img_tablet, (10, 15))
        self.combined_img4.paste(self.img_right, (170, 15))
        self.draw4.text((50, 20), "Журнал", fill="white", font=self.font)
        self.combined_photo4 = ImageTk.PhotoImage(self.combined_img4)

        self.combined_img5 = Image.new("RGB", (200, 60), "black")
        self.draw5 = ImageDraw.Draw(self.combined_img5)
        self.combined_img5.paste(self.img_gear_wheel, (10, 15))
        self.combined_img5.paste(self.img_right, (170, 15))
        self.draw5.text((50, 10), "Настройки\nстанции", fill="white", font=self.font)
        self.combined_photo5 = ImageTk.PhotoImage(self.combined_img5)

        self.combined_img6 = Image.new("RGB", (200, 60), "black")
        self.draw6 = ImageDraw.Draw(self.combined_img6)
        self.combined_img6.paste(self.img_wrench, (10, 15))
        self.combined_img6.paste(self.img_right, (170, 15))
        self.draw6.text((50, 10), "Инженерное\nменю", fill="white", font=self.font)
        self.combined_photo6 = ImageTk.PhotoImage(self.combined_img6)

        self.combined_img7 = Image.new("RGB", (200, 60), "black")
        self.draw7 = ImageDraw.Draw(self.combined_img7)
        self.combined_img7.paste(self.img_gear_wheel_bg, (10, 15))
        self.draw7.text((50, 10), "Настройки\nпанели", fill="white", font=self.font)
        self.combined_photo7 = ImageTk.PhotoImage(self.combined_img7)

        self.combined_img8 = Image.new("RGB", (200, 60), "black")
        self.draw8 = ImageDraw.Draw(self.combined_img8)
        self.combined_img8.paste(self.img_phone, (10, 15))
        self.draw8.text((50, 20), "Контакты", fill="white", font=self.font)
        self.combined_photo8 = ImageTk.PhotoImage(self.combined_img8)

        button = tk.Button(self, image=self.combined_photo1, bg='black', relief="groove", activebackground="black",
                           command=lambda: controller.show_frame("Frame1_1"))
        button.place(x=0, y=0, width=200, height=60)
        button2 = tk.Button(self, image=self.combined_photo2, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame2"))
        button2.place(x=0, y=60, width=200, height=60)
        button3 = tk.Button(self, image=self.combined_photo3, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame3"))
        button3.place(x=0, y=120, width=200, height=60)
        button4 = tk.Button(self, image=self.combined_photo4, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame6"))
        button4.place(x=0, y=180, width=200, height=60)
        button5 = tk.Button(self, image=self.combined_photo5, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame9"))
        button5.place(x=0, y=240, width=200, height=60)
        button6 = tk.Button(self, image=self.combined_photo6, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame16"))
        button6.place(x=0, y=300, width=200, height=60)
        button7 = tk.Button(self, image=self.combined_photo7, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame19"))
        button7.place(x=0, y=360, width=200, height=60)
        button8 = tk.Button(self, image=self.combined_photo8, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame20"))
        button8.place(x=0, y=420, width=200, height=60)

    def update_clock(self, current_time):
        self.clock_label.config(text=current_time)

class Frame3(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='black')
        self.clock_label = tk.Label(self, text="", fg='white', bg='black', font=('Roboto Bold', 12))
        self.clock_label.place(x=680, y=5)

        self.canvas = Canvas(
            self,
            bg="black",
            height=480,
            width=800,
            bd=0,
            highlightthickness=0,
            relief="ridge")
        self.canvas.place(x=0, y=0)

        self.font = ImageFont.truetype("Roboto-Bold.ttf", 18)
        self.img_screen = Image.open(r"new_images\screen.png")
        self.img_peak = Image.open(r"new_images\peak.png")
        self.img_timer = Image.open(r"new_images\timer.png")
        self.img_right = Image.open(r"new_images\right.png")
        self.img_left = Image.open(r"new_images\left.png")
        self.img_triangle = Image.open(r"new_images\triangle.png")

        self.combined_img1 = Image.new("RGB", (200, 60), "black")
        self.draw1 = ImageDraw.Draw(self.combined_img1)
        self.combined_img1.paste(self.img_screen, (15, 20))
        self.draw1.text((50, 20), "Главный экран", fill="white", font=self.font)
        self.combined_photo1 = ImageTk.PhotoImage(self.combined_img1)

        self.combined_img2 = Image.new("RGB", (200, 60), "black")
        self.draw2 = ImageDraw.Draw(self.combined_img2)
        self.combined_img2.paste(self.img_left, (15, 20))
        self.draw2.text((50, 20), "Назад", fill="white", font=self.font)
        self.combined_photo2 = ImageTk.PhotoImage(self.combined_img2)

        self.combined_img3 = Image.new("RGB", (200, 60), "black")
        self.draw3 = ImageDraw.Draw(self.combined_img3)
        self.combined_img3.paste(self.img_peak, (10, 15))
        self.combined_img3.paste(self.img_triangle, (180, 13))
        self.draw3.text((50, 10), "Тренды\nонлайн", fill="white", font=self.font)
        self.combined_photo3 = ImageTk.PhotoImage(self.combined_img3)

        self.combined_img4 = Image.new("RGB", (200, 60), "black")
        self.draw4 = ImageDraw.Draw(self.combined_img4)
        self.combined_img4.paste(self.img_peak, (10, 15))
        self.combined_img4.paste(self.img_right, (170, 15))
        self.draw4.text((50, 10), "Тренды\nистории", fill="white", font=self.font)
        self.combined_photo4 = ImageTk.PhotoImage(self.combined_img4)

        self.combined_img5 = Image.new("RGB", (200, 60), "black")
        self.draw5 = ImageDraw.Draw(self.combined_img5)
        self.combined_img5.paste(self.img_timer, (10, 15))
        self.draw5.text((50, 10), "Наработки\nнасосов", fill="white", font=self.font)
        self.combined_photo5 = ImageTk.PhotoImage(self.combined_img5)

        button = tk.Button(self, image=self.combined_photo1, bg='black', relief="groove", activebackground="black",
                           command=lambda: controller.show_frame("Frame1_1"))
        button.place(x=0, y=0, width=200, height=60)
        button2 = tk.Button(self, image=self.combined_photo2, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame2"))
        button2.place(x=0, y=60, width=200, height=60)
        button3 = tk.Button(self, image=self.combined_photo3, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame3"))
        button3.place(x=0, y=120, width=200, height=60)
        button4 = tk.Button(self, image=self.combined_photo4, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame4"))
        button4.place(x=0, y=180, width=200, height=60)
        button5 = tk.Button(self, image=self.combined_photo5, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame5"))
        button5.place(x=0, y=240, width=200, height=60)

    def update_clock(self, current_time):
        self.clock_label.config(text=current_time)


class Frame4(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='black')
        self.clock_label = tk.Label(self, text="", fg='white', bg='black', font=('Roboto Bold', 12))
        self.clock_label.place(x=680, y=5)

        self.canvas = Canvas(
            self,
            bg="black",
            height=480,
            width=800,
            bd=0,
            highlightthickness=0,
            relief="ridge")
        self.canvas.place(x=0, y=0)

        self.font = ImageFont.truetype("Roboto-Bold.ttf", 18)
        self.img_screen = Image.open(r"new_images\screen.png")
        self.img_left = Image.open(r"new_images\left.png")

        self.combined_img1 = Image.new("RGB", (200, 60), "black")
        self.draw1 = ImageDraw.Draw(self.combined_img1)
        self.combined_img1.paste(self.img_screen, (15, 20))
        self.draw1.text((50, 20), "Главный экран", fill="white", font=self.font)
        self.combined_photo1 = ImageTk.PhotoImage(self.combined_img1)

        self.combined_img2 = Image.new("RGB", (200, 60), "black")
        self.draw2 = ImageDraw.Draw(self.combined_img2)
        self.combined_img2.paste(self.img_left, (15, 20))
        self.draw2.text((50, 20), "Назад", fill="white", font=self.font)
        self.combined_photo2 = ImageTk.PhotoImage(self.combined_img2)

        button = tk.Button(self, image=self.combined_photo1, bg='black', relief="groove", activebackground="black",
                           command=lambda: controller.show_frame("Frame1_1"))
        button.place(x=0, y=0, width=200, height=60)
        button2 = tk.Button(self, image=self.combined_photo2, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame3"))
        button2.place(x=0, y=60, width=200, height=60)


    def update_clock(self, current_time):
        self.clock_label.config(text=current_time)


class Frame5(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='black')
        self.clock_label = tk.Label(self, text="", fg='white', bg='black', font=('Roboto Bold', 12))
        self.clock_label.place(x=680, y=5)

        self.canvas = Canvas(
            self,
            bg="black",
            height=480,
            width=800,
            bd=0,
            highlightthickness=0,
            relief="ridge")
        self.canvas.place(x=0, y=0)

        self.font = ImageFont.truetype("Roboto-Bold.ttf", 18)
        self.img_screen = Image.open(r"new_images\screen.png")
        self.img_peak = Image.open(r"new_images\peak.png")
        self.img_timer = Image.open(r"new_images\timer.png")
        self.img_right = Image.open(r"new_images\right.png")
        self.img_left = Image.open(r"new_images\left.png")
        self.img_triangle = Image.open(r"new_images\triangle.png")

        self.combined_img1 = Image.new("RGB", (200, 60), "black")
        self.draw1 = ImageDraw.Draw(self.combined_img1)
        self.combined_img1.paste(self.img_screen, (15, 20))
        self.draw1.text((50, 20), "Главный экран", fill="white", font=self.font)
        self.combined_photo1 = ImageTk.PhotoImage(self.combined_img1)

        self.combined_img2 = Image.new("RGB", (200, 60), "black")
        self.draw2 = ImageDraw.Draw(self.combined_img2)
        self.combined_img2.paste(self.img_left, (15, 20))
        self.draw2.text((50, 20), "Назад", fill="white", font=self.font)
        self.combined_photo2 = ImageTk.PhotoImage(self.combined_img2)

        self.combined_img3 = Image.new("RGB", (200, 60), "black")
        self.draw3 = ImageDraw.Draw(self.combined_img3)
        self.combined_img3.paste(self.img_peak, (10, 15))
        self.draw3.text((50, 10), "Тренды\nонлайн", fill="white", font=self.font)
        self.combined_photo3 = ImageTk.PhotoImage(self.combined_img3)

        self.combined_img4 = Image.new("RGB", (200, 60), "black")
        self.draw4 = ImageDraw.Draw(self.combined_img4)
        self.combined_img4.paste(self.img_peak, (10, 15))
        self.combined_img4.paste(self.img_right, (170, 15))
        self.draw4.text((50, 10), "Тренды\nистории", fill="white", font=self.font)
        self.combined_photo4 = ImageTk.PhotoImage(self.combined_img4)

        self.combined_img5 = Image.new("RGB", (200, 60), "black")
        self.draw5 = ImageDraw.Draw(self.combined_img5)
        self.combined_img5.paste(self.img_timer, (10, 15))
        self.combined_img5.paste(self.img_triangle, (180, 13))
        self.draw5.text((50, 10), "Наработки\nнасосов", fill="white", font=self.font)
        self.combined_photo5 = ImageTk.PhotoImage(self.combined_img5)

        button = tk.Button(self, image=self.combined_photo1, bg='black', relief="groove", activebackground="black",
                           command=lambda: controller.show_frame("Frame1_1"))
        button.place(x=0, y=0, width=200, height=60)
        button2 = tk.Button(self, image=self.combined_photo2, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame2"))
        button2.place(x=0, y=60, width=200, height=60)
        button3 = tk.Button(self, image=self.combined_photo3, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame3"))
        button3.place(x=0, y=120, width=200, height=60)
        button4 = tk.Button(self, image=self.combined_photo4, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame4"))
        button4.place(x=0, y=180, width=200, height=60)
        button5 = tk.Button(self, image=self.combined_photo5, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame5"))
        button5.place(x=0, y=240, width=200, height=60)


    def update_clock(self, current_time):
        self.clock_label.config(text=current_time)

class Frame6(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='black')
        self.canvas = Canvas(
            self,
            bg="black",
            height=480,
            width=800,
            bd=0,
            highlightthickness=0,
            relief="ridge")
        self.canvas.place(x=0, y=0)

        self.clock_label = tk.Label(self.canvas, text="", fg='white', bg='black', font=('Roboto Bold', 12))
        self.clock_label.place(x=680, y=5)

        self.font = ImageFont.truetype("Roboto-Bold.ttf", 18)
        self.img_screen = Image.open(r"new_images\screen.png")
        self.img_peak = Image.open(r"new_images\peak.png")
        self.img_timer = Image.open(r"new_images\timer.png")
        self.img_right = Image.open(r"new_images\right.png")
        self.img_left = Image.open(r"new_images\left.png")
        self.img_triangle = Image.open(r"new_images\triangle.png")

        self.combined_img1 = Image.new("RGB", (200, 60), "black")
        self.draw1 = ImageDraw.Draw(self.combined_img1)
        self.combined_img1.paste(self.img_screen, (15, 20))
        self.draw1.text((50, 20), "Главный экран", fill="white", font=self.font)
        self.combined_photo1 = ImageTk.PhotoImage(self.combined_img1)

        self.combined_img2 = Image.new("RGB", (200, 60), "black")
        self.draw2 = ImageDraw.Draw(self.combined_img2)
        self.combined_img2.paste(self.img_left, (15, 20))
        self.draw2.text((50, 20), "Назад", fill="white", font=self.font)
        self.combined_photo2 = ImageTk.PhotoImage(self.combined_img2)

        self.combined_img3 = Image.new("RGB", (200, 60), "black")
        self.draw3 = ImageDraw.Draw(self.combined_img3)
        self.combined_img3.paste(self.img_peak, (10, 15))
        self.combined_img3.paste(self.img_triangle, (180, 13))
        self.draw3.text((50, 10), "Текущие\nсобытия", fill="white", font=self.font)
        self.combined_photo3 = ImageTk.PhotoImage(self.combined_img3)

        self.combined_img4 = Image.new("RGB", (200, 60), "black")
        self.draw4 = ImageDraw.Draw(self.combined_img4)
        self.combined_img4.paste(self.img_peak, (10, 15))
        self.combined_img4.paste(self.img_right, (170, 15))
        self.draw4.text((50, 10), "Журнал\nистория", fill="white", font=self.font)
        self.combined_photo4 = ImageTk.PhotoImage(self.combined_img4)

        self.combined_img5 = Image.new("RGB", (200, 60), "black")
        self.draw5 = ImageDraw.Draw(self.combined_img5)
        self.combined_img5.paste(self.img_timer, (10, 15))
        self.draw5.text((50, 10), "Журнал\nизменений", fill="white", font=self.font)
        self.combined_photo5 = ImageTk.PhotoImage(self.combined_img5)

        button = tk.Button(self, image=self.combined_photo1, bg='black', relief="groove", activebackground="black",
                           command=lambda: controller.show_frame("Frame1_1"))
        button.place(x=0, y=0, width=200, height=60)
        button2 = tk.Button(self, image=self.combined_photo2, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame2"))
        button2.place(x=0, y=60, width=200, height=60)
        button3 = tk.Button(self, image=self.combined_photo3, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame6"))
        button3.place(x=0, y=120, width=200, height=60)
        button4 = tk.Button(self, image=self.combined_photo4, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame7"))
        button4.place(x=0, y=180, width=200, height=60)
        button5 = tk.Button(self, image=self.combined_photo5, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame8"))
        button5.place(x=0, y=240, width=200, height=60)

    def update_clock(self, current_time):
        self.clock_label.config(text=current_time)

class Frame7(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='black')
        self.canvas = Canvas(
            self,
            bg="black",
            height=480,
            width=800,
            bd=0,
            highlightthickness=0,
            relief="ridge")
        self.canvas.place(x=0, y=0)

        self.clock_label = tk.Label(self.canvas, text="", fg='white', bg='black', font=('Roboto Bold', 12))
        self.clock_label.place(x=680, y=5)

        self.font = ImageFont.truetype("Roboto-Bold.ttf", 18)
        self.img_screen = Image.open(r"new_images\screen.png")
        self.img_left = Image.open(r"new_images\left.png")

        self.combined_img1 = Image.new("RGB", (200, 60), "black")
        self.draw1 = ImageDraw.Draw(self.combined_img1)
        self.combined_img1.paste(self.img_screen, (15, 20))
        self.draw1.text((50, 20), "Главный экран", fill="white", font=self.font)
        self.combined_photo1 = ImageTk.PhotoImage(self.combined_img1)

        self.combined_img2 = Image.new("RGB", (200, 60), "black")
        self.draw2 = ImageDraw.Draw(self.combined_img2)
        self.combined_img2.paste(self.img_left, (15, 20))
        self.draw2.text((50, 20), "Назад", fill="white", font=self.font)
        self.combined_photo2 = ImageTk.PhotoImage(self.combined_img2)

        button = tk.Button(self, image=self.combined_photo1, bg='black', relief="groove", activebackground="black",
                           command=lambda: controller.show_frame("Frame1_1"))
        button.place(x=0, y=0, width=200, height=60)
        button2 = tk.Button(self, image=self.combined_photo2, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame6"))
        button2.place(x=0, y=60, width=200, height=60)


    def update_clock(self, current_time):
        self.clock_label.config(text=current_time)

class Frame8(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='black')
        self.canvas = Canvas(
            self,
            bg="black",
            height=480,
            width=800,
            bd=0,
            highlightthickness=0,
            relief="ridge")
        self.canvas.place(x=0, y=0)

        self.clock_label = tk.Label(self.canvas, text="", fg='white', bg='black', font=('Roboto Bold', 12))
        self.clock_label.place(x=680, y=5)

        self.font = ImageFont.truetype("Roboto-Bold.ttf", 18)
        self.img_screen = Image.open(r"new_images\screen.png")
        self.img_peak = Image.open(r"new_images\peak.png")
        self.img_timer = Image.open(r"new_images\timer.png")
        self.img_right = Image.open(r"new_images\right.png")
        self.img_left = Image.open(r"new_images\left.png")
        self.img_triangle = Image.open(r"new_images\triangle.png")

        self.combined_img1 = Image.new("RGB", (200, 60), "black")
        self.draw1 = ImageDraw.Draw(self.combined_img1)
        self.combined_img1.paste(self.img_screen, (15, 20))
        self.draw1.text((50, 20), "Главный экран", fill="white", font=self.font)
        self.combined_photo1 = ImageTk.PhotoImage(self.combined_img1)

        self.combined_img2 = Image.new("RGB", (200, 60), "black")
        self.draw2 = ImageDraw.Draw(self.combined_img2)
        self.combined_img2.paste(self.img_left, (15, 20))
        self.draw2.text((50, 20), "Назад", fill="white", font=self.font)
        self.combined_photo2 = ImageTk.PhotoImage(self.combined_img2)

        self.combined_img3 = Image.new("RGB", (200, 60), "black")
        self.draw3 = ImageDraw.Draw(self.combined_img3)
        self.combined_img3.paste(self.img_peak, (10, 15))
        self.draw3.text((50, 10), "Текущие\nсобытия", fill="white", font=self.font)
        self.combined_photo3 = ImageTk.PhotoImage(self.combined_img3)

        self.combined_img4 = Image.new("RGB", (200, 60), "black")
        self.draw4 = ImageDraw.Draw(self.combined_img4)
        self.combined_img4.paste(self.img_peak, (10, 15))
        self.combined_img4.paste(self.img_right, (170, 15))
        self.draw4.text((50, 10), "Журнал\nистория", fill="white", font=self.font)
        self.combined_photo4 = ImageTk.PhotoImage(self.combined_img4)

        self.combined_img5 = Image.new("RGB", (200, 60), "black")
        self.draw5 = ImageDraw.Draw(self.combined_img5)
        self.combined_img5.paste(self.img_timer, (10, 15))
        self.combined_img5.paste(self.img_triangle, (180, 13))
        self.draw5.text((50, 10), "Журнал\nизменений", fill="white", font=self.font)
        self.combined_photo5 = ImageTk.PhotoImage(self.combined_img5)

        button = tk.Button(self, image=self.combined_photo1, bg='black', relief="groove", activebackground="black",
                           command=lambda: controller.show_frame("Frame1_1"))
        button.place(x=0, y=0, width=200, height=60)
        button2 = tk.Button(self, image=self.combined_photo2, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame2"))
        button2.place(x=0, y=60, width=200, height=60)
        button3 = tk.Button(self, image=self.combined_photo3, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame6"))
        button3.place(x=0, y=120, width=200, height=60)
        button4 = tk.Button(self, image=self.combined_photo4, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame7"))
        button4.place(x=0, y=180, width=200, height=60)
        button5 = tk.Button(self, image=self.combined_photo5, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame8"))
        button5.place(x=0, y=240, width=200, height=60)

    def update_clock(self, current_time):
        self.clock_label.config(text=current_time)

class Frame9(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='black')

        self.canvas = Canvas(
            self,
            bg="black",
            height=480,
            width=800,
            bd=0,
            highlightthickness=0,
            relief="ridge")
        self.canvas.place(x=0, y=0)

        self.clock_label = tk.Label(self, text="", fg='white', bg='black', font=('Roboto Bold', 12))
        self.clock_label.place(x=680, y=5)

        self.font = ImageFont.truetype("Roboto-Bold.ttf", 18)
        self.img_screen = Image.open(r"new_images\screen.png")
        self.img_left = Image.open(r"new_images\left.png")
        self.img_triangle = Image.open(r"new_images\triangle.png")
        self.img_diode = Image.open(r"new_images\diode.png")
        self.img_swap = Image.open(r"new_images\swap.png")
        self.img_plusone = Image.open(r"new_images\plus_one.png")
        self.img_minusone = Image.open(r"new_images\minus_one.png")
        self.img_options = Image.open(r"new_images\options.png")
        self.img_emergency = Image.open(r"new_images\emergency.png")

        self.combined_img1 = Image.new("RGB", (200, 60), "black")
        self.draw1 = ImageDraw.Draw(self.combined_img1)
        self.combined_img1.paste(self.img_screen, (15, 20))
        self.draw1.text((50, 20), "Главный экран", fill="white", font=self.font)
        self.combined_photo1 = ImageTk.PhotoImage(self.combined_img1)

        self.combined_img2 = Image.new("RGB", (200, 60), "black")
        self.draw2 = ImageDraw.Draw(self.combined_img2)
        self.combined_img2.paste(self.img_left, (15, 20))
        self.draw2.text((50, 20), "Назад", fill="white", font=self.font)
        self.combined_photo2 = ImageTk.PhotoImage(self.combined_img2)

        self.combined_img3 = Image.new("RGB", (200, 60), "black")
        self.draw3 = ImageDraw.Draw(self.combined_img3)
        self.combined_img3.paste(self.img_diode, (10, 15))
        self.combined_img3.paste(self.img_triangle, (180, 13))
        self.draw3.text((50, 10), "Параметры\nдвигателей", fill="white", font=self.font)
        self.combined_photo3 = ImageTk.PhotoImage(self.combined_img3)

        self.combined_img4 = Image.new("RGB", (200, 60), "black")
        self.draw4 = ImageDraw.Draw(self.combined_img4)
        self.combined_img4.paste(self.img_swap, (15, 15))
        self.draw4.text((50, 10), "Настройки\nдатчиков", fill="white", font=self.font)
        self.combined_photo4 = ImageTk.PhotoImage(self.combined_img4)

        self.combined_img5 = Image.new("RGB", (200, 60), "black")
        self.draw5 = ImageDraw.Draw(self.combined_img5)
        self.combined_img5.paste(self.img_swap, (15, 15))
        self.draw5.text((50, 10), "Параметры\nнасосов общ.", fill="white", font=self.font)
        self.combined_photo5 = ImageTk.PhotoImage(self.combined_img5)

        self.combined_img6 = Image.new("RGB", (200, 60), "black")
        self.draw6 = ImageDraw.Draw(self.combined_img6)
        self.combined_img6.paste(self.img_plusone, (15, 15))
        self.draw6.text((50, 10), "Вкл. доп.\nнасосов", fill="white", font=self.font)
        self.combined_photo6 = ImageTk.PhotoImage(self.combined_img6)

        self.combined_img7 = Image.new("RGB", (200, 60), "black")
        self.draw7 = ImageDraw.Draw(self.combined_img7)
        self.combined_img7.paste(self.img_minusone, (15, 15))
        self.draw7.text((50, 10), "Откл. доп.\nнасосов", fill="white", font=self.font)
        self.combined_photo7 = ImageTk.PhotoImage(self.combined_img7)

        self.combined_img8 = Image.new("RGB", (200, 60), "black")
        self.draw8 = ImageDraw.Draw(self.combined_img8)
        self.combined_img8.paste(self.img_options, (15, 15))
        self.draw8.text((50, 20), "Опции", fill="white", font=self.font)
        self.combined_photo8 = ImageTk.PhotoImage(self.combined_img8)

        self.combined_img9 = Image.new("RGB", (200, 60), "black")
        self.draw9 = ImageDraw.Draw(self.combined_img9)
        self.combined_img9.paste(self.img_emergency, (15, 15))
        self.draw9.text((50, 10), "Аварийные\nрежимы", fill="white", font=self.font)
        self.combined_photo9 = ImageTk.PhotoImage(self.combined_img9)

        button = tk.Button(self, image=self.combined_photo1, bg='black', relief="groove", activebackground="black",
                           command=lambda: controller.show_frame("Frame1_1"))
        button.place(x=0, y=0, width=200, height=60)
        button2 = tk.Button(self, image=self.combined_photo2, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame2"))
        button2.place(x=0, y=60, width=200, height=52.5)
        button3 = tk.Button(self, image=self.combined_photo3, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame9"))
        button3.place(x=0, y=112.5, width=200, height=52.5)
        button4 = tk.Button(self, image=self.combined_photo4, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame10"))
        button4.place(x=0, y=165, width=200, height=52.5)
        button5 = tk.Button(self, image=self.combined_photo5, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame11"))
        button5.place(x=0, y=217.5, width=200, height=52.5)
        button6 = tk.Button(self, image=self.combined_photo6, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame12"))
        button6.place(x=0, y=270, width=200, height=52.5)
        button7 = tk.Button(self, image=self.combined_photo7, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame13"))
        button7.place(x=0, y=322.5, width=200, height=52.5)
        button8 = tk.Button(self, image=self.combined_photo8, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame14"))
        button8.place(x=0, y=375, width=200, height=52.5)
        button9 = tk.Button(self, image=self.combined_photo9, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame15"))
        button9.place(x=0, y=427.5, width=200, height=52.5)

        self.InterfaceScreen_img = PhotoImage(file=r"images\StationSettings\EngineParameters.png")
        self.InterfaceScreen = self.canvas.create_image(498, 230, image=self.InterfaceScreen_img)

        self.Switch_Flat_first_img = PhotoImage(file=r"images\StationSettings\ReadingGray.png")
        self.Switch_Flat_first_button = self.canvas.create_image(676, 362, image=self.Switch_Flat_first_img)
        self.canvas.tag_bind(self.Switch_Flat_first_button, "<Button-1>", self.update_switch_first)

        self.Switch_Flat_second_img = PhotoImage(file=r"images\StationSettings\RecordGray.png")
        self.Switch_Flat_second_button = self.canvas.create_image(676, 404, image=self.Switch_Flat_second_img)
        self.canvas.tag_bind(self.Switch_Flat_second_button, "<Button-1>", self.update_switch_second)

    def update_switch_first(self, event):
        if self.Switch_Flat_first_img.cget("file") == "images\StationSettings\ReadingGray.png":
            self.Switch_Flat_first_img = PhotoImage(file=r"images\StationSettings\ReadingGreen.png")
        elif self.Switch_Flat_first_img.cget("file") == "images\StationSettings\ReadingGreen.png":
            self.Switch_Flat_first_img = PhotoImage(file=r"images\StationSettings\ReadingGray.png")
        self.Switch_Flat_first_button = self.canvas.create_image(676, 362, image=self.Switch_Flat_first_img)
        self.canvas.tag_bind(self.Switch_Flat_first_button, "<Button-1>", self.update_switch_first)

    def update_switch_second(self, event):
        if self.Switch_Flat_second_img.cget("file") == "images\StationSettings\RecordGray.png":
            self.Switch_Flat_second_img = PhotoImage(file=r"images\StationSettings\RecordGreen.png")
        elif self.Switch_Flat_second_img.cget("file") == "images\StationSettings\RecordGreen.png":
            self.Switch_Flat_second_img = PhotoImage(file=r"images\StationSettings\RecordGray.png")
        self.Switch_Flat_second_button = self.canvas.create_image(676, 404, image=self.Switch_Flat_second_img)
        self.canvas.tag_bind(self.Switch_Flat_second_button, "<Button-1>", self.update_switch_second)

    def update_clock(self, current_time):
        self.clock_label.config(text=current_time)

class Frame10(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='black')

        self.canvas = Canvas(
            self,
            bg="black",
            height=480,
            width=800,
            bd=0,
            highlightthickness=0,
            relief="ridge")
        self.canvas.place(x=0, y=0)

        self.clock_label = tk.Label(self, text="", fg='white', bg='black', font=('Roboto Bold', 12))
        self.clock_label.place(x=680, y=5)

        self.font = ImageFont.truetype("Roboto-Bold.ttf", 18)
        self.img_screen = Image.open(r"new_images\screen.png")
        self.img_left = Image.open(r"new_images\left.png")
        self.img_triangle = Image.open(r"new_images\triangle.png")
        self.img_diode = Image.open(r"new_images\diode.png")
        self.img_swap = Image.open(r"new_images\swap.png")
        self.img_plusone = Image.open(r"new_images\plus_one.png")
        self.img_minusone = Image.open(r"new_images\minus_one.png")
        self.img_options = Image.open(r"new_images\options.png")
        self.img_emergency = Image.open(r"new_images\emergency.png")

        self.combined_img1 = Image.new("RGB", (200, 60), "black")
        self.draw1 = ImageDraw.Draw(self.combined_img1)
        self.combined_img1.paste(self.img_screen, (15, 20))
        self.draw1.text((50, 20), "Главный экран", fill="white", font=self.font)
        self.combined_photo1 = ImageTk.PhotoImage(self.combined_img1)

        self.combined_img2 = Image.new("RGB", (200, 60), "black")
        self.draw2 = ImageDraw.Draw(self.combined_img2)
        self.combined_img2.paste(self.img_left, (15, 20))
        self.draw2.text((50, 20), "Назад", fill="white", font=self.font)
        self.combined_photo2 = ImageTk.PhotoImage(self.combined_img2)

        self.combined_img3 = Image.new("RGB", (200, 60), "black")
        self.draw3 = ImageDraw.Draw(self.combined_img3)
        self.combined_img3.paste(self.img_diode, (10, 15))
        self.draw3.text((50, 10), "Параметры\nдвигателей", fill="white", font=self.font)
        self.combined_photo3 = ImageTk.PhotoImage(self.combined_img3)

        self.combined_img4 = Image.new("RGB", (200, 60), "black")
        self.draw4 = ImageDraw.Draw(self.combined_img4)
        self.combined_img4.paste(self.img_swap, (15, 15))
        self.combined_img4.paste(self.img_triangle, (180, 13))
        self.draw4.text((50, 10), "Настройки\nдатчиков", fill="white", font=self.font)
        self.combined_photo4 = ImageTk.PhotoImage(self.combined_img4)

        self.combined_img5 = Image.new("RGB", (200, 60), "black")
        self.draw5 = ImageDraw.Draw(self.combined_img5)
        self.combined_img5.paste(self.img_swap, (15, 15))
        self.draw5.text((50, 10), "Параметры\nнасосов общ.", fill="white", font=self.font)
        self.combined_photo5 = ImageTk.PhotoImage(self.combined_img5)

        self.combined_img6 = Image.new("RGB", (200, 60), "black")
        self.draw6 = ImageDraw.Draw(self.combined_img6)
        self.combined_img6.paste(self.img_plusone, (15, 15))
        self.draw6.text((50, 10), "Вкл. доп.\nнасосов", fill="white", font=self.font)
        self.combined_photo6 = ImageTk.PhotoImage(self.combined_img6)

        self.combined_img7 = Image.new("RGB", (200, 60), "black")
        self.draw7 = ImageDraw.Draw(self.combined_img7)
        self.combined_img7.paste(self.img_minusone, (15, 15))
        self.draw7.text((50, 10), "Откл. доп.\nнасосов", fill="white", font=self.font)
        self.combined_photo7 = ImageTk.PhotoImage(self.combined_img7)

        self.combined_img8 = Image.new("RGB", (200, 60), "black")
        self.draw8 = ImageDraw.Draw(self.combined_img8)
        self.combined_img8.paste(self.img_options, (15, 15))
        self.draw8.text((50, 20), "Опции", fill="white", font=self.font)
        self.combined_photo8 = ImageTk.PhotoImage(self.combined_img8)

        self.combined_img9 = Image.new("RGB", (200, 60), "black")
        self.draw9 = ImageDraw.Draw(self.combined_img9)
        self.combined_img9.paste(self.img_emergency, (15, 15))
        self.draw9.text((50, 10), "Аварийные\nрежимы", fill="white", font=self.font)
        self.combined_photo9 = ImageTk.PhotoImage(self.combined_img9)

        button = tk.Button(self, image=self.combined_photo1, bg='black', relief="groove", activebackground="black",
                           command=lambda: controller.show_frame("Frame1_1"))
        button.place(x=0, y=0, width=200, height=60)
        button2 = tk.Button(self, image=self.combined_photo2, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame2"))
        button2.place(x=0, y=60, width=200, height=52.5)
        button3 = tk.Button(self, image=self.combined_photo3, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame9"))
        button3.place(x=0, y=112.5, width=200, height=52.5)
        button4 = tk.Button(self, image=self.combined_photo4, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame10"))
        button4.place(x=0, y=165, width=200, height=52.5)
        button5 = tk.Button(self, image=self.combined_photo5, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame11"))
        button5.place(x=0, y=217.5, width=200, height=52.5)
        button6 = tk.Button(self, image=self.combined_photo6, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame12"))
        button6.place(x=0, y=270, width=200, height=52.5)
        button7 = tk.Button(self, image=self.combined_photo7, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame13"))
        button7.place(x=0, y=322.5, width=200, height=52.5)
        button8 = tk.Button(self, image=self.combined_photo8, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame14"))
        button8.place(x=0, y=375, width=200, height=52.5)
        button9 = tk.Button(self, image=self.combined_photo9, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame15"))
        button9.place(x=0, y=427.5, width=200, height=52.5)

        self.InterfaceScreen_img = PhotoImage(file=r"images\StationSettings\SensorSettings.png")
        self.InterfaceScreen = self.canvas.create_image(500, 160, image=self.InterfaceScreen_img)

    def update_clock(self, current_time):
        self.clock_label.config(text=current_time)
class Frame11(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='black')

        self.canvas = Canvas(
            self,
            bg="black",
            height=480,
            width=800,
            bd=0,
            highlightthickness=0,
            relief="ridge")
        self.canvas.place(x=0, y=0)

        self.clock_label = tk.Label(self, text="", fg='white', bg='black', font=('Roboto Bold', 12))
        self.clock_label.place(x=680, y=5)

        self.font = ImageFont.truetype("Roboto-Bold.ttf", 18)
        self.img_screen = Image.open(r"new_images\screen.png")
        self.img_left = Image.open(r"new_images\left.png")
        self.img_triangle = Image.open(r"new_images\triangle.png")
        self.img_diode = Image.open(r"new_images\diode.png")
        self.img_swap = Image.open(r"new_images\swap.png")
        self.img_plusone = Image.open(r"new_images\plus_one.png")
        self.img_minusone = Image.open(r"new_images\minus_one.png")
        self.img_options = Image.open(r"new_images\options.png")
        self.img_emergency = Image.open(r"new_images\emergency.png")

        self.combined_img1 = Image.new("RGB", (200, 60), "black")
        self.draw1 = ImageDraw.Draw(self.combined_img1)
        self.combined_img1.paste(self.img_screen, (15, 20))
        self.draw1.text((50, 20), "Главный экран", fill="white", font=self.font)
        self.combined_photo1 = ImageTk.PhotoImage(self.combined_img1)

        self.combined_img2 = Image.new("RGB", (200, 60), "black")
        self.draw2 = ImageDraw.Draw(self.combined_img2)
        self.combined_img2.paste(self.img_left, (15, 20))
        self.draw2.text((50, 20), "Назад", fill="white", font=self.font)
        self.combined_photo2 = ImageTk.PhotoImage(self.combined_img2)

        self.combined_img3 = Image.new("RGB", (200, 60), "black")
        self.draw3 = ImageDraw.Draw(self.combined_img3)
        self.combined_img3.paste(self.img_diode, (10, 15))
        self.draw3.text((50, 10), "Параметры\nдвигателей", fill="white", font=self.font)
        self.combined_photo3 = ImageTk.PhotoImage(self.combined_img3)

        self.combined_img4 = Image.new("RGB", (200, 60), "black")
        self.draw4 = ImageDraw.Draw(self.combined_img4)
        self.combined_img4.paste(self.img_swap, (15, 15))
        self.draw4.text((50, 10), "Настройки\nдатчиков", fill="white", font=self.font)
        self.combined_photo4 = ImageTk.PhotoImage(self.combined_img4)

        self.combined_img5 = Image.new("RGB", (200, 60), "black")
        self.draw5 = ImageDraw.Draw(self.combined_img5)
        self.combined_img5.paste(self.img_swap, (15, 15))
        self.combined_img5.paste(self.img_triangle, (180, 13))
        self.draw5.text((50, 10), "Параметры\nнасосов общ.", fill="white", font=self.font)
        self.combined_photo5 = ImageTk.PhotoImage(self.combined_img5)

        self.combined_img6 = Image.new("RGB", (200, 60), "black")
        self.draw6 = ImageDraw.Draw(self.combined_img6)
        self.combined_img6.paste(self.img_plusone, (15, 15))
        self.draw6.text((50, 10), "Вкл. доп.\nнасосов", fill="white", font=self.font)
        self.combined_photo6 = ImageTk.PhotoImage(self.combined_img6)

        self.combined_img7 = Image.new("RGB", (200, 60), "black")
        self.draw7 = ImageDraw.Draw(self.combined_img7)
        self.combined_img7.paste(self.img_minusone, (15, 15))
        self.draw7.text((50, 10), "Откл. доп.\nнасосов", fill="white", font=self.font)
        self.combined_photo7 = ImageTk.PhotoImage(self.combined_img7)

        self.combined_img8 = Image.new("RGB", (200, 60), "black")
        self.draw8 = ImageDraw.Draw(self.combined_img8)
        self.combined_img8.paste(self.img_options, (15, 15))
        self.draw8.text((50, 20), "Опции", fill="white", font=self.font)
        self.combined_photo8 = ImageTk.PhotoImage(self.combined_img8)

        self.combined_img9 = Image.new("RGB", (200, 60), "black")
        self.draw9 = ImageDraw.Draw(self.combined_img9)
        self.combined_img9.paste(self.img_emergency, (15, 15))
        self.draw9.text((50, 10), "Аварийные\nрежимы", fill="white", font=self.font)
        self.combined_photo9 = ImageTk.PhotoImage(self.combined_img9)

        button = tk.Button(self, image=self.combined_photo1, bg='black', relief="groove", activebackground="black",
                           command=lambda: controller.show_frame("Frame1_1"))
        button.place(x=0, y=0, width=200, height=60)
        button2 = tk.Button(self, image=self.combined_photo2, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame2"))
        button2.place(x=0, y=60, width=200, height=52.5)
        button3 = tk.Button(self, image=self.combined_photo3, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame9"))
        button3.place(x=0, y=112.5, width=200, height=52.5)
        button4 = tk.Button(self, image=self.combined_photo4, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame10"))
        button4.place(x=0, y=165, width=200, height=52.5)
        button5 = tk.Button(self, image=self.combined_photo5, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame11"))
        button5.place(x=0, y=217.5, width=200, height=52.5)
        button6 = tk.Button(self, image=self.combined_photo6, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame12"))
        button6.place(x=0, y=270, width=200, height=52.5)
        button7 = tk.Button(self, image=self.combined_photo7, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame13"))
        button7.place(x=0, y=322.5, width=200, height=52.5)
        button8 = tk.Button(self, image=self.combined_photo8, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame14"))
        button8.place(x=0, y=375, width=200, height=52.5)
        button9 = tk.Button(self, image=self.combined_photo9, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame15"))
        button9.place(x=0, y=427.5, width=200, height=52.5)

        self.InterfaceScreen_img = PhotoImage(file=r"images\StationSettings\ParametersOfTheDrivePump.png")
        self.InterfaceScreen = self.canvas.create_image(500, 200, image=self.InterfaceScreen_img)

        self.Switch_Flat_first_img = PhotoImage(file=r"images\StationSettings\Switch-0.png")
        self.Switch_Flat_first_button = self.canvas.create_image(670, 176, image=self.Switch_Flat_first_img)
        self.canvas.tag_bind(self.Switch_Flat_first_button, "<Button-1>", self.update_switch_first)

        self.Switch_Flat_second_img = PhotoImage(file=r"images\StationSettings\Switch-0.png")
        self.Switch_Flat_second_button = self.canvas.create_image(670, 218, image=self.Switch_Flat_second_img)
        self.canvas.tag_bind(self.Switch_Flat_second_button, "<Button-1>", self.update_switch_second)


    def update_switch_first(self, event):
        if self.Switch_Flat_first_img.cget("file") ==  "images\StationSettings\Switch-0.png":
            self.Switch_Flat_first_img = PhotoImage(file=r"images\StationSettings\Switch-1.png")
        elif self.Switch_Flat_first_img.cget("file") == "images\StationSettings\Switch-1.png":
            self.Switch_Flat_first_img = PhotoImage(file=r"images\StationSettings\Switch-0.png")
        self.Switch_Flat_first_button = self.canvas.create_image(670, 176, image=self.Switch_Flat_first_img)
        self.canvas.tag_bind(self.Switch_Flat_first_button, "<Button-1>", self.update_switch_first)

    def update_switch_second(self, event):
        if self.Switch_Flat_second_img.cget("file") == "images\StationSettings\Switch-0.png":
            self.Switch_Flat_second_img = PhotoImage(file=r"images\StationSettings\Switch-1.png")
        elif self.Switch_Flat_second_img.cget("file") == "images\StationSettings\Switch-1.png":
            self.Switch_Flat_second_img = PhotoImage(file=r"images\StationSettings\Switch-0.png")
        self.Switch_Flat_second_button = self.canvas.create_image(670, 218, image=self.Switch_Flat_second_img)
        self.canvas.tag_bind(self.Switch_Flat_second_button, "<Button-1>", self.update_switch_second)
    def update_clock(self, current_time):
        self.clock_label.config(text=current_time)

class Frame12(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='black')

        self.canvas = Canvas(
            self,
            bg="black",
            height=480,
            width=800,
            bd=0,
            highlightthickness=0,
            relief="ridge")
        self.canvas.place(x=0, y=0)

        self.clock_label = tk.Label(self, text="", fg='white', bg='black', font=('Roboto Bold', 12))
        self.clock_label.place(x=680, y=5)

        self.font = ImageFont.truetype("Roboto-Bold.ttf", 18)
        self.img_screen = Image.open(r"new_images\screen.png")
        self.img_left = Image.open(r"new_images\left.png")
        self.img_triangle = Image.open(r"new_images\triangle.png")
        self.img_diode = Image.open(r"new_images\diode.png")
        self.img_swap = Image.open(r"new_images\swap.png")
        self.img_plusone = Image.open(r"new_images\plus_one.png")
        self.img_minusone = Image.open(r"new_images\minus_one.png")
        self.img_options = Image.open(r"new_images\options.png")
        self.img_emergency = Image.open(r"new_images\emergency.png")

        self.combined_img1 = Image.new("RGB", (200, 60), "black")
        self.draw1 = ImageDraw.Draw(self.combined_img1)
        self.combined_img1.paste(self.img_screen, (15, 20))
        self.draw1.text((50, 20), "Главный экран", fill="white", font=self.font)
        self.combined_photo1 = ImageTk.PhotoImage(self.combined_img1)

        self.combined_img2 = Image.new("RGB", (200, 60), "black")
        self.draw2 = ImageDraw.Draw(self.combined_img2)
        self.combined_img2.paste(self.img_left, (15, 20))
        self.draw2.text((50, 20), "Назад", fill="white", font=self.font)
        self.combined_photo2 = ImageTk.PhotoImage(self.combined_img2)

        self.combined_img3 = Image.new("RGB", (200, 60), "black")
        self.draw3 = ImageDraw.Draw(self.combined_img3)
        self.combined_img3.paste(self.img_diode, (10, 15))
        self.draw3.text((50, 10), "Параметры\nдвигателей", fill="white", font=self.font)
        self.combined_photo3 = ImageTk.PhotoImage(self.combined_img3)

        self.combined_img4 = Image.new("RGB", (200, 60), "black")
        self.draw4 = ImageDraw.Draw(self.combined_img4)
        self.combined_img4.paste(self.img_swap, (15, 15))
        self.draw4.text((50, 10), "Настройки\nдатчиков", fill="white", font=self.font)
        self.combined_photo4 = ImageTk.PhotoImage(self.combined_img4)

        self.combined_img5 = Image.new("RGB", (200, 60), "black")
        self.draw5 = ImageDraw.Draw(self.combined_img5)
        self.combined_img5.paste(self.img_swap, (15, 15))
        self.draw5.text((50, 10), "Параметры\nнасосов общ.", fill="white", font=self.font)
        self.combined_photo5 = ImageTk.PhotoImage(self.combined_img5)

        self.combined_img6 = Image.new("RGB", (200, 60), "black")
        self.draw6 = ImageDraw.Draw(self.combined_img6)
        self.combined_img6.paste(self.img_plusone, (15, 15))
        self.combined_img6.paste(self.img_triangle, (180, 13))
        self.draw6.text((50, 10), "Вкл. доп.\nнасосов", fill="white", font=self.font)
        self.combined_photo6 = ImageTk.PhotoImage(self.combined_img6)

        self.combined_img7 = Image.new("RGB", (200, 60), "black")
        self.draw7 = ImageDraw.Draw(self.combined_img7)
        self.combined_img7.paste(self.img_minusone, (15, 15))
        self.draw7.text((50, 10), "Откл. доп.\nнасосов", fill="white", font=self.font)
        self.combined_photo7 = ImageTk.PhotoImage(self.combined_img7)

        self.combined_img8 = Image.new("RGB", (200, 60), "black")
        self.draw8 = ImageDraw.Draw(self.combined_img8)
        self.combined_img8.paste(self.img_options, (15, 15))
        self.draw8.text((50, 20), "Опции", fill="white", font=self.font)
        self.combined_photo8 = ImageTk.PhotoImage(self.combined_img8)

        self.combined_img9 = Image.new("RGB", (200, 60), "black")
        self.draw9 = ImageDraw.Draw(self.combined_img9)
        self.combined_img9.paste(self.img_emergency, (15, 15))
        self.draw9.text((50, 10), "Аварийные\nрежимы", fill="white", font=self.font)
        self.combined_photo9 = ImageTk.PhotoImage(self.combined_img9)

        button = tk.Button(self, image=self.combined_photo1, bg='black', relief="groove", activebackground="black",
                           command=lambda: controller.show_frame("Frame1_1"))
        button.place(x=0, y=0, width=200, height=60)
        button2 = tk.Button(self, image=self.combined_photo2, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame2"))
        button2.place(x=0, y=60, width=200, height=52.5)
        button3 = tk.Button(self, image=self.combined_photo3, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame9"))
        button3.place(x=0, y=112.5, width=200, height=52.5)
        button4 = tk.Button(self, image=self.combined_photo4, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame10"))
        button4.place(x=0, y=165, width=200, height=52.5)
        button5 = tk.Button(self, image=self.combined_photo5, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame11"))
        button5.place(x=0, y=217.5, width=200, height=52.5)
        button6 = tk.Button(self, image=self.combined_photo6, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame12"))
        button6.place(x=0, y=270, width=200, height=52.5)
        button7 = tk.Button(self, image=self.combined_photo7, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame13"))
        button7.place(x=0, y=322.5, width=200, height=52.5)
        button8 = tk.Button(self, image=self.combined_photo8, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame14"))
        button8.place(x=0, y=375, width=200, height=52.5)
        button9 = tk.Button(self, image=self.combined_photo9, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame15"))
        button9.place(x=0, y=427.5, width=200, height=52.5)

        self.InterfaceScreen_img = PhotoImage(file=r"images\StationSettings\ParametersForEnablingExtras.png")
        self.InterfaceScreen = self.canvas.create_image(500, 245, image=self.InterfaceScreen_img)

    def update_clock(self, current_time):
        self.clock_label.config(text=current_time)

class Frame13(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='black')

        self.canvas = Canvas(
            self,
            bg="black",
            height=480,
            width=800,
            bd=0,
            highlightthickness=0,
            relief="ridge")
        self.canvas.place(x=0, y=0)

        self.clock_label = tk.Label(self, text="", fg='white', bg='black', font=('Roboto Bold', 12))
        self.clock_label.place(x=680, y=5)

        self.font = ImageFont.truetype("Roboto-Bold.ttf", 18)
        self.img_screen = Image.open(r"new_images\screen.png")
        self.img_left = Image.open(r"new_images\left.png")
        self.img_triangle = Image.open(r"new_images\triangle.png")
        self.img_diode = Image.open(r"new_images\diode.png")
        self.img_swap = Image.open(r"new_images\swap.png")
        self.img_plusone = Image.open(r"new_images\plus_one.png")
        self.img_minusone = Image.open(r"new_images\minus_one.png")
        self.img_options = Image.open(r"new_images\options.png")
        self.img_emergency = Image.open(r"new_images\emergency.png")

        self.combined_img1 = Image.new("RGB", (200, 60), "black")
        self.draw1 = ImageDraw.Draw(self.combined_img1)
        self.combined_img1.paste(self.img_screen, (15, 20))
        self.draw1.text((50, 20), "Главный экран", fill="white", font=self.font)
        self.combined_photo1 = ImageTk.PhotoImage(self.combined_img1)

        self.combined_img2 = Image.new("RGB", (200, 60), "black")
        self.draw2 = ImageDraw.Draw(self.combined_img2)
        self.combined_img2.paste(self.img_left, (15, 20))
        self.draw2.text((50, 20), "Назад", fill="white", font=self.font)
        self.combined_photo2 = ImageTk.PhotoImage(self.combined_img2)

        self.combined_img3 = Image.new("RGB", (200, 60), "black")
        self.draw3 = ImageDraw.Draw(self.combined_img3)
        self.combined_img3.paste(self.img_diode, (10, 15))
        self.draw3.text((50, 10), "Параметры\nдвигателей", fill="white", font=self.font)
        self.combined_photo3 = ImageTk.PhotoImage(self.combined_img3)

        self.combined_img4 = Image.new("RGB", (200, 60), "black")
        self.draw4 = ImageDraw.Draw(self.combined_img4)
        self.combined_img4.paste(self.img_swap, (15, 15))
        self.draw4.text((50, 10), "Настройки\nдатчиков", fill="white", font=self.font)
        self.combined_photo4 = ImageTk.PhotoImage(self.combined_img4)

        self.combined_img5 = Image.new("RGB", (200, 60), "black")
        self.draw5 = ImageDraw.Draw(self.combined_img5)
        self.combined_img5.paste(self.img_swap, (15, 15))
        self.draw5.text((50, 10), "Параметры\nнасосов общ.", fill="white", font=self.font)
        self.combined_photo5 = ImageTk.PhotoImage(self.combined_img5)

        self.combined_img6 = Image.new("RGB", (200, 60), "black")
        self.draw6 = ImageDraw.Draw(self.combined_img6)
        self.combined_img6.paste(self.img_plusone, (15, 15))
        self.draw6.text((50, 10), "Вкл. доп.\nнасосов", fill="white", font=self.font)
        self.combined_photo6 = ImageTk.PhotoImage(self.combined_img6)

        self.combined_img7 = Image.new("RGB", (200, 60), "black")
        self.draw7 = ImageDraw.Draw(self.combined_img7)
        self.combined_img7.paste(self.img_minusone, (15, 15))
        self.combined_img7.paste(self.img_triangle, (180, 13))
        self.draw7.text((50, 10), "Откл. доп.\nнасосов", fill="white", font=self.font)
        self.combined_photo7 = ImageTk.PhotoImage(self.combined_img7)

        self.combined_img8 = Image.new("RGB", (200, 60), "black")
        self.draw8 = ImageDraw.Draw(self.combined_img8)
        self.combined_img8.paste(self.img_options, (15, 15))
        self.draw8.text((50, 20), "Опции", fill="white", font=self.font)
        self.combined_photo8 = ImageTk.PhotoImage(self.combined_img8)

        self.combined_img9 = Image.new("RGB", (200, 60), "black")
        self.draw9 = ImageDraw.Draw(self.combined_img9)
        self.combined_img9.paste(self.img_emergency, (15, 15))
        self.draw9.text((50, 10), "Аварийные\nрежимы", fill="white", font=self.font)
        self.combined_photo9 = ImageTk.PhotoImage(self.combined_img9)

        button = tk.Button(self, image=self.combined_photo1, bg='black', relief="groove", activebackground="black",
                           command=lambda: controller.show_frame("Frame1_1"))
        button.place(x=0, y=0, width=200, height=60)
        button2 = tk.Button(self, image=self.combined_photo2, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame2"))
        button2.place(x=0, y=60, width=200, height=52.5)
        button3 = tk.Button(self, image=self.combined_photo3, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame9"))
        button3.place(x=0, y=112.5, width=200, height=52.5)
        button4 = tk.Button(self, image=self.combined_photo4, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame10"))
        button4.place(x=0, y=165, width=200, height=52.5)
        button5 = tk.Button(self, image=self.combined_photo5, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame11"))
        button5.place(x=0, y=217.5, width=200, height=52.5)
        button6 = tk.Button(self, image=self.combined_photo6, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame12"))
        button6.place(x=0, y=270, width=200, height=52.5)
        button7 = tk.Button(self, image=self.combined_photo7, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame13"))
        button7.place(x=0, y=322.5, width=200, height=52.5)
        button8 = tk.Button(self, image=self.combined_photo8, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame14"))
        button8.place(x=0, y=375, width=200, height=52.5)
        button9 = tk.Button(self, image=self.combined_photo9, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame15"))
        button9.place(x=0, y=427.5, width=200, height=52.5)

        self.InterfaceScreen_img = PhotoImage(file=r"images\StationSettings\OptionsForTurningOffExtras.png")
        self.InterfaceScreen = self.canvas.create_image(500, 245, image=self.InterfaceScreen_img)

    def update_clock(self, current_time):
        self.clock_label.config(text=current_time)
class Frame14(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='black')

        self.canvas = Canvas(
            self,
            bg="black",
            height=480,
            width=800,
            bd=0,
            highlightthickness=0,
            relief="ridge")
        self.canvas.place(x=0, y=0)

        self.clock_label = tk.Label(self, text="", fg='white', bg='black', font=('Roboto Bold', 12))
        self.clock_label.place(x=680, y=5)

        self.font = ImageFont.truetype("Roboto-Bold.ttf", 18)
        self.img_screen = Image.open(r"new_images\screen.png")
        self.img_left = Image.open(r"new_images\left.png")
        self.img_triangle = Image.open(r"new_images\triangle.png")
        self.img_diode = Image.open(r"new_images\diode.png")
        self.img_swap = Image.open(r"new_images\swap.png")
        self.img_plusone = Image.open(r"new_images\plus_one.png")
        self.img_minusone = Image.open(r"new_images\minus_one.png")
        self.img_options = Image.open(r"new_images\options.png")
        self.img_emergency = Image.open(r"new_images\emergency.png")

        self.combined_img1 = Image.new("RGB", (200, 60), "black")
        self.draw1 = ImageDraw.Draw(self.combined_img1)
        self.combined_img1.paste(self.img_screen, (15, 20))
        self.draw1.text((50, 20), "Главный экран", fill="white", font=self.font)
        self.combined_photo1 = ImageTk.PhotoImage(self.combined_img1)

        self.combined_img2 = Image.new("RGB", (200, 60), "black")
        self.draw2 = ImageDraw.Draw(self.combined_img2)
        self.combined_img2.paste(self.img_left, (15, 20))
        self.draw2.text((50, 20), "Назад", fill="white", font=self.font)
        self.combined_photo2 = ImageTk.PhotoImage(self.combined_img2)

        self.combined_img3 = Image.new("RGB", (200, 60), "black")
        self.draw3 = ImageDraw.Draw(self.combined_img3)
        self.combined_img3.paste(self.img_diode, (10, 15))
        self.draw3.text((50, 10), "Параметры\nдвигателей", fill="white", font=self.font)
        self.combined_photo3 = ImageTk.PhotoImage(self.combined_img3)

        self.combined_img4 = Image.new("RGB", (200, 60), "black")
        self.draw4 = ImageDraw.Draw(self.combined_img4)
        self.combined_img4.paste(self.img_swap, (15, 15))
        self.draw4.text((50, 10), "Настройки\nдатчиков", fill="white", font=self.font)
        self.combined_photo4 = ImageTk.PhotoImage(self.combined_img4)

        self.combined_img5 = Image.new("RGB", (200, 60), "black")
        self.draw5 = ImageDraw.Draw(self.combined_img5)
        self.combined_img5.paste(self.img_swap, (15, 15))
        self.draw5.text((50, 10), "Параметры\nнасосов общ.", fill="white", font=self.font)
        self.combined_photo5 = ImageTk.PhotoImage(self.combined_img5)

        self.combined_img6 = Image.new("RGB", (200, 60), "black")
        self.draw6 = ImageDraw.Draw(self.combined_img6)
        self.combined_img6.paste(self.img_plusone, (15, 15))
        self.draw6.text((50, 10), "Вкл. доп.\nнасосов", fill="white", font=self.font)
        self.combined_photo6 = ImageTk.PhotoImage(self.combined_img6)

        self.combined_img7 = Image.new("RGB", (200, 60), "black")
        self.draw7 = ImageDraw.Draw(self.combined_img7)
        self.combined_img7.paste(self.img_minusone, (15, 15))
        self.draw7.text((50, 10), "Откл. доп.\nнасосов", fill="white", font=self.font)
        self.combined_photo7 = ImageTk.PhotoImage(self.combined_img7)

        self.combined_img8 = Image.new("RGB", (200, 60), "black")
        self.draw8 = ImageDraw.Draw(self.combined_img8)
        self.combined_img8.paste(self.img_options, (15, 15))
        self.combined_img8.paste(self.img_triangle, (180, 13))
        self.draw8.text((50, 20), "Опции", fill="white", font=self.font)
        self.combined_photo8 = ImageTk.PhotoImage(self.combined_img8)

        self.combined_img9 = Image.new("RGB", (200, 60), "black")
        self.draw9 = ImageDraw.Draw(self.combined_img9)
        self.combined_img9.paste(self.img_emergency, (15, 15))
        self.draw9.text((50, 10), "Аварийные\nрежимы", fill="white", font=self.font)
        self.combined_photo9 = ImageTk.PhotoImage(self.combined_img9)

        button = tk.Button(self, image=self.combined_photo1, bg='black', relief="groove", activebackground="black",
                           command=lambda: controller.show_frame("Frame1_1"))
        button.place(x=0, y=0, width=200, height=60)
        button2 = tk.Button(self, image=self.combined_photo2, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame2"))
        button2.place(x=0, y=60, width=200, height=52.5)
        button3 = tk.Button(self, image=self.combined_photo3, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame9"))
        button3.place(x=0, y=112.5, width=200, height=52.5)
        button4 = tk.Button(self, image=self.combined_photo4, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame10"))
        button4.place(x=0, y=165, width=200, height=52.5)
        button5 = tk.Button(self, image=self.combined_photo5, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame11"))
        button5.place(x=0, y=217.5, width=200, height=52.5)
        button6 = tk.Button(self, image=self.combined_photo6, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame12"))
        button6.place(x=0, y=270, width=200, height=52.5)
        button7 = tk.Button(self, image=self.combined_photo7, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame13"))
        button7.place(x=0, y=322.5, width=200, height=52.5)
        button8 = tk.Button(self, image=self.combined_photo8, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame14"))
        button8.place(x=0, y=375, width=200, height=52.5)
        button9 = tk.Button(self, image=self.combined_photo9, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame15"))
        button9.place(x=0, y=427.5, width=200, height=52.5)

        self.InterfaceScreen_img = PhotoImage(file=r"images\StationSettings\Options.png")
        self.InterfaceScreen = self.canvas.create_image(500, 245, image=self.InterfaceScreen_img)
        self.Switch_Flat_img = PhotoImage(file=r"images\StationSettings\Switch-0.png")
        self.Switch_Flat_button = self.canvas.create_image(670, 78, image=self.Switch_Flat_img)
        self.canvas.tag_bind(self.Switch_Flat_button, "<Button-1>", self.update_switch)

    def update_switch(self, event):
        if self.Switch_Flat_img.cget("file") == "images\StationSettings\Switch-0.png":
            self.Switch_Flat_img = PhotoImage(file=r"images\StationSettings\Switch-1.png")
        elif self.Switch_Flat_img.cget("file") == "images\StationSettings\Switch-1.png":
            self.Switch_Flat_img = PhotoImage(file=r"images\StationSettings\Switch-0.png")
        self.Switch_Flat_button = self.canvas.create_image(670, 78, image=self.Switch_Flat_img)
        self.canvas.tag_bind(self.Switch_Flat_button, "<Button-1>", self.update_switch)

    def update_clock(self, current_time):
        self.clock_label.config(text=current_time)

class Frame15(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='black')

        self.canvas = Canvas(
            self,
            bg="black",
            height=480,
            width=800,
            bd=0,
            highlightthickness=0,
            relief="ridge")
        self.canvas.place(x=0, y=0)
        self.clock_label = tk.Label(self, text="", fg='white', bg='black', font=('Roboto Bold', 12))
        self.clock_label.place(x=680, y=5)

        self.font = ImageFont.truetype("Roboto-Bold.ttf", 18)
        self.img_screen = Image.open(r"new_images\screen.png")
        self.img_left = Image.open(r"new_images\left.png")
        self.img_triangle = Image.open(r"new_images\triangle.png")
        self.img_diode = Image.open(r"new_images\diode.png")
        self.img_swap = Image.open(r"new_images\swap.png")
        self.img_plusone = Image.open(r"new_images\plus_one.png")
        self.img_minusone = Image.open(r"new_images\minus_one.png")
        self.img_options = Image.open(r"new_images\options.png")
        self.img_emergency = Image.open(r"new_images\emergency.png")

        self.combined_img1 = Image.new("RGB", (200, 60), "black")
        self.draw1 = ImageDraw.Draw(self.combined_img1)
        self.combined_img1.paste(self.img_screen, (15, 20))
        self.draw1.text((50, 20), "Главный экран", fill="white", font=self.font)
        self.combined_photo1 = ImageTk.PhotoImage(self.combined_img1)

        self.combined_img2 = Image.new("RGB", (200, 60), "black")
        self.draw2 = ImageDraw.Draw(self.combined_img2)
        self.combined_img2.paste(self.img_left, (15, 20))
        self.draw2.text((50, 20), "Назад", fill="white", font=self.font)
        self.combined_photo2 = ImageTk.PhotoImage(self.combined_img2)

        self.combined_img3 = Image.new("RGB", (200, 60), "black")
        self.draw3 = ImageDraw.Draw(self.combined_img3)
        self.combined_img3.paste(self.img_diode, (10, 15))
        self.draw3.text((50, 10), "Параметры\nдвигателей", fill="white", font=self.font)
        self.combined_photo3 = ImageTk.PhotoImage(self.combined_img3)

        self.combined_img4 = Image.new("RGB", (200, 60), "black")
        self.draw4 = ImageDraw.Draw(self.combined_img4)
        self.combined_img4.paste(self.img_swap, (15, 15))
        self.draw4.text((50, 10), "Настройки\nдатчиков", fill="white", font=self.font)
        self.combined_photo4 = ImageTk.PhotoImage(self.combined_img4)

        self.combined_img5 = Image.new("RGB", (200, 60), "black")
        self.draw5 = ImageDraw.Draw(self.combined_img5)
        self.combined_img5.paste(self.img_swap, (15, 15))
        self.draw5.text((50, 10), "Параметры\nнасосов общ.", fill="white", font=self.font)
        self.combined_photo5 = ImageTk.PhotoImage(self.combined_img5)

        self.combined_img6 = Image.new("RGB", (200, 60), "black")
        self.draw6 = ImageDraw.Draw(self.combined_img6)
        self.combined_img6.paste(self.img_plusone, (15, 15))
        self.draw6.text((50, 10), "Вкл. доп.\nнасосов", fill="white", font=self.font)
        self.combined_photo6 = ImageTk.PhotoImage(self.combined_img6)

        self.combined_img7 = Image.new("RGB", (200, 60), "black")
        self.draw7 = ImageDraw.Draw(self.combined_img7)
        self.combined_img7.paste(self.img_minusone, (15, 15))
        self.draw7.text((50, 10), "Откл. доп.\nнасосов", fill="white", font=self.font)
        self.combined_photo7 = ImageTk.PhotoImage(self.combined_img7)

        self.combined_img8 = Image.new("RGB", (200, 60), "black")
        self.draw8 = ImageDraw.Draw(self.combined_img8)
        self.combined_img8.paste(self.img_options, (15, 15))
        self.draw8.text((50, 20), "Опции", fill="white", font=self.font)
        self.combined_photo8 = ImageTk.PhotoImage(self.combined_img8)

        self.combined_img9 = Image.new("RGB", (200, 60), "black")
        self.draw9 = ImageDraw.Draw(self.combined_img9)
        self.combined_img9.paste(self.img_emergency, (15, 15))
        self.combined_img9.paste(self.img_triangle, (180, 13))
        self.draw9.text((50, 10), "Аварийные\nрежимы", fill="white", font=self.font)
        self.combined_photo9 = ImageTk.PhotoImage(self.combined_img9)

        button = tk.Button(self, image=self.combined_photo1, bg='black', relief="groove", activebackground="black",
                           command=lambda: controller.show_frame("Frame1_1"))
        button.place(x=0, y=0, width=200, height=60)
        button2 = tk.Button(self, image=self.combined_photo2, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame2"))
        button2.place(x=0, y=60, width=200, height=52.5)
        button3 = tk.Button(self, image=self.combined_photo3, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame9"))
        button3.place(x=0, y=112.5, width=200, height=52.5)
        button4 = tk.Button(self, image=self.combined_photo4, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame10"))
        button4.place(x=0, y=165, width=200, height=52.5)
        button5 = tk.Button(self, image=self.combined_photo5, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame11"))
        button5.place(x=0, y=217.5, width=200, height=52.5)
        button6 = tk.Button(self, image=self.combined_photo6, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame12"))
        button6.place(x=0, y=270, width=200, height=52.5)
        button7 = tk.Button(self, image=self.combined_photo7, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame13"))
        button7.place(x=0, y=322.5, width=200, height=52.5)
        button8 = tk.Button(self, image=self.combined_photo8, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame14"))
        button8.place(x=0, y=375, width=200, height=52.5)
        button9 = tk.Button(self, image=self.combined_photo9, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame15"))
        button9.place(x=0, y=427.5, width=200, height=52.5)

        self.EmergencyModes_img = PhotoImage(file=r"images\StationSettings\EmergencyModes1_1.png")
        self.EmergencyModes_button = self.canvas.create_image(100, 419.4 + 30, image=self.EmergencyModes_img)

        self.InterfaceScreen_img = PhotoImage(file=r"images\StationSettings\EmergencyModes.png")
        self.InterfaceScreen = self.canvas.create_image(500, 245, image=self.InterfaceScreen_img)
        self.Switch_Flat_img = PhotoImage(file=r"images\StationSettings\_NO_YES.png")
        self.Switch_Flat_button = self.canvas.create_image(670, 440, image=self.Switch_Flat_img)
        self.canvas.tag_bind(self.Switch_Flat_button, "<Button-1>", self.update_switch)

    def update_switch(self, event):
        if self.Switch_Flat_img.cget("file") == "images\StationSettings\_NO_YES.png":
            self.Switch_Flat_img = PhotoImage(file=r"images\StationSettings\_YES_NO.png")
        elif self.Switch_Flat_img.cget("file") == "images\StationSettings\_YES_NO.png":
            self.Switch_Flat_img = PhotoImage(file=r"images\StationSettings\_NO_YES.png")
        self.Switch_Flat_button = self.canvas.create_image(670, 440, image=self.Switch_Flat_img)
        self.canvas.tag_bind(self.Switch_Flat_button, "<Button-1>", self.update_switch)

    def update_clock(self, current_time):
        self.clock_label.config(text=current_time)

class Frame16(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='black')

        self.canvas = Canvas(
            self,
            bg="black",
            height=480,
            width=800,
            bd=0,
            highlightthickness=0,
            relief="ridge")
        self.canvas.place(x=0, y=0)
        self.clock_label = tk.Label(self, text="", fg='white', bg='black', font=('Roboto Bold', 12))
        self.clock_label.place(x=680, y=5)

        self.font = ImageFont.truetype("Roboto-Bold.ttf", 18)
        self.img_screen = Image.open(r"new_images\screen.png")
        self.img_peak = Image.open(r"new_images\peak.png")
        self.img_timer = Image.open(r"new_images\timer.png")
        self.img_right = Image.open(r"new_images\right.png")
        self.img_left = Image.open(r"new_images\left.png")
        self.img_triangle = Image.open(r"new_images\triangle.png")

        self.combined_img1 = Image.new("RGB", (200, 60), "black")
        self.draw1 = ImageDraw.Draw(self.combined_img1)
        self.combined_img1.paste(self.img_screen, (15, 20))
        self.draw1.text((50, 20), "Главный экран", fill="white", font=self.font)
        self.combined_photo1 = ImageTk.PhotoImage(self.combined_img1)

        self.combined_img2 = Image.new("RGB", (200, 60), "black")
        self.draw2 = ImageDraw.Draw(self.combined_img2)
        self.combined_img2.paste(self.img_left, (15, 20))
        self.draw2.text((50, 20), "Назад", fill="white", font=self.font)
        self.combined_photo2 = ImageTk.PhotoImage(self.combined_img2)

        self.combined_img3 = Image.new("RGB", (200, 60), "black")
        self.draw3 = ImageDraw.Draw(self.combined_img3)
        self.combined_img3.paste(self.img_peak, (10, 15))
        self.combined_img3.paste(self.img_triangle, (180, 13))
        self.draw3.text((50, 10), "Настройки\nПИД-рег.", fill="white", font=self.font)
        self.combined_photo3 = ImageTk.PhotoImage(self.combined_img3)

        self.combined_img4 = Image.new("RGB", (200, 60), "black")
        self.draw4 = ImageDraw.Draw(self.combined_img4)
        self.draw4.text((50, 20), "PLC", fill="white", font=self.font)
        self.combined_photo4 = ImageTk.PhotoImage(self.combined_img4)

        self.combined_img5 = Image.new("RGB", (200, 60), "black")
        self.draw5 = ImageDraw.Draw(self.combined_img5)
        self.draw5.text((50, 20), "Бэкап", fill="white", font=self.font)
        self.combined_photo5 = ImageTk.PhotoImage(self.combined_img5)

        button = tk.Button(self, image=self.combined_photo1, bg='black', relief="groove", activebackground="black",
                           command=lambda: controller.show_frame("Frame1_1"))
        button.place(x=0, y=0, width=200, height=60)
        button2 = tk.Button(self, image=self.combined_photo2, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame2"))
        button2.place(x=0, y=60, width=200, height=60)
        button3 = tk.Button(self, image=self.combined_photo3, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame16"))
        button3.place(x=0, y=120, width=200, height=60)
        button4 = tk.Button(self, image=self.combined_photo4, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame17"))
        button4.place(x=0, y=180, width=200, height=60)
        button5 = tk.Button(self, image=self.combined_photo5, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame18"))
        button5.place(x=0, y=240, width=200, height=60)


        self.InterfaceScreen_img = PhotoImage(file=r"images\PanelSettings\Settings.png")
        self.InterfaceScreen = self.canvas.create_image(490, 230, image=self.InterfaceScreen_img)
        self.Switch_Flat_img = PhotoImage(file=r"images\PanelSettings\Switch-0.png")
        self.Switch_Flat_button = self.canvas.create_image(659, 203, image=self.Switch_Flat_img)
        self.canvas.tag_bind(self.Switch_Flat_button, "<Button-1>", self.update_switch)

    def update_switch(self, event):
        if self.Switch_Flat_img.cget("file") == "images\PanelSettings\Switch-0.png":
            self.Switch_Flat_img = PhotoImage(file=r"images\PanelSettings\Switch-1.png")
        elif self.Switch_Flat_img.cget("file") == "images\PanelSettings\Switch-1.png":
            self.Switch_Flat_img = PhotoImage(file=r"images\PanelSettings\Switch-0.png")
        self.Switch_Flat_button = self.canvas.create_image(659, 203, image=self.Switch_Flat_img)
        self.canvas.tag_bind(self.Switch_Flat_button, "<Button-1>", self.update_switch)

    def update_clock(self, current_time):
        self.clock_label.config(text=current_time)

class Frame17(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='black')

        self.canvas = Canvas(
            self,
            bg="black",
            height=480,
            width=800,
            bd=0,
            highlightthickness=0,
            relief="ridge")
        self.canvas.place(x=0, y=0)

        self.clock_label = tk.Label(self, text="", fg='white', bg='black', font=('Roboto Bold', 12), )

        self.font = ImageFont.truetype("Roboto-Bold.ttf", 18)
        self.img_screen = Image.open(r"new_images\screen.png")
        self.img_peak = Image.open(r"new_images\peak.png")
        self.img_timer = Image.open(r"new_images\timer.png")
        self.img_right = Image.open(r"new_images\right.png")
        self.img_left = Image.open(r"new_images\left.png")
        self.img_triangle = Image.open(r"new_images\triangle.png")

        self.combined_img1 = Image.new("RGB", (200, 60), "black")
        self.draw1 = ImageDraw.Draw(self.combined_img1)
        self.combined_img1.paste(self.img_screen, (15, 20))
        self.draw1.text((50, 20), "Главный экран", fill="white", font=self.font)
        self.combined_photo1 = ImageTk.PhotoImage(self.combined_img1)

        self.combined_img2 = Image.new("RGB", (200, 60), "black")
        self.draw2 = ImageDraw.Draw(self.combined_img2)
        self.combined_img2.paste(self.img_left, (15, 20))
        self.draw2.text((50, 20), "Назад", fill="white", font=self.font)
        self.combined_photo2 = ImageTk.PhotoImage(self.combined_img2)

        self.combined_img3 = Image.new("RGB", (200, 60), "black")
        self.draw3 = ImageDraw.Draw(self.combined_img3)
        self.combined_img3.paste(self.img_peak, (10, 15))
        self.draw3.text((50, 10), "Настройки\nПИД-рег.", fill="white", font=self.font)
        self.combined_photo3 = ImageTk.PhotoImage(self.combined_img3)

        self.combined_img4 = Image.new("RGB", (200, 60), "black")
        self.draw4 = ImageDraw.Draw(self.combined_img4)
        self.combined_img4.paste(self.img_triangle, (180, 13))
        self.draw4.text((50, 20), "PLC", fill="white", font=self.font)
        self.combined_photo4 = ImageTk.PhotoImage(self.combined_img4)

        self.combined_img5 = Image.new("RGB", (200, 60), "black")
        self.draw5 = ImageDraw.Draw(self.combined_img5)
        self.draw5.text((50, 20), "Бэкап", fill="white", font=self.font)
        self.combined_photo5 = ImageTk.PhotoImage(self.combined_img5)

        button = tk.Button(self, image=self.combined_photo1, bg='black', relief="groove", activebackground="black",
                           command=lambda: controller.show_frame("Frame1_1"))
        button.place(x=0, y=0, width=200, height=60)
        button2 = tk.Button(self, image=self.combined_photo2, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame2"))
        button2.place(x=0, y=60, width=200, height=60)
        button3 = tk.Button(self, image=self.combined_photo3, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame16"))
        button3.place(x=0, y=120, width=200, height=60)
        button4 = tk.Button(self, image=self.combined_photo4, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame17"))
        button4.place(x=0, y=180, width=200, height=60)
        button5 = tk.Button(self, image=self.combined_photo5, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame18"))
        button5.place(x=0, y=240, width=200, height=60)

        self.InterfaceScreen_img = PhotoImage(file=r"images\PanelSettings\PLC.png")
        self.InterfaceScreen = self.canvas.create_image(500, 230, image=self.InterfaceScreen_img)

        self.switch_btn_di1_img = PhotoImage(file=r"images\PanelSettings\Switch1-0.png")
        self.switch_btn_di1_button = self.canvas.create_image(269, 97, image=self.switch_btn_di1_img)
        self.switch_btn_di2_img = PhotoImage(file=r"images\PanelSettings\Switch1-0.png")
        self.switch_btn_di2_button = self.canvas.create_image(295, 97, image=self.switch_btn_di2_img)
        self.switch_btn_di3_img = PhotoImage(file=r"images\PanelSettings\Switch1-0.png")
        self.switch_btn_di3_button = self.canvas.create_image(321, 97, image=self.switch_btn_di3_img)
        self.switch_btn_di4_img = PhotoImage(file=r"images\PanelSettings\Switch1-0.png")
        self.switch_btn_di4_button = self.canvas.create_image(350, 97, image=self.switch_btn_di4_img)
        self.switch_btn_di5_img = PhotoImage(file=r"images\PanelSettings\Switch1-0.png")
        self.switch_btn_di5_button = self.canvas.create_image(377, 97, image=self.switch_btn_di5_img)
        self.switch_btn_di6_img = PhotoImage(file=r"images\PanelSettings\Switch1-0.png")
        self.switch_btn_di6_button = self.canvas.create_image(404, 97, image=self.switch_btn_di6_img)
        self.switch_btn_di7_img = PhotoImage(file=r"images\PanelSettings\Switch1-0.png")
        self.switch_btn_di7_button = self.canvas.create_image(432, 97, image=self.switch_btn_di7_img)
        self.switch_btn_di8_img = PhotoImage(file=r"images\PanelSettings\Switch1-0.png")
        self.switch_btn_di8_button = self.canvas.create_image(458, 97, image=self.switch_btn_di8_img)
        self.switch_btn_di9_img = PhotoImage(file=r"images\PanelSettings\Switch1-0.png")
        self.switch_btn_di9_button = self.canvas.create_image(487, 97, image=self.switch_btn_di9_img)
        self.switch_btn_di10_img = PhotoImage(file=r"images\PanelSettings\Switch1-0.png")
        self.switch_btn_di10_button = self.canvas.create_image(514, 97, image=self.switch_btn_di10_img)
        self.switch_btn_di11_img = PhotoImage(file=r"images\PanelSettings\Switch1-0.png")
        self.switch_btn_di11_button = self.canvas.create_image(541, 97, image=self.switch_btn_di11_img)
        self.switch_btn_di12_img = PhotoImage(file=r"images\PanelSettings\Switch1-0.png")
        self.switch_btn_di12_button = self.canvas.create_image(568, 97, image=self.switch_btn_di12_img)
        self.switch_btn_rs485_img = PhotoImage(file=r"images\PanelSettings\Switch2-0.png")
        self.switch_btn_rs485_button = self.canvas.create_image(719, 97, image=self.switch_btn_rs485_img)

        self.switch_btn_dq1_img = PhotoImage(file=r"images\PanelSettings\Switch1-0.png")
        self.switch_btn_dq1_button = self.canvas.create_image(269.5, 249, image=self.switch_btn_dq1_img)
        self.switch_btn_dq2_img = PhotoImage(file=r"images\PanelSettings\Switch1-0.png")
        self.switch_btn_dq2_button = self.canvas.create_image(296.5, 249, image=self.switch_btn_dq2_img)
        self.switch_btn_dq3_img = PhotoImage(file=r"images\PanelSettings\Switch1-0.png")
        self.switch_btn_dq3_button = self.canvas.create_image(323.5, 249, image=self.switch_btn_dq3_img)
        self.switch_btn_dq4_img = PhotoImage(file=r"images\PanelSettings\Switch1-0.png")
        self.switch_btn_dq4_button = self.canvas.create_image(352.5, 249, image=self.switch_btn_dq4_img)
        self.switch_btn_dq5_img = PhotoImage(file=r"images\PanelSettings\Switch1-0.png")
        self.switch_btn_dq5_button = self.canvas.create_image(378.5, 249, image=self.switch_btn_dq5_img)
        self.switch_btn_dq6_img = PhotoImage(file=r"images\PanelSettings\Switch1-0.png")
        self.switch_btn_dq6_button = self.canvas.create_image(406, 249, image=self.switch_btn_dq6_img)
        self.switch_btn_dq7_img = PhotoImage(file=r"images\PanelSettings\Switch1-0.png")
        self.switch_btn_dq7_button = self.canvas.create_image(434, 249, image=self.switch_btn_dq7_img)
        self.switch_btn_dq8_img = PhotoImage(file=r"images\PanelSettings\Switch1-0.png")
        self.switch_btn_dq8_button = self.canvas.create_image(460, 249, image=self.switch_btn_dq8_img)
        self.switch_btn_dq9_img = PhotoImage(file=r"images\PanelSettings\Switch1-0.png")
        self.switch_btn_dq9_button = self.canvas.create_image(488, 249, image=self.switch_btn_dq9_img)
        self.switch_btn_dq10_img = PhotoImage(file=r"images\PanelSettings\Switch1-0.png")
        self.switch_btn_dq10_button = self.canvas.create_image(515, 249, image=self.switch_btn_dq10_img)
        self.switch_btn_dq11_img = PhotoImage(file=r"images\PanelSettings\Switch1-0.png")
        self.switch_btn_dq11_button = self.canvas.create_image(542, 249, image=self.switch_btn_dq11_img)
        self.switch_btn_dq12_img = PhotoImage(file=r"images\PanelSettings\Switch1-0.png")
        self.switch_btn_dq12_button = self.canvas.create_image(571, 249, image=self.switch_btn_dq12_img)
        self.switch_btn_aq1_img = PhotoImage(file=r"images\PanelSettings\Switch1-0.png")
        self.switch_btn_aq1_button = self.canvas.create_image(601, 249, image=self.switch_btn_aq1_img)
        self.switch_btn_ai1_img = PhotoImage(file=r"images\PanelSettings\Switch1-0.png")
        self.switch_btn_ai1_button = self.canvas.create_image(625, 249, image=self.switch_btn_ai1_img)
        self.switch_btn_ai2_img = PhotoImage(file=r"images\PanelSettings\Switch1-0.png")
        self.switch_btn_ai2_button = self.canvas.create_image(650.5, 249, image=self.switch_btn_ai2_img)
        self.switch_btn_ai3_img = PhotoImage(file=r"images\PanelSettings\Switch1-0.png")
        self.switch_btn_ai3_button = self.canvas.create_image(677.5, 249, image=self.switch_btn_ai3_img)
        self.switch_btn_ai4_img = PhotoImage(file=r"images\PanelSettings\Switch1-0.png")
        self.switch_btn_ai4_button = self.canvas.create_image(705, 249, image=self.switch_btn_ai4_img)
        self.switch_btn_ai5_img = PhotoImage(file=r"images\PanelSettings\Switch1-0.png")
        self.switch_btn_ai5_button = self.canvas.create_image(729, 249, image=self.switch_btn_ai5_img)

    def update_clock(self, current_time):
        self.clock_label.config(text=current_time)

class Frame18(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='black')

        self.canvas = Canvas(
            self,
            bg="black",
            height=480,
            width=800,
            bd=0,
            highlightthickness=0,
            relief="ridge")
        self.canvas.place(x=0, y=0)
        self.clock_label = tk.Label(self, text="", fg='white', bg='black', font=('Roboto Bold', 12))
        self.clock_label.place(x=680, y=5)

        self.font = ImageFont.truetype("Roboto-Bold.ttf", 18)
        self.img_screen = Image.open(r"new_images\screen.png")
        self.img_peak = Image.open(r"new_images\peak.png")
        self.img_timer = Image.open(r"new_images\timer.png")
        self.img_right = Image.open(r"new_images\right.png")
        self.img_left = Image.open(r"new_images\left.png")
        self.img_triangle = Image.open(r"new_images\triangle.png")

        self.combined_img1 = Image.new("RGB", (200, 60), "black")
        self.draw1 = ImageDraw.Draw(self.combined_img1)
        self.combined_img1.paste(self.img_screen, (15, 20))
        self.draw1.text((50, 20), "Главный экран", fill="white", font=self.font)
        self.combined_photo1 = ImageTk.PhotoImage(self.combined_img1)

        self.combined_img2 = Image.new("RGB", (200, 60), "black")
        self.draw2 = ImageDraw.Draw(self.combined_img2)
        self.combined_img2.paste(self.img_left, (15, 20))
        self.draw2.text((50, 20), "Назад", fill="white", font=self.font)
        self.combined_photo2 = ImageTk.PhotoImage(self.combined_img2)

        self.combined_img3 = Image.new("RGB", (200, 60), "black")
        self.draw3 = ImageDraw.Draw(self.combined_img3)
        self.combined_img3.paste(self.img_peak, (10, 15))
        self.draw3.text((50, 10), "Настройки\nПИД-рег.", fill="white", font=self.font)
        self.combined_photo3 = ImageTk.PhotoImage(self.combined_img3)

        self.combined_img4 = Image.new("RGB", (200, 60), "black")
        self.draw4 = ImageDraw.Draw(self.combined_img4)
        self.draw4.text((50, 20), "PLC", fill="white", font=self.font)
        self.combined_photo4 = ImageTk.PhotoImage(self.combined_img4)

        self.combined_img5 = Image.new("RGB", (200, 60), "black")
        self.draw5 = ImageDraw.Draw(self.combined_img5)
        self.combined_img5.paste(self.img_triangle, (180, 13))
        self.draw5.text((50, 20), "Бэкап", fill="white", font=self.font)
        self.combined_photo5 = ImageTk.PhotoImage(self.combined_img5)

        button = tk.Button(self, image=self.combined_photo1, bg='black', relief="groove", activebackground="black",
                           command=lambda: controller.show_frame("Frame1_1"))
        button.place(x=0, y=0, width=200, height=60)
        button2 = tk.Button(self, image=self.combined_photo2, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame2"))
        button2.place(x=0, y=60, width=200, height=60)
        button3 = tk.Button(self, image=self.combined_photo3, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame16"))
        button3.place(x=0, y=120, width=200, height=60)
        button4 = tk.Button(self, image=self.combined_photo4, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame17"))
        button4.place(x=0, y=180, width=200, height=60)
        button5 = tk.Button(self, image=self.combined_photo5, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame18"))
        button5.place(x=0, y=240, width=200, height=60)

        self.InterfaceScreen_img = PhotoImage(file=r"images\PanelSettings\Bek.png")
        self.InterfaceScreen = self.canvas.create_image(500, 230, image=self.InterfaceScreen_img)
        self.Switch_Flat_img = PhotoImage(file=r"images\PanelSettings\Switch-0.png")
        self.Switch_Flat_button = self.canvas.create_image(670, 152, image=self.Switch_Flat_img)
        self.canvas.tag_bind(self.Switch_Flat_button, "<Button-1>", self.update_switch)

        self.ip_ = NetInfo().ipv4
        self.result_IP = self.ip_.split(".")

        self.net_if_addrs = psutil.net_if_addrs()

        for interface, addresses in self.net_if_addrs.items():
            for address in addresses:
                if address.family == 2:
                    if address.address == self.ip_:
                        self.result_netmask = address.netmask

        self.result_netmask_split = self.result_netmask.split(".")

        if (len(self.result_netmask_split[0]) == 1):
            self.netmask_1 = tk.Label(self.canvas, text=f"{self.result_netmask_split[0]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.netmask_1.place(x=418, y=335)
        elif (len(self.result_netmask_split[0]) == 2):
            self.netmask_1 = tk.Label(self.canvas, text=f"{self.result_netmask_split[0]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.netmask_1.place(x=414, y=335)
        elif (len(self.result_netmask_split[0]) == 3):
            self.netmask_1 = tk.Label(self.canvas, text=f"{self.result_netmask_split[0]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.netmask_1.place(x=410, y=335)
        if (len(self.result_netmask_split[1]) == 1):
            self.netmask_1 = tk.Label(self.canvas, text=f"{self.result_netmask_split[1]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.netmask_1.place(x=520, y=335)
        elif (len(self.result_netmask_split[1]) == 2):
            self.netmask_1 = tk.Label(self.canvas, text=f"{self.result_netmask_split[1]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.netmask_1.place(x=516, y=335)
        elif (len(self.result_netmask_split[1]) == 3):
            self.netmask_1 = tk.Label(self.canvas, text=f"{self.result_netmask_split[1]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.netmask_1.place(x=512, y=335)
        if (len(self.result_netmask_split[2]) == 1):
            self.netmask_1 = tk.Label(self.canvas, text=f"{self.result_netmask_split[2]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.netmask_1.place(x=622, y=335)
        elif (len(self.result_netmask_split[2]) == 2):
            self.netmask_1 = tk.Label(self.canvas, text=f"{self.result_netmask_split[2]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.netmask_1.place(x=617, y=335)
        elif (len(self.result_netmask_split[2]) == 3):
            self.netmask_1 = tk.Label(self.canvas, text=f"{self.result_netmask_split[2]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.netmask_1.place(x=614, y=335)
        if (len(self.result_netmask_split[3]) == 1):
            self.netmask_1 = tk.Label(self.canvas, text=f"{self.result_netmask_split[3]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.netmask_1.place(x=724, y=335)
        elif (len(self.result_netmask_split[3]) == 2):
            self.netmask_1 = tk.Label(self.canvas, text=f"{self.result_netmask_split[3]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.netmask_1.place(x=720, y=335)
        elif (len(self.result_netmask_split[3]) == 3):
            self.netmask_1 = tk.Label(self.canvas, text=f"{self.result_netmask_split[3]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.netmask_1.place(x=717, y=335)

        self.time_display_1 = tk.Label(self.canvas, text="**", fg='white', bg='black', font=('Roboto Bold', 12))
        self.time_display_1.place(x=645, y=63)
        self.time_display_2 = tk.Label(self.canvas, text="**", fg='white', bg='black', font=('Roboto Bold', 12))
        self.time_display_2.place(x=645, y=103)

        def show_data_and_time():
            now = datetime.now()
            self.show_day.config(text=now.strftime("%d"))
            self.show_month.config(text=now.strftime("%m"))
            self.show_year.config(text=now.strftime("%Y"))
            self.show_hour.config(text=now.strftime("%H"))
            self.show_minute.config(text=now.strftime("%M"))
            self.show_second.config(text=now.strftime("%S"))
            self.canvas.after(100, show_data_and_time)

        wmi_obj = wmi.WMI()
        wmi_sql = "select IPAddress,DefaultIPGateway from Win32_NetworkAdapterConfiguration where IPEnabled=TRUE"
        self.wmi_out = wmi_obj.query(wmi_sql)

        self.show_hour = tk.Label(self.canvas, text="", fg='white', bg='black', font=('Roboto Bold', 12))
        self.show_hour.place(x=480, y=234)
        self.show_minute = tk.Label(self.canvas, text="", fg='white', bg='black', font=('Roboto Bold', 12))
        self.show_minute.place(x=584, y=234)
        self.show_second = tk.Label(self.canvas, text="", fg='white', bg='black', font=('Roboto Bold', 12))
        self.show_second.place(x=684, y=234)
        self.show_day = tk.Label(self.canvas, text="", fg='white', bg='black', font=('Roboto Bold', 12))
        self.show_day.place(x=480, y=195)
        self.show_month = tk.Label(self.canvas, text="", fg='white', bg='black', font=('Roboto Bold', 12))
        self.show_month.place(x=584, y=195)
        self.show_year = tk.Label(self.canvas, text="", fg='white', bg='black', font=('Roboto Bold', 12))
        self.show_year.place(x=684, y=195)

        show_data_and_time()

        self.result_IP = self.ip_.split(".")

        if (len(self.result_IP[0]) == 1):
            self.IP_1 = tk.Label(self.canvas, text=f"{self.result_IP[0]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.IP_1.place(x=418, y=294)
        elif (len(self.result_IP[0]) == 2):
            self.IP_1 = tk.Label(self.canvas, text=f"{self.result_IP[0]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.IP_1.place(x=414, y=294)
        elif (len(self.result_IP[0]) == 3):
            self.IP_1 = tk.Label(self.canvas, text=f"{self.result_IP[0]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.IP_1.place(x=410, y=294)
        if (len(self.result_IP[1]) == 1):
            self.IP_2 = tk.Label(self.canvas, text=f"{self.result_IP[1]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.IP_2.place(x=520, y=294)
        elif (len(self.result_IP[1]) == 2):
            self.IP_2 = tk.Label(self.canvas, text=f"{self.result_IP[1]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.IP_2.place(x=516, y=294)
        elif (len(self.result_IP[1]) == 3):
            self.IP_2 = tk.Label(self.canvas, text=f"{self.result_IP[1]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.IP_2.place(x=512, y=294)
        if (len(self.result_IP[2]) == 1):
            self.IP_3 = tk.Label(self.canvas, text=f"{self.result_IP[2]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.IP_3.place(x=622, y=294)
        elif (len(self.result_IP[2]) == 2):
            self.IP_3 = tk.Label(self.canvas, text=f"{self.result_IP[2]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.IP_3.place(x=617, y=294)
        elif (len(self.result_IP[2]) == 3):
            self.IP_3 = tk.Label(self.canvas, text=f"{self.result_IP[2]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.IP_3.place(x=614, y=294)
        if (len(self.result_IP[3]) == 1):
            self.IP_4 = tk.Label(self.canvas, text=f"{self.result_IP[3]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.IP_4.place(x=724, y=294)
        elif (len(self.result_IP[3]) == 2):
            self.IP_4 = tk.Label(self.canvas, text=f"{self.result_IP[3]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.IP_4.place(x=720, y=294)
        elif (len(self.result_IP[3]) == 3):
            self.IP_4 = tk.Label(self.canvas, text=f"{self.result_IP[3]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.IP_4.place(x=717, y=294)

        for dev in self.wmi_out:
            self.result_gateway = dev.DefaultIPGateway[0]
        self.result_gateway_split = self.result_gateway.split(".")

        if (len(self.result_gateway_split[0]) == 1):
            self.gateway_1 = tk.Label(self.canvas, text=f"{self.result_gateway_split[0]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.gateway_1.place(x=418, y=374)
        elif (len(self.result_gateway_split[0]) == 2):
            self.gateway_1 = tk.Label(self.canvas, text=f"{self.result_gateway_split[0]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.gateway_1.place(x=414, y=374)
        elif (len(self.result_gateway_split[0]) == 3):
            self.gateway_1 = tk.Label(self.canvas, text=f"{self.result_gateway_split[0]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.gateway_1.place(x=410, y=374)
        if (len(self.result_gateway_split[1]) == 1):
            self.gateway_2 = tk.Label(self.canvas, text=f"{self.result_gateway_split[1]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.gateway_2.place(x=520, y=374)
        elif (len(self.result_gateway_split[1]) == 2):
            self.gateway_2 = tk.Label(self.canvas, text=f"{self.result_gateway_split[1]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.gateway_2.place(x=516, y=374)
        elif (len(self.result_gateway_split[1]) == 3):
            self.gateway_2 = tk.Label(self.canvas, text=f"{self.result_gateway_split[1]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.gateway_2.place(x=512, y=374)
        if (len(self.result_gateway_split[2]) == 1):
            self.gateway_3 = tk.Label(self.canvas, text=f"{self.result_gateway_split[2]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.gateway_3.place(x=622, y=374)
        elif (len(self.result_gateway_split[2]) == 2):
            self.gateway_3 = tk.Label(self.canvas, text=f"{self.result_gateway_split[2]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.gateway_3.place(x=617, y=374)
        elif (len(self.result_gateway_split[2]) == 3):
            self.gateway_3 = tk.Label(self.canvas, text=f"{self.result_gateway_split[2]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.gateway_3.place(x=614, y=374)
        if (len(self.result_gateway_split[3]) == 1):
            self.gateway_4 = tk.Label(self.canvas, text=f"{self.result_gateway_split[3]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.gateway_4.place(x=724, y=374)
        elif (len(self.result_gateway_split[3]) == 2):
            self.gateway_4 = tk.Label(self.canvas, text=f"{self.result_gateway_split[3]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.gateway_4.place(x=720, y=374)
        elif (len(self.result_gateway_split[3]) == 3):
            self.gateway_4 = tk.Label(self.canvas, text=f"{self.result_gateway_split[3]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.gateway_4.place(x=717, y=374)

    def update_switch(self, event):
        if self.Switch_Flat_img.cget("file") == "images\PanelSettings\Switch-0.png":
            self.Switch_Flat_img = PhotoImage(file=r"images\PanelSettings\Switch-1.png")
        elif self.Switch_Flat_img.cget("file") == "images\PanelSettings\Switch-1.png":
            self.Switch_Flat_img = PhotoImage(file=r"images\PanelSettings\Switch-0.png")
        self.Switch_Flat_button = self.canvas.create_image(670, 152, image=self.Switch_Flat_img)
        self.canvas.tag_bind(self.Switch_Flat_button, "<Button-1>", self.update_switch)


    def update_clock(self, current_time):
        self.clock_label.config(text=current_time)

class NetInfo:
    def __init__(self):
        self.ipv4 = self.local()
        self.platform = system()
        self.mac = None
        self.iface = None
        self.ipv6 = None
        if self.platform == "Windows":
            self.mac_iface_win()
        elif self.platform == "Linux":
            self.mac_iface_lin()
        else:
            exit(0)

    @staticmethod
    def local():
        st = socket(AF_INET, SOCK_DGRAM)
        try:
            st.connect(('10.255.255.255', 1))
            ip = st.getsockname()[0]
        except OSError:
            ip = '127.0.0.1'
        finally:
            st.close()
        return ip

    def mac_iface_win(self):
        adapter_lst = check_output("wmic NICCONFIG WHERE IPEnabled=true GET MACAddress, "
                                   "IPAddress /FORMAT:csv", shell=False).decode().strip().splitlines()
        for adapter in adapter_lst:
            if adapter.strip():
                node, ipaddr, mac = adapter.split(",")
                ipaddr = sub("[{}]", "", ipaddr).split(";")
                if ipaddr[0] == self.ipv4:
                    self.mac = mac.upper()
                    try:
                        self.ipv6 = ipaddr[1]
                    except IndexError:
                        pass
        if self.mac:
            interface_all = check_output('getmac /FO csv /NH /V', shell=False).decode('cp866').splitlines()
            for line in interface_all:
                if self.mac.upper().replace(":", "-") in line:
                    self.iface = line.split(",")[0].replace('"', '')
                    break

    def mac_iface_lin(self):
        com_run = check_output('ip -h -br a | grep UP', shell=True).decode().split()
        self.iface = com_run[0].strip()
        self.ipv6 = com_run[3].strip().split("/")[0]
        self.mac = check_output("ip a | grep ether | gawk '{print $2}'", shell=True).decode().strip().upper()

class Frame19(tk.Frame, NetInfo):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='black')

        self.canvas = Canvas(
            self,
            bg="black",
            height=480,
            width=800,
            bd=0,
            highlightthickness=0,
            relief="ridge")
        self.canvas.place(x=0, y=0)
        self.clock_label = tk.Label(self.canvas, text="", fg='white', bg='black', font=('Roboto Bold', 12))
        self.clock_label.place(x=680, y=5)

        self.new_window = None

        self.font = ImageFont.truetype("Roboto-Bold.ttf", 18)
        self.img_screen = Image.open(r"new_images\screen.png")
        self.img_calendar = Image.open(r"new_images\calendar.png")
        self.img_peak = Image.open(r"new_images\peak.png")
        self.img_tablet = Image.open(r"new_images\tablet.png")
        self.img_gear_wheel = Image.open(r"new_images\gear_wheel.png")
        self.img_wrench = Image.open(r"new_images\wrench.png")
        self.img_gear_wheel_bg = Image.open(r"new_images\gear_wheel_bg.png")
        self.img_phone = Image.open(r"new_images\phone.png")
        self.img_right = Image.open(r"new_images\right.png")
        self.img_triangle = Image.open(r"new_images\triangle.png")

        self.combined_img1 = Image.new("RGB", (200, 60), "black")
        self.draw1 = ImageDraw.Draw(self.combined_img1)
        self.combined_img1.paste(self.img_screen, (15, 20))
        self.draw1.text((50, 20), "Главный экран", fill="white", font=self.font)
        self.combined_photo1 = ImageTk.PhotoImage(self.combined_img1)

        self.combined_img2 = Image.new("RGB", (200, 60), "black")
        self.draw2 = ImageDraw.Draw(self.combined_img2)
        self.combined_img2.paste(self.img_calendar, (10, 15))
        self.draw2.text((50, 10), "Планировщик\nуставок", fill="white", font=self.font)
        self.combined_photo2 = ImageTk.PhotoImage(self.combined_img2)

        self.combined_img3 = Image.new("RGB", (200, 60), "black")
        self.draw3 = ImageDraw.Draw(self.combined_img3)
        self.combined_img3.paste(self.img_peak, (10, 15))
        self.combined_img3.paste(self.img_right, (170, 15))
        self.draw3.text((50, 20), "Мониторинг", fill="white", font=self.font)
        self.combined_photo3 = ImageTk.PhotoImage(self.combined_img3)

        self.combined_img4 = Image.new("RGB", (200, 60), "black")
        self.draw4 = ImageDraw.Draw(self.combined_img4)
        self.combined_img4.paste(self.img_tablet, (10, 15))
        self.combined_img4.paste(self.img_right, (170, 15))
        self.draw4.text((50, 20), "Журнал", fill="white", font=self.font)
        self.combined_photo4 = ImageTk.PhotoImage(self.combined_img4)

        self.combined_img5 = Image.new("RGB", (200, 60), "black")
        self.draw5 = ImageDraw.Draw(self.combined_img5)
        self.combined_img5.paste(self.img_gear_wheel, (10, 15))
        self.combined_img5.paste(self.img_right, (170, 15))
        self.draw5.text((50, 10), "Настройки\nстанции", fill="white", font=self.font)
        self.combined_photo5 = ImageTk.PhotoImage(self.combined_img5)

        self.combined_img6 = Image.new("RGB", (200, 60), "black")
        self.draw6 = ImageDraw.Draw(self.combined_img6)
        self.combined_img6.paste(self.img_wrench, (10, 15))
        self.combined_img6.paste(self.img_right, (170, 15))
        self.draw6.text((50, 10), "Инженерное\nменю", fill="white", font=self.font)
        self.combined_photo6 = ImageTk.PhotoImage(self.combined_img6)

        self.combined_img7 = Image.new("RGB", (200, 60), "black")
        self.draw7 = ImageDraw.Draw(self.combined_img7)
        self.combined_img7.paste(self.img_gear_wheel_bg, (10, 15))
        self.combined_img7.paste(self.img_triangle, (180, 13))
        self.draw7.text((50, 10), "Настройки\nпанели", fill="white", font=self.font)
        self.combined_photo7 = ImageTk.PhotoImage(self.combined_img7)

        self.combined_img8 = Image.new("RGB", (200, 60), "black")
        self.draw8 = ImageDraw.Draw(self.combined_img8)
        self.combined_img8.paste(self.img_phone, (10, 15))
        self.draw8.text((50, 20), "Контакты", fill="white", font=self.font)
        self.combined_photo8 = ImageTk.PhotoImage(self.combined_img8)

        button = tk.Button(self, image=self.combined_photo1, bg='black', relief="groove", activebackground="black",
                           command=lambda: controller.show_frame("Frame1_1"))
        button.place(x=0, y=0, width=200, height=60)
        button2 = tk.Button(self, image=self.combined_photo2, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame2"))
        button2.place(x=0, y=60, width=200, height=60)
        button3 = tk.Button(self, image=self.combined_photo3, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame3"))
        button3.place(x=0, y=120, width=200, height=60)
        button4 = tk.Button(self, image=self.combined_photo4, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame6"))
        button4.place(x=0, y=180, width=200, height=60)
        button5 = tk.Button(self, image=self.combined_photo5, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame9"))
        button5.place(x=0, y=240, width=200, height=60)
        button6 = tk.Button(self, image=self.combined_photo6, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame16"))
        button6.place(x=0, y=300, width=200, height=60)
        button7 = tk.Button(self, image=self.combined_photo7, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame19"))
        button7.place(x=0, y=360, width=200, height=60)
        button8 = tk.Button(self, image=self.combined_photo8, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame20"))
        button8.place(x=0, y=420, width=200, height=60)

        self.img_noon = PhotoImage(file=r"new_images\noon.png")
        self.img_scrn = PhotoImage(file=r"new_images\screen.png")
        self.img_note = PhotoImage(file=r"new_images\note.png")
        self.img_cal = PhotoImage(file=r"new_images\calendar.png")
        self.img_time = PhotoImage(file=r"new_images\time.png")
        self.img_ip = PhotoImage(file=r"new_images\ip.png")
        self.img_mask = PhotoImage(file=r"new_images\mask.png")
        self.img_gateway = PhotoImage(file=r"new_images\gateway.png")
        self.img_shield = PhotoImage(file=r"new_images\shield.png")
        self.img_rectangle_l = PhotoImage(file=r"new_images\rectangle_long.png")
        self.img_rectangle_s = PhotoImage(file=r"new_images\rectangle_short.png")

        self.canvas.create_line(220, 180, 790, 180, fill="gray", width=2)
        self.canvas.create_line(220, 270, 790, 270, fill="gray", width=2)

        self.canvas.create_image(233, 70, image=self.img_noon)
        self.canvas.create_image(233, 110, image=self.img_scrn)
        self.canvas.create_image(233, 145, image=self.img_note)
        self.canvas.create_image(233, 202, image=self.img_cal)
        self.canvas.create_image(233, 237, image=self.img_time)
        self.canvas.create_image(233, 303, image=self.img_ip)
        self.canvas.create_image(233, 342, image=self.img_mask)
        self.canvas.create_image(233, 381, image=self.img_gateway)
        self.canvas.create_image(624, 70, image=self.img_shield)
        self.canvas.create_image(624, 109, image=self.img_shield)
        self.canvas.create_image(624, 147, image=self.img_shield)
        self.canvas.create_image(461.25, 201.75, image=self.img_shield)
        self.canvas.create_image(461.25, 242.75, image=self.img_shield)
        self.canvas.create_image(362.25, 302.75, image=self.img_shield)
        self.canvas.create_image(362.25, 342.75, image=self.img_shield)
        self.canvas.create_image(362.25, 380.75, image=self.img_shield)

        self.label1 = tk.Label(self.canvas, text="Ethernet", fg='white', bg='black',
                               font=('Roboto Bold', 10))
        self.label1.place(x=216, y=273, width=54, height=14)
        self.label2 = tk.Label(self.canvas, text="Время до отключения дисплея", fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label2.place(x=259, y=59)
        self.label3 = tk.Label(self.canvas, text="Время до отключения заставки", fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label3.place(x=259, y=99)
        self.label4 = tk.Label(self.canvas, text="Зуммер", fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label4.place(x=259, y=136)
        self.label5 = tk.Label(self.canvas, text="Дата", fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label5.place(x=259, y=193)
        self.label6 = tk.Label(self.canvas, text="Время", fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label6.place(x=259, y=227)
        self.label7 = tk.Label(self.canvas, text="IP Адрес", fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label7.place(x=259, y=294)
        self.label8 = tk.Label(self.canvas, text="Маска", fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label8.place(x=259, y=333)
        self.label9 = tk.Label(self.canvas, text="Шлюз", fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label9.place(x=259, y=372)

        self.Switch_Flat_img = PhotoImage(file=r"images\PanelSettings\Switch-0.png")
        self.Switch_Flat_button = self.canvas.create_image(670, 152, image=self.Switch_Flat_img)
        self.canvas.tag_bind(self.Switch_Flat_button, "<Button-1>", self.update_switch)

        self.ip_ = NetInfo().ipv4
        self.result_IP = self.ip_.split(".")

        self.net_if_addrs = psutil.net_if_addrs()

        for interface, addresses in self.net_if_addrs.items():
            for address in addresses:
                if address.family == 2:  # IPv4
                    if address.address == self.ip_:
                        self.result_netmask = address.netmask

        self.result_netmask_split = self.result_netmask.split(".")

        if (len(self.result_netmask_split[0])== 1):
            self.netmask_1 = tk.Label(self.canvas, text=f"{self.result_netmask_split[0]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.netmask_1.place(x=418, y=332)
        elif (len(self.result_netmask_split[0])== 2):
            self.netmask_1 = tk.Label(self.canvas, text=f"{self.result_netmask_split[0]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.netmask_1.place(x=414, y=332)
        elif (len(self.result_netmask_split[0])== 3):
            self.netmask_1 = tk.Label(self.canvas, text=f"{self.result_netmask_split[0]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.netmask_1.place(x=410, y=332)
        if (len(self.result_netmask_split[1])== 1):
            self.netmask_1 = tk.Label(self.canvas, text=f"{self.result_netmask_split[1]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.netmask_1.place(x=520, y=332)
        elif (len(self.result_netmask_split[1])== 2):
            self.netmask_1 = tk.Label(self.canvas, text=f"{self.result_netmask_split[1]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.netmask_1.place(x=516, y=332)
        elif (len(self.result_netmask_split[1])== 3):
            self.netmask_1 = tk.Label(self.canvas, text=f"{self.result_netmask_split[1]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.netmask_1.place(x=512, y=332)
        if (len(self.result_netmask_split[2])== 1):
            self.netmask_1 = tk.Label(self.canvas, text=f"{self.result_netmask_split[2]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.netmask_1.place(x=622, y=332)
        elif (len(self.result_netmask_split[2])== 2):
            self.netmask_1 = tk.Label(self.canvas, text=f"{self.result_netmask_split[2]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.netmask_1.place(x=617, y=332)
        elif (len(self.result_netmask_split[2])== 3):
            self.netmask_1 = tk.Label(self.canvas, text=f"{self.result_netmask_split[2]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.netmask_1.place(x=614, y=332)
        if (len(self.result_netmask_split[3])== 1):
            self.netmask_1 = tk.Label(self.canvas, text=f"{self.result_netmask_split[3]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.netmask_1.place(x=724, y=332)
        elif (len(self.result_netmask_split[3])== 2):
            self.netmask_1 = tk.Label(self.canvas, text=f"{self.result_netmask_split[3]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.netmask_1.place(x=720, y=332)
        elif (len(self.result_netmask_split[3])== 3):
            self.netmask_1 = tk.Label(self.canvas, text=f"{self.result_netmask_split[3]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.netmask_1.place(x=717, y=332)

        # Кликабельная зона
        self.time_rectangle_1 = self.canvas.create_image(715, 69.5, image=self.img_rectangle_l)
        self.time_rectangle_2 = self.canvas.create_image(715, 109.5, image=self.img_rectangle_l)
        self.time_display_1 = tk.Label(self.canvas, text="30", fg='white', bg='black', font=('Roboto Bold', 12))
        self.time_display_1.place(x=645, y=58)
        self.time_label_1 = tk.Label(self.canvas, text="минут", fg='white', bg='black', font=('Roboto Bold', 12))
        self.time_label_1.place(x=738, y=59, width=47, height=19)
        self.time_display_2 = tk.Label(self.canvas, text="15", fg='white', bg='black', font=('Roboto Bold', 12))
        self.time_display_2.place(x=645, y=98)
        self.time_label_2 = tk.Label(self.canvas, text="минут", fg='white', bg='black', font=('Roboto Bold', 12))
        self.time_label_2.place(x=738, y=99, width=47, height=19)

        self.data_days = self.canvas.create_image(525, 205, image=self.img_rectangle_s)
        self.data_days_label = tk.Label(self.canvas, text="День", fg='white', bg='black', font=('Roboto Bold', 12))
        self.data_days_label.place(x=530, y=198, width=39, height=19)
        self.data_months = self.canvas.create_image(630, 205, image=self.img_rectangle_s)
        self.data_months_label = tk.Label(self.canvas, text="Месяц", fg='white', bg='black', font=('Roboto Bold', 12))
        self.data_months_label.place(x=620, y=198, width=59, height=19)
        self.data_years = self.canvas.create_image(735, 205, image=self.img_rectangle_s)
        self.data_years_label = tk.Label(self.canvas, text="Год", fg='white', bg='black', font=('Roboto Bold', 12))
        self.data_years_label.place(x=745, y=198, width=39, height=19)
        self.data_hours = self.canvas.create_image(525, 245, image=self.img_rectangle_s)
        self.data_hours_label = tk.Label(self.canvas, text="Часы", fg='white', bg='black', font=('Roboto Bold', 12))
        self.data_hours_label.place(x=530, y=237, width=39, height=19)
        self.data_minutes = self.canvas.create_image(630, 245, image=self.img_rectangle_s)
        self.data_minutes_label = tk.Label(self.canvas, text="Минуты", fg='white', bg='black', font=('Roboto Bold', 12))
        self.data_minutes_label.place(x=615, y=237, width=59, height=19)
        self.data_seconds = self.canvas.create_image(735, 245, image=self.img_rectangle_s)
        self.data_seconds_label = tk.Label(self.canvas, text="Секунды", fg='white', bg='black', font=('Roboto Bold', 12))
        self.data_seconds_label.place(x=715, y=237, width=66, height=19)

        self.ip_rectangle_1 = self.canvas.create_image(428.75, 302.5, image=self.img_rectangle_s)
        self.ip_rectangle_2 = self.canvas.create_image(530.75, 302.5, image=self.img_rectangle_s)
        self.ip_rectangle_3 = self.canvas.create_image(632.75, 302.5, image=self.img_rectangle_s)
        self.ip_rectangle_4 = self.canvas.create_image(734.75, 302.5, image=self.img_rectangle_s)
        self.mask_rectangle_1 = self.canvas.create_image(428.75, 342.5, image=self.img_rectangle_s)
        self.mask_rectangle_2 = self.canvas.create_image(530.75, 342.5, image=self.img_rectangle_s)
        self.mask_rectangle_3 = self.canvas.create_image(632.75, 342.5, image=self.img_rectangle_s)
        self.mask_rectangle_4 = self.canvas.create_image(734.75, 342.5, image=self.img_rectangle_s)
        self.gateway_rectangle_1 = self.canvas.create_image(428.75, 382.5, image=self.img_rectangle_s)
        self.gateway_rectangle_2 = self.canvas.create_image(530.75, 382.5, image=self.img_rectangle_s)
        self.gateway_rectangle_3 = self.canvas.create_image(632.75, 382.5, image=self.img_rectangle_s)
        self.gateway_rectangle_4 = self.canvas.create_image(734.75, 382.5, image=self.img_rectangle_s)
        # Кликабельная зона

        def show_data_and_time():
            now = datetime.now()
            self.show_day.config(text = now.strftime("%d"))
            self.show_month.config(text = now.strftime("%m"))
            self.show_year.config(text = now.strftime("%Y"))
            self.show_hour.config(text = now.strftime("%H"))
            self.show_minute.config(text = now.strftime("%M"))
            self.show_second.config(text = now.strftime("%S"))
            self.canvas.after(100, show_data_and_time)

        wmi_obj = wmi.WMI()
        wmi_sql = "select IPAddress,DefaultIPGateway from Win32_NetworkAdapterConfiguration where IPEnabled=TRUE"
        self.wmi_out = wmi_obj.query(wmi_sql)

        self.show_hour = tk.Label(self.canvas, text="", fg='white', bg='black', font=('Roboto Bold', 12))
        self.show_hour.place(x=480, y=234)
        self.show_minute = tk.Label(self.canvas, text="", fg='white', bg='black', font=('Roboto Bold', 12))
        self.show_minute.place(x=584, y=234)
        self.show_second = tk.Label(self.canvas, text="", fg='white', bg='black', font=('Roboto Bold', 12))
        self.show_second.place(x=689, y=234)
        self.show_day = tk.Label(self.canvas, text="", fg='white', bg='black', font=('Roboto Bold', 12))
        self.show_day.place(x=480, y=195)
        self.show_month = tk.Label(self.canvas, text="", fg='white', bg='black', font=('Roboto Bold', 12))
        self.show_month.place(x=584, y=195)
        self.show_year = tk.Label(self.canvas, text="", fg='white', bg='black', font=('Roboto Bold', 12))
        self.show_year.place(x=689, y=195)

        show_data_and_time()

        self.result_IP = self.ip_.split(".")

        if(len(self.result_IP[0]) == 1):
            self.IP_1 = tk.Label(self.canvas, text=f"{self.result_IP[0]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.IP_1.place(x=418, y=294)
        elif(len(self.result_IP[0]) == 2):
            self.IP_1 = tk.Label(self.canvas, text=f"{self.result_IP[0]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.IP_1.place(x=414, y=294)
        elif (len(self.result_IP[0]) == 3):
            self.IP_1 = tk.Label(self.canvas, text=f"{self.result_IP[0]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.IP_1.place(x=410, y=294)
        if (len(self.result_IP[1]) == 1):
            self.IP_2 = tk.Label(self.canvas, text=f"{self.result_IP[1]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.IP_2.place(x=520, y=294)
        elif (len(self.result_IP[1]) == 2):
            self.IP_2 = tk.Label(self.canvas, text=f"{self.result_IP[1]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.IP_2.place(x=516, y=294)
        elif (len(self.result_IP[1]) == 3):
            self.IP_2 = tk.Label(self.canvas, text=f"{self.result_IP[1]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.IP_2.place(x=512, y=294)
        if (len(self.result_IP[2]) == 1):
            self.IP_3 = tk.Label(self.canvas, text=f"{self.result_IP[2]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.IP_3.place(x=622, y=294)
        elif (len(self.result_IP[2]) == 2):
            self.IP_3 = tk.Label(self.canvas, text=f"{self.result_IP[2]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.IP_3.place(x=617, y=294)
        elif (len(self.result_IP[2]) == 3):
            self.IP_3 = tk.Label(self.canvas, text=f"{self.result_IP[2]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.IP_3.place(x=614, y=294)
        if (len(self.result_IP[3]) == 1):
            self.IP_4 = tk.Label(self.canvas, text=f"{self.result_IP[3]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.IP_4.place(x=724, y=294)
        elif (len(self.result_IP[3]) == 2):
            self.IP_4 = tk.Label(self.canvas, text=f"{self.result_IP[3]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.IP_4.place(x=720, y=294)
        elif (len(self.result_IP[3]) == 3):
            self.IP_4 = tk.Label(self.canvas, text=f"{self.result_IP[3]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.IP_4.place(x=717, y=294)

        for dev in self.wmi_out:
            self.result_gateway = dev.DefaultIPGateway[0]

        self.result_gateway_split = self.result_gateway.split(".")

        if (len(self.result_gateway_split[0]) == 1):
            self.gateway_1 = tk.Label(self.canvas, text=f"{self.result_gateway_split[0]}", fg='white', bg='black',font=('Roboto Bold', 12))
            self.gateway_1.place(x=418, y=374)
        elif (len(self.result_gateway_split[0]) == 2):
            self.gateway_1 = tk.Label(self.canvas, text=f"{self.result_gateway_split[0]}", fg='white', bg='black',font=('Roboto Bold', 12))
            self.gateway_1.place(x=414, y=374)
        elif (len(self.result_gateway_split[0]) == 3):
            self.gateway_1 = tk.Label(self.canvas, text=f"{self.result_gateway_split[0]}", fg='white', bg='black',font=('Roboto Bold', 12))
            self.gateway_1.place(x=410, y=374)
        if (len(self.result_gateway_split[1]) == 1):
            self.gateway_2 = tk.Label(self.canvas, text=f"{self.result_gateway_split[1]}", fg='white', bg='black',font=('Roboto Bold', 12))
            self.gateway_2.place(x=520, y=374)
        elif (len(self.result_gateway_split[1]) == 2):
            self.gateway_2 = tk.Label(self.canvas, text=f"{self.result_gateway_split[1]}", fg='white', bg='black',font=('Roboto Bold', 12))
            self.gateway_2.place(x=516, y=374)
        elif (len(self.result_gateway_split[1]) == 3):
            self.gateway_2 = tk.Label(self.canvas, text=f"{self.result_gateway_split[1]}", fg='white', bg='black',font=('Roboto Bold', 12))
            self.gateway_2.place(x=512, y=374)
        if (len(self.result_gateway_split[2]) == 1):
            self.gateway_3 = tk.Label(self.canvas, text=f"{self.result_gateway_split[2]}", fg='white', bg='black',font=('Roboto Bold', 12))
            self.gateway_3.place(x=622, y=374)
        elif (len(self.result_gateway_split[2]) == 2):
            self.gateway_3 = tk.Label(self.canvas, text=f"{self.result_gateway_split[2]}", fg='white', bg='black',font=('Roboto Bold', 12))
            self.gateway_3.place(x=617, y=374)
        elif (len(self.result_gateway_split[2]) == 3):
            self.gateway_3 = tk.Label(self.canvas, text=f"{self.result_gateway_split[2]}", fg='white', bg='black',font=('Roboto Bold', 12))
            self.gateway_3.place(x=614, y=374)
        if (len(self.result_gateway_split[3]) == 1):
            self.gateway_4 = tk.Label(self.canvas, text=f"{self.result_gateway_split[3]}", fg='white', bg='black',font=('Roboto Bold', 12))
            self.gateway_4.place(x=724, y=374)
        elif (len(self.result_gateway_split[3]) == 2):
            self.gateway_4 = tk.Label(self.canvas, text=f"{self.result_gateway_split[3]}", fg='white', bg='black',font=('Roboto Bold', 12))
            self.gateway_4.place(x=720, y=374)
        elif (len(self.result_gateway_split[3]) == 3):
            self.gateway_4 = tk.Label(self.canvas, text=f"{self.result_gateway_split[3]}", fg='white', bg='black',font=('Roboto Bold', 12))
            self.gateway_4.place(x=717, y=374)

    def update_switch(self, event):
        self.new_window = Keypad("Frame19")
        # self.new_window.grab_set() блок
        if self.Switch_Flat_img.cget("file") == "images\PanelSettings\Switch-0.png":
            self.Switch_Flat_img = PhotoImage(file=r"images\PanelSettings\Switch-1.png")
        elif self.Switch_Flat_img.cget("file") == "images\PanelSettings\Switch-1.png":
            self.Switch_Flat_img = PhotoImage(file=r"images\PanelSettings\Switch-0.png")
        self.Switch_Flat_button = self.canvas.create_image(670, 152, image=self.Switch_Flat_img)
        self.canvas.tag_bind(self.Switch_Flat_button, "<Button-1>", self.update_switch)


    def update_clock(self, current_time):
        self.clock_label.config(text=current_time)

class Frame20(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='black')
        self.canvas = Canvas(
            self,
            bg="black",
            height=480,
            width=800,
            bd=0,
            highlightthickness=0,
            relief="ridge")
        self.canvas.place(x=0, y=0)
        self.clock_label = tk.Label(self.canvas, text="", fg='white', bg='black', font=('Roboto Bold', 12))
        self.clock_label.place(x=680, y=5)

        self.font = ImageFont.truetype("Roboto-Bold.ttf", 18)
        self.img_screen = Image.open(r"new_images\screen.png")
        self.img_calendar = Image.open(r"new_images\calendar.png")
        self.img_peak = Image.open(r"new_images\peak.png")
        self.img_tablet = Image.open(r"new_images\tablet.png")
        self.img_gear_wheel = Image.open(r"new_images\gear_wheel.png")
        self.img_wrench = Image.open(r"new_images\wrench.png")
        self.img_gear_wheel_bg = Image.open(r"new_images\gear_wheel_bg.png")
        self.img_phone = Image.open(r"new_images\phone.png")
        self.img_right = Image.open(r"new_images\right.png")
        self.img_triangle = Image.open(r"new_images\triangle.png")

        self.combined_img1 = Image.new("RGB", (200, 60), "black")
        self.draw1 = ImageDraw.Draw(self.combined_img1)
        self.combined_img1.paste(self.img_screen, (15, 20))
        self.draw1.text((50, 20), "Главный экран", fill="white", font=self.font)
        self.combined_photo1 = ImageTk.PhotoImage(self.combined_img1)

        self.combined_img2 = Image.new("RGB", (200, 60), "black")
        self.draw2 = ImageDraw.Draw(self.combined_img2)
        self.combined_img2.paste(self.img_calendar, (10, 15))
        self.draw2.text((50, 10), "Планировщик\nуставок", fill="white", font=self.font)
        self.combined_photo2 = ImageTk.PhotoImage(self.combined_img2)

        self.combined_img3 = Image.new("RGB", (200, 60), "black")
        self.draw3 = ImageDraw.Draw(self.combined_img3)
        self.combined_img3.paste(self.img_peak, (10, 15))
        self.combined_img3.paste(self.img_right, (170, 15))
        self.draw3.text((50, 20), "Мониторинг", fill="white", font=self.font)
        self.combined_photo3 = ImageTk.PhotoImage(self.combined_img3)

        self.combined_img4 = Image.new("RGB", (200, 60), "black")
        self.draw4 = ImageDraw.Draw(self.combined_img4)
        self.combined_img4.paste(self.img_tablet, (10, 15))
        self.combined_img4.paste(self.img_right, (170, 15))
        self.draw4.text((50, 20), "Журнал", fill="white", font=self.font)
        self.combined_photo4 = ImageTk.PhotoImage(self.combined_img4)

        self.combined_img5 = Image.new("RGB", (200, 60), "black")
        self.draw5 = ImageDraw.Draw(self.combined_img5)
        self.combined_img5.paste(self.img_gear_wheel, (10, 15))
        self.combined_img5.paste(self.img_right, (170, 15))
        self.draw5.text((50, 10), "Настройки\nстанции", fill="white", font=self.font)
        self.combined_photo5 = ImageTk.PhotoImage(self.combined_img5)

        self.combined_img6 = Image.new("RGB", (200, 60), "black")
        self.draw6 = ImageDraw.Draw(self.combined_img6)
        self.combined_img6.paste(self.img_wrench, (10, 15))
        self.combined_img6.paste(self.img_right, (170, 15))
        self.draw6.text((50, 10), "Инженерное\nменю", fill="white", font=self.font)
        self.combined_photo6 = ImageTk.PhotoImage(self.combined_img6)

        self.combined_img7 = Image.new("RGB", (200, 60), "black")
        self.draw7 = ImageDraw.Draw(self.combined_img7)
        self.combined_img7.paste(self.img_gear_wheel_bg, (10, 15))
        self.draw7.text((50, 10), "Настройки\nпанели", fill="white", font=self.font)
        self.combined_photo7 = ImageTk.PhotoImage(self.combined_img7)

        self.combined_img8 = Image.new("RGB", (200, 60), "black")
        self.draw8 = ImageDraw.Draw(self.combined_img8)
        self.combined_img8.paste(self.img_phone, (10, 15))
        self.combined_img8.paste(self.img_triangle, (180, 13))
        self.draw8.text((50, 20), "Контакты", fill="white", font=self.font)
        self.combined_photo8 = ImageTk.PhotoImage(self.combined_img8)

        button = tk.Button(self, image=self.combined_photo1, bg='black', relief="groove", activebackground="black",
                           command=lambda: controller.show_frame("Frame1_1"))
        button.place(x=0, y=0, width=200, height=60)
        button2 = tk.Button(self, image=self.combined_photo2, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame2"))
        button2.place(x=0, y=60, width=200, height=60)
        button3 = tk.Button(self, image=self.combined_photo3, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame3"))
        button3.place(x=0, y=120, width=200, height=60)
        button4 = tk.Button(self, image=self.combined_photo4, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame6"))
        button4.place(x=0, y=180, width=200, height=60)
        button5 = tk.Button(self, image=self.combined_photo5, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame9"))
        button5.place(x=0, y=240, width=200, height=60)
        button6 = tk.Button(self, image=self.combined_photo6, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame16"))
        button6.place(x=0, y=300, width=200, height=60)
        button7 = tk.Button(self, image=self.combined_photo7, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame19"))
        button7.place(x=0, y=360, width=200, height=60)
        button8 = tk.Button(self, image=self.combined_photo8, bg='black', relief="groove", activebackground="black",
                            command=lambda: controller.show_frame("Frame20"))
        button8.place(x=0, y=420, width=200, height=60)

        self.img_question = PhotoImage(file=r"new_images\question.png")
        self.img_key = PhotoImage(file=r"new_images\key.png")
        self.img_swap = PhotoImage(file=r"new_images\swap.png")
        self.img_cal = PhotoImage(file=r"new_images\calendar.png")
        self.img_mail = PhotoImage(file=r"new_images\mail.png")
        self.img_site = PhotoImage(file=r"new_images\site.png")
        self.img_support = PhotoImage(file=r"new_images\support.png")

        self.canvas.create_line(220, 160, 790, 160, fill="gray", width=2)
        self.canvas.create_line(220, 240, 790, 240, fill="gray", width=2)

        self.canvas.create_image(233, 61, image=self.img_question)
        self.canvas.create_image(233, 96, image=self.img_question)
        self.canvas.create_image(233, 132, image=self.img_cal)
        self.canvas.create_image(233, 178, image=self.img_key)
        self.canvas.create_image(233, 217, image=self.img_swap)
        self.canvas.create_image(233, 265, image=self.img_mail)
        self.canvas.create_image(233, 298, image=self.img_site)
        self.canvas.create_image(233, 334, image=self.img_support)

        self.label1 = tk.Label(self.canvas, text="Программное обеспечение", fg='white', bg='black', font=('Roboto Bold', 12))
        self.label1.place(x=259, y=50)
        self.label2 = tk.Label(self.canvas, text="Версия EasyBuilder", fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label2.place(x=259, y=86)
        self.label3 = tk.Label(self.canvas, text="Дата компиляции", fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label3.place(x=259, y=122)
        self.label4 = tk.Label(self.canvas, text="Код продукта", fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label4.place(x=259, y=168)
        self.label5 = tk.Label(self.canvas, text="Количество насосов", fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label5.place(x=259, y=207)
        self.label6 = tk.Label(self.canvas, text="Почта", fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label6.place(x=259, y=255)
        self.label7 = tk.Label(self.canvas, text="Вэб-сайт", fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label7.place(x=259, y=288)
        self.label8 = tk.Label(self.canvas, text="Техническая поддержка", fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label8.place(x=259, y=324)
        self.label9 = tk.Label(self.canvas, text="из них работающих", fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label9.place(x=485, y=207)
        self.label10 = tk.Label(self.canvas, text="info@mfmc.ru", fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label10.place(x=644, y=255)
        self.label11 = tk.Label(self.canvas, text="www.mfmc.ru", fg='white', bg='black',
                                font=('Roboto Bold', 12))
        self.label11.place(x=644, y=289)
        self.label12 = tk.Label(self.canvas, text="+7 (495) 122-22-62\n+7 (800) 333-14-61", fg='white', bg='black',
                                font=('Roboto Bold', 12))
        self.label12.place(x=644, y=321)

        self.software_label = tk.Label(self.canvas, text="AAAAAAAAAAAAAAAAAAAAAAAA", fg='white', bg='black', font=('Roboto Bold', 12))
        self.software_label.place(x=485, y=48)
        self.version_label = tk.Label(self.canvas, text="##########", fg='white', bg='black', font=('Roboto Bold', 12))
        self.version_label.place(x=485, y=83)
        self.compilationDate_label = tk.Label(self.canvas, text="##:##:#####", fg='white', bg='black', font=('Roboto Bold', 12))
        self.compilationDate_label.place(x=485, y=119)
        self.productCode1_label = tk.Label(self.canvas, text="#########", fg='white', bg='black', font=('Roboto Bold', 12))
        self.productCode1_label.place(x=420, y=166)
        self.productCode2_label = tk.Label(self.canvas, text="#########", fg='white', bg='black', font=('Roboto Bold', 12))
        self.productCode2_label.place(x=526, y=166)
        self.productCode3_label = tk.Label(self.canvas, text="#########", fg='white', bg='black', font=('Roboto Bold', 12))
        self.productCode3_label.place(x=632, y=166)
        self.pumpsAll_label = tk.Label(self.canvas, text="##", fg='white', bg='black', font=('Roboto Bold', 12))
        self.pumpsAll_label.place(x=444, y=205)
        self.pumpsWorking_label = tk.Label(self.canvas, text="##", fg='white', bg='black', font=('Roboto Bold', 12))
        self.pumpsWorking_label.place(x=651, y=205)

    def update_clock(self, current_time):
        self.clock_label.config(text=current_time)


app = App()
app.mainloop()

