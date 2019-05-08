from tkinter import *
import cv2 as cv
from PIL import ImageTk, Image
from Exp1 import Exp1
from Exp2 import Exp2
from Exp3 import Exp3

IMAGE_PATH = 'lena.bmp'
BOAT_PATH = 'boat.png'

root = Tk()
image = None

def openWindow3():
    global image
    global root

    exp2 = Exp3(cv.imread(BOAT_PATH), root)
    root.withdraw()

def openWindow2():
    global image
    global root

    exp2 = Exp2(image, root)
    root.withdraw()

def openWindow1():
    global root
    global image

    exp1 = Exp1(image, root)
    root.withdraw()

root.title('数字图像处理')
img = Image.open(IMAGE_PATH)
image = cv.imread(IMAGE_PATH)
image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
imgShow = ImageTk.PhotoImage(img)
imageLabel = Label(master = root, image = imgShow)
imageLabel.grid(row = 2, column = 1, rowspan = 5, columnspan = 5, padx = 5, pady = 5)

button1 = Button(root, text = '实验一', width = 25, height = 3, command = openWindow1)
button2 = Button(root, text = '实验二', width = 25, height = 3, command = openWindow2)
button3 = Button(root, text = '实验三', width = 25, height = 3, command = openWindow3)
button4 = Button(root, text = '实验四', width = 25, height = 3)
button5 = Button(root, text = '实验五', width = 25, height = 3)
button1.grid(row = 2, column = 7, padx = 10)
button2.grid(row = 3, column = 7, padx = 10)
button3.grid(row = 4, column = 7, padx = 10)
button4.grid(row = 5, column = 7, padx = 10)
button5.grid(row = 6, column = 7, padx = 10)


root.mainloop()