import cv2 as cv
import numpy as np

def fft_transform(img, do_fftshift = True, do_log = True, normalize = True):

    if (len(np.shape(img)) >= 2):
        img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    img_fft = np.fft.fft2(img)
    if (do_fftshift):
        img_fft = np.fft.fftshift(img_fft)
    if (do_log):
        img_fft = np.log(np.abs(img_fft))
        if (normalize):
            img_fft = (img_fft - img_fft.min())/(img_fft.max() - img_fft.min())

    return img_fft


if __name__ == '__main__':

    img = cv.imread('lena.bmp')
    img = fft_transform(img)
    cv.imshow('image', img)
    cv.waitKey(5000)
