import numpy as np
import cv2 as cv
from tkinter import *
from PIL import ImageTk, Image
from transforms import fft_transform, image_for_display

class Exp2(object):

    __button1 = None
    __button2 = None
    __button3 = None
    __imgDisplay1 = []
    __imgDisplay2 = []
    __imageLabel1 = None
    __imageLabel2 = None
    __root = None
    __img = []
    __imgBlur_fft = []
    __imgBlur_fft_noise = []
    __imgBlur = []
    __N = 0
    __parent = None
    __scale1 = None
    __scale2 = None
    __blurFilter = []
    __r0 = 363
    __K = 0
    __Filter1 = None
    __Filter2 = None
    __Filter3 = None
    __psnrLabel = None
    __sigma = 0
    __psnr = 0
    __real = []
    __imag = []
     
    def __init__(self, img, rootWindow):
        self.__root = Toplevel()
        self.__root.title('实验二')
        self.__img = img
        self.__N = img.shape[0]*img.shape[1]
        self.__parent = rootWindow
        self.__root.protocol('WM_DELETE_WINDOW', self.onClose)
        self.addComponent()

    def addComponent(self):
        imgShow = ImageTk.PhotoImage(Image.fromarray(self.__img))
        self.__imageLabel1 = Label(master = self.__root, image = imgShow)
        self.__imageLabel1.config(image = imgShow)
        self.__imageLabel1.image = imgShow
        self.__imageLabel1.grid(row = 2, column = 1, rowspan = 5, columnspan = 5, padx = 5, pady = 5)
        self.generateBlurImage()
        imgShow = ImageTk.PhotoImage(Image.fromarray(self.__imgBlur))
        self.__imageLabel2 = Label(master = self.__root, image = imgShow)
        self.__imageLabel2.config(image = imgShow)
        self.__imageLabel2.image = imgShow
        self.__imageLabel2.grid(row = 2, column = 7, rowspan = 5, columnspan = 5, padx = 5, pady = 5)
        self.__psnrLabel = Label(master = self.__root, text = 'PSNR = ')
        self.__psnrLabel.grid(row = 1, column = 14)
        self.__button1 = Button(self.__root, text = '反向滤波', width = 25, height = 3, command = self.button1Click)
        self.__button1.grid(row = 4, column = 14, padx = 10)
        self.__button2 = Button(self.__root, text = '维纳滤波', width = 25, height = 3, command = self.button2Click)
        self.__button2.grid(row = 5, column = 14, padx = 10)
#        self.__button3 = Button(self.__root, text = '添加噪声', width = 25, height = 3, command = self.button3Click)
#        self.__button3.grid(row = 6, column = 14, padx = 10)
        self.__scale1 = Scale(self.__root,
                             orient = HORIZONTAL,
                             from_ = 1,
                             to = 363,
                             resolution = 1,
                             digits = 3,
                             length = 300,
                             tickinterval = 50,
                             label = '反向滤波r0',
                             command = self.scale1Change)
        self.__scale1.set(363)
        self.__scale1.grid(row = 2, column = 14)
        self.__scale2 = Scale(self.__root,
                             orient = HORIZONTAL,
                             from_ = 0,
                             to = 1e-31,
                             resolution = 1e-41,
                             digits = 3,
                             length = 300,
                             tickinterval = 5e-32,
                             label = '维纳滤波K',
                             command = self.scale2Change)
        self.__scale2.set(0)
        self.__scale2.grid(row = 3, column = 14)
#        self.__scale3 = Scale(self.__root,
#                             orient = HORIZONTAL,
#                             from_ = 0,
#                             to = 50,
#                             resolution = 0.01,
#                             digits = 5,
#                             length = 300,
#                             tickinterval = 10,
#                             label = '噪声系数Sigma',
#                             command = self.scale3Change)
#        self.__scale3.set(0)
#        self.__scale3.grid(row = 1, column = 14)
#        self.__real = np.random.standard_normal((self.__img.shape[0], self.__img.shape[0]))
#        self.__imag = np.random.standard_normal((self.__img.shape[0], self.__img.shape[0]))

    def scale1Change(self, text):
        self.__r0 = self.__scale1.get()

    def scale2Change(self, text):
        self.__K = self.__scale2.get()

    def scale3Change(self, text):
        self.__sigma = self.__scale3.get()

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

    def button1Click(self):
        filter = np.copy(self.__blurFilter)
        filter = 1/filter
        n = self.__img.shape[0]
        for x in range(n):
            for y in range(n):
                if ((256 - x)**2 + (256 - y)**2 > self.__r0**2):
                    filter[x][y] = 1
        self.__Filter1 = filter
        self.__imgDisplay1 = fft_transform(np.multiply(filter, self.__imgBlur_fft_noise), True)
        psnr = self.calcPSNR(self.__imgDisplay1, self.__img)
        self.updatePSNR(psnr)
        self.updateImage1()

    def button2Click(self):
        filter = np.copy(self.__blurFilter)
        filter_mol = np.abs(filter)
        filter_mol = np.multiply(filter_mol, filter_mol)
        filter_mol = np.divide(filter_mol, filter_mol + self.__K)
        filter = 1/filter
        filter = np.multiply(filter, filter_mol)
        self.__Filter2 = filter
        self.__imgDisplay1 = fft_transform(np.multiply(filter, self.__imgBlur_fft_noise), True)
        self.updateImage1()
        psnr = self.calcPSNR(self.__imgDisplay1, self.__img)
        self.updatePSNR(psnr)
        self.updateImage1()

    def button3Click(self):
        self.__imgBlur_fft_noise = self.__imgBlur_fft + self.__sigma*(self.__real + 1j*self.__imag)
        self.__imgBlur = fft_transform(self.__imgBlur_fft_noise, True)
        self.__imgDisplay2 = self.__imgBlur
        self.updateImage2()

        
    def updateImage1(self, img = []):
        if (len(img) == 0):
            imgShow = ImageTk.PhotoImage(Image.fromarray(self.__imgDisplay1))
            self.__imageLabel1.config(image = imgShow)
            self.__imageLabel1.image = imgShow
            self.__root.update()
        else:
            imgShow = ImageTk.PhotoImage(Image.fromarray(img))
            self.__imageLabel1.config(image = imgShow)
            self.__imageLabel1.image = imgShow
            self.__root.update()

    def updateImage2(self, img = []):
        if (len(img) == 0):
            imgShow = ImageTk.PhotoImage(Image.fromarray(self.__imgDisplay2))
            self.__imageLabel2.config(image = imgShow)
            self.__imageLabel2.image = imgShow
            self.__root.update()
        else:
            imgShow = ImageTk.PhotoImage(Image.fromarray(img))
            self.__imageLabel2.config(image = imgShow)
            self.__imageLabel2.image = imgShow
            self.__root.update()

    def calcBlurFilter(self):
        T = 1

        if (len(self.__blurFilter) != 0):
            return

        n = self.__img.shape[0]
        self.__blurFilter = np.zeros((n, n)) + 1j*np.zeros((n, n))
        for x in range(n):
            for y in range(n):
                u = x - n/2
                v = y - n/2
                if (u + v == 0):
                    self.__blurFilter[x][y] = T
                else:
                    self.__blurFilter[x][y] = T*np.sin(np.pi*(u + v))*np.exp(-1j*np.pi*(u + v))/(np.pi*(u + v))

    def generateBlurImage(self):
        if (len(self.__imgBlur) != 0):
            return

        self.calcBlurFilter()
        img_fft = fft_transform(self.__img)
        #cv.imshow('aaa', image_for_display(img_fft))
        #cv.waitKey(5000)
        img_fft = np.multiply(img_fft, self.__blurFilter)
        #cv.imshow('aaa', image_for_display(img_fft))
        #cv.waitKey(5000)
        self.__imgBlur_fft = img_fft
        self.__imgBlur_fft_noise = img_fft
        self.__imgBlur = fft_transform(img_fft, True)
        #self.__imgBlur = image_for_display(self.__imgBlur)
        #self.__imgBlur = self.__imgBlur
        #print(self.__imgBlur)
        #print(self.__imgBlur.max())
        #print(self.__imgBlur.min())

    def onClose(self):
        self.__root.destroy()
        self.__parent.update()
        self.__parent.deiconify()

