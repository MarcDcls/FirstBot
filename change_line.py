import sys

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

FIRST_LOOP = 2

line_color = "blue"
nb_args = len(sys.argv)
if nb_args > 1:
    line_color = sys.argv[1]

default_speed, p = init_values(line_color)

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

speed = (-default_speed, default_speed)

cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

i = 0

change_line = False
initial_time = 0

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?).")
            continue

        x, y, change = processing(frame)
        print("x, y :", x, y)

        """if change and not change_line:
            change_line = True
            # dxl_io.set_moving_speed({1:0, 2:0})
            if line_color == "blue":
                line_color = "red"
                default_speed, p = init_values("red")
                initial_time = time.time()
            else:
                line_color = "blue"
                default_speed, p = init_values("blue")

        elif not change:
            change_line = False"""

        # print(line_color)

        if x == None:
            print("No Line")
            dxl_io.set_moving_speed({
                1: speed[0],
                2: speed[1]
            })

        #     print("No line detected.")
        #     s = 40
        #     mean_speed = {
        #         1: -default_speed + s,
        #         2: default_speed + s
        #     }
        #     dxl_io.set_moving_speed(mean_speed)
        #
        # else:
        else:
            speed = (
                - default_speed + 0.65 * x,
                default_speed + 0.65 * x
            )
            print(x)
            print(speed)

            dxl_io.set_moving_speed({
                1: speed[0],
                2: speed[1]
            })

except KeyboardInterrupt:
    speed = {1: 0, 2: 0}
    dxl_io.set_moving_speed(speed)
    cap.release()
    exit()
