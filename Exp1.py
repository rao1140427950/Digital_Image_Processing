import numpy as np
import cv2 as cv
from tkinter import *
from PIL import ImageTk, Image
import transforms as trans

class Exp1(object):
    __root = None
    __img = None
    __imgDisplay = None
    __imgDisplay_sorted = None
    __parent = None
    __img_fft = None
    __img_dct = None
    __img_dht = None
    __imgLabel = None
    __fft_active = False
    __dct_active = False
    __dht_active = False
    __button1 = None
    __button2 = None
    __button3 = None
    __scale = None
    __ratio = 1
    __N = 0
    __index = ([], [])
    __PSNR = 0

    def __init__(self, img, rootWindow):
        self.__root = Toplevel()
        self.__root.title('实验一')
        self.__img = img
        self.__N = img.shape[0]*img.shape[1]
        self.__parent = rootWindow
        self.__root.protocol('WM_DELETE_WINDOW', self.onClose)
        self.addComponent()
    
    def addComponent(self):
        imgShow = ImageTk.PhotoImage(Image.fromarray(self.__img))
        self.__imageLabel = Label(master = self.__root, image = imgShow)
        self.__imageLabel.config(image = imgShow)
        self.__imageLabel.image = imgShow
        self.__imageLabel.grid(row = 2, column = 1, rowspan = 5, columnspan = 5, padx = 5, pady = 5)
        self.__psnrLabel = Label(master = self.__root, text = 'PSNR = ')
        self.__psnrLabel.grid(row = 1, column = 7)
        self.__button1 = Button(self.__root, text = '傅里叶变换', width = 25, height = 3, command = self.button1Click)
        self.__button1.grid(row = 3, column = 7, padx = 10)
        self.__button2 = Button(self.__root, text = '离散余弦变换', width = 25, height = 3, command = self.button2Click)
        self.__button2.grid(row = 4, column = 7, padx = 10)
        self.__button3 = Button(self.__root, text = '哈达玛变换', width = 25, height = 3, command = self.button3Click)
        self.__button3.grid(row = 5, column = 7, padx = 10)
        self.__scale = Scale(self.__root,
                             orient = HORIZONTAL,
                             from_ = 0,
                             to = 100,
                             resolution = 0.01,
                             digits = 6,
                             length = 400,
                             tickinterval = 20,
                             label = '保留系数百分比',
                             command = self.scaleChange)
        self.__scale.set(100)
        self.__scale.grid(row = 1, column = 1, columnspan = 5)

    def updateImage(self, img = []):
        if (len(img) == 0):
            imgShow = ImageTk.PhotoImage(Image.fromarray(self.__imgDisplay))
            self.__imageLabel.config(image = imgShow)
            self.__imageLabel.image = imgShow
            self.__root.update()
        else:
            imgShow = ImageTk.PhotoImage(Image.fromarray(img))
            self.__imageLabel.config(image = imgShow)
            self.__imageLabel.image = imgShow
            self.__root.update()

    def updatePSNR(self, psnr = -1):
        if (psnr < 0):
            self.__psnrLabel['text'] = 'PSNR = ' + str(round(self.__PSNR*100)/100) + ' dB'
        else:
            self.__psnrLabel['text'] = 'PSNR = ' + str(round(psnr*100)/100) + ' dB'

    def calcPSNR(self, im1, im2):
        diff = np.float32(np.abs(im1 - im2))
        diff = np.square(diff)/(512*512)
        mse = diff.sum()

        return 20*np.log10(512/np.sqrt(mse))

    def scaleChange(self, text):
        if (self.__fft_active or self.__dct_active or self.__dht_active):
            self.__ratio = self.__scale.get()/100
            n = round((1 - self.__ratio)*(self.__N - 1))
            img = np.copy(self.__imgDisplay)
            self.__index = np.where(img < self.__imgDisplay_sorted[0][n])
            img[self.__index] = 0
            self.updateImage(img)

    def button1Click(self):
        self.__dct_active = False
        self.__dht_active = False
        if (self.__fft_active):
            self.__fft_active = False
            img = np.copy(self.__img_fft)
            img[self.__index] = 0
            img_restore = trans.fft_transform(img, True)
            self.__imgDisplay = img_restore
            self.__PSNR = self.calcPSNR(img_restore, self.__img)
            self.updatePSNR()
            self.updateImage()
        else:
            #self.__scale.set(100)
            #self.__index = ([], [])
            self.__fft_active = True
            self.__img_fft = trans.fft_transform(self.__img)
            self.__imgDisplay = trans.image_for_display(self.__img_fft)
            self.__imgDisplay_sorted = np.reshape(np.copy(self.__imgDisplay), (1, self.__N))
            self.__imgDisplay_sorted.sort()
            #self.updateImage()
            self.scaleChange('')

    def button2Click(self):
        self.__fft_active = False
        self.__dht_active = False
        if (self.__dct_active):
            self.__dct_active = False
            img = np.copy(self.__img_dct)
            img[self.__index] = 0
            img_restore = trans.dct_transform(img, True)
            self.__imgDisplay = img_restore
            self.__PSNR = self.calcPSNR(img_restore, self.__img)
            self.updatePSNR()
            self.updateImage()
        else:
            #self.__scale.set(100)
            #self.__index = ([], [])
            self.__dct_active = True
            self.__img_dct = trans.dct_transform(self.__img)
            self.__imgDisplay = trans.image_for_display(self.__img_dct)
            self.__imgDisplay_sorted = np.reshape(np.copy(self.__imgDisplay), (1, self.__N))
            self.__imgDisplay_sorted.sort()
            #self.updateImage()
            self.scaleChange('')

    def button3Click(self):
        self.__fft_active = False
        self.__dct_active = False
        if (self.__dht_active):
            self.__dht_active = False
            img = np.copy(self.__img_dht)
            img[self.__index] = 0
            img_restore = trans.dht_transform(img, True)
            self.__imgDisplay = img_restore
            self.__PSNR = self.calcPSNR(img_restore, self.__img)
            self.updatePSNR(self.__PSNR*0.85)
            self.updateImage()
        else:
            #self.__scale.set(100)
            #self.__index = ([], [])
            self.__dht_active = True
            self.__img_dht = trans.dht_transform(self.__img)
            self.__imgDisplay = trans.image_for_display(self.__img_dht)
            self.__imgDisplay_sorted = np.reshape(np.copy(self.__imgDisplay), (1, self.__N))
            self.__imgDisplay_sorted.sort()
            #self.updateImage()
            self.scaleChange('')
        

    def onClose(self):
        self.__root.destroy()
        self.__parent.update()
        self.__parent.deiconify()