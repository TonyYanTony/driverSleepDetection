from tkinter import *
from PIL import Image, ImageTk
import time

window = Tk()
window.geometry("1000x800")

# The title bar
frame = Frame(window, width=1000, height=100)
img = Image.open("title.jpg")
reimg = img.resize((1000, 100))
newimg = ImageTk.PhotoImage(reimg)
# The video stream shown
frame2 = Frame(window, width=640, height=480)
img2 = Image.open("image.png")
newimg2 = ImageTk.PhotoImage(img2)
# pack the title bar
frame.pack(fill=BOTH, expand=True)
label1 = Label(frame, image=newimg)
label1.pack()
# pack the video stream
frame2.place(rely=0.5, relx=0.02, anchor=W)
label2 = Label(frame2, image=newimg2)
label2.pack()
# create and pack the results
data = open('data.txt', 'r')
str = data.read()
label3 = Label(window, text=str, font=('Arial', 25), fg="#f00")
label3.place(rely=0.5, relx=0.95, anchor=E)
label4 = Label(window, text="状态:", font=('Arial', 25))
label4.place(rely=0.5, relx=0.8, anchor=E)
# create and pack the time
timestr = time.strftime("%H:%M:%S")
label5 = Label(window, text=timestr, font=('Arial', 10), fg="#555")
label5.place(rely=1, relx=1, anchor=SE)

# loop
while True:
    # data = open('data.txt', 'r')
    # str = data.read()
    # label3 = Label(window, text=str, font=('Arial', 25), fg="#f00")
    # label3.place(rely=0.5, relx=0.95, anchor=E)
    timestr = time.strftime("%H:%M:%S")
    label5 = Label(window, text=timestr, font=('Arial', 10), fg="#555")
    label5.place(rely=1, relx=1, anchor=SE)
    window.update()

window.mainloop()
