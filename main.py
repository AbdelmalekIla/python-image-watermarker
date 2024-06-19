from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog


def upload_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
    if file_path:
        img = Image.open(file_path)
        img.thumbnail((300, 300))
        img_tk = ImageTk.PhotoImage(img)
        image_label.config(image=img_tk)
        image_label.image = img_tk


window = Tk()
window.title("Image Watermarking Application")
window.geometry("600x400")
window.config(background="lightgrey")

upload_button = Button(window, text='Upload', command=upload_image)
upload_button.pack(pady=10)
image_label = Label(window)
image_label.pack(pady=10)





window.mainloop()