import tkinter as tk
from tkinter import PhotoImage, Canvas, messagebox
class Keypad(tk.Tk):
    def __init__(self, master=None, ):
        super().__init__(master)
        self.title("Главный экран")
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

        self.password = "123"
        self.enter_password = ""

        self.entry_label = tk.Label(self.canvas, text="", fg='white', bg='black', font=('Roboto Bold', 16), width=20, anchor='e')
        self.entry_label.place(x=15, y=54, width=271, height=51)

        self.info_label = tk.Label(self.canvas, text="Введите пароль", fg='#A70000', bg='black', font=('Roboto Bold', 18),
                                    anchor='c')
        self.info_label.place(x=0, y=0, width=300, height=39)

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

        self.button_comma = tk.Button(self, text=',', font=('Roboto Bold', 18), bg='black', fg='white', relief="groove",
                                    activebackground="black", activeforeground="white")
        self.button_comma.place(x=15, y=324, width=61, height=61)
        self.button_zero = tk.Button(self, text='0', font=('Roboto Bold', 18), bg='black', fg='white', relief="groove",
                                      activebackground="black", activeforeground="white", command=self.zero_func)
        self.button_zero.place(x=85, y=324, width=61, height=61)
        self.button_enter = tk.Button(self, text='Enter', font=('Roboto Bold', 18), bg='#008000', fg='white', relief="groove",
                                    activebackground="#008000", activeforeground="white", command=self.enter_button_func)
        self.button_enter.place(x=155, y=324, width=131, height=61)


    ''' ЗАПЯТАЯ 
    def cammo_func(self, event):
        self.enter_password.config(text=self.enter_password.cget('text')+",")
    '''
    def zero_func(self):
        if len(self.enter_password) != 8:
            self.enter_password = self.enter_password + "0"
            self.entry_label.config(text=self.entry_label.cget('text')+"*")
    def one_func(self):
        if len(self.enter_password) != 8:
            self.enter_password = self.enter_password + "1"
            self.entry_label.config(text=self.entry_label.cget('text')+"*")
    def two_func(self):
        if len(self.enter_password) != 8:
            self.enter_password = self.enter_password + "2"
            self.entry_label.config(text=self.entry_label.cget('text')+"*")
    def three_func(self):
        if len(self.enter_password) != 8:
            self.enter_password = self.enter_password + "3"
            self.entry_label.config(text=self.entry_label.cget('text')+"*")
    def four_func(self):
        if len(self.enter_password) != 8:
            self.enter_password = self.enter_password + "4"
            self.entry_label.config(text=self.entry_label.cget('text')+"*")
    def five_func(self):
        if len(self.enter_password) != 8:
            self.enter_password = self.enter_password + "5"
            self.entry_label.config(text=self.entry_label.cget('text')+"*")
    def six_func(self):
        if len(self.enter_password) != 8:
            self.enter_password = self.enter_password + "6"
            self.entry_label.config(text=self.entry_label.cget('text')+"*")
    def seven_func(self):
        if len(self.enter_password) != 8:
            self.enter_password = self.enter_password + "7"
            self.entry_label.config(text=self.entry_label.cget('text')+"*")
    def eight_func(self):
        if len(self.enter_password) != 8:
            self.enter_password = self.enter_password + "8"
            self.entry_label.config(text=self.entry_label.cget('text')+"*")
    def nine_func(self):
        if len(self.enter_password) != 8:
            self.enter_password = self.enter_password + "9"
            self.entry_label.config(text=self.entry_label.cget('text')+"*")
    def clear_all_button_func(self):
        self.enter_password = ""
        self.entry_label.config(text="")
    def clear_button_func(self):
        past_text = self.entry_label.cget('text')
        new_text = past_text[:-1]
        self.enter_password = self.enter_password[:-1]
        self.entry_label.config(text=new_text)
    def enter_button_func(self):
        if self.enter_password == self.password:

            self.entry_label.config(text="")
            print("Успешный вход!")
            if self.callback_function:
                self.callback_function()
            self.destroy()
            self.enter_password = ""

        else:
            messagebox.showerror("Ошибка!", "Введен неправильный пароль!")

    def escape_button_func(self):
        self.destroy()


#app = Keypad()
#app.mainloop()