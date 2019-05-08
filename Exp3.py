import numpy as np
import cv2 as cv
from tkinter import *
from PIL import ImageTk, Image
from blur_thresh import *

class Exp3(object):
    
    __root = None
    __img = None
    __imgDisplay = None
    __imgBlur = None
    __imgBin = None
    __parent = None
    __imgLabel = None
    __button1 = None
    __scale1 = None
    __scale2 = None
    __scale3 = None
    __N = 0
    __n = 0
    __midFilter_R = 1
    __dilate_R = 1
    __erode_R = 1
    __isBinary = False
    
    def __init__(self, img, rootWindow):
        self.__root = Toplevel()
        self.__root.title('实验三')
        if (len(np.shape(img)) > 2):
            img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        self.__img = img
        self.__imgBlur = img
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
        self.__button1 = Button(self.__root, text = '阈值分割', width = 25, height = 3, command = self.button1Click)
        self.__button1.grid(row = 3, column = 7, padx = 10)
        self.__scale1 = Scale(self.__root,
                             orient = HORIZONTAL,
                             from_ = 1,
                             to = 101,
                             resolution = 1,
                             digits = 2,
                             length = 300,
                             tickinterval = 20,
                             label = '中值滤波半径',
                             command = self.scale1Change)
        self.__scale1.set(1)
        self.__scale1.grid(row = 2, column = 7)
        self.__scale2 = Scale(self.__root,
                             orient = HORIZONTAL,
                             from_ = 1,
                             to = 7,
                             resolution = 1,
                             digits = 2,
                             length = 300,
                             tickinterval = 2,
                             label = '胀运算半径',
                             command = self.scale2Change)
        self.__scale2.set(1)
        self.__scale2.grid(row = 4, column = 7)
        self.__scale3 = Scale(self.__root,
                             orient = HORIZONTAL,
                             from_ = 1,
                             to = 7,
                             resolution = 1,
                             digits = 2,
                             length = 300,
                             tickinterval = 2,
                             label = '腐蚀运算半径',
                             command = self.scale3Change)
        self.__scale3.set(1)
        self.__scale3.grid(row = 5, column = 7)

    def scale1Change(self, text):
        self.__midFilter_R = self.__scale1.get()
        if (self.__midFilter_R%2 == 0):
            self.__midFilter_R = self.__midFilter_R - 1
            self.__scale1.set(self.__midFilter_R)
        self.__imgDisplay = cv.medianBlur(self.__img, self.__midFilter_R)
        self.__imgBlur = np.copy(self.__imgDisplay)
        self.updateImage()

    def scale2Change(self, text):
        self.__dilate_R = self.__scale2.get()
        if (self.__dilate_R%2 == 0):
            self.__dilate_R = self.__dilate_R - 1
            self.__scale2.set(self.__dilate_R)
        if (self.__isBinary):
            kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (int(self.__dilate_R), int(self.__dilate_R)))
            img = dilate(self.__imgBin, kernel, False)
            self.updateImage(img)

    def scale3Change(self, text):
        self.__erode_R = self.__scale3.get()
        if (self.__erode_R%2 == 0):
            self.__erode_R = self.__erode_R - 1
            self.__scale3.set(self.__erode_R)
        if (self.__isBinary):
            kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (int(self.__erode_R), int(self.__erode_R)))
            #print(kernel)
            img = erode(self.__imgBin, kernel)
            self.updateImage(img)

    def button1Click(self):
        if (self.__isBinary):
            self.__isBinary = False
            self.updateImage(self.__img)
        else:
            self.__isBinary = True
            img = thresh_otsu(self.__imgBlur)
            self.__imgBin = img
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


