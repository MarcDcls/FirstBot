import cv2 as cv
import numpy as np
from time import time


def hist_equalization(image):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    cv.imwrite('1_grayLevel.jpg', gray)

    # égalisation d'histogramme
    image = cv.equalizeHist(gray)
    cv.imwrite('2_equalizationHist.jpg', image)

    return image


def edge_detection(image, canny = True):
    # on floute légèrement l'image (permet une meilleure détection des contours)
    image = cv.GaussianBlur(image, (3,3), 0)    # filtre gaussien
    cv.imwrite('3_gauss.jpg', image)

    # érosion puis dilatation
    structElt = cv.getStructuringElement(cv.MORPH_ELLIPSE, (10, 10))
    image = cv.erode(image, structElt)
    image = cv.dilate(image, structElt)
    cv.imwrite('4_erodeAndDilate.jpg', image)

    # détection des contours
    if canny:
        # technique de Canny
        image = cv.Canny(image=image, threshold1=85, threshold2=170)
        cv.imwrite('5_edgeCanny.jpg', image)
    else:
        # technique de Sobel
        image = cv.Sobel(src=image, ddepth=cv.CV_64F, dx=1, dy=1, ksize=5)
        cv.imwrite('5_edgeSobel.jpg', image)

    return image


def get_centroid(image, canny = True):

    if not canny:
        # seuillage (passage à une image binaire)
        _, image = cv.threshold(image, 100, 255, 0)    
        cv.imwrite('6_threshold.jpg', image)
    
    # calcul des moments de l'image binaire
    M = cv.moments(image)

    # calcul des coordonnées x,y du centre
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])

    return cX, cY


def processing(image):

    # Technique de détection de contours utilisée (True = Canny, False = Sobel)
    canny = True

    start = time()

    img = hist_equalization(image)
    step1 = time()
    print("Egalisation d'histogramme :", step1-start, "s")

    img = edge_detection(img, canny)
    step2 = time()
    print("Détection de contours :", step2-step1, "s")

    x, y = get_centroid(img, canny)
    step3 = time()
    print("Calcul de centroïde :", step3-step2, "s")

    total = step3-start
    print("Temps total :", total, "s")
    print("(fréquence :", np.ceil(1/total), "Hz)")

    cv.circle(image, (x, y), 5, (0, 0, 255), -1)
    cv.imwrite('7_centroid.jpg', image)


if __name__ == "__main__":
    img = cv.imread('img.jpg')
    processing(img)