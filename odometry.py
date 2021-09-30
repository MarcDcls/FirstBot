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
"""while T > 0:
    w_l, w_r = dxl_io.get_moving_speed(ids)
   
    v, w = direct_kinematics(w_l, w_r)

    dt = time.time() - current
    current += dt
    T -= dt

    X, Y, THETA = kinematic.tick_odom(X, Y, THETA, v, w, dt)

    #print("X :", X, "\nY :", Y, "\nTHETA :", THETA,"\nw_l : ",w_l,"\nw_r :",w_r)"""

time.sleep(10)

last_position = dxl_io.get_present_position(ids)
distance = math.sqrt((last_position[0]-first_position[0])*(last_position[0]-first_position[0]) + (last_position[1]-first_position[1])*(last_position[1]-first_position[1]))
print("last position : ",last_position)
print(distance)
