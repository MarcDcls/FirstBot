import time

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

FRAMERATE = 1 / 30

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
print("first position : ", first_position)

new_pr, new_pl = dxl_io.get_present_position(ids)

# positions = []

while T > 0:
    old_pl = new_pl
    old_pr = new_pr
    new_pr, new_pl = dxl_io.get_present_position(ids)
    # print("angle relatif droite :", first_position[0] - new_pr)
    # print("angle relatif gauche :", new_pl - first_position[1])

    diff_l = new_pl - old_pl
    diff_r = old_pr - new_pr
    print("L :", diff_l, "R :", diff_r)

    # if diff_l > 180:
    #     if new_pl < old_pl:
    #         diff_l = (new_pl - old_pl) % 360
    #     else:
    #         diff_l = (old_pl - new_pl) % 360
    # if diff_r > 180:
    #     if new_pr < old_pr:
    #         diff_r = (new_pr - old_pr) % 360
    #     else:
    #         diff_r = (old_pr - new_pr) % 360

    dt = time.time() - current
    current += dt
    T -= dt

    w_l = diff_l * (np.pi / 180) / dt
    w_r = diff_r * (np.pi / 180) / dt

    v, w = direct_kinematics(w_l, w_r)

    X, Y, THETA = kinematic.tick_odom(X, Y, THETA, v, w, dt)

    # positions.append((X, Y, THETA))

    print("X :", X, "\nY :", Y, "\nTHETA :", THETA)

    time.sleep(FRAMERATE)

# with open("positions.json", 'x') as f:
#     json.dump(positions, f)
