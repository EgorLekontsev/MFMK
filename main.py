import tkinter as tk
from tkinter import PhotoImage, Canvas, messagebox, ttk
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageTk
from platform import system
from re import sub
from subprocess import check_output
from socket import socket, AF_INET, SOCK_DGRAM
import wmi
import psutil
import os

import keypad
import numpad
import json_methods

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
class App(tk.Tk):
    # Основной класс с характеристиками окна
    # Будет содержать какие-то глобальные значения внутри сессии
    file_path = "data/desktop_journal/"+datetime.now().strftime("%d.%m.%Y")+".json"
    if not os.path.exists(file_path):
        json_methods.save_data(file_path, [])
    journal_data = json_methods.load_data(file_path)
    storage_data = json_methods.load_data(r"data/desktop_storage.json")

    Pumps_active = int(storage_data["Pumps"])
    LVL_access = 10
    session_access = False
    global_controller = None
    numpad_instance = 0
    after_function = 0

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

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        print("TESTING")
        print(App.journal_data)
        #App.global_controller.frames["Frame8"].update_tree(datetime.now().strftime("%d.%m.%Y"))
        json_methods.save_data(App.file_path, App.journal_data)
        self.destroy()

    def shields_hide(event=None): #Сокрытие щитов, а также вызов метода показа щитов
        if App.LVL_access == 0:
            App.global_controller.frames["Frame2"].canvas.itemconfig(App.global_controller.frames["Frame2"].shield1,
                                                                     state='hidden')
            App.global_controller.frames["Frame2"].canvas.itemconfig(App.global_controller.frames["Frame2"].shield2,
                                                                     state='hidden')
            App.global_controller.frames["Frame2"].canvas.itemconfig(App.global_controller.frames["Frame2"].shield3,
                                                                     state='hidden')
            App.global_controller.frames["Frame2"].canvas.itemconfig(App.global_controller.frames["Frame2"].shield4,
                                                                     state='hidden')
            App.global_controller.frames["Frame2"].canvas.itemconfig(App.global_controller.frames["Frame2"].shield5,
                                                                     state='hidden')
            App.global_controller.frames["Frame2"].canvas.itemconfig(App.global_controller.frames["Frame2"].shield6,
                                                                     state='hidden')
            App.global_controller.frames["Frame9"].canvas.itemconfig(App.global_controller.frames["Frame9"].shield1,
                                                                     state='hidden')
            App.global_controller.frames["Frame9"].canvas.itemconfig(App.global_controller.frames["Frame9"].shield2,
                                                                     state='hidden')
            App.global_controller.frames["Frame9"].canvas.itemconfig(App.global_controller.frames["Frame9"].shield3,
                                                                     state='hidden')
            App.global_controller.frames["Frame9"].canvas.itemconfig(App.global_controller.frames["Frame9"].shield4,
                                                                     state='hidden')
            App.global_controller.frames["Frame9"].canvas.itemconfig(App.global_controller.frames["Frame9"].shield5,
                                                                     state='hidden')
            App.global_controller.frames["Frame9"].canvas.itemconfig(App.global_controller.frames["Frame9"].shield6,
                                                                     state='hidden')
            App.global_controller.frames["Frame9"].canvas.itemconfig(App.global_controller.frames["Frame9"].shield7,
                                                                     state='hidden')
            App.global_controller.frames["Frame9"].canvas.itemconfig(App.global_controller.frames["Frame9"].shield8,
                                                                     state='hidden')
            App.global_controller.frames["Frame9"].canvas.itemconfig(App.global_controller.frames["Frame9"].shield9,
                                                                     state='hidden')
            App.global_controller.frames["Frame10"].canvas.itemconfig(App.global_controller.frames["Frame10"].shield1,
                                                                      state='hidden')
            App.global_controller.frames["Frame10"].canvas.itemconfig(App.global_controller.frames["Frame10"].shield2,
                                                                      state='hidden')
            App.global_controller.frames["Frame11"].canvas.itemconfig(App.global_controller.frames["Frame11"].shield1,
                                                                      state='hidden')
            App.global_controller.frames["Frame11"].canvas.itemconfig(App.global_controller.frames["Frame11"].shield2,
                                                                      state='hidden')
            App.global_controller.frames["Frame11"].canvas.itemconfig(App.global_controller.frames["Frame11"].shield3,
                                                                      state='hidden')
            App.global_controller.frames["Frame11"].canvas.itemconfig(App.global_controller.frames["Frame11"].shield4,
                                                                      state='hidden')
            App.global_controller.frames["Frame11"].canvas.itemconfig(App.global_controller.frames["Frame11"].shield5,
                                                                      state='hidden')
            App.global_controller.frames["Frame11"].canvas.itemconfig(App.global_controller.frames["Frame11"].shield6,
                                                                      state='hidden')
            App.global_controller.frames["Frame12"].canvas.itemconfig(App.global_controller.frames["Frame12"].shield1,
                                                                      state='hidden')
            App.global_controller.frames["Frame12"].canvas.itemconfig(App.global_controller.frames["Frame12"].shield2,
                                                                      state='hidden')
            App.global_controller.frames["Frame12"].canvas.itemconfig(App.global_controller.frames["Frame12"].shield3,
                                                                      state='hidden')
            App.global_controller.frames["Frame12"].canvas.itemconfig(App.global_controller.frames["Frame12"].shield4,
                                                                      state='hidden')
            App.global_controller.frames["Frame12"].canvas.itemconfig(App.global_controller.frames["Frame12"].shield5,
                                                                      state='hidden')
            App.global_controller.frames["Frame12"].canvas.itemconfig(App.global_controller.frames["Frame12"].shield6,
                                                                      state='hidden')
            App.global_controller.frames["Frame12"].canvas.itemconfig(App.global_controller.frames["Frame12"].shield7,
                                                                      state='hidden')
            App.global_controller.frames["Frame12"].canvas.itemconfig(App.global_controller.frames["Frame12"].shield8,
                                                                      state='hidden')
            App.global_controller.frames["Frame13"].canvas.itemconfig(App.global_controller.frames["Frame13"].shield1,
                                                                      state='hidden')
            App.global_controller.frames["Frame13"].canvas.itemconfig(App.global_controller.frames["Frame13"].shield2,
                                                                      state='hidden')
            App.global_controller.frames["Frame13"].canvas.itemconfig(App.global_controller.frames["Frame13"].shield3,
                                                                      state='hidden')
            App.global_controller.frames["Frame13"].canvas.itemconfig(App.global_controller.frames["Frame13"].shield4,
                                                                      state='hidden')
            App.global_controller.frames["Frame13"].canvas.itemconfig(App.global_controller.frames["Frame13"].shield5,
                                                                      state='hidden')
            App.global_controller.frames["Frame13"].canvas.itemconfig(App.global_controller.frames["Frame13"].shield6,
                                                                      state='hidden')
            App.global_controller.frames["Frame13"].canvas.itemconfig(App.global_controller.frames["Frame13"].shield7,
                                                                      state='hidden')
            App.global_controller.frames["Frame13"].canvas.itemconfig(App.global_controller.frames["Frame13"].shield8,
                                                                      state='hidden')
            App.global_controller.frames["Frame14"].canvas.itemconfig(App.global_controller.frames["Frame14"].shield1,
                                                                      state='hidden')
            App.global_controller.frames["Frame14"].canvas.itemconfig(App.global_controller.frames["Frame14"].shield2,
                                                                      state='hidden')
            App.global_controller.frames["Frame14"].canvas.itemconfig(App.global_controller.frames["Frame14"].shield3,
                                                                      state='hidden')
            App.global_controller.frames["Frame14"].canvas.itemconfig(App.global_controller.frames["Frame14"].shield4,
                                                                      state='hidden')
            App.global_controller.frames["Frame14"].canvas.itemconfig(App.global_controller.frames["Frame14"].shield5,
                                                                      state='hidden')
            App.global_controller.frames["Frame14"].canvas.itemconfig(App.global_controller.frames["Frame14"].shield6,
                                                                      state='hidden')
            App.global_controller.frames["Frame14"].canvas.itemconfig(App.global_controller.frames["Frame14"].shield7,
                                                                      state='hidden')
            App.global_controller.frames["Frame15"].canvas.itemconfig(App.global_controller.frames["Frame15"].shield1,
                                                                      state='hidden')
            App.global_controller.frames["Frame15"].canvas.itemconfig(App.global_controller.frames["Frame15"].shield2,
                                                                      state='hidden')
            App.global_controller.frames["Frame15"].canvas.itemconfig(App.global_controller.frames["Frame15"].shield3,
                                                                      state='hidden')
            App.global_controller.frames["Frame15"].canvas.itemconfig(App.global_controller.frames["Frame15"].shield4,
                                                                      state='hidden')
            App.global_controller.frames["Frame15"].canvas.itemconfig(App.global_controller.frames["Frame15"].shield5,
                                                                      state='hidden')
            App.global_controller.frames["Frame15"].canvas.itemconfig(App.global_controller.frames["Frame15"].shield6,
                                                                      state='hidden')
            App.global_controller.frames["Frame15"].canvas.itemconfig(App.global_controller.frames["Frame15"].shield7,
                                                                      state='hidden')
            App.global_controller.frames["Frame15"].canvas.itemconfig(App.global_controller.frames["Frame15"].shield8,
                                                                      state='hidden')
            App.global_controller.frames["Frame15"].canvas.itemconfig(App.global_controller.frames["Frame15"].shield9,
                                                                      state='hidden')
            App.global_controller.frames["Frame16"].canvas.itemconfig(App.global_controller.frames["Frame16"].shield1,
                                                                      state='hidden')
            App.global_controller.frames["Frame16"].canvas.itemconfig(App.global_controller.frames["Frame16"].shield2,
                                                                      state='hidden')
            App.global_controller.frames["Frame16"].canvas.itemconfig(App.global_controller.frames["Frame16"].shield3,
                                                                      state='hidden')
            App.global_controller.frames["Frame16"].canvas.itemconfig(App.global_controller.frames["Frame16"].shield4,
                                                                      state='hidden')
            App.global_controller.frames["Frame16"].canvas.itemconfig(App.global_controller.frames["Frame16"].shield5,
                                                                      state='hidden')
            App.global_controller.frames["Frame16"].canvas.itemconfig(App.global_controller.frames["Frame16"].shield6,
                                                                      state='hidden')
            App.global_controller.frames["Frame18"].canvas.itemconfig(App.global_controller.frames["Frame18"].shield1,
                                                                      state='hidden')
            App.global_controller.frames["Frame18"].canvas.itemconfig(App.global_controller.frames["Frame18"].shield2,
                                                                      state='hidden')
            App.global_controller.frames["Frame18"].canvas.itemconfig(App.global_controller.frames["Frame18"].shield3,
                                                                      state='hidden')
            App.global_controller.frames["Frame18"].canvas.itemconfig(App.global_controller.frames["Frame18"].shield4,
                                                                      state='hidden')
            App.global_controller.frames["Frame19"].canvas.itemconfig(App.global_controller.frames["Frame19"].shield1,
                                                                      state='hidden')
            App.global_controller.frames["Frame19"].canvas.itemconfig(App.global_controller.frames["Frame19"].shield2,
                                                                      state='hidden')
            App.global_controller.frames["Frame19"].canvas.itemconfig(App.global_controller.frames["Frame19"].shield3,
                                                                      state='hidden')
            App.global_controller.frames["Frame19"].canvas.itemconfig(App.global_controller.frames["Frame19"].shield4,
                                                                      state='hidden')
            App.global_controller.frames["Frame19"].canvas.itemconfig(App.global_controller.frames["Frame19"].shield5,
                                                                      state='hidden')
            App.global_controller.frames["Frame19"].canvas.itemconfig(App.global_controller.frames["Frame19"].shield6,
                                                                      state='hidden')
            App.global_controller.frames["Frame19"].canvas.itemconfig(App.global_controller.frames["Frame19"].shield7,
                                                                      state='hidden')
            App.global_controller.frames["Frame19"].canvas.itemconfig(App.global_controller.frames["Frame19"].shield8,
                                                                      state='hidden')
            App.global_controller.frames["Frame20"].canvas.itemconfig(App.global_controller.frames["Frame20"].shield1,
                                                                      state='hidden')
        elif App.LVL_access == 5:
            App.global_controller.frames["Frame2"].canvas.itemconfig(App.global_controller.frames["Frame2"].shield1,
                                                                     state='hidden')
            App.global_controller.frames["Frame2"].canvas.itemconfig(App.global_controller.frames["Frame2"].shield2,
                                                                     state='hidden')
            App.global_controller.frames["Frame2"].canvas.itemconfig(App.global_controller.frames["Frame2"].shield3,
                                                                     state='hidden')
            App.global_controller.frames["Frame2"].canvas.itemconfig(App.global_controller.frames["Frame2"].shield4,
                                                                     state='hidden')
            App.global_controller.frames["Frame2"].canvas.itemconfig(App.global_controller.frames["Frame2"].shield5,
                                                                     state='hidden')
            App.global_controller.frames["Frame2"].canvas.itemconfig(App.global_controller.frames["Frame2"].shield6,
                                                                     state='hidden')
            App.global_controller.frames["Frame9"].canvas.itemconfig(App.global_controller.frames["Frame9"].shield1,
                                                                     state='hidden')
            App.global_controller.frames["Frame9"].canvas.itemconfig(App.global_controller.frames["Frame9"].shield2,
                                                                     state='hidden')
            App.global_controller.frames["Frame9"].canvas.itemconfig(App.global_controller.frames["Frame9"].shield3,
                                                                     state='hidden')
            App.global_controller.frames["Frame9"].canvas.itemconfig(App.global_controller.frames["Frame9"].shield4,
                                                                     state='hidden')
            App.global_controller.frames["Frame9"].canvas.itemconfig(App.global_controller.frames["Frame9"].shield5,
                                                                     state='hidden')
            App.global_controller.frames["Frame9"].canvas.itemconfig(App.global_controller.frames["Frame9"].shield6,
                                                                     state='hidden')
            App.global_controller.frames["Frame9"].canvas.itemconfig(App.global_controller.frames["Frame9"].shield7,
                                                                     state='hidden')
            App.global_controller.frames["Frame9"].canvas.itemconfig(App.global_controller.frames["Frame9"].shield8,
                                                                     state='hidden')
            App.global_controller.frames["Frame9"].canvas.itemconfig(App.global_controller.frames["Frame9"].shield9,
                                                                     state='hidden')
            App.global_controller.frames["Frame10"].canvas.itemconfig(App.global_controller.frames["Frame10"].shield1,
                                                                      state='hidden')
            App.global_controller.frames["Frame10"].canvas.itemconfig(App.global_controller.frames["Frame10"].shield2,
                                                                      state='hidden')
            App.global_controller.frames["Frame11"].canvas.itemconfig(App.global_controller.frames["Frame11"].shield1,
                                                                      state='hidden')
            App.global_controller.frames["Frame11"].canvas.itemconfig(App.global_controller.frames["Frame11"].shield2,
                                                                      state='hidden')
            App.global_controller.frames["Frame11"].canvas.itemconfig(App.global_controller.frames["Frame11"].shield3,
                                                                      state='hidden')
            App.global_controller.frames["Frame11"].canvas.itemconfig(App.global_controller.frames["Frame11"].shield4,
                                                                      state='hidden')
            App.global_controller.frames["Frame11"].canvas.itemconfig(App.global_controller.frames["Frame11"].shield5,
                                                                      state='hidden')
            App.global_controller.frames["Frame11"].canvas.itemconfig(App.global_controller.frames["Frame11"].shield6,
                                                                      state='hidden')
            App.global_controller.frames["Frame12"].canvas.itemconfig(App.global_controller.frames["Frame12"].shield1,
                                                                      state='hidden')
            App.global_controller.frames["Frame12"].canvas.itemconfig(App.global_controller.frames["Frame12"].shield2,
                                                                      state='hidden')
            App.global_controller.frames["Frame12"].canvas.itemconfig(App.global_controller.frames["Frame12"].shield3,
                                                                      state='hidden')
            App.global_controller.frames["Frame12"].canvas.itemconfig(App.global_controller.frames["Frame12"].shield4,
                                                                      state='hidden')
            App.global_controller.frames["Frame12"].canvas.itemconfig(App.global_controller.frames["Frame12"].shield5,
                                                                      state='hidden')
            App.global_controller.frames["Frame12"].canvas.itemconfig(App.global_controller.frames["Frame12"].shield6,
                                                                      state='hidden')
            App.global_controller.frames["Frame12"].canvas.itemconfig(App.global_controller.frames["Frame12"].shield7,
                                                                      state='hidden')
            App.global_controller.frames["Frame12"].canvas.itemconfig(App.global_controller.frames["Frame12"].shield8,
                                                                      state='hidden')
            App.global_controller.frames["Frame13"].canvas.itemconfig(App.global_controller.frames["Frame13"].shield1,
                                                                      state='hidden')
            App.global_controller.frames["Frame13"].canvas.itemconfig(App.global_controller.frames["Frame13"].shield2,
                                                                      state='hidden')
            App.global_controller.frames["Frame13"].canvas.itemconfig(App.global_controller.frames["Frame13"].shield3,
                                                                      state='hidden')
            App.global_controller.frames["Frame13"].canvas.itemconfig(App.global_controller.frames["Frame13"].shield4,
                                                                      state='hidden')
            App.global_controller.frames["Frame13"].canvas.itemconfig(App.global_controller.frames["Frame13"].shield5,
                                                                      state='hidden')
            App.global_controller.frames["Frame13"].canvas.itemconfig(App.global_controller.frames["Frame13"].shield6,
                                                                      state='hidden')
            App.global_controller.frames["Frame13"].canvas.itemconfig(App.global_controller.frames["Frame13"].shield7,
                                                                      state='hidden')
            App.global_controller.frames["Frame13"].canvas.itemconfig(App.global_controller.frames["Frame13"].shield8,
                                                                      state='hidden')
            App.global_controller.frames["Frame14"].canvas.itemconfig(App.global_controller.frames["Frame14"].shield1,
                                                                      state='hidden')
            App.global_controller.frames["Frame14"].canvas.itemconfig(App.global_controller.frames["Frame14"].shield2,
                                                                      state='hidden')
            App.global_controller.frames["Frame14"].canvas.itemconfig(App.global_controller.frames["Frame14"].shield3,
                                                                      state='hidden')
            App.global_controller.frames["Frame14"].canvas.itemconfig(App.global_controller.frames["Frame14"].shield4,
                                                                      state='hidden')
            App.global_controller.frames["Frame14"].canvas.itemconfig(App.global_controller.frames["Frame14"].shield5,
                                                                      state='hidden')
            App.global_controller.frames["Frame14"].canvas.itemconfig(App.global_controller.frames["Frame14"].shield6,
                                                                      state='hidden')
            App.global_controller.frames["Frame14"].canvas.itemconfig(App.global_controller.frames["Frame14"].shield7,
                                                                      state='hidden')
            App.global_controller.frames["Frame15"].canvas.itemconfig(App.global_controller.frames["Frame15"].shield1,
                                                                      state='hidden')
            App.global_controller.frames["Frame15"].canvas.itemconfig(App.global_controller.frames["Frame15"].shield2,
                                                                      state='hidden')
            App.global_controller.frames["Frame15"].canvas.itemconfig(App.global_controller.frames["Frame15"].shield3,
                                                                      state='hidden')
            App.global_controller.frames["Frame15"].canvas.itemconfig(App.global_controller.frames["Frame15"].shield4,
                                                                      state='hidden')
            App.global_controller.frames["Frame15"].canvas.itemconfig(App.global_controller.frames["Frame15"].shield5,
                                                                      state='hidden')
            App.global_controller.frames["Frame15"].canvas.itemconfig(App.global_controller.frames["Frame15"].shield6,
                                                                      state='hidden')
            App.global_controller.frames["Frame15"].canvas.itemconfig(App.global_controller.frames["Frame15"].shield7,
                                                                      state='hidden')
            App.global_controller.frames["Frame15"].canvas.itemconfig(App.global_controller.frames["Frame15"].shield8,
                                                                      state='hidden')
            App.global_controller.frames["Frame15"].canvas.itemconfig(App.global_controller.frames["Frame15"].shield9,
                                                                      state='hidden')
            App.global_controller.frames["Frame16"].canvas.itemconfig(App.global_controller.frames["Frame16"].shield1,
                                                                      state='hidden')
            App.global_controller.frames["Frame16"].canvas.itemconfig(App.global_controller.frames["Frame16"].shield2,
                                                                      state='hidden')
            App.global_controller.frames["Frame16"].canvas.itemconfig(App.global_controller.frames["Frame16"].shield3,
                                                                      state='hidden')
            App.global_controller.frames["Frame16"].canvas.itemconfig(App.global_controller.frames["Frame16"].shield4,
                                                                      state='hidden')
            App.global_controller.frames["Frame16"].canvas.itemconfig(App.global_controller.frames["Frame16"].shield5,
                                                                      state='hidden')
            App.global_controller.frames["Frame16"].canvas.itemconfig(App.global_controller.frames["Frame16"].shield6,
                                                                      state='hidden')
            App.global_controller.frames["Frame18"].canvas.itemconfig(App.global_controller.frames["Frame18"].shield1,
                                                                      state='hidden')
            App.global_controller.frames["Frame18"].canvas.itemconfig(App.global_controller.frames["Frame18"].shield2,
                                                                      state='hidden')
            App.global_controller.frames["Frame18"].canvas.itemconfig(App.global_controller.frames["Frame18"].shield3,
                                                                      state='hidden')
            App.global_controller.frames["Frame18"].canvas.itemconfig(App.global_controller.frames["Frame18"].shield4,
                                                                      state='hidden')
            App.global_controller.frames["Frame19"].canvas.itemconfig(App.global_controller.frames["Frame19"].shield1,
                                                                      state='hidden')
            App.global_controller.frames["Frame19"].canvas.itemconfig(App.global_controller.frames["Frame19"].shield2,
                                                                      state='hidden')
            App.global_controller.frames["Frame19"].canvas.itemconfig(App.global_controller.frames["Frame19"].shield3,
                                                                      state='hidden')
            App.global_controller.frames["Frame19"].canvas.itemconfig(App.global_controller.frames["Frame19"].shield4,
                                                                      state='hidden')
            App.global_controller.frames["Frame19"].canvas.itemconfig(App.global_controller.frames["Frame19"].shield5,
                                                                      state='hidden')
            App.global_controller.frames["Frame19"].canvas.itemconfig(App.global_controller.frames["Frame19"].shield6,
                                                                      state='hidden')
            App.global_controller.frames["Frame19"].canvas.itemconfig(App.global_controller.frames["Frame19"].shield7,
                                                                      state='hidden')
            App.global_controller.frames["Frame19"].canvas.itemconfig(App.global_controller.frames["Frame19"].shield8,
                                                                      state='hidden')
        elif App.LVL_access == 7:
            App.global_controller.frames["Frame2"].canvas.itemconfig(App.global_controller.frames["Frame2"].shield1,
                                                                     state='hidden')
            App.global_controller.frames["Frame2"].canvas.itemconfig(App.global_controller.frames["Frame2"].shield2,
                                                                     state='hidden')
            App.global_controller.frames["Frame2"].canvas.itemconfig(App.global_controller.frames["Frame2"].shield3,
                                                                     state='hidden')
            App.global_controller.frames["Frame2"].canvas.itemconfig(App.global_controller.frames["Frame2"].shield4,
                                                                     state='hidden')
            App.global_controller.frames["Frame2"].canvas.itemconfig(App.global_controller.frames["Frame2"].shield5,
                                                                     state='hidden')
            App.global_controller.frames["Frame2"].canvas.itemconfig(App.global_controller.frames["Frame2"].shield6,
                                                                     state='hidden')
        if App.after_function != 0:
            App.global_controller.frames["Frame1_1"].after_cancel(App.after_function)
        App.after_function = App.global_controller.frames["Frame1_1"].after(10000, App.shields_show)

    def shields_show(event=None):
        if App.LVL_access == 0:
            App.global_controller.frames["Frame2"].canvas.itemconfig(App.global_controller.frames["Frame2"].shield1,
                                                                     state='normal')
            App.global_controller.frames["Frame2"].canvas.itemconfig(App.global_controller.frames["Frame2"].shield2,
                                                                     state='normal')
            App.global_controller.frames["Frame2"].canvas.itemconfig(App.global_controller.frames["Frame2"].shield3,
                                                                     state='normal')
            App.global_controller.frames["Frame2"].canvas.itemconfig(App.global_controller.frames["Frame2"].shield4,
                                                                     state='normal')
            App.global_controller.frames["Frame2"].canvas.itemconfig(App.global_controller.frames["Frame2"].shield5,
                                                                     state='normal')
            App.global_controller.frames["Frame2"].canvas.itemconfig(App.global_controller.frames["Frame2"].shield6,
                                                                     state='normal')
            App.global_controller.frames["Frame9"].canvas.itemconfig(App.global_controller.frames["Frame9"].shield1,
                                                                     state='normal')
            App.global_controller.frames["Frame9"].canvas.itemconfig(App.global_controller.frames["Frame9"].shield2,
                                                                     state='normal')
            App.global_controller.frames["Frame9"].canvas.itemconfig(App.global_controller.frames["Frame9"].shield3,
                                                                     state='normal')
            App.global_controller.frames["Frame9"].canvas.itemconfig(App.global_controller.frames["Frame9"].shield4,
                                                                     state='normal')
            App.global_controller.frames["Frame9"].canvas.itemconfig(App.global_controller.frames["Frame9"].shield5,
                                                                     state='normal')
            App.global_controller.frames["Frame9"].canvas.itemconfig(App.global_controller.frames["Frame9"].shield6,
                                                                     state='normal')
            App.global_controller.frames["Frame9"].canvas.itemconfig(App.global_controller.frames["Frame9"].shield7,
                                                                     state='normal')
            App.global_controller.frames["Frame9"].canvas.itemconfig(App.global_controller.frames["Frame9"].shield8,
                                                                     state='normal')
            App.global_controller.frames["Frame9"].canvas.itemconfig(App.global_controller.frames["Frame9"].shield9,
                                                                     state='normal')
            App.global_controller.frames["Frame10"].canvas.itemconfig(App.global_controller.frames["Frame10"].shield1,
                                                                      state='normal')
            App.global_controller.frames["Frame10"].canvas.itemconfig(App.global_controller.frames["Frame10"].shield2,
                                                                      state='normal')
            App.global_controller.frames["Frame11"].canvas.itemconfig(App.global_controller.frames["Frame11"].shield1,
                                                                      state='normal')
            App.global_controller.frames["Frame11"].canvas.itemconfig(App.global_controller.frames["Frame11"].shield2,
                                                                      state='normal')
            App.global_controller.frames["Frame11"].canvas.itemconfig(App.global_controller.frames["Frame11"].shield3,
                                                                      state='normal')
            App.global_controller.frames["Frame11"].canvas.itemconfig(App.global_controller.frames["Frame11"].shield4,
                                                                      state='normal')
            App.global_controller.frames["Frame11"].canvas.itemconfig(App.global_controller.frames["Frame11"].shield5,
                                                                      state='normal')
            App.global_controller.frames["Frame11"].canvas.itemconfig(App.global_controller.frames["Frame11"].shield6,
                                                                      state='normal')
            App.global_controller.frames["Frame12"].canvas.itemconfig(App.global_controller.frames["Frame12"].shield1,
                                                                      state='normal')
            App.global_controller.frames["Frame12"].canvas.itemconfig(App.global_controller.frames["Frame12"].shield2,
                                                                      state='normal')
            App.global_controller.frames["Frame12"].canvas.itemconfig(App.global_controller.frames["Frame12"].shield3,
                                                                      state='normal')
            App.global_controller.frames["Frame12"].canvas.itemconfig(App.global_controller.frames["Frame12"].shield4,
                                                                      state='normal')
            App.global_controller.frames["Frame12"].canvas.itemconfig(App.global_controller.frames["Frame12"].shield5,
                                                                      state='normal')
            App.global_controller.frames["Frame12"].canvas.itemconfig(App.global_controller.frames["Frame12"].shield6,
                                                                      state='normal')
            App.global_controller.frames["Frame12"].canvas.itemconfig(App.global_controller.frames["Frame12"].shield7,
                                                                      state='normal')
            App.global_controller.frames["Frame12"].canvas.itemconfig(App.global_controller.frames["Frame12"].shield8,
                                                                      state='normal')
            App.global_controller.frames["Frame13"].canvas.itemconfig(App.global_controller.frames["Frame13"].shield1,
                                                                      state='normal')
            App.global_controller.frames["Frame13"].canvas.itemconfig(App.global_controller.frames["Frame13"].shield2,
                                                                      state='normal')
            App.global_controller.frames["Frame13"].canvas.itemconfig(App.global_controller.frames["Frame13"].shield3,
                                                                      state='normal')
            App.global_controller.frames["Frame13"].canvas.itemconfig(App.global_controller.frames["Frame13"].shield4,
                                                                      state='normal')
            App.global_controller.frames["Frame13"].canvas.itemconfig(App.global_controller.frames["Frame13"].shield5,
                                                                      state='normal')
            App.global_controller.frames["Frame13"].canvas.itemconfig(App.global_controller.frames["Frame13"].shield6,
                                                                      state='normal')
            App.global_controller.frames["Frame13"].canvas.itemconfig(App.global_controller.frames["Frame13"].shield7,
                                                                      state='normal')
            App.global_controller.frames["Frame13"].canvas.itemconfig(App.global_controller.frames["Frame13"].shield8,
                                                                      state='normal')
            App.global_controller.frames["Frame14"].canvas.itemconfig(App.global_controller.frames["Frame14"].shield1,
                                                                      state='normal')
            App.global_controller.frames["Frame14"].canvas.itemconfig(App.global_controller.frames["Frame14"].shield2,
                                                                      state='normal')
            App.global_controller.frames["Frame14"].canvas.itemconfig(App.global_controller.frames["Frame14"].shield3,
                                                                      state='normal')
            App.global_controller.frames["Frame14"].canvas.itemconfig(App.global_controller.frames["Frame14"].shield4,
                                                                      state='normal')
            App.global_controller.frames["Frame14"].canvas.itemconfig(App.global_controller.frames["Frame14"].shield5,
                                                                      state='normal')
            App.global_controller.frames["Frame14"].canvas.itemconfig(App.global_controller.frames["Frame14"].shield6,
                                                                      state='normal')
            App.global_controller.frames["Frame14"].canvas.itemconfig(App.global_controller.frames["Frame14"].shield7,
                                                                      state='normal')
            App.global_controller.frames["Frame15"].canvas.itemconfig(App.global_controller.frames["Frame15"].shield1,
                                                                      state='normal')
            App.global_controller.frames["Frame15"].canvas.itemconfig(App.global_controller.frames["Frame15"].shield2,
                                                                      state='normal')
            App.global_controller.frames["Frame15"].canvas.itemconfig(App.global_controller.frames["Frame15"].shield3,
                                                                      state='normal')
            App.global_controller.frames["Frame15"].canvas.itemconfig(App.global_controller.frames["Frame15"].shield4,
                                                                      state='normal')
            App.global_controller.frames["Frame15"].canvas.itemconfig(App.global_controller.frames["Frame15"].shield5,
                                                                      state='normal')
            App.global_controller.frames["Frame15"].canvas.itemconfig(App.global_controller.frames["Frame15"].shield6,
                                                                      state='normal')
            App.global_controller.frames["Frame15"].canvas.itemconfig(App.global_controller.frames["Frame15"].shield7,
                                                                      state='normal')
            App.global_controller.frames["Frame15"].canvas.itemconfig(App.global_controller.frames["Frame15"].shield8,
                                                                      state='normal')
            App.global_controller.frames["Frame15"].canvas.itemconfig(App.global_controller.frames["Frame15"].shield9,
                                                                      state='normal')
            App.global_controller.frames["Frame16"].canvas.itemconfig(App.global_controller.frames["Frame16"].shield1,
                                                                      state='normal')
            App.global_controller.frames["Frame16"].canvas.itemconfig(App.global_controller.frames["Frame16"].shield2,
                                                                      state='normal')
            App.global_controller.frames["Frame16"].canvas.itemconfig(App.global_controller.frames["Frame16"].shield3,
                                                                      state='normal')
            App.global_controller.frames["Frame16"].canvas.itemconfig(App.global_controller.frames["Frame16"].shield4,
                                                                      state='normal')
            App.global_controller.frames["Frame16"].canvas.itemconfig(App.global_controller.frames["Frame16"].shield5,
                                                                      state='normal')
            App.global_controller.frames["Frame16"].canvas.itemconfig(App.global_controller.frames["Frame16"].shield6,
                                                                      state='normal')
            App.global_controller.frames["Frame18"].canvas.itemconfig(App.global_controller.frames["Frame18"].shield1,
                                                                      state='normal')
            App.global_controller.frames["Frame18"].canvas.itemconfig(App.global_controller.frames["Frame18"].shield2,
                                                                      state='normal')
            App.global_controller.frames["Frame18"].canvas.itemconfig(App.global_controller.frames["Frame18"].shield3,
                                                                      state='normal')
            App.global_controller.frames["Frame18"].canvas.itemconfig(App.global_controller.frames["Frame18"].shield4,
                                                                      state='normal')
            App.global_controller.frames["Frame19"].canvas.itemconfig(App.global_controller.frames["Frame19"].shield1,
                                                                      state='normal')
            App.global_controller.frames["Frame19"].canvas.itemconfig(App.global_controller.frames["Frame19"].shield2,
                                                                      state='normal')
            App.global_controller.frames["Frame19"].canvas.itemconfig(App.global_controller.frames["Frame19"].shield3,
                                                                      state='normal')
            App.global_controller.frames["Frame19"].canvas.itemconfig(App.global_controller.frames["Frame19"].shield4,
                                                                      state='normal')
            App.global_controller.frames["Frame19"].canvas.itemconfig(App.global_controller.frames["Frame19"].shield5,
                                                                      state='normal')
            App.global_controller.frames["Frame19"].canvas.itemconfig(App.global_controller.frames["Frame19"].shield6,
                                                                      state='normal')
            App.global_controller.frames["Frame19"].canvas.itemconfig(App.global_controller.frames["Frame19"].shield7,
                                                                      state='normal')
            App.global_controller.frames["Frame19"].canvas.itemconfig(App.global_controller.frames["Frame19"].shield8,
                                                                      state='normal')
            App.global_controller.frames["Frame20"].canvas.itemconfig(App.global_controller.frames["Frame20"].shield1,
                                                                      state='normal')
        elif App.LVL_access == 5:
            App.global_controller.frames["Frame2"].canvas.itemconfig(App.global_controller.frames["Frame2"].shield1,
                                                                     state='normal')
            App.global_controller.frames["Frame2"].canvas.itemconfig(App.global_controller.frames["Frame2"].shield2,
                                                                     state='normal')
            App.global_controller.frames["Frame2"].canvas.itemconfig(App.global_controller.frames["Frame2"].shield3,
                                                                     state='normal')
            App.global_controller.frames["Frame2"].canvas.itemconfig(App.global_controller.frames["Frame2"].shield4,
                                                                     state='normal')
            App.global_controller.frames["Frame2"].canvas.itemconfig(App.global_controller.frames["Frame2"].shield5,
                                                                     state='normal')
            App.global_controller.frames["Frame2"].canvas.itemconfig(App.global_controller.frames["Frame2"].shield6,
                                                                     state='normal')
            App.global_controller.frames["Frame9"].canvas.itemconfig(App.global_controller.frames["Frame9"].shield1,
                                                                     state='normal')
            App.global_controller.frames["Frame9"].canvas.itemconfig(App.global_controller.frames["Frame9"].shield2,
                                                                     state='normal')
            App.global_controller.frames["Frame9"].canvas.itemconfig(App.global_controller.frames["Frame9"].shield3,
                                                                     state='normal')
            App.global_controller.frames["Frame9"].canvas.itemconfig(App.global_controller.frames["Frame9"].shield4,
                                                                     state='normal')
            App.global_controller.frames["Frame9"].canvas.itemconfig(App.global_controller.frames["Frame9"].shield5,
                                                                     state='normal')
            App.global_controller.frames["Frame9"].canvas.itemconfig(App.global_controller.frames["Frame9"].shield6,
                                                                     state='normal')
            App.global_controller.frames["Frame9"].canvas.itemconfig(App.global_controller.frames["Frame9"].shield7,
                                                                     state='normal')
            App.global_controller.frames["Frame9"].canvas.itemconfig(App.global_controller.frames["Frame9"].shield8,
                                                                     state='normal')
            App.global_controller.frames["Frame9"].canvas.itemconfig(App.global_controller.frames["Frame9"].shield9,
                                                                     state='normal')
            App.global_controller.frames["Frame10"].canvas.itemconfig(App.global_controller.frames["Frame10"].shield1,
                                                                      state='normal')
            App.global_controller.frames["Frame10"].canvas.itemconfig(App.global_controller.frames["Frame10"].shield2,
                                                                      state='normal')
            App.global_controller.frames["Frame11"].canvas.itemconfig(App.global_controller.frames["Frame11"].shield1,
                                                                      state='normal')
            App.global_controller.frames["Frame11"].canvas.itemconfig(App.global_controller.frames["Frame11"].shield2,
                                                                      state='normal')
            App.global_controller.frames["Frame11"].canvas.itemconfig(App.global_controller.frames["Frame11"].shield3,
                                                                      state='normal')
            App.global_controller.frames["Frame11"].canvas.itemconfig(App.global_controller.frames["Frame11"].shield4,
                                                                      state='normal')
            App.global_controller.frames["Frame11"].canvas.itemconfig(App.global_controller.frames["Frame11"].shield5,
                                                                      state='normal')
            App.global_controller.frames["Frame11"].canvas.itemconfig(App.global_controller.frames["Frame11"].shield6,
                                                                      state='normal')
            App.global_controller.frames["Frame12"].canvas.itemconfig(App.global_controller.frames["Frame12"].shield1,
                                                                      state='normal')
            App.global_controller.frames["Frame12"].canvas.itemconfig(App.global_controller.frames["Frame12"].shield2,
                                                                      state='normal')
            App.global_controller.frames["Frame12"].canvas.itemconfig(App.global_controller.frames["Frame12"].shield3,
                                                                      state='normal')
            App.global_controller.frames["Frame12"].canvas.itemconfig(App.global_controller.frames["Frame12"].shield4,
                                                                      state='normal')
            App.global_controller.frames["Frame12"].canvas.itemconfig(App.global_controller.frames["Frame12"].shield5,
                                                                      state='normal')
            App.global_controller.frames["Frame12"].canvas.itemconfig(App.global_controller.frames["Frame12"].shield6,
                                                                      state='normal')
            App.global_controller.frames["Frame12"].canvas.itemconfig(App.global_controller.frames["Frame12"].shield7,
                                                                      state='normal')
            App.global_controller.frames["Frame12"].canvas.itemconfig(App.global_controller.frames["Frame12"].shield8,
                                                                      state='normal')
            App.global_controller.frames["Frame13"].canvas.itemconfig(App.global_controller.frames["Frame13"].shield1,
                                                                      state='normal')
            App.global_controller.frames["Frame13"].canvas.itemconfig(App.global_controller.frames["Frame13"].shield2,
                                                                      state='normal')
            App.global_controller.frames["Frame13"].canvas.itemconfig(App.global_controller.frames["Frame13"].shield3,
                                                                      state='normal')
            App.global_controller.frames["Frame13"].canvas.itemconfig(App.global_controller.frames["Frame13"].shield4,
                                                                      state='normal')
            App.global_controller.frames["Frame13"].canvas.itemconfig(App.global_controller.frames["Frame13"].shield5,
                                                                      state='normal')
            App.global_controller.frames["Frame13"].canvas.itemconfig(App.global_controller.frames["Frame13"].shield6,
                                                                      state='normal')
            App.global_controller.frames["Frame13"].canvas.itemconfig(App.global_controller.frames["Frame13"].shield7,
                                                                      state='normal')
            App.global_controller.frames["Frame13"].canvas.itemconfig(App.global_controller.frames["Frame13"].shield8,
                                                                      state='normal')
            App.global_controller.frames["Frame14"].canvas.itemconfig(App.global_controller.frames["Frame14"].shield1,
                                                                      state='normal')
            App.global_controller.frames["Frame14"].canvas.itemconfig(App.global_controller.frames["Frame14"].shield2,
                                                                      state='normal')
            App.global_controller.frames["Frame14"].canvas.itemconfig(App.global_controller.frames["Frame14"].shield3,
                                                                      state='normal')
            App.global_controller.frames["Frame14"].canvas.itemconfig(App.global_controller.frames["Frame14"].shield4,
                                                                      state='normal')
            App.global_controller.frames["Frame14"].canvas.itemconfig(App.global_controller.frames["Frame14"].shield5,
                                                                      state='normal')
            App.global_controller.frames["Frame14"].canvas.itemconfig(App.global_controller.frames["Frame14"].shield6,
                                                                      state='normal')
            App.global_controller.frames["Frame14"].canvas.itemconfig(App.global_controller.frames["Frame14"].shield7,
                                                                      state='normal')
            App.global_controller.frames["Frame15"].canvas.itemconfig(App.global_controller.frames["Frame15"].shield1,
                                                                      state='normal')
            App.global_controller.frames["Frame15"].canvas.itemconfig(App.global_controller.frames["Frame15"].shield2,
                                                                      state='normal')
            App.global_controller.frames["Frame15"].canvas.itemconfig(App.global_controller.frames["Frame15"].shield3,
                                                                      state='normal')
            App.global_controller.frames["Frame15"].canvas.itemconfig(App.global_controller.frames["Frame15"].shield4,
                                                                      state='normal')
            App.global_controller.frames["Frame15"].canvas.itemconfig(App.global_controller.frames["Frame15"].shield5,
                                                                      state='normal')
            App.global_controller.frames["Frame15"].canvas.itemconfig(App.global_controller.frames["Frame15"].shield6,
                                                                      state='normal')
            App.global_controller.frames["Frame15"].canvas.itemconfig(App.global_controller.frames["Frame15"].shield7,
                                                                      state='normal')
            App.global_controller.frames["Frame15"].canvas.itemconfig(App.global_controller.frames["Frame15"].shield8,
                                                                      state='normal')
            App.global_controller.frames["Frame15"].canvas.itemconfig(App.global_controller.frames["Frame15"].shield9,
                                                                      state='normal')
            App.global_controller.frames["Frame16"].canvas.itemconfig(App.global_controller.frames["Frame16"].shield1,
                                                                      state='normal')
            App.global_controller.frames["Frame16"].canvas.itemconfig(App.global_controller.frames["Frame16"].shield2,
                                                                      state='normal')
            App.global_controller.frames["Frame16"].canvas.itemconfig(App.global_controller.frames["Frame16"].shield3,
                                                                      state='normal')
            App.global_controller.frames["Frame16"].canvas.itemconfig(App.global_controller.frames["Frame16"].shield4,
                                                                      state='normal')
            App.global_controller.frames["Frame16"].canvas.itemconfig(App.global_controller.frames["Frame16"].shield5,
                                                                      state='normal')
            App.global_controller.frames["Frame16"].canvas.itemconfig(App.global_controller.frames["Frame16"].shield6,
                                                                      state='normal')
            App.global_controller.frames["Frame18"].canvas.itemconfig(App.global_controller.frames["Frame18"].shield1,
                                                                      state='normal')
            App.global_controller.frames["Frame18"].canvas.itemconfig(App.global_controller.frames["Frame18"].shield2,
                                                                      state='normal')
            App.global_controller.frames["Frame18"].canvas.itemconfig(App.global_controller.frames["Frame18"].shield3,
                                                                      state='normal')
            App.global_controller.frames["Frame18"].canvas.itemconfig(App.global_controller.frames["Frame18"].shield4,
                                                                      state='normal')
            App.global_controller.frames["Frame19"].canvas.itemconfig(App.global_controller.frames["Frame19"].shield1,
                                                                      state='normal')
            App.global_controller.frames["Frame19"].canvas.itemconfig(App.global_controller.frames["Frame19"].shield2,
                                                                      state='normal')
            App.global_controller.frames["Frame19"].canvas.itemconfig(App.global_controller.frames["Frame19"].shield3,
                                                                      state='normal')
            App.global_controller.frames["Frame19"].canvas.itemconfig(App.global_controller.frames["Frame19"].shield4,
                                                                      state='normal')
            App.global_controller.frames["Frame19"].canvas.itemconfig(App.global_controller.frames["Frame19"].shield5,
                                                                      state='normal')
            App.global_controller.frames["Frame19"].canvas.itemconfig(App.global_controller.frames["Frame19"].shield6,
                                                                      state='normal')
            App.global_controller.frames["Frame19"].canvas.itemconfig(App.global_controller.frames["Frame19"].shield7,
                                                                      state='normal')
            App.global_controller.frames["Frame19"].canvas.itemconfig(App.global_controller.frames["Frame19"].shield8,
                                                                      state='normal')
        elif App.LVL_access == 7:
            App.global_controller.frames["Frame2"].canvas.itemconfig(App.global_controller.frames["Frame2"].shield1,
                                                                     state='normal')
            App.global_controller.frames["Frame2"].canvas.itemconfig(App.global_controller.frames["Frame2"].shield2,
                                                                     state='normal')
            App.global_controller.frames["Frame2"].canvas.itemconfig(App.global_controller.frames["Frame2"].shield3,
                                                                     state='normal')
            App.global_controller.frames["Frame2"].canvas.itemconfig(App.global_controller.frames["Frame2"].shield4,
                                                                     state='normal')
            App.global_controller.frames["Frame2"].canvas.itemconfig(App.global_controller.frames["Frame2"].shield5,
                                                                     state='normal')
            App.global_controller.frames["Frame2"].canvas.itemconfig(App.global_controller.frames["Frame2"].shield6,
                                                                     state='normal')
        if App.numpad_instance != 0:
            if App.numpad_instance.winfo_exists():
                App.numpad_instance.destroy()
        App.session_access = False
        App.LVL_access = 10
        print("Доступ прекращен")





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
        self.after(500, self.update_clock) # Тик-так


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
        App.global_controller = controller
        button = tk.Button(self, text="Настройки", fg='white', bg='black', font=('Roboto Bold', 14), activebackground="black", activeforeground="white",
                           relief="groove", command=lambda: controller.show_frame("Frame2"))
        button.place(x=0, y=0, width=135, height=37)
        self.indicators_img = PhotoImage(file=r"new_images/indicator_0.png")
        self.indicators_button = self.canvas.create_image(195, 20, image=self.indicators_img)
        self.canvas.tag_bind(self.indicators_button, "<Button-1>", lambda event: controller.show_frame("Frame1_2"))
        self.background_img = PhotoImage(file=r"new_images/stop_icon.png")
        self.canvas.create_image(655, 20, image=self.background_img)
        self.clock_label = tk.Label(self.canvas, text="", fg='white', bg='black', font=('Roboto Bold', 12))
        self.clock_label.place(x=680, y=5)
        self.right_img = PhotoImage(file=r"new_images/red.png")
        self.right_button = self.canvas.create_image(770, 180, image=self.right_img)
        self.canvas.tag_bind(self.right_button, "<Button-1>", self.update_right)
        self.img_pump_on = PhotoImage(file=r"new_images/pump_on.png")
        self.img_pump_off = PhotoImage(file=r"new_images/pump_off.png")
        self.img_blue_rectangle = PhotoImage(file=r"new_images/blue_rectangle.png")
        self.output = tk.Label(self.canvas, text="Выход:",
                                fg='#449344', bg='black',
                                font=('Roboto Bold', 10))
        self.output_value = tk.Label(self.canvas, text="0.00",
                            fg='white', bg='black',
                            font=('Roboto Bold', 10))
        self.task = tk.Label(self.canvas, text="Задание:",
                            fg='#A70909', bg='black',
                            font=('Roboto Bold', 10))
        self.task_value = tk.Label(self.canvas, text="0.00",
                                  fg='white', bg='black',
                                  font=('Roboto Bold', 10))
        self.triangle = tk.Label(self.canvas, text="△:",
                             fg='white', bg='black',
                             font=('Roboto Bold', 10))
        self.triangle_value = tk.Label(self.canvas, text="0.00",
                                   fg='white', bg='black',
                                   font=('Roboto Bold', 10))
        self.rate = tk.Label(self.canvas, text="Частота:",
                              fg='white', bg='black',
                              font=('Roboto Bold', 10))
        self.rate_value = tk.Label(self.canvas, text="0.00",
                                    fg='white', bg='black',
                                    font=('Roboto Bold', 10))
        self.input = tk.Label(self.canvas, text="Вход:",
                                 fg='#0000FF', bg='black',
                                 font=('Roboto Bold', 10))
        self.input_value = tk.Label(self.canvas, text="0.00",
                                       fg='white', bg='black',
                                       font=('Roboto Bold', 10))
        self.label1 = tk.Label(self.canvas, text="Бар",
                             fg='white', bg='black',
                             font=('Roboto Bold', 10))
        self.label2 = tk.Label(self.canvas, text="Бар",
                               fg='white', bg='black',
                               font=('Roboto Bold', 10))
        self.label3 = tk.Label(self.canvas, text="Бар",
                               fg='white', bg='black',
                               font=('Roboto Bold', 10))
        self.label4 = tk.Label(self.canvas, text="Гц",
                               fg='white', bg='black',
                               font=('Roboto Bold', 10))
        self.label5 = tk.Label(self.canvas, text="Бар",
                               fg='white', bg='black',
                               font=('Roboto Bold', 10))

        self.red_line = self.canvas.create_line(0, 0, 0, 0, fill="red", width=2)
        self.x = 45
        self.y = 302

        #self.initialization_graphic()
        self.initialization_pumps()

    def initialization_graphic(self):
        if self.x == 730:
            self.x = 45
        else:
            self.x = self.x + 5
        self.canvas.coords(self.red_line, 50, self.y, self.x, self.y)
        self.canvas.update()
        #self.red_line = self.canvas.create_line(50, 302, self.x, 302, fill="red", width=2)
        #self.canvas.after(500, self.initialization_graphic())


    def initialization_pumps(self, Pumps_active=App.Pumps_active): #Показ насосов
        match (Pumps_active):
            case 1:
                self.Pump_six = self.canvas.create_image(620, 400, image=self.img_pump_off)
                self.Pump_five = self.canvas.create_image(520, 400, image=self.img_pump_off)
                self.Pump_four = self.canvas.create_image(420, 400, image=self.img_pump_off)
                self.Pump_three = self.canvas.create_image(320, 400, image=self.img_pump_off)
                self.Pump_two = self.canvas.create_image(220, 400, image=self.img_pump_off)
                self.Pump_one = self.canvas.create_image(120, 400, image=self.img_pump_on)
            case 2:
                self.Pump_six = self.canvas.create_image(620, 400, image=self.img_pump_off)
                self.Pump_five = self.canvas.create_image(520, 400, image=self.img_pump_off)
                self.Pump_four = self.canvas.create_image(420, 400, image=self.img_pump_off)
                self.Pump_three = self.canvas.create_image(320, 400, image=self.img_pump_off)
                self.Pump_two = self.canvas.create_image(220, 400, image=self.img_pump_on)
                self.Pump_one = self.canvas.create_image(120, 400, image=self.img_pump_on)
            case 3:
                self.Pump_six = self.canvas.create_image(620, 400, image=self.img_pump_off)
                self.Pump_five = self.canvas.create_image(520, 400, image=self.img_pump_off)
                self.Pump_four = self.canvas.create_image(420, 400, image=self.img_pump_off)
                self.Pump_three = self.canvas.create_image(320, 400, image=self.img_pump_on)
                self.Pump_two = self.canvas.create_image(220, 400, image=self.img_pump_on)
                self.Pump_one = self.canvas.create_image(120, 400, image=self.img_pump_on)
            case 4:
                self.Pump_six = self.canvas.create_image(620, 400, image=self.img_pump_off)
                self.Pump_five = self.canvas.create_image(520, 400, image=self.img_pump_off)
                self.Pump_four = self.canvas.create_image(420, 400, image=self.img_pump_on)
                self.Pump_three = self.canvas.create_image(320, 400, image=self.img_pump_on)
                self.Pump_two = self.canvas.create_image(220, 400, image=self.img_pump_on)
                self.Pump_one = self.canvas.create_image(120, 400, image=self.img_pump_on)
            case 5:
                self.Pump_six = self.canvas.create_image(620, 400, image=self.img_pump_off)
                self.Pump_five = self.canvas.create_image(520, 400, image=self.img_pump_on)
                self.Pump_four = self.canvas.create_image(420, 400, image=self.img_pump_on)
                self.Pump_three = self.canvas.create_image(320, 400, image=self.img_pump_on)
                self.Pump_two = self.canvas.create_image(220, 400, image=self.img_pump_on)
                self.Pump_one = self.canvas.create_image(120, 400, image=self.img_pump_on)
            case 6:
                self.Pump_six = self.canvas.create_image(620, 400, image=self.img_pump_on)
                self.Pump_five = self.canvas.create_image(520, 400, image=self.img_pump_on)
                self.Pump_four = self.canvas.create_image(420, 400, image=self.img_pump_on)
                self.Pump_three = self.canvas.create_image(320, 400, image=self.img_pump_on)
                self.Pump_two = self.canvas.create_image(220, 400, image=self.img_pump_on)
                self.Pump_one = self.canvas.create_image(120, 400, image=self.img_pump_on)

        self.canvas.create_image(87, 342.435, image=self.img_blue_rectangle)
        self.canvas.create_image(87, 456.435, image=self.img_blue_rectangle)

        self.output.place(x=10, y=330)
        self.output_value.place(x=78, y=330)
        self.task.place(x=10, y=360)
        self.task_value.place(x=78, y=360)
        self.triangle.place(x=10, y=390)
        self.triangle_value.place(x=78, y=390)
        self.rate.place(x=10, y=420)
        self.rate_value.place(x=78, y=420)
        self.input.place(x=10, y=445)
        self.input_value.place(x=78, y=445)
        self.label1.place(x=130, y=330)
        self.label2.place(x=130, y=360)
        self.label3.place(x=130, y=390)
        self.label4.place(x=130, y=420)
        self.label5.place(x=130, y=445)

    def update_right(self, event):
        if self.right_img.cget("file") == r"new_images/red.png":
            self.right_img = PhotoImage(file=r"new_images/blue.png")
        elif self.right_img.cget("file") == r"new_images/blue.png":
            self.right_img = PhotoImage(file=r"new_images/green.png")
        elif self.right_img.cget("file") == r"new_images/green.png":
            self.right_img = PhotoImage(file=r"new_images/pink.png")
        elif self.right_img.cget("file") == r"new_images/pink.png":
            self.right_img = PhotoImage(file=r"new_images/orange.png")
        elif self.right_img.cget("file") == r"new_images/orange.png":
            self.right_img = PhotoImage(file=r"new_images/yellow.png")
        elif self.right_img.cget("file") == r"new_images/yellow.png":
            self.right_img = PhotoImage(file=r"new_images/red.png")
        self.right_button = self.canvas.create_image(770, 180, image=self.right_img)
        self.canvas.tag_bind(self.right_button, "<Button-1>", self.update_right)
    def update_clock(self, current_time):
        self.clock_label.config(text=current_time)
        self.initialization_graphic()

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
        self.indicators_img = PhotoImage(file=r"new_images/indicator_1.png")
        self.indicators_button = self.canvas.create_image(195, 20, image=self.indicators_img)
        self.canvas.tag_bind(self.indicators_button, "<Button-1>", lambda event: controller.show_frame("Frame1_3"))
        self.background_img = PhotoImage(file=r"new_images/stop_icon.png")
        background = self.canvas.create_image(655, 20, image=self.background_img)
        self.clock_label = tk.Label(self.canvas, text="", fg='white', bg='black', font=('Roboto Bold', 12))
        self.clock_label.place(x=680, y=5)
        self.img_pump_on = PhotoImage(file=r"new_images/pump_on.png")
        self.img_pump_off = PhotoImage(file=r"new_images/pump_off.png")
        self.img_blue_rectangle = PhotoImage(file=r"new_images/blue_rectangle.png")
        self.output = tk.Label(self.canvas, text="Выход:",
                               fg='#449344', bg='black',
                               font=('Roboto Bold', 10))
        self.output_value = tk.Label(self.canvas, text="0.00",
                                     fg='white', bg='black',
                                     font=('Roboto Bold', 10))
        self.task = tk.Label(self.canvas, text="Задание:",
                             fg='#A70909', bg='black',
                             font=('Roboto Bold', 10))
        self.task_value = tk.Label(self.canvas, text="0.00",
                                   fg='white', bg='black',
                                   font=('Roboto Bold', 10))
        self.triangle = tk.Label(self.canvas, text="△:",
                                 fg='white', bg='black',
                                 font=('Roboto Bold', 10))
        self.triangle_value = tk.Label(self.canvas, text="0.00",
                                       fg='white', bg='black',
                                       font=('Roboto Bold', 10))
        self.rate = tk.Label(self.canvas, text="Частота:",
                             fg='white', bg='black',
                             font=('Roboto Bold', 10))
        self.rate_value = tk.Label(self.canvas, text="0.00",
                                   fg='white', bg='black',
                                   font=('Roboto Bold', 10))
        self.input = tk.Label(self.canvas, text="Вход:",
                              fg='#0000FF', bg='black',
                              font=('Roboto Bold', 10))
        self.input_value = tk.Label(self.canvas, text="0.00",
                                    fg='white', bg='black',
                                    font=('Roboto Bold', 10))
        self.label1 = tk.Label(self.canvas, text="Бар",
                               fg='white', bg='black',
                               font=('Roboto Bold', 10))
        self.label2 = tk.Label(self.canvas, text="Бар",
                               fg='white', bg='black',
                               font=('Roboto Bold', 10))
        self.label3 = tk.Label(self.canvas, text="Бар",
                               fg='white', bg='black',
                               font=('Roboto Bold', 10))
        self.label4 = tk.Label(self.canvas, text="Гц",
                               fg='white', bg='black',
                               font=('Roboto Bold', 10))
        self.label5 = tk.Label(self.canvas, text="Бар",
                               fg='white', bg='black',
                               font=('Roboto Bold', 10))

        self.initialization_pumps()
    def initialization_pumps(self, Pumps_active=App.Pumps_active):
        match (Pumps_active):
            case 1:
                self.Pump_six = self.canvas.create_image(620, 400, image=self.img_pump_off)
                self.Pump_five = self.canvas.create_image(520, 400, image=self.img_pump_off)
                self.Pump_four = self.canvas.create_image(420, 400, image=self.img_pump_off)
                self.Pump_three = self.canvas.create_image(320, 400, image=self.img_pump_off)
                self.Pump_two = self.canvas.create_image(220, 400, image=self.img_pump_off)
                self.Pump_one = self.canvas.create_image(120, 400, image=self.img_pump_on)
            case 2:
                self.Pump_six = self.canvas.create_image(620, 400, image=self.img_pump_off)
                self.Pump_five = self.canvas.create_image(520, 400, image=self.img_pump_off)
                self.Pump_four = self.canvas.create_image(420, 400, image=self.img_pump_off)
                self.Pump_three = self.canvas.create_image(320, 400, image=self.img_pump_off)
                self.Pump_two = self.canvas.create_image(220, 400, image=self.img_pump_on)
                self.Pump_one = self.canvas.create_image(120, 400, image=self.img_pump_on)
            case 3:
                self.Pump_six = self.canvas.create_image(620, 400, image=self.img_pump_off)
                self.Pump_five = self.canvas.create_image(520, 400, image=self.img_pump_off)
                self.Pump_four = self.canvas.create_image(420, 400, image=self.img_pump_off)
                self.Pump_three = self.canvas.create_image(320, 400, image=self.img_pump_on)
                self.Pump_two = self.canvas.create_image(220, 400, image=self.img_pump_on)
                self.Pump_one = self.canvas.create_image(120, 400, image=self.img_pump_on)
            case 4:
                self.Pump_six = self.canvas.create_image(620, 400, image=self.img_pump_off)
                self.Pump_five = self.canvas.create_image(520, 400, image=self.img_pump_off)
                self.Pump_four = self.canvas.create_image(420, 400, image=self.img_pump_on)
                self.Pump_three = self.canvas.create_image(320, 400, image=self.img_pump_on)
                self.Pump_two = self.canvas.create_image(220, 400, image=self.img_pump_on)
                self.Pump_one = self.canvas.create_image(120, 400, image=self.img_pump_on)
            case 5:
                self.Pump_six = self.canvas.create_image(620, 400, image=self.img_pump_off)
                self.Pump_five = self.canvas.create_image(520, 400, image=self.img_pump_on)
                self.Pump_four = self.canvas.create_image(420, 400, image=self.img_pump_on)
                self.Pump_three = self.canvas.create_image(320, 400, image=self.img_pump_on)
                self.Pump_two = self.canvas.create_image(220, 400, image=self.img_pump_on)
                self.Pump_one = self.canvas.create_image(120, 400, image=self.img_pump_on)
            case 6:
                self.Pump_six = self.canvas.create_image(620, 400, image=self.img_pump_on)
                self.Pump_five = self.canvas.create_image(520, 400, image=self.img_pump_on)
                self.Pump_four = self.canvas.create_image(420, 400, image=self.img_pump_on)
                self.Pump_three = self.canvas.create_image(320, 400, image=self.img_pump_on)
                self.Pump_two = self.canvas.create_image(220, 400, image=self.img_pump_on)
                self.Pump_one = self.canvas.create_image(120, 400, image=self.img_pump_on)

        self.canvas.create_image(87, 342.435, image=self.img_blue_rectangle)
        self.canvas.create_image(87, 456.435, image=self.img_blue_rectangle)

        self.output.place(x=10, y=330)
        self.output_value.place(x=78, y=330)
        self.task.place(x=10, y=360)
        self.task_value.place(x=78, y=360)
        self.triangle.place(x=10, y=390)
        self.triangle_value.place(x=78, y=390)
        self.rate.place(x=10, y=420)
        self.rate_value.place(x=78, y=420)
        self.input.place(x=10, y=445)
        self.input_value.place(x=78, y=445)
        self.label1.place(x=130, y=330)
        self.label2.place(x=130, y=360)
        self.label3.place(x=130, y=390)
        self.label4.place(x=130, y=420)
        self.label5.place(x=130, y=445)

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
        self.indicators_img = PhotoImage(file=r"new_images/indicator_1.png")
        self.indicators_button = self.canvas.create_image(195, 20, image=self.indicators_img)
        self.canvas.tag_bind(self.indicators_button, "<Button-1>", lambda event: controller.show_frame("Frame1_4"))
        self.background_img = PhotoImage(file=r"new_images/stop_icon.png")
        self.canvas.create_image(655, 20, image=self.background_img)
        self.clock_label = tk.Label(self.canvas, text="", fg='white', bg='black', font=('Roboto Bold', 12))
        self.clock_label.place(x=680, y=5)
        self.img_pump_on = PhotoImage(file=r"new_images/pump_on.png")
        self.img_pump_off = PhotoImage(file=r"new_images/pump_off.png")
        self.img_blue_rectangle = PhotoImage(file=r"new_images/blue_rectangle.png")
        self.output = tk.Label(self.canvas, text="Выход:",
                               fg='#449344', bg='black',
                               font=('Roboto Bold', 10))
        self.output_value = tk.Label(self.canvas, text="0.00",
                                     fg='white', bg='black',
                                     font=('Roboto Bold', 10))
        self.task = tk.Label(self.canvas, text="Задание:",
                             fg='#A70909', bg='black',
                             font=('Roboto Bold', 10))
        self.task_value = tk.Label(self.canvas, text="0.00",
                                   fg='white', bg='black',
                                   font=('Roboto Bold', 10))
        self.triangle = tk.Label(self.canvas, text="△:",
                                 fg='white', bg='black',
                                 font=('Roboto Bold', 10))
        self.triangle_value = tk.Label(self.canvas, text="0.00",
                                       fg='white', bg='black',
                                       font=('Roboto Bold', 10))
        self.rate = tk.Label(self.canvas, text="Частота:",
                             fg='white', bg='black',
                             font=('Roboto Bold', 10))
        self.rate_value = tk.Label(self.canvas, text="0.00",
                                   fg='white', bg='black',
                                   font=('Roboto Bold', 10))
        self.input = tk.Label(self.canvas, text="Вход:",
                              fg='#0000FF', bg='black',
                              font=('Roboto Bold', 10))
        self.input_value = tk.Label(self.canvas, text="0.00",
                                    fg='white', bg='black',
                                    font=('Roboto Bold', 10))
        self.label1 = tk.Label(self.canvas, text="Бар",
                               fg='white', bg='black',
                               font=('Roboto Bold', 10))
        self.label2 = tk.Label(self.canvas, text="Бар",
                               fg='white', bg='black',
                               font=('Roboto Bold', 10))
        self.label3 = tk.Label(self.canvas, text="Бар",
                               fg='white', bg='black',
                               font=('Roboto Bold', 10))
        self.label4 = tk.Label(self.canvas, text="Гц",
                               fg='white', bg='black',
                               font=('Roboto Bold', 10))
        self.label5 = tk.Label(self.canvas, text="Бар",
                               fg='white', bg='black',
                               font=('Roboto Bold', 10))

        self.button1_img = PhotoImage(file=r"new_images/ON.png")
        self.button1_button = self.canvas.create_image(235, 200, image=self.button1_img)
        self.canvas.tag_bind(self.button1_button, "<Button-1>", self.update_button1)
        self.button2_img = PhotoImage(file=r"new_images/ON.png")
        self.button2_button = self.canvas.create_image(330, 200, image=self.button2_img)
        self.canvas.tag_bind(self.button2_button, "<Button-1>", self.update_button2)
        self.button3_img = PhotoImage(file=r"new_images/ON.png")
        self.button3_button = self.canvas.create_image(425, 200, image=self.button3_img)
        self.canvas.tag_bind(self.button3_button, "<Button-1>", self.update_button3)
        self.button4_img = PhotoImage(file=r"new_images/ON.png")
        self.button4_button = self.canvas.create_image(520, 200, image=self.button4_img)
        self.canvas.tag_bind(self.button4_button, "<Button-1>", self.update_button4)
        self.button5_img = PhotoImage(file=r"new_images/ON.png")
        self.button5_button = self.canvas.create_image(615, 200, image=self.button5_img)
        self.canvas.tag_bind(self.button5_button, "<Button-1>", self.update_button5)
        self.button6_img = PhotoImage(file=r"new_images/ON.png")
        self.button6_button = self.canvas.create_image(710, 200, image=self.button6_img)
        self.canvas.tag_bind(self.button6_button, "<Button-1>", self.update_button6)

        self.initialization_pumps()

    def update_button1(self, event):
        if self.button1_img.cget("file") == r"new_images/OFF.png":
            self.button1_img = PhotoImage(file=r"new_images/ON.png")
        elif self.button1_img.cget("file") == r"new_images/ON.png":
            self.button1_img = PhotoImage(file=r"new_images/OFF.png")
        self.button1_button = self.canvas.create_image(235, 200, image=self.button1_img)
        self.canvas.tag_bind(self.button1_button, "<Button-1>", self.update_button1)

    def update_button2(self, event):
        if self.button2_img.cget("file") == r"new_images/OFF.png":
            self.button2_img = PhotoImage(file=r"new_images/ON.png")
        elif self.button2_img.cget("file") == r"new_images/ON.png":
            self.button2_img = PhotoImage(file=r"new_images/OFF.png")
        self.button2_button = self.canvas.create_image(330, 200, image=self.button2_img)
        self.canvas.tag_bind(self.button2_button, "<Button-1>", self.update_button2)

    def update_button3(self, event):
        if self.button3_img.cget("file") == r"new_images/OFF.png":
            self.button3_img = PhotoImage(file=r"inew_images/ON.png")
        elif self.button3_img.cget("file") == r"new_images/ON.png":
            self.button3_img = PhotoImage(file=r"new_images/OFF.png")
        self.button3_button = self.canvas.create_image(425, 200, image=self.button3_img)
        self.canvas.tag_bind(self.button3_button, "<Button-1>", self.update_button3)
    def update_button4(self, event):
        if self.button4_img.cget("file") == r"new_images/OFF.png":
            self.button4_img = PhotoImage(file=r"new_images/ON.png")
        elif self.button4_img.cget("file") == r"new_images/ON.png":
            self.button4_img = PhotoImage(file=r"new_images/OFF.png")
        self.button4_button = self.canvas.create_image(520, 200, image=self.button4_img)
        self.canvas.tag_bind(self.button4_button, "<Button-1>", self.update_button4)

    def update_button5(self, event):
        if self.button5_img.cget("file") == r"new_images/OFF.png":
            self.button5_img = PhotoImage(file=r"new_images/ON.png")
        elif self.button5_img.cget("file") == r"new_images/ON.png":
            self.button5_img = PhotoImage(file=r"new_images/OFF.png")
        self.button5_button = self.canvas.create_image(615, 200, image=self.button5_img)
        self.canvas.tag_bind(self.button5_button, "<Button-1>", self.update_button5)

    def update_button6(self, event):
        if self.button6_img.cget("file") == r"new_images/OFF.png":
            self.button6_img = PhotoImage(file=r"new_images/ON.png")
        elif self.button6_img.cget("file") == r"new_images/ON.png":
            self.button6_img = PhotoImage(file=r"new_images/OFF.png")
        self.button6_button = self.canvas.create_image(710, 200, image=self.button6_img)
        self.canvas.tag_bind(self.button6_button, "<Button-1>", self.update_button6)

    def initialization_pumps(self, Pumps_active=App.Pumps_active):
        match (Pumps_active):
            case 1:
                self.Pump_six = self.canvas.create_image(620, 400, image=self.img_pump_off)
                self.Pump_five = self.canvas.create_image(520, 400, image=self.img_pump_off)
                self.Pump_four = self.canvas.create_image(420, 400, image=self.img_pump_off)
                self.Pump_three = self.canvas.create_image(320, 400, image=self.img_pump_off)
                self.Pump_two = self.canvas.create_image(220, 400, image=self.img_pump_off)
                self.Pump_one = self.canvas.create_image(120, 400, image=self.img_pump_on)
            case 2:
                self.Pump_six = self.canvas.create_image(620, 400, image=self.img_pump_off)
                self.Pump_five = self.canvas.create_image(520, 400, image=self.img_pump_off)
                self.Pump_four = self.canvas.create_image(420, 400, image=self.img_pump_off)
                self.Pump_three = self.canvas.create_image(320, 400, image=self.img_pump_off)
                self.Pump_two = self.canvas.create_image(220, 400, image=self.img_pump_on)
                self.Pump_one = self.canvas.create_image(120, 400, image=self.img_pump_on)
            case 3:
                self.Pump_six = self.canvas.create_image(620, 400, image=self.img_pump_off)
                self.Pump_five = self.canvas.create_image(520, 400, image=self.img_pump_off)
                self.Pump_four = self.canvas.create_image(420, 400, image=self.img_pump_off)
                self.Pump_three = self.canvas.create_image(320, 400, image=self.img_pump_on)
                self.Pump_two = self.canvas.create_image(220, 400, image=self.img_pump_on)
                self.Pump_one = self.canvas.create_image(120, 400, image=self.img_pump_on)
            case 4:
                self.Pump_six = self.canvas.create_image(620, 400, image=self.img_pump_off)
                self.Pump_five = self.canvas.create_image(520, 400, image=self.img_pump_off)
                self.Pump_four = self.canvas.create_image(420, 400, image=self.img_pump_on)
                self.Pump_three = self.canvas.create_image(320, 400, image=self.img_pump_on)
                self.Pump_two = self.canvas.create_image(220, 400, image=self.img_pump_on)
                self.Pump_one = self.canvas.create_image(120, 400, image=self.img_pump_on)
            case 5:
                self.Pump_six = self.canvas.create_image(620, 400, image=self.img_pump_off)
                self.Pump_five = self.canvas.create_image(520, 400, image=self.img_pump_on)
                self.Pump_four = self.canvas.create_image(420, 400, image=self.img_pump_on)
                self.Pump_three = self.canvas.create_image(320, 400, image=self.img_pump_on)
                self.Pump_two = self.canvas.create_image(220, 400, image=self.img_pump_on)
                self.Pump_one = self.canvas.create_image(120, 400, image=self.img_pump_on)
            case 6:
                self.Pump_six = self.canvas.create_image(620, 400, image=self.img_pump_on)
                self.Pump_five = self.canvas.create_image(520, 400, image=self.img_pump_on)
                self.Pump_four = self.canvas.create_image(420, 400, image=self.img_pump_on)
                self.Pump_three = self.canvas.create_image(320, 400, image=self.img_pump_on)
                self.Pump_two = self.canvas.create_image(220, 400, image=self.img_pump_on)
                self.Pump_one = self.canvas.create_image(120, 400, image=self.img_pump_on)

        self.canvas.create_image(87, 342.435, image=self.img_blue_rectangle)
        self.canvas.create_image(87, 456.435, image=self.img_blue_rectangle)

        self.output.place(x=10, y=330)
        self.output_value.place(x=78, y=330)
        self.task.place(x=10, y=360)
        self.task_value.place(x=78, y=360)
        self.triangle.place(x=10, y=390)
        self.triangle_value.place(x=78, y=390)
        self.rate.place(x=10, y=420)
        self.rate_value.place(x=78, y=420)
        self.input.place(x=10, y=445)
        self.input_value.place(x=78, y=445)
        self.label1.place(x=130, y=330)
        self.label2.place(x=130, y=360)
        self.label3.place(x=130, y=390)
        self.label4.place(x=130, y=420)
        self.label5.place(x=130, y=445)


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
        self.indicators_img = PhotoImage(file=r"new_images/indicator_2.png")
        self.indicators_button = self.canvas.create_image(195, 20, image=self.indicators_img)
        self.canvas.tag_bind(self.indicators_button, "<Button-1>", lambda event: controller.show_frame("Frame1_1"))
        self.background_img = PhotoImage(file=r"new_images/stop_icon.png")
        background = self.canvas.create_image(655, 20, image=self.background_img)
        self.clock_label = tk.Label(self.canvas, text="", fg='white', bg='black', font=('Roboto Bold', 12))
        self.clock_label.place(x=680, y=5)
        self.img_pump_on = PhotoImage(file=r"new_images/pump_on.png")
        self.img_pump_off = PhotoImage(file=r"new_images/pump_off.png")
        self.img_blue_rectangle = PhotoImage(file=r"new_images/blue_rectangle.png")
        self.output = tk.Label(self.canvas, text="Выход:",
                               fg='#449344', bg='black',
                               font=('Roboto Bold', 10))
        self.output_value = tk.Label(self.canvas, text="0.00",
                                     fg='white', bg='black',
                                     font=('Roboto Bold', 10))
        self.task = tk.Label(self.canvas, text="Задание:",
                             fg='#A70909', bg='black',
                             font=('Roboto Bold', 10))
        self.task_value = tk.Label(self.canvas, text="0.00",
                                   fg='white', bg='black',
                                   font=('Roboto Bold', 10))
        self.triangle = tk.Label(self.canvas, text="△:",
                                 fg='white', bg='black',
                                 font=('Roboto Bold', 10))
        self.triangle_value = tk.Label(self.canvas, text="0.00",
                                       fg='white', bg='black',
                                       font=('Roboto Bold', 10))
        self.rate = tk.Label(self.canvas, text="Частота:",
                             fg='white', bg='black',
                             font=('Roboto Bold', 10))
        self.rate_value = tk.Label(self.canvas, text="0.00",
                                   fg='white', bg='black',
                                   font=('Roboto Bold', 10))
        self.input = tk.Label(self.canvas, text="Вход:",
                              fg='#0000FF', bg='black',
                              font=('Roboto Bold', 10))
        self.input_value = tk.Label(self.canvas, text="0.00",
                                    fg='white', bg='black',
                                    font=('Roboto Bold', 10))
        self.label1 = tk.Label(self.canvas, text="Бар",
                               fg='white', bg='black',
                               font=('Roboto Bold', 10))
        self.label2 = tk.Label(self.canvas, text="Бар",
                               fg='white', bg='black',
                               font=('Roboto Bold', 10))
        self.label3 = tk.Label(self.canvas, text="Бар",
                               fg='white', bg='black',
                               font=('Roboto Bold', 10))
        self.label4 = tk.Label(self.canvas, text="Гц",
                               fg='white', bg='black',
                               font=('Roboto Bold', 10))
        self.label5 = tk.Label(self.canvas, text="Бар",
                               fg='white', bg='black',
                               font=('Roboto Bold', 10))
        self.initialization_pumps()

    def initialization_pumps(self, Pumps_active=App.Pumps_active):
        match (Pumps_active):
            case 1:
                self.Pump_six = self.canvas.create_image(620, 400, image=self.img_pump_off)
                self.Pump_five = self.canvas.create_image(520, 400, image=self.img_pump_off)
                self.Pump_four = self.canvas.create_image(420, 400, image=self.img_pump_off)
                self.Pump_three = self.canvas.create_image(320, 400, image=self.img_pump_off)
                self.Pump_two = self.canvas.create_image(220, 400, image=self.img_pump_off)
                self.Pump_one = self.canvas.create_image(120, 400, image=self.img_pump_on)
            case 2:
                self.Pump_six = self.canvas.create_image(620, 400, image=self.img_pump_off)
                self.Pump_five = self.canvas.create_image(520, 400, image=self.img_pump_off)
                self.Pump_four = self.canvas.create_image(420, 400, image=self.img_pump_off)
                self.Pump_three = self.canvas.create_image(320, 400, image=self.img_pump_off)
                self.Pump_two = self.canvas.create_image(220, 400, image=self.img_pump_on)
                self.Pump_one = self.canvas.create_image(120, 400, image=self.img_pump_on)
            case 3:
                self.Pump_six = self.canvas.create_image(620, 400, image=self.img_pump_off)
                self.Pump_five = self.canvas.create_image(520, 400, image=self.img_pump_off)
                self.Pump_four = self.canvas.create_image(420, 400, image=self.img_pump_off)
                self.Pump_three = self.canvas.create_image(320, 400, image=self.img_pump_on)
                self.Pump_two = self.canvas.create_image(220, 400, image=self.img_pump_on)
                self.Pump_one = self.canvas.create_image(120, 400, image=self.img_pump_on)
            case 4:
                self.Pump_six = self.canvas.create_image(620, 400, image=self.img_pump_off)
                self.Pump_five = self.canvas.create_image(520, 400, image=self.img_pump_off)
                self.Pump_four = self.canvas.create_image(420, 400, image=self.img_pump_on)
                self.Pump_three = self.canvas.create_image(320, 400, image=self.img_pump_on)
                self.Pump_two = self.canvas.create_image(220, 400, image=self.img_pump_on)
                self.Pump_one = self.canvas.create_image(120, 400, image=self.img_pump_on)
            case 5:
                self.Pump_six = self.canvas.create_image(620, 400, image=self.img_pump_off)
                self.Pump_five = self.canvas.create_image(520, 400, image=self.img_pump_on)
                self.Pump_four = self.canvas.create_image(420, 400, image=self.img_pump_on)
                self.Pump_three = self.canvas.create_image(320, 400, image=self.img_pump_on)
                self.Pump_two = self.canvas.create_image(220, 400, image=self.img_pump_on)
                self.Pump_one = self.canvas.create_image(120, 400, image=self.img_pump_on)
            case 6:
                self.Pump_six = self.canvas.create_image(620, 400, image=self.img_pump_on)
                self.Pump_five = self.canvas.create_image(520, 400, image=self.img_pump_on)
                self.Pump_four = self.canvas.create_image(420, 400, image=self.img_pump_on)
                self.Pump_three = self.canvas.create_image(320, 400, image=self.img_pump_on)
                self.Pump_two = self.canvas.create_image(220, 400, image=self.img_pump_on)
                self.Pump_one = self.canvas.create_image(120, 400, image=self.img_pump_on)

        self.canvas.create_image(87, 342.435, image=self.img_blue_rectangle)
        self.canvas.create_image(87, 456.435, image=self.img_blue_rectangle)

        self.output.place(x=10, y=330)
        self.output_value.place(x=78, y=330)
        self.task.place(x=10, y=360)
        self.task_value.place(x=78, y=360)
        self.triangle.place(x=10, y=390)
        self.triangle_value.place(x=78, y=390)
        self.rate.place(x=10, y=420)
        self.rate_value.place(x=78, y=420)
        self.input.place(x=10, y=445)
        self.input_value.place(x=78, y=445)
        self.label1.place(x=130, y=330)
        self.label2.place(x=130, y=360)
        self.label3.place(x=130, y=390)
        self.label4.place(x=130, y=420)
        self.label5.place(x=130, y=445)

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

        self.img_share = PhotoImage(file=r"new_images/share.png")
        self.img_user = PhotoImage(file=r"new_images/user.png")
        self.img_cal = PhotoImage(file=r"new_images/calendar.png")
        self.img_day = PhotoImage(file=r"new_images/day.png")
        self.img_eye = PhotoImage(file=r"new_images/eye.png")
        self.img_shield = PhotoImage(file=r"new_images/shield.png")
        self.img_field_l = PhotoImage(file=r"new_images/field_long.png")
        self.img_field_s = PhotoImage(file=r"new_images/field_short.png")

        self.canvas.create_image(231, 30, image=self.img_share)
        self.canvas.create_image(231, 78, image=self.img_user)
        self.canvas.create_image(231, 226, image=self.img_day)
        self.canvas.create_image(231, 271, image=self.img_day)
        self.canvas.create_image(231, 316, image=self.img_day)
        self.canvas.create_image(231, 361, image=self.img_day)

        self.shield1 = self.canvas.create_image(594, 77, image=self.img_shield)
        self.shield2 = self.canvas.create_image(491, 122, image=self.img_shield)
        self.shield3 = self.canvas.create_image(354, 227, image=self.img_shield)
        self.shield4 = self.canvas.create_image(354, 273, image=self.img_shield)
        self.shield5 = self.canvas.create_image(354, 318, image=self.img_shield)
        self.shield6 = self.canvas.create_image(354, 363, image=self.img_shield)

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
        self.label28 = tk.Label(self.canvas, text="Бар", fg='white', bg='black',
                                font=('Roboto Bold', 12))
        self.label28.place(x=750, y=66, width=28, height=19)
        self.setpoint_value = tk.Label(self.canvas, text=App.storage_data["User_Setpoint"], fg='white', bg='black',
                                font=('Roboto Bold', 12))
        self.setpoint_value.place(x=644, y=64)

        self.weekdays_morning_h = tk.Label(self.canvas, text=App.storage_data["Setpoint_Planner_Morning_Weekday_Hour"], fg='white', bg='black',
                                font=('Roboto Bold', 12))
        self.weekdays_morning_h.place(x=388, y=216, width=19, height=19)
        self.weekdays_afternoon_h = tk.Label(self.canvas, text=App.storage_data["Setpoint_Planner_Day_Weekday_Hour"], fg='white', bg='black',
                                           font=('Roboto Bold', 12))
        self.weekdays_afternoon_h.place(x=388, y=265, width=19, height=19)
        self.weekdays_evening_h = tk.Label(self.canvas, text=App.storage_data["Setpoint_Planner_Evening_Weekday_Hour"], fg='white', bg='black',
                                             font=('Roboto Bold', 12))
        self.weekdays_evening_h.place(x=388, y=307, width=19, height=19)
        self.weekdays_night_h = tk.Label(self.canvas, text=App.storage_data["Setpoint_Planner_Night_Weekday_Hour"], fg='white', bg='black',
                                             font=('Roboto Bold', 12))
        self.weekdays_night_h.place(x=388, y=350, width=19, height=19)

        self.weekdays_morning_m = tk.Label(self.canvas, text=App.storage_data["Setpoint_Planner_Morning_Weekday_Minute"], fg='white', bg='black',
                                           font=('Roboto Bold', 12))
        self.weekdays_morning_m.place(x=440, y=216, width=19, height=19)
        self.weekdays_afternoon_m = tk.Label(self.canvas, text=App.storage_data["Setpoint_Planner_Day_Weekday_Minute"], fg='white', bg='black',
                                             font=('Roboto Bold', 12))
        self.weekdays_afternoon_m.place(x=440, y=265, width=19, height=19)
        self.weekdays_evening_m = tk.Label(self.canvas, text=App.storage_data["Setpoint_Planner_Evening_Weekday_Minute"], fg='white', bg='black',
                                           font=('Roboto Bold', 12))
        self.weekdays_evening_m.place(x=440, y=307, width=19, height=19)
        self.weekdays_night_m = tk.Label(self.canvas, text=App.storage_data["Setpoint_Planner_Night_Weekday_Minute"], fg='white', bg='black',
                                         font=('Roboto Bold', 12))
        self.weekdays_night_m.place(x=440, y=350, width=19, height=19)

        self.weekends_morning_h = tk.Label(self.canvas, text=App.storage_data["Setpoint_Planner_Morning_Weekend_Hour"], fg='white', bg='black',
                                           font=('Roboto Bold', 12))
        self.weekends_morning_h.place(x=492, y=216, width=19, height=19)
        self.weekends_afternoon_h = tk.Label(self.canvas, text=App.storage_data["Setpoint_Planner_Day_Weekend_Hour"], fg='white', bg='black',
                                             font=('Roboto Bold', 12))
        self.weekends_afternoon_h.place(x=492, y=265, width=19, height=19)
        self.weekends_evening_h = tk.Label(self.canvas, text=App.storage_data["Setpoint_Planner_Morning_Weekend_Hour"], fg='white', bg='black',
                                           font=('Roboto Bold', 12))
        self.weekends_evening_h.place(x=492, y=307, width=19, height=19)
        self.weekends_night_h = tk.Label(self.canvas, text=App.storage_data["Setpoint_Planner_Night_Weekend_Hour"], fg='white', bg='black',
                                         font=('Roboto Bold', 12))
        self.weekends_night_h.place(x=492, y=350, width=19, height=19)

        self.weekends_morning_m = tk.Label(self.canvas, text=App.storage_data["Setpoint_Planner_Morning_Weekend_Minute"], fg='white', bg='black',
                                           font=('Roboto Bold', 12))
        self.weekends_morning_m.place(x=544, y=216, width=19, height=19)
        self.weekends_afternoon_m = tk.Label(self.canvas, text=App.storage_data["Setpoint_Planner_Day_Weekend_Minute"], fg='white', bg='black',
                                             font=('Roboto Bold', 12))
        self.weekends_afternoon_m.place(x=544, y=265, width=19, height=19)
        self.weekends_evening_m = tk.Label(self.canvas, text=App.storage_data["Setpoint_Planner_Evening_Weekend_Minute"], fg='white', bg='black',
                                           font=('Roboto Bold', 12))
        self.weekends_evening_m.place(x=544, y=307, width=19, height=19)
        self.weekends_night_m = tk.Label(self.canvas, text=App.storage_data["Setpoint_Planner_Night_Weekend_Minute"], fg='white', bg='black',
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

        self.weekdays_morning_value = tk.Label(self.canvas, text=App.storage_data["Setpoint_Planner_Morning_Weekday_Setpoint"], fg='white', bg='black',
                                       font=('Roboto Bold', 12))
        self.weekdays_morning_value.place(x=599, y=214)
        self.label29 = tk.Label(self.canvas, text="Бар", fg='white', bg='black',
                                font=('Roboto Bold', 12))
        self.label29.place(x=653, y=215, width=28, height=19)
        self.weekdays_afternoon_value = tk.Label(self.canvas, text=App.storage_data["Setpoint_Planner_Day_Weekday_Setpoint"], fg='white', bg='black',
                                               font=('Roboto Bold', 12))
        self.weekdays_afternoon_value.place(x=599, y=262)
        self.label30 = tk.Label(self.canvas, text="Бар", fg='white', bg='black',
                                font=('Roboto Bold', 12))
        self.label30.place(x=653, y=264, width=28, height=19)
        self.weekdays_evening_value = tk.Label(self.canvas, text=App.storage_data["Setpoint_Planner_Evening_Weekday_Setpoint"], fg='white', bg='black',
                                               font=('Roboto Bold', 12))
        self.weekdays_evening_value.place(x=599, y=304)
        self.label31 = tk.Label(self.canvas, text="Бар", fg='white', bg='black',
                                font=('Roboto Bold', 12))
        self.label31.place(x=653, y=306, width=28, height=19)
        self.weekdays_night_value = tk.Label(self.canvas, text=App.storage_data["Setpoint_Planner_Night_Weekday_Setpoint"], fg='white', bg='black',
                                               font=('Roboto Bold', 12))
        self.weekdays_night_value.place(x=599, y=348)
        self.label32 = tk.Label(self.canvas, text="Бар", fg='white', bg='black',
                                font=('Roboto Bold', 12))
        self.label32.place(x=653, y=351, width=28, height=19)


        self.weekends_morning_value = tk.Label(self.canvas, text=App.storage_data["Setpoint_Planner_Morning_Weekend_Setpoint"], fg='white', bg='black',
                                               font=('Roboto Bold', 12))
        self.weekends_morning_value.place(x=704, y=214)
        self.label33 = tk.Label(self.canvas, text="Бар", fg='white', bg='black',
                                font=('Roboto Bold', 12))
        self.label33.place(x=757, y=215, width=28, height=19)
        self.weekends_afternoon_value = tk.Label(self.canvas, text=App.storage_data["Setpoint_Planner_Day_Weekend_Setpoint"], fg='white', bg='black',
                                                 font=('Roboto Bold', 12))
        self.weekends_afternoon_value.place(x=704, y=262)
        self.label34 = tk.Label(self.canvas, text="Бар", fg='white', bg='black',
                                font=('Roboto Bold', 12))
        self.label34.place(x=757, y=265, width=28, height=19)
        self.weekends_evening_value = tk.Label(self.canvas, text=App.storage_data["Setpoint_Planner_Evening_Weekend_Setpoint"], fg='white', bg='black',
                                               font=('Roboto Bold', 12))
        self.weekends_evening_value.place(x=704, y=304)
        self.label35 = tk.Label(self.canvas, text="Бар", fg='white', bg='black',
                                font=('Roboto Bold', 12))
        self.label35.place(x=757, y=306, width=28, height=19)
        self.weekends_night_value = tk.Label(self.canvas, text=App.storage_data["Setpoint_Planner_Night_Weekend_Setpoint"], fg='white', bg='black',
                                             font=('Roboto Bold', 12))
        self.weekends_night_value.place(x=704, y=348)
        self.label36 = tk.Label(self.canvas, text="Бар", fg='white', bg='black',
                                font=('Roboto Bold', 12))
        self.label36.place(x=757, y=350, width=28, height=19)

        self.button_day1 = tk.Button(self, text='ПН', font=('Roboto Bold', 12), bg=self.colors_button(App.storage_data["Button_one_color"]), fg='white', relief="groove",
                                activebackground=self.colors_button(App.storage_data["Button_one_color"]), activeforeground="white", command=lambda: self.check_password("button1"))
        self.button_day1.place(x=510, y=107, width=35, height=35)
        self.button_day2 = tk.Button(self, text='ВТ', font=('Roboto Bold', 12), bg=self.colors_button(App.storage_data["Button_two_color"]), fg='white', relief="groove",
                                activebackground=self.colors_button(App.storage_data["Button_two_color"]), activeforeground="white", command=lambda: self.check_password("button2"))
        self.button_day2.place(x=550, y=107, width=35, height=35)
        self.button_day3 = tk.Button(self, text='СР', font=('Roboto Bold', 12), bg=self.colors_button(App.storage_data["Button_three_color"]), fg='white', relief="groove",
                                activebackground=self.colors_button(App.storage_data["Button_three_color"]), activeforeground="white", command=lambda: self.check_password("button3"))
        self.button_day3.place(x=590, y=107, width=35, height=35)
        self.button_day4 = tk.Button(self, text='ЧТ', font=('Roboto Bold', 12), bg=self.colors_button(App.storage_data["Button_four_color"]), fg='white', relief="groove",
                                activebackground=self.colors_button(App.storage_data["Button_four_color"]), activeforeground="white", command=lambda: self.check_password("button4"))
        self.button_day4.place(x=630, y=107, width=35, height=35)
        self.button_day5 = tk.Button(self, text='ПТ', font=('Roboto Bold', 12), bg=self.colors_button(App.storage_data["Button_five_color"]), fg='white', relief="groove",
                                activebackground=self.colors_button(App.storage_data["Button_five_color"]), activeforeground="white", command=lambda: self.check_password("button5"))
        self.button_day5.place(x=670, y=107, width=35, height=35)
        self.button_day6 = tk.Button(self, text='СБ', font=('Roboto Bold', 12), bg=self.colors_button(App.storage_data["Button_six_color"]), fg='white', relief="groove",
                                activebackground=self.colors_button(App.storage_data["Button_six_color"]), activeforeground="white", command=lambda: self.check_password("button6"))
        self.button_day6.place(x=710, y=107, width=35, height=35)
        self.button_day7 = tk.Button(self, text='ВС', font=('Roboto Bold', 12), bg=self.colors_button(App.storage_data["Button_seven_color"]), fg='white', relief="groove",
                                activebackground=self.colors_button(App.storage_data["Button_seven_color"]), activeforeground="white", command=lambda: self.check_password("button7"))
        self.button_day7.place(x=750, y=107, width=35, height=35)
        self.button_dict = {"Понедельник": self.button_day1.cget('bg'), "Вторник": self.button_day2.cget('bg'), "Среда": self.button_day3.cget('bg'),
                            "Четверг": self.button_day4.cget('bg'), "Пятница": self.button_day5.cget('bg'), "Суббота": self.button_day6.cget('bg'),
                            "Воскресенье": self.button_day7.cget('bg')}

        self.canvas.tag_bind(self.setpoint, "<Button-1>", lambda event: self.check_password("click1"))
        self.setpoint_value.bind("<Button-1>", lambda event: self.check_password("click1"))
        self.label28.bind("<Button-1>", lambda event: self.check_password("click1"))

        self.weekdays_morning_h.bind("<Button-1>", lambda event: self.check_password("click2"))
        self.weekdays_afternoon_h.bind("<Button-1>", lambda event: self.check_password("click3"))
        self.weekdays_evening_h.bind("<Button-1>", lambda event: self.check_password("click4"))
        self.weekdays_night_h.bind("<Button-1>", lambda event: self.check_password("click5"))
        self.weekdays_morning_m.bind("<Button-1>", lambda event: self.check_password("click6"))
        self.weekdays_afternoon_m.bind("<Button-1>", lambda event: self.check_password("click7"))
        self.weekdays_evening_m.bind("<Button-1>", lambda event: self.check_password("click8"))
        self.weekdays_night_m.bind("<Button-1>", lambda event: self.check_password("click9"))
        self.weekends_morning_h.bind("<Button-1>", lambda event: self.check_password("click10"))
        self.weekends_afternoon_h.bind("<Button-1>", lambda event: self.check_password("click11"))
        self.weekends_evening_h.bind("<Button-1>", lambda event: self.check_password("click12"))
        self.weekends_night_h.bind("<Button-1>", lambda event: self.check_password("click13"))
        self.weekends_morning_m.bind("<Button-1>", lambda event: self.check_password("click14"))
        self.weekends_afternoon_m.bind("<Button-1>", lambda event: self.check_password("click15"))
        self.weekends_evening_m.bind("<Button-1>", lambda event: self.check_password("click16"))
        self.weekends_night_m.bind("<Button-1>", lambda event: self.check_password("click17"))

        self.canvas.tag_bind(self.weekdays_morning_field, "<Button-1>", lambda event: self.check_password("click18"))
        self.weekdays_morning_value.bind("<Button-1>", lambda event: self.check_password("click18"))
        self.label29.bind("<Button-1>", lambda event: self.check_password("click18"))
        self.canvas.tag_bind(self.weekdays_afternoon_field, "<Button-1>", lambda event: self.check_password("click19"))
        self.weekdays_afternoon_value.bind("<Button-1>", lambda event: self.check_password("click19"))
        self.label30.bind("<Button-1>", lambda event: self.check_password("click19"))
        self.canvas.tag_bind(self.weekdays_evening_field, "<Button-1>", lambda event: self.check_password("click20"))
        self.weekdays_evening_value.bind("<Button-1>", lambda event: self.check_password("click20"))
        self.label31.bind("<Button-1>", lambda event: self.check_password("click20"))
        self.canvas.tag_bind(self.weekdays_night_field, "<Button-1>", lambda event: self.check_password("click21"))
        self.weekdays_night_value.bind("<Button-1>", lambda event: self.check_password("click21"))
        self.label32.bind("<Button-1>", lambda event: self.check_password("click21"))

        self.canvas.tag_bind(self.weekends_morning_field, "<Button-1>", lambda event: self.check_password("click22"))
        self.weekends_morning_value.bind("<Button-1>", lambda event: self.check_password("click22"))
        self.label33.bind("<Button-1>", lambda event: self.check_password("click22"))
        self.canvas.tag_bind(self.weekends_afternoon_field, "<Button-1>", lambda event: self.check_password("click23"))
        self.weekends_afternoon_value.bind("<Button-1>", lambda event: self.check_password("click23"))
        self.label34.bind("<Button-1>", lambda event: self.check_password("click23"))
        self.canvas.tag_bind(self.weekends_evening_field, "<Button-1>", lambda event: self.check_password("click24"))
        self.weekends_evening_value.bind("<Button-1>", lambda event: self.check_password("click24"))
        self.label35.bind("<Button-1>", lambda event: self.check_password("click24"))
        self.canvas.tag_bind(self.weekends_night_field, "<Button-1>", lambda event: self.check_password("click25"))
        self.weekends_night_value.bind("<Button-1>", lambda event: self.check_password("click25"))
        self.label36.bind("<Button-1>", lambda event: self.check_password("click25"))
        # Кликабельная зона

        self.day = tk.Label(self.canvas, text="", fg='white', bg='black',
                                font=('Roboto Bold', 12))
        self.current_day = datetime.now()
        self.weekday = self.current_day.weekday() + 1
        match (self.weekday):
            case 1:
                self.day.config(text="Понедельник")
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

        self.type_setpoint = tk.Label(self.canvas, text="Пользователь" if App.storage_data["Substitution_Setpoint"] == "0" else "PID", fg='white', bg='black',
                            font=('Roboto Bold', 12))
        self.type_setpoint.place(x=354, y=444)


        self.type_day = tk.Label(self.canvas, text="", fg='white', bg='black',
                                      font=('Roboto Bold', 12))
        self.type_day.place(x=625, y=414)

        self.current_setpoint = tk.Label(self.canvas, text="", fg='white', bg='black',
                                 font=('Roboto Bold', 12))
        self.current_setpoint.config(text="3.00")
        self.current_setpoint.place(x=675, y=444)


        self.clock_label = tk.Label(self.canvas, text="", fg='white', bg='black', font=('Roboto Bold', 12))
        self.clock_label.place(x=680, y=5)

        self.font = ImageFont.truetype("Roboto-Bold.ttf", 18)
        self.img_screen = Image.open(r"new_images/screen.png")
        self.img_calendar = Image.open(r"new_images/calendar.png")
        self.img_peak = Image.open(r"new_images/peak.png")
        self.img_tablet = Image.open(r"new_images/tablet.png")
        self.img_gear_wheel = Image.open(r"new_images/gear_wheel.png")
        self.img_wrench = Image.open(r"new_images/wrench.png")
        self.img_gear_wheel_bg = Image.open(r"new_images/gear_wheel_bg.png")
        self.img_phone = Image.open(r"new_images/phone.png")
        self.img_right = Image.open(r"new_images/right.png")
        self.img_triangle = Image.open(r"new_images/triangle.png")

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

        self.update_type_day()
        self.after(500, self.update_setpoints)

    def update_setpoints(self):
        if self.type_setpoint.cget('text') == "Пользователь":
            self.current_setpoint.config(text=self.setpoint_value.cget('text'))
        elif self.type_setpoint.cget('text') == "PID":
            self.current_setpoint.config(text=App.global_controller.frames["Frame16"].setpoint.cget('text'))
        App.global_controller.frames["Frame1_1"].task_value.config(text=self.current_setpoint.cget('text'))
        App.global_controller.frames["Frame1_2"].task_value.config(text=self.current_setpoint.cget('text'))
        App.global_controller.frames["Frame1_3"].task_value.config(text=self.current_setpoint.cget('text'))
        App.global_controller.frames["Frame1_4"].task_value.config(text=self.current_setpoint.cget('text'))
        App.global_controller.frames["Frame16"].current_setpoint.config(text=self.current_setpoint.cget('text'))


    def colors_button(self, choice):
        match (choice):
            case "buttonblue":
                return "#0F91DA"
            case "buttonred":
                return "#871212"
            case "buttongray":
                return "#3C3C3C"

    def update_type_day(self):
        self.button_dict = {"Понедельник": self.button_day1.cget('bg'), "Вторник": self.button_day2.cget('bg'),
                            "Среда": self.button_day3.cget('bg'),
                            "Четверг": self.button_day4.cget('bg'), "Пятница": self.button_day5.cget('bg'),
                            "Суббота": self.button_day6.cget('bg'),
                            "Воскресенье": self.button_day7.cget('bg')}
        match (self.button_dict[self.day.cget('text')]):
            case "#3C3C3C":
                self.type_day.config(text="Не определен")
            case "#0F91DA":
                self.type_day.config(text="Будний")
            case "#871212":
                self.type_day.config(text="Выходной")
    def check_password(self, word):
        print("check_password")
        if App.session_access == True:
            if App.LVL_access <= 7:
                App.global_controller.frames["Frame8"].update_tree(datetime.now().strftime("%d.%m.%Y"))
                if word == "click1":
                    App.numpad_instance = numpad.Numpad(None, "FLOAT2")
                    App.numpad_instance.min_value.config(text="0.00")
                    App.numpad_instance.max_value.config(text="99.99")
                    App.numpad_instance.new_title("Уставка пользователя ")
                    App.numpad_instance.entry_label.config(text=self.setpoint_value.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click1
                elif word == "click2":
                    App.numpad_instance = numpad.Numpad(None, "INT")
                    App.numpad_instance.min_value.config(text="0")
                    App.numpad_instance.max_value.config(text="23")
                    App.numpad_instance.new_title("Будни утро(часы) ")
                    App.numpad_instance.entry_label.config(text=self.weekdays_morning_h.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click2
                elif word == "click3":
                    App.numpad_instance = numpad.Numpad(None, "INT")
                    App.numpad_instance.min_value.config(text="0")
                    App.numpad_instance.max_value.config(text="23")
                    App.numpad_instance.new_title("Будни день(часы) ")
                    App.numpad_instance.entry_label.config(text=self.weekdays_afternoon_h.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click3
                elif word == "click4":
                    App.numpad_instance = numpad.Numpad(None, "INT")
                    App.numpad_instance.min_value.config(text="0")
                    App.numpad_instance.max_value.config(text="23")
                    App.numpad_instance.new_title("Будни вечер(часы) ")
                    App.numpad_instance.entry_label.config(text=self.weekdays_evening_h.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click4
                elif word == "click5":
                    App.numpad_instance = numpad.Numpad(None, "INT")
                    App.numpad_instance.min_value.config(text="0")
                    App.numpad_instance.max_value.config(text="23")
                    App.numpad_instance.new_title("Будни ночь(часы) ")
                    App.numpad_instance.entry_label.config(text=self.weekdays_night_h.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click5
                elif word == "click6":
                    App.numpad_instance = numpad.Numpad(None, "INT")
                    App.numpad_instance.min_value.config(text="0")
                    App.numpad_instance.max_value.config(text="59")
                    App.numpad_instance.new_title("Будни утро(минуты) ")
                    App.numpad_instance.entry_label.config(text=self.weekdays_morning_m.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click6
                elif word == "click7":
                    App.numpad_instance = numpad.Numpad(None, "INT")
                    App.numpad_instance.min_value.config(text="0")
                    App.numpad_instance.max_value.config(text="59")
                    App.numpad_instance.new_title("Будни день(минуты) ")
                    App.numpad_instance.entry_label.config(text=self.weekdays_afternoon_m.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click7
                elif word == "click8":
                    App.numpad_instance = numpad.Numpad(None, "INT")
                    App.numpad_instance.min_value.config(text="0")
                    App.numpad_instance.max_value.config(text="59")
                    App.numpad_instance.new_title("Будни вечер(минуты) ")
                    App.numpad_instance.entry_label.config(text=self.weekdays_evening_m.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click8
                elif word == "click9":
                    App.numpad_instance = numpad.Numpad(None, "INT")
                    App.numpad_instance.min_value.config(text="0")
                    App.numpad_instance.max_value.config(text="59")
                    App.numpad_instance.new_title("Будни ночь(минуты) ")
                    App.numpad_instance.entry_label.config(text=self.weekdays_night_m.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click9
                elif word == "click10":
                    App.numpad_instance = numpad.Numpad(None, "INT")
                    App.numpad_instance.min_value.config(text="0")
                    App.numpad_instance.max_value.config(text="23")
                    App.numpad_instance.new_title("Выходные утро(часы) ")
                    App.numpad_instance.entry_label.config(text=self.weekends_morning_h.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click10
                elif word == "click11":
                    App.numpad_instance = numpad.Numpad(None, "INT")
                    App.numpad_instance.min_value.config(text="0")
                    App.numpad_instance.max_value.config(text="23")
                    App.numpad_instance.new_title("Выходные день(часы) ")
                    App.numpad_instance.entry_label.config(text=self.weekends_afternoon_h.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click11
                elif word == "click12":
                    App.numpad_instance = numpad.Numpad(None, "INT")
                    App.numpad_instance.min_value.config(text="0")
                    App.numpad_instance.max_value.config(text="23")
                    App.numpad_instance.new_title("Выходные вечер(часы) ")
                    App.numpad_instance.entry_label.config(text=self.weekends_evening_h.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click12
                elif word == "click13":
                    App.numpad_instance = numpad.Numpad(None, "INT")
                    App.numpad_instance.min_value.config(text="0")
                    App.numpad_instance.max_value.config(text="23")
                    App.numpad_instance.new_title("Выходные ночь(часы) ")
                    App.numpad_instance.entry_label.config(text=self.weekends_night_h.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click13
                elif word == "click14":
                    App.numpad_instance = numpad.Numpad(None, "INT")
                    App.numpad_instance.min_value.config(text="0")
                    App.numpad_instance.max_value.config(text="59")
                    App.numpad_instance.new_title("Выходные утро(минуты) ")
                    App.numpad_instance.entry_label.config(text=self.weekends_morning_m.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click14
                elif word == "click15":
                    App.numpad_instance = numpad.Numpad(None, "INT")
                    App.numpad_instance.min_value.config(text="0")
                    App.numpad_instance.max_value.config(text="59")
                    App.numpad_instance.new_title("Выходные день(минуты) ")
                    App.numpad_instance.entry_label.config(text=self.weekends_afternoon_m.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click15
                elif word == "click16":
                    App.numpad_instance = numpad.Numpad(None, "INT")
                    App.numpad_instance.min_value.config(text="0")
                    App.numpad_instance.max_value.config(text="59")
                    App.numpad_instance.new_title("Выходные вечер(минуты) ")
                    App.numpad_instance.entry_label.config(text=self.weekends_evening_m.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click16
                elif word == "click17":
                    App.numpad_instance = numpad.Numpad(None, "INT")
                    App.numpad_instance.min_value.config(text="0")
                    App.numpad_instance.max_value.config(text="59")
                    App.numpad_instance.new_title("Выходные ночь(минуты) ")
                    App.numpad_instance.entry_label.config(text=self.weekends_night_m.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click17
                elif word == "click18":
                    App.numpad_instance = numpad.Numpad(None, "FLOAT2")
                    App.numpad_instance.min_value.config(text="0.00")
                    App.numpad_instance.max_value.config(text="99.99")
                    App.numpad_instance.new_title("Будни утро уставка ")
                    App.numpad_instance.entry_label.config(text=self.weekdays_morning_value.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click18
                elif word == "click19":
                    App.numpad_instance = numpad.Numpad(None, "FLOAT2")
                    App.numpad_instance.min_value.config(text="0.00")
                    App.numpad_instance.max_value.config(text="99.99")
                    App.numpad_instance.new_title("Будни день уставка ")
                    App.numpad_instance.entry_label.config(text=self.weekdays_afternoon_value.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click19
                elif word == "click20":
                    App.numpad_instance = numpad.Numpad(None, "FLOAT2")
                    App.numpad_instance.min_value.config(text="0.00")
                    App.numpad_instance.max_value.config(text="99.99")
                    App.numpad_instance.new_title("Будни вечер уставка ")
                    App.numpad_instance.entry_label.config(text=self.weekdays_evening_value.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click20
                elif word == "click21":
                    App.numpad_instance = numpad.Numpad(None, "FLOAT2")
                    App.numpad_instance.min_value.config(text="0.00")
                    App.numpad_instance.max_value.config(text="99.99")
                    App.numpad_instance.new_title("Будни ночь уставка ")
                    App.numpad_instance.entry_label.config(text=self.weekdays_night_value.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click21
                elif word == "click22":
                    App.numpad_instance = numpad.Numpad(None, "FLOAT2")
                    App.numpad_instance.min_value.config(text="0.00")
                    App.numpad_instance.max_value.config(text="99.99")
                    App.numpad_instance.new_title("Выходные утро уставка ")
                    App.numpad_instance.entry_label.config(text=self.weekends_morning_value.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click22
                elif word == "click23":
                    App.numpad_instance = numpad.Numpad(None, "FLOAT2")
                    App.numpad_instance.min_value.config(text="0.00")
                    App.numpad_instance.max_value.config(text="99.99")
                    App.numpad_instance.new_title("Выходные день уставка ")
                    App.numpad_instance.entry_label.config(text=self.weekends_afternoon_value.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click23
                elif word == "click24":
                    App.numpad_instance = numpad.Numpad(None, "FLOAT2")
                    App.numpad_instance.min_value.config(text="0.00")
                    App.numpad_instance.max_value.config(text="99.99")
                    App.numpad_instance.new_title("Выходные вечер уставка ")
                    App.numpad_instance.entry_label.config(text=self.weekends_evening_value.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click24
                elif word == "click25":
                    App.numpad_instance = numpad.Numpad(None, "FLOAT2")
                    App.numpad_instance.min_value.config(text="0.00")
                    App.numpad_instance.max_value.config(text="99.99")
                    App.numpad_instance.new_title("Выходные ночь уставка ")
                    App.numpad_instance.entry_label.config(text=self.weekends_night_value.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click25
                elif word == "button1":
                    if self.button_day1.cget('bg') == "#3C3C3C":
                        self.button_day1.config(bg="#0F91DA", activebackground="#0F91DA")
                        App.storage_data["Button_one_color"] = "buttonblue"
                    elif self.button_day1.cget('bg') == "#0F91DA":
                        self.button_day1.config(bg="#871212", activebackground="#871212")
                        App.storage_data["Button_one_color"] = "buttonred"
                    else:
                        self.button_day1.config(bg="#3C3C3C", activebackground="#3C3C3C")
                        App.storage_data["Button_one_color"] = "buttongray"
                    self.update_type_day()
                elif word == "button2":
                    if self.button_day2.cget('bg') == "#3C3C3C":
                        self.button_day2.config(bg="#0F91DA", activebackground="#0F91DA")
                        App.storage_data["Button_two_color"] = "buttonblue"
                    elif self.button_day2.cget('bg') == "#0F91DA":
                        self.button_day2.config(bg="#871212", activebackground="#871212")
                        App.storage_data["Button_two_color"] = "buttonred"
                    else:
                        self.button_day2.config(bg="#3C3C3C", activebackground="#3C3C3C")
                        App.storage_data["Button_two_color"] = "buttongray"
                    self.update_type_day()
                elif word == "button3":
                    if self.button_day3.cget('bg') == "#3C3C3C":
                        self.button_day3.config(bg="#0F91DA", activebackground="#0F91DA")
                        App.storage_data["Button_three_color"] = "buttonblue"
                    elif self.button_day3.cget('bg') == "#0F91DA":
                        self.button_day3.config(bg="#871212", activebackground="#871212")
                        App.storage_data["Button_three_color"] = "buttonred"
                    else:
                        self.button_day3.config(bg="#3C3C3C", activebackground="#3C3C3C")
                        App.storage_data["Button_three_color"] = "buttongray"
                    self.update_type_day()
                elif word == "button4":
                    if self.button_day4.cget('bg') == "#3C3C3C":
                        self.button_day4.config(bg="#0F91DA", activebackground="#0F91DA")
                        App.storage_data["Button_four_color"] = "buttonblue"
                    elif self.button_day4.cget('bg') == "#0F91DA":
                        self.button_day4.config(bg="#871212", activebackground="#871212")
                        App.storage_data["Button_four_color"] = "buttonred"
                    else:
                        self.button_day4.config(bg="#3C3C3C", activebackground="#3C3C3C")
                        App.storage_data["Button_four_color"] = "buttongray"
                    self.update_type_day()
                elif word == "button5":
                    if self.button_day5.cget('bg') == "#3C3C3C":
                        self.button_day5.config(bg="#0F91DA", activebackground="#0F91DA")
                        App.storage_data["Button_five_color"] = "buttonblue"
                    elif self.button_day5.cget('bg') == "#0F91DA":
                        self.button_day5.config(bg="#871212", activebackground="#871212")
                        App.storage_data["Button_five_color"] = "buttonred"
                    else:
                        self.button_day5.config(bg="#3C3C3C", activebackground="#3C3C3C")
                        App.storage_data["Button_five_color"] = "buttongray"
                    self.update_type_day()
                elif word == "button6":
                    if self.button_day6.cget('bg') == "#3C3C3C":
                        self.button_day6.config(bg="#0F91DA", activebackground="#0F91DA")
                        App.storage_data["Button_six_color"] = "buttonblue"
                    elif self.button_day6.cget('bg') == "#0F91DA":
                        self.button_day6.config(bg="#871212", activebackground="#871212")
                        App.storage_data["Button_six_color"] = "buttonred"
                    else:
                        self.button_day6.config(bg="#3C3C3C", activebackground="#3C3C3C")
                        App.storage_data["Button_six_color"] = "buttongray"
                    self.update_type_day()
                elif word == "button7":
                    if self.button_day7.cget('bg') == "#3C3C3C":
                        self.button_day7.config(bg="#0F91DA", activebackground="#0F91DA")
                        App.storage_data["Button_seven_color"] = "buttonblue"
                    elif self.button_day7.cget('bg') == "#0F91DA":
                        self.button_day7.config(bg="#871212", activebackground="#871212")
                        App.storage_data["Button_seven_color"] = "buttonred"
                    else:
                        self.button_day7.config(bg="#3C3C3C", activebackground="#3C3C3C")
                        App.storage_data["Button_seven_color"] = "buttongray"
                    self.update_type_day()
                json_methods.save_data(r"data/desktop_storage.json", App.storage_data)
            else:
                messagebox.showerror("Ошибка!", "Недостаточно прав!")
        else:
            self.keypad_instance = keypad.Keypad()
            self.keypad_instance.grab_set()
            self.keypad_instance.callback_function = self.set_access

    def click1(self):
        App.global_controller.frames["Frame8"].tree.insert("", tk.END, values=(datetime.now().strftime("%d.%m.%Y"), datetime.now().strftime("%H:%M:%S"), self.label2.cget('text'), f"{self.setpoint_value.cget('text')} -> {App.numpad_instance.current_value}", "SetpointPlanner"))
        App.global_controller.frames["Frame2"].setpoint_value.config(text=App.numpad_instance.current_value)
        App.storage_data["User_Setpoint"] = App.numpad_instance.current_value
        json_methods.save_data(r"data/desktop_storage.json", App.storage_data)
        self.update_setpoints()
        json_methods.save_data(App.file_path, App.global_controller.frames["Frame8"].save_journal_data())
    def click2(self):
        if len(App.numpad_instance.current_value) == 1:
            App.numpad_instance.current_value = "0" + App.numpad_instance.current_value
        App.global_controller.frames["Frame2"].weekdays_morning_h.config(text=App.numpad_instance.current_value)
        App.storage_data["Setpoint_Planner_Morning_Weekday_Hour"] = App.numpad_instance.current_value
        json_methods.save_data(r"data/desktop_storage.json", App.storage_data)

    def click3(self):
        if len(App.numpad_instance.current_value) == 1:
            App.numpad_instance.current_value = "0" + App.numpad_instance.current_value
        App.global_controller.frames["Frame2"].weekdays_afternoon_h.config(text=App.numpad_instance.current_value)
        App.storage_data["Setpoint_Planner_Day_Weekday_Hour"] = App.numpad_instance.current_value
        json_methods.save_data(r"data/desktop_storage.json", App.storage_data)

    def click4(self):
        if len(App.numpad_instance.current_value) == 1:
            App.numpad_instance.current_value = "0" + App.numpad_instance.current_value
        App.global_controller.frames["Frame2"].weekdays_evening_h.config(text=App.numpad_instance.current_value)
        App.storage_data["Setpoint_Planner_Evening_Weekday_Hour"] = App.numpad_instance.current_value
        json_methods.save_data(r"data/desktop_storage.json", App.storage_data)
    def click5(self):
        if len(App.numpad_instance.current_value) == 1:
            App.numpad_instance.current_value = "0" + App.numpad_instance.current_value
        App.global_controller.frames["Frame2"].weekdays_night_h.config(text=App.numpad_instance.current_value)
        App.storage_data["Setpoint_Planner_Night_Weekday_Hour"] = App.numpad_instance.current_value
        json_methods.save_data(r"data/desktop_storage.json", App.storage_data)

    def click6(self):
        if len(App.numpad_instance.current_value) == 1:
            App.numpad_instance.current_value = "0" + App.numpad_instance.current_value
        App.global_controller.frames["Frame2"].weekdays_morning_m.config(text=App.numpad_instance.current_value)
        App.storage_data["Setpoint_Planner_Morning_Weekday_Minute"] = App.numpad_instance.current_value
        json_methods.save_data(r"data/desktop_storage.json", App.storage_data)

    def click7(self):
        if len(App.numpad_instance.current_value) == 1:
            App.numpad_instance.current_value = "0" + App.numpad_instance.current_value
        App.global_controller.frames["Frame2"].weekdays_afternoon_m.config(text=App.numpad_instance.current_value)
        App.storage_data["Setpoint_Planner_Day_Weekday_Minute"] = App.numpad_instance.current_value
        json_methods.save_data(r"data/desktop_storage.json", App.storage_data)

    def click8(self):
        if len(App.numpad_instance.current_value) == 1:
            App.numpad_instance.current_value = "0" + App.numpad_instance.current_value
        App.global_controller.frames["Frame2"].weekdays_evening_m.config(text=App.numpad_instance.current_value)
        App.storage_data["Setpoint_Planner_Evening_Weekday_Minute"] = App.numpad_instance.current_value
        json_methods.save_data(r"data/desktop_storage.json", App.storage_data)

    def click9(self):
        if len(App.numpad_instance.current_value) == 1:
            App.numpad_instance.current_value = "0" + App.numpad_instance.current_value
        App.global_controller.frames["Frame2"].weekdays_night_m.config(text=App.numpad_instance.current_value)
        App.storage_data["Setpoint_Planner_Night_Weekday_Minute"] = App.numpad_instance.current_value
        json_methods.save_data(r"data/desktop_storage.json", App.storage_data)

    def click10(self):
        if len(App.numpad_instance.current_value) == 1:
            App.numpad_instance.current_value = "0" + App.numpad_instance.current_value
        App.global_controller.frames["Frame2"].weekends_morning_h.config(text=App.numpad_instance.current_value)
        App.storage_data["Setpoint_Planner_Morning_Weekend_Hour"] = App.numpad_instance.current_value
        json_methods.save_data(r"data/desktop_storage.json", App.storage_data)

    def click11(self):
        if len(App.numpad_instance.current_value) == 1:
            App.numpad_instance.current_value = "0" + App.numpad_instance.current_value
        App.global_controller.frames["Frame2"].weekends_afternoon_h.config(text=App.numpad_instance.current_value)
        App.storage_data["Setpoint_Planner_Day_Weekend_Hour"] = App.numpad_instance.current_value
        json_methods.save_data(r"data/desktop_storage.json", App.storage_data)

    def click12(self):
        if len(App.numpad_instance.current_value) == 1:
            App.numpad_instance.current_value = "0" + App.numpad_instance.current_value
        App.global_controller.frames["Frame2"].weekends_evening_h.config(text=App.numpad_instance.current_value)
        App.storage_data["Setpoint_Planner_Evening_Weekend_Hour"] = App.numpad_instance.current_value
        json_methods.save_data(r"data/desktop_storage.json", App.storage_data)

    def click13(self):
        if len(App.numpad_instance.current_value) == 1:
            App.numpad_instance.current_value = "0" + App.numpad_instance.current_value
        App.global_controller.frames["Frame2"].weekends_night_h.config(text=App.numpad_instance.current_value)
        App.storage_data["Setpoint_Planner_Night_Weekend_Hour"] = App.numpad_instance.current_value
        json_methods.save_data(r"data/desktop_storage.json", App.storage_data)

    def click14(self):
        if len(App.numpad_instance.current_value) == 1:
            App.numpad_instance.current_value = "0" + App.numpad_instance.current_value
        App.global_controller.frames["Frame2"].weekends_morning_m.config(text=App.numpad_instance.current_value)
        App.storage_data["Setpoint_Planner_Morning_Weekend_Minute"] = App.numpad_instance.current_value
        json_methods.save_data(r"data/desktop_storage.json", App.storage_data)

    def click15(self):
        if len(App.numpad_instance.current_value) == 1:
            App.numpad_instance.current_value = "0" + App.numpad_instance.current_value
        App.global_controller.frames["Frame2"].weekends_afternoon_m.config(text=App.numpad_instance.current_value)
        App.storage_data["Setpoint_Planner_Day_Weekend_Minute"] = App.numpad_instance.current_value
        json_methods.save_data(r"data/desktop_storage.json", App.storage_data)

    def click16(self):
        if len(App.numpad_instance.current_value) == 1:
            App.numpad_instance.current_value = "0" + App.numpad_instance.current_value
        App.global_controller.frames["Frame2"].weekends_evening_m.config(text=App.numpad_instance.current_value)
        App.storage_data["Setpoint_Planner_Evening_Weekend_Minute"] = App.numpad_instance.current_value
        json_methods.save_data(r"data/desktop_storage.json", App.storage_data)

    def click17(self):
        if len(App.numpad_instance.current_value) == 1:
            App.numpad_instance.current_value = "0" + App.numpad_instance.current_value
        App.global_controller.frames["Frame2"].weekends_night_m.config(text=App.numpad_instance.current_value)
        App.storage_data["Setpoint_Planner_Night_Weekend_Minute"] = App.numpad_instance.current_value
        json_methods.save_data(r"data/desktop_storage.json", App.storage_data)

    def click18(self):
        App.global_controller.frames["Frame2"].weekdays_morning_value.config(text=App.numpad_instance.current_value)
        App.storage_data["Setpoint_Planner_Morning_Weekday_Setpoint"] = App.numpad_instance.current_value
        json_methods.save_data(r"data/desktop_storage.json", App.storage_data)

    def click19(self):
        App.global_controller.frames["Frame2"].weekdays_afternoon_value.config(text=App.numpad_instance.current_value)
        App.storage_data["Setpoint_Planner_Day_Weekday_Setpoint"] = App.numpad_instance.current_value
        json_methods.save_data(r"data/desktop_storage.json", App.storage_data)

    def click20(self):
        App.global_controller.frames["Frame2"].weekdays_evening_value.config(text=App.numpad_instance.current_value)
        App.storage_data["Setpoint_Planner_Evening_Weekday_Setpoint"] = App.numpad_instance.current_value
        json_methods.save_data(r"data/desktop_storage.json", App.storage_data)

    def click21(self):
        App.global_controller.frames["Frame2"].weekdays_night_value.config(text=App.numpad_instance.current_value)
        App.storage_data["Setpoint_Planner_Night_Weekday_Setpoint"] = App.numpad_instance.current_value
        json_methods.save_data(r"data/desktop_storage.json", App.storage_data)

    def click22(self):
        App.global_controller.frames["Frame2"].weekends_morning_value.config(text=App.numpad_instance.current_value)
        App.storage_data["Setpoint_Planner_Morning_Weekend_Setpoint"] = App.numpad_instance.current_value
        json_methods.save_data(r"data/desktop_storage.json", App.storage_data)

    def click23(self):
        App.global_controller.frames["Frame2"].weekends_afternoon_value.config(text=App.numpad_instance.current_value)
        App.storage_data["Setpoint_Planner_Day_Weekend_Setpoint"] = App.numpad_instance.current_value
        json_methods.save_data(r"data/desktop_storage.json", App.storage_data)

    def click24(self):
        App.global_controller.frames["Frame2"].weekends_evening_value.config(text=App.numpad_instance.current_value)
        App.storage_data["Setpoint_Planner_Evening_Weekend_Setpoint"] = App.numpad_instance.current_value
        json_methods.save_data(r"data/desktop_storage.json", App.storage_data)

    def click25(self):
        App.global_controller.frames["Frame2"].weekends_night_value.config(text=App.numpad_instance.current_value)
        App.storage_data["Setpoint_Planner_Night_Weekend_Setpoint"] = App.numpad_instance.current_value
        json_methods.save_data(r"data/desktop_storage.json", App.storage_data)


    def set_access(self, event=None):
        print("set_access")
        App.session_access = True
        App.LVL_access = self.keypad_instance.access
        App.shields_hide()
        if App.LVL_access > 7:
            messagebox.showerror("Ошибка!", "Недостаточно прав!")



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
        self.img_screen = Image.open(r"new_images/screen.png")
        self.img_peak = Image.open(r"new_images/peak.png")
        self.img_timer = Image.open(r"new_images/timer.png")
        self.img_right = Image.open(r"new_images/right.png")
        self.img_left = Image.open(r"new_images/left.png")
        self.img_triangle = Image.open(r"new_images/triangle.png")

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
        self.img_screen = Image.open(r"new_images/screen.png")
        self.img_left = Image.open(r"new_images/left.png")

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
        self.img_screen = Image.open(r"new_images/screen.png")
        self.img_peak = Image.open(r"new_images/peak.png")
        self.img_timer = Image.open(r"new_images/timer.png")
        self.img_right = Image.open(r"new_images/right.png")
        self.img_left = Image.open(r"new_images/left.png")
        self.img_triangle = Image.open(r"new_images/triangle.png")

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
        self.img_screen = Image.open(r"new_images/screen.png")
        self.img_peak = Image.open(r"new_images/peak.png")
        self.img_timer = Image.open(r"new_images/timer.png")
        self.img_right = Image.open(r"new_images/right.png")
        self.img_left = Image.open(r"new_images/left.png")
        self.img_triangle = Image.open(r"new_images/triangle.png")

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
        self.img_screen = Image.open(r"new_images/screen.png")
        self.img_left = Image.open(r"new_images/left.png")

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

        self.button_all = tk.Button(self, text="Все", fg="white", font=('Roboto', 10), bg="#616161", relief="groove", activebackground="#616161", activeforeground="white", command=lambda: self.update_tree("All"))
        self.button_all.place(x=206, y=2, width=90, height=35)
        self.button_accident = tk.Button(self, text="Авария", fg="white", font=('Roboto', 10), bg="black", relief="groove",
                                    activebackground="black", activeforeground="white",
                                    command=lambda: self.update_tree("Accident"))
        self.button_accident.place(x=295, y=2, width=90, height=35)
        self.button_warnings = tk.Button(self, text="Предупреждения", fg="white", font=('Roboto', 10), bg="black", relief="groove",
                                    activebackground="black", activeforeground="white",
                                    command=lambda: self.update_tree("Warnings"))
        self.button_warnings.place(x=384, y=2, width=110, height=35)
        self.button_messages = tk.Button(self, text="Сообщения", fg="white", font=('Roboto', 10), bg="black", relief="groove",
                                    activebackground="black", activeforeground="white",
                                    command=lambda: self.update_tree("Messages"))
        self.button_messages.place(x=493, y=2, width=90, height=35)
        self.button_events = tk.Button(self, text="События\nпользователя", fg="white", font=('Roboto', 10), bg="black", relief="groove",
                                    activebackground="black", activeforeground="white",
                                    command=lambda: self.update_tree("Events"))
        self.button_events.place(x=582, y=2, width=90, height=35)




        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Treeview",
                             font=('Roboto', 12),
                             rowheight=25,
                             background="black",
                             foreground="white",
                             fieldbackground="black",
                             bordercolor="white")
        self.style.map("Treeview",
                       background=[('selected', 'gray')])

        self.list_box = tk.Listbox(self, bg="#161616", relief="ridge", foreground="white", selectbackground="#616161")

        files = os.listdir(r"data/desktop_journal/")
        for file in files:
            filename, extension = os.path.splitext(file)
            # Проверяем, является ли файл JSON файлом
            if extension == ".json":
                self.list_box.insert(tk.END, filename)
        self.list_box.place(x=4, y=129, width=196, height=344)
        self.list_box.bind('<<ListboxSelect>>', lambda event: App.global_controller.frames["Frame8"].update_tree(self.list_box.get(self.list_box.curselection())))

        self.tree = ttk.Treeview(self, columns=("Number", "Time", "Info"))
        self.tree["show"] = "headings"
        # Устанавливаем заголовки столбцов
        self.tree.heading("Number", text="№")
        self.tree.heading("Time", text="Время")
        self.tree.heading("Info", text="Текст события")
        self.tree.column("Number", anchor="w", width=10)
        self.tree.column("Time", anchor="w", width=50)
        self.tree.column("Info", anchor="w", width=430)

        self.tree.place(x=206, y=39, width=588, height=434)

    def update_tree(self, word):
        if word == "All":
            self.button_all.config(bg="#616161", activebackground="#616161")
            self.button_accident.config(bg="black", activebackground="black")
            self.button_warnings.config(bg="black", activebackground="black")
            self.button_messages.config(bg="black", activebackground="black")
            self.button_events.config(bg="black", activebackground="black")
        elif word == "Accident":
            self.button_all.config(bg="black", activebackground="black")
            self.button_accident.config(bg="#616161", activebackground="#616161")
            self.button_warnings.config(bg="black", activebackground="black")
            self.button_messages.config(bg="black", activebackground="black")
            self.button_events.config(bg="black", activebackground="black")
        elif word == "Warnings":
            self.button_all.config(bg="black", activebackground="black")
            self.button_accident.config(bg="black", activebackground="black")
            self.button_warnings.config(bg="#616161", activebackground="#616161")
            self.button_messages.config(bg="black", activebackground="black")
            self.button_events.config(bg="black", activebackground="black")
        elif word == "Messages":
            self.button_all.config(bg="black", activebackground="black")
            self.button_accident.config(bg="black", activebackground="black")
            self.button_warnings.config(bg="black", activebackground="black")
            self.button_messages.config(bg="#616161", activebackground="#616161")
            self.button_events.config(bg="black", activebackground="black")
        elif word == "Events":
            self.button_all.config(bg="black", activebackground="black")
            self.button_accident.config(bg="black", activebackground="black")
            self.button_warnings.config(bg="black", activebackground="black")
            self.button_messages.config(bg="black", activebackground="black")
            self.button_events.config(bg="#616161", activebackground="#616161")
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
        self.img_screen = Image.open(r"new_images/screen.png")
        self.img_peak = Image.open(r"new_images/peak.png")
        self.img_timer = Image.open(r"new_images/timer.png")
        self.img_right = Image.open(r"new_images/right.png")
        self.img_left = Image.open(r"new_images/left.png")
        self.img_triangle = Image.open(r"new_images/triangle.png")

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

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Treeview",
                        font=('Roboto', 12),
                        rowheight=25,
                        background="black",
                        foreground="white",
                        fieldbackground="black",
                        bordercolor="white")
        self.style.map("Treeview",
                  background=[('selected', 'gray')])

        self.tree = ttk.Treeview(self, columns=("Date", "Time", "Comment", "Info", "Link"))
        self.tree["show"] = "headings"
        # Устанавливаем заголовки столбцов
        self.tree.heading("Date", text="Дата")
        self.tree.heading("Time", text="Время")
        self.tree.heading("Comment", text="Комментарий")
        self.tree.heading("Info", text="Информация") #lambda: self.sort_column("Info", False)
        self.tree.heading("Link")
        self.tree.column("Date", anchor="w", width=50)
        self.tree.column("Time", anchor="w", width=50)
        self.tree.column("Comment", anchor="w", width=200)
        self.tree.column("Info", anchor="w", width=100)
        self.tree.column("Link", width=0, stretch=False)

        # Добавляем данные в TreeView
        for item in App.journal_data:
            self.tree.insert("", tk.END, values=(item["Date"], item["Time"], item["Comment"], item["Info"], item["Link"]))

        self.tree.place(x=206, y=39, width=588, height=434)
        self.tree.bind('<<TreeviewSelect>>', self.handle_treeview_select)
    '''
    def sort_column(self, col, reverse):
        data = [(self.tree.set(child, col), child) for child in self.tree.get_children("")]
        data.sort(reverse=reverse)
        for index, (value, child) in enumerate(data):
            self.tree.move(child, "", index)

        self.tree.heading(col, command=lambda: self.sort_column(col, not reverse))
    '''

    def handle_treeview_select(self, event):
        # Получаем выделенный элемент TreeView
        selected_item = self.tree.selection()
        # Получаем данные из столбца link выделенного элемента
        try:
            link = self.tree.item(selected_item)['values'][4]
            match link:
                case "SetpointPlanner":
                    App.global_controller.show_frame("Frame2")
                case "EngineParameters":
                    App.global_controller.show_frame("Frame9")
                case "SensorSettings":
                    App.global_controller.show_frame("Frame10")
                case "PumpParametersInGeneral":
                    App.global_controller.show_frame("Frame11")
                case "OnAdditionalPumps":
                    App.global_controller.show_frame("Frame12")
                case "OffOfAdditionalPumps":
                    App.global_controller.show_frame("Frame13")
                case "Options":
                    App.global_controller.show_frame("Frame14")
                case "EmergencyModes":
                    App.global_controller.show_frame("Frame15")
                case "SettingsPID":
                    App.global_controller.show_frame("Frame16")
            self.tree.selection_remove(selected_item)
        except IndexError:
            pass






    def save_journal_data(self):
        data = []
        for item_id in self.tree.get_children():
            date = self.tree.item(item_id)['values'][0]  # Получаем данные из первой колонки
            time = self.tree.item(item_id)['values'][1]  # Получаем данные из второй колонки
            comment = self.tree.item(item_id)['values'][2]  # Получаем данные из третьей колонки
            info = self.tree.item(item_id)['values'][3]  # Получаем данные из четвертой колонки
            link = self.tree.item(item_id)['values'][4]
            data.append({"Date": date, "Time": time, "Comment": comment, "Info": info, "Link": link})
        print("save in journal")
        print(data)
        App.journal_data = data
        return data
    def update_tree(self, new_path):
        self.current_journal_data = []
        print(1)
        for item_id in self.tree.get_children():
            date = self.tree.item(item_id)['values'][0]  # Получаем данные из первой колонки
            time = self.tree.item(item_id)['values'][1]  # Получаем данные из второй колонки
            comment = self.tree.item(item_id)['values'][2]  # Получаем данные из третьей колонки
            info = self.tree.item(item_id)['values'][3]  # Получаем данные из четвертой колонки
            link = self.tree.item(item_id)['values'][4]  # Получаем данные из четвертой колонки
            self.current_journal_data.append({"Date": date, "Time": time, "Comment": comment, "Info": info, "Link":link})
        if self.current_journal_data == [] or self.current_journal_data[0]["Date"] == datetime.now().strftime("%d.%m.%Y"):
            print("==")
            print(self.current_journal_data)
            if self.current_journal_data != json_methods.load_data("data/desktop_journal/"+datetime.now().strftime("%d.%m.%Y")+".json"):
                App.journal_data = self.current_journal_data
                print("save")
            else:
                print(2)
                self.tree.delete(*self.tree.get_children())
                for item in json_methods.load_data("data/desktop_journal/"+new_path+".json"):
                    self.tree.insert("", tk.END, values=(item["Date"], item["Time"], item["Comment"], item["Info"], item["Link"]))
        else:
            print(3)
            self.tree.delete(*self.tree.get_children())
            for item in json_methods.load_data("data/desktop_journal/" + new_path + ".json"):
                self.tree.insert("", tk.END, values=(item["Date"], item["Time"], item["Comment"], item["Info"], item["Link"]))




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
        self.img_screen = Image.open(r"new_images/screen.png")
        self.img_left = Image.open(r"new_images/left.png")
        self.img_triangle = Image.open(r"new_images/triangle.png")
        self.img_diode = Image.open(r"new_images/diode.png")
        self.img_swap = Image.open(r"new_images/swap.png")
        self.img_plusone = Image.open(r"new_images/plus_one.png")
        self.img_minusone = Image.open(r"new_images/minus_one.png")
        self.img_options = Image.open(r"new_images/options.png")
        self.img_emergency = Image.open(r"new_images/warning.png")

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

        self.img_thunderbolt = PhotoImage(file=f"new_images/thunderbolt.png")
        self.img_ampere = PhotoImage(file=f"new_images/ampere.png")
        self.img_frequency = PhotoImage(file=f"new_images/frequency.png")
        self.img_indicator = PhotoImage(file=f"new_images/indicator.png")
        self.img_fork = PhotoImage(file=f"new_images/fork.png")
        self.img_clock = PhotoImage(file=f"new_images/clock.png")
        self.img_clock_reverse = PhotoImage(file=f"new_images/clock_reverse.png")
        self.img_arrow_left = PhotoImage(file=f"new_images/arrow_left.png")
        self.img_arrow_right = PhotoImage(file=f"new_images/arrow_right.png")
        self.img_shield = PhotoImage(file=f"new_images/shield.png")
        self.img_rectangle_l = PhotoImage(file=f"new_images/rectangle_long.png")

        self.canvas.create_image(233, 75, image=self.img_thunderbolt)
        self.canvas.create_image(236, 111, image=self.img_ampere)
        self.canvas.create_image(235, 152, image=self.img_frequency)
        self.canvas.create_image(234, 191, image=self.img_indicator)
        self.canvas.create_image(234, 230, image=self.img_fork)
        self.canvas.create_image(232, 290, image=self.img_clock)
        self.canvas.create_image(232, 326, image=self.img_clock_reverse)
        self.canvas.create_image(229, 388, image=self.img_arrow_left)
        self.canvas.create_image(229, 424, image=self.img_arrow_right)

        self.shield1 = self.canvas.create_image(624, 75, image=self.img_shield)
        self.shield2 = self.canvas.create_image(624, 113, image=self.img_shield)
        self.shield3 = self.canvas.create_image(624, 151, image=self.img_shield)
        self.shield4 = self.canvas.create_image(624, 189, image=self.img_shield)
        self.shield5 = self.canvas.create_image(624, 227, image=self.img_shield)
        self.shield6 = self.canvas.create_image(624, 289, image=self.img_shield)
        self.shield7 = self.canvas.create_image(624, 327, image=self.img_shield)
        self.shield8 = self.canvas.create_image(624, 386, image=self.img_shield)
        self.shield9 = self.canvas.create_image(624, 424, image=self.img_shield)



        self.label1 = tk.Label(self.canvas, text="Параметры двигателей", fg='white', bg='black',
                                font=('Roboto Bold', 10))
        self.label1.place(x=210, y=40)
        self.label2 = tk.Label(self.canvas, text="Напряжение", fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label2.place(x=259, y=65)
        self.label3 = tk.Label(self.canvas, text="Ток", fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label3.place(x=259, y=103)
        self.label4 = tk.Label(self.canvas, text="Частота", fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label4.place(x=259, y=143)
        self.label5 = tk.Label(self.canvas, text="Скорость", fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label5.place(x=259, y=182)
        self.label6 = tk.Label(self.canvas, text="Мощность", fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label6.place(x=259, y=221)
        self.label7 = tk.Label(self.canvas, text="Разгон и торможение", fg='white', bg='black',
                               font=('Roboto Bold', 10))
        self.label7.place(x=213, y=258)
        self.label8 = tk.Label(self.canvas, text="Время ускорения", fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label8.place(x=259, y=280)
        self.label9 = tk.Label(self.canvas, text="Время торможения", fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label9.place(x=259, y=317)
        self.label10 = tk.Label(self.canvas, text="Управление параметрами ПЧ", fg='white', bg='black',
                               font=('Roboto Bold', 10))
        self.label10.place(x=213, y=355)
        self.label11 = tk.Label(self.canvas, text="Считывание настроек с ПЧ", fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label11.place(x=259, y=380)
        self.label12 = tk.Label(self.canvas, text="Запись настроек в ПЧ", fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label12.place(x=259, y=414)
        self.label13 = tk.Label(self.canvas, text="Внимание запись и считывание настроек возможна только в режиме стоп", fg='#FFFF00', bg='black',
                               font=('Roboto Bold', 10))
        self.label13.place(x=213, y=453)

        self.canvas.create_line(210, 255, 790, 255, fill="gray", width=1)
        self.canvas.create_line(210, 350, 790, 350, fill="gray", width=1)
        #Кликабельная зона

        self.rectangle_voltage = self.canvas.create_image(718, 71, image=self.img_rectangle_l)
        self.rectangle_current = self.canvas.create_image(718, 111, image=self.img_rectangle_l)
        self.rectangle_frequency = self.canvas.create_image(718, 151, image=self.img_rectangle_l)
        self.rectangle_speed = self.canvas.create_image(718, 191, image=self.img_rectangle_l)
        self.rectangle_power = self.canvas.create_image(718, 231, image=self.img_rectangle_l)
        self.rectangle_boost = self.canvas.create_image(718, 282, image=self.img_rectangle_l)
        self.rectangle_braking = self.canvas.create_image(718, 322, image=self.img_rectangle_l)

        self.voltage_label = tk.Label(self.canvas, text="В", fg='white', bg='black',
                                font=('Roboto Bold', 12))
        self.voltage_label.place(x=768, y=60)
        self.current_label = tk.Label(self.canvas, text="А", fg='white', bg='black',
                                font=('Roboto Bold', 12))
        self.current_label.place(x=768, y=100)
        self.frequency_label = tk.Label(self.canvas, text="Гц", fg='white', bg='black',
                                font=('Roboto Bold', 12))
        self.frequency_label.place(x=764, y=140)
        self.speed_label = tk.Label(self.canvas, text="Об/мин", fg='white', bg='black',
                                font=('Roboto Bold', 12))
        self.speed_label.place(x=728, y=180)
        self.power_label = tk.Label(self.canvas, text="кВт", fg='white', bg='black',
                                font=('Roboto Bold', 12))
        self.power_label.place(x=756, y=220)
        self.boost_label = tk.Label(self.canvas, text="Сек", fg='white', bg='black',
                                font=('Roboto Bold', 12))
        self.boost_label.place(x=752, y=270)
        self.braking_label = tk.Label(self.canvas, text="Сек", fg='white', bg='black',
                                font=('Roboto Bold', 12))
        self.braking_label.place(x=750, y=310)

        self.voltage_value = tk.Label(self.canvas, text=App.storage_data["Voltage"], fg='white', bg='black',
                                      font=('Roboto Bold', 12))
        self.voltage_value.place(x=646, y=60)
        self.current_value = tk.Label(self.canvas, text=App.storage_data["Amperage"], fg='white', bg='black',
                                      font=('Roboto Bold', 12))
        self.current_value.place(x=646, y=100)
        self.frequency_value = tk.Label(self.canvas, text=App.storage_data["Frequency"], fg='white', bg='black',
                                        font=('Roboto Bold', 12))
        self.frequency_value.place(x=646, y=140)
        self.speed_value = tk.Label(self.canvas, text=App.storage_data["Speed"], fg='white', bg='black',
                                    font=('Roboto Bold', 12))
        self.speed_value.place(x=646, y=180)
        self.power_value = tk.Label(self.canvas, text=App.storage_data["Power"], fg='white', bg='black',
                                    font=('Roboto Bold', 12))
        self.power_value.place(x=646, y=220)
        self.boost_value = tk.Label(self.canvas, text=App.storage_data["Acceleration_Time"], fg='white', bg='black',
                                    font=('Roboto Bold', 12))
        self.boost_value.place(x=646, y=270)
        self.braking_value = tk.Label(self.canvas, text=App.storage_data["Braking_Time"], fg='white', bg='black',
                                      font=('Roboto Bold', 12))
        self.braking_value.place(x=646, y=310)

        self.Switch_Flat_first_img = PhotoImage(file=r"new_images/ReadingGray.png") if App.storage_data["Reading_Settings"] == "0" else PhotoImage(file=r"new_images/ReadingGreen.png")
        self.Switch_Flat_first_button = self.canvas.create_image(689, 386.5, image=self.Switch_Flat_first_img)
        self.canvas.tag_bind(self.Switch_Flat_first_button, "<Button-1>", lambda event: self.check_password("switch1"))

        self.Switch_Flat_second_img = PhotoImage(file=r"new_images/RecordingGray.png") if App.storage_data["Recording_Settings"] == "0" else PhotoImage(file=r"new_images/RecordingGreen.png")
        self.Switch_Flat_second_button = self.canvas.create_image(689, 424.5, image=self.Switch_Flat_second_img)
        self.canvas.tag_bind(self.Switch_Flat_second_button, "<Button-1>", lambda event: self.check_password("switch2"))

        self.canvas.tag_bind(self.rectangle_voltage, "<Button-1>", lambda event: self.check_password("click1"))
        self.voltage_value.bind("<Button-1>", lambda event: self.check_password("click1"))
        self.voltage_label.bind("<Button-1>", lambda event: self.check_password("click1"))
        self.canvas.tag_bind(self.rectangle_current, "<Button-1>", lambda event: self.check_password("click2"))
        self.current_value.bind("<Button-1>", lambda event: self.check_password("click2"))
        self.current_label.bind("<Button-1>", lambda event: self.check_password("click2"))
        self.canvas.tag_bind(self.rectangle_frequency, "<Button-1>", lambda event: self.check_password("click3"))
        self.frequency_value.bind("<Button-1>", lambda event: self.check_password("click3"))
        self.frequency_label.bind("<Button-1>", lambda event: self.check_password("click3"))
        self.canvas.tag_bind(self.rectangle_speed, "<Button-1>", lambda event: self.check_password("click4"))
        self.speed_value.bind("<Button-1>", lambda event: self.check_password("click4"))
        self.speed_label.bind("<Button-1>", lambda event: self.check_password("click4"))
        self.canvas.tag_bind(self.rectangle_power, "<Button-1>", lambda event: self.check_password("click5"))
        self.power_value.bind("<Button-1>", lambda event: self.check_password("click5"))
        self.power_label.bind("<Button-1>", lambda event: self.check_password("click5"))
        self.canvas.tag_bind(self.rectangle_boost, "<Button-1>", lambda event: self.check_password("click6"))
        self.boost_value.bind("<Button-1>", lambda event: self.check_password("click6"))
        self.boost_label.bind("<Button-1>", lambda event: self.check_password("click6"))
        self.canvas.tag_bind(self.rectangle_braking, "<Button-1>", lambda event: self.check_password("click7"))
        self.braking_value.bind("<Button-1>", lambda event: self.check_password("click7"))
        self.braking_label.bind("<Button-1>", lambda event: self.check_password("click7"))
        # Кликабельная зона
    def check_password(self, word):
        print("check_password")
        if App.session_access == True:
            if App.LVL_access <= 5:
                App.global_controller.frames["Frame8"].update_tree(datetime.now().strftime("%d.%m.%Y"))
                if word == "click1":
                    App.numpad_instance = numpad.Numpad(None, "INT")
                    App.numpad_instance.min_value.config(text="100")
                    App.numpad_instance.max_value.config(text="1000")
                    App.numpad_instance.new_title(self.label2.cget('text') + " ")
                    App.numpad_instance.entry_label.config(text=self.voltage_value.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click1
                elif word == "click2":
                    App.numpad_instance = numpad.Numpad(None, "FLOAT1")
                    App.numpad_instance.min_value.config(text="0.0")
                    App.numpad_instance.max_value.config(text="99.9")
                    App.numpad_instance.new_title(self.label3.cget('text') + " ")
                    App.numpad_instance.entry_label.config(text=self.current_value.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click2
                elif word == "click3":
                    App.numpad_instance = numpad.Numpad(None, "FLOAT1")
                    App.numpad_instance.min_value.config(text="0.0")
                    App.numpad_instance.max_value.config(text="99.9")
                    App.numpad_instance.new_title(self.label4.cget('text') + " ")
                    App.numpad_instance.entry_label.config(text=self.frequency_value.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click3
                elif word == "click4":
                    App.numpad_instance = numpad.Numpad(None, "INT")
                    App.numpad_instance.min_value.config(text="0")
                    App.numpad_instance.max_value.config(text="9999")
                    App.numpad_instance.new_title(self.label5.cget('text') + " ")
                    App.numpad_instance.entry_label.config(text=self.speed_value.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click4
                elif word == "click5":
                    App.numpad_instance = numpad.Numpad(None, "FLOAT2")
                    App.numpad_instance.min_value.config(text="0.00")
                    App.numpad_instance.max_value.config(text="655.35")
                    App.numpad_instance.new_title(self.label6.cget('text') + " ")
                    App.numpad_instance.entry_label.config(text=self.power_value.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click5
                elif word == "click6":
                    App.numpad_instance = numpad.Numpad(None, "FLOAT1")
                    App.numpad_instance.min_value.config(text="0.0")
                    App.numpad_instance.max_value.config(text="99.9")
                    App.numpad_instance.new_title(self.label8.cget('text') + " ")
                    App.numpad_instance.entry_label.config(text=self.boost_value.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click6
                elif word == "click7":
                    App.numpad_instance = numpad.Numpad(None, "FLOAT1")
                    App.numpad_instance.min_value.config(text="0.0")
                    App.numpad_instance.max_value.config(text="99.9")
                    App.numpad_instance.new_title(self.label9.cget('text') + " ")
                    App.numpad_instance.entry_label.config(text=self.braking_value.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click7
                elif word == "switch1":
                    self.update_switch_first()
                elif word == "switch2":
                    self.update_switch_second()
                json_methods.save_data(r"data/desktop_storage.json", App.storage_data)
            else:
                messagebox.showerror("Ошибка!", "Недостаточно прав!")
        else:
            self.keypad_instance = keypad.Keypad()
            self.keypad_instance.grab_set()
            self.keypad_instance.callback_function = self.set_access

    def click1(self):
        App.global_controller.frames["Frame8"].tree.insert("", tk.END, values=(datetime.now().strftime("%d.%m.%Y"), datetime.now().strftime("%H:%M:%S"), self.label2.cget('text'), f"{self.voltage_value.cget('text')} -> {App.numpad_instance.current_value}", "EngineParameters"))
        App.global_controller.frames["Frame9"].voltage_value.config(text=App.numpad_instance.current_value)
        App.storage_data["Voltage"] = App.numpad_instance.current_value
        json_methods.save_data(App.file_path, App.global_controller.frames["Frame8"].save_journal_data())

    def click2(self):
        App.global_controller.frames["Frame8"].tree.insert("", tk.END, values=(
        datetime.now().strftime("%d.%m.%Y"), datetime.now().strftime("%H:%M:%S"), self.label3.cget('text'),
        f"{self.current_value.cget('text')} -> {App.numpad_instance.current_value}", "EngineParameters"))
        App.global_controller.frames["Frame9"].current_value.config(text=App.numpad_instance.current_value)
        App.storage_data["Amperage"] = App.numpad_instance.current_value
        json_methods.save_data(App.file_path, App.global_controller.frames["Frame8"].save_journal_data())
    def click3(self):
        App.global_controller.frames["Frame8"].tree.insert("", tk.END, values=(
            datetime.now().strftime("%d.%m.%Y"), datetime.now().strftime("%H:%M:%S"), self.label4.cget('text'),
            f"{self.frequency_value.cget('text')} -> {App.numpad_instance.current_value}", "EngineParameters"))
        App.global_controller.frames["Frame9"].frequency_value.config(text=App.numpad_instance.current_value)
        App.storage_data["Frequency"] = App.numpad_instance.current_value
        json_methods.save_data(App.file_path, App.global_controller.frames["Frame8"].save_journal_data())
    def click4(self):
        App.global_controller.frames["Frame8"].tree.insert("", tk.END, values=(
            datetime.now().strftime("%d.%m.%Y"), datetime.now().strftime("%H:%M:%S"), self.label5.cget('text'),
            f"{self.speed_value.cget('text')} -> {App.numpad_instance.current_value}", "EngineParameters"))
        App.global_controller.frames["Frame9"].speed_value.config(text=App.numpad_instance.current_value)
        App.storage_data["Speed"] = App.numpad_instance.current_value
        json_methods.save_data(App.file_path, App.global_controller.frames["Frame8"].save_journal_data())
    def click5(self):
        App.global_controller.frames["Frame8"].tree.insert("", tk.END, values=(
            datetime.now().strftime("%d.%m.%Y"), datetime.now().strftime("%H:%M:%S"), self.label6.cget('text'),
            f"{self.power_value.cget('text')} -> {App.numpad_instance.current_value}", "EngineParameters"))
        App.global_controller.frames["Frame9"].power_value.config(text=App.numpad_instance.current_value)
        App.storage_data["Power"] = App.numpad_instance.current_value
        json_methods.save_data(App.file_path, App.global_controller.frames["Frame8"].save_journal_data())
    def click6(self):
        App.global_controller.frames["Frame8"].tree.insert("", tk.END, values=(
            datetime.now().strftime("%d.%m.%Y"), datetime.now().strftime("%H:%M:%S"), self.label8.cget('text'),
            f"{self.boost_value.cget('text')} -> {App.numpad_instance.current_value}", "EngineParameters"))
        App.global_controller.frames["Frame9"].boost_value.config(text=App.numpad_instance.current_value)
        App.storage_data["Acceleration_Time"] = App.numpad_instance.current_value
        json_methods.save_data(App.file_path, App.global_controller.frames["Frame8"].save_journal_data())
    def click7(self):
        App.global_controller.frames["Frame8"].tree.insert("", tk.END, values=(
            datetime.now().strftime("%d.%m.%Y"), datetime.now().strftime("%H:%M:%S"), self.label9.cget('text'),
            f"{self.braking_value.cget('text')} -> {App.numpad_instance.current_value}", "EngineParameters"))
        App.global_controller.frames["Frame9"].braking_value.config(text=App.numpad_instance.current_value)
        App.storage_data["Braking_Time"] = App.numpad_instance.current_value
        json_methods.save_data(App.file_path, App.global_controller.frames["Frame8"].save_journal_data())

    def set_access(self, event=None):
        print("set_access")
        App.session_access = True
        App.LVL_access = self.keypad_instance.access
        App.shields_hide()
        if App.LVL_access > 5:
            messagebox.showerror("Ошибка!", "Недостаточно прав!")
    def update_switch_first(self):
        if self.Switch_Flat_first_img.cget("file") == "new_images/ReadingGray.png":
            self.Switch_Flat_first_img = PhotoImage(file=r"new_images/ReadingGreen.png")
            App.storage_data["Reading_Settings"] = "1"
            App.global_controller.frames["Frame8"].tree.insert("", tk.END, values=(
                datetime.now().strftime("%d.%m.%Y"), datetime.now().strftime("%H:%M:%S"), self.label11.cget('text'),
                f"OFF -> ON", "EngineParameters"))
            json_methods.save_data(App.file_path, App.global_controller.frames["Frame8"].save_journal_data())
        elif self.Switch_Flat_first_img.cget("file") == "new_images/ReadingGreen.png":
            self.Switch_Flat_first_img = PhotoImage(file=r"new_images/ReadingGray.png")
            App.storage_data["Reading_Settings"] = "0"
            App.global_controller.frames["Frame8"].tree.insert("", tk.END, values=(
                datetime.now().strftime("%d.%m.%Y"), datetime.now().strftime("%H:%M:%S"), self.label11.cget('text'),
                f"ON -> OFF", "EngineParameters"))
            json_methods.save_data(App.file_path, App.global_controller.frames["Frame8"].save_journal_data())
        self.Switch_Flat_first_button = self.canvas.create_image(689, 386.5, image=self.Switch_Flat_first_img)
        self.canvas.tag_bind(self.Switch_Flat_first_button, "<Button-1>", lambda event: self.check_password("switch1"))

    def update_switch_second(self):
        if self.Switch_Flat_second_img.cget("file") == "new_images/RecordingGray.png":
            self.Switch_Flat_second_img = PhotoImage(file=r"new_images/RecordingGreen.png")
            App.storage_data["Recording_Settings"] = "1"
            App.global_controller.frames["Frame8"].tree.insert("", tk.END, values=(
                datetime.now().strftime("%d.%m.%Y"), datetime.now().strftime("%H:%M:%S"), self.label12.cget('text'),
                f"OFF -> ON", "EngineParameters"))
            json_methods.save_data(App.file_path, App.global_controller.frames["Frame8"].save_journal_data())
        elif self.Switch_Flat_second_img.cget("file") == "new_images/RecordingGreen.png":
            self.Switch_Flat_second_img = PhotoImage(file=r"new_images/RecordingGray.png")
            App.storage_data["Recording_Settings"] = "0"
            App.global_controller.frames["Frame8"].tree.insert("", tk.END, values=(
                datetime.now().strftime("%d.%m.%Y"), datetime.now().strftime("%H:%M:%S"), self.label12.cget('text'),
                f"ON -> OFF", "EngineParameters"))
            json_methods.save_data(App.file_path, App.global_controller.frames["Frame8"].save_journal_data())
        self.Switch_Flat_second_button = self.canvas.create_image(689, 424.5, image=self.Switch_Flat_second_img)
        self.canvas.tag_bind(self.Switch_Flat_second_button, "<Button-1>", lambda event: self.check_password("switch2"))

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
        self.img_screen = Image.open(r"new_images/screen.png")
        self.img_left = Image.open(r"new_images/left.png")
        self.img_triangle = Image.open(r"new_images/triangle.png")
        self.img_diode = Image.open(r"new_images/diode.png")
        self.img_swap = Image.open(r"new_images/swap.png")
        self.img_plusone = Image.open(r"new_images/plus_one.png")
        self.img_minusone = Image.open(r"new_images/minus_one.png")
        self.img_options = Image.open(r"new_images/options.png")
        self.img_emergency = Image.open(r"new_images/warning.png")

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

        self.img_s_sensor = PhotoImage(file=f"new_images/suction_pressure_sensor.png")
        self.img_d_sensor = PhotoImage(file=f"new_images/discharge_pressure_sensor.png")
        self.img_eye = PhotoImage(file=f"new_images/eye.png")
        self.img_shield = PhotoImage(file=f"new_images/shield.png")
        self.img_rectangle_l = PhotoImage(file=f"new_images/rectangle_long.png")

        self.canvas.create_image(234, 75, image=self.img_s_sensor)
        self.canvas.create_image(234, 111, image=self.img_d_sensor)
        self.canvas.create_image(231, 166.375, image=self.img_eye)
        self.canvas.create_image(231, 196.375, image=self.img_eye)
        self.canvas.create_image(231, 238.375, image=self.img_eye)
        self.canvas.create_image(231, 272.375, image=self.img_eye)
        self.canvas.create_line(215, 143, 795, 143, fill="gray", width=1)

        self.label1 = tk.Label(self.canvas, text="Датчик давления",
                                fg='white', bg='black',
                                font=('Roboto Bold', 10))
        self.label1.place(x=213, y=40)
        self.label2 = tk.Label(self.canvas, text="Номинал датчика на всасывание",
                               fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label2.place(x=259, y=65)
        self.label3 = tk.Label(self.canvas, text="Номинал датчика на нагнетание",
                               fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label3.place(x=259, y=103)
        self.label4 = tk.Label(self.canvas, text="Показание датчика на всасывание",
                               fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label4.place(x=259, y=157)
        self.label5 = tk.Label(self.canvas, text="Показание датчика на нагнетание",
                               fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label5.place(x=259, y=187)
        self.label6 = tk.Label(self.canvas, text="Миллиампер на всасывание",
                               fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label6.place(x=259, y=230)
        self.label7 = tk.Label(self.canvas, text="Миллиампер на нагнетание",
                               fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label7.place(x=259, y=261)

        self.sensor_s_value = tk.Label(self.canvas, text="10.00",
                               fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.sensor_s_value.place(x=649, y=157)
        self.label8 = tk.Label(self.canvas, text="Бар",
                               fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label8.place(x=756, y=157)
        self.sensor_d_value = tk.Label(self.canvas, text="0.00",
                                       fg='white', bg='black',
                                       font=('Roboto Bold', 12))
        self.sensor_d_value.place(x=649, y=187)
        self.label9 = tk.Label(self.canvas, text="Бар",
                               fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label9.place(x=756, y=187)
        self.s_value = tk.Label(self.canvas, text="5.00",
                                fg='white', bg='black',
                                font=('Roboto Bold', 12))
        self.s_value.place(x=649, y=230)
        self.label10 = tk.Label(self.canvas, text="mA",
                               fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label10.place(x=758, y=230)
        self.d_value = tk.Label(self.canvas, text="0.00",
                                fg='white', bg='black',
                                font=('Roboto Bold', 12))
        self.d_value.place(x=649, y=261)
        self.label11 = tk.Label(self.canvas, text="mA",
                               fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label11.place(x=758, y=261)

        self.shield1 = self.canvas.create_image(624, 75, image=self.img_shield)
        self.shield2 = self.canvas.create_image(624, 113, image=self.img_shield)

        # Кликабельная зона
        self.rectangle_s_nominal = self.canvas.create_image(718, 75, image=self.img_rectangle_l)
        self.nominal_s_value = tk.Label(self.canvas, text=App.storage_data["Suction_Rating"],
                                fg='white', bg='black',
                                font=('Roboto Bold', 12))
        self.nominal_s_value.place(x=649, y=65)
        self.s_label = tk.Label(self.canvas, text="Бар",
                               fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.s_label.place(x=756, y=65)
        self.rectangle_d_nominal = self.canvas.create_image(718, 115, image=self.img_rectangle_l)
        self.nominal_d_value = tk.Label(self.canvas, text=App.storage_data["Discharge_Rating"],
                                        fg='white', bg='black',
                                        font=('Roboto Bold', 12))
        self.nominal_d_value.place(x=649, y=105)
        self.d_label = tk.Label(self.canvas, text="Бар",
                                fg='white', bg='black',
                                font=('Roboto Bold', 12))
        self.d_label.place(x=756, y=105)
        self.canvas.tag_bind(self.rectangle_s_nominal, "<Button-1>", lambda event: self.check_password("click1"))
        self.nominal_s_value.bind("<Button-1>", lambda event: self.check_password("click1"))
        self.s_label.bind("<Button-1>", lambda event: self.check_password("click1"))
        self.canvas.tag_bind(self.rectangle_d_nominal, "<Button-1>", lambda event: self.check_password("click2"))
        self.nominal_d_value.bind("<Button-1>", lambda event: self.check_password("click2"))
        self.d_label.bind("<Button-1>", lambda event: self.check_password("click2"))
        # Кликабельная зона
    def check_password(self, word):
        print("check_password")
        if App.session_access == True:
            if App.LVL_access <= 5:
                App.global_controller.frames["Frame8"].update_tree(datetime.now().strftime("%d.%m.%Y"))
                if word == "click1":
                    App.numpad_instance = numpad.Numpad(None, "FLOAT2")
                    App.numpad_instance.min_value.config(text="0.00")
                    App.numpad_instance.max_value.config(text="99.99")
                    App.numpad_instance.new_title(self.label2.cget('text') + " ")
                    App.numpad_instance.entry_label.config(text=self.nominal_s_value.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click1
                elif word == "click2":
                    App.numpad_instance = numpad.Numpad(None, "FLOAT2")
                    App.numpad_instance.min_value.config(text="0.00")
                    App.numpad_instance.max_value.config(text="99.99")
                    App.numpad_instance.new_title(self.label3.cget('text') + " ")
                    App.numpad_instance.entry_label.config(text=self.nominal_d_value.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click2
                json_methods.save_data(r"data/desktop_storage.json", App.storage_data)
            else:
                messagebox.showerror("Ошибка!", "Недостаточно прав!")
        else:
            self.keypad_instance = keypad.Keypad()
            self.keypad_instance.grab_set()
            self.keypad_instance.callback_function = self.set_access

    def click1(self):
        App.global_controller.frames["Frame8"].tree.insert("", tk.END, values=(
        datetime.now().strftime("%d.%m.%Y"), datetime.now().strftime("%H:%M:%S"), self.label2.cget('text'),
        f"{self.nominal_s_value.cget('text')} -> {App.numpad_instance.current_value}", "SensorSettings"))
        App.global_controller.frames["Frame10"].nominal_s_value.config(text=App.numpad_instance.current_value)
        App.storage_data["Suction_Rating"] = App.numpad_instance.current_value
        json_methods.save_data(App.file_path, App.global_controller.frames["Frame8"].save_journal_data())


    def click2(self):
        App.global_controller.frames["Frame8"].tree.insert("", tk.END, values=(
            datetime.now().strftime("%d.%m.%Y"), datetime.now().strftime("%H:%M:%S"), self.label3.cget('text'),
            f"{self.nominal_d_value.cget('text')} -> {App.numpad_instance.current_value}", "SensorSettings"))
        App.global_controller.frames["Frame10"].nominal_d_value.config(text=App.numpad_instance.current_value)
        App.storage_data["Discharge_Rating"] = App.numpad_instance.current_value
        json_methods.save_data(App.file_path, App.global_controller.frames["Frame8"].save_journal_data())

    def set_access(self, event=None):
        print("set_access")
        App.session_access = True
        App.LVL_access = self.keypad_instance.access
        App.shields_hide()
        if App.LVL_access > 5:
            messagebox.showerror("Ошибка!", "Недостаточно прав!")

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
        self.img_screen = Image.open(r"new_images/screen.png")
        self.img_left = Image.open(r"new_images/left.png")
        self.img_triangle = Image.open(r"new_images/triangle.png")
        self.img_diode = Image.open(r"new_images/diode.png")
        self.img_swap = Image.open(r"new_images/swap.png")
        self.img_plusone = Image.open(r"new_images/plus_one.png")
        self.img_minusone = Image.open(r"new_images/minus_one.png")
        self.img_options = Image.open(r"new_images/options.png")
        self.img_emergency = Image.open(r"new_images/warning.png")

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

        self.img_frequency = PhotoImage(file=f"new_images/frequency.png")
        self.img_zero = PhotoImage(file=f"new_images/zero.png")
        self.img_rotation = PhotoImage(file=f"new_images/rotation.png")
        self.img_interval = PhotoImage(file=f"new_images/interval.png")
        self.img_time = PhotoImage(file=f"new_images/time.png")
        self.img_shield = PhotoImage(file=f"new_images/shield.png")
        self.img_rectangle_l = PhotoImage(file=f"new_images/rectangle_long.png")

        self.canvas.create_image(233, 75, image=self.img_frequency)
        self.canvas.create_image(233, 114, image=self.img_frequency)
        self.canvas.create_image(233, 152.375, image=self.img_zero)
        self.canvas.create_image(233, 195, image=self.img_rotation)
        self.canvas.create_image(233, 232, image=self.img_interval)
        self.canvas.create_image(233, 268, image=self.img_time)
        self.canvas.create_line(215, 173, 795, 173, fill="gray", width=1)
        self.canvas.create_line(215, 294, 795, 294, fill="gray", width=1)

        self.shield1 = self.canvas.create_image(624, 75, image=self.img_shield)
        self.shield2 = self.canvas.create_image(624, 114, image=self.img_shield)
        self.shield3 = self.canvas.create_image(624, 153, image=self.img_shield)
        self.shield4 = self.canvas.create_image(624, 193, image=self.img_shield)
        self.shield5 = self.canvas.create_image(624, 231, image=self.img_shield)
        self.shield6 = self.canvas.create_image(624, 269, image=self.img_shield)

        self.label1 = tk.Label(self.canvas, text="Минимальная частота работы",
                               fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label1.place(x=259, y=64)
        self.label2 = tk.Label(self.canvas, text="Максимальная частота работы",
                               fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label2.place(x=259, y=102)
        self.label3 = tk.Label(self.canvas, text="Использовать пуск мастера с 0 Гц",
                               fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label3.place(x=259, y=144)
        self.label4 = tk.Label(self.canvas, text="Использовать ротацию насосов",
                               fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label4.place(x=259, y=183)
        self.label5 = tk.Label(self.canvas, text="Интервал ротации насосов",
                               fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label5.place(x=259, y=221)
        self.label6 = tk.Label(self.canvas, text="Время суток ротации",
                               fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label6.place(x=259, y=259)

        # Кликабельная зона
        self.rectangle_min_f = self.canvas.create_image(718, 75, image=self.img_rectangle_l)
        self.min_f_value = tk.Label(self.canvas, text=App.storage_data["Minimum_Frequency"],
                                        fg='white', bg='black',
                                        font=('Roboto Bold', 12))
        self.min_f_value.place(x=649, y=65)
        self.min_f_label = tk.Label(self.canvas, text="Гц",
                                fg='white', bg='black',
                                font=('Roboto Bold', 12))
        self.min_f_label.place(x=759, y=65)
        self.rectangle_max_f = self.canvas.create_image(718, 115, image=self.img_rectangle_l)
        self.max_f_value = tk.Label(self.canvas, text=App.storage_data["Maximum_Frequency"],
                                        fg='white', bg='black',
                                        font=('Roboto Bold', 12))
        self.max_f_value.place(x=649, y=105)
        self.max_f_label = tk.Label(self.canvas, text="Гц",
                                fg='white', bg='black',
                                font=('Roboto Bold', 12))
        self.max_f_label.place(x=759, y=105)

        self.Switch_Flat_first_img = PhotoImage(file=r"new_images/Switch-0.png") if App.storage_data["Start_The_Master"] == "0" else PhotoImage(file=r"new_images/Switch-1.png")
        self.Switch_Flat_first_button = self.canvas.create_image(670, 152, image=self.Switch_Flat_first_img)
        self.canvas.tag_bind(self.Switch_Flat_first_button, "<Button-1>", lambda event: self.check_password("switch1"))

        self.Switch_Flat_second_img = PhotoImage(file=r"new_images/Switch-0.png") if App.storage_data["Pump_Rotation"] == "0" else PhotoImage(file=r"new_images/Switch-1.png")
        self.Switch_Flat_second_button = self.canvas.create_image(670, 194, image=self.Switch_Flat_second_img)
        self.canvas.tag_bind(self.Switch_Flat_second_button, "<Button-1>", lambda event: self.check_password("switch2"))

        self.rectangle_interval = self.canvas.create_image(718, 230, image=self.img_rectangle_l)
        self.interval_value = tk.Label(self.canvas, text=App.storage_data["Pump_Rotation_Interval"],
                                    fg='white', bg='black',
                                    font=('Roboto Bold', 12))
        self.interval_value.place(x=649, y=220)

        self.interval_label = tk.Label(self.canvas, text="час",
                                    fg='white', bg='black',
                                    font=('Roboto Bold', 12))
        self.interval_label.place(x=759, y=220)
        self.rectangle_time = self.canvas.create_image(718, 270, image=self.img_rectangle_l)
        self.time_value = tk.Label(self.canvas, text=App.storage_data["Rotation_Time_Of_Day"],
                                    fg='white', bg='black',
                                    font=('Roboto Bold', 12))
        self.time_value.place(x=649, y=260)
        self.time_label = tk.Label(self.canvas, text="час",
                                    fg='white', bg='black',
                                    font=('Roboto Bold', 12))
        self.time_label.place(x=759, y=260)
        self.canvas.tag_bind(self.rectangle_min_f, "<Button-1>", lambda event: self.check_password("click1"))
        self.min_f_value.bind("<Button-1>", lambda event: self.check_password("click1"))
        self.min_f_label.bind("<Button-1>", lambda event: self.check_password("click1"))
        self.canvas.tag_bind(self.rectangle_max_f, "<Button-1>", lambda event: self.check_password("click2"))
        self.max_f_value.bind("<Button-1>", lambda event: self.check_password("click2"))
        self.max_f_label.bind("<Button-1>", lambda event: self.check_password("click2"))
        self.canvas.tag_bind(self.rectangle_interval, "<Button-1>", lambda event: self.check_password("click3"))
        self.interval_value.bind("<Button-1>", lambda event: self.check_password("click3"))
        self.interval_label.bind("<Button-1>", lambda event: self.check_password("click3"))
        self.canvas.tag_bind(self.rectangle_time, "<Button-1>", lambda event: self.check_password("click4"))
        self.time_value.bind("<Button-1>", lambda event: self.check_password("click4"))
        self.time_label.bind("<Button-1>", lambda event: self.check_password("click4"))
        # Кликабельная зона
    def check_password(self, word):
        print("check_password")
        if App.session_access == True:
            if App.LVL_access <= 5:
                App.global_controller.frames["Frame8"].update_tree(datetime.now().strftime("%d.%m.%Y"))
                if word == "click1":
                    App.numpad_instance = numpad.Numpad(None, "FLOAT1")
                    App.numpad_instance.min_value.config(text="15.0")
                    App.numpad_instance.max_value.config(text="30.0")
                    App.numpad_instance.new_title(self.label1.cget('text') + " ")
                    App.numpad_instance.entry_label.config(text=self.min_f_value.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click1
                elif word == "click2":
                    App.numpad_instance = numpad.Numpad(None, "FLOAT2")
                    App.numpad_instance.min_value.config(text="40.00")
                    App.numpad_instance.max_value.config(text="50.00")
                    App.numpad_instance.new_title(self.label2.cget('text') + " ")
                    App.numpad_instance.entry_label.config(text=self.max_f_value.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click2
                elif word == "click3":
                    App.numpad_instance = numpad.Numpad(None, "INT")
                    App.numpad_instance.min_value.config(text="24")
                    App.numpad_instance.max_value.config(text="72")
                    App.numpad_instance.new_title(self.label5.cget('text') + " ")
                    App.numpad_instance.entry_label.config(text=self.interval_value.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click3
                elif word == "click4":
                    App.numpad_instance = numpad.Numpad(None, "INT")
                    App.numpad_instance.min_value.config(text="0")
                    App.numpad_instance.max_value.config(text="23")
                    App.numpad_instance.new_title(self.label6.cget('text') + " ")
                    App.numpad_instance.entry_label.config(text=self.time_value.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click4
                elif word == "switch1":
                    self.update_switch_first()
                elif word == "switch2":
                    self.update_switch_second()
                json_methods.save_data(r"data/desktop_storage.json", App.storage_data)

            else:
                messagebox.showerror("Ошибка!", "Недостаточно прав!")
        else:
            self.keypad_instance = keypad.Keypad()
            self.keypad_instance.grab_set()
            self.keypad_instance.callback_function = self.set_access

    def click1(self):
        App.global_controller.frames["Frame8"].tree.insert("", tk.END, values=(
            datetime.now().strftime("%d.%m.%Y"), datetime.now().strftime("%H:%M:%S"), self.label1.cget('text'),
            f"{self.min_f_value.cget('text')} -> {App.numpad_instance.current_value}", "PumpParametersInGeneral"))
        App.global_controller.frames["Frame11"].min_f_value.config(text=App.numpad_instance.current_value)
        json_methods.save_data(App.file_path, App.global_controller.frames["Frame8"].save_journal_data())

    def click2(self):
        App.global_controller.frames["Frame8"].tree.insert("", tk.END, values=(
            datetime.now().strftime("%d.%m.%Y"), datetime.now().strftime("%H:%M:%S"), self.label2.cget('text'),
            f"{self.max_f_value.cget('text')} -> {App.numpad_instance.current_value}", "PumpParametersInGeneral"))
        App.global_controller.frames["Frame11"].max_f_value.config(text=App.numpad_instance.current_value)
        json_methods.save_data(App.file_path, App.global_controller.frames["Frame8"].save_journal_data())

    def click3(self):
        App.global_controller.frames["Frame8"].tree.insert("", tk.END, values=(
            datetime.now().strftime("%d.%m.%Y"), datetime.now().strftime("%H:%M:%S"), self.label5.cget('text'),
            f"{self.interval_value.cget('text')} -> {App.numpad_instance.current_value}", "PumpParametersInGeneral"))
        App.global_controller.frames["Frame11"].interval_value.config(text=App.numpad_instance.current_value)
        json_methods.save_data(App.file_path, App.global_controller.frames["Frame8"].save_journal_data())

    def click4(self):
        App.global_controller.frames["Frame8"].tree.insert("", tk.END, values=(
            datetime.now().strftime("%d.%m.%Y"), datetime.now().strftime("%H:%M:%S"), self.label6.cget('text'),
            f"{self.time_value.cget('text')} -> {App.numpad_instance.current_value}", "PumpParametersInGeneral"))
        App.global_controller.frames["Frame11"].time_value.config(text=App.numpad_instance.current_value)
        json_methods.save_data(App.file_path, App.global_controller.frames["Frame8"].save_journal_data())


    def set_access(self, event=None):
        print("set_access")
        App.session_access = True
        App.LVL_access = self.keypad_instance.access
        App.shields_hide()
        if App.LVL_access > 5:
            messagebox.showerror("Ошибка!", "Недостаточно прав!")

    def update_switch_first(self):
        if self.Switch_Flat_first_img.cget("file") ==  r"new_images/Switch-0.png":
            App.global_controller.frames["Frame8"].tree.insert("", tk.END, values=(
                datetime.now().strftime("%d.%m.%Y"), datetime.now().strftime("%H:%M:%S"), self.label3.cget('text'),
                f"OFF -> ON", "PumpParametersInGeneral"))
            self.Switch_Flat_first_img = PhotoImage(file=r"new_images/Switch-1.png")
            App.storage_data["Start_The_Master"] = "1"
            json_methods.save_data(App.file_path, App.global_controller.frames["Frame8"].save_journal_data())
        elif self.Switch_Flat_first_img.cget("file") == r"new_images/Switch-1.png":
            App.global_controller.frames["Frame8"].tree.insert("", tk.END, values=(
                datetime.now().strftime("%d.%m.%Y"), datetime.now().strftime("%H:%M:%S"), self.label3.cget('text'),
                f"ON -> OFF", "PumpParametersInGeneral"))
            self.Switch_Flat_first_img = PhotoImage(file=r"new_images/Switch-0.png")
            App.storage_data["Start_The_Master"] = "0"
            json_methods.save_data(App.file_path, App.global_controller.frames["Frame8"].save_journal_data())
        self.Switch_Flat_first_button = self.canvas.create_image(670, 152, image=self.Switch_Flat_first_img)
        self.canvas.tag_bind(self.Switch_Flat_first_button, "<Button-1>", lambda event: self.check_password("switch1"))

    def update_switch_second(self):
        if self.Switch_Flat_second_img.cget("file") == r"new_images/Switch-0.png":
            App.global_controller.frames["Frame8"].tree.insert("", tk.END, values=(
                datetime.now().strftime("%d.%m.%Y"), datetime.now().strftime("%H:%M:%S"), self.label4.cget('text'),
                f"OFF -> ON", "PumpParametersInGeneral"))
            self.Switch_Flat_second_img = PhotoImage(file=r"new_images/Switch-1.png")
            App.storage_data["Pump_Rotation"] = "1"
            json_methods.save_data(App.file_path, App.global_controller.frames["Frame8"].save_journal_data())
        elif self.Switch_Flat_second_img.cget("file") == r"new_images/Switch-1.png":
            App.global_controller.frames["Frame8"].tree.insert("", tk.END, values=(
                datetime.now().strftime("%d.%m.%Y"), datetime.now().strftime("%H:%M:%S"), self.label4.cget('text'),
                f"ON -> OFF", "PumpParametersInGeneral"))
            self.Switch_Flat_second_img = PhotoImage(file=r"new_images/Switch-0.png")
            App.storage_data["Pump_Rotation"] = "0"
            json_methods.save_data(App.file_path, App.global_controller.frames["Frame8"].save_journal_data())
        self.Switch_Flat_second_button = self.canvas.create_image(670, 194, image=self.Switch_Flat_second_img)
        self.canvas.tag_bind(self.Switch_Flat_second_button, "<Button-1>", lambda event: self.check_password("switch2"))
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
        self.img_screen = Image.open(r"new_images/screen.png")
        self.img_left = Image.open(r"new_images/left.png")
        self.img_triangle = Image.open(r"new_images/triangle.png")
        self.img_diode = Image.open(r"new_images/diode.png")
        self.img_swap = Image.open(r"new_images/swap.png")
        self.img_plusone = Image.open(r"new_images/plus_one.png")
        self.img_minusone = Image.open(r"new_images/minus_one.png")
        self.img_options = Image.open(r"new_images/options.png")
        self.img_emergency = Image.open(r"new_images/warning.png")

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

        self.img_frequency = PhotoImage(file=f"new_images/frequency.png")
        self.img_completed = PhotoImage(file=f"new_images/completed.png")
        self.img_interval = PhotoImage(file=f"new_images/interval.png")
        self.img_emergency = PhotoImage(file=f"new_images/warning.png")
        self.img_time = PhotoImage(file=f"new_images/time.png")
        self.img_shield = PhotoImage(file=f"new_images/shield.png")
        self.img_rectangle_l = PhotoImage(file=f"new_images/rectangle_long.png")

        self.canvas.create_image(233, 68, image=self.img_frequency)
        self.canvas.create_image(233, 144, image=self.img_completed)
        self.canvas.create_image(233, 176, image=self.img_interval)
        self.canvas.create_image(233, 245.375, image=self.img_emergency)
        self.canvas.create_image(233, 283, image=self.img_interval)
        self.canvas.create_image(233, 346, image=self.img_interval)
        self.canvas.create_image(233, 387, image=self.img_frequency)
        self.canvas.create_image(232.995, 427.995, image=self.img_time)

        self.shield1 = self.canvas.create_image(624, 69, image=self.img_shield)
        self.shield2 = self.canvas.create_image(624, 144, image=self.img_shield)
        self.shield3 = self.canvas.create_image(624, 183, image=self.img_shield)
        self.shield4 = self.canvas.create_image(624, 246, image=self.img_shield)
        self.shield5 = self.canvas.create_image(624, 285, image=self.img_shield)
        self.shield6 = self.canvas.create_image(624, 348, image=self.img_shield)
        self.shield7 = self.canvas.create_image(624, 387, image=self.img_shield)
        self.shield8 = self.canvas.create_image(624, 426, image=self.img_shield)

        self.canvas.create_line(215, 101, 795, 101, fill="gray", width=1)
        self.canvas.create_line(215, 209, 795, 209, fill="gray", width=1)
        self.canvas.create_line(215, 310, 795, 310, fill="gray", width=1)

        self.label1 = tk.Label(self.canvas, text="Частота мастера на включение доп. насоса",
                               fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label1.place(x=259, y=60)
        self.label2 = tk.Label(self.canvas, text="Включение при допустимой просадке",
                               fg='white', bg='black',
                               font=('Roboto Bold', 10))
        self.label2.place(x=213, y=103)
        self.label3 = tk.Label(self.canvas, text="Допустимая просадка (Пуск доп.насоса)",
                               fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label3.place(x=259, y=134)
        self.label4 = tk.Label(self.canvas, text="Задержка включения",
                               fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label4.place(x=259, y=167)
        self.label5 = tk.Label(self.canvas, text="Включение при критической просадке",
                               fg='white', bg='black',
                               font=('Roboto Bold', 10))
        self.label5.place(x=213, y=210)
        self.label6 = tk.Label(self.canvas, text="Критическая просадка (Пуск доп. насоса)",
                               fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label6.place(x=259, y=236)
        self.label7 = tk.Label(self.canvas, text="Задержка включения",
                               fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label7.place(x=259, y=273)
        self.label8 = tk.Label(self.canvas, text="Параметры работы мастера при включении доп. насоса",
                               fg='white', bg='black',
                               font=('Roboto Bold', 10))
        self.label8.place(x=213, y=312)
        self.label9 = tk.Label(self.canvas, text="Задержка ухода на фиксированную частоту",
                               fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label9.place(x=259, y=337)
        self.label10 = tk.Label(self.canvas, text="Фиксированная частота",
                               fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label10.place(x=259, y=378)
        self.label11 = tk.Label(self.canvas, text="Время работы на фиксированной частоте",
                               fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label11.place(x=259, y=418)

        # Кликабельная зона
        self.rectangle_master_f_on = self.canvas.create_image(718, 70, image=self.img_rectangle_l)
        self.master_f_on_value = tk.Label(self.canvas, text=App.storage_data["Frequency_Master_Enabled"],
                                    fg='white', bg='black',
                                    font=('Roboto Bold', 12))
        self.master_f_on_value.place(x=649, y=60)
        self.master_f_on_label = tk.Label(self.canvas, text="Гц",
                                    fg='white', bg='black',
                                    font=('Roboto Bold', 12))
        self.master_f_on_label.place(x=759, y=60)

        self.rectangle_acceptable_drawdown = self.canvas.create_image(718, 145, image=self.img_rectangle_l)
        self.acceptable_drawdown_value = tk.Label(self.canvas, text=App.storage_data["Acceptable_Drawdown_Start"],
                                       fg='white', bg='black',
                                       font=('Roboto Bold', 12))
        self.acceptable_drawdown_value.place(x=649, y=135)
        self.acceptable_drawdown_label = tk.Label(self.canvas, text="Бар",
                                       fg='white', bg='black',
                                       font=('Roboto Bold', 12))
        self.acceptable_drawdown_label.place(x=756, y=135)
        self.rectangle_acceptable_сooldown_on = self.canvas.create_image(718, 185, image=self.img_rectangle_l)
        self.acceptable_сooldown_on_value = tk.Label(self.canvas, text=App.storage_data["Power_Delay_One"],
                                                  fg='white', bg='black',
                                                  font=('Roboto Bold', 12))
        self.acceptable_сooldown_on_value.place(x=649, y=175)
        self.acceptable_сooldown_on_label = tk.Label(self.canvas, text="Сек",
                                                  fg='white', bg='black',
                                                  font=('Roboto Bold', 12))
        self.acceptable_сooldown_on_label.place(x=756, y=175)

        self.rectangle_crit_drawdown = self.canvas.create_image(718, 245, image=self.img_rectangle_l)
        self.crit_drawdown_value = tk.Label(self.canvas, text=App.storage_data["Critical_Drawdown_Start"],
                                                  fg='white', bg='black',
                                                  font=('Roboto Bold', 12))
        self.crit_drawdown_value.place(x=649, y=235)
        self.crit_drawdown_label = tk.Label(self.canvas, text="Бар",
                                                  fg='white', bg='black',
                                                  font=('Roboto Bold', 12))
        self.crit_drawdown_label.place(x=756, y=235)
        self.rectangle_crit_сooldown_on = self.canvas.create_image(718, 285, image=self.img_rectangle_l)
        self.crit_сooldown_on_value = tk.Label(self.canvas, text=App.storage_data["Power_Delay_Two"],
                                          fg='white', bg='black',
                                          font=('Roboto Bold', 12))
        self.crit_сooldown_on_value.place(x=649, y=275)
        self.crit_сooldown_on_label = tk.Label(self.canvas, text="Сек",
                                          fg='white', bg='black',
                                          font=('Roboto Bold', 12))
        self.crit_сooldown_on_label.place(x=756, y=275)

        self.rectangle_fix_сooldown_on = self.canvas.create_image(718, 347, image=self.img_rectangle_l)
        self.fix_сooldown_on_value = tk.Label(self.canvas, text=App.storage_data["Delayed_Care_One"],
                                               fg='white', bg='black',
                                               font=('Roboto Bold', 12))
        self.fix_сooldown_on_value.place(x=649, y=337)
        self.fix_сooldown_on_label = tk.Label(self.canvas, text="Сек",
                                               fg='white', bg='black',
                                               font=('Roboto Bold', 12))
        self.fix_сooldown_on_label.place(x=756, y=337)
        self.rectangle_fix_f_on = self.canvas.create_image(718, 386, image=self.img_rectangle_l)
        self.fix_f_on_value = tk.Label(self.canvas, text=App.storage_data["Fixed_Frequency_One"],
                                              fg='white', bg='black',
                                              font=('Roboto Bold', 12))
        self.fix_f_on_value.place(x=649, y=376)
        self.fix_f_on_label = tk.Label(self.canvas, text="Гц",
                                              fg='white', bg='black',
                                              font=('Roboto Bold', 12))
        self.fix_f_on_label.place(x=759, y=376)
        self.rectangle_time_work_on = self.canvas.create_image(718, 424, image=self.img_rectangle_l)
        self.time_work_on_value = tk.Label(self.canvas, text=App.storage_data["Working_Hours_One"],
                                       fg='white', bg='black',
                                       font=('Roboto Bold', 12))
        self.time_work_on_value.place(x=649, y=414)
        self.time_work_on_label = tk.Label(self.canvas, text="Сек",
                                       fg='white', bg='black',
                                       font=('Roboto Bold', 12))
        self.time_work_on_label.place(x=756, y=414)
        self.canvas.tag_bind(self.rectangle_master_f_on, "<Button-1>", lambda event: self.check_password("click1"))
        self.master_f_on_value.bind("<Button-1>", lambda event: self.check_password("click1"))
        self.master_f_on_label.bind("<Button-1>", lambda event: self.check_password("click1"))
        self.canvas.tag_bind(self.rectangle_acceptable_drawdown, "<Button-1>", lambda event: self.check_password("click2"))
        self.acceptable_drawdown_value.bind("<Button-1>", lambda event: self.check_password("click2"))
        self.acceptable_drawdown_label.bind("<Button-1>", lambda event: self.check_password("click2"))
        self.canvas.tag_bind(self.rectangle_acceptable_сooldown_on, "<Button-1>", lambda event: self.check_password("click3"))
        self.acceptable_сooldown_on_value.bind("<Button-1>", lambda event: self.check_password("click3"))
        self.acceptable_сooldown_on_label.bind("<Button-1>", lambda event: self.check_password("click3"))
        self.canvas.tag_bind(self.rectangle_crit_drawdown, "<Button-1>", lambda event: self.check_password("click4"))
        self.crit_drawdown_value.bind("<Button-1>", lambda event: self.check_password("click4"))
        self.crit_drawdown_label.bind("<Button-1>", lambda event: self.check_password("click4"))
        self.canvas.tag_bind(self.rectangle_crit_сooldown_on, "<Button-1>",lambda event: self.check_password("click5"))
        self.crit_сooldown_on_value.bind("<Button-1>", lambda event: self.check_password("click5"))
        self.crit_сooldown_on_label.bind("<Button-1>", lambda event: self.check_password("click5"))
        self.canvas.tag_bind(self.rectangle_fix_сooldown_on, "<Button-1>", lambda event: self.check_password("click6"))
        self.fix_сooldown_on_value.bind("<Button-1>", lambda event: self.check_password("click6"))
        self.fix_сooldown_on_label.bind("<Button-1>", lambda event: self.check_password("click6"))
        self.canvas.tag_bind(self.rectangle_fix_f_on, "<Button-1>", lambda event: self.check_password("click7"))
        self.fix_f_on_value.bind("<Button-1>", lambda event: self.check_password("click7"))
        self.fix_f_on_label.bind("<Button-1>", lambda event: self.check_password("click7"))
        self.canvas.tag_bind(self.rectangle_time_work_on, "<Button-1>", lambda event: self.check_password("click8"))
        self.time_work_on_value.bind("<Button-1>", lambda event: self.check_password("click8"))
        self.time_work_on_label.bind("<Button-1>", lambda event: self.check_password("click8"))
        # Кликабельная зона

    def check_password(self, word):
        print("check_password")
        if App.session_access == True:
            if App.LVL_access <= 5:
                App.global_controller.frames["Frame8"].update_tree(datetime.now().strftime("%d.%m.%Y"))
                if word == "click1":
                    App.numpad_instance = numpad.Numpad(None, "FLOAT1")
                    App.numpad_instance.min_value.config(text="35.0")
                    App.numpad_instance.max_value.config(text="50.0")
                    App.numpad_instance.new_title(self.label1.cget('text') + " ")
                    App.numpad_instance.entry_label.config(text=self.master_f_on_value.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click1
                elif word == "click2":
                    App.numpad_instance = numpad.Numpad(None, "FLOAT2")
                    App.numpad_instance.min_value.config(text="0.00")
                    App.numpad_instance.max_value.config(text="5.00")
                    App.numpad_instance.new_title(self.label3.cget('text') + " ")
                    App.numpad_instance.entry_label.config(text=self.acceptable_drawdown_value.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click2
                elif word == "click3":
                    App.numpad_instance = numpad.Numpad(None, "INT")
                    App.numpad_instance.min_value.config(text="0")
                    App.numpad_instance.max_value.config(text="30")
                    App.numpad_instance.new_title(self.label4.cget('text') + " (Допустимая просадка) ")
                    App.numpad_instance.entry_label.config(text=self.acceptable_сooldown_on_value.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click3
                elif word == "click4":
                    App.numpad_instance = numpad.Numpad(None, "FLOAT2")
                    App.numpad_instance.min_value.config(text="0.00")
                    App.numpad_instance.max_value.config(text="5.00")
                    App.numpad_instance.new_title(self.label6.cget('text') + " ")
                    App.numpad_instance.entry_label.config(text=self.crit_drawdown_value.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click4
                elif word == "click5":
                    App.numpad_instance = numpad.Numpad(None, "INT")
                    App.numpad_instance.min_value.config(text="0")
                    App.numpad_instance.max_value.config(text="30")
                    App.numpad_instance.new_title(self.label7.cget('text') + " (Критическая просадка) ")
                    App.numpad_instance.entry_label.config(text=self.crit_сooldown_on_value.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click5
                elif word == "click6":
                    App.numpad_instance = numpad.Numpad(None, "FLOAT1")
                    App.numpad_instance.min_value.config(text="0.0")
                    App.numpad_instance.max_value.config(text="9.9")
                    App.numpad_instance.new_title(self.label9.cget('text') + " ")
                    App.numpad_instance.entry_label.config(text=self.fix_сooldown_on_value.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click6
                elif word == "click7":
                    App.numpad_instance = numpad.Numpad(None, "FLOAT1")
                    App.numpad_instance.min_value.config(text="0.0")
                    App.numpad_instance.max_value.config(text="50.0")
                    App.numpad_instance.new_title(self.label10.cget('text') + " ")
                    App.numpad_instance.entry_label.config(text=self.fix_f_on_value.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click7
                elif word == "click8":
                    App.numpad_instance = numpad.Numpad(None, "INT")
                    App.numpad_instance.min_value.config(text="0")
                    App.numpad_instance.max_value.config(text="30")
                    App.numpad_instance.new_title(self.label11.cget('text') + " ")
                    App.numpad_instance.entry_label.config(text=self.time_work_on_value.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click8
                json_methods.save_data(r"data/desktop_storage.json", App.storage_data)
            else:
                messagebox.showerror("Ошибка!", "Недостаточно прав!")
        else:
            self.keypad_instance = keypad.Keypad()
            self.keypad_instance.grab_set()
            self.keypad_instance.callback_function = self.set_access

    def click1(self):
        App.global_controller.frames["Frame8"].tree.insert("", tk.END, values=(
            datetime.now().strftime("%d.%m.%Y"), datetime.now().strftime("%H:%M:%S"), self.label1.cget('text'),
            f"{self.master_f_on_value.cget('text')} -> {App.numpad_instance.current_value}", "OnAdditionalPumps"))
        App.global_controller.frames["Frame12"].master_f_on_value.config(text=App.numpad_instance.current_value)
        App.storage_data["Frequency_Master_Enabled"] = App.numpad_instance.current_value
        json_methods.save_data(App.file_path, App.global_controller.frames["Frame8"].save_journal_data())

    def click2(self):
        App.global_controller.frames["Frame8"].tree.insert("", tk.END, values=(
            datetime.now().strftime("%d.%m.%Y"), datetime.now().strftime("%H:%M:%S"), self.label3.cget('text'),
            f"{self.acceptable_drawdown_value.cget('text')} -> {App.numpad_instance.current_value}", "OnAdditionalPumps"))
        App.global_controller.frames["Frame12"].acceptable_drawdown_value.config(text=App.numpad_instance.current_value)
        App.storage_data["Acceptable_Drawdown_Start"] = App.numpad_instance.current_value
        json_methods.save_data(App.file_path, App.global_controller.frames["Frame8"].save_journal_data())

    def click3(self):
        App.global_controller.frames["Frame8"].tree.insert("", tk.END, values=(
            datetime.now().strftime("%d.%m.%Y"), datetime.now().strftime("%H:%M:%S"), self.label4.cget('text'),
            f"{self.acceptable_сooldown_on_value.cget('text')} -> {App.numpad_instance.current_value}", "OnAdditionalPumps"))
        App.global_controller.frames["Frame12"].acceptable_сooldown_on_value.config(text=App.numpad_instance.current_value)
        App.storage_data["Power_Delay_One"] = App.numpad_instance.current_value
        json_methods.save_data(App.file_path, App.global_controller.frames["Frame8"].save_journal_data())

    def click4(self):
        App.global_controller.frames["Frame8"].tree.insert("", tk.END, values=(
            datetime.now().strftime("%d.%m.%Y"), datetime.now().strftime("%H:%M:%S"), self.label6.cget('text'),
            f"{self.crit_drawdown_value.cget('text')} -> {App.numpad_instance.current_value}", "OnAdditionalPumps"))
        App.global_controller.frames["Frame12"].crit_drawdown_value.config(text=App.numpad_instance.current_value)
        App.storage_data["Critical_Drawdown_Start"] = App.numpad_instance.current_value
        json_methods.save_data(App.file_path, App.global_controller.frames["Frame8"].save_journal_data())

    def click5(self):
        App.global_controller.frames["Frame8"].tree.insert("", tk.END, values=(
            datetime.now().strftime("%d.%m.%Y"), datetime.now().strftime("%H:%M:%S"), self.label7.cget('text'),
            f"{self.crit_сooldown_on_value.cget('text')} -> {App.numpad_instance.current_value}", "OnAdditionalPumps"))
        App.global_controller.frames["Frame12"].crit_сooldown_on_value.config(text=App.numpad_instance.current_value)
        App.storage_data["Power_Delay_Two"] = App.numpad_instance.current_value
        json_methods.save_data(App.file_path, App.global_controller.frames["Frame8"].save_journal_data())

    def click6(self):
        App.global_controller.frames["Frame8"].tree.insert("", tk.END, values=(
            datetime.now().strftime("%d.%m.%Y"), datetime.now().strftime("%H:%M:%S"), self.label9.cget('text'),
            f"{self.fix_сooldown_on_value.cget('text')} -> {App.numpad_instance.current_value}", "OnAdditionalPumps"))
        App.global_controller.frames["Frame12"].fix_сooldown_on_value.config(text=App.numpad_instance.current_value)
        App.storage_data["Delayed_Care_One"] = App.numpad_instance.current_value
        json_methods.save_data(App.file_path, App.global_controller.frames["Frame8"].save_journal_data())

    def click7(self):
        App.global_controller.frames["Frame8"].tree.insert("", tk.END, values=(
            datetime.now().strftime("%d.%m.%Y"), datetime.now().strftime("%H:%M:%S"), self.label10.cget('text'),
            f"{self.fix_f_on_value.cget('text')} -> {App.numpad_instance.current_value}", "OnAdditionalPumps"))
        App.global_controller.frames["Frame12"].fix_f_on_value.config(text=App.numpad_instance.current_value)
        App.storage_data["Fixed_Frequency_One"] = App.numpad_instance.current_value
        json_methods.save_data(App.file_path, App.global_controller.frames["Frame8"].save_journal_data())

    def click8(self):
        App.global_controller.frames["Frame8"].tree.insert("", tk.END, values=(
            datetime.now().strftime("%d.%m.%Y"), datetime.now().strftime("%H:%M:%S"), self.label11.cget('text'),
            f"{self.time_work_on_value.cget('text')} -> {App.numpad_instance.current_value}", "OnAdditionalPumps"))
        App.global_controller.frames["Frame12"].time_work_on_value.config(text=App.numpad_instance.current_value)
        App.storage_data["Working_Hours_One"] = App.numpad_instance.current_value
        json_methods.save_data(App.file_path, App.global_controller.frames["Frame8"].save_journal_data())

    def set_access(self, event=None):
        print("set_access")
        App.session_access = True
        App.LVL_access = self.keypad_instance.access
        App.shields_hide()
        if App.LVL_access > 5:
            messagebox.showerror("Ошибка!", "Недостаточно прав!")

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
        self.img_screen = Image.open(r"new_images/screen.png")
        self.img_left = Image.open(r"new_images/left.png")
        self.img_triangle = Image.open(r"new_images/triangle.png")
        self.img_diode = Image.open(r"new_images/diode.png")
        self.img_swap = Image.open(r"new_images/swap.png")
        self.img_plusone = Image.open(r"new_images/plus_one.png")
        self.img_minusone = Image.open(r"new_images/minus_one.png")
        self.img_options = Image.open(r"new_images/options.png")
        self.img_emergency = Image.open(r"new_images/warning.png")

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

        self.img_frequency = PhotoImage(file=f"new_images/frequency.png")
        self.img_completed = PhotoImage(file=f"new_images/completed.png")
        self.img_interval = PhotoImage(file=f"new_images/interval.png")
        self.img_emergency = PhotoImage(file=f"new_images/warning.png")
        self.img_time = PhotoImage(file=f"new_images/time.png")
        self.img_shield = PhotoImage(file=f"new_images/shield.png")
        self.img_rectangle_l = PhotoImage(file=f"new_images/rectangle_long.png")

        self.canvas.create_image(233, 68, image=self.img_frequency)
        self.canvas.create_image(233, 144, image=self.img_completed)
        self.canvas.create_image(233, 176, image=self.img_interval)
        self.canvas.create_image(233, 245.375, image=self.img_emergency)
        self.canvas.create_image(233, 283, image=self.img_interval)
        self.canvas.create_image(233, 346, image=self.img_interval)
        self.canvas.create_image(233, 387, image=self.img_frequency)
        self.canvas.create_image(232.995, 427.995, image=self.img_time)

        self.shield1 = self.canvas.create_image(624, 69, image=self.img_shield)
        self.shield2 = self.canvas.create_image(624, 144, image=self.img_shield)
        self.shield3 = self.canvas.create_image(624, 183, image=self.img_shield)
        self.shield4 = self.canvas.create_image(624, 246, image=self.img_shield)
        self.shield5 = self.canvas.create_image(624, 285, image=self.img_shield)
        self.shield6 = self.canvas.create_image(624, 348, image=self.img_shield)
        self.shield7 = self.canvas.create_image(624, 387, image=self.img_shield)
        self.shield8 = self.canvas.create_image(624, 426, image=self.img_shield)

        self.canvas.create_line(215, 101, 795, 101, fill="gray", width=1)
        self.canvas.create_line(215, 209, 795, 209, fill="gray", width=1)
        self.canvas.create_line(215, 310, 795, 310, fill="gray", width=1)

        self.label1 = tk.Label(self.canvas, text="Частота мастера на отключение доп. насоса",
                               fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label1.place(x=259, y=60)
        self.label2 = tk.Label(self.canvas, text="Отключение при допустимом скаске",
                               fg='white', bg='black',
                               font=('Roboto Bold', 10))
        self.label2.place(x=213, y=103)
        self.label3 = tk.Label(self.canvas, text="Допустимый скачок (Стоп доп.насоса)",
                               fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label3.place(x=259, y=134)
        self.label4 = tk.Label(self.canvas, text="Задержка выключения",
                               fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label4.place(x=259, y=167)
        self.label5 = tk.Label(self.canvas, text="Выключение при критическом скачке",
                               fg='white', bg='black',
                               font=('Roboto Bold', 10))
        self.label5.place(x=213, y=210)
        self.label6 = tk.Label(self.canvas, text="Критический скачок (Стоп доп. насоса)",
                               fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label6.place(x=259, y=236)
        self.label7 = tk.Label(self.canvas, text="Задержка выключения",
                               fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label7.place(x=259, y=273)
        self.label8 = tk.Label(self.canvas, text="Параметры работы мастера при отключении доп. насоса",
                               fg='white', bg='black',
                               font=('Roboto Bold', 10))
        self.label8.place(x=213, y=312)
        self.label9 = tk.Label(self.canvas, text="Задержка ухода на фиксированную частоту",
                               fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label9.place(x=259, y=337)
        self.label10 = tk.Label(self.canvas, text="Фиксированная частота",
                                fg='white', bg='black',
                                font=('Roboto Bold', 12))
        self.label10.place(x=259, y=378)
        self.label11 = tk.Label(self.canvas, text="Время работы на фиксированной частоте",
                                fg='white', bg='black',
                                font=('Roboto Bold', 12))
        self.label11.place(x=259, y=418)

        # Кликабельная зона
        self.rectangle_master_f_off = self.canvas.create_image(718, 70, image=self.img_rectangle_l)
        self.master_f_off_value = tk.Label(self.canvas, text=App.storage_data["Frequency_Master_Shutdown"],
                                       fg='white', bg='black',
                                       font=('Roboto Bold', 12))
        self.master_f_off_value.place(x=649, y=60)
        self.master_f_off_label = tk.Label(self.canvas, text="Гц",
                                       fg='white', bg='black',
                                       font=('Roboto Bold', 12))
        self.master_f_off_label.place(x=759, y=60)

        self.rectangle_acceptable_jump = self.canvas.create_image(718, 145, image=self.img_rectangle_l)
        self.acceptable_jump_value = tk.Label(self.canvas, text=App.storage_data["Acceptable_Drawdown_Stop"],
                                                  fg='white', bg='black',
                                                  font=('Roboto Bold', 12))
        self.acceptable_jump_value.place(x=649, y=135)
        self.acceptable_jump_label = tk.Label(self.canvas, text="Бар",
                                                  fg='white', bg='black',
                                                  font=('Roboto Bold', 12))
        self.acceptable_jump_label.place(x=756, y=135)
        self.rectangle_acceptable_сooldown_off = self.canvas.create_image(718, 185, image=self.img_rectangle_l)
        self.acceptable_сooldown_off_value = tk.Label(self.canvas, text=App.storage_data["Shutdown_Delay_One"],
                                                     fg='white', bg='black',
                                                     font=('Roboto Bold', 12))
        self.acceptable_сooldown_off_value.place(x=649, y=175)
        self.acceptable_сooldown_off_label = tk.Label(self.canvas, text="Сек",
                                                     fg='white', bg='black',
                                                     font=('Roboto Bold', 12))
        self.acceptable_сooldown_off_label.place(x=756, y=175)

        self.rectangle_crit_jump = self.canvas.create_image(718, 245, image=self.img_rectangle_l)
        self.crit_jump_value = tk.Label(self.canvas, text=App.storage_data["Critical_Drawdown_Stop"],
                                            fg='white', bg='black',
                                            font=('Roboto Bold', 12))
        self.crit_jump_value.place(x=649, y=235)
        self.crit_jump_label = tk.Label(self.canvas, text="Бар",
                                            fg='white', bg='black',
                                            font=('Roboto Bold', 12))
        self.crit_jump_label.place(x=756, y=235)
        self.rectangle_crit_сooldown_off = self.canvas.create_image(718, 285, image=self.img_rectangle_l)
        self.crit_сooldown_off_value = tk.Label(self.canvas, text=App.storage_data["Shutdown_Delay_Two"],
                                               fg='white', bg='black',
                                               font=('Roboto Bold', 12))
        self.crit_сooldown_off_value.place(x=649, y=275)
        self.crit_сooldown_off_label = tk.Label(self.canvas, text="Сек",
                                               fg='white', bg='black',
                                               font=('Roboto Bold', 12))
        self.crit_сooldown_off_label.place(x=756, y=275)

        self.rectangle_fix_сooldown_off = self.canvas.create_image(718, 347, image=self.img_rectangle_l)
        self.fix_сooldown_off_value = tk.Label(self.canvas, text=App.storage_data["Delayed_Care_Two"],
                                              fg='white', bg='black',
                                              font=('Roboto Bold', 12))
        self.fix_сooldown_off_value.place(x=649, y=337)
        self.fix_сooldown_off_label = tk.Label(self.canvas, text="Сек",
                                              fg='white', bg='black',
                                              font=('Roboto Bold', 12))
        self.fix_сooldown_off_label.place(x=756, y=337)
        self.rectangle_fix_f_off = self.canvas.create_image(718, 386, image=self.img_rectangle_l)
        self.fix_f_off_value = tk.Label(self.canvas, text=App.storage_data["Fixed_Frequency_Two"],
                                       fg='white', bg='black',
                                       font=('Roboto Bold', 12))
        self.fix_f_off_value.place(x=649, y=376)
        self.fix_f_off_label = tk.Label(self.canvas, text="Гц",
                                       fg='white', bg='black',
                                       font=('Roboto Bold', 12))
        self.fix_f_off_label.place(x=759, y=376)
        self.rectangle_time_work_off = self.canvas.create_image(718, 424, image=self.img_rectangle_l)
        self.time_work_off_value = tk.Label(self.canvas, text=App.storage_data["Working_Hours_Two"],
                                           fg='white', bg='black',
                                           font=('Roboto Bold', 12))
        self.time_work_off_value.place(x=649, y=414)
        self.time_work_off_label = tk.Label(self.canvas, text="Сек",
                                           fg='white', bg='black',
                                           font=('Roboto Bold', 12))
        self.time_work_off_label.place(x=756, y=414)
        self.canvas.tag_bind(self.rectangle_master_f_off, "<Button-1>", lambda event: self.check_password("click1"))
        self.master_f_off_value.bind("<Button-1>", lambda event: self.check_password("click1"))
        self.master_f_off_label.bind("<Button-1>", lambda event: self.check_password("click1"))
        self.canvas.tag_bind(self.rectangle_acceptable_jump, "<Button-1>", lambda event: self.check_password("click2"))
        self.acceptable_jump_value.bind("<Button-1>", lambda event: self.check_password("click2"))
        self.acceptable_jump_label.bind("<Button-1>", lambda event: self.check_password("click2"))
        self.canvas.tag_bind(self.rectangle_acceptable_сooldown_off, "<Button-1>", lambda event: self.check_password("click3"))
        self.acceptable_сooldown_off_value.bind("<Button-1>", lambda event: self.check_password("click3"))
        self.acceptable_сooldown_off_label.bind("<Button-1>", lambda event: self.check_password("click3"))
        self.canvas.tag_bind(self.rectangle_crit_jump, "<Button-1>", lambda event: self.check_password("click4"))
        self.crit_jump_value.bind("<Button-1>", lambda event: self.check_password("click4"))
        self.crit_jump_label.bind("<Button-1>", lambda event: self.check_password("click4"))
        self.canvas.tag_bind(self.rectangle_crit_сooldown_off, "<Button-1>", lambda event: self.check_password("click5"))
        self.crit_сooldown_off_value.bind("<Button-1>", lambda event: self.check_password("click5"))
        self.crit_сooldown_off_label.bind("<Button-1>", lambda event: self.check_password("click5"))
        self.canvas.tag_bind(self.rectangle_fix_сooldown_off, "<Button-1>", lambda event: self.check_password("click6"))
        self.fix_сooldown_off_value.bind("<Button-1>", lambda event: self.check_password("click6"))
        self.fix_сooldown_off_label.bind("<Button-1>", lambda event: self.check_password("click6"))
        self.canvas.tag_bind(self.rectangle_fix_f_off, "<Button-1>", lambda event: self.check_password("click7"))
        self.fix_f_off_value.bind("<Button-1>", lambda event: self.check_password("click7"))
        self.fix_f_off_label.bind("<Button-1>", lambda event: self.check_password("click7"))
        self.canvas.tag_bind(self.rectangle_time_work_off, "<Button-1>", lambda event: self.check_password("click8"))
        self.time_work_off_value.bind("<Button-1>", lambda event: self.check_password("click8"))
        self.time_work_off_label.bind("<Button-1>", lambda event: self.check_password("click8"))
        # Кликабельная зона
    def check_password(self, word):
        print("check_password")
        if App.session_access == True:
            if App.LVL_access <= 5:
                App.global_controller.frames["Frame8"].update_tree(datetime.now().strftime("%d.%m.%Y"))
                if word == "click1":
                    App.numpad_instance = numpad.Numpad(None, "FLOAT1")
                    App.numpad_instance.min_value.config(text="35.0")
                    App.numpad_instance.max_value.config(text="50.0")
                    App.numpad_instance.new_title(self.label1.cget('text') + " ")
                    App.numpad_instance.entry_label.config(text=self.master_f_off_value.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click1
                elif word == "click2":
                    App.numpad_instance = numpad.Numpad(None, "FLOAT2")
                    App.numpad_instance.min_value.config(text="0.00")
                    App.numpad_instance.max_value.config(text="5.00")
                    App.numpad_instance.new_title(self.label3.cget('text') + " ")
                    App.numpad_instance.entry_label.config(text=self.acceptable_jump_value.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click2
                elif word == "click3":
                    App.numpad_instance = numpad.Numpad(None, "INT")
                    App.numpad_instance.min_value.config(text="0")
                    App.numpad_instance.max_value.config(text="30")
                    App.numpad_instance.new_title(self.label4.cget('text') + " (Допустимый скачок) ")
                    App.numpad_instance.entry_label.config(text=self.acceptable_сooldown_off_value.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click3
                elif word == "click4":
                    App.numpad_instance = numpad.Numpad(None, "FLOAT2")
                    App.numpad_instance.min_value.config(text="0.00")
                    App.numpad_instance.max_value.config(text="5.00")
                    App.numpad_instance.new_title(self.label6.cget('text') + " ")
                    App.numpad_instance.entry_label.config(text=self.crit_jump_value.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click4
                elif word == "click5":
                    App.numpad_instance = numpad.Numpad(None, "INT")
                    App.numpad_instance.min_value.config(text="0")
                    App.numpad_instance.max_value.config(text="30")
                    App.numpad_instance.new_title(self.label7.cget('text') + " (Критический скачок) ")
                    App.numpad_instance.entry_label.config(text=self.crit_сooldown_off_value.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click5
                elif word == "click6":
                    App.numpad_instance = numpad.Numpad(None, "FLOAT1")
                    App.numpad_instance.min_value.config(text="0.0")
                    App.numpad_instance.max_value.config(text="9.9")
                    App.numpad_instance.new_title(self.label9.cget('text') + " ")
                    App.numpad_instance.entry_label.config(text=self.fix_сooldown_off_value.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click6
                elif word == "click7":
                    App.numpad_instance = numpad.Numpad(None, "FLOAT1")
                    App.numpad_instance.min_value.config(text="0.0")
                    App.numpad_instance.max_value.config(text="50.0")
                    App.numpad_instance.new_title(self.label10.cget('text') + " ")
                    App.numpad_instance.entry_label.config(text=self.fix_f_off_value.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click7
                elif word == "click8":
                    App.numpad_instance = numpad.Numpad(None, "INT")
                    App.numpad_instance.min_value.config(text="0")
                    App.numpad_instance.max_value.config(text="30")
                    App.numpad_instance.new_title(self.label11.cget('text') + " ")
                    App.numpad_instance.entry_label.config(text=self.time_work_off_value.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click8
                json_methods.save_data(r"data/desktop_storage.json", App.storage_data)
            else:
                messagebox.showerror("Ошибка!", "Недостаточно прав!")
        else:
            self.keypad_instance = keypad.Keypad()
            self.keypad_instance.grab_set()
            self.keypad_instance.callback_function = self.set_access

    def click1(self):
        App.global_controller.frames["Frame8"].tree.insert("", tk.END, values=(
            datetime.now().strftime("%d.%m.%Y"), datetime.now().strftime("%H:%M:%S"), self.label1.cget('text'),
            f"{self.acceptable_jump_value.cget('text')} -> {App.numpad_instance.current_value}", "OffOfAdditionalPumps"))
        App.global_controller.frames["Frame13"].acceptable_jump_value.config(text=App.numpad_instance.current_value)
        App.storage_data["Frequency_Master_Shutdown"] = App.numpad_instance.current_value
        json_methods.save_data(App.file_path, App.global_controller.frames["Frame8"].save_journal_data())
    def click2(self):
        App.global_controller.frames["Frame8"].tree.insert("", tk.END, values=(
            datetime.now().strftime("%d.%m.%Y"), datetime.now().strftime("%H:%M:%S"), self.label3.cget('text'),
            f"{self.acceptable_сooldown_off_value.cget('text')} -> {App.numpad_instance.current_value}", "OffOfAdditionalPumps"))
        App.global_controller.frames["Frame13"].acceptable_сooldown_off_value.config(text=App.numpad_instance.current_value)
        App.storage_data["Acceptable_Drawdown_Stop"] = App.numpad_instance.current_value
        json_methods.save_data(App.file_path, App.global_controller.frames["Frame8"].save_journal_data())
    def click3(self):
        App.global_controller.frames["Frame8"].tree.insert("", tk.END, values=(
            datetime.now().strftime("%d.%m.%Y"), datetime.now().strftime("%H:%M:%S"), self.label4.cget('text'),
            f"{self.max_emergency_value.cget('text')} -> {App.numpad_instance.current_value}", "OffOfAdditionalPumps"))
        App.global_controller.frames["Frame13"].max_emergency_value.config(text=App.numpad_instance.current_value)
        App.storage_data["Shutdown_Delay_One"] = App.numpad_instance.current_value
        json_methods.save_data(App.file_path, App.global_controller.frames["Frame8"].save_journal_data())
    def click4(self):
        App.global_controller.frames["Frame8"].tree.insert("", tk.END, values=(
            datetime.now().strftime("%d.%m.%Y"), datetime.now().strftime("%H:%M:%S"), self.label6.cget('text'),
            f"{self.crit_jump_value.cget('text')} -> {App.numpad_instance.current_value}", "OffOfAdditionalPumps"))
        App.global_controller.frames["Frame13"].crit_jump_value.config(text=App.numpad_instance.current_value)
        App.storage_data["Critical_Drawdown_Stop"] = App.numpad_instance.current_value
        json_methods.save_data(App.file_path, App.global_controller.frames["Frame8"].save_journal_data())
    def click5(self):
        App.global_controller.frames["Frame8"].tree.insert("", tk.END, values=(
            datetime.now().strftime("%d.%m.%Y"), datetime.now().strftime("%H:%M:%S"), self.label7.cget('text'),
            f"{self.crit_сooldown_off_value.cget('text')} -> {App.numpad_instance.current_value}", "OffOfAdditionalPumps"))
        App.global_controller.frames["Frame13"].crit_сooldown_off_value.config(text=App.numpad_instance.current_value)
        App.storage_data["Shutdown_Delay_Two"] = App.numpad_instance.current_value
        json_methods.save_data(App.file_path, App.global_controller.frames["Frame8"].save_journal_data())

    def click6(self):
        App.global_controller.frames["Frame8"].tree.insert("", tk.END, values=(
            datetime.now().strftime("%d.%m.%Y"), datetime.now().strftime("%H:%M:%S"), self.label9.cget('text'),
            f"{self.fix_сooldown_off_value.cget('text')} -> {App.numpad_instance.current_value}", "OffOfAdditionalPumps"))
        App.global_controller.frames["Frame13"].fix_сooldown_off_value.config(text=App.numpad_instance.current_value)
        App.storage_data["Delayed_Care_Two"] = App.numpad_instance.current_value
        json_methods.save_data(App.file_path, App.global_controller.frames["Frame8"].save_journal_data())

    def click7(self):
        App.global_controller.frames["Frame8"].tree.insert("", tk.END, values=(
            datetime.now().strftime("%d.%m.%Y"), datetime.now().strftime("%H:%M:%S"), self.label10.cget('text'),
            f"{self.fix_f_off_value.cget('text')} -> {App.numpad_instance.current_value}", "OffOfAdditionalPumps"))
        App.global_controller.frames["Frame13"].fix_f_off_value.config(text=App.numpad_instance.current_value)
        App.storage_data["Fixed_Frequency_Two"] = App.numpad_instance.current_value
        json_methods.save_data(App.file_path, App.global_controller.frames["Frame8"].save_journal_data())

    def click8(self):
        App.global_controller.frames["Frame8"].tree.insert("", tk.END, values=(
            datetime.now().strftime("%d.%m.%Y"), datetime.now().strftime("%H:%M:%S"), self.label11.cget('text'),
            f"{self.time_work_off_value.cget('text')} -> {App.numpad_instance.current_value}", "OffOfAdditionalPumps"))
        App.global_controller.frames["Frame13"].time_work_off_value.config(text=App.numpad_instance.current_value)
        App.storage_data["Working_Hours_Two"] = App.numpad_instance.current_value
        json_methods.save_data(App.file_path, App.global_controller.frames["Frame8"].save_journal_data())

    def set_access(self, event=None):
        print("set_access")
        App.session_access = True
        App.LVL_access = self.keypad_instance.access
        App.shields_hide()
        if App.LVL_access > 5:
            messagebox.showerror("Ошибка!", "Недостаточно прав!")
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
        self.img_screen = Image.open(r"new_images/screen.png")
        self.img_left = Image.open(r"new_images/left.png")
        self.img_triangle = Image.open(r"new_images/triangle.png")
        self.img_diode = Image.open(r"new_images/diode.png")
        self.img_swap = Image.open(r"new_images/swap.png")
        self.img_plusone = Image.open(r"new_images/plus_one.png")
        self.img_minusone = Image.open(r"new_images/minus_one.png")
        self.img_options = Image.open(r"new_images/options.png")
        self.img_emergency = Image.open(r"new_images/warning.png")

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

        self.img_econom = PhotoImage(file=f"new_images/econom.png")
        self.img_interval = PhotoImage(file=f"new_images/interval.png")
        self.img_upper_pressure = PhotoImage(file=f"new_images/upper_pressure.png")
        self.img_lower_pressure = PhotoImage(file=f"new_images/lower_pressure.png")
        self.img_swing_time = PhotoImage(file=f"new_images/swing_time.png")
        self.img_acceptable_range= PhotoImage(file=f"new_images/acceptable_range.png")
        self.img_eye = PhotoImage(file=f"new_images/eye.png")
        self.img_shield = PhotoImage(file=f"new_images/shield.png")
        self.img_rectangle_l = PhotoImage(file=f"new_images/rectangle_long.png")

        self.canvas.create_image(232.995, 83.005, image=self.img_econom)
        self.canvas.create_image(233, 117, image=self.img_interval)
        self.canvas.create_image(233, 155, image=self.img_upper_pressure)
        self.canvas.create_image(233, 191, image=self.img_lower_pressure)
        self.canvas.create_image(233, 228, image=self.img_swing_time)
        self.canvas.create_image(233, 265, image=self.img_acceptable_range)
        self.canvas.create_image(233, 306, image=self.img_acceptable_range)
        self.canvas.create_image(233, 367.375, image=self.img_eye)
        self.canvas.create_image(233, 402.375, image=self.img_eye)
        self.canvas.create_image(233, 440.375, image=self.img_eye)

        self.shield1 = self.canvas.create_image(624, 83, image=self.img_shield)
        self.shield2 = self.canvas.create_image(624, 120, image=self.img_shield)
        self.shield3 = self.canvas.create_image(624, 157, image=self.img_shield)
        self.shield4 = self.canvas.create_image(624, 194, image=self.img_shield)
        self.shield5 = self.canvas.create_image(624, 231, image=self.img_shield)
        self.shield6 = self.canvas.create_image(624, 268, image=self.img_shield)
        self.shield7 = self.canvas.create_image(624, 305, image=self.img_shield)

        self.label1 = tk.Label(self.canvas, text="Параметры энергосбережения",
                               fg='white', bg='black',
                               font=('Roboto Bold', 10))
        self.label1.place(x=214, y=46)
        self.label2 = tk.Label(self.canvas, text="Режим энергосбережения",
                               fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label2.place(x=259, y=74)
        self.label3 = tk.Label(self.canvas, text="Запускать режим энергосбережения раз в",
                               fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label3.place(x=259, y=108)
        self.label4 = tk.Label(self.canvas, text="Просадка давления для выкл. энерг. сбер.",
                               fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label4.place(x=259, y=146)
        self.label5 = tk.Label(self.canvas, text="Повышать давление на",
                               fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label5.place(x=259, y=182)
        self.label6 = tk.Label(self.canvas, text="Время интегрирования размаха",
                               fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label6.place(x=259, y=220)
        self.label7 = tk.Label(self.canvas, text="Допустимый размах давления",
                               fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label7.place(x=259, y=256)
        self.label8 = tk.Label(self.canvas, text="Допустимый размах частоты",
                               fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label8.place(x=259, y=296)
        self.label9 = tk.Label(self.canvas, text="Параметры энергосбережения",
                               fg='white', bg='black',
                               font=('Roboto Bold', 10))
        self.label9.place(x=214, y=330)
        self.label10 = tk.Label(self.canvas, text="Текущий размах давления",
                               fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label10.place(x=259, y=358)
        self.label11 = tk.Label(self.canvas, text="Текущий размах частоты",
                               fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label11.place(x=259, y=392)
        self.label12 = tk.Label(self.canvas, text="Выход алгоритма энергосбережения",
                               fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label12.place(x=259, y=430)
        self.label13 = tk.Label(self.canvas, text="Бар",
                                fg='white', bg='black',
                                font=('Roboto Bold', 12))
        self.label13.place(x=754, y=354)
        self.label14 = tk.Label(self.canvas, text="Гц",
                                fg='white', bg='black',
                                font=('Roboto Bold', 12))
        self.label14.place(x=759, y=391)

        self.canvas.create_line(215, 45, 795, 45, fill="gray", width=1)
        self.canvas.create_line(215, 326, 795, 326, fill="gray", width=1)

        # Кликабельная зона
        self.Switch_Flat_img = PhotoImage(file=r"new_images/Switch-0.png") if App.storage_data["Power_Savingmode"] == "0" else PhotoImage(file=r"new_images/Switch-1.png")
        self.Switch_Flat_button = self.canvas.create_image(670, 78, image=self.Switch_Flat_img)
        self.canvas.tag_bind(self.Switch_Flat_button, "<Button-1>", lambda event: self.check_password("switch"))

        self.rectangle_start_mod = self.canvas.create_image(714, 115, image=self.img_rectangle_l)
        self.start_mod_value = tk.Label(self.canvas, text=App.storage_data["Starting_Power_Savingmode"],
                                fg='white', bg='black',
                                font=('Roboto Bold', 12))
        self.start_mod_value.place(x=645, y=105)
        self.start_mod_label = tk.Label(self.canvas, text="Сек",
                                fg='white', bg='black',
                                font=('Roboto Bold', 12))
        self.start_mod_label.place(x=754, y=105)
        self.rectangle_upper_pressure = self.canvas.create_image(714, 153, image=self.img_rectangle_l)
        self.upper_pressure_value = tk.Label(self.canvas, text=App.storage_data["Pressure_Drawdown"],
                                        fg='white', bg='black',
                                        font=('Roboto Bold', 12))
        self.upper_pressure_value.place(x=645, y=143)
        self.upper_pressure_label = tk.Label(self.canvas, text="Бар",
                                        fg='white', bg='black',
                                        font=('Roboto Bold', 12))
        self.upper_pressure_label.place(x=754, y=143)
        self.rectangle_lower_pressure = self.canvas.create_image(714, 191, image=self.img_rectangle_l)
        self.lower_pressure_value = tk.Label(self.canvas, text=App.storage_data["Pressure_Increase"],
                                             fg='white', bg='black',
                                             font=('Roboto Bold', 12))
        self.lower_pressure_value.place(x=645, y=181)
        self.lower_pressure_label = tk.Label(self.canvas, text="Бар",
                                             fg='white', bg='black',
                                             font=('Roboto Bold', 12))
        self.lower_pressure_label.place(x=754, y=181)
        self.rectangle_swing_time = self.canvas.create_image(714, 229, image=self.img_rectangle_l)
        self.swing_time_value = tk.Label(self.canvas, text=App.storage_data["Swing_Time"],
                                             fg='white', bg='black',
                                             font=('Roboto Bold', 12))
        self.swing_time_value.place(x=645, y=219)
        self.swing_time_label = tk.Label(self.canvas, text="Сек",
                                             fg='white', bg='black',
                                             font=('Roboto Bold', 12))
        self.swing_time_label.place(x=754, y=219)
        self.acceptable_range = self.canvas.create_image(714, 267, image=self.img_rectangle_l)
        self.acceptable_range_value = tk.Label(self.canvas, text=App.storage_data["Pressure_Range"],
                                         fg='white', bg='black',
                                         font=('Roboto Bold', 12))
        self.acceptable_range_value.place(x=645, y=257)
        self.acceptable_range_label = tk.Label(self.canvas, text="Бар",
                                         fg='white', bg='black',
                                         font=('Roboto Bold', 12))
        self.acceptable_range_label.place(x=754, y=257)
        self.acceptable_frequency = self.canvas.create_image(714, 305, image=self.img_rectangle_l)
        self.acceptable_frequency_value = tk.Label(self.canvas, text=App.storage_data["Frequency_Range"],
                                               fg='white', bg='black',
                                               font=('Roboto Bold', 12))
        self.acceptable_frequency_value.place(x=645, y=295)
        self.acceptable_frequency_label = tk.Label(self.canvas, text="Гц",
                                               fg='white', bg='black',
                                               font=('Roboto Bold', 12))
        self.acceptable_frequency_label.place(x=759, y=295)
        self.canvas.tag_bind(self.rectangle_start_mod, "<Button-1>", lambda event: self.check_password("click1"))
        self.start_mod_value.bind("<Button-1>", lambda event: self.check_password("click1"))
        self.start_mod_label.bind("<Button-1>", lambda event: self.check_password("click1"))
        self.canvas.tag_bind(self.rectangle_upper_pressure, "<Button-1>", lambda event: self.check_password("click2"))
        self.upper_pressure_value.bind("<Button-1>", lambda event: self.check_password("click2"))
        self.upper_pressure_label.bind("<Button-1>", lambda event: self.check_password("click2"))
        self.canvas.tag_bind(self.rectangle_lower_pressure, "<Button-1>", lambda event: self.check_password("click3"))
        self.lower_pressure_value.bind("<Button-1>", lambda event: self.check_password("click3"))
        self.lower_pressure_label.bind("<Button-1>", lambda event: self.check_password("click3"))
        self.canvas.tag_bind(self.rectangle_swing_time, "<Button-1>", lambda event: self.check_password("click4"))
        self.swing_time_value.bind("<Button-1>", lambda event: self.check_password("click4"))
        self.swing_time_label.bind("<Button-1>", lambda event: self.check_password("click4"))
        self.canvas.tag_bind(self.acceptable_range, "<Button-1>", lambda event: self.check_password("click5"))
        self.acceptable_range_value.bind("<Button-1>", lambda event: self.check_password("click5"))
        self.acceptable_range_label.bind("<Button-1>", lambda event: self.check_password("click5"))
        self.canvas.tag_bind(self.acceptable_frequency, "<Button-1>", lambda event: self.check_password("click6"))
        self.acceptable_frequency_value.bind("<Button-1>", lambda event: self.check_password("click6"))
        self.acceptable_frequency_label.bind("<Button-1>", lambda event: self.check_password("click6"))
        # Кликабельная зона

        self.current_swing_pressure = tk.Label(self.canvas, text="0.00",
                                                fg='white', bg='black',
                                                font=('Roboto Bold', 12))
        self.current_swing_pressure.place(x=645, y=354)
        self.current_swing_frequency = tk.Label(self.canvas, text="0.0",
                                                   fg='white', bg='black',
                                                   font=('Roboto Bold', 12))
        self.current_swing_frequency.place(x=645, y=391)
        self.out_alg = tk.Label(self.canvas, text="0",
                                                fg='white', bg='black',
                                                font=('Roboto Bold', 12))
        self.out_alg.place(x=645, y=428)
    def check_password(self, word):
        print("check_password")
        if App.session_access == True:
            if App.LVL_access <= 5:
                App.global_controller.frames["Frame8"].update_tree(datetime.now().strftime("%d.%m.%Y"))
                if word == "switch":
                    print("CALL FUNCTION")
                    self.update_switch(self)
                elif word == "click1":
                    App.numpad_instance = numpad.Numpad(None, "INT")
                    App.numpad_instance.min_value.config(text="0")
                    App.numpad_instance.max_value.config(text="9999")
                    App.numpad_instance.new_title(self.label3.cget('text')+" ")
                    App.numpad_instance.entry_label.config(text=self.start_mod_value.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click1
                elif word == "click2":
                    App.numpad_instance = numpad.Numpad(None, "FLOAT2")
                    App.numpad_instance.min_value.config(text="0.00")
                    App.numpad_instance.max_value.config(text="99.99")
                    App.numpad_instance.new_title(self.label4.cget('text')+" ")
                    App.numpad_instance.entry_label.config(text=self.upper_pressure_value.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click2
                elif word == "click3":
                    App.numpad_instance = numpad.Numpad(None, "FLOAT2")
                    App.numpad_instance.min_value.config(text="0.00")
                    App.numpad_instance.max_value.config(text="99.99")
                    App.numpad_instance.new_title(self.label5.cget('text')+" ")
                    App.numpad_instance.entry_label.config(text=self.lower_pressure_value.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click3
                elif word == "click4":
                    App.numpad_instance = numpad.Numpad(None, "INT")
                    App.numpad_instance.min_value.config(text="0")
                    App.numpad_instance.max_value.config(text="30")
                    App.numpad_instance.new_title(self.label6.cget('text')+" ")
                    App.numpad_instance.entry_label.config(text=self.swing_time_value.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click4
                elif word == "click5":
                    App.numpad_instance = numpad.Numpad(None, "FLOAT2")
                    App.numpad_instance.min_value.config(text="0.00")
                    App.numpad_instance.max_value.config(text="99.99")
                    App.numpad_instance.new_title(self.label7.cget('text')+" ")
                    App.numpad_instance.entry_label.config(text=self.acceptable_range_value.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click5
                elif word == "click6":
                    App.numpad_instance = numpad.Numpad(None, "FLOAT1")
                    App.numpad_instance.min_value.config(text="0")
                    App.numpad_instance.max_value.config(text="5.0")
                    App.numpad_instance.new_title(self.label8.cget('text')+" ")
                    App.numpad_instance.entry_label.config(text=self.acceptable_frequency_value.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click6
                json_methods.save_data(r"data/desktop_storage.json", App.storage_data)
            else:
                messagebox.showerror("Ошибка!", "Недостаточно прав!")
        else:
            self.keypad_instance = keypad.Keypad()
            self.keypad_instance.grab_set()
            self.keypad_instance.callback_function = self.set_access

    def click1(self):
        App.global_controller.frames["Frame8"].tree.insert("", tk.END, values=(
            datetime.now().strftime("%d.%m.%Y"), datetime.now().strftime("%H:%M:%S"), self.label3.cget('text'),
            f"{self.start_mod_value.cget('text')} -> {App.numpad_instance.current_value}", "Options"))
        App.global_controller.frames["Frame14"].start_mod_value.config(text=App.numpad_instance.current_value)
        App.storage_data["Starting_Power_Savingmode"] = App.numpad_instance.current_value
        json_methods.save_data(App.file_path, App.global_controller.frames["Frame8"].save_journal_data())

    def click2(self):
        App.global_controller.frames["Frame8"].tree.insert("", tk.END, values=(
            datetime.now().strftime("%d.%m.%Y"), datetime.now().strftime("%H:%M:%S"), self.label4.cget('text'),
            f"{self.upper_pressure_value.cget('text')} -> {App.numpad_instance.current_value}", "Options"))
        App.global_controller.frames["Frame14"].upper_pressure_value.config(text=App.numpad_instance.current_value)
        App.storage_data["Pressure_Drawdown"] = App.numpad_instance.current_value
        json_methods.save_data(App.file_path, App.global_controller.frames["Frame8"].save_journal_data())

    def click3(self):
        App.global_controller.frames["Frame8"].tree.insert("", tk.END, values=(
            datetime.now().strftime("%d.%m.%Y"), datetime.now().strftime("%H:%M:%S"), self.label5.cget('text'),
            f"{self.lower_pressure_value.cget('text')} -> {App.numpad_instance.current_value}", "Options"))
        App.global_controller.frames["Frame14"].lower_pressure_value.config(text=App.numpad_instance.current_value)
        App.storage_data["Pressure_Increase"] = App.numpad_instance.current_value
        json_methods.save_data(App.file_path, App.global_controller.frames["Frame8"].save_journal_data())

    def click4(self):
        App.global_controller.frames["Frame8"].tree.insert("", tk.END, values=(
            datetime.now().strftime("%d.%m.%Y"), datetime.now().strftime("%H:%M:%S"), self.label6.cget('text'),
            f"{self.swing_time_value.cget('text')} -> {App.numpad_instance.current_value}", "Options"))
        App.global_controller.frames["Frame14"].swing_time_value.config(text=App.numpad_instance.current_value)
        App.storage_data["Swing_Time"] = App.numpad_instance.current_value
        json_methods.save_data(App.file_path, App.global_controller.frames["Frame8"].save_journal_data())

    def click5(self):
        App.global_controller.frames["Frame8"].tree.insert("", tk.END, values=(
            datetime.now().strftime("%d.%m.%Y"), datetime.now().strftime("%H:%M:%S"), self.label7.cget('text'),
            f"{self.acceptable_range_value.cget('text')} -> {App.numpad_instance.current_value}", "Options"))
        App.global_controller.frames["Frame14"].acceptable_range_value.config(text=App.numpad_instance.current_value)
        App.storage_data["Pressure_Range"] = App.numpad_instance.current_value
        json_methods.save_data(App.file_path, App.global_controller.frames["Frame8"].save_journal_data())

    def click6(self):
        App.global_controller.frames["Frame8"].tree.insert("", tk.END, values=(
            datetime.now().strftime("%d.%m.%Y"), datetime.now().strftime("%H:%M:%S"), self.label8.cget('text'),
            f"{self.acceptable_frequency_value.cget('text')} -> {App.numpad_instance.current_value}", "Options"))
        App.global_controller.frames["Frame14"].acceptable_frequency_value.config(text=App.numpad_instance.current_value)
        App.storage_data["Frequency_Range"] = App.numpad_instance.current_value
        json_methods.save_data(App.file_path, App.global_controller.frames["Frame8"].save_journal_data())

    def set_access(self, event=None):
        print("set_access")
        App.session_access = True
        App.LVL_access = self.keypad_instance.access
        App.shields_hide()
        if App.LVL_access > 5:
            messagebox.showerror("Ошибка!", "Недостаточно прав!")
    def update_switch(self, event):
        if self.Switch_Flat_img.cget("file") == "new_images/Switch-0.png":
            App.global_controller.frames["Frame8"].tree.insert("", tk.END, values=(
                datetime.now().strftime("%d.%m.%Y"), datetime.now().strftime("%H:%M:%S"), self.label2.cget('text'),
                f"OFF -> ON", "Options"))
            self.Switch_Flat_img = PhotoImage(file=r"new_images/Switch-1.png")
            App.storage_data["Power_Savingmode"] = "1"
            json_methods.save_data(App.file_path, App.global_controller.frames["Frame8"].save_journal_data())
        elif self.Switch_Flat_img.cget("file") == "new_images/Switch-1.png":
            App.global_controller.frames["Frame8"].tree.insert("", tk.END, values=(
                datetime.now().strftime("%d.%m.%Y"), datetime.now().strftime("%H:%M:%S"), self.label2.cget('text'),
                f"ON -> OFF", "Options"))
            self.Switch_Flat_img = PhotoImage(file=r"new_images/Switch-0.png")
            App.storage_data["Power_Savingmode"] = "0"
            json_methods.save_data(App.file_path, App.global_controller.frames["Frame8"].save_journal_data())
        self.Switch_Flat_button = self.canvas.create_image(670, 78, image=self.Switch_Flat_img)
        self.canvas.tag_bind(self.Switch_Flat_button, "<Button-1>", lambda event: self.check_password("switch"))

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
        self.img_screen = Image.open(r"new_images/screen.png")
        self.img_left = Image.open(r"new_images/left.png")
        self.img_triangle = Image.open(r"new_images/triangle.png")
        self.img_diode = Image.open(r"new_images/diode.png")
        self.img_swap = Image.open(r"new_images/swap.png")
        self.img_plusone = Image.open(r"new_images/plus_one.png")
        self.img_minusone = Image.open(r"new_images/minus_one.png")
        self.img_options = Image.open(r"new_images/options.png")
        self.img_emergency = Image.open(r"new_images/warning.png")

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

        self.img_suction_pressure_sensor = PhotoImage(file=f"new_images/suction_pressure_sensor.png")
        self.img_interval = PhotoImage(file=f"new_images/interval.png")
        self.img_discharge_pressure_sensore = PhotoImage(file=f"new_images/discharge_pressure_sensor.png")
        self.img_warning = PhotoImage(file=f"new_images/warning.png")
        self.img_emergency = PhotoImage(file=f"new_images/emergency.png")
        self.img_stop_sign = PhotoImage(file=f"new_images/stop_sign.png")
        self.img_stop_crit_pressure = PhotoImage(file=f"new_images/stop_crit_pressure.png")
        self.img_pipe = PhotoImage(file=f"new_images/pipe.png")
        self.img_shield = PhotoImage(file=f"new_images/shield.png")
        self.img_rectangle_l = PhotoImage(file=f"new_images/rectangle_long.png")

        self.canvas.create_image(233, 75, image=self.img_suction_pressure_sensor)
        self.canvas.create_image(233, 111, image=self.img_interval)
        self.canvas.create_image(233, 150, image=self.img_discharge_pressure_sensore)
        self.canvas.create_image(233, 220, image=self.img_warning)
        self.canvas.create_image(233, 259, image=self.img_emergency)
        self.canvas.create_image(233, 298, image=self.img_interval)
        self.canvas.create_image(233, 363, image=self.img_stop_sign)
        self.canvas.create_image(233, 405, image=self.img_stop_crit_pressure)
        self.canvas.create_image(233, 450, image=self.img_pipe)

        self.shield1 = self.canvas.create_image(624, 75, image=self.img_shield)
        self.shield2 = self.canvas.create_image(624, 113, image=self.img_shield)
        self.shield3 = self.canvas.create_image(624, 152, image=self.img_shield)
        self.shield4 = self.canvas.create_image(624, 222, image=self.img_shield)
        self.shield5 = self.canvas.create_image(624, 261, image=self.img_shield)
        self.shield6 = self.canvas.create_image(624, 300, image=self.img_shield)
        self.shield7 = self.canvas.create_image(624, 364, image=self.img_shield)
        self.shield8 = self.canvas.create_image(624, 402, image=self.img_shield)
        self.shield9 = self.canvas.create_image(624, 438, image=self.img_shield)

        self.label1 = tk.Label(self.canvas, text="Реле перепада давления",
                               fg='white', bg='black',
                               font=('Roboto Bold', 10))
        self.label1.place(x=217, y=38)
        self.label2 = tk.Label(self.canvas, text="Частота срабатывания",
                                fg='white', bg='black',
                                font=('Roboto Bold', 12))
        self.label2.place(x=259, y=65)
        self.label3 = tk.Label(self.canvas, text="Задержка аварии",
                               fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label3.place(x=259, y=101)
        self.label4 = tk.Label(self.canvas, text="Максимальное число аварий",
                               fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label4.place(x=259, y=139)
        self.label5 = tk.Label(self.canvas, text="Настройки сухого хода",
                               fg='white', bg='black',
                               font=('Roboto Bold', 10))
        self.label5.place(x=217, y=185)
        self.label6 = tk.Label(self.canvas, text="Предупреждения",
                               fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label6.place(x=259, y=210)
        self.label7 = tk.Label(self.canvas, text="Авария",
                               fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label7.place(x=259, y=249)
        self.label8 = tk.Label(self.canvas, text="Задержка аварии",
                               fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label8.place(x=259, y=288)
        self.label9 = tk.Label(self.canvas, text="Параметры стопа насосов при аварии",
                               fg='white', bg='black',
                               font=('Roboto Bold', 10))
        self.label9.place(x=217, y=328)
        self.label10 = tk.Label(self.canvas, text="Задержка выключения",
                               fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label10.place(x=259, y=353)
        self.label11 = tk.Label(self.canvas, text="Стоп по критическому давлению",
                               fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label11.place(x=259, y=394)
        self.label12 = tk.Label(self.canvas, text="Контроль разрыва трубопровода",
                               fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label12.place(x=259, y=436)

        self.canvas.create_line(215, 179, 795, 179, fill="gray", width=1)
        self.canvas.create_line(215, 326, 795, 326, fill="gray", width=1)
        # Кликабельная зона
        self.response_frequency = self.canvas.create_image(716, 73, image=self.img_rectangle_l)
        self.response_frequency_value = tk.Label(self.canvas, text=App.storage_data["Response_Frequency"],
                                                   fg='white', bg='black',
                                                   font=('Roboto Bold', 12))
        self.response_frequency_value.place(x=645, y=63)
        self.response_frequency_label = tk.Label(self.canvas, text="Гц",
                                                   fg='white', bg='black',
                                                   font=('Roboto Bold', 12))
        self.response_frequency_label.place(x=759, y=63)
        self.canvas.tag_bind(self.response_frequency, "<Button-1>", lambda event: self.check_password("click1"))
        self.response_frequency_value.bind("<Button-1>", lambda event: self.check_password("click1"))
        self.response_frequency_label.bind("<Button-1>", lambda event: self.check_password("click1"))
        self.cooldown_emergency = self.canvas.create_image(716, 111, image=self.img_rectangle_l)
        self.cooldown_emergency_value = tk.Label(self.canvas, text=App.storage_data["Delay_Accident_One"],
                                                 fg='white', bg='black',
                                                 font=('Roboto Bold', 12))
        self.cooldown_emergency_value.place(x=645, y=101)
        self.cooldown_emergency_label = tk.Label(self.canvas, text="Сек",
                                                 fg='white', bg='black',
                                                 font=('Roboto Bold', 12))
        self.cooldown_emergency_label.place(x=753, y=101)
        self.canvas.tag_bind(self.cooldown_emergency, "<Button-1>", lambda event: self.check_password("click2"))
        self.cooldown_emergency_value.bind("<Button-1>", lambda event: self.check_password("click2"))
        self.cooldown_emergency_label.bind("<Button-1>", lambda event: self.check_password("click2"))
        self.max_emergency = self.canvas.create_image(716, 150, image=self.img_rectangle_l)
        self.max_emergency_value = tk.Label(self.canvas, text=App.storage_data["Number_Accidents"],
                                                 fg='white', bg='black',
                                                 font=('Roboto Bold', 12))
        self.max_emergency_value.place(x=645, y=140)
        self.max_emergency_label = tk.Label(self.canvas, text="Шт",
                                                 fg='white', bg='black',
                                                 font=('Roboto Bold', 12))
        self.max_emergency_label.place(x=753, y=140)
        self.canvas.tag_bind(self.max_emergency, "<Button-1>", lambda event: self.check_password("click3"))
        self.max_emergency_value.bind("<Button-1>", lambda event: self.check_password("click3"))
        self.max_emergency_label.bind("<Button-1>", lambda event: self.check_password("click3"))
        self.warnings = self.canvas.create_image(716, 220, image=self.img_rectangle_l)
        self.warnings_value = tk.Label(self.canvas, text=App.storage_data["Warnings"],
                                                 fg='white', bg='black',
                                                 font=('Roboto Bold', 12))
        self.warnings_value.place(x=645, y=210)
        self.warnings_label = tk.Label(self.canvas, text="Бар",
                                                 fg='white', bg='black',
                                                 font=('Roboto Bold', 12))
        self.warnings_label.place(x=753, y=210)
        self.canvas.tag_bind(self.warnings, "<Button-1>", lambda event: self.check_password("click4"))
        self.warnings_value.bind("<Button-1>", lambda event: self.check_password("click4"))
        self.warnings_label.bind("<Button-1>", lambda event: self.check_password("click4"))
        self.emergency = self.canvas.create_image(716, 259, image=self.img_rectangle_l)
        self.emergency_value = tk.Label(self.canvas, text=App.storage_data["Crash"],
                                       fg='white', bg='black',
                                       font=('Roboto Bold', 12))
        self.emergency_value.place(x=645, y=249)
        self.emergency_label = tk.Label(self.canvas, text="Бар",
                                       fg='white', bg='black',
                                       font=('Roboto Bold', 12))
        self.emergency_label.place(x=753, y=249)
        self.canvas.tag_bind(self.max_emergency, "<Button-1>", lambda event: self.check_password("click5"))
        self.max_emergency_value.bind("<Button-1>", lambda event: self.check_password("click5"))
        self.max_emergency_label.bind("<Button-1>", lambda event: self.check_password("click5"))
        self.cd_emergency = self.canvas.create_image(716, 298, image=self.img_rectangle_l)
        self.cd_emergency_value = tk.Label(self.canvas, text=App.storage_data["Delay_Accident_Two"],
                                        fg='white', bg='black',
                                        font=('Roboto Bold', 12))
        self.cd_emergency_value.place(x=645, y=288)
        self.cd_emergency_label = tk.Label(self.canvas, text="Сек",
                                        fg='white', bg='black',
                                        font=('Roboto Bold', 12))
        self.cd_emergency_label.place(x=753, y=288)
        self.canvas.tag_bind(self.cd_emergency, "<Button-1>", lambda event: self.check_password("click6"))
        self.cd_emergency_value.bind("<Button-1>", lambda event: self.check_password("click6"))
        self.cd_emergency_label.bind("<Button-1>", lambda event: self.check_password("click6"))
        self.cd_off = self.canvas.create_image(716, 362, image=self.img_rectangle_l)
        self.cd_off_value = tk.Label(self.canvas, text=App.storage_data["Shutdown_Delay"],
                                           fg='white', bg='black',
                                           font=('Roboto Bold', 12))
        self.cd_off_value.place(x=645, y=352)
        self.cd_off_label = tk.Label(self.canvas, text="Сек",
                                           fg='white', bg='black',
                                           font=('Roboto Bold', 12))
        self.cd_off_label.place(x=753, y=352)
        self.canvas.tag_bind(self.cd_off, "<Button-1>", lambda event: self.check_password("click7"))
        self.cd_off_value.bind("<Button-1>", lambda event: self.check_password("click7"))
        self.cd_off_label.bind("<Button-1>", lambda event: self.check_password("click7"))
        self.stop_crit_pressure = self.canvas.create_image(716, 400, image=self.img_rectangle_l)
        self.stop_crit_pressure_value = tk.Label(self.canvas, text=App.storage_data["Pressure_Stop"],
                                     fg='white', bg='black',
                                     font=('Roboto Bold', 12))
        self.stop_crit_pressure_value.place(x=645, y=390)
        self.stop_crit_pressure_label = tk.Label(self.canvas, text="Бар",
                                     fg='white', bg='black',
                                     font=('Roboto Bold', 12))
        self.stop_crit_pressure_label.place(x=753, y=390)
        self.canvas.tag_bind(self.stop_crit_pressure, "<Button-1>", lambda event: self.check_password("click8"))
        self.stop_crit_pressure_value.bind("<Button-1>", lambda event: self.check_password("click8"))
        self.stop_crit_pressure_label.bind("<Button-1>", lambda event: self.check_password("click8"))


        self.Switch_Flat_img = PhotoImage(file=r"new_images/_NO_YES.png") if App.storage_data["Gap_Control"] == "0" else PhotoImage(file=r"new_images/_YES_NO.png")
        self.Switch_Flat_button = self.canvas.create_image(674, 440, image=self.Switch_Flat_img)
        self.canvas.tag_bind(self.Switch_Flat_button, "<Button-1>", lambda event: self.check_password("switch"))
        # Кликабельная зона

    def check_password(self, word):
        print("check_password")
        if App.session_access == True:
            if App.LVL_access <= 5:
                App.global_controller.frames["Frame8"].update_tree(datetime.now().strftime("%d.%m.%Y"))
                if word == "switch":
                    print("CALL FUNCTION")
                    self.update_switch(self)
                elif word == "click1":
                    App.numpad_instance = numpad.Numpad(None, "FLOAT1")
                    App.numpad_instance.min_value.config(text="0.0")
                    App.numpad_instance.max_value.config(text="99.9")
                    App.numpad_instance.new_title(self.label2.cget('text') + " ")
                    App.numpad_instance.entry_label.config(text=self.response_frequency_value.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click1
                elif word == "click2":
                    App.numpad_instance = numpad.Numpad(None, "INT")
                    App.numpad_instance.min_value.config(text="0")
                    App.numpad_instance.max_value.config(text="10")
                    App.numpad_instance.new_title(self.label3.cget('text') + " (Реле) ")
                    App.numpad_instance.entry_label.config(text=self.cooldown_emergency_value.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click2
                elif word == "click3":
                    App.numpad_instance = numpad.Numpad(None, "INT")
                    App.numpad_instance.min_value.config(text="0")
                    App.numpad_instance.max_value.config(text="99")
                    App.numpad_instance.new_title(self.label4.cget('text') + " ")
                    App.numpad_instance.entry_label.config(text=self.max_emergency_value.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click3
                elif word == "click4":
                    App.numpad_instance = numpad.Numpad(None, "FLOAT2")
                    App.numpad_instance.min_value.config(text="0.00")
                    App.numpad_instance.max_value.config(text="99.99")
                    App.numpad_instance.new_title(self.label6.cget('text') + " ")
                    App.numpad_instance.entry_label.config(text=self.warnings_value.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click4
                elif word == "click5":
                    App.numpad_instance = numpad.Numpad(None, "FLOAT2")
                    App.numpad_instance.min_value.config(text="0.00")
                    App.numpad_instance.max_value.config(text="99.99")
                    App.numpad_instance.new_title(self.label7.cget('text') + " ")
                    App.numpad_instance.entry_label.config(text=self.emergency_value.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click5
                elif word == "click6":
                    App.numpad_instance = numpad.Numpad(None, "INT")
                    App.numpad_instance.min_value.config(text="0")
                    App.numpad_instance.max_value.config(text="99")
                    App.numpad_instance.new_title(self.label8.cget('text') + " (Сухой ход) ")
                    App.numpad_instance.entry_label.config(text=self.cd_emergency_value.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click6
                elif word == "click7":
                    App.numpad_instance = numpad.Numpad(None, "INT")
                    App.numpad_instance.min_value.config(text="0")
                    App.numpad_instance.max_value.config(text="5")
                    App.numpad_instance.new_title(self.label10.cget('text') + " ")
                    App.numpad_instance.entry_label.config(text=self.cd_off_value.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click7
                elif word == "click8":
                    App.numpad_instance = numpad.Numpad(None, "FLOAT2")
                    App.numpad_instance.min_value.config(text="0.00")
                    App.numpad_instance.max_value.config(text="99.99")
                    App.numpad_instance.new_title(self.label11.cget('text') + " ")
                    App.numpad_instance.entry_label.config(text=self.stop_crit_pressure_value.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click8
                json_methods.save_data(r"data/desktop_storage.json", App.storage_data)
            else:
                messagebox.showerror("Ошибка!", "Недостаточно прав!")
        else:
            self.keypad_instance = keypad.Keypad()
            self.keypad_instance.grab_set()
            self.keypad_instance.callback_function = self.set_access

    def click1(self):
        App.global_controller.frames["Frame8"].tree.insert("", tk.END, values=(
            datetime.now().strftime("%d.%m.%Y"), datetime.now().strftime("%H:%M:%S"), self.label2.cget('text'),
            f"{self.response_frequency_value.cget('text')} -> {App.numpad_instance.current_value}", "EmergencyModes"))
        App.global_controller.frames["Frame15"].response_frequency_value.config(text=App.numpad_instance.current_value)
        App.storage_data["Response_Frequency"] = App.numpad_instance.current_value
        json_methods.save_data(App.file_path, App.global_controller.frames["Frame8"].save_journal_data())

    def click2(self):
        App.global_controller.frames["Frame8"].tree.insert("", tk.END, values=(
            datetime.now().strftime("%d.%m.%Y"), datetime.now().strftime("%H:%M:%S"), self.label3.cget('text'),
            f"{self.cooldown_emergency_value.cget('text')} -> {App.numpad_instance.current_value}", "EmergencyModes"))
        App.global_controller.frames["Frame15"].cooldown_emergency_value.config(text=App.numpad_instance.current_value)
        App.storage_data["Delay_Accident_One"] = App.numpad_instance.current_value
        json_methods.save_data(App.file_path, App.global_controller.frames["Frame8"].save_journal_data())

    def click3(self):
        App.global_controller.frames["Frame8"].tree.insert("", tk.END, values=(
            datetime.now().strftime("%d.%m.%Y"), datetime.now().strftime("%H:%M:%S"), self.label4.cget('text'),
            f"{self.max_emergency_value.cget('text')} -> {App.numpad_instance.current_value}", "EmergencyModes"))
        App.global_controller.frames["Frame15"].max_emergency_value.config(text=App.numpad_instance.current_value)
        App.storage_data["Number_Accidents"] = App.numpad_instance.current_value
        json_methods.save_data(App.file_path, App.global_controller.frames["Frame8"].save_journal_data())

    def click4(self):
        App.global_controller.frames["Frame8"].tree.insert("", tk.END, values=(
            datetime.now().strftime("%d.%m.%Y"), datetime.now().strftime("%H:%M:%S"), self.label6.cget('text'),
            f"{self.warnings_value.cget('text')} -> {App.numpad_instance.current_value}", "EmergencyModes"))
        App.global_controller.frames["Frame15"].warnings_value.config(text=App.numpad_instance.current_value)
        App.storage_data["Warnings"] = App.numpad_instance.current_value
        json_methods.save_data(App.file_path, App.global_controller.frames["Frame8"].save_journal_data())

    def click5(self):
        App.global_controller.frames["Frame8"].tree.insert("", tk.END, values=(
            datetime.now().strftime("%d.%m.%Y"), datetime.now().strftime("%H:%M:%S"), self.label7.cget('text'),
            f"{self.emergency_value.cget('text')} -> {App.numpad_instance.current_value}", "EmergencyModes"))
        App.global_controller.frames["Frame15"].emergency_value.config(text=App.numpad_instance.current_value)
        App.storage_data["Crash"] = App.numpad_instance.current_value
        json_methods.save_data(App.file_path, App.global_controller.frames["Frame8"].save_journal_data())

    def click6(self):
        App.global_controller.frames["Frame8"].tree.insert("", tk.END, values=(
            datetime.now().strftime("%d.%m.%Y"), datetime.now().strftime("%H:%M:%S"), self.label8.cget('text'),
            f"{self.cd_emergency_value.cget('text')} -> {App.numpad_instance.current_value}", "EmergencyModes"))
        App.global_controller.frames["Frame15"].cd_emergency_value.config(text=App.numpad_instance.current_value)
        App.storage_data["Delay_Accident_Two"] = App.numpad_instance.current_value
        json_methods.save_data(App.file_path, App.global_controller.frames["Frame8"].save_journal_data())

    def click7(self):
        App.global_controller.frames["Frame8"].tree.insert("", tk.END, values=(
            datetime.now().strftime("%d.%m.%Y"), datetime.now().strftime("%H:%M:%S"), self.label10.cget('text'),
            f"{self.cd_off_value.cget('text')} -> {App.numpad_instance.current_value}", "EmergencyModes"))
        App.global_controller.frames["Frame15"].cd_off_value.config(text=App.numpad_instance.current_value)
        App.storage_data["Shutdown_Delay"] = App.numpad_instance.current_value
        json_methods.save_data(App.file_path, App.global_controller.frames["Frame8"].save_journal_data())

    def click8(self):
        App.global_controller.frames["Frame8"].tree.insert("", tk.END, values=(
            datetime.now().strftime("%d.%m.%Y"), datetime.now().strftime("%H:%M:%S"), self.label11.cget('text'),
            f"{self.stop_crit_pressure_value.cget('text')} -> {App.numpad_instance.current_value}", "EmergencyModes"))
        App.global_controller.frames["Frame15"].stop_crit_pressure_value.config(text=App.numpad_instance.current_value)
        App.storage_data["Pressure_Stop"] = App.numpad_instance.current_value
        json_methods.save_data(App.file_path, App.global_controller.frames["Frame8"].save_journal_data())

    def set_access(self, event=None):
        print("set_access")
        App.session_access = True
        App.LVL_access = self.keypad_instance.access
        App.shields_hide()
        if App.LVL_access > 5:
            messagebox.showerror("Ошибка!", "Недостаточно прав!")

    def update_switch(self, event):
        if self.Switch_Flat_img.cget("file") == "new_images/_NO_YES.png":
            App.global_controller.frames["Frame8"].tree.insert("", tk.END, values=(
                datetime.now().strftime("%d.%m.%Y"), datetime.now().strftime("%H:%M:%S"), self.label12.cget('text'),
                f"OFF -> ON", "EmergencyModes"))
            self.Switch_Flat_img = PhotoImage(file=r"new_images/_YES_NO.png")
            App.storage_data["Gap_Control"] = "1"
            json_methods.save_data(App.file_path, App.global_controller.frames["Frame8"].save_journal_data())
        elif self.Switch_Flat_img.cget("file") == "new_images/_YES_NO.png":
            App.global_controller.frames["Frame8"].tree.insert("", tk.END, values=(
                datetime.now().strftime("%d.%m.%Y"), datetime.now().strftime("%H:%M:%S"), self.label12.cget('text'),
                f"ON -> OFF", "EmergencyModes"))
            self.Switch_Flat_img = PhotoImage(file=r"new_images/_NO_YES.png")
            App.storage_data["Gap_Control"] = "0"
            json_methods.save_data(App.file_path, App.global_controller.frames["Frame8"].save_journal_data())
        self.Switch_Flat_button = self.canvas.create_image(674, 440, image=self.Switch_Flat_img)
        self.canvas.tag_bind(self.Switch_Flat_button, "<Button-1>", lambda event: self.check_password("switch"))

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
        self.img_screen = Image.open(r"new_images/screen.png")
        self.img_switches = Image.open(r"new_images/switches.png")
        self.img_timer = Image.open(r"new_images/timer.png")
        self.img_right = Image.open(r"new_images/right.png")
        self.img_left = Image.open(r"new_images/left.png")
        self.img_triangle = Image.open(r"new_images/triangle.png")

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
        self.combined_img3.paste(self.img_switches, (10, 13))
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

        self.img_shield = PhotoImage(file=r"new_images/shield.png")
        self.img_p = PhotoImage(file=r"new_images/p.png")
        self.img_i = PhotoImage(file=r"new_images/i.png")
        self.img_d = PhotoImage(file=r"new_images/d.png")
        self.img_integral = PhotoImage(file=r"new_images/integral.png")
        self.img_thunderbolt = PhotoImage(file=r"new_images/thunderbolt.png")
        self.img_share = PhotoImage(file=r"new_images/share.png")
        self.img_pid = PhotoImage(file=r"new_images/pid.png")
        self.img_eye = PhotoImage(file=r"new_images/eye.png")

        self.canvas.create_image(233.005, 60, image=self.img_p)
        self.canvas.create_image(233, 101.005, image=self.img_i)
        self.canvas.create_image(233, 140.995, image=self.img_d)
        self.canvas.create_image(232.875, 174.445, image=self.img_integral)
        self.canvas.create_image(233, 212, image=self.img_share)
        self.canvas.create_image(233, 253, image=self.img_thunderbolt)
        self.canvas.create_image(233, 300.375, image=self.img_eye)
        self.canvas.create_image(236, 378.65, image=self.img_pid)

        self.canvas.create_line(220, 280, 790, 280, fill="gray", width=1)

        self.shield1 = self.canvas.create_image(620.25, 62.75, image=self.img_shield)
        self.shield2 = self.canvas.create_image(620.25, 99.75, image=self.img_shield)
        self.shield3 = self.canvas.create_image(620.25, 139.75, image=self.img_shield)
        self.shield4 = self.canvas.create_image(620.25, 178.75, image=self.img_shield)
        self.shield5 = self.canvas.create_image(620.25, 215.75, image=self.img_shield)
        self.shield6 = self.canvas.create_image(620.25, 252.75, image=self.img_shield)

        self.label1 = tk.Label(self.canvas, text="Пропорциональный коэффициент", fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label1.place(x=259, y=50)
        self.label2 = tk.Label(self.canvas, text="Интегральный коэффициент", fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label2.place(x=259, y=91)
        self.label3 = tk.Label(self.canvas, text="Диффиеренциальный коэффициент", fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label3.place(x=259, y=131)
        self.label4 = tk.Label(self.canvas, text="Постоянная интегрирования", fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label4.place(x=259, y=168)
        self.label5 = tk.Label(self.canvas, text="Подменить установку", fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label5.place(x=259, y=203)
        self.label6 = tk.Label(self.canvas, text="Установка на подмену", fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label6.place(x=259, y=244)

        self.label7 = tk.Label(self.canvas, text="Текущее давление", fg='white', bg='black',
                               font=('Roboto Bold', 10))
        self.label7.place(x=258, y=288)
        self.label8 = tk.Label(self.canvas, text="текущая уставка", fg='white', bg='black',
                               font=('Roboto Bold', 10))
        self.label8.place(x=258, y=306)
        self.label9 = tk.Label(self.canvas, text="Error", fg='white', bg='black',
                               font=('Roboto Bold', 10))
        self.label9.place(x=258, y=327)
        self.label10 = tk.Label(self.canvas, text="Proportional", fg='white', bg='black',
                               font=('Roboto Bold', 10))
        self.label10.place(x=258, y=349)
        self.label11 = tk.Label(self.canvas, text="Integral", fg='white', bg='black',
                               font=('Roboto Bold', 10))
        self.label11.place(x=258, y=369)
        self.label12 = tk.Label(self.canvas, text="Derivative", fg='white', bg='black',
                               font=('Roboto Bold', 10))
        self.label12.place(x=258, y=392)
        self.label13 = tk.Label(self.canvas, text="Выход PID", fg='white', bg='black',
                               font=('Roboto Bold', 10))
        self.label13.place(x=258, y=410)
        self.label14 = tk.Label(self.canvas, text="Частота", fg='white', bg='black',
                               font=('Roboto Bold', 10))
        self.label14.place(x=258, y=429)

        # Кликабельная зона
        self.img_rectangle_l = PhotoImage(file=r"new_images/rectangle_long.png")

        self.p_rectangle = self.canvas.create_image(715, 62.5, image=self.img_rectangle_l)
        self.canvas.tag_bind(self.p_rectangle, "<Button-1>", lambda event: self.check_password("click1"))
        self.p_k = tk.Label(self.canvas, text=App.storage_data["Proportional_Coefficient"], fg='white', bg='black',
                                font=('Roboto Bold', 12))
        self.p_k.place(x=646, y=52)
        self.p_k.bind("<Button-1>", lambda event: self.check_password("click1"))

        self.i_rectangle = self.canvas.create_image(715, 101.5, image=self.img_rectangle_l)
        self.canvas.tag_bind(self.i_rectangle, "<Button-1>", lambda event: self.check_password("click2"))
        self.i_k = tk.Label(self.canvas, text=App.storage_data["Integral_Coefficient"], fg='white', bg='black',
                            font=('Roboto Bold', 12))
        self.i_k.place(x=646, y=91)
        self.i_k.bind("<Button-1>", lambda event: self.check_password("click2"))

        self.d_rectangle = self.canvas.create_image(715, 140.5, image=self.img_rectangle_l)
        self.canvas.tag_bind(self.d_rectangle, "<Button-1>", lambda event: self.check_password("click3"))
        self.d_k = tk.Label(self.canvas, text=App.storage_data["Differential_Coefficient"], fg='white', bg='black',
                            font=('Roboto Bold', 12))
        self.d_k.place(x=646, y=130)
        self.d_k.bind("<Button-1>", lambda event: self.check_password("click3"))

        self.integral_rectangle = self.canvas.create_image(715, 179.5, image=self.img_rectangle_l)
        self.canvas.tag_bind(self.integral_rectangle, "<Button-1>", lambda event: self.check_password("click4"))
        self.const_integral = tk.Label(self.canvas, text=App.storage_data["Constant_Integrations"], fg='white', bg='black',
                            font=('Roboto Bold', 12))
        self.const_integral.place(x=646, y=169)
        self.const_integral.bind("<Button-1>", lambda event: self.check_password("click4"))

        self.set_rectangle = self.canvas.create_image(715, 257.5, image=self.img_rectangle_l)
        self.canvas.tag_bind(self.set_rectangle, "<Button-1>", lambda event: self.check_password("click5"))
        self.setpoint = tk.Label(self.canvas, text=App.storage_data["Setting_Substitution"], fg='white', bg='black',
                                       font=('Roboto Bold', 12))
        self.setpoint.place(x=646, y=246)
        self.setpoint.bind("<Button-1>", lambda event: self.check_password("click5"))

        self.Switch_Flat_img = PhotoImage(file=r"new_images/Switch-0.png") if App.storage_data["Substitution_Setpoint"] == "0" else PhotoImage(file=r"new_images/Switch-1.png")
        self.Switch_Flat_button = self.canvas.create_image(670, 219, image=self.Switch_Flat_img)
        self.canvas.tag_bind(self.Switch_Flat_button, "<Button-1>", lambda event: self.check_password("switch"))

        self.current_press = tk.Label(self.canvas, text="0.00", fg='#008000', bg='black',
                                font=('Roboto Bold', 10))
        self.current_press.place(x=379, y=289)
        self.current_setpoint = tk.Label(self.canvas, text="0.00", fg='#CE1A1A', bg='black',
                                      font=('Roboto Bold', 10))
        self.current_setpoint.place(x=379, y=307)
        self.error = tk.Label(self.canvas, text="0.0000", fg='white', bg='black',
                                      font=('Roboto Bold', 10))
        self.error.place(x=379, y=327)
        self.proportional = tk.Label(self.canvas, text="0.0000", fg='white', bg='black',
                              font=('Roboto Bold', 10))
        self.proportional.place(x=379, y=349)
        self.integral = tk.Label(self.canvas, text="0.0000", fg='white', bg='black',
                                     font=('Roboto Bold', 10))
        self.integral.place(x=379, y=369)
        self.derivative = tk.Label(self.canvas, text="0.0000", fg='white', bg='black',
                                     font=('Roboto Bold', 10))
        self.derivative.place(x=379, y=392)
        self.out_pid = tk.Label(self.canvas, text="0.0", fg='white', bg='black',
                                   font=('Roboto Bold', 10))
        self.out_pid.place(x=379, y=410)
        self.frequency = tk.Label(self.canvas, text="0.0", fg='#0000FF', bg='black',
                                font=('Roboto Bold', 10))
        self.frequency.place(x=379, y=429)
        # Кликабельная зона

    def check_password(self, word):  # Сверка пароля и вызов необходимого метода, путем слова
        print("check_password")
        if App.session_access == True:
            if App.LVL_access <= 5:
                App.global_controller.frames["Frame8"].update_tree(datetime.now().strftime("%d.%m.%Y"))
                if word == "switch":  # Переключатель
                    print("CALL FUNCTION")
                    self.update_switch(self)
                elif word == "click1":  # Первое поле
                    App.numpad_instance = numpad.Numpad(None, "FLOAT3")
                    App.numpad_instance.min_value.config(text="0.000")
                    App.numpad_instance.max_value.config(text="5.999")
                    App.numpad_instance.new_title(self.label1.cget('text') + " ")
                    App.numpad_instance.entry_label.config(text=self.p_k.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click1
                elif word == "click2":  # Второе поле
                    App.numpad_instance = numpad.Numpad(None, "FLOAT3")
                    App.numpad_instance.min_value.config(text="0.000")
                    App.numpad_instance.max_value.config(text="5.999")
                    App.numpad_instance.new_title(self.label2.cget('text') + " ")
                    App.numpad_instance.entry_label.config(text=self.i_k.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click2
                elif word == "click3":  # Второе поле
                    App.numpad_instance = numpad.Numpad(None, "FLOAT3")
                    App.numpad_instance.min_value.config(text="0.000")
                    App.numpad_instance.max_value.config(text="5.999")
                    App.numpad_instance.new_title(self.label3.cget('text') + " ")
                    App.numpad_instance.entry_label.config(text=self.d_k.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click3
                elif word == "click4":  # Второе поле
                    App.numpad_instance = numpad.Numpad(None, "FLOAT3")
                    App.numpad_instance.min_value.config(text="0.000")
                    App.numpad_instance.max_value.config(text="5.999")
                    App.numpad_instance.new_title(self.label4.cget('text') + " ")
                    App.numpad_instance.entry_label.config(text=self.const_integral.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click4
                elif word == "click5":  # Второе поле
                    App.numpad_instance = numpad.Numpad(None, "FLOAT2")
                    App.numpad_instance.min_value.config(text="0.00")
                    App.numpad_instance.max_value.config(text="99.99")
                    App.numpad_instance.new_title(self.label6.cget('text') + " ")
                    App.numpad_instance.entry_label.config(text=self.setpoint.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click5
                json_methods.save_data(r"data/desktop_storage.json", App.storage_data)
            else:
                messagebox.showerror("Ошибка!", "Недостаточно прав!")
        else:
            self.keypad_instance = keypad.Keypad()
            self.keypad_instance.grab_set()
            self.keypad_instance.callback_function = self.set_access

    def click1(self):
        App.global_controller.frames["Frame8"].tree.insert("", tk.END, values=(
            datetime.now().strftime("%d.%m.%Y"), datetime.now().strftime("%H:%M:%S"), self.label1.cget('text'),
            f"{self.p_k.cget('text')} -> {App.numpad_instance.current_value}", "SettingsPID"))
        App.global_controller.frames["Frame16"].p_k.config(text=App.numpad_instance.current_value)
        App.storage_data["Proportional_Coefficient"] = App.numpad_instance.current_value
        json_methods.save_data(App.file_path, App.global_controller.frames["Frame8"].save_journal_data())

    def click2(self):
        App.global_controller.frames["Frame8"].tree.insert("", tk.END, values=(
            datetime.now().strftime("%d.%m.%Y"), datetime.now().strftime("%H:%M:%S"), self.label2.cget('text'),
            f"{self.i_k.cget('text')} -> {App.numpad_instance.current_value}", "SettingsPID"))
        App.global_controller.frames["Frame16"].i_k.config(text=App.numpad_instance.current_value)
        App.storage_data["Integral_Coefficient"] = App.numpad_instance.current_value
        json_methods.save_data(App.file_path, App.global_controller.frames["Frame8"].save_journal_data())
    def click3(self):
        App.global_controller.frames["Frame8"].tree.insert("", tk.END, values=(
            datetime.now().strftime("%d.%m.%Y"), datetime.now().strftime("%H:%M:%S"), self.label3.cget('text'),
            f"{self.d_k.cget('text')} -> {App.numpad_instance.current_value}", "SettingsPID"))
        App.global_controller.frames["Frame16"].d_k.config(text=App.numpad_instance.current_value)
        App.storage_data["Differential_Coefficient"] = App.numpad_instance.current_value
        json_methods.save_data(App.file_path, App.global_controller.frames["Frame8"].save_journal_data())

    def click4(self):
        App.global_controller.frames["Frame8"].tree.insert("", tk.END, values=(
            datetime.now().strftime("%d.%m.%Y"), datetime.now().strftime("%H:%M:%S"), self.label4.cget('text'),
            f"{self.const_integral.cget('text')} -> {App.numpad_instance.current_value}", "SettingsPID"))
        App.global_controller.frames["Frame16"].const_integral.config(text=App.numpad_instance.current_value)
        App.storage_data["Constant_Integrations"] = App.numpad_instance.current_value
        json_methods.save_data(App.file_path, App.global_controller.frames["Frame8"].save_journal_data())

    def click5(self):
        App.global_controller.frames["Frame8"].tree.insert("", tk.END, values=(
            datetime.now().strftime("%d.%m.%Y"), datetime.now().strftime("%H:%M:%S"), self.label6.cget('text'),
            f"{self.setpoint.cget('text')} -> {App.numpad_instance.current_value}", "SettingsPID"))
        App.global_controller.frames["Frame16"].setpoint.config(text=App.numpad_instance.current_value)
        App.storage_data["Setting_Substitution"] = App.numpad_instance.current_value
        App.global_controller.frames["Frame2"].update_setpoints()
        json_methods.save_data(App.file_path, App.global_controller.frames["Frame8"].save_journal_data())


    # Получение доступа
    def set_access(self, event=None):
        print("set_access")
        App.session_access = True
        App.LVL_access = self.keypad_instance.access
        App.shields_hide()
        if App.LVL_access > 5:
            messagebox.showerror("Ошибка!", "Недостаточно прав!")

    def update_switch(self, event):
        if self.Switch_Flat_img.cget("file") == "new_images/Switch-0.png":
            App.global_controller.frames["Frame8"].tree.insert("", tk.END, values=(
                datetime.now().strftime("%d.%m.%Y"), datetime.now().strftime("%H:%M:%S"), self.label5.cget('text'),
                f"OFF -> ON", "SettingsPID"))
            self.Switch_Flat_img = PhotoImage(file=r"new_images/Switch-1.png")
            App.storage_data["Substitution_Setpoint"] = "1"
            App.global_controller.frames["Frame2"].type_setpoint.config(text="PID")
            json_methods.save_data(App.file_path, App.global_controller.frames["Frame8"].save_journal_data())
        elif self.Switch_Flat_img.cget("file") == "new_images/Switch-1.png":
            App.global_controller.frames["Frame8"].tree.insert("", tk.END, values=(
                datetime.now().strftime("%d.%m.%Y"), datetime.now().strftime("%H:%M:%S"), self.label5.cget('text'),
                f"ON -> OFF", "SettingsPID"))
            self.Switch_Flat_img = PhotoImage(file=r"new_images/Switch-0.png")
            App.storage_data["Substitution_Setpoint"] = "0"
            App.global_controller.frames["Frame2"].type_setpoint.config(text="Пользователь")
            json_methods.save_data(App.file_path, App.global_controller.frames["Frame8"].save_journal_data())
        self.Switch_Flat_button = self.canvas.create_image(670, 219, image=self.Switch_Flat_img)
        self.canvas.tag_bind(self.Switch_Flat_button, "<Button-1>", lambda event: self.check_password("switch"))
        App.global_controller.frames["Frame2"].update_setpoints()

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
        self.img_screen = Image.open(r"new_images/screen.png")
        self.img_switches = Image.open(r"new_images/switches.png")
        self.img_timer = Image.open(r"new_images/timer.png")
        self.img_right = Image.open(r"new_images/right.png")
        self.img_left = Image.open(r"new_images/left.png")
        self.img_triangle = Image.open(r"new_images/triangle.png")

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
        self.combined_img3.paste(self.img_switches, (10, 13))
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

        self.InterfaceScreen_img = PhotoImage(file=r"new_images/PLC.png")
        self.InterfaceScreen = self.canvas.create_image(500, 175, image=self.InterfaceScreen_img)

        self.switch_btn_di1_img = PhotoImage(file=r"new_images/Switch1-0.png")
        self.switch_btn_di1_button = self.canvas.create_image(269, 97, image=self.switch_btn_di1_img)
        self.switch_btn_di2_img = PhotoImage(file=r"new_images/Switch1-0.png")
        self.switch_btn_di2_button = self.canvas.create_image(295, 97, image=self.switch_btn_di2_img)
        self.switch_btn_di3_img = PhotoImage(file=r"new_images/Switch1-0.png")
        self.switch_btn_di3_button = self.canvas.create_image(321, 97, image=self.switch_btn_di3_img)
        self.switch_btn_di4_img = PhotoImage(file=r"new_images/Switch1-0.png")
        self.switch_btn_di4_button = self.canvas.create_image(350, 97, image=self.switch_btn_di4_img)
        self.switch_btn_di5_img = PhotoImage(file=r"new_images/Switch1-0.png")
        self.switch_btn_di5_button = self.canvas.create_image(377, 97, image=self.switch_btn_di5_img)
        self.switch_btn_di6_img = PhotoImage(file=r"new_images/Switch1-0.png")
        self.switch_btn_di6_button = self.canvas.create_image(404, 97, image=self.switch_btn_di6_img)
        self.switch_btn_di7_img = PhotoImage(file=r"new_images/Switch1-0.png")
        self.switch_btn_di7_button = self.canvas.create_image(432, 97, image=self.switch_btn_di7_img)
        self.switch_btn_di8_img = PhotoImage(file=r"new_images/Switch1-0.png")
        self.switch_btn_di8_button = self.canvas.create_image(458, 97, image=self.switch_btn_di8_img)
        self.switch_btn_di9_img = PhotoImage(file=r"new_images/Switch1-0.png")
        self.switch_btn_di9_button = self.canvas.create_image(487, 97, image=self.switch_btn_di9_img)
        self.switch_btn_di10_img = PhotoImage(file=r"new_images/Switch1-0.png")
        self.switch_btn_di10_button = self.canvas.create_image(514, 97, image=self.switch_btn_di10_img)
        self.switch_btn_di11_img = PhotoImage(file=r"new_images/Switch1-0.png")
        self.switch_btn_di11_button = self.canvas.create_image(541, 97, image=self.switch_btn_di11_img)
        self.switch_btn_di12_img = PhotoImage(file=r"new_images/Switch1-0.png")
        self.switch_btn_di12_button = self.canvas.create_image(568, 97, image=self.switch_btn_di12_img)
        self.switch_btn_rs485_img = PhotoImage(file=r"new_images/Switch2-0.png")
        self.switch_btn_rs485_button = self.canvas.create_image(719, 97, image=self.switch_btn_rs485_img)

        self.switch_btn_dq1_img = PhotoImage(file=r"new_images/Switch1-0.png")
        self.switch_btn_dq1_button = self.canvas.create_image(269.5, 249, image=self.switch_btn_dq1_img)
        self.switch_btn_dq2_img = PhotoImage(file=r"new_images/Switch1-0.png")
        self.switch_btn_dq2_button = self.canvas.create_image(296.5, 249, image=self.switch_btn_dq2_img)
        self.switch_btn_dq3_img = PhotoImage(file=r"new_images/Switch1-0.png")
        self.switch_btn_dq3_button = self.canvas.create_image(323.5, 249, image=self.switch_btn_dq3_img)
        self.switch_btn_dq4_img = PhotoImage(file=r"new_images/Switch1-0.png")
        self.switch_btn_dq4_button = self.canvas.create_image(352.5, 249, image=self.switch_btn_dq4_img)
        self.switch_btn_dq5_img = PhotoImage(file=r"new_images/Switch1-0.png")
        self.switch_btn_dq5_button = self.canvas.create_image(378.5, 249, image=self.switch_btn_dq5_img)
        self.switch_btn_dq6_img = PhotoImage(file=r"new_images/Switch1-0.png")
        self.switch_btn_dq6_button = self.canvas.create_image(406, 249, image=self.switch_btn_dq6_img)
        self.switch_btn_dq7_img = PhotoImage(file=r"new_images/Switch1-0.png")
        self.switch_btn_dq7_button = self.canvas.create_image(434, 249, image=self.switch_btn_dq7_img)
        self.switch_btn_dq8_img = PhotoImage(file=r"new_images/Switch1-0.png")
        self.switch_btn_dq8_button = self.canvas.create_image(460, 249, image=self.switch_btn_dq8_img)
        self.switch_btn_dq9_img = PhotoImage(file=r"new_images/Switch1-0.png")
        self.switch_btn_dq9_button = self.canvas.create_image(488, 249, image=self.switch_btn_dq9_img)
        self.switch_btn_dq10_img = PhotoImage(file=r"new_images/Switch1-0.png")
        self.switch_btn_dq10_button = self.canvas.create_image(515, 249, image=self.switch_btn_dq10_img)
        self.switch_btn_dq11_img = PhotoImage(file=r"new_images/Switch1-0.png")
        self.switch_btn_dq11_button = self.canvas.create_image(542, 249, image=self.switch_btn_dq11_img)
        self.switch_btn_dq12_img = PhotoImage(file=r"new_images/Switch1-0.png")
        self.switch_btn_dq12_button = self.canvas.create_image(571, 249, image=self.switch_btn_dq12_img)
        self.switch_btn_ai1_img = PhotoImage(file=r"new_images/Switch1-0.png")
        self.switch_btn_ai1_button = self.canvas.create_image(625, 249, image=self.switch_btn_ai1_img)
        self.switch_btn_ai2_img = PhotoImage(file=r"new_images/Switch1-0.png")
        self.switch_btn_ai2_button = self.canvas.create_image(650.5, 249, image=self.switch_btn_ai2_img)
        self.switch_btn_ai3_img = PhotoImage(file=r"new_images/Switch1-0.png")
        self.switch_btn_ai3_button = self.canvas.create_image(677.5, 249, image=self.switch_btn_ai3_img)
        self.switch_btn_ai4_img = PhotoImage(file=r"new_images/Switch1-0.png")
        self.switch_btn_ai4_button = self.canvas.create_image(705, 249, image=self.switch_btn_ai4_img)
        self.switch_btn_ai5_img = PhotoImage(file=r"new_images/Switch1-0.png")
        self.switch_btn_ai5_button = self.canvas.create_image(729, 249, image=self.switch_btn_ai5_img)

        self.label1 = tk.Label(self.canvas, text="AI1:", fg='white', bg='black',
                                font=('Roboto Bold', 10))
        self.label1.place(x=244, y=358, width=30, height=14)
        self.label2 = tk.Label(self.canvas, text="AI2:", fg='white', bg='black',
                                font=('Roboto Bold', 10))
        self.label2.place(x=244, y=378, width=30, height=14)
        self.label3 = tk.Label(self.canvas, text="AI3:", fg='white', bg='black',
                                font=('Roboto Bold', 10))
        self.label3.place(x=244, y=398, width=30, height=14)
        self.label4 = tk.Label(self.canvas, text="AI4:", fg='white', bg='black',
                                font=('Roboto Bold', 10))
        self.label4.place(x=244, y=418, width=30, height=14)
        self.label5 = tk.Label(self.canvas, text="AI5:", fg='white', bg='black',
                                font=('Roboto Bold', 10))
        self.label5.place(x=244, y=438, width=30, height=14)

        self.label6 = tk.Label(self.canvas, text="AQ1:", fg='white', bg='black',
                                font=('Roboto Bold', 10))
        self.label6.place(x=600, y=358, width=30, height=14)

        self.labelA1 = tk.Label(self.canvas, text="0", fg='white', bg='black',
                               font=('Roboto Bold', 10))
        self.labelA1.place(x=274, y=358, width=30, height=14)
        self.labelA2 = tk.Label(self.canvas, text="0", fg='white', bg='black',
                                font=('Roboto Bold', 10))
        self.labelA2.place(x=274, y=378, width=30, height=14)
        self.labelA3 = tk.Label(self.canvas, text="0", fg='white', bg='black',
                                font=('Roboto Bold', 10))
        self.labelA3.place(x=274, y=398, width=30, height=14)
        self.labelA4 = tk.Label(self.canvas, text="0", fg='white', bg='black',
                                font=('Roboto Bold', 10))
        self.labelA4.place(x=274, y=418, width=30, height=14)
        self.labelA5 = tk.Label(self.canvas, text="0", fg='white', bg='black',
                                font=('Roboto Bold', 10))
        self.labelA5.place(x=274, y=438, width=30, height=14)

        self.labelAQ = tk.Label(self.canvas, text="0", fg='white', bg='black',
                                font=('Roboto Bold', 10))
        self.labelAQ.place(x=630, y=358, width=30, height=14)

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
        self.img_screen = Image.open(r"new_images/screen.png")
        self.img_switches = Image.open(r"new_images/switches.png")
        self.img_timer = Image.open(r"new_images/timer.png")
        self.img_right = Image.open(r"new_images/right.png")
        self.img_left = Image.open(r"new_images/left.png")
        self.img_triangle = Image.open(r"new_images/triangle.png")


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
        self.combined_img3.paste(self.img_switches, (10, 13))
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

        self.img_tablet = PhotoImage(file=r"new_images/tablet.png")
        self.img_chip = PhotoImage(file=r"new_images/chip.png")
        self.img_peak = PhotoImage(file=r"new_images/peak.png")
        self.img_clock_reverse = PhotoImage(file=r"new_images/clock_reverse.png")
        self.img_hourglass = PhotoImage(file=r"new_images/hourglass.png")
        self.img_shield = PhotoImage(file=r"new_images/shield.png")

        self.canvas.create_image(234.25, 79.5, image=self.img_tablet)
        self.canvas.create_image(233, 128, image=self.img_chip)
        self.canvas.create_image(234.25, 174.25, image=self.img_peak)
        self.canvas.create_image(238, 244, image=self.img_clock_reverse)
        self.canvas.create_image(753, 81, image=self.img_hourglass)
        self.canvas.create_image(753, 126, image=self.img_hourglass)
        self.canvas.create_image(753, 173, image=self.img_hourglass)

        self.shield1 = self.canvas.create_image(633.25, 78.75, image=self.img_shield)
        self.shield2 = self.canvas.create_image(633.25, 123.75, image=self.img_shield)
        self.shield3 = self.canvas.create_image(633.25, 171.75, image=self.img_shield)
        self.shield4 = self.canvas.create_image(633.25, 245.75, image=self.img_shield)

        self.canvas.create_line(220, 220, 790, 220, fill="gray", width=2)

        self.label1 = tk.Label(self.canvas, text="Копирование данных на USB носитель:", fg='white', bg='black',
                               font=('Roboto Bold', 10))
        self.label1.place(x=218, y=41)
        self.label2 = tk.Label(self.canvas, text="Журнал за 90 дней", fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label2.place(x=256, y=72)
        self.label3 = tk.Label(self.canvas, text="Энергозависимая память", fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label3.place(x=259, y=120)
        self.label4 = tk.Label(self.canvas, text="Тренды", fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label4.place(x=259, y=166)
        self.label5 = tk.Label(self.canvas, text="Сброс всех настроек на заводские", fg='white', bg='black',
                               font=('Roboto Bold', 12))
        self.label5.place(x=259, y=237)
        self.label6 = tk.Label(self.canvas, text="Внимание копирование данных может занять продолжительное время!", fg='white', bg='black',
                               font=('Roboto Bold', 10))
        self.label6.place(x=252, y=307)

        # Кликабельная зона
        self.Switch_Flat_first_img = PhotoImage(file=r"new_images/Switch-0.png")
        self.Switch_Flat_first_button = self.canvas.create_image(694.5, 81, image=self.Switch_Flat_first_img)
        self.canvas.tag_bind(self.Switch_Flat_first_button, "<Button-1>", lambda event: self.check_password("switch1"))

        self.Switch_Flat_second_img = PhotoImage(file=r"new_images/Switch-0.png")
        self.Switch_Flat_second_button = self.canvas.create_image(694.5, 126, image=self.Switch_Flat_second_img)
        self.canvas.tag_bind(self.Switch_Flat_second_button, "<Button-1>", lambda event: self.check_password("switch2"))

        self.Switch_Flat_third_img = PhotoImage(file=r"new_images/Switch-0.png")
        self.Switch_Flat_third_button = self.canvas.create_image(694.5, 173, image=self.Switch_Flat_third_img)
        self.canvas.tag_bind(self.Switch_Flat_third_button, "<Button-1>", lambda event: self.check_password("switch3"))

        self.Switch_Flat_fourth_img = PhotoImage(file=r"new_images/Switch-0.png")
        self.Switch_Flat_fourth_button = self.canvas.create_image(694.5, 246, image=self.Switch_Flat_fourth_img)
        self.canvas.tag_bind(self.Switch_Flat_fourth_button, "<Button-1>", lambda event: self.check_password("switch4"))
        # Кликабельная зона

    def check_password(self, word): #Сверка пароля и вызов необходимого метода, путем слова
        print("check_password")
        if App.session_access == True:
            if App.LVL_access <= 5:
                if word == "switch1": #Переключатель
                    self.update_switch_one()
                elif word == "switch2": #Первое поле
                    self.update_switch_two()
                elif word == "switch3": #Второе поле
                    self.update_switch_three()
                elif word == "switch4": #Второе поле
                    self.update_switch_four()
            else:
                self.keypad_instance = keypad.Keypad()
                self.keypad_instance.grab_set()
                self.keypad_instance.callback_function = self.set_access
        else:
            self.keypad_instance = keypad.Keypad()
            self.keypad_instance.grab_set()
            self.keypad_instance.callback_function = self.set_access
    def set_access(self, event=None):
        print("set_access")
        App.session_access = True
        App.LVL_access = self.keypad_instance.access
        App.shields_hide()
        if App.LVL_access > 5 :
            messagebox.showerror("Ошибка!", "Недостаточно прав!")

    def update_switch_one(self):
        if self.Switch_Flat_first_img.cget("file") == "new_images/Switch-0.png":
            self.Switch_Flat_first_img = PhotoImage(file=r"new_images/Switch-1.png")
        elif self.Switch_Flat_first_img.cget("file") == "new_images/Switch-1.png":
            self.Switch_Flat_first_img = PhotoImage(file=r"new_images/Switch-0.png")
        self.Switch_Flat_first_button = self.canvas.create_image(694.5, 81, image=self.Switch_Flat_first_img)
        self.canvas.tag_bind(self.Switch_Flat_first_button, "<Button-1>", lambda event: self.check_password("switch1"))

    def update_switch_two(self):
        if self.Switch_Flat_second_img.cget("file") == "new_images/Switch-0.png":
            self.Switch_Flat_second_img = PhotoImage(file=r"new_images/Switch-1.png")
        elif self.Switch_Flat_second_img.cget("file") == "new_images/Switch-1.png":
            self.Switch_Flat_second_img = PhotoImage(file=r"new_images/Switch-0.png")
        self.Switch_Flat_second_button = self.canvas.create_image(694.5, 126, image=self.Switch_Flat_second_img)
        self.canvas.tag_bind(self.Switch_Flat_second_button, "<Button-1>", lambda event: self.check_password("switch2"))

    def update_switch_three(self, event):
        if self.Switch_Flat_third_img.cget("file") == "new_images/Switch-0.png":
            self.Switch_Flat_third_img = PhotoImage(file=r"new_images/Switch-1.png")
        elif self.Switch_Flat_third_img.cget("file") == "new_images/Switch-1.png":
            self.Switch_Flat_third_img = PhotoImage(file=r"new_images/Switch-0.png")
        self.Switch_Flat_third_button = self.canvas.create_image(694.5, 173, image=self.Switch_Flat_third_img)
        self.canvas.tag_bind(self.Switch_Flat_third_button, "<Button-1>", lambda event: self.check_password("switch3"))

    def update_switch_four(self, event):
        if self.Switch_Flat_fourth_img.cget("file") == "new_images/Switch-0.png":
            self.Switch_Flat_fourth_img = PhotoImage(file=r"new_images/Switch-1.png")
        elif self.Switch_Flat_fourth_img.cget("file") == "new_images/Switch-1.png":
            self.Switch_Flat_fourth_img = PhotoImage(file=r"new_images/Switch-0.png")
        self.Switch_Flat_fourth_button = self.canvas.create_image(694.5, 246, image=self.Switch_Flat_fourth_img)
        self.canvas.tag_bind(self.Switch_Flat_fourth_button, "<Button-1>", lambda event: self.check_password("switch4"))

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
        self.font = ImageFont.truetype("Roboto-Bold.ttf", 18)
        self.img_screen = Image.open(r"new_images/screen.png")
        self.img_calendar = Image.open(r"new_images/calendar.png")
        self.img_peak = Image.open(r"new_images/peak.png")
        self.img_tablet = Image.open(r"new_images/tablet.png")
        self.img_gear_wheel = Image.open(r"new_images/gear_wheel.png")
        self.img_wrench = Image.open(r"new_images/wrench.png")
        self.img_gear_wheel_bg = Image.open(r"new_images/gear_wheel_bg.png")
        self.img_phone = Image.open(r"new_images/phone.png")
        self.img_right = Image.open(r"new_images/right.png")
        self.img_triangle = Image.open(r"new_images/triangle.png")

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

        self.img_noon = PhotoImage(file=r"new_images/noon.png")
        self.img_scrn = PhotoImage(file=r"new_images/screen.png")
        self.img_note = PhotoImage(file=r"new_images/note.png")
        self.img_cal = PhotoImage(file=r"new_images/calendar.png")
        self.img_time = PhotoImage(file=r"new_images/time.png")
        self.img_ip = PhotoImage(file=r"new_images/ip.png")
        self.img_mask = PhotoImage(file=r"new_images/mask.png")
        self.img_gateway = PhotoImage(file=r"new_images/gateway.png")
        self.img_shield = PhotoImage(file=r"new_images/shield.png")
        self.img_rectangle_l = PhotoImage(file=r"new_images/rectangle_long.png")
        self.img_rectangle_s = PhotoImage(file=r"new_images/rectangle_short.png")

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

        self.shield1 = self.canvas.create_image(624, 70, image=self.img_shield)
        self.shield2 = self.canvas.create_image(624, 109, image=self.img_shield)
        self.shield3 = self.canvas.create_image(624, 147, image=self.img_shield)
        self.shield4 = self.canvas.create_image(461.25, 201.75, image=self.img_shield)
        self.shield5 = self.canvas.create_image(461.25, 242.75, image=self.img_shield)
        self.shield6 = self.canvas.create_image(362.25, 302.75, image=self.img_shield)
        self.shield7 = self.canvas.create_image(362.25, 342.75, image=self.img_shield)
        self.shield8 = self.canvas.create_image(362.25, 380.75, image=self.img_shield)

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
        self.canvas.tag_bind(self.time_rectangle_1, "<Button-1>", lambda event: self.check_password("click1"))
        self.time_display_1 = tk.Label(self.canvas, text=App.storage_data["Time_screensaver_settings_panel"], fg='white', bg='black', font=('Roboto Bold', 12))
        self.time_display_1.place(x=645, y=58)
        self.time_display_1.bind("<Button-1>", lambda event: self.check_password("click1"))
        self.time_label_1 = tk.Label(self.canvas, text="минут", fg='white', bg='black', font=('Roboto Bold', 12))
        self.time_label_1.place(x=738, y=59, width=47, height=19)
        self.time_label_1.bind("<Button-1>", lambda event: self.check_password("click1"))

        self.time_rectangle_2 = self.canvas.create_image(715, 109.5, image=self.img_rectangle_l)
        self.canvas.tag_bind(self.time_rectangle_2, "<Button-1>", lambda event: self.check_password("click2"))
        self.time_display_2 = tk.Label(self.canvas, text=App.storage_data["Time_display_settings_panel"], fg='white', bg='black', font=('Roboto Bold', 12))
        self.time_display_2.place(x=645, y=98)
        self.time_display_2.bind("<Button-1>", lambda event: self.check_password("click2"))
        self.time_label_2 = tk.Label(self.canvas, text="минут", fg='white', bg='black', font=('Roboto Bold', 12))
        self.time_label_2.place(x=738, y=99, width=47, height=19)
        self.time_label_2.bind("<Button-1>", lambda event: self.check_password("click2"))

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

        self.Switch_Flat_img = PhotoImage(file=r"new_images/Switch-0.png") if App.storage_data["Switch_settings_panel"] == "0" else PhotoImage(file=r"new_images/Switch-1.png")
        self.Switch_Flat_button = self.canvas.create_image(670, 152, image=self.Switch_Flat_img)
        self.canvas.tag_bind(self.Switch_Flat_button, "<Button-1>", lambda event: self.check_password("switch"))

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

    def check_password(self, word): #Сверка пароля и вызов необходимого метода, путем слова
        print("check_password")
        if App.session_access == True:
            if App.LVL_access <= 5:
                App.global_controller.frames["Frame8"].update_tree(datetime.now().strftime("%d.%m.%Y"))
                if word == "switch": #Переключатель
                    print("CALL FUNCTION")
                    self.update_switch()
                elif word == "click1": #Первое поле
                    App.numpad_instance = numpad.Numpad(None, "INT")
                    App.numpad_instance.min_value.config(text="0")
                    App.numpad_instance.max_value.config(text="30")
                    App.numpad_instance.new_title(self.label2.cget('text') + " ")
                    App.numpad_instance.entry_label.config(text=self.time_display_1.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click1
                elif word == "click2": #Второе поле
                    App.numpad_instance = numpad.Numpad(None, "INT")
                    App.numpad_instance.min_value.config(text="0")
                    App.numpad_instance.max_value.config(text="30")
                    App.numpad_instance.new_title(self.label3.cget('text') + " ")
                    App.numpad_instance.entry_label.config(text=self.time_display_2.cget('text'))
                    App.numpad_instance.grab_set()
                    App.numpad_instance.callback_function = self.click2
                json_methods.save_data(r"data/desktop_storage.json", App.storage_data)
            else:
                self.keypad_instance = keypad.Keypad()
                self.keypad_instance.grab_set()
                self.keypad_instance.callback_function = self.set_access
        else:
            self.keypad_instance = keypad.Keypad()
            self.keypad_instance.grab_set()
            self.keypad_instance.callback_function = self.set_access

    #Получение доступа
    def set_access(self, event=None):
        print("set_access")
        App.session_access = True
        App.LVL_access = self.keypad_instance.access
        App.shields_hide()
        if App.LVL_access > 5:
            messagebox.showerror("Ошибка!", "Недостаточно прав!")

    def click1(self):
        App.storage_data["Time_screensaver_settings_panel"] = App.numpad_instance.current_value
        App.global_controller.frames["Frame19"].time_display_1.config(text=App.numpad_instance.current_value)
    def click2(self):
        App.storage_data["Time_display_settings_panel"] = App.numpad_instance.current_value
        App.global_controller.frames["Frame19"].time_display_2.config(text=App.numpad_instance.current_value)


    def update_switch(self):  # Смена переключателей
        print("step 1")
        if self.Switch_Flat_img.cget("file") == r"new_images/Switch-0.png":
            self.Switch_Flat_img = PhotoImage(file=r"new_images/Switch-1.png")
            print("step 2")
            App.storage_data["Switch_settings_panel"] = "1"
        elif self.Switch_Flat_img.cget("file") == r"new_images/Switch-1.png":
            self.Switch_Flat_img = PhotoImage(file=r"new_images/Switch-0.png")
            print("step 3")
            App.storage_data["Switch_settings_panel"] = "0"
        self.Switch_Flat_button = self.canvas.create_image(670, 152, image=self.Switch_Flat_img)
        self.canvas.tag_bind(self.Switch_Flat_button, "<Button-1>", lambda event: self.check_password("switch"))
        self.canvas.update()
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
        self.img_screen = Image.open(r"new_images/screen.png")
        self.img_calendar = Image.open(r"new_images/calendar.png")
        self.img_peak = Image.open(r"new_images/peak.png")
        self.img_tablet = Image.open(r"new_images/tablet.png")
        self.img_gear_wheel = Image.open(r"new_images/gear_wheel.png")
        self.img_wrench = Image.open(r"new_images/wrench.png")
        self.img_gear_wheel_bg = Image.open(r"new_images/gear_wheel_bg.png")
        self.img_phone = Image.open(r"new_images/phone.png")
        self.img_right = Image.open(r"new_images/right.png")
        self.img_triangle = Image.open(r"new_images/triangle.png")

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

        self.img_question = PhotoImage(file=r"new_images/question.png")
        self.img_key = PhotoImage(file=r"new_images/key.png")
        self.img_swap = PhotoImage(file=r"new_images/swap.png")
        self.img_cal = PhotoImage(file=r"new_images/calendar.png")
        self.img_mail = PhotoImage(file=r"new_images/mail.png")
        self.img_site = PhotoImage(file=r"new_images/site.png")
        self.img_support = PhotoImage(file=r"new_images/support.png")
        self.img_shield = PhotoImage(file=r"new_images/shield.png")

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
        self.pumpsAll_label = tk.Label(self.canvas, text="6", fg='white', bg='black', font=('Roboto Bold', 12))
        self.pumpsAll_label.place(x=444, y=207)
        self.pumpsWorking_label = tk.Label(self.canvas, text=App.storage_data["Pumps"], fg='white', bg='black', font=('Roboto Bold', 12))
        self.pumpsWorking_label.place(x=651, y=207)
        self.pumpsWorking_label.bind("<Button-1>", lambda event: self.check_password())

        self.shield1 = self.canvas.create_image(695.25, 216.75, image=self.img_shield)

    def check_password(self):
        print("check_password")
        if App.session_access == True:
            if App.LVL_access <= 0:
                App.numpad_instance = numpad.Numpad(None, "INT")
                App.numpad_instance.max_value.config(text="6")
                App.numpad_instance.min_value.config(text="1")
                App.numpad_instance.new_title("Насосы ")
                App.numpad_instance.entry_label.config(text=self.pumpsWorking_label.cget('text'))
                App.numpad_instance.grab_set()
                App.numpad_instance.callback_function = self.change_active_pumps
                json_methods.save_data(r"data/desktop_storage.json", App.storage_data)
            else:
                messagebox.showerror("Ошибка!", "Недостаточно прав!")
        else:
            self.keypad_instance = keypad.Keypad()
            self.keypad_instance.grab_set()
            self.keypad_instance.callback_function = self.set_access

    def set_access(self, event=None):
        print("set_access")
        App.session_access = True
        App.LVL_access = self.keypad_instance.access
        App.shields_hide()
        if App.LVL_access > 0:
            messagebox.showerror("Ошибка!", "Недостаточно прав!")

    def change_active_pumps(self):
        App.Pumps_active = int(App.numpad_instance.current_value)
        App.storage_data["Pumps"] = str(App.Pumps_active)
        json_methods.save_data(r"data/desktop_storage.json", App.storage_data)
        App.global_controller.frames["Frame20"].pumpsWorking_label.config(text=App.Pumps_active)
        App.global_controller.frames["Frame1_1"].canvas.delete(App.global_controller.frames["Frame1_1"].Pump_six)
        App.global_controller.frames["Frame1_1"].canvas.delete(App.global_controller.frames["Frame1_1"].Pump_five)
        App.global_controller.frames["Frame1_1"].canvas.delete(App.global_controller.frames["Frame1_1"].Pump_four)
        App.global_controller.frames["Frame1_1"].canvas.delete(App.global_controller.frames["Frame1_1"].Pump_three)
        App.global_controller.frames["Frame1_1"].canvas.delete(App.global_controller.frames["Frame1_1"].Pump_two)
        App.global_controller.frames["Frame1_1"].canvas.delete(App.global_controller.frames["Frame1_1"].Pump_one)
        App.global_controller.frames["Frame1_2"].canvas.delete(App.global_controller.frames["Frame1_2"].Pump_six)
        App.global_controller.frames["Frame1_2"].canvas.delete(App.global_controller.frames["Frame1_2"].Pump_five)
        App.global_controller.frames["Frame1_2"].canvas.delete(App.global_controller.frames["Frame1_2"].Pump_four)
        App.global_controller.frames["Frame1_2"].canvas.delete(App.global_controller.frames["Frame1_2"].Pump_three)
        App.global_controller.frames["Frame1_2"].canvas.delete(App.global_controller.frames["Frame1_2"].Pump_two)
        App.global_controller.frames["Frame1_2"].canvas.delete(App.global_controller.frames["Frame1_2"].Pump_one)
        App.global_controller.frames["Frame1_3"].canvas.delete(App.global_controller.frames["Frame1_3"].Pump_six)
        App.global_controller.frames["Frame1_3"].canvas.delete(App.global_controller.frames["Frame1_3"].Pump_five)
        App.global_controller.frames["Frame1_3"].canvas.delete(App.global_controller.frames["Frame1_3"].Pump_four)
        App.global_controller.frames["Frame1_3"].canvas.delete(App.global_controller.frames["Frame1_3"].Pump_three)
        App.global_controller.frames["Frame1_3"].canvas.delete(App.global_controller.frames["Frame1_3"].Pump_two)
        App.global_controller.frames["Frame1_3"].canvas.delete(App.global_controller.frames["Frame1_3"].Pump_one)
        App.global_controller.frames["Frame1_4"].canvas.delete(App.global_controller.frames["Frame1_4"].Pump_six)
        App.global_controller.frames["Frame1_4"].canvas.delete(App.global_controller.frames["Frame1_4"].Pump_five)
        App.global_controller.frames["Frame1_4"].canvas.delete(App.global_controller.frames["Frame1_4"].Pump_four)
        App.global_controller.frames["Frame1_4"].canvas.delete(App.global_controller.frames["Frame1_4"].Pump_three)
        App.global_controller.frames["Frame1_4"].canvas.delete(App.global_controller.frames["Frame1_4"].Pump_two)
        App.global_controller.frames["Frame1_4"].canvas.delete(App.global_controller.frames["Frame1_4"].Pump_one)
        App.global_controller.frames["Frame1_1"].initialization_pumps(App.Pumps_active)
        App.global_controller.frames["Frame1_2"].initialization_pumps(App.Pumps_active)
        App.global_controller.frames["Frame1_3"].initialization_pumps(App.Pumps_active)
        App.global_controller.frames["Frame1_4"].initialization_pumps(App.Pumps_active)

    def update_clock(self, current_time):
        self.clock_label.config(text=current_time)


app = App()
app.mainloop()

