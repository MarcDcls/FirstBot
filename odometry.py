import time, math

import pypot.dynamixel

import kinematic
from kinematic import *

################################### TIMER ###################################

T = 10

############################### RETURN VALUES ###############################

X = 0
Y = 0
THETA = 0

#############################################################################


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
current = time.time()
first_position = dxl_io.get_present_position(ids)
print("first position : ",first_position)

old_pl, old_pr = dxl_io.get_present_position(ids)

while T > 0:
    old_pl = new_pl
    old_pr = new_pr
    new_pl, new_pr = dxl_io.get_present_position(ids)
    diff_l = new_pl-old_pl
    diff_r = new_pr-old_pr

    dt = time.time() - current
    current += dt
    T -= dt

    speed_l = diff_l / dt
    speed_r = diff_r / dt
    speed_l *= (math.pi/180)
    speed_r *= (math.pi/180)

    v, w = direct_kinematics(speed_l, speed_r)

    X, Y, THETA = kinematic.tick_odom(X, Y, THETA, v, w, dt)

    print("X :", X, "\nY :", Y, "\nTHETA :", THETA)

