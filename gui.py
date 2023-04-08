from tkinter import *
from PIL import Image, ImageTk
window = Tk()
window.geometry("1000x800")

frame = Frame(window, width=700, height=500)
img = Image.open("someImage.jpg")
reimg = img.resize((1000, 100))
newimg = ImageTk.PhotoImage(reimg)

frame.pack(fill = BOTH, expand = True)
label1 = Label(frame, image=newimg)
label1.pack()


window.mainloop()