from tkinter import *
from PIL import Image, ImageDraw, ImageFont, ImageTk

root = Tk()

# Создание композитного изображения с текстом и изображениями
combined_img = Image.new("RGB", (200, 60), "black")
draw = ImageDraw.Draw(combined_img)

# Загрузка изображений
img1 = Image.open(r"new_images\tablet.png")
img2 = Image.open(r"new_images\right.png")

# Вставка изображений
combined_img.paste(img1, (10, 15))
combined_img.paste(img2, (170, 15))

# Добавление текста
font = ImageFont.truetype("Roboto-Bold.ttf", 18)
draw.text((50, 20), "Мониторинг", fill="white", font=font, bg="black")

combined_photo = ImageTk.PhotoImage(combined_img)

# Создание кнопки с композитным изображением
button = Button(root, image=combined_photo)
button.pack()

root.mainloop()
