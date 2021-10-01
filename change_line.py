import sys
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


BLUE_TIME = 34
initial_time = time.time()
try:
    default_speed, p = init_values("blue")
    speed = (-default_speed, default_speed)
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
            speed = (
                - default_speed + 0.5 * x,
                default_speed + 0.5 * x
            )
            print(x)
            print(speed)

            dxl_io.set_moving_speed({
                1: speed[0],
                2: speed[1]
            })
        if time.time() - initial_time > BLUE_TIME :
            break

    default_speed, p = init_values("red")
    speed = (-default_speed, default_speed)
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
            speed = (
                - default_speed + 0.8 * (x / abs(x)) * x ** 2,
                default_speed + 0.8 * (x / abs(x)) * x ** 2
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
