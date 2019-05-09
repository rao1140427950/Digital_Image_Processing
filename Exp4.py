import numpy as np
import cv2 as cv
from tkinter import *
from PIL import ImageTk, Image
#from func_hough import *

class Exp4(object):
    
    __root = None
    __img = None
    __imgDisplay = None
    __imgBlur = None
    __imgNoise = None
    __imgDiff = None
    __parent = None
    __button1 = None
    __scale1 = None
    __scale2 = None
    __N = 0
    __n = 0
    __use_cv = True
    __imageLabel = None
    __noise = 0
    __midFilter_R = 1
    __robert_times = 0
    __sobel_times = 0

    def __init__(self, img, rootWindow, use_cv = True):
        self.__root = Toplevel()
        self.__use_cv = use_cv
        self.__root.title('实验四')
        if (len(np.shape(img)) > 2):
            img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        self.__img = img
        self.__imgBlur = img
        self.__imgNoise = img
        self.__imgDiff = img
        self.__N = img.shape[0]*img.shape[1]
        self.__n = img.shape[0]
        self.__parent = rootWindow
        self.__root.protocol('WM_DELETE_WINDOW', self.onClose)
        self.addComponent()
    
    def addComponent(self):
        imgShow = ImageTk.PhotoImage(Image.fromarray(self.__img))
        self.__imageLabel = Label(master = self.__root, image = imgShow)
        self.__imageLabel.config(image = imgShow)
        self.__imageLabel.image = imgShow
        self.__imageLabel.grid(row = 2, column = 1, rowspan = 5, columnspan = 5, padx = 50, pady = 50)
        self.__scale1 = Scale(self.__root,
                             orient = HORIZONTAL,
                             from_ = 0,
                             to = 100,
                             resolution = 1,
                             digits = 1,
                             length = 300,
                             tickinterval = 20,
                             label = '噪声强度',
                             command = self.scale1Change)
        self.__scale1.set(0)
        self.__scale1.grid(row = 2, column = 7, columnspan = 3)
        self.__button1 = Button(self.__root, text = '原始图像', width = 25, height = 3, command = self.button1Click)
        self.__button1.grid(row = 3, column = 7, padx = 10)
        self.__button2 = Button(self.__root, text = '添加高斯噪声', width = 25, height = 3, command = self.button2Click)
        self.__button2.grid(row = 3, column = 8, padx = 10)
        self.__button3 = Button(self.__root, text = '添加椒盐噪声', width = 25, height = 3, command = self.button3Click)
        self.__button3.grid(row = 3, column = 9, padx = 10)
        self.__scale2 = Scale(self.__root,
                             orient = HORIZONTAL,
                             from_ = 1,
                             to = 101,
                             resolution = 1,
                             digits = 2,
                             length = 300,
                             tickinterval = 20,
                             label = '中值滤波半径',
                             command = self.scale2Change)
        self.__scale2.set(1)
        self.__scale2.grid(row = 4, column = 7, columnspan = 3)
        self.__button4 = Button(self.__root, text = 'Robert', width = 25, height = 3, command = self.button4Click)
        self.__button4.grid(row = 5, column = 7, padx = 10)
        self.__button5 = Button(self.__root, text = 'Sobel', width = 25, height = 3, command = self.button5Click)
        self.__button5.grid(row = 5, column = 8, padx = 10)
        self.__button6 = Button(self.__root, text = 'Laplacian', width = 25, height = 3, command = self.button6Click)
        self.__button6.grid(row = 5, column = 9, padx = 10)
        self.__button7 = Button(self.__root, text = 'Hough变换', width = 35, height = 3, command = self.button7Click)
        self.__button7.grid(row = 6, column = 7, padx = 10, columnspan = 3)

    def scale1Change(self, text):
        self.__noise = self.__scale1.get()

    def scale2Change(self, text):
        self.__midFilter_R = self.__scale2.get()
        if (self.__midFilter_R%2 == 0):
            self.__midFilter_R = self.__midFilter_R - 1
            self.__scale2.set(self.__midFilter_R)
        self.__imgDisplay = cv.medianBlur(self.__imgNoise, self.__midFilter_R)
        self.__imgBlur = np.copy(self.__imgDisplay)
        self.updateImage()

    def button1Click(self):
        self.updateImage(self.__img)
        self.__imgNoise = np.copy(self.__img)

    def button2Click(self):
        noise = np.random.standard_normal((self.__img.shape))
        noise = self.__noise*noise
        noise = self.__img + noise
        index = np.where(noise > 255)
        noise[index] = 255
        index = np.where(noise < 0)
        noise[index] = 0
        self.__imgNoise = np.uint8(noise)
        self.updateImage(noise)

    def button3Click(self):
        noise = np.copy(self.__img)
        num = int(self.__noise*self.__N/100)
        for i in range(num):
            randX = np.random.random_integers(0, noise.shape[0] - 1)
            randY = np.random.random_integers(0, noise.shape[1] - 1)
            if (np.random.random_integers(0, 1) == 0):
                noise[randX, randY] = 0
            else:
                noise[randX, randY] = 255
        self.__imgNoise = noise
        self.updateImage(noise)

    def button4Click(self):
        if (self.__robert_times == 0):
            kernal = np.array([[0, -1], [1, 0]])
            self.__imgDiff = cv.filter2D(self.__imgBlur, -1, kernal)
            self.__imgDisplay = self.__imgDiff
            self.updateImage()
        else :
            kernal = np.array([[-1, 0], [0, 1]])
            self.__imgDiff = cv.filter2D(self.__imgBlur, -1, kernal)
            self.__imgDisplay = self.__imgDiff
            self.updateImage()
        self.__robert_times = (self.__robert_times + 1)%2

    def button5Click(self):
        if (self.__sobel_times == 0):
            sobelx = cv.Sobel(self.__imgBlur, cv.CV_8U, 1, 0, ksize=5)
            self.__imgDiff = sobelx
            self.updateImage(sobelx)
        else:
            sobely = cv.Sobel(self.__imgBlur, cv.CV_8U, 0, 1, ksize=5)
            self.__imgDiff = sobely
            self.updateImage(sobely)
        self.__sobel_times = (self.__sobel_times + 1)%2

    def button6Click(self):
        laplacian = cv.Laplacian(self.__imgBlur, cv.CV_8U)
        self.__imgDiff = laplacian
        self.updateImage(self.__imgDiff)

    def button7Click(self):
        circles = cv.HoughCircles(self.__imgDiff, cv.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=0, maxRadius=0)
        circles = np.uint16(np.around(circles))
        img = np.copy(self.__imgNoise)
        for i in circles[0, :]:
            # draw the circle
            cv.circle(img, (i[0], i[1]), i[2], (127), 2)
            break
        self.updateImage(img)


    def updateImage(self, img = np.array([])):
        if (img.size == 0):
            imgShow = ImageTk.PhotoImage(Image.fromarray(self.__imgDisplay))
            self.__imageLabel.config(image = imgShow)
            self.__imageLabel.image = imgShow
            self.__root.update()
        else:
            imgShow = ImageTk.PhotoImage(Image.fromarray(img))
            self.__imageLabel.config(image = imgShow)
            self.__imageLabel.image = imgShow
            self.__root.update()

    def onClose(self):
        self.__root.destroy()
        self.__parent.update()
        self.__parent.deiconify()

