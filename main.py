import tkinter as tk
from tkinter import PhotoImage, Canvas
from datetime import datetime
from PIL import Image, ImageTk
from platform import system
from re import sub
from subprocess import check_output
from socket import socket, AF_INET, SOCK_DGRAM
import wmi
import psutil

'''
Keypad - кейпад
Frame1 - Главный экран - 1 2 3 4 фреймы индикаторов
Menu - Настройки
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
        for F in (Frame1_1, Frame1_2, Frame1_3, Frame1_4, Menu, Frame2, Frame3, Frame4, Frame5, Frame6, Frame7, Frame8, Frame9, Frame10, Frame11, Frame12, Frame13, Frame14, Frame15, Frame16, Frame17, Frame18, Frame19, Frame20):
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
            case "Menu":
                self.title("Меню")
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
        self.options_img = PhotoImage(file=r"images\Buttons\options.png")
        self.options_button = self.canvas.create_image(65, 18, image=self.options_img)
        self.canvas.tag_bind(self.options_button, "<Button-1>", lambda event: controller.show_frame("Menu"))
        self.indicators_img = PhotoImage(file=r"images\MainScreen\indicator_0.png")
        self.indicators_button = self.canvas.create_image(195, 20, image=self.indicators_img)
        self.canvas.tag_bind(self.indicators_button, "<Button-1>", lambda event: controller.show_frame("Frame1_2"))
        self.background_img = PhotoImage(file=r"images\MainScreen\stop_icon.png")
        background = self.canvas.create_image(655, 20, image=self.background_img)
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
        self.options_img = PhotoImage(file=r"images\Buttons\options.png")
        self.options_button = self.canvas.create_image(65, 18, image=self.options_img)
        self.canvas.tag_bind(self.options_button, "<Button-1>", lambda event: controller.show_frame("Menu"))
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
        self.options_img = PhotoImage(file=r"images\Buttons\options.png")
        self.options_button = self.canvas.create_image(65, 18, image=self.options_img)
        self.canvas.tag_bind(self.options_button, "<Button-1>", lambda event: controller.show_frame("Menu"))
        self.indicators_img = PhotoImage(file=r"images\MainScreen\indicator_1.png")
        self.indicators_button = self.canvas.create_image(195, 20, image=self.indicators_img)
        self.canvas.tag_bind(self.indicators_button, "<Button-1>", lambda event: controller.show_frame("Frame1_4"))
        self.background_img = PhotoImage(file=r"images\MainScreen\stop_icon.png")
        background = self.canvas.create_image(655, 20, image=self.background_img)
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
        self.options_img = PhotoImage(file=r"images\Buttons\options.png")
        self.options_button = self.canvas.create_image(65, 18, image=self.options_img)
        self.canvas.tag_bind(self.options_button, "<Button-1>", lambda event: controller.show_frame("Menu"))
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


class Menu(tk.Frame):
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
        self.MainScreen_img = PhotoImage(file=r"images\Buttons\MainScreen.png")
        self.MainScreen_button = self.canvas.create_image(100, 30, image=self.MainScreen_img)
        self.canvas.tag_bind(self.MainScreen_button, "<Button-1>", lambda event: controller.show_frame("Frame1_1"))
        self.SetpointPlanner_img = PhotoImage(file=r"images\Buttons\SetpointPlanner.png")
        self.SetpointPlanner_button = self.canvas.create_image(100, 90, image=self.SetpointPlanner_img)
        self.canvas.tag_bind(self.SetpointPlanner_button, "<Button-1>", lambda event: controller.show_frame("Frame2"))
        self.Monitoring_img = PhotoImage(file=r"images\Buttons\Monitoring.png")
        self.Monitoring_button = self.canvas.create_image(100, 150, image=self.Monitoring_img)
        self.canvas.tag_bind(self.Monitoring_button, "<Button-1>", lambda event: controller.show_frame("Frame3"))
        self.Journal_img = PhotoImage(file=r"images\Buttons\Journal.png")
        self.Journal_button = self.canvas.create_image(100, 210, image=self.Journal_img)
        self.canvas.tag_bind(self.Journal_button, "<Button-1>", lambda event: controller.show_frame("Frame6"))
        self.StationSettings_img = PhotoImage(file=r"images\Buttons\StationSettings.png")
        self.StationSettings_button = self.canvas.create_image(100, 270, image=self.StationSettings_img)
        self.canvas.tag_bind(self.StationSettings_button, "<Button-1>", lambda event: controller.show_frame("Frame9"))
        self.EngineeringMenu_img = PhotoImage(file=r"images\Buttons\EngineeringMenu.png")
        self.EngineeringMenu_button = self.canvas.create_image(100, 330, image=self.EngineeringMenu_img)
        self.canvas.tag_bind(self.EngineeringMenu_button, "<Button-1>", lambda event: controller.show_frame("Frame16"))
        self.PanelSettings_img = PhotoImage(file=r"images\Buttons\PanelSettings.png")
        self.PanelSettings_button = self.canvas.create_image(100, 390, image=self.PanelSettings_img)
        self.canvas.tag_bind(self.PanelSettings_button, "<Button-1>", lambda event: controller.show_frame("Frame19"))
        self.Contacts_img = PhotoImage(file=r"images\Buttons\Contacts.png")
        self.Contacts_button = self.canvas.create_image(100, 450, image=self.Contacts_img)
        self.canvas.tag_bind(self.Contacts_button, "<Button-1>", lambda event: controller.show_frame("Frame20"))
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

        self.InterfaceScreen_img = PhotoImage(file=r"images\SetpointPlannerScreen\Interface.png")
        self.InterfaceScreen = self.canvas.create_image(500, 250, image=self.InterfaceScreen_img)
        self.day1_img = PhotoImage(file=r"images\SetpointPlannerScreen\day_1.png")
        self.day1_button = self.canvas.create_image(535, 130, image=self.day1_img)
        self.day2_img = PhotoImage(file=r"images\SetpointPlannerScreen\day_2.png")
        self.day2_button = self.canvas.create_image(575, 130, image=self.day2_img)
        self.day3_img = PhotoImage(file=r"images\SetpointPlannerScreen\day_3.png")
        self.day3_button = self.canvas.create_image(615, 130, image=self.day3_img)
        self.day4_img = PhotoImage(file=r"images\SetpointPlannerScreen\day_4.png")
        self.day4_button = self.canvas.create_image(655, 130, image=self.day4_img)
        self.day5_img = PhotoImage(file=r"images\SetpointPlannerScreen\day_5.png")
        self.day5_button = self.canvas.create_image(695, 130, image=self.day5_img)
        self.day6_img = PhotoImage(file=r"images\SetpointPlannerScreen\day_6.png")
        self.day6_button = self.canvas.create_image(735, 130, image=self.day6_img)
        self.day7_img = PhotoImage(file=r"images\SetpointPlannerScreen\day_7.png")
        self.day7_button = self.canvas.create_image(775, 130, image=self.day7_img)



        self.clock_label = tk.Label(self.canvas, text="", fg='white', bg='black', font=('Roboto Bold', 12))
        self.clock_label.place(x=680, y=5)
        self.MainScreen_img = PhotoImage(file=r"images\Buttons\MainScreen.png")
        self.MainScreen_button = self.canvas.create_image(100, 30, image=self.MainScreen_img)
        self.canvas.tag_bind(self.MainScreen_button, "<Button-1>", lambda event: controller.show_frame("Frame1_1"))
        self.SetpointPlanner_img = PhotoImage(file=r"images\Buttons\SetpointPlannerOpen.png")
        self.SetpointPlanner_button = self.canvas.create_image(100, 90, image=self.SetpointPlanner_img)
        self.Monitoring_img = PhotoImage(file=r"images\Buttons\Monitoring.png")
        self.Monitoring_button = self.canvas.create_image(100, 150, image=self.Monitoring_img)
        self.canvas.tag_bind(self.Monitoring_button, "<Button-1>", lambda event: controller.show_frame("Frame3"))
        self.Journal_img = PhotoImage(file=r"images\Buttons\Journal.png")
        self.Journal_button = self.canvas.create_image(100, 210, image=self.Journal_img)
        self.canvas.tag_bind(self.Journal_button, "<Button-1>", lambda event: controller.show_frame("Frame6"))
        self.StationSettings_img = PhotoImage(file=r"images\Buttons\StationSettings.png")
        self.StationSettings_button = self.canvas.create_image(100, 270, image=self.StationSettings_img)
        self.canvas.tag_bind(self.StationSettings_button, "<Button-1>", lambda event: controller.show_frame("Frame9"))
        self.EngineeringMenu_img = PhotoImage(file=r"images\Buttons\EngineeringMenu.png")
        self.EngineeringMenu_button = self.canvas.create_image(100, 330, image=self.EngineeringMenu_img)
        self.canvas.tag_bind(self.EngineeringMenu_button, "<Button-1>", lambda event: controller.show_frame("Frame16"))
        self.PanelSettings_img = PhotoImage(file=r"images\Buttons\PanelSettings.png")
        self.PanelSettings_button = self.canvas.create_image(100, 390, image=self.PanelSettings_img)
        self.canvas.tag_bind(self.PanelSettings_button, "<Button-1>", lambda event: controller.show_frame("Frame19"))
        self.Contacts_img = PhotoImage(file=r"images\Buttons\Contacts.png")
        self.Contacts_button = self.canvas.create_image(100, 450, image=self.Contacts_img)
        self.canvas.tag_bind(self.Contacts_button, "<Button-1>", lambda event: controller.show_frame("Frame20"))

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

        self.MainScreen_img = PhotoImage(file=r"images\Buttons\MainScreen.png")
        self.MainScreen_button = self.canvas.create_image(100, 30, image=self.MainScreen_img)
        self.canvas.tag_bind(self.MainScreen_button, "<Button-1>", lambda event: controller.show_frame("Frame1_1"))
        self.Back_img = PhotoImage(file=r"images\Buttons\Back.png")
        self.Back_button = self.canvas.create_image(100, 90, image=self.Back_img)
        self.canvas.tag_bind(self.Back_button, "<Button-1>", lambda event: controller.show_frame("Menu"))
        self.TO_img = PhotoImage(file=r"images\Buttons\TrendsOnlineOPEN.png")
        self.TO_button = self.canvas.create_image(100, 150, image=self.TO_img)
        self.TS_img = PhotoImage(file=r"images\Buttons\TrendingStories.png")
        self.TS_button = self.canvas.create_image(100, 210, image=self.TS_img)
        self.canvas.tag_bind(self.TS_button, "<Button-1>", lambda event: controller.show_frame("Frame4"))
        self.Pumps_img = PhotoImage(file=r"images\Buttons\OperatingTimeOfPumps.png")
        self.Pumps_button = self.canvas.create_image(100, 270, image=self.Pumps_img)
        self.canvas.tag_bind(self.Pumps_button, "<Button-1>", lambda event: controller.show_frame("Frame5"))

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

        self.MainScreen_img = PhotoImage(file=r"images\Buttons\MainScreen.png")
        self.MainScreen_button = self.canvas.create_image(100, 30, image=self.MainScreen_img)
        self.canvas.tag_bind(self.MainScreen_button, "<Button-1>", lambda event: controller.show_frame("Frame1_1"))
        self.Back_img = PhotoImage(file=r"images\Buttons\Back.png")
        self.Back_button = self.canvas.create_image(100, 90, image=self.Back_img)
        self.canvas.tag_bind(self.Back_button, "<Button-1>", lambda event: controller.show_frame("Frame3"))

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

        self.MainScreen_img = PhotoImage(file=r"images\Buttons\MainScreen.png")
        self.MainScreen_button = self.canvas.create_image(100, 30, image=self.MainScreen_img)
        self.canvas.tag_bind(self.MainScreen_button, "<Button-1>", lambda event: controller.show_frame("Frame1_1"))
        self.Back_img = PhotoImage(file=r"images\Buttons\Back.png")
        self.Back_button = self.canvas.create_image(100, 90, image=self.Back_img)
        self.canvas.tag_bind(self.Back_button, "<Button-1>", lambda event: controller.show_frame("Menu"))
        self.TO_img = PhotoImage(file=r"images\Buttons\TrendsOnline.png")
        self.TO_button = self.canvas.create_image(100, 150, image=self.TO_img)
        self.canvas.tag_bind(self.TO_button, "<Button-1>", lambda event: controller.show_frame("Frame3"))
        self.TS_img = PhotoImage(file=r"images\Buttons\TrendingStories.png")
        self.TS_button = self.canvas.create_image(100, 210, image=self.TS_img)
        self.canvas.tag_bind(self.TS_button, "<Button-1>", lambda event: controller.show_frame("Frame4"))
        self.Pumps_img = PhotoImage(file=r"images\Buttons\OperatingTimeOfPumpsOPEN.png")
        self.Pumps_button = self.canvas.create_image(100, 270, image=self.Pumps_img)


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

        self.MainScreen_img = PhotoImage(file=r"images\Buttons\MainScreen.png")
        self.MainScreen_button = self.canvas.create_image(100, 30, image=self.MainScreen_img)
        self.canvas.tag_bind(self.MainScreen_button, "<Button-1>", lambda event: controller.show_frame("Frame1_1"))
        self.Back_img = PhotoImage(file=r"images\Buttons\Back.png")
        self.Back_button = self.canvas.create_image(100, 90, image=self.Back_img)
        self.canvas.tag_bind(self.Back_button, "<Button-1>", lambda event: controller.show_frame("Menu"))
        self.NowEvents_img = PhotoImage(file=r"images\Buttons\NowEventsOpen.png")
        self.NowEvents_button = self.canvas.create_image(100, 150, image=self.NowEvents_img)
        self.JournalHistory_img = PhotoImage(file=r"images\Buttons\JournalHistory.png")
        self.JournalHistory_button = self.canvas.create_image(100, 210, image=self.JournalHistory_img)
        self.canvas.tag_bind(self.JournalHistory_button, "<Button-1>", lambda event: controller.show_frame("Frame7"))
        self.JournalEdits_img = PhotoImage(file=r"images\Buttons\JournalEdits.png")
        self.JournalEdits_button = self.canvas.create_image(100, 270, image=self.JournalEdits_img)
        self.canvas.tag_bind(self.JournalEdits_button, "<Button-1>", lambda event: controller.show_frame("Frame8"))

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

        self.MainScreen_img = PhotoImage(file=r"images\Buttons\MainScreen.png")
        self.MainScreen_button = self.canvas.create_image(100, 30, image=self.MainScreen_img)
        self.canvas.tag_bind(self.MainScreen_button, "<Button-1>", lambda event: controller.show_frame("Frame1_1"))
        self.Back_img = PhotoImage(file=r"images\Buttons\Back.png")
        self.Back_button = self.canvas.create_image(100, 90, image=self.Back_img)
        self.canvas.tag_bind(self.Back_button, "<Button-1>", lambda event: controller.show_frame("Frame6"))


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

        self.MainScreen_img = PhotoImage(file=r"images\Buttons\MainScreen.png")
        self.MainScreen_button = self.canvas.create_image(100, 30, image=self.MainScreen_img)
        self.canvas.tag_bind(self.MainScreen_button, "<Button-1>", lambda event: controller.show_frame("Frame1_1"))
        self.Back_img = PhotoImage(file=r"images\Buttons\Back.png")
        self.Back_button = self.canvas.create_image(100, 90, image=self.Back_img)
        self.canvas.tag_bind(self.Back_button, "<Button-1>", lambda event: controller.show_frame("Frame6"))
        self.NowEvents_img = PhotoImage(file=r"images\Buttons\NowEvents.png")
        self.NowEvents_button = self.canvas.create_image(100, 150, image=self.NowEvents_img)
        self.canvas.tag_bind(self.NowEvents_button, "<Button-1>", lambda event: controller.show_frame("Frame6"))
        self.JournalHistory_img = PhotoImage(file=r"images\Buttons\JournalHistory.png")
        self.JournalHistory_button = self.canvas.create_image(100, 210, image=self.JournalHistory_img)
        self.canvas.tag_bind(self.JournalHistory_button, "<Button-1>", lambda event: controller.show_frame("Frame7"))
        self.JournalEdits_img = PhotoImage(file=r"images\Buttons\JournalEditsOpen.png")
        self.JournalEdits_button = self.canvas.create_image(100, 270, image=self.JournalEdits_img)

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

        self.MainScreen_img = PhotoImage(file=r"images\StationSettings\MainScreen.png")
        self.MainScreen_button = self.canvas.create_image(100, 0+30, image=self.MainScreen_img)
        self.canvas.tag_bind(self.MainScreen_button, "<Button-1>", lambda event: controller.show_frame("Frame1_1"))

        self.BackToMenu_img = PhotoImage(file=r"images\StationSettings\Back.png")
        self.BackToMenu_button = self.canvas.create_image(100, 56.4+30, image=self.BackToMenu_img)
        self.canvas.tag_bind(self.BackToMenu_button, "<Button-1>", lambda event: controller.show_frame("Menu"))

        self.EngineParameters_img = PhotoImage(file=r"images\StationSettings\EngineParameters1_1.png")
        self.EngineParameters_button = self.canvas.create_image(100, 107.4+30, image=self.EngineParameters_img)

        self.SensorSettings_img = PhotoImage(file=r"images\StationSettings\SensorSettings1_0.png")
        self.SensorSettings_button = self.canvas.create_image(100, 160.4+30, image=self.SensorSettings_img)
        self.canvas.tag_bind(self.SensorSettings_button, "<Button-1>", lambda event: controller.show_frame("Frame10"))

        self.PumpParametersInGeneral_img = PhotoImage(file=r"images\StationSettings\PumpParametersInGeneral1_0.png")
        self.PumpParametersInGeneral_button = self.canvas.create_image(100, 211.4+30, image=self.PumpParametersInGeneral_img)
        self.canvas.tag_bind(self.PumpParametersInGeneral_button, "<Button-1>", lambda event: controller.show_frame("Frame11"))

        self.OnAdditionalPumps_img = PhotoImage(file=r"images\StationSettings\OnAdditionalPumps1_0.png")
        self.OnAdditionalPumps_button = self.canvas.create_image(100, 264.4+30, image=self.OnAdditionalPumps_img)
        self.canvas.tag_bind(self.OnAdditionalPumps_button, "<Button-1>", lambda event: controller.show_frame("Frame12"))

        self.OffOfAdditionalPumps_img = PhotoImage(file=r"images\StationSettings\OffOfAdditionalPumps1_0.png")
        self.OffOfAdditionalPumps_button = self.canvas.create_image(100, 315.4+30, image=self.OffOfAdditionalPumps_img)
        self.canvas.tag_bind(self.OffOfAdditionalPumps_button, "<Button-1>", lambda event: controller.show_frame("Frame13"))

        self.Options_img = PhotoImage(file=r"images\StationSettings\Options1_0.png")
        self.Options_button = self.canvas.create_image(100, 368.4+30, image=self.Options_img)
        self.canvas.tag_bind(self.Options_button, "<Button-1>", lambda event: controller.show_frame("Frame14"))

        self.EmergencyModes_img = PhotoImage(file=r"images\StationSettings\EmergencyModes1_0.png")
        self.EmergencyModes_button = self.canvas.create_image(100, 419.4+30, image=self.EmergencyModes_img)
        self.canvas.tag_bind(self.EmergencyModes_button, "<Button-1>", lambda event: controller.show_frame("Frame15"))

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

        self.MainScreen_img = PhotoImage(file=r"images\StationSettings\MainScreen.png")
        self.MainScreen_button = self.canvas.create_image(100, 0 + 30, image=self.MainScreen_img)
        self.canvas.tag_bind(self.MainScreen_button, "<Button-1>", lambda event: controller.show_frame("Frame1_1"))

        self.BackToMenu_img = PhotoImage(file=r"images\StationSettings\Back.png")
        self.BackToMenu_button = self.canvas.create_image(100, 56.4 + 30, image=self.BackToMenu_img)
        self.canvas.tag_bind(self.BackToMenu_button, "<Button-1>", lambda event: controller.show_frame("Menu"))

        self.EngineParameters_img = PhotoImage(file=r"images\StationSettings\EngineParameters1_0.png")
        self.EngineParameters_button = self.canvas.create_image(100, 107.4 + 30, image=self.EngineParameters_img)
        self.canvas.tag_bind(self.EngineParameters_button, "<Button-1>", lambda event: controller.show_frame("Frame9"))

        self.SensorSettings_img = PhotoImage(file=r"images\StationSettings\SensorSettings1_1.png")
        self.SensorSettings_button = self.canvas.create_image(100, 160.4 + 30, image=self.SensorSettings_img)

        self.PumpParametersInGeneral_img = PhotoImage(file=r"images\StationSettings\PumpParametersInGeneral1_0.png")
        self.PumpParametersInGeneral_button = self.canvas.create_image(100, 211.4 + 30, image=self.PumpParametersInGeneral_img)
        self.canvas.tag_bind(self.PumpParametersInGeneral_button, "<Button-1>", lambda event: controller.show_frame("Frame11"))

        self.OnAdditionalPumps_img = PhotoImage(file=r"images\StationSettings\OnAdditionalPumps1_0.png")
        self.OnAdditionalPumps_button = self.canvas.create_image(100, 264.4 + 30, image=self.OnAdditionalPumps_img)
        self.canvas.tag_bind(self.OnAdditionalPumps_button, "<Button-1>", lambda event: controller.show_frame("Frame12"))

        self.OffOfAdditionalPumps_img = PhotoImage(file=r"images\StationSettings\OffOfAdditionalPumps1_0.png")
        self.OffOfAdditionalPumps_button = self.canvas.create_image(100, 315.4 + 30, image=self.OffOfAdditionalPumps_img)
        self.canvas.tag_bind(self.OffOfAdditionalPumps_button, "<Button-1>", lambda event: controller.show_frame("Frame13"))

        self.Options_img = PhotoImage(file=r"images\StationSettings\Options1_0.png")
        self.Options_button = self.canvas.create_image(100, 368.4 + 30, image=self.Options_img)
        self.canvas.tag_bind(self.Options_button, "<Button-1>", lambda event: controller.show_frame("Frame14"))

        self.EmergencyModes_img = PhotoImage(file=r"images\StationSettings\EmergencyModes1_0.png")
        self.EmergencyModes_button = self.canvas.create_image(100, 419.4 + 30, image=self.EmergencyModes_img)
        self.canvas.tag_bind(self.EmergencyModes_button, "<Button-1>", lambda event: controller.show_frame("Frame15"))

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

        self.MainScreen_img = PhotoImage(file=r"images\StationSettings\MainScreen.png")
        self.MainScreen_button = self.canvas.create_image(100, 0 + 30, image=self.MainScreen_img)
        self.canvas.tag_bind(self.MainScreen_button, "<Button-1>", lambda event: controller.show_frame("Frame1_1"))

        self.BackToMenu_img = PhotoImage(file=r"images\StationSettings\Back.png")
        self.BackToMenu_button = self.canvas.create_image(100, 56.4 + 30, image=self.BackToMenu_img)
        self.canvas.tag_bind(self.BackToMenu_button, "<Button-1>", lambda event: controller.show_frame("Menu"))

        self.EngineParameters_img = PhotoImage(file=r"images\StationSettings\EngineParameters1_0.png")
        self.EngineParameters_button = self.canvas.create_image(100, 107.4 + 30, image=self.EngineParameters_img)
        self.canvas.tag_bind(self.EngineParameters_button, "<Button-1>", lambda event: controller.show_frame("Frame9"))

        self.SensorSettings_img = PhotoImage(file=r"images\StationSettings\SensorSettings1_0.png")
        self.SensorSettings_button = self.canvas.create_image(100, 160.4 + 30, image=self.SensorSettings_img)
        self.canvas.tag_bind(self.SensorSettings_button, "<Button-1>", lambda event: controller.show_frame("Frame10"))

        self.PumpParametersInGeneral_img = PhotoImage(file=r"images\StationSettings\PumpParametersInGeneral1_1.png")
        self.PumpParametersInGeneral_button = self.canvas.create_image(100, 211.4 + 30, image=self.PumpParametersInGeneral_img)

        self.OnAdditionalPumps_img = PhotoImage(file=r"images\StationSettings\OnAdditionalPumps1_0.png")
        self.OnAdditionalPumps_button = self.canvas.create_image(100, 264.4 + 30, image=self.OnAdditionalPumps_img)
        self.canvas.tag_bind(self.OnAdditionalPumps_button, "<Button-1>", lambda event: controller.show_frame("Frame12"))

        self.OffOfAdditionalPumps_img = PhotoImage(file=r"images\StationSettings\OffOfAdditionalPumps1_0.png")
        self.OffOfAdditionalPumps_button = self.canvas.create_image(100, 315.4 + 30, image=self.OffOfAdditionalPumps_img)
        self.canvas.tag_bind(self.OffOfAdditionalPumps_button, "<Button-1>", lambda event: controller.show_frame("Frame13"))

        self.Options_img = PhotoImage(file=r"images\StationSettings\Options1_0.png")
        self.Options_button = self.canvas.create_image(100, 368.4 + 30, image=self.Options_img)
        self.canvas.tag_bind(self.Options_button, "<Button-1>", lambda event: controller.show_frame("Frame14"))

        self.EmergencyModes_img = PhotoImage(file=r"images\StationSettings\EmergencyModes1_0.png")
        self.EmergencyModes_button = self.canvas.create_image(100, 419.4 + 30, image=self.EmergencyModes_img)
        self.canvas.tag_bind(self.EmergencyModes_button, "<Button-1>", lambda event: controller.show_frame("Frame15"))

        self.InterfaceScreen_img = PhotoImage(file=r"images\StationSettings\ParametersOfTheDrivePump.png")
        self.InterfaceScreen = self.canvas.create_image(500, 200, image=self.InterfaceScreen_img)

        self.Switch_Flat_first_img = PhotoImage(file=r"images\StationSettings\Switch-0.png")
        self.Switch_Flat_first_button = self.canvas.create_image(670, 176, image=self.Switch_Flat_first_img)
        self.canvas.tag_bind(self.Switch_Flat_first_button, "<Button-1>", self.update_switch_first)

        self.Switch_Flat_second_img = PhotoImage(file=r"images\StationSettings\Switch-0.png")
        self.Switch_Flat_second_button = self.canvas.create_image(670, 218, image=self.Switch_Flat_second_img)
        self.canvas.tag_bind(self.Switch_Flat_second_button, "<Button-1>", self.update_switch_second)


    def update_switch_first(self, event):
        if self.Switch_Flat_first_img.cget("file") == "images\StationSettings\Switch-0.png":
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

        self.MainScreen_img = PhotoImage(file=r"images\StationSettings\MainScreen.png")
        self.MainScreen_button = self.canvas.create_image(100, 0 + 30, image=self.MainScreen_img)
        self.canvas.tag_bind(self.MainScreen_button, "<Button-1>", lambda event: controller.show_frame("Frame1_1"))

        self.BackToMenu_img = PhotoImage(file=r"images\StationSettings\Back.png")
        self.BackToMenu_button = self.canvas.create_image(100, 56.4 + 30, image=self.BackToMenu_img)
        self.canvas.tag_bind(self.BackToMenu_button, "<Button-1>", lambda event: controller.show_frame("Menu"))

        self.EngineParameters_img = PhotoImage(file=r"images\StationSettings\EngineParameters1_0.png")
        self.EngineParameters_button = self.canvas.create_image(100, 107.4 + 30, image=self.EngineParameters_img)
        self.canvas.tag_bind(self.EngineParameters_button, "<Button-1>", lambda event: controller.show_frame("Frame9"))

        self.SensorSettings_img = PhotoImage(file=r"images\StationSettings\SensorSettings1_0.png")
        self.SensorSettings_button = self.canvas.create_image(100, 160.4 + 30, image=self.SensorSettings_img)
        self.canvas.tag_bind(self.SensorSettings_button, "<Button-1>", lambda event: controller.show_frame("Frame10"))

        self.PumpParametersInGeneral_img = PhotoImage(file=r"images\StationSettings\PumpParametersInGeneral1_0.png")
        self.PumpParametersInGeneral_button = self.canvas.create_image(100, 211.4 + 30, image=self.PumpParametersInGeneral_img)
        self.canvas.tag_bind(self.PumpParametersInGeneral_button, "<Button-1>", lambda event: controller.show_frame("Frame11"))

        self.OnAdditionalPumps_img = PhotoImage(file=r"images\StationSettings\OnAdditionalPumps1_1.png")
        self.OnAdditionalPumps_button = self.canvas.create_image(100, 264.4 + 30, image=self.OnAdditionalPumps_img)

        self.OffOfAdditionalPumps_img = PhotoImage(file=r"images\StationSettings\OffOfAdditionalPumps1_0.png")
        self.OffOfAdditionalPumps_button = self.canvas.create_image(100, 315.4 + 30, image=self.OffOfAdditionalPumps_img)
        self.canvas.tag_bind(self.OffOfAdditionalPumps_button, "<Button-1>", lambda event: controller.show_frame("Frame13"))

        self.Options_img = PhotoImage(file=r"images\StationSettings\Options1_0.png")
        self.Options_button = self.canvas.create_image(100, 368.4 + 30, image=self.Options_img)
        self.canvas.tag_bind(self.Options_button, "<Button-1>", lambda event: controller.show_frame("Frame14"))

        self.EmergencyModes_img = PhotoImage(file=r"images\StationSettings\EmergencyModes1_0.png")
        self.EmergencyModes_button = self.canvas.create_image(100, 419.4 + 30, image=self.EmergencyModes_img)
        self.canvas.tag_bind(self.EmergencyModes_button, "<Button-1>", lambda event: controller.show_frame("Frame15"))

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

        self.MainScreen_img = PhotoImage(file=r"images\StationSettings\MainScreen.png")
        self.MainScreen_button = self.canvas.create_image(100, 0 + 30, image=self.MainScreen_img)
        self.canvas.tag_bind(self.MainScreen_button, "<Button-1>", lambda event: controller.show_frame("Frame1_1"))

        self.BackToMenu_img = PhotoImage(file=r"images\StationSettings\Back.png")
        self.BackToMenu_button = self.canvas.create_image(100, 56.4 + 30, image=self.BackToMenu_img)
        self.canvas.tag_bind(self.BackToMenu_button, "<Button-1>", lambda event: controller.show_frame("Menu"))

        self.EngineParameters_img = PhotoImage(file=r"images\StationSettings\EngineParameters1_0.png")
        self.EngineParameters_button = self.canvas.create_image(100, 107.4 + 30, image=self.EngineParameters_img)
        self.canvas.tag_bind(self.EngineParameters_button, "<Button-1>", lambda event: controller.show_frame("Frame9"))

        self.SensorSettings_img = PhotoImage(file=r"images\StationSettings\SensorSettings1_0.png")
        self.SensorSettings_button = self.canvas.create_image(100, 160.4 + 30, image=self.SensorSettings_img)
        self.canvas.tag_bind(self.SensorSettings_button, "<Button-1>", lambda event: controller.show_frame("Frame10"))

        self.PumpParametersInGeneral_img = PhotoImage(file=r"images\StationSettings\PumpParametersInGeneral1_0.png")
        self.PumpParametersInGeneral_button = self.canvas.create_image(100, 211.4 + 30, image=self.PumpParametersInGeneral_img)
        self.canvas.tag_bind(self.PumpParametersInGeneral_button, "<Button-1>", lambda event: controller.show_frame("Frame11"))

        self.OnAdditionalPumps_img = PhotoImage(file=r"images\StationSettings\OnAdditionalPumps1_0.png")
        self.OnAdditionalPumps_button = self.canvas.create_image(100, 264.4 + 30, image=self.OnAdditionalPumps_img)
        self.canvas.tag_bind(self.OnAdditionalPumps_button, "<Button-1>", lambda event: controller.show_frame("Frame12"))

        self.OffOfAdditionalPumps_img = PhotoImage(file=r"images\StationSettings\OffOfAdditionalPumps1_1.png")
        self.OffOfAdditionalPumps_button = self.canvas.create_image(100, 315.4 + 30, image=self.OffOfAdditionalPumps_img)

        self.Options_img = PhotoImage(file=r"images\StationSettings\Options1_0.png")
        self.Options_button = self.canvas.create_image(100, 368.4 + 30, image=self.Options_img)
        self.canvas.tag_bind(self.Options_button, "<Button-1>", lambda event: controller.show_frame("Frame14"))

        self.EmergencyModes_img = PhotoImage(file=r"images\StationSettings\EmergencyModes1_0.png")
        self.EmergencyModes_button = self.canvas.create_image(100, 419.4 + 30, image=self.EmergencyModes_img)
        self.canvas.tag_bind(self.EmergencyModes_button, "<Button-1>", lambda event: controller.show_frame("Frame15"))

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

        self.MainScreen_img = PhotoImage(file=r"images\StationSettings\MainScreen.png")
        self.MainScreen_button = self.canvas.create_image(100, 0 + 30, image=self.MainScreen_img)
        self.canvas.tag_bind(self.MainScreen_button, "<Button-1>", lambda event: controller.show_frame("Frame1_1"))

        self.BackToMenu_img = PhotoImage(file=r"images\StationSettings\Back.png")
        self.BackToMenu_button = self.canvas.create_image(100, 56.4 + 30, image=self.BackToMenu_img)
        self.canvas.tag_bind(self.BackToMenu_button, "<Button-1>", lambda event: controller.show_frame("Menu"))

        self.EngineParameters_img = PhotoImage(file=r"images\StationSettings\EngineParameters1_0.png")
        self.EngineParameters_button = self.canvas.create_image(100, 107.4 + 30, image=self.EngineParameters_img)
        self.canvas.tag_bind(self.EngineParameters_button, "<Button-1>", lambda event: controller.show_frame("Frame9"))

        self.SensorSettings_img = PhotoImage(file=r"images\StationSettings\SensorSettings1_0.png")
        self.SensorSettings_button = self.canvas.create_image(100, 160.4 + 30, image=self.SensorSettings_img)
        self.canvas.tag_bind(self.SensorSettings_button, "<Button-1>", lambda event: controller.show_frame("Frame10"))

        self.PumpParametersInGeneral_img = PhotoImage(file=r"images\StationSettings\PumpParametersInGeneral1_0.png")
        self.PumpParametersInGeneral_button = self.canvas.create_image(100, 211.4 + 30, image=self.PumpParametersInGeneral_img)
        self.canvas.tag_bind(self.PumpParametersInGeneral_button, "<Button-1>", lambda event: controller.show_frame("Frame11"))

        self.OnAdditionalPumps_img = PhotoImage(file=r"images\StationSettings\OnAdditionalPumps1_0.png")
        self.OnAdditionalPumps_button = self.canvas.create_image(100, 264.4 + 30, image=self.OnAdditionalPumps_img)
        self.canvas.tag_bind(self.OnAdditionalPumps_button, "<Button-1>", lambda event: controller.show_frame("Frame12"))

        self.OffOfAdditionalPumps_img = PhotoImage(file=r"images\StationSettings\OffOfAdditionalPumps1_0.png")
        self.OffOfAdditionalPumps_button = self.canvas.create_image(100, 315.4 + 30, image=self.OffOfAdditionalPumps_img)
        self.canvas.tag_bind(self.OffOfAdditionalPumps_button, "<Button-1>", lambda event: controller.show_frame("Frame13"))

        self.Options_img = PhotoImage(file=r"images\StationSettings\Options1_1.png")
        self.Options_button = self.canvas.create_image(100, 368.4 + 30, image=self.Options_img)

        self.EmergencyModes_img = PhotoImage(file=r"images\StationSettings\EmergencyModes1_0.png")
        self.EmergencyModes_button = self.canvas.create_image(100, 419.4 + 30, image=self.EmergencyModes_img)
        self.canvas.tag_bind(self.EmergencyModes_button, "<Button-1>", lambda event: controller.show_frame("Frame15"))

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

        self.MainScreen_img = PhotoImage(file=r"images\StationSettings\MainScreen.png")
        self.MainScreen_button = self.canvas.create_image(100, 0 + 30, image=self.MainScreen_img)
        self.canvas.tag_bind(self.MainScreen_button, "<Button-1>", lambda event: controller.show_frame("Frame1_1"))

        self.BackToMenu_img = PhotoImage(file=r"images\StationSettings\Back.png")
        self.BackToMenu_button = self.canvas.create_image(100, 56.4 + 30, image=self.BackToMenu_img)
        self.canvas.tag_bind(self.BackToMenu_button, "<Button-1>", lambda event: controller.show_frame("Menu"))

        self.EngineParameters_img = PhotoImage(file=r"images\StationSettings\EngineParameters1_0.png")
        self.EngineParameters_button = self.canvas.create_image(100, 107.4 + 30, image=self.EngineParameters_img)
        self.canvas.tag_bind(self.EngineParameters_button, "<Button-1>", lambda event: controller.show_frame("Frame9"))

        self.SensorSettings_img = PhotoImage(file=r"images\StationSettings\SensorSettings1_0.png")
        self.SensorSettings_button = self.canvas.create_image(100, 160.4 + 30, image=self.SensorSettings_img)
        self.canvas.tag_bind(self.SensorSettings_button, "<Button-1>", lambda event: controller.show_frame("Frame10"))

        self.PumpParametersInGeneral_img = PhotoImage(file=r"images\StationSettings\PumpParametersInGeneral1_0.png")
        self.PumpParametersInGeneral_button = self.canvas.create_image(100, 211.4 + 30, image=self.PumpParametersInGeneral_img)
        self.canvas.tag_bind(self.PumpParametersInGeneral_button, "<Button-1>", lambda event: controller.show_frame("Frame11"))

        self.OnAdditionalPumps_img = PhotoImage(file=r"images\StationSettings\OnAdditionalPumps1_0.png")
        self.OnAdditionalPumps_button = self.canvas.create_image(100, 264.4 + 30, image=self.OnAdditionalPumps_img)
        self.canvas.tag_bind(self.OnAdditionalPumps_button, "<Button-1>", lambda event: controller.show_frame("Frame12"))

        self.OffOfAdditionalPumps_img = PhotoImage(file=r"images\StationSettings\OffOfAdditionalPumps1_0.png")
        self.OffOfAdditionalPumps_button = self.canvas.create_image(100, 315.4 + 30, image=self.OffOfAdditionalPumps_img)
        self.canvas.tag_bind(self.OffOfAdditionalPumps_button, "<Button-1>", lambda event: controller.show_frame("Frame13"))

        self.Options_img = PhotoImage(file=r"images\StationSettings\Options1_0.png")
        self.Options_button = self.canvas.create_image(100, 368.4 + 30, image=self.Options_img)
        self.canvas.tag_bind(self.Options_button, "<Button-1>", lambda event: controller.show_frame("Frame14"))

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

        self.MainScreen_img = PhotoImage(file=r"images\Buttons\MainScreen.png")
        self.MainScreen_button = self.canvas.create_image(100, 30, image=self.MainScreen_img)
        self.canvas.tag_bind(self.MainScreen_button, "<Button-1>", lambda event: controller.show_frame("Frame1_1"))
        self.Back_img = PhotoImage(file=r"images\Buttons\Back.png")
        self.Back_button = self.canvas.create_image(100, 90, image=self.Back_img)
        self.canvas.tag_bind(self.Back_button, "<Button-1>", lambda event: controller.show_frame("Menu"))
        self.PID_img = PhotoImage(file=r"images\Buttons\pidOPEN.png")
        self.PID_button = self.canvas.create_image(100, 150, image=self.PID_img)
        self.PLC_img = PhotoImage(file=r"images\Buttons\plc.png")
        self.PLC_button = self.canvas.create_image(100, 210, image=self.PLC_img)
        self.canvas.tag_bind(self.PLC_button, "<Button-1>", lambda event: controller.show_frame("Frame17"))
        self.Backup_img = PhotoImage(file=r"images\Buttons\Backup.png")
        self.Backup_button = self.canvas.create_image(100, 270, image=self.Backup_img)
        self.canvas.tag_bind(self.Backup_button, "<Button-1>", lambda event: controller.show_frame("Frame18"))


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

        self.MainScreen_img = PhotoImage(file=r"images\Buttons\MainScreen.png")
        self.MainScreen_button = self.canvas.create_image(100, 30, image=self.MainScreen_img)
        self.canvas.tag_bind(self.MainScreen_button, "<Button-1>", lambda event: controller.show_frame("Frame1_1"))
        self.Back_img = PhotoImage(file=r"images\Buttons\Back.png")
        self.Back_button = self.canvas.create_image(100, 90, image=self.Back_img)
        self.canvas.tag_bind(self.Back_button, "<Button-1>", lambda event: controller.show_frame("Menu"))
        self.PID_img = PhotoImage(file=r"images\Buttons\pid.png")
        self.PID_button = self.canvas.create_image(100, 150, image=self.PID_img)
        self.canvas.tag_bind(self.PID_button, "<Button-1>", lambda event: controller.show_frame("Frame16"))
        self.PLC_img = PhotoImage(file=r"images\Buttons\plcOPEN.png")
        self.PLC_button = self.canvas.create_image(100, 210, image=self.PLC_img)
        self.Backup_img = PhotoImage(file=r"images\Buttons\Backup.png")
        self.Backup_button = self.canvas.create_image(100, 270, image=self.Backup_img)
        self.canvas.tag_bind(self.Backup_button, "<Button-1>", lambda event: controller.show_frame("Frame18"))

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

        self.MainScreen_img = PhotoImage(file=r"images\Buttons\MainScreen.png")
        self.MainScreen_button = self.canvas.create_image(100, 30, image=self.MainScreen_img)
        self.canvas.tag_bind(self.MainScreen_button, "<Button-1>", lambda event: controller.show_frame("Frame1_1"))
        self.Back_img = PhotoImage(file=r"images\Buttons\Back.png")
        self.Back_button = self.canvas.create_image(100, 90, image=self.Back_img)
        self.canvas.tag_bind(self.Back_button, "<Button-1>", lambda event: controller.show_frame("Menu"))
        self.PID_img = PhotoImage(file=r"images\Buttons\pid.png")
        self.PID_button = self.canvas.create_image(100, 150, image=self.PID_img)
        self.canvas.tag_bind(self.PID_button, "<Button-1>", lambda event: controller.show_frame("Frame16"))
        self.PLC_img = PhotoImage(file=r"images\Buttons\plc.png")
        self.PLC_button = self.canvas.create_image(100, 210, image=self.PLC_img)
        self.canvas.tag_bind(self.PLC_button, "<Button-1>", lambda event: controller.show_frame("Frame17"))
        self.Backup_img = PhotoImage(file=r"images\Buttons\BackupOPEN.png")
        self.Backup_button = self.canvas.create_image(100, 270, image=self.Backup_img)


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

        self.MainScreen_img = PhotoImage(file=r"images\Buttons\MainScreen.png")
        self.MainScreen_button = self.canvas.create_image(100, 30, image=self.MainScreen_img)
        self.canvas.tag_bind(self.MainScreen_button, "<Button-1>", lambda event: controller.show_frame("Frame1_1"))

        self.SetpointPlanner_img = PhotoImage(file=r"images\Buttons\SetpointPlanner.png")
        self.SetpointPlanner_button = self.canvas.create_image(100, 90, image=self.SetpointPlanner_img)
        self.canvas.tag_bind(self.SetpointPlanner_button, "<Button-1>", lambda event: controller.show_frame("Frame2"))

        self.Monitoring_img = PhotoImage(file=r"images\Buttons\Monitoring.png")
        self.Monitoring_button = self.canvas.create_image(100, 150, image=self.Monitoring_img)
        self.canvas.tag_bind(self.Monitoring_button, "<Button-1>", lambda event: controller.show_frame("Frame3"))

        self.Journal_img = PhotoImage(file=r"images\Buttons\Journal.png")
        self.Journal_button = self.canvas.create_image(100, 210, image=self.Journal_img)
        self.canvas.tag_bind(self.Journal_button, "<Button-1>", lambda event: controller.show_frame("Frame6"))

        self.StationSettings_img = PhotoImage(file=r"images\Buttons\StationSettings.png")
        self.StationSettings_button = self.canvas.create_image(100, 270, image=self.StationSettings_img)
        self.canvas.tag_bind(self.StationSettings_button, "<Button-1>", lambda event: controller.show_frame("Frame9"))

        self.EngineeringMenu_img = PhotoImage(file=r"images\Buttons\EngineeringMenu.png")
        self.EngineeringMenu_button = self.canvas.create_image(100, 330, image=self.EngineeringMenu_img)
        self.canvas.tag_bind(self.EngineeringMenu_button, "<Button-1>", lambda event: controller.show_frame("Frame16"))

        self.PanelSettings_img = PhotoImage(file=r"images\Buttons\PanelSettingsOpen.png")
        self.PanelSettings_button = self.canvas.create_image(100, 390, image=self.PanelSettings_img)

        self.Contacts_img = PhotoImage(file=r"images\Buttons\Contacts.png")
        self.Contacts_button = self.canvas.create_image(100, 450, image=self.Contacts_img)
        self.canvas.tag_bind(self.Contacts_button, "<Button-1>", lambda event: controller.show_frame("Frame20"))

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
                if address.family == 2:  # IPv4
                    if address.address == self.ip_:
                        self.result_netmask = address.netmask

        self.result_netmask_split = self.result_netmask.split(".")

        if (len(self.result_netmask_split[0])== 1):
            self.netmask_1 = tk.Label(self.canvas, text=f"{self.result_netmask_split[0]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.netmask_1.place(x=418, y=335)
        elif (len(self.result_netmask_split[0])== 2):
            self.netmask_1 = tk.Label(self.canvas, text=f"{self.result_netmask_split[0]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.netmask_1.place(x=414, y=335)
        elif (len(self.result_netmask_split[0])== 3):
            self.netmask_1 = tk.Label(self.canvas, text=f"{self.result_netmask_split[0]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.netmask_1.place(x=410, y=335)
        if (len(self.result_netmask_split[1])== 1):
            self.netmask_1 = tk.Label(self.canvas, text=f"{self.result_netmask_split[1]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.netmask_1.place(x=520, y=335)
        elif (len(self.result_netmask_split[1])== 2):
            self.netmask_1 = tk.Label(self.canvas, text=f"{self.result_netmask_split[1]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.netmask_1.place(x=516, y=335)
        elif (len(self.result_netmask_split[1])== 3):
            self.netmask_1 = tk.Label(self.canvas, text=f"{self.result_netmask_split[1]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.netmask_1.place(x=512, y=335)
        if (len(self.result_netmask_split[2])== 1):
            self.netmask_1 = tk.Label(self.canvas, text=f"{self.result_netmask_split[2]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.netmask_1.place(x=622, y=335)
        elif (len(self.result_netmask_split[2])== 2):
            self.netmask_1 = tk.Label(self.canvas, text=f"{self.result_netmask_split[2]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.netmask_1.place(x=617, y=335)
        elif (len(self.result_netmask_split[2])== 3):
            self.netmask_1 = tk.Label(self.canvas, text=f"{self.result_netmask_split[2]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.netmask_1.place(x=614, y=335)
        if (len(self.result_netmask_split[3])== 1):
            self.netmask_1 = tk.Label(self.canvas, text=f"{self.result_netmask_split[3]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.netmask_1.place(x=724, y=335)
        elif (len(self.result_netmask_split[3])== 2):
            self.netmask_1 = tk.Label(self.canvas, text=f"{self.result_netmask_split[3]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.netmask_1.place(x=720, y=335)
        elif (len(self.result_netmask_split[3])== 3):
            self.netmask_1 = tk.Label(self.canvas, text=f"{self.result_netmask_split[3]}", fg='white', bg='black', font=('Roboto Bold', 12))
            self.netmask_1.place(x=717, y=335)

        self.time_display_1 = tk.Label(self.canvas, text="**", fg='white', bg='black', font=('Roboto Bold', 12))
        self.time_display_1.place(x=645, y=63)
        self.time_display_2 = tk.Label(self.canvas, text="**", fg='white', bg='black', font=('Roboto Bold', 12))
        self.time_display_2.place(x=645, y=103)
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
        self.show_second.place(x=684, y=234)
        self.show_day = tk.Label(self.canvas, text="", fg='white', bg='black', font=('Roboto Bold', 12))
        self.show_day.place(x=480, y=195)
        self.show_month = tk.Label(self.canvas, text="", fg='white', bg='black', font=('Roboto Bold', 12))
        self.show_month.place(x=584, y=195)
        self.show_year = tk.Label(self.canvas, text="", fg='white', bg='black', font=('Roboto Bold', 12))
        self.show_year.place(x=684, y=195)

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

        self.MainScreen_img = PhotoImage(file=r"images\Buttons\MainScreen.png")
        self.MainScreen_button = self.canvas.create_image(100, 30, image=self.MainScreen_img)
        self.canvas.tag_bind(self.MainScreen_button, "<Button-1>", lambda event: controller.show_frame("Frame1_1"))
        self.SetpointPlanner_img = PhotoImage(file=r"images\Buttons\SetpointPlanner.png")
        self.SetpointPlanner_button = self.canvas.create_image(100, 90, image=self.SetpointPlanner_img)
        self.canvas.tag_bind(self.SetpointPlanner_button, "<Button-1>", lambda event: controller.show_frame("Frame2"))
        self.Monitoring_img = PhotoImage(file=r"images\Buttons\Monitoring.png")
        self.Monitoring_button = self.canvas.create_image(100, 150, image=self.Monitoring_img)
        self.canvas.tag_bind(self.Monitoring_button, "<Button-1>", lambda event: controller.show_frame("Frame3"))
        self.Journal_img = PhotoImage(file=r"images\Buttons\Journal.png")
        self.Journal_button = self.canvas.create_image(100, 210, image=self.Journal_img)
        self.canvas.tag_bind(self.Journal_button, "<Button-1>", lambda event: controller.show_frame("Frame6"))
        self.StationSettings_img = PhotoImage(file=r"images\Buttons\StationSettings.png")
        self.StationSettings_button = self.canvas.create_image(100, 270, image=self.StationSettings_img)
        self.canvas.tag_bind(self.StationSettings_button, "<Button-1>", lambda event: controller.show_frame("Frame9"))
        self.EngineeringMenu_img = PhotoImage(file=r"images\Buttons\EngineeringMenu.png")
        self.EngineeringMenu_button = self.canvas.create_image(100, 330, image=self.EngineeringMenu_img)
        self.canvas.tag_bind(self.EngineeringMenu_button, "<Button-1>", lambda event: controller.show_frame("Frame16"))
        self.PanelSettings_img = PhotoImage(file=r"images\Buttons\PanelSettings.png")
        self.PanelSettings_button = self.canvas.create_image(100, 390, image=self.PanelSettings_img)
        self.canvas.tag_bind(self.PanelSettings_button, "<Button-1>", lambda event: controller.show_frame("Frame19"))
        self.Contacts_img = PhotoImage(file=r"images\Buttons\ContactsOpen.png")
        self.Contacts_button = self.canvas.create_image(100, 450, image=self.Contacts_img)

        self.InterfaceScreen_img = PhotoImage(file=r"images\Contacts\Contacts.png")
        self.InterfaceScreen = self.canvas.create_image(500, 202, image=self.InterfaceScreen_img)

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
