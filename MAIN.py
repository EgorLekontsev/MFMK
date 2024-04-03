import tkinter as tk
from datetime import datetime

'''
Frame1 - Экран №1 - Главный экран 
Menu - Меню - Настройки
Frame2 - Экран №2 - Планировщик установок 
Frame3 - Экран №3 - Журнал
Frame4 - Экран №4 - Мониторинг(Журнал)
Frame5 - Экран №5 - Мониторинг(История)
Frame6 - Экран №6 - Мониторинг(Тренды)
Frame7 - Экран №7 - Счетчик эл.(Настройки)
Frame8 - Экран №8 - Счетчик эл.(Тарифы)
Frame9 - Экран №9 - Счетчик эл.(История электроэнергии)
Frame10 - Экран №10 - Счетчик эл.(Тренды электроэнергии)
Frame11 - Экран №11 - ПЧ(ABX)
Frame12 - Экран №12 - ПЧ(ВВ ПЧ 1-3)
Frame13 - Экран №13 - ПЧ(ВВ ПЧ 4-6)
Frame14 - Экран №14 - ПЧ(Настройки ПЧ)
Frame15 - Экран №15 - Насосы(Настройки)
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
            self.title("Настройки")

    def update_clock(self): # Часики
        current_time = datetime.now().strftime('%d/%m/%y %H:%M')
        for frame_name in self.frames:
            self.frames[frame_name].update_clock(current_time)
        self.after(1000, self.update_clock) # Тик-так


class Frame1(tk.Frame): #Экран №1
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='black')
        self.clock_label = tk.Label(self, text="", fg='white', bg='black', font=('Roboto Bold', 12))
        self.clock_label.pack(anchor='ne', padx=10, pady=10)

        button = tk.Button(self, text="Настройки", fg='white', bg='black', font=('Roboto Bold', 12),
                           relief="groove", command=lambda: controller.show_frame("Menu"))
        button.place(x=0, y=0)
    def update_clock(self, current_time):
        self.clock_label.config(text=current_time)


class Menu(tk.Frame): #Меню
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='black')
        self.clock_label = tk.Label(self, text="", fg='white', bg='black', font=('Roboto Bold', 12))
        self.clock_label.pack(anchor='ne', padx=10, pady=10)

        button = tk.Button(self, text="Главный экран", fg='white', bg='black', font=('Roboto Bold', 12),
                           relief="groove", command=lambda: controller.show_frame("Frame1"))
        button.place(x=0, y=0)
        button2 = tk.Button(self, text="Главный экран", fg='white', bg='black', font=('Roboto Bold', 12),
                           relief="groove", command=lambda: controller.show_frame("Frame1"))
        button2.place(x=0, y=0)

    def update_clock(self, current_time):
        self.clock_label.config(text=current_time)

class Frame2(tk.Frame): #Экран №2
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='black')
        self.clock_label = tk.Label(self, text="", fg='white', bg='black', font=('Roboto Bold', 12))
        self.clock_label.pack(anchor='ne', padx=10, pady=10)

        button = tk.Button(self, text="Настройки", fg='white', bg='black', font=('Roboto Bold', 12),
                           relief="groove", command=lambda: controller.show_frame("Frame2"))
        button.place(x=0, y=0)
    def update_clock(self, current_time):
        self.clock_label.config(text=current_time)


app = App()
app.mainloop()
