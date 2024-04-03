import tkinter as tk
from datetime import datetime


class App(tk.Tk):
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

        for F in (Frame1, Frame2):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Frame1")

        self.update_clock()

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

        if page_name == "Frame1":
            self.title("Главный экран")  # Изменяем название окна для Frame1
        elif page_name == "Frame2":
            self.title("Настройки")  # Изменяем название окна для Frame2

    def update_clock(self):
        current_time = datetime.now().strftime('%d/%m/%y %H:%M')
        for frame_name in self.frames:
            self.frames[frame_name].update_clock(current_time)
        self.after(1000, self.update_clock)


class Frame1(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='black')

        self.clock_label = tk.Label(self, text="", fg='white', bg='black', font=('Roboto Bold', 12))
        self.clock_label.pack(anchor='ne', padx=10, pady=10)

        button = tk.Button(self, text="Настройки", command=lambda: controller.show_frame("Frame2"))
        button.pack(pady=10)

    def update_clock(self, current_time):
        self.clock_label.config(text=current_time)


class Frame2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='black')

        self.clock_label = tk.Label(self, text="", fg='white', bg='black', font=('Roboto Bold', 12))
        self.clock_label.pack(anchor='ne', padx=10, pady=10)

        button = tk.Button(self, text="Главный экран", command=lambda: controller.show_frame("Frame1"))
        button.pack(pady=10)

    def update_clock(self, current_time):
        self.clock_label.config(text=current_time)


app = App()
app.mainloop()
