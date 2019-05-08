import numpy as np
import cv2 as cv

def thresh_otsu(img, use_cv = True):
    
    if (use_cv):
        rst, otsu = cv.threshold(img, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
        return otsu

    else:
        hist = cv.calcHist([img], [0], None, [256], [0,256])
        hist_norm = hist.ravel()/hist.max()
        Q = hist_norm.cumsum()

        bins = np.arange(256)

        fn_min = np.inf
        thresh = -1

        for i in range(1, 256):
            p1, p2 = np.hsplit(hist_norm, [i]) # probabilities
            q1, q2 = Q[i], Q[255] - Q[i] # cum sum of classes
            b1, b2 = np.hsplit(bins,[i]) # weights

            # finding means and variances
            if (q1 == 0 or q2 == 0):
                continue
            m1, m2 = np.sum(p1*b1)/q1, np.sum(p2*b2)/q2
            v1, v2 = np.sum(((b1-m1)**2)*p1)/q1, np.sum(((b2-m2)**2)*p2)/q2

            # calculates the minimization function
            fn = v1*q1 + v2*q2
            if fn < fn_min:
                fn_min = fn
                thresh = i
        rst, img = cv.threshold(img, thresh, 255, cv.THRESH_BINARY)
        return img

def erode(img, kernel, use_cv = True):

    if (use_cv):
        return cv.erode(img, kernel)
    else:
        img = cv.filter2D(img, -1, kernel/kernel.sum())
        index1 = np.where(img == 255)
        index2 = np.where(img < 255)
        img[index1] = 255
        img[index2] = 0
        return img

def dilate(img, kernel, use_cv = True):

    if (use_cv):
        return cv.dilate(img, kernel)
    else:
        img = cv.filter2D(img, -1, kernel/kernel.sum())
        index1 = np.where(img > 0)
        index2 = np.where(img == 0)
        img[index1] = 255
        img[index2] = 0
        return img