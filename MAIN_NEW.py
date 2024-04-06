import tkinter as tk
from tkinter import PhotoImage, Canvas
from datetime import datetime
from PIL import Image, ImageTk
from platform import system
from re import sub
from subprocess import check_output
from socket import socket, AF_INET, SOCK_DGRAM

'''
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

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        '''
        При добавлении фрейма, обновить кортеж снизу!!!
        Так же не забыть создать класс для нового фрейма, по аналогии!!!
        '''
        for F in (Frame1_1, Frame1_2, Frame1_3, Frame1_4, Menu, Frame2, Frame3, Frame4, Frame5, Frame6, Frame7, Frame8, Frame9, Frame10, Frame11, Frame12, Frame13, Frame14, Frame15, Frame16, Frame17, Frame18, Frame19, Frame20):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
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

        button = tk.Button(self, text="Главный экран", fg='white', bg='black', font=('Roboto Bold', 12),
                           relief="groove", command=lambda: controller.show_frame("Frame1_1"), width=18, height=3)
        button.place(x=0, y=0)
        button2 = tk.Button(self, text="Назад", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Menu"), width=18, height=3)
        button2.place(x=0, y=60)
        button3 = tk.Button(self, text="Тренды онлайн", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Frame3"), width=18, height=3)
        button3.place(x=0, y=120)
        button4 = tk.Button(self, text="Тренды истории", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Frame4"), width=18, height=3)
        button4.place(x=0, y=180)
        button5 = tk.Button(self, text="Наработка насосов", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Frame5"), width=18, height=3)
        button5.place(x=0, y=240)

    def update_clock(self, current_time):
        self.clock_label.config(text=current_time)


class Frame4(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='black')
        self.clock_label = tk.Label(self, text="", fg='white', bg='black', font=('Roboto Bold', 12))
        self.clock_label.place(x=680, y=5)

        button = tk.Button(self, text="Главный экран", fg='white', bg='black', font=('Roboto Bold', 12),
                           relief="groove", command=lambda: controller.show_frame("Frame1_1"), width=18, height=3)
        button.place(x=0, y=0)
        button2 = tk.Button(self, text="Назад", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Menu"), width=18, height=3)
        button2.place(x=0, y=60)
        button3 = tk.Button(self, text="Тренды онлайн", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Frame3"), width=18, height=3)
        button3.place(x=0, y=120)
        button4 = tk.Button(self, text="Тренды истории", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Frame4"), width=18, height=3)
        button4.place(x=0, y=180)
        button5 = tk.Button(self, text="Наработка насосов", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Frame5"), width=18, height=3)
        button5.place(x=0, y=240)

    def update_clock(self, current_time):
        self.clock_label.config(text=current_time)


class Frame5(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='black')
        self.clock_label = tk.Label(self, text="", fg='white', bg='black', font=('Roboto Bold', 12))
        self.clock_label.place(x=680, y=5)

        button = tk.Button(self, text="Главный экран", fg='white', bg='black', font=('Roboto Bold', 12),
                           relief="groove", command=lambda: controller.show_frame("Frame1_1"), width=18, height=3)
        button.place(x=0, y=0)
        button2 = tk.Button(self, text="Назад", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Menu"), width=18, height=3)
        button2.place(x=0, y=60)
        button3 = tk.Button(self, text="Тренды онлайн", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Frame3"), width=18, height=3)
        button3.place(x=0, y=120)
        button4 = tk.Button(self, text="Тренды истории", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Frame4"), width=18, height=3)
        button4.place(x=0, y=180)
        button5 = tk.Button(self, text="Наработка насосов", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Frame5"), width=18, height=3)
        button5.place(x=0, y=240)

    def update_clock(self, current_time):
        self.clock_label.config(text=current_time)

class Frame6(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='black')
        self.clock_label = tk.Label(self, text="", fg='white', bg='black', font=('Roboto Bold', 12))
        self.clock_label.place(x=680, y=5)

        button = tk.Button(self, text="Главный экран", fg='white', bg='black', font=('Roboto Bold', 12),
                           relief="groove", command=lambda: controller.show_frame("Frame1_1"), width=18, height=3)
        button.place(x=0, y=0)
        button2 = tk.Button(self, text="Назад", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Menu"), width=18, height=3)
        button2.place(x=0, y=60)
        button3 = tk.Button(self, text="Текущие события", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Frame6"), width=18, height=3)
        button3.place(x=0, y=120)
        button4 = tk.Button(self, text="Журнал история", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Frame7"), width=18, height=3)
        button4.place(x=0, y=180)
        button5 = tk.Button(self, text="Журнал изменений", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Frame8"), width=18, height=3)
        button5.place(x=0, y=240)

    def update_clock(self, current_time):
        self.clock_label.config(text=current_time)

class Frame7(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='black')
        self.clock_label = tk.Label(self, text="", fg='white', bg='black', font=('Roboto Bold', 12))
        self.clock_label.place(x=680, y=5)

        button = tk.Button(self, text="Главный экран", fg='white', bg='black', font=('Roboto Bold', 12),
                           relief="groove", command=lambda: controller.show_frame("Frame1_1"), width=18, height=3)
        button.place(x=0, y=0)
        button2 = tk.Button(self, text="Назад", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Menu"), width=18, height=3)
        button2.place(x=0, y=60)
        button3 = tk.Button(self, text="Текущие события", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Frame6"), width=18, height=3)
        button3.place(x=0, y=120)
        button4 = tk.Button(self, text="Журнал история", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Frame7"), width=18, height=3)
        button4.place(x=0, y=180)
        button5 = tk.Button(self, text="Журнал изменений", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Frame8"), width=18, height=3)
        button5.place(x=0, y=240)

    def update_clock(self, current_time):
        self.clock_label.config(text=current_time)

class Frame8(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='black')
        self.clock_label = tk.Label(self, text="", fg='white', bg='black', font=('Roboto Bold', 12))
        self.clock_label.place(x=680, y=5)

        button = tk.Button(self, text="Главный экран", fg='white', bg='black', font=('Roboto Bold', 12),
                           relief="groove", command=lambda: controller.show_frame("Frame1_1"), width=18, height=3)
        button.place(x=0, y=0)
        button2 = tk.Button(self, text="Назад", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Menu"), width=18, height=3)
        button2.place(x=0, y=60)
        button3 = tk.Button(self, text="Текущие события", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Frame6"), width=18, height=3)
        button3.place(x=0, y=120)
        button4 = tk.Button(self, text="Журнал история", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Frame7"), width=18, height=3)
        button4.place(x=0, y=180)
        button5 = tk.Button(self, text="Журнал изменений", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Frame8"), width=18, height=3)
        button5.place(x=0, y=240)

    def update_clock(self, current_time):
        self.clock_label.config(text=current_time)

class Frame9(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='black')
        self.clock_label = tk.Label(self, text="", fg='white', bg='black', font=('Roboto Bold', 12))
        self.clock_label.place(x=680, y=5)

        button = tk.Button(self, text="Главный экран", fg='white', bg='black', font=('Roboto Bold', 12),
                           relief="groove", command=lambda: controller.show_frame("Frame1_1"), width=18, height=3)
        button.place(x=0, y=0)
        button2 = tk.Button(self, text="Назад", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Menu"), width=18, height=3)
        button2.place(x=0, y=50)
        button3 = tk.Button(self, text="Параметры двигателей", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Frame9"), width=18, height=3)
        button3.place(x=0, y=100)
        button4 = tk.Button(self, text="Настройки датчиков", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Frame10"), width=18, height=3)
        button4.place(x=0, y=150)
        button5 = tk.Button(self, text="Параметры насосов общ.", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Frame11"), width=18, height=3)
        button5.place(x=0, y=200)
        button6 = tk.Button(self, text="Вкл. доп. насосов", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Frame12"), width=18, height=3)
        button6.place(x=0, y=250)
        button7 = tk.Button(self, text="Откл. доп. насосов", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Frame13"), width=18, height=3)
        button7.place(x=0, y=300)
        button8 = tk.Button(self, text="Опции", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Frame14"), width=18, height=3)
        button8.place(x=0, y=350)
        button9 = tk.Button(self, text="Аварийные режимы", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Frame15"), width=18, height=3)
        button9.place(x=0, y=400)

    def update_clock(self, current_time):
        self.clock_label.config(text=current_time)

class Frame10(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='black')
        self.clock_label = tk.Label(self, text="", fg='white', bg='black', font=('Roboto Bold', 12))
        self.clock_label.place(x=680, y=5)

        button = tk.Button(self, text="Главный экран", fg='white', bg='black', font=('Roboto Bold', 12),
                           relief="groove", command=lambda: controller.show_frame("Frame1_1"), width=18, height=3)
        button.place(x=0, y=0)
        button2 = tk.Button(self, text="Назад", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Menu"), width=18, height=3)
        button2.place(x=0, y=50)
        '''
        ВСТАВИТЬ ИСПРАВЛЕННЫЕ КНОПКИ
        '''

    def update_clock(self, current_time):
        self.clock_label.config(text=current_time)
class Frame11(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='black')
        self.clock_label = tk.Label(self, text="", fg='white', bg='black', font=('Roboto Bold', 12))
        self.clock_label.place(x=680, y=5)

        button = tk.Button(self, text="Главный экран", fg='white', bg='black', font=('Roboto Bold', 12),
                           relief="groove", command=lambda: controller.show_frame("Frame1_1"), width=18, height=3)
        button.place(x=0, y=0)
        button2 = tk.Button(self, text="Назад", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Menu"), width=18, height=3)
        button2.place(x=0, y=50)
        '''
        ВСТАВИТЬ ИСПРАВЛЕННЫЕ КНОПКИ
        '''

    def update_clock(self, current_time):
        self.clock_label.config(text=current_time)

class Frame12(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='black')
        self.clock_label = tk.Label(self, text="", fg='white', bg='black', font=('Roboto Bold', 12))
        self.clock_label.place(x=680, y=5)

        button = tk.Button(self, text="Главный экран", fg='white', bg='black', font=('Roboto Bold', 12),
                           relief="groove", command=lambda: controller.show_frame("Frame1_1"), width=18, height=3)
        button.place(x=0, y=0)
        button2 = tk.Button(self, text="Назад", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Menu"), width=18, height=3)
        button2.place(x=0, y=50)
        '''
        ВСТАВИТЬ ИСПРАВЛЕННЫЕ КНОПКИ
        '''
    def update_clock(self, current_time):
        self.clock_label.config(text=current_time)

class Frame13(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='black')
        self.clock_label = tk.Label(self, text="", fg='white', bg='black', font=('Roboto Bold', 12))
        self.clock_label.place(x=680, y=5)

        button = tk.Button(self, text="Главный экран", fg='white', bg='black', font=('Roboto Bold', 12),
                           relief="groove", command=lambda: controller.show_frame("Frame1_1"), width=18, height=3)
        button.place(x=0, y=0)
        button2 = tk.Button(self, text="Назад", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Menu"), width=18, height=3)
        button2.place(x=0, y=50)
        '''
        ВСТАВИТЬ ИСПРАВЛЕННЫЕ КНОПКИ
        '''

    def update_clock(self, current_time):
        self.clock_label.config(text=current_time)
class Frame14(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='black')
        self.clock_label = tk.Label(self, text="", fg='white', bg='black', font=('Roboto Bold', 12))
        self.clock_label.place(x=680, y=5)

        button = tk.Button(self, text="Главный экран", fg='white', bg='black', font=('Roboto Bold', 12),
                           relief="groove", command=lambda: controller.show_frame("Frame1"), width=18, height=3)
        button.place(x=0, y=0)
        button2 = tk.Button(self, text="Назад", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Menu"), width=18, height=3)
        button2.place(x=0, y=50)
        '''
        ВСТАВИТЬ ИСПРАВЛЕННЫЕ КНОПКИ
        '''

    def update_clock(self, current_time):
        self.clock_label.config(text=current_time)

class Frame15(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='black')
        self.clock_label = tk.Label(self, text="", fg='white', bg='black', font=('Roboto Bold', 12))
        self.clock_label.place(x=680, y=5)

        button = tk.Button(self, text="Главный экран", fg='white', bg='black', font=('Roboto Bold', 12),
                           relief="groove", command=lambda: controller.show_frame("Frame1"), width=18, height=3)
        button.place(x=0, y=0)
        button2 = tk.Button(self, text="Назад", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Menu"), width=18, height=3)
        button2.place(x=0, y=50)
        '''
        ВСТАВИТЬ ИСПРАВЛЕННЫЕ КНОПКИ
        '''

    def update_clock(self, current_time):
        self.clock_label.config(text=current_time)

class Frame16(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='black')
        self.clock_label = tk.Label(self, text="", fg='white', bg='black', font=('Roboto Bold', 12))
        self.clock_label.place(x=680, y=5)

        button = tk.Button(self, text="Главный экран", fg='white', bg='black', font=('Roboto Bold', 12),
                           relief="groove", command=lambda: controller.show_frame("Frame1_1"), width=18, height=3)
        button.place(x=0, y=0)
        button2 = tk.Button(self, text="Назад", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Menu"), width=18, height=3)
        button2.place(x=0, y=60)
        button3 = tk.Button(self, text="Настройки ПИД-рег.", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Frame16"), width=18, height=3)
        button3.place(x=0, y=120)
        button4 = tk.Button(self, text="PLC", fg='white', bg='black', font=('Roboto', 12),
                            relief="groove", command=lambda: controller.show_frame("Frame17"), width=18, height=3)
        button4.place(x=0, y=180)
        button5 = tk.Button(self, text="Бэкап", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Frame18"), width=18, height=3)
        button5.place(x=0, y=240)


    def update_clock(self, current_time):
        self.clock_label.config(text=current_time)

class Frame17(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='black')
        self.clock_label = tk.Label(self, text="", fg='white', bg='black', font=('Roboto Bold', 12))
        self.clock_label.place(x=680, y=5)

        button = tk.Button(self, text="Главный экран", fg='white', bg='black', font=('Roboto Bold', 12),
                           relief="groove", command=lambda: controller.show_frame("Frame1_1"), width=18, height=3)
        button.place(x=0, y=0)
        button2 = tk.Button(self, text="Назад", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Menu"), width=18, height=3)
        button2.place(x=0, y=60)
        button3 = tk.Button(self, text="Настройки ПИД-рег.", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Frame16"), width=18, height=3)
        button3.place(x=0, y=120)
        button4 = tk.Button(self, text="PLC", fg='white', bg='black', font=('Roboto', 12),
                            relief="groove", command=lambda: controller.show_frame("Frame17"), width=18, height=3)
        button4.place(x=0, y=180)
        button5 = tk.Button(self, text="Бэкап", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Frame18"), width=18, height=3)
        button5.place(x=0, y=240)


    def update_clock(self, current_time):
        self.clock_label.config(text=current_time)

class Frame18(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='black')
        self.clock_label = tk.Label(self, text="", fg='white', bg='black', font=('Roboto Bold', 12))
        self.clock_label.place(x=680, y=5)

        button = tk.Button(self, text="Главный экран", fg='white', bg='black', font=('Roboto Bold', 12),
                           relief="groove", command=lambda: controller.show_frame("Frame1_1"), width=18, height=3)
        button.place(x=0, y=0)
        button2 = tk.Button(self, text="Назад", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Menu"), width=18, height=3)
        button2.place(x=0, y=60)
        button3 = tk.Button(self, text="Настройки ПИД-рег.", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Frame16"), width=18, height=3)
        button3.place(x=0, y=120)
        button4 = tk.Button(self, text="PLC", fg='white', bg='black', font=('Roboto', 12),
                            relief="groove", command=lambda: controller.show_frame("Frame17"), width=18, height=3)
        button4.place(x=0, y=180)
        button5 = tk.Button(self, text="Бэкап", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Frame18"), width=18, height=3)
        button5.place(x=0, y=240)


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

        self.InterfaceScreen_img = PhotoImage(file=r"images\PanelSettings\Settings.png")
        self.InterfaceScreen = self.canvas.create_image(500, 230, image=self.InterfaceScreen_img)
        self.Switch_Flat_img = PhotoImage(file=r"images\PanelSettings\Switch-0.png")
        self.Switch_Flat_button = self.canvas.create_image(670, 152, image=self.Switch_Flat_img)
        self.canvas.tag_bind(self.Switch_Flat_button, "<Button-1>", self.update_switch)

        self.ip_ = NetInfo().ipv4
        self.result = self.ip_.split(".")

        self.IP_1 = tk.Label(self.canvas, text=f"{self.result[0]}", fg='white', bg='black', font=('Roboto Bold', 12))
        self.IP_1.place(x=404, y=294)
        self.IP_2 = tk.Label(self.canvas, text=f"{self.result[1]}", fg='white', bg='black', font=('Roboto Bold', 12))
        self.IP_2.place(x=509, y=294)
        self.IP_3 = tk.Label(self.canvas, text=f"{self.result[2]}", fg='white', bg='black', font=('Roboto Bold', 12))
        self.IP_3.place(x=612, y=294)
        self.IP_4 = tk.Label(self.canvas, text=f"{self.result[3]}", fg='white', bg='black', font=('Roboto Bold', 12))
        self.IP_4.place(x=715, y=294)

    def update_switch(self, event):
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

