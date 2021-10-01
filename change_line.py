import time

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
RED_TIME_2 = 44
RED_TIME_3 = 48

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
        print("x, y :", x, y)

        if x == None:
            print("No Line")
            dxl_io.set_moving_speed({
                1: speed[0],
                2: speed[1]
            })

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
        if time.time() - initial_time > BLUE_TIME:
            break

    initial_time = time.time()
    init_values("red")
    speed = (-RED_SPEED, RED_SPEED)
    while True:

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
                RED_SPEED - 250
            )

            dxl_io.set_moving_speed({
                1: speed[0],
                2: speed[1]
            })
            continue

        elif RED_TIME_3 < time.time() - initial_time < RED_TIME_3 + 2:
            speed = (
                - RED_SPEED + 150,
                RED_SPEED
            )

            dxl_io.set_moving_speed({
                1: speed[0],
                2: speed[1]
            })
            continue

        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?).")
            continue

        x, y, change = processing(frame)
        print("x, y :", x, y)

        if x == None:
            print("No Line")
            dxl_io.set_moving_speed({
                1: speed[0],
                2: speed[1]
            })

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

except KeyboardInterrupt:
    speed = {1: 0, 2: 0}
    dxl_io.set_moving_speed(speed)
    cap.release()
    exit()
