import time

import cv2 as cv
import pypot.dynamixel
from robot import *

from image_processing import processing, init_values

# def mean(list_speed):
#     sum_1 = 0
#     sum_2 = 0
#     l = len(list_speed)
#     for i in range(l):
#         sum_1 += list_speed[i][0]
#         sum_2 += list_speed[i][1]
#     return sum_1/l, sum_2/l

ports = pypot.dynamixel.get_available_ports()

if not ports:
    exit('No port')

port = ports[0]
print('Using the first on the list', port)

dxl_io = pypot.dynamixel.DxlIO(port)
print('Connected!')

found_ids = dxl_io.scan([1, 2])
print('Found ids:', found_ids)

ids = found_ids[:2]
dxl_io.enable_torque(ids)

cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

BLUE_SPEED = 500
RED_SPEED = 400
BLUE_TIME = 34
RED_TIME_1 = 8
RED_TIME_2 = 45
RED_TIME_3 = 46

blue_x = []
blue_y = []
red_x = []
red_y = []
robot = Robot()

try:
    initial_time = time.time()
    init_values("blue")
    speed = (-BLUE_SPEED, BLUE_SPEED)
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?).")
            continue

        vari, _, _ = processing(frame)

        if vari is None:
            print("No Line")

        else:
            if vari == 0:
                speed = (
                    - BLUE_SPEED,
                    BLUE_SPEED
                )
            else:
                speed = (
                    - BLUE_SPEED + 0.5 * vari + 0.001 * (vari / abs(vari)) * vari ** 2,
                    BLUE_SPEED + 0.5 * vari + 0.001 * (vari / abs(vari)) * vari ** 2
                )

        dxl_io.set_moving_speed({
            1: speed[0],
            2: speed[1]
        })

        x, y = robot.odom(direct_kinematics())
        blue_x.append(x)
        blue_y.append(y)
        if time.time() - initial_time > BLUE_TIME:
            break

    initial_time = time.time()
    init_values("red")
    speed = (-RED_SPEED, RED_SPEED)
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?).")
            continue

        vari, _, _ = processing(frame)

        if RED_TIME_1 < time.time() - initial_time < RED_TIME_1 + 2:
            speed = (
                - RED_SPEED,
                RED_SPEED - 250
            )

        elif RED_TIME_2 < time.time() - initial_time < RED_TIME_2 + 1:
            speed = (
                - RED_SPEED,
                RED_SPEED
            )

        elif RED_TIME_3 < time.time() - initial_time < RED_TIME_3 + 3:
            speed = (
                - RED_SPEED + 200,
                RED_SPEED
            )

        else:
            if vari == 0:
                speed = (
                    - RED_SPEED,
                    RED_SPEED
                )
            else:
                speed = (
                    - RED_SPEED + 0.6 * vari + 0.0005 * (vari / abs(vari)) * vari ** 2,
                    RED_SPEED + 0.6 * vari + 0.0005 * (vari / abs(vari)) * vari ** 2
                )

        dxl_io.set_moving_speed({
            1: speed[0],
            2: speed[1]
        })

        x, y = robot.odom(direct_kinematics())
        blue_x.append(x)
        blue_y.append(y)

except KeyboardInterrupt:
    speed = {1: 0, 2: 0}
    dxl_io.set_moving_speed(speed)
    cap.release()
    exit()
