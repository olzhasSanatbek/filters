#Filters 
import cv2
import numpy as np  
from matplotlib import pyplot as plt

class Filters():
    #Linear filtering
    #Box Filter
    def box_filter(path):
        img = cv2.imread(path)

        kernel = (10,10)
        blur = cv2.blur(img,kernel)
        return blur

    #Non-linear filtering
    #Bilateral Filter
    def bilateral_filter(path):
        img = cv2.imread(path)

        blur = cv2.bilateralFilter(img,9,75,75)
        return blur

    #median blur
    def median_blur_filter(path):
        img = cv2.imread(path)

        blur = cv2.medianBlur(img, 5)
        return blur

    #Laplacian Derivatives
    def laplacian(path):
        img = cv2.imread(path)

        img_gray = color_to_gray(img)
        laplacian = cv2.Laplacian(img_gray, cv2.CV_64F, ksize=7)
        return laplacian

#Change color
#Color image changes to gray scale
def color_to_gray(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return gray

#Show us differences after the filtering
def plot(img, PATH):
    plt.imshow(img)
    plt.savefig(PATH)
