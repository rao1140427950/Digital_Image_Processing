import cv2 as cv
import numpy as np
from scipy.io import loadmat

dctMat = []
dhtMat = []

def image_for_display(img):

    img = np.abs(img)
    index = np.where(img < 1e-100)
    img[index] = 1e-10
    img = np.log(np.abs(img))
    img = (img - img.min())/(img.max() - img.min())
    img = np.uint8(img*255)

    return img

def fft_transform(img, inverse = False, do_fftshift = True):

    if (len(np.shape(img)) > 2):
        img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    if (inverse):
        if(do_fftshift):
            img = np.fft.ifftshift(img)
        img_ifft = np.fft.ifft2(img)
        
        return np.abs(img_ifft)

    else:
        img_fft = np.fft.fft2(img)
        if (do_fftshift):
            img_fft = np.fft.fftshift(img_fft)

        return img_fft

def calcHadamard(i, j):
    temp = i&j
    result = 0

    for k in range(32):
        result = result + (temp >> k) & 1
    if (result % 2 == 0):
        return 1
    else:
        return -1
    
def getMatrix_DHT(N, loadMat = True):
    if (loadMat):
        mat = loadmat('hadamard512.mat')
        return mat['H']
    else:
        mat = np.zeros((N, N))
        for i in range(N):
            for j in range(N):
                mat[i][j] = calcHadamard(i, j)
        return mat


def getMatrix_DCT(N):
    
    dctMat = np.zeros((N, N))
    dctMat[0, :] = 1*np.sqrt(1/N)
    for i in range(1, N):
        for j in range(N):
            dctMat[i, j] = np.cos(np.pi*i*(2*j + 1)/(2*N))*np.sqrt(2/N)
    
    return dctMat

def dht_transform(img, inverse = False, use_matrix = True):
    global dhtMat

    if (len(np.shape(img)) > 2):
        img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    if (len(dhtMat) == 0):
        if (use_matrix):
            dhtMat = getMatrix_DHT(img.shape[0], True)
        else:
            dhtMat = getMatrix_DHT(img.shape[0], False)

    img = img.astype('float')

    if (inverse):
        img_idht = np.dot(dhtMat, img)
        img_idht = np.dot(img_idht, dhtMat)
        return np.abs(img_idht)
    else:
        img_dht = np.dot(dhtMat, img)
        img_dht = np.dot(img_dht, dhtMat)
        img_dht = img_dht/(img.shape[0]*img.shape[1])
        return img_dht

def dct_transform(img, inverse = False, use_matrix = True):
    global dctMat

    if (len(dctMat) == 0):
       dctMat = getMatrix_DCT(img.shape[0])

    if (len(np.shape(img)) > 2):
        img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img = img.astype('float')
    #img_dct = cv.dct(img)

    if (inverse):
        if (use_matrix):
            img_idct = np.dot(np.transpose(dctMat), img)
            img_idct = np.dot(img_idct, dctMat)
        else:
            img_idct = cv.idct(img)
        return np.abs(img_idct)
    else:
        if (use_matrix):
            img_dct = np.dot(dctMat, img)
            img_dct = np.dot(img_dct, np.transpose(dctMat))
        else:
            img_dct = cv.dct(img)
        
        return img_dct

if __name__ == '__main__':

    img = cv.imread('lena.bmp')
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    img1 = fft_transform(fft_transform(img), True)

    print(img1.max())
    img = abs(img - img1)
    
    print(img.sum())

    #cv.imshow('image', img)
    #cv.waitKey(5000)
