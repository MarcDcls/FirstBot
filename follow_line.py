import cv2 as cv
from image_processing import processing, init_color
import pypot.dynamixel
import sys
import numpy as np

def mean(list_speed):
    sum_1 = 0
    sum_2 = 0
    l = len(list_speed)
    for i in range(l):
        sum_1 += list_speed[i][0]
        sum_2 += list_speed[i][1]
    return sum_1/l, sum_2/l

line_color = "blue"
nb_args = len(sys.argv)
if nb_args > 1:
    line_color = sys.argv[1]

init_color(line_color)


ports = pypot.dynamixel.get_available_ports()
if not ports:
    exit('No port')

port = ports[0]
print('Using the first on the list', port)

dxl_io = pypot.dynamixel.DxlIO(port)
print('Connected!')

found_ids = dxl_io.scan([1,2])
print('Found ids:', found_ids)

ids = found_ids[:2]
dxl_io.enable_torque(ids)

default_speed = 200

speed = (-default_speed, default_speed)

cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

list_speed = [speed]*30


try:
    while True:
        
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?).")
            continue

        x, y = processing(frame)

        if x == None:
            mean_1, mean_2 = mean(list_speed)
            mean_speed = {
                1: mean_1,
                2: mean_2
            }
            dxl_io.set_moving_speed(mean_speed)

        else:

            speed = (
                -default_speed + 0.4*x,
                default_speed + 0.4*x
            )
            del list_speed[0]
            list_speed.append(speed)
            print(speed)

            dxl_io.set_moving_speed({
                1: speed[0],
                2: speed[1]
            })

except KeyboardInterrupt:
    speed = {1:0, 2:0}
    dxl_io.set_moving_speed(speed)
    cap.release()
    exit()

