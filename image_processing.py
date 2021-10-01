import cv2 as cv
import numpy as np
from time import time
import json


max_value = 255
low_H = 0
low_S = 0
low_V = 0
high_H = max_value
high_S = max_value
high_V = max_value


def init_values(color: str):
    global low_H, high_H, low_S, low_V

    with open("colors.json") as f:
        colors = json.load(f)
        if not color in colors:
            print("Color does not exist")
            exit()

        values = colors[color]

        low_H = values["low_H"]
        high_H = values["high_H"]
        low_S = values["low_S"]
        low_V = values["low_V"]

        return values["speed"], values["p"]


def threshold(image):
   
    image = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    image = cv.inRange(image, (low_H,low_S,low_V),(high_H,high_S,high_V))


    structElt = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
    image = cv.erode(image, structElt)
    image = cv.dilate(image, structElt)

    #cv.imwrite('1_threshold.jpg', image)

    return image


def get_centroid(image):
    
    M = cv.moments(image)

    # calcul du centroïde (si tout vaut 0, alors pas de ligne détectée)
    try:
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
    except:
        print("No line detected.")
        return None,None
	 

    height, width = image.shape
    cx -= width/2

    return cx, cy

def is_yellow(image):
   
    image = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    image = cv.inRange(image, (20,80,80),(100,high_S,high_V))


    structElt = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
    image = cv.erode(image, structElt)
    image = cv.dilate(image, structElt)

    x,y = get_centroid(image)
    return x != None


def processing(image):

    img = threshold(image)
    x, y = get_centroid(img)

    # change = False
    # if is_yellow(image):
    #     change = True

    return x, y, False # change


if __name__ == "__main__":
    image = cv.imread('img2.jpg')
    processing(image)

