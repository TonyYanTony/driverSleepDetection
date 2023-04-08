import tkinter
from tkinter import *
from PIL import Image, ImageTk

window = Tk()
window.geometry("1000x800")

frame = Frame(window, width=1000, height=100)
img = Image.open("someImage.jpg")
reimg = img.resize((1000, 100))
newimg = ImageTk.PhotoImage(reimg)

frame.pack(fill=BOTH, expand=True)
label1 = Label(frame, image=newimg)
label1.pack()

data = open('data.txt', 'r')
str = data.read()
label3 = Label(window, text=str, font=('Arial', 25), fg="#f00")
label3.pack(side=RIGHT, ipadx=20, ipady=900)
label2 = Label(window, text="状态:", font=('Arial', 25))
label2.pack(side=RIGHT, ipadx=0, ipady=900)

window.mainloop()
