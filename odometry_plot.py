import time

import pypot.dynamixel

from robot import *

import matplotlib.pyplot as plt

################################### TIMER ###################################

T = 20

#############################################################################

FRAMERATE = 1 / 120

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
dxl_io.disable_torque(ids)

#array of coordinates
coordinates = ([],[])

try:
    robot = Robot()
    current_time = time.time()

    i = 0
    j = 1
    while T > 0:
        i += 1
        w_r, w_l = dxl_io.get_present_speed(ids)
        w_r, w_l = - w_r * (np.pi / 180), w_l * (np.pi / 180)
        v, w = direct_kinematics(w_l, w_r)
        # print("SPEED :", w_r, w_l)

        dt = time.time() - current_time
        current_time += dt
        T -= dt

        robot.odom(v, w, dt)

        coordinates[0].append(robot.x)
        coordinates[1].append(robot.y)
        
        if i / 100 == j:
            j += 1
            # print("v, w :", v, w)
            print("X :", robot.x, "\nY :", robot.y, "\nTHETA :", robot.theta)

        time.sleep(FRAMERATE)

    # print("X :", X, "\nY :", Y, "\nTHETA :", THETA)

plt.plot(coordinates[0],coordinates[1])
plt.savefig('trace_odometry.png')

except KeyboardInterrupt:
    speed = {1:0, 2:0}
    dxl_io.set_moving_speed(speed)
    exit()

