import os
import numpy
import serial
import cv2
import tkinter as tk
import time
from tkinter import *
from PIL import Image, ImageTk  # 图像控件

# ser = serial.Serial('COM5', 9600, timeout=1)
cap = cv2.VideoCapture(0)  # 创建摄像头对象
bb = '湿度:'


# 界面画布更新图像
def on():
    print("f")
    # ser.write('f'.encode())


def off():
    print("a")
    ser.write('a'.encode())

    pass


def b():
    print("b")
    ser.write('b'.encode())

    pass


def d():
    print("d")
    # ser.write('a'.encode())


def c():
    print("c")
    # ser.write('f'.encode())


def e():
    print("e")
    # ser.write('a'.encode())


def tkImage():
    global b
    ret, frame = cap.read()

    frame = cv2.flip(frame, 1)  # 摄像头翻转
    cvimage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    pilImage = Image.fromarray(cvimage)
    pilImage = pilImage.resize((image_width, image_height), Image.ANTIALIAS)
    tkImage = ImageTk.PhotoImage(image=pilImage)
    #    if cv2.waitKey(1) & 0xFF == ord('q'):
    #        break
    return tkImage


top = tk.Tk()
top.title('视频窗口')
top.geometry('800x600')
photo = Image.open("image.png")  # 括号里为需要显示在图形化界面里的图片
photo = photo.resize((800, 100))  # 规定图片大小
img0 = ImageTk.PhotoImage(photo)
img1 = tk.Label(text="照片:", image=img0)
img1.pack()
Button(top, text='浇水', font=("黑体", 22), width=8, height=2, command=on).place(x=20, y=230, anchor='nw')
Button(top, text='停止', font=("黑体", 22), width=8, height=2, command=off).place(x=20, y=330, anchor='nw')
Button(top, text='湿润', font=("黑体", 22), width=8, height=2, command=e).place(x=20, y=430, anchor='nw')
Button(top, text='干旱', font=("黑体", 22), width=8, height=2, command=b).place(x=600, y=330, anchor='nw')
Button(top, text='半湿润', font=("黑体", 22), width=8, height=2, command=d).place(x=20, y=530, anchor='nw')
Button(top, text='半干旱', font=("黑体", 22), width=8, height=2, command=c).place(x=600, y=430, anchor='nw')

image_width = 400
image_height = 400
canvas = Canvas(top, bg='white', width=image_width, height=image_height)  # 绘制画布
Label(top, text='智慧农业智能管理平台', font=("黑体", 32), width=20, height=1).place(x=120, y=120, anchor='nw')
# Label1(top,text = '车牌：',font = ("黑体",44),width =20,height = 1).place(x =350,y = 170,anchor = 'nw')
canvas.place(x=200, y=140)


def read_ser():
    global bb
    val = ser.readline().decode('utf-8')
    parsed = val.split(',')
    # print(parsed)
    parsed = [x.rstrip() for x in parsed]
    if len(parsed) >= 1:
        # print(parsed)
        bb = "温度：" + str(parsed[0])
        # a = int(int(parsed[0] + '0') / 10)
        # b = int(int(parsed[1] + '0') / 10)
        # print(a)
        print(bb)


while True:
    # read_ser()
    # print(bb)
    # global bb
    Label(top, text=bb, font=("黑体", 22), width=8, height=2).place(x=600, y=230, anchor='nw')

    pic = tkImage()
    canvas.create_image(0, 0, anchor='nw', image=pic)
    top.update()
    # top.after(100)
cap.release()
top.mainloop()


