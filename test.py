from tkinter import *
def btn_clicked(event):
    print("Button Clicked")
window = Tk()
window.geometry("800x480")
window.configure(bg="#161616")
canvas = Canvas(
    window,
    bg="#161616",
    height=480,
    width=800,
    bd=0,
    highlightthickness=0,
    relief="ridge")
canvas.place(x=0, y=0)
add_data_button_img = PhotoImage(file=r"images\MainScreen\options.png")
add_data_button = canvas.create_image(65, 20, image=add_data_button_img)
canvas.tag_bind(add_data_button, "<Button-1>", btn_clicked)
background_img = PhotoImage(file=r"images\MainScreen\stop_icon.png")
background = canvas.create_image(675, 20, image=background_img)
window.resizable(False, False)
window.mainloop()