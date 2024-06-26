import tkinter as tk
class Numpad(tk.Toplevel):
    def __init__(self, master=None, word=None):
        super().__init__(master)
        self.title("Нумпад")
        self.geometry("300x400")
        self.resizable(width=False, height=False)
        self.canvas = tk.Canvas(
            self,
            bg="#626262",
            height=400,
            width=300,
            bd=0,
            highlightthickness=0,
            relief="ridge")
        self.canvas.place(x=0, y=0)
        self.word = word
        # Ключ слово определяющее каким будет число(его форма) в нумпаде
        #    1/  1.0 / 1.00 / 1.000
        # int/float1/float2/float3
        self.current_title = "" #Название окна
        self.entry_label = tk.Label(self.canvas, text="", fg='white', bg='black', font=('Roboto Bold', 16), width=20, anchor='e')
        self.entry_label.place(x=15, y=54, width=271, height=51)

        self.button_seven = tk.Button(self, text='7', font=('Roboto Bold', 18), bg='black', fg='white', relief="groove",
                                activebackground="black", activeforeground="white", command=self.seven_func)
        self.button_seven.place(x=15, y=114, width=61, height=61)
        self.button_eight = tk.Button(self, text='8', font=('Roboto Bold', 18), bg='black', fg='white', relief="groove",
                                      activebackground="black", activeforeground="white", command=self.eight_func)
        self.button_eight.place(x=85, y=114, width=61, height=61)
        self.button_nine = tk.Button(self, text='9', font=('Roboto Bold', 18), bg='black', fg='white', relief="groove",
                                      activebackground="black", activeforeground="white", command=self.nine_func)
        self.button_nine.place(x=155, y=114, width=61, height=61)
        self.button_C = tk.Button(self, text='C', font=('Roboto Bold', 18), bg='#8E0000', fg='white', relief="groove",
                                      activebackground="#8E0000", activeforeground="white", command=self.clear_all_button_func)
        self.button_C.place(x=225, y=114, width=61, height=61)

        self.button_four = tk.Button(self, text='4', font=('Roboto Bold', 18), bg='black', fg='white', relief="groove",
                                      activebackground="black", activeforeground="white", command=self.four_func)
        self.button_four.place(x=15, y=184, width=61, height=61)
        self.button_five = tk.Button(self, text='5', font=('Roboto Bold', 18), bg='black', fg='white', relief="groove",
                                      activebackground="black", activeforeground="white", command=self.five_func)
        self.button_five.place(x=85, y=184, width=61, height=61)
        self.button_six = tk.Button(self, text='6', font=('Roboto Bold', 18), bg='black', fg='white', relief="groove",
                                     activebackground="black", activeforeground="white", command=self.six_func)
        self.button_six.place(x=155, y=184, width=61, height=61)
        self.button_del = tk.Button(self, text='<-', font=('Roboto Bold', 18), bg='black', fg='white', relief="groove",
                                  activebackground="black", activeforeground="white", command=self.clear_button_func)
        self.button_del.place(x=225, y=184, width=61, height=61)

        self.button_one = tk.Button(self, text='1', font=('Roboto Bold', 18), bg='black', fg='white', relief="groove",
                                     activebackground="black", activeforeground="white", command=self.one_func)
        self.button_one.place(x=15, y=254, width=61, height=61)
        self.button_two = tk.Button(self, text='2', font=('Roboto Bold', 18), bg='black', fg='white', relief="groove",
                                     activebackground="black", activeforeground="white", command=self.two_func)
        self.button_two.place(x=85, y=254, width=61, height=61)
        self.button_three = tk.Button(self, text='3', font=('Roboto Bold', 18), bg='black', fg='white', relief="groove",
                                    activebackground="black", activeforeground="white", command=self.three_func)
        self.button_three.place(x=155, y=254, width=61, height=61)
        self.button_esc = tk.Button(self, text='Esc', font=('Roboto Bold', 18), bg='black', fg='white', relief="groove",
                                    activebackground="black", activeforeground="white", command=self.escape_button_func)
        self.button_esc.place(x=225, y=254, width=61, height=61)

        self.button_comma = tk.Button(self, text='.', font=('Roboto Bold', 18), bg='black', fg='white', relief="groove",
                                    activebackground="black", activeforeground="white", command=self.cammo_func)
        self.button_comma.place(x=15, y=324, width=61, height=61)
        self.button_zero = tk.Button(self, text='0', font=('Roboto Bold', 18), bg='black', fg='white', relief="groove",
                                      activebackground="black", activeforeground="white", command=self.zero_func)
        self.button_zero.place(x=85, y=324, width=61, height=61)
        self.button_enter = tk.Button(self, text='Enter', font=('Roboto Bold', 18), bg='#008000', fg='white', relief="groove",
                                    activebackground="#008000", activeforeground="white", command=self.enter_button_func)
        self.button_enter.place(x=155, y=324, width=131, height=61)

        self.min_label = tk.Label(self.canvas, text="MIN:", fg='white', bg='#626262', font=('Roboto Bold', 16))
        self.min_label.place(x=14, y=17)
        self.min_value = tk.Label(self.canvas, text="0", fg='white', bg='#626262', font=('Roboto Bold', 16))
        self.min_value.place(x=62, y=17)
        self.max_label = tk.Label(self.canvas, text="MAX:", fg='white', bg='#626262', font=('Roboto Bold', 16))
        self.max_label.place(x=165, y=17)
        self.max_value = tk.Label(self.canvas, text="30", fg='white', bg='#626262', font=('Roboto Bold', 16))
        self.max_value.place(x=220, y=17)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        pass

    def cammo_func(self):
        if self.word != "INT":
            if self.entry_label.cget('text') != "":
                if "." not in self.entry_label.cget('text'):
                    self.entry_label.config(text=self.entry_label.cget('text') + ".")

    def zero_func(self):
        if self.word == "FLOAT3":
            if len(str(self.entry_label.cget('text'))) != 5:
                self.entry_label.config(text=str(self.entry_label.cget('text')) + "0")
        elif self.word == "FLOAT2":
            if '.' in str(self.entry_label.cget('text')):
                if len(str(self.entry_label.cget('text')).split('.')[1]) != 2:
                    self.entry_label.config(text=str(self.entry_label.cget('text')) + "0")
            else:
                self.entry_label.config(text=str(self.entry_label.cget('text')) + "0")
        elif self.word == "FLOAT1":
            if '.' in str(self.entry_label.cget('text')):
                if len(str(self.entry_label.cget('text')).split('.')[1]) != 1:
                    self.entry_label.config(text=str(self.entry_label.cget('text')) + "0")
            else:
                self.entry_label.config(text=str(self.entry_label.cget('text')) + "0")
        elif self.word == "INT":
            if len(str(self.entry_label.cget('text'))) != 8:
                self.entry_label.config(text=str(self.entry_label.cget('text')) + "0")

    def one_func(self):
        if self.word == "FLOAT3":
            if len(str(self.entry_label.cget('text'))) != 5:
                self.entry_label.config(text=str(self.entry_label.cget('text')) + "1")
        elif self.word == "FLOAT2":
            if '.' in str(self.entry_label.cget('text')):
                if len(str(self.entry_label.cget('text')).split('.')[1]) != 2:
                    self.entry_label.config(text=str(self.entry_label.cget('text')) + "1")
            else:
                self.entry_label.config(text=str(self.entry_label.cget('text')) + "1")
        elif self.word == "FLOAT1":
            if '.' in str(self.entry_label.cget('text')):
                if len(str(self.entry_label.cget('text')).split('.')[1]) != 1:
                    self.entry_label.config(text=str(self.entry_label.cget('text')) + "1")
            else:
                self.entry_label.config(text=str(self.entry_label.cget('text')) + "1")
        elif self.word == "INT":
            if len(str(self.entry_label.cget('text'))) != 8:
                self.entry_label.config(text=str(self.entry_label.cget('text')) + "1")

    def two_func(self):
        if self.word == "FLOAT3":
            if len(str(self.entry_label.cget('text'))) != 5:
                self.entry_label.config(text=str(self.entry_label.cget('text')) + "2")
        elif self.word == "FLOAT2":
            if '.' in str(self.entry_label.cget('text')):
                if len(str(self.entry_label.cget('text')).split('.')[1]) != 2:
                    self.entry_label.config(text=str(self.entry_label.cget('text')) + "2")
            else:
                self.entry_label.config(text=str(self.entry_label.cget('text')) + "2")
        elif self.word == "FLOAT1":
            if '.' in str(self.entry_label.cget('text')):
                if len(str(self.entry_label.cget('text')).split('.')[1]) != 1:
                    self.entry_label.config(text=str(self.entry_label.cget('text')) + "2")
            else:
                self.entry_label.config(text=str(self.entry_label.cget('text')) + "2")
        elif self.word == "INT":
            if len(str(self.entry_label.cget('text'))) != 8:
                self.entry_label.config(text=str(self.entry_label.cget('text')) + "2")

    def three_func(self):
        if self.word == "FLOAT3":
            if len(str(self.entry_label.cget('text'))) != 5:
                self.entry_label.config(text=str(self.entry_label.cget('text')) + "3")
        elif self.word == "FLOAT2":
            if '.' in str(self.entry_label.cget('text')):
                if len(str(self.entry_label.cget('text')).split('.')[1]) != 2:
                    self.entry_label.config(text=str(self.entry_label.cget('text')) + "3")
            else:
                self.entry_label.config(text=str(self.entry_label.cget('text')) + "3")
        elif self.word == "FLOAT1":
            if '.' in str(self.entry_label.cget('text')):
                if len(str(self.entry_label.cget('text')).split('.')[1]) != 1:
                    self.entry_label.config(text=str(self.entry_label.cget('text')) + "3")
            else:
                self.entry_label.config(text=str(self.entry_label.cget('text')) + "3")
        elif self.word == "INT":
            if len(str(self.entry_label.cget('text'))) != 8:
                self.entry_label.config(text=str(self.entry_label.cget('text')) + "3")

    def four_func(self):
        if self.word == "FLOAT3":
            if len(str(self.entry_label.cget('text'))) != 5:
                self.entry_label.config(text=str(self.entry_label.cget('text')) + "4")
        elif self.word == "FLOAT2":
            if '.' in str(self.entry_label.cget('text')):
                if len(str(self.entry_label.cget('text')).split('.')[1]) != 2:
                    self.entry_label.config(text=str(self.entry_label.cget('text')) + "4")
            else:
                self.entry_label.config(text=str(self.entry_label.cget('text')) + "4")
        elif self.word == "FLOAT1":
            if '.' in str(self.entry_label.cget('text')):
                if len(str(self.entry_label.cget('text')).split('.')[1]) != 1:
                    self.entry_label.config(text=str(self.entry_label.cget('text')) + "4")
            else:
                self.entry_label.config(text=str(self.entry_label.cget('text')) + "4")
        elif self.word == "INT":
            if len(str(self.entry_label.cget('text'))) != 8:
                self.entry_label.config(text=str(self.entry_label.cget('text')) + "4")

    def five_func(self):
        if self.word == "FLOAT3":
            if len(str(self.entry_label.cget('text'))) != 5:
                self.entry_label.config(text=str(self.entry_label.cget('text')) + "5")
        elif self.word == "FLOAT2":
            if '.' in str(self.entry_label.cget('text')):
                if len(str(self.entry_label.cget('text')).split('.')[1]) != 2:
                    self.entry_label.config(text=str(self.entry_label.cget('text')) + "5")
            else:
                self.entry_label.config(text=str(self.entry_label.cget('text')) + "5")
        elif self.word == "FLOAT1":
            if '.' in str(self.entry_label.cget('text')):
                if len(str(self.entry_label.cget('text')).split('.')[1]) != 1:
                    self.entry_label.config(text=str(self.entry_label.cget('text')) + "5")
            else:
                self.entry_label.config(text=str(self.entry_label.cget('text')) + "5")
        elif self.word == "INT":
            if len(str(self.entry_label.cget('text'))) != 8:
                self.entry_label.config(text=str(self.entry_label.cget('text')) + "5")

    def six_func(self):
        if self.word == "FLOAT3":
            if len(str(self.entry_label.cget('text'))) != 5:
                self.entry_label.config(text=str(self.entry_label.cget('text')) + "6")
        elif self.word == "FLOAT2":
            if '.' in str(self.entry_label.cget('text')):
                if len(str(self.entry_label.cget('text')).split('.')[1]) != 2:
                    self.entry_label.config(text=str(self.entry_label.cget('text')) + "6")
            else:
                self.entry_label.config(text=str(self.entry_label.cget('text')) + "6")
        elif self.word == "FLOAT1":
            if '.' in str(self.entry_label.cget('text')):
                if len(str(self.entry_label.cget('text')).split('.')[1]) != 1:
                    self.entry_label.config(text=str(self.entry_label.cget('text')) + "6")
            else:
                self.entry_label.config(text=str(self.entry_label.cget('text')) + "6")
        elif self.word == "INT":
            if len(str(self.entry_label.cget('text'))) != 8:
                self.entry_label.config(text=str(self.entry_label.cget('text')) + "6")

    def seven_func(self):
        if self.word == "FLOAT3":
            if len(str(self.entry_label.cget('text'))) != 5:
                self.entry_label.config(text=str(self.entry_label.cget('text')) + "7")
        elif self.word == "FLOAT2":
            if '.' in str(self.entry_label.cget('text')):
                if len(str(self.entry_label.cget('text')).split('.')[1]) != 2:
                    self.entry_label.config(text=str(self.entry_label.cget('text')) + "7")
            else:
                self.entry_label.config(text=str(self.entry_label.cget('text')) + "7")
        elif self.word == "FLOAT1":
            if '.' in str(self.entry_label.cget('text')):
                if len(str(self.entry_label.cget('text')).split('.')[1]) != 1:
                    self.entry_label.config(text=str(self.entry_label.cget('text')) + "7")
            else:
                self.entry_label.config(text=str(self.entry_label.cget('text')) + "7")
        elif self.word == "INT":
            if len(str(self.entry_label.cget('text'))) != 8:
                self.entry_label.config(text=str(self.entry_label.cget('text')) + "7")

    def eight_func(self):
        if self.word == "FLOAT3":
            if len(str(self.entry_label.cget('text'))) != 5:
                self.entry_label.config(text=str(self.entry_label.cget('text')) + "8")
        elif self.word == "FLOAT2":
            if '.' in str(self.entry_label.cget('text')):
                if len(str(self.entry_label.cget('text')).split('.')[1]) != 2:
                    self.entry_label.config(text=str(self.entry_label.cget('text')) + "8")
            else:
                self.entry_label.config(text=str(self.entry_label.cget('text')) + "8")
        elif self.word == "FLOAT1":
            if '.' in str(self.entry_label.cget('text')):
                if len(str(self.entry_label.cget('text')).split('.')[1]) != 1:
                    self.entry_label.config(text=str(self.entry_label.cget('text')) + "8")
            else:
                self.entry_label.config(text=str(self.entry_label.cget('text')) + "8")
        elif self.word == "INT":
            if len(str(self.entry_label.cget('text'))) != 8:
                self.entry_label.config(text=str(self.entry_label.cget('text')) + "8")

    def nine_func(self):
        if self.word == "FLOAT3":
            if len(str(self.entry_label.cget('text'))) != 5:
                self.entry_label.config(text=str(self.entry_label.cget('text')) + "9")
        elif self.word == "FLOAT2":
            if '.' in str(self.entry_label.cget('text')):
                if len(str(self.entry_label.cget('text')).split('.')[1]) != 2:
                    self.entry_label.config(text=str(self.entry_label.cget('text')) + "9")
            else:
                self.entry_label.config(text=str(self.entry_label.cget('text')) + "9")
        elif self.word == "FLOAT1":
            if '.' in str(self.entry_label.cget('text')):
                if len(str(self.entry_label.cget('text')).split('.')[1]) != 1:
                    self.entry_label.config(text=str(self.entry_label.cget('text')) + "9")
            else:
                self.entry_label.config(text=str(self.entry_label.cget('text')) + "9")
        elif self.word == "INT":
            if len(str(self.entry_label.cget('text'))) != 8:
                self.entry_label.config(text=str(self.entry_label.cget('text')) + "9")


    def clear_all_button_func(self):
        self.entry_label.config(text="")

    def clear_button_func(self):
        past_text = str(self.entry_label.cget('text'))
        new_text = past_text[:-1]
        self.entry_label.config(text=new_text)

    def enter_button_func(self):
        self.current_value = self.entry_label.cget('text')
        if self.current_value != "":
            if self.word == "INT":
                self.current_value = int(self.current_value)
                if int(self.min_value.cget('text')) <= self.current_value <= int(self.max_value.cget('text')):
                    self.current_value = str(self.current_value)
                else:
                    return
            elif self.word == "FLOAT3":
                self.current_value = float(self.current_value)
                if float(self.min_value.cget('text')) <= self.current_value <= float(self.max_value.cget('text')):
                    self.current_value = str(self.current_value)
                    for _ in range(5 - len(self.current_value)):
                        self.current_value += "0"
                else:
                    return
            elif self.word == "FLOAT2":
                self.current_value = float(self.current_value)
                if float(self.min_value.cget('text')) <= self.current_value <= float(self.max_value.cget('text')):
                    self.current_value = str(self.current_value)
                    for _ in range(2-len(self.current_value.split('.')[1])):
                        self.current_value += "0"
                else:
                    return
            elif self.word == "FLOAT1":
                self.current_value = float(self.current_value)
                if float(self.min_value.cget('text')) <= self.current_value <= float(self.max_value.cget('text')):
                    self.current_value = str(self.current_value)
                else:
                    return
            self.entry_label.config(text="")
            print("Успешный ввод!")
            #После ввода вызов обратной функции, если она есть
            if self.callback_function:
                self.callback_function()
                self.destroy()

    def escape_button_func(self):
        self.destroy()

    def new_title(self, new_title):
        # Установки названия поля
        self.current_title = new_title
        self.after(200, self.update_title)
    def update_title(self):
        #Создание "бегущей" строки
        next_title = self.current_title[1:] + self.current_title[0]
        self.title(next_title)
        self.current_title = next_title
        self.after(200, self.update_title)


#app = Numpad()
#app.mainloop()