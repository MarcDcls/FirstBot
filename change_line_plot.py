import time
from robot import *
import cv2 as cv
import pypot.dynamixel

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

        x, y, change = processing(frame)

        if x == None:
            print("No Line")

        else:
            if x == 0:
                speed = (
                    - BLUE_SPEED,
                    BLUE_SPEED
                )
            else:
                speed = (
                    - BLUE_SPEED + 0.5 * x + 0.001 * (x / abs(x)) * x ** 2,
                    BLUE_SPEED + 0.5 * x + 0.001 * (x / abs(x)) * x ** 2
                )

        dxl_io.set_moving_speed({
            1: speed[0],
            2: speed[1]
        })

        xx, yy = robot.odom(direct_kinematics(speed[0], speed[1]))
        blue_x.append(xx)
        blue_y.append(yy)

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

        x, y, change = processing(frame)

        if RED_TIME_1 < time.time() - initial_time < RED_TIME_1 + 2:
            speed = (
                - RED_SPEED,
                RED_SPEED - 250
            )

            dxl_io.set_moving_speed({
                1: speed[0],
                2: speed[1]
            })
            continue

        elif RED_TIME_2 < time.time() - initial_time < RED_TIME_2 + 1:
            speed = (
                - RED_SPEED,
                RED_SPEED
            )

            dxl_io.set_moving_speed({
                1: speed[0],
                2: speed[1]
            })
            continue

        elif RED_TIME_3 < time.time() - initial_time < RED_TIME_3 + 2.5:
            speed = (
                - RED_SPEED + 200,
                RED_SPEED
            )

        elif x == None:
            print("No Line")

        else:
            if x == 0:
                speed = (
                    - RED_SPEED,
                    RED_SPEED
                )
            else:
                speed = (
                    - RED_SPEED + 0.6 * x + 0.0005 * (x / abs(x)) * x ** 2,
                    RED_SPEED + 0.6 * x + 0.0005 * (x / abs(x)) * x ** 2
                )

        dxl_io.set_moving_speed({
            1: speed[0],
            2: speed[1]
        })

        xx, yy = robot.odom(direct_kinematics(speed[0], speed[1]))
        red_x.append(xx)
        red_y.append(yy)

except KeyboardInterrupt:
    speed = {1: 0, 2: 0}
    dxl_io.set_moving_speed(speed)
    cap.release()
    exit()

# import cv2 as cv
# from image_processing import processing, init_values
# import pypot.dynamixel
# import sys
# import numpy as np
# import time
#
# # def mean(list_speed):
# #     sum_1 = 0
# #     sum_2 = 0
# #     l = len(list_speed)
# #     for i in range(l):
# #         sum_1 += list_speed[i][0]
# #         sum_2 += list_speed[i][1]
# #     return sum_1/l, sum_2/l
#
# FIRST_LOOP = 2
#
# line_color = "blue"
# nb_args = len(sys.argv)
# if nb_args > 1:
#     line_color = sys.argv[1]
#
# default_speed, p = init_values(line_color)
#
#
# ports = pypot.dynamixel.get_available_ports()
# if not ports:
#     exit('No port')
#
# port = ports[0]
# print('Using the first on the list', port)
#
# dxl_io = pypot.dynamixel.DxlIO(port)
# print('Connected!')
#
# found_ids = dxl_io.scan([1,2])
# print('Found ids:', found_ids)
#
# ids = found_ids[:2]
# dxl_io.enable_torque(ids)
#
# speed = (-default_speed, default_speed)
#
# cap = cv.VideoCapture(0)
# if not cap.isOpened():
#     print("Cannot open camera")
#     exit()
#
# i = 0
#
# change_line = False
# initial_time = 0
#
# coordinates_blue = ([],[])
# coordinates_red = ([],[])
#
# try:
#     robot = Robot()
#     current_time = time.time()
#
#     i = 0
#     j = 1
#     while True:
#         i += 1
#         ret, frame = cap.read()
#         if not ret:
#             print("Can't receive frame (stream end?).")
#             continue
#
#         x, y, change = processing(frame)
#
#         if change and not change_line:
#             change_line = True
#             # dxl_io.set_moving_speed({1:0, 2:0})
#             if line_color == "blue":
#                 default_speed, p = init_values("red")
#                 initial_time = time.time()
#             else:
#                 default_speed, p = init_values("blue")
#
#         elif not change:
#             change_line = False
#
#         print(line_color)
#         #odometry
#         i += 1
#         w_r, w_l = dxl_io.get_present_speed(ids)
#         w_r, w_l = - w_r * (np.pi / 180), w_l * (np.pi / 180)
#         v, w = direct_kinematics(w_l, w_r)
#         # print("SPEED :", w_r, w_l)
#
#         dt = time.time() - current_time
#         current_time += dt
#         T -= dt
#
#         robot.odom(v, w, dt)
#         if line_color == "blue":
#             coordinates_blue[0].append(robot.x)
#             coordinates_blue[1].append(robot.y)
#         else:
#             if line_color == "red":
#                 coordinates_red[0].append(robot.x)
#                 coordinates_red[1].append(robot.y)
#         if x == None:
#             print("No line detected.")
#             s = 40
#             mean_speed = {
#                 1: -default_speed + s,
#                 2: default_speed + s
#             }
#             dxl_io.set_moving_speed(mean_speed)
#
#         else:
#
#             speed = (
#                 -default_speed + 0.5*x,
#                 default_speed + 0.5*x
#             )
#             print(x)
#             print(speed)
#
#             dxl_io.set_moving_speed({
#                 1: speed[0],
#                 2: speed[1]
#             })
#
#     plt.plot(coordinates_blue[0],coordinates_blue[1],'b')
#     plt.plot(coordinates_red[0],coordinates_red[1],'r')
#     plt.savefig('trace_line.png')
#
# except KeyboardInterrupt:
#     speed = {1:0, 2:0}
#     dxl_io.set_moving_speed(speed)
#     cap.release()
#     exit()
#
