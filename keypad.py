import tkinter as tk
from tkinter import END
from tkinter.messagebox import showinfo


# noinspection PyTypeChecker
class Keypad(tk.Tk):
    password="12345678"
    r = ""
    def __init__(self):
        super().__init__()

        self.geometry("300x400")
        self.configure(bg='gray')

        def clear():
            self.entry.delete("0", END)

        def delete():
            self.entry.delete("0", END)
            self.r = self.r[:-1]
            self.entry.insert(END, self.r)

        def esc():
            app.destroy()

        def enter():
            if self.r==self.password:
                showinfo("Информация", "Вход выполнен")
            else:
                app.destroy()


        def typing(text):
            self.entry.insert(END, "*")
            self.r += text

        self.label = tk.Label(self, width=25, text="Введите пароль", font=('Roboto Bold', 16), bg='black', fg='red')
        self.label.place(height=40, x=1, y=1)
        self.entry = tk.Entry(self, width=13, font=('Roboto Bold', 28), bg='black', fg='white', justify="right")
        self.entry.insert(0, "*")
        self.entry.place(height=50, x=15, y=55)
        self.button7 = tk.Button(self, text="7", font=('Roboto Bold', 14), height=2, width=5, bg="black", fg="white", command=lambda: typing("7"))
        self.button7.place(x=15, y=115)
        self.button8 = tk.Button(self, text="8", font=('Roboto Bold', 14), height=2, width=5, bg="black", fg="white", command=lambda: typing("8"))
        self.button8.place(x=85, y=115)
        self.button9 = tk.Button(self, text="9", font=('Roboto Bold', 14), height=2, width=5, bg="black", fg="white", command=lambda: typing("9"))
        self.button9.place(x=155, y=115)
        self.buttonC = tk.Button(self, text="C", font=('Roboto Bold', 14), height=2, width=5, bg="red", fg="white", command=clear)
        self.buttonC.place(x=225, y=115)
        self.button4 = tk.Button(self, text="4", font=('Roboto Bold', 14), height=2, width=5, bg="black", fg="white", command=lambda: typing("4"))
        self.button4.place(x=15, y=185)
        self.button5 = tk.Button(self, text="5", font=('Roboto Bold', 14), height=2, width=5, bg="black", fg="white", command=lambda: typing("5"))
        self.button5.place(x=85, y=185)
        self.button6 = tk.Button(self, text="6", font=('Roboto Bold', 14), height=2, width=5, bg="black", fg="white", command=lambda: typing("6"))
        self.button6.place(x=155, y=185)
        self.buttonD = tk.Button(self, text="<-", font=('Roboto Bold', 14), height=2, width=5, bg="black", fg="white", command=delete)
        self.buttonD.place(x=225, y=185)
        self.button1 = tk.Button(self, text="1", font=('Roboto Bold', 14), height=2, width=5, bg="black", fg="white", command=lambda: typing("1"))
        self.button1.place(x=15, y=255)
        self.button2 = tk.Button(self, text="2", font=('Roboto Bold', 14), height=2, width=5, bg="black", fg="white", command=lambda: typing("2"))
        self.button2.place(x=85, y=255)
        self.button3 = tk.Button(self, text="3", font=('Roboto Bold', 14), height=2, width=5, bg="black", fg="white", command=lambda: typing("3"))
        self.button3.place(x=155, y=255)
        self.buttonEsc = tk.Button(self, text="Esc", font=('Roboto Bold', 14), height=2, width=5, bg="black", fg="white", command=esc)
        self.buttonEsc.place(x=225, y=255)
        self.buttonZ = tk.Button(self, text=",", font=('Roboto Bold', 14), height=2, width=5, bg="black", fg="white", command=lambda: typing(","))
        self.buttonZ.place(x=15, y=325)
        self.button0 = tk.Button(self, text="0", font=('Roboto Bold', 14), height=2, width=5, bg="black", fg="white", command=lambda: typing("0"))
        self.button0.place(x=85, y=325)
        self.buttonEsc = tk.Button(self, text="Enter", font=('Roboto Bold', 14), height=2, width=11, bg="green", fg="white", command=enter)
        self.buttonEsc.place(x=155, y=325)


app = Keypad()
app.mainloop()
