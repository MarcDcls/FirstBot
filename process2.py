# Code inspiré de :
# http://einsteiniumstudios.com/tutorials.html
# (BeagleBone Line Following Bot with openCV)


import cv2 as cv
import numpy as np
from time import time


def edge_detection(image):

    image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    cv.imwrite('1_grayLevel.jpg', image)

    # on floute légèrement l'image (permet une meilleure détection des contours)
    image = cv.GaussianBlur(image, (3,3), 0)    # filtre gaussien
    cv.imwrite('2_gauss.jpg', image)

    # Color thresholding
    _,thresh = cv.threshold(image, 100, 255, cv.THRESH_BINARY_INV)
    cv.imwrite('3_thresh.jpg', thresh)

    # Find the contours of the frame
    contours,_ = cv.findContours(thresh.copy(), 1, cv.CHAIN_APPROX_NONE)

    return contours


def get_centroid(image, contours):
    
    c = max(contours, key=cv.contourArea)
    M = cv.moments(c)

    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])

    cv.line(image,(cx,0),(cx,720),(255,0,0),1)
    cv.line(image,(0,cy),(1280,cy),(255,0,0),1)
    cv.circle(image, (cx, cy), 5, (0, 0, 255), -1)

    cv.drawContours(image, contours, -1, (0,255,0), 1)

    cv.imwrite('4_centroid.jpg', image)

    return cx, cy


def processing(image):

    start = time()

    contours = edge_detection(image)
    step2 = time()
    print("Détection de contours :", step2-start, "s")

    x, y = get_centroid(image, contours)
    step3 = time()
    print("Calcul de centroïde :", step3-step2, "s")

    total = step3-start
    print("Temps total :", total, "s")
    print("(fréquence :", np.ceil(1/total), "Hz)")


if __name__ == "__main__":
    img = cv.imread('img2.jpg')
    processing(img)