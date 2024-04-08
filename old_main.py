import tkinter as tk
from tkinter import PhotoImage, Canvas
from datetime import datetime
from PIL import Image, ImageTk

'''
Frame1 - Главный экран 
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
        for F in (Frame1, Menu, Frame2, Frame3, Frame4, Frame5, Frame6, Frame7, Frame8, Frame9, Frame10, Frame11, Frame12, Frame13, Frame14, Frame15, Frame16, Frame17, Frame18, Frame19, Frame20):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Frame1")
        self.update_clock()

    def show_frame(self, page_name): # Смена фреймов
        frame = self.frames[page_name]
        frame.tkraise()

        match page_name: # Смена названий окна
            case "Frame1":
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


class Frame1(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='black')

        self.clock_label = tk.Label(self, text="", fg='white', bg='black', font=('Roboto Bold', 12))
        self.clock_label.place(x=680, y=5)

        button = tk.Button(self, text="Меню", fg='white', bg='black', font=('Roboto Bold', 12),
                           relief="groove", command=lambda: controller.show_frame("Menu"))
        button.place(x=0, y=0)
    def update_clock(self, current_time):
        self.clock_label.config(text=current_time)


class Menu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='black')
        self.clock_label = tk.Label(self, text="", fg='white', bg='black', font=('Roboto Bold', 12))
        self.clock_label.place(x=680, y=5)
        button = tk.Button(self, text="Главный экран", fg='white', bg='black', font=('Roboto Bold', 12),
                           relief="groove", command=lambda: controller.show_frame("Frame1"), width=18, height=3)
        button.place(x=0, y=0)
        button2 = tk.Button(self, text="Планировщик уставок", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Frame2"), width=18, height=3)
        button2.place(x=0, y=60)
        button3 = tk.Button(self, text="Мониторинг", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Frame3"), width=18, height=3)
        button3.place(x=0, y=120)
        button4 = tk.Button(self, text="Журнал", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Frame6"), width=18, height=3)
        button4.place(x=0, y=180)
        button5 = tk.Button(self, text="Настройки станции", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Frame9"), width=18, height=3)
        button5.place(x=0, y=240)
        button6 = tk.Button(self, text="Инженерное меню", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Frame16"), width=18, height=3)
        button6.place(x=0, y=300)
        button7 = tk.Button(self, text="Настройки панели", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Frame19"), width=18, height=3)
        button7.place(x=0, y=360)
        button8 = tk.Button(self, text="Контакты", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Frame20"), width=18, height=3)
        button8.place(x=0, y=420)

    def update_clock(self, current_time):
        self.clock_label.config(text=current_time)

class Frame2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='black')
        self.clock_label = tk.Label(self, text="", fg='white', bg='black', font=('Roboto Bold', 12))
        self.clock_label.place(x=680, y=5)

        button = tk.Button(self, text="Главный экран", fg='white', bg='black', font=('Roboto Bold', 12),
                           relief="groove", command=lambda: controller.show_frame("Frame1"), width=18, height=3)
        button.place(x=0, y=0)
        button2 = tk.Button(self, text="Планировщик уставок", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Frame2"), width=18, height=3)
        button2.place(x=0, y=60)
        button3 = tk.Button(self, text="Мониторинг", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Frame3"), width=18, height=3)
        button3.place(x=0, y=120)
        button4 = tk.Button(self, text="Журнал", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Frame6"), width=18, height=3)
        button4.place(x=0, y=180)
        button5 = tk.Button(self, text="Настройки станции", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Frame9"), width=18, height=3)
        button5.place(x=0, y=240)
        button6 = tk.Button(self, text="Инженерное меню", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Frame16"), width=18, height=3)
        button6.place(x=0, y=300)
        button7 = tk.Button(self, text="Настройки панели", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Frame19"), width=18, height=3)
        button7.place(x=0, y=360)
        button8 = tk.Button(self, text="Контакты", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Frame20"), width=18, height=3)
        button8.place(x=0, y=420)
    def update_clock(self, current_time):
        self.clock_label.config(text=current_time)

class Frame3(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='black')
        self.clock_label = tk.Label(self, text="", fg='white', bg='black', font=('Roboto Bold', 12))
        self.clock_label.place(x=680, y=5)

        button = tk.Button(self, text="Главный экран", fg='white', bg='black', font=('Roboto Bold', 12),
                           relief="groove", command=lambda: controller.show_frame("Frame1"), width=18, height=3)
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
                           relief="groove", command=lambda: controller.show_frame("Frame1"), width=18, height=3)
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
                           relief="groove", command=lambda: controller.show_frame("Frame1"), width=18, height=3)
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
                           relief="groove", command=lambda: controller.show_frame("Frame1"), width=18, height=3)
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
                           relief="groove", command=lambda: controller.show_frame("Frame1"), width=18, height=3)
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
                           relief="groove", command=lambda: controller.show_frame("Frame1"), width=18, height=3)
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
                           relief="groove", command=lambda: controller.show_frame("Frame1"), width=18, height=3)
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
class Frame11(tk.Frame):
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

class Frame12(tk.Frame):
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

class Frame13(tk.Frame):
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
                           relief="groove", command=lambda: controller.show_frame("Frame1"), width=18, height=3)
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
                           relief="groove", command=lambda: controller.show_frame("Frame1"), width=18, height=3)
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
                           relief="groove", command=lambda: controller.show_frame("Frame1"), width=18, height=3)
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

class Frame19(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='black')
        self.clock_label = tk.Label(self, text="", fg='white', bg='black', font=('Roboto Bold', 12))
        self.clock_label.place(x=680, y=5)

        button = tk.Button(self, text="Главный экран", fg='white', bg='black', font=('Roboto Bold', 12),
                           relief="groove", command=lambda: controller.show_frame("Frame1"), width=18, height=3)
        button.place(x=0, y=0)
        button2 = tk.Button(self, text="Планировщик уставок", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Frame2"), width=18, height=3)
        button2.place(x=0, y=60)
        button3 = tk.Button(self, text="Мониторинг", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Frame3"), width=18, height=3)
        button3.place(x=0, y=120)
        button4 = tk.Button(self, text="Журнал", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Frame6"), width=18, height=3)
        button4.place(x=0, y=180)
        button5 = tk.Button(self, text="Настройки станции", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Frame9"), width=18, height=3)
        button5.place(x=0, y=240)
        button6 = tk.Button(self, text="Инженерное меню", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Frame16"), width=18, height=3)
        button6.place(x=0, y=300)
        button7 = tk.Button(self, text="Настройки панели", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Frame19"), width=18, height=3)
        button7.place(x=0, y=360)
        button8 = tk.Button(self, text="Контакты", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Frame20"), width=18, height=3)
        button8.place(x=0, y=420)
    def update_clock(self, current_time):
        self.clock_label.config(text=current_time)

class Frame20(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='black')
        self.clock_label = tk.Label(self, text="", fg='white', bg='black', font=('Roboto Bold', 12))
        self.clock_label.place(x=680, y=5)

        button = tk.Button(self, text="Главный экран", fg='white', bg='black', font=('Roboto Bold', 12),
                           relief="groove", command=lambda: controller.show_frame("Frame1"), width=18, height=3)
        button.place(x=0, y=0)
        button2 = tk.Button(self, text="Планировщик уставок", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Frame2"), width=18, height=3)
        button2.place(x=0, y=60)
        button3 = tk.Button(self, text="Мониторинг", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Frame3"), width=18, height=3)
        button3.place(x=0, y=120)
        button4 = tk.Button(self, text="Журнал", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Frame6"), width=18, height=3)
        button4.place(x=0, y=180)
        button5 = tk.Button(self, text="Настройки станции", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Frame9"), width=18, height=3)
        button5.place(x=0, y=240)
        button6 = tk.Button(self, text="Инженерное меню", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Frame16"), width=18, height=3)
        button6.place(x=0, y=300)
        button7 = tk.Button(self, text="Настройки панели", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Frame19"), width=18, height=3)
        button7.place(x=0, y=360)
        button8 = tk.Button(self, text="Контакты", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Frame20"), width=18, height=3)
        button8.place(x=0, y=420)
    def update_clock(self, current_time):
        self.clock_label.config(text=current_time)


app = App()
app.mainloop()