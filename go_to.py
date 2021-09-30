import time

import pypot.dynamixel

from robot import *

################################ DESTINATION ################################

X = 0
Y = 1
THETA = 0

################################# VARIABLES #################################

FRAMERATE = 1 / 30

LINEAR_FACTOR = 0.1
ANGULAR_FACTOR = 2

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

try:
    robot = Robot()
    current_time = time.time()

    while abs(X - robot.x) > 0.03 or abs(Y - robot.y) > 0.03:
        distance = np.sqrt((X - robot.x) ** 2 + (Y - robot.y) ** 2)
        v = LINEAR_FACTOR * distance

        angle = np.arctan2(Y - robot.y, X - robot.x) - np.pi / 2
        w = ANGULAR_FACTOR * angle
        # print("angle :", angle)
        print("v, w :", v, w)

        w_l, w_r = inverse_kinematics(v, w)
        speed = {1: - w_r * 180 / np.pi, 2: w_l * 180 / np.pi}
        print("Speed :", speed)
        dxl_io.set_moving_speed(speed)

        dt = time.time() - current_time
        current_time += dt

        robot.odom(v, w, dt)
        print("x, y, theta :", robot.x, robot.y, robot.theta)
        time.sleep(FRAMERATE)

except KeyboardInterrupt:
    speed = {1: 0, 2: 0}
    dxl_io.set_moving_speed(speed)
    exit()
