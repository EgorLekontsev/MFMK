import tkinter as tk
from datetime import datetime

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
        for F in (Frame1, Menu, Frame2):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Frame1")

        self.update_clock()

    def show_frame(self, page_name): # Смена фреймов
        frame = self.frames[page_name]
        frame.tkraise()

        if page_name == "Frame1": # Смена названия окна
            self.title("Главный экран")
        elif page_name == "Menu":
            self.title("Меню")

    def update_clock(self): # Часики
        current_time = datetime.now().strftime('%d/%m/%y %H:%M')
        for frame_name in self.frames:
            self.frames[frame_name].update_clock(current_time)
        self.after(1000, self.update_clock) # Тик-так


class Frame1(tk.Frame): #Экран №1
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='black')
        self.clock_label = tk.Label(self, text="", fg='white', bg='black', font=('Roboto Bold', 9))
        self.clock_label.pack(anchor='ne', padx=10, pady=10)

        button = tk.Button(self, text="Меню", fg='white', bg='black', font=('Roboto Bold', 12),
                           relief="groove", command=lambda: controller.show_frame("Menu"))
        button.place(x=0, y=0)
    def update_clock(self, current_time):
        self.clock_label.config(text=current_time)


class Menu(tk.Frame): #Меню
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='black')
        self.clock_label = tk.Label(self, text="", fg='white', bg='black', font=('Roboto Bold', 9))
        self.clock_label.pack(anchor='ne', padx=10, pady=10)
        button = tk.Button(self, text="Главный экран", fg='white', bg='black', font=('Roboto Bold', 12),
                           relief="groove", command=lambda: controller.show_frame("Frame1"))
        button.place(x=0, y=0)
        button2 = tk.Button(self, text="Уставки", fg='white', bg='black', font=('Roboto Bold', 12),
                           relief="groove", command=lambda: controller.show_frame("Frame2"))
        button2.place(x=0, y=35)
        button3 = tk.Button(self, text="Мониторинг", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Frame2"))
        button3.place(x=0, y=70)
        button4 = tk.Button(self, text="Журнал", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Frame2"))
        button4.place(x=0, y=105)
        button5 = tk.Button(self, text="Настройки станции", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Frame2"))
        button5.place(x=0, y=140)
        button6 = tk.Button(self, text="Инженерное меню", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Frame2"))
        button6.place(x=0, y=175)
        button7 = tk.Button(self, text="Настройки панели", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Frame2"))
        button7.place(x=0, y=210)
        button8 = tk.Button(self, text="Контакты", fg='white', bg='black', font=('Roboto Bold', 12),
                            relief="groove", command=lambda: controller.show_frame("Frame2"))
        button8.place(x=0, y=245)

    def update_clock(self, current_time):
        self.clock_label.config(text=current_time)

class Frame2(tk.Frame): #Экран №2
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='black')
        self.clock_label = tk.Label(self, text="", fg='white', bg='black', font=('Roboto Bold', 9))
        self.clock_label.pack(anchor='ne', padx=10, pady=10)

        button = tk.Button(self, text="Назад", fg='white', bg='black', font=('Roboto Bold', 12),
                           relief="groove", command=lambda: controller.show_frame("Menu"))
        button.place(x=0, y=0)
    def update_clock(self, current_time):
        self.clock_label.config(text=current_time)


app = App()
app.mainloop()
