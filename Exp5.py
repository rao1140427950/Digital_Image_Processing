import numpy as np
import cv2 as cv
from tkinter import *
from PIL import ImageTk, Image
from tensorflow.examples.tutorials.mnist import input_data
import tensorflow as tf
from network import network

class Exp5(object):
    
    __root = None
    __imgTrain = None
    __imgDisplay = None
    __parent = None
    __imgLabel = None
    __accLabel = None
    __button1 = None
    __mnist = None
    __MODE_SAVE_PATH = './checkpoint/mnist_checkpoint.ckpt'
    __DATA_PATH = './mnist_dataset/'
    __testImg = None
    __testIndex = 0
    __testImgNoise = None
    __noise  = 0
    __noise_std = None

    def __init__(self, img, rootWindow, use_cv = True):
        self.__root = Toplevel()
        self.__root.title('实验五')
        self.__imgTrain = img
        self.__parent = rootWindow
        self.__root.protocol('WM_DELETE_WINDOW', self.onClose)
        self.addComponent()
        self.__mnist = input_data.read_data_sets(self.__DATA_PATH, one_hot = True)
        self.__testImg = np.reshape(self.__mnist.test.images[0,:], (28, 28))*255
        self.__testImgNoise = self.__testImg
        self.__noise_std = np.random.standard_normal((28, 28))
        network.initGraph()
    
    def addComponent(self):
        imgShow = ImageTk.PhotoImage(Image.fromarray(self.__imgTrain))
        self.__imageLabel = Label(master = self.__root, image = imgShow)
        self.__imageLabel.config(image = imgShow)
        self.__imageLabel.image = imgShow
        self.__imageLabel.grid(row = 3, column = 1, rowspan = 5, columnspan = 5, padx = 5, pady = 5)
        self.__accLabel = Label(master = self.__root, text = '测试集正确率 = ')
        self.__accLabel.grid(row = 2, column = 7, padx = 10)
        self.__button1 = Button(self.__root, text = '显示学习曲线', width = 25, height = 3, command = self.button1Click)
        self.__button1.grid(row = 3, column = 7, padx = 10)
        self.__button2 = Button(self.__root, text = '显示测试图片', width = 25, height = 3, command = self.button2Click)
        self.__button2.grid(row = 4, column = 7, padx = 10)
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
        self.__scale1.grid(row = 5, column = 7, columnspan = 3)
        self.__button3 = Button(self.__root, text = '添加噪声', width = 25, height = 3, command = self.button3Click)
        self.__button3.grid(row = 6, column = 7, padx = 10)
        self.__button3 = Button(self.__root, text = '测试集识别', width = 25, height = 3, command = self.button4Click)
        self.__button3.grid(row = 7, column = 7, padx = 10)

    def scale1Change(self, text):
        self.__noise = self.__scale1.get()

    def button3Click(self):
        self.__testImgNoise = np.copy(self.__testImg)
        self.__testImgNoise = self.__testImgNoise + self.__noise_std*self.__noise*2.55
        self.updateImage(self.__testImgNoise)
        self.__imageLabel.grid(row = 2, column = 1, rowspan = 5, columnspan = 5, padx = 200, pady = 200)

    def button4Click(self):
        images = self.__mnist.test.images
        labels = self.__mnist.test.labels
        num_examples = self.__mnist.test.num_examples
        images = np.random.standard_normal(images.shape)*self.__noise/100 + images
        acc = network.getTestAccuracy(images, labels, num_examples)
        self.__accLabel['text'] = '测试集正确率 = ' + str(round(acc*10000)/100) + '%'


    def button2Click(self):
        self.__testImg = np.reshape(self.__mnist.test.images[self.__testIndex,:], (28, 28))*255
        #self.__testImg = cv.resize(self.__testImg, (256, 256))
        self.__testIndex = self.__testIndex + 1
        self.updateImage(self.__testImg)
        #self.__imageLabel.config(padx = 100, pady = 100)
        #self.__imageLabel.padx = 100
        #self.__imageLabel.pady = 100
        self.__imageLabel.grid(row = 2, column = 1, rowspan = 5, columnspan = 5, padx = 200, pady = 200)

    def button1Click(self):
        self.updateImage(self.__imgTrain)
        self.__imageLabel.grid(row = 2, column = 1, rowspan = 5, columnspan = 5, padx = 5, pady = 5)

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
