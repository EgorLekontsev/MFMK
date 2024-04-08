import tkinter as tk

root = tk.Tk()
root.geometry("601x270")
root.configure(bg="#606060")
root.resizable(False, False)
root.title("Клавиатура")


numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
for n in range(len(numbers)):
    button = tk.Button(bg="#a5a5a5", fg="white", font=('Roboto Bold', 12), text=numbers[n], command=lambda text=numbers[n]: print(text))
    button.place(x=n*55+0, y=0, height=50, width=51)

alp_ru = [["й", "ц", "у", "к", "е", "н", "г", "ш", "щ", "з", "х"],
          ["ф", "ы", "в", "а", "п", "р", "о", "л", "д", "ж", "э"],
          ["я", "ч", "с", "м", "и", "т", "ь", "ъ", "б", "ю"]]
alp_RU = [["Й", "Ц", "У", "К", "Е", "Н", "Г", "Ш", "Щ", "З", "Х"],
          ["Ф", "Ы", "В", "А", "П", "Р", "О", "Л", "Д", "Ж", "Э"],
          ["Я", "Ч", "С", "М", "И", "Т", "Ь", "Ъ", "Б", "Ю"]]
alp_en = [["q","w","e","r","t","y","u","i","o","p"],
       ["a","s","d","f","g","h","j","k","l"],
       ["z","x","c","v","b","n","m"]]
alp_EN = [["Q","W","E","R","T","Y","U","I","O","P"],
          ["A","S","D","F","G","H","J","K","L"],
          ["Z","X","C","V","B","N","M"]]

buttons = []

def alp_en_function():
    for y in range(len(alp_en)):
        for x in range(len(alp_en[y])):
            button = tk.Button(bg="#a5a5a5", fg="white", font=('Roboto Bold', 12), text=alp_en[y][x], command=lambda text=alp_en[y][x]: print(text))
            if y == 2:
                button.place(x=x * 55 + 55, y=y * 54 + 54, height=51, width=51)
            else:
                button.place(x=x * 55 + 0, y=y * 54 + 54, height=51, width=51)
            buttons.append(button)
def alp_EN_function():
    for y in range(len(alp_EN)):
        for x in range(len(alp_EN[y])):
            button = tk.Button(bg="#a5a5a5", fg="white", font=('Roboto Bold', 12), text=alp_EN[y][x], command=lambda text=alp_EN[y][x]: print(text))
            if y == 2:
                button.place(x=x * 55 + 55, y=y * 54 + 54, height=51, width=51)
            else:
                button.place(x=x * 55 + 0, y=y * 54 + 54, height=51, width=51)
            buttons.append(button)
def alp_ru_function():
    for y in range(len(alp_ru)):
        for x in range(len(alp_ru[y])):
            button = tk.Button(bg="#a5a5a5", fg="white", font=('Roboto Bold', 12), text=alp_ru[y][x], command=lambda text=alp_ru[y][x]: print(text))
            if y == 2:
                if alp_ru[y][x] == "ь":
                    button.place(x=x * 55 + 55, y=y * 54 + 54, height=51, width=26)
                elif alp_ru[y][x] == "ъ":
                    button.place(x=x * 55 + 24, y=y * 54 + 54, height=51, width=26)
                elif alp_ru[y][x] == "б":
                    button.place(x=440, y=164, height=51, width=51)
                elif alp_ru[y][x] == "ю":
                    button.place(x=495, y=164, height=51, width=51)
                else:
                    button.place(x=x * 55 + 55, y=y * 54 + 54, height=51, width=51)
            else:
                button.place(x=x * 55 + 0, y=y * 54 + 54, height=51, width=51)
            buttons.append(button)

def alp_RU_function():
    for y in range(len(alp_RU)):
        for x in range(len(alp_RU[y])):
            button = tk.Button(bg="#a5a5a5", fg="white", font=('Roboto Bold', 12), text=alp_RU[y][x], command=lambda text=alp_RU[y][x]: print(text))
            if y == 2:
                if alp_RU[y][x] == "Ь":
                    button.place(x=x * 55 + 55, y=y * 54 + 54, height=51, width=26)
                elif alp_RU[y][x] == "Ъ":
                    button.place(x=x * 55 + 24, y=y * 54 + 54, height=51, width=26)
                elif alp_RU[y][x] == "Б":
                    button.place(x=440, y=164, height=51, width=51)
                elif alp_RU[y][x] == "Ю":
                    button.place(x=495, y=164, height=51, width=51)
                else:
                    button.place(x=x * 55 + 55, y=y * 54 + 54, height=51, width=51)
            else:
                button.place(x=x * 55 + 0, y=y * 54 + 54, height=51, width=51)
            buttons.append(button)

grade = False
def grade_func():
    global grade
    if grade:
        grade = False
        for button in buttons:
            button.config(text=(chr(ord(button.cget('text')) + 32)))
            button.config(command=lambda text=button.cget('text'): print(text))
    else:
        grade = True
        for button in buttons:
            button.config(text=(chr(ord(button.cget('text')) - 32)))
            button.config(command=lambda text=button.cget('text'): print(text))

def lang_func():
    global buttons
    if lang_button.cget('text') == "EN":
        char = buttons[0].cget('text')
        for button in buttons:
            button.destroy()
        buttons = []
        if char == "й":
            alp_en_function()
        if char == "Й":
            alp_EN_function()
        if char == "q":
            alp_ru_function()
        if char == "Q":
            alp_RU_function()



bs_button = tk.Button(bg="#a5a5a5", fg="white", font=('Roboto Bold', 12), text="<", command=lambda: print("Удалить"))
bs_button.place(x=550, y=0, height=50, width=51)
#cl_button = tk.Button(root, bg="#a5a5a5", fg="white", font=('Roboto Bold', 12), text="CL", command=lambda: [button.destroy() for button in numbers_buttons])
cl_button = tk.Button(bg="#a5a5a5", fg="white", font=('Roboto Bold', 12), text="CL", command=lambda: print("Очистить все"))
cl_button.place(x=550, y=164, height=51, width=51)
space_button = tk.Button(bg="#a5a5a5", fg="white", font=('Roboto Bold', 12), text="Пробел", command=lambda: print("Пробел"))
space_button.place(x=220, y=220, height=50, width=216)
enter_button = tk.Button(bg="#a5a5a5", fg="white", font=('Roboto Bold', 12), text="Ввод", command=lambda: print("Ввод"))
enter_button.place(x=495, y=220, height=50, width=106)
grade_button = tk.Button(bg="#a5a5a5", fg="white", font=('Roboto Bold', 12), text="^", command=grade_func)
grade_button.place(x=0, y=162, height=51, width=51)
lang_button = tk.Button(bg="#a5a5a5", fg="white", font=('Roboto Bold', 12), text="EN", command=lang_func)
lang_button.place(x=110, y=220, height=50, width=51)

alp_ru_function()

root.mainloop()