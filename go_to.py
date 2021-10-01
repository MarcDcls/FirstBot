import time

import pypot.dynamixel

from robot import *

################################ DESTINATION ################################

X = 1
Y = 0
THETA = 0 # - np.pi / 2

################################# VARIABLES #################################

FRAMERATE = 1 / 30

LINEAR_FACTOR = 0.4
ANGULAR_FACTOR = 1
DELTA = 0.03

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
    initial_distance = np.sqrt(X ** 2 + Y ** 2)
    initial_angle = np.arctan2(X + robot.x, Y - robot.y)
    sign = 1
    if abs(initial_angle) > np.pi / 2:
        sign = - 1
        if initial_angle > 0:
            initial_angle -= np.pi / 2
        else:
            initial_angle += np.pi / 2

    distance = initial_distance
    while distance > DELTA:
        distance = np.sqrt((X + robot.x) ** 2 + (Y - robot.y) ** 2)
        # print(distance)
        # print("x, y :", robot.x, robot.y)
        v = sign * LINEAR_FACTOR * distance

        angle = robot.theta - np.arctan2(X + robot.x, Y - robot.y)
        w = sign * ANGULAR_FACTOR * angle
        print("angle :", angle)
        print("v, w :", v, w)

        w_l, w_r = inverse_kinematics(v, w)
        speed = {1: - w_l * 180 / np.pi, # * (initial_distance - distance),
                 2: w_r * 180 / np.pi} # * (initial_distance - distance)}
        # print("Speed :", speed)
        dxl_io.set_moving_speed(speed)

        dt = time.time() - current_time
        current_time += dt

        robot.odom(v, w, dt)
        # print("x, y, theta :", robot.x, robot.y, robot.theta)
        time.sleep(FRAMERATE)

    speed = {1: 0, 2: 0}
    dxl_io.set_moving_speed(speed)

except KeyboardInterrupt:
    speed = {1: 0, 2: 0}
    dxl_io.set_moving_speed(speed)
    exit()
