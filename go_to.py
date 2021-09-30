import time

import kinematic
from kinematic import *

################################ DESTINATION ################################

X = 1
Y = 1
THETA = 0

################################# VARIABLES #################################

FRAMERATE = 1 / 30
MOTOR_SPEED = 200

LINEAR_FACTOR = 0.0001
ANGULAR_FACTOR = 0.0001

# ports = pypot.dynamixel.get_available_ports()
# if not ports:
# 	exit('No port')
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
#
# dxl_io.enable_torque(ids)
#
# speed = dict(zip(ids, itertools.repeat(1)))
# dxl_io.set_moving_speed(speed)


x = 0
y = 0
theta = 0
t1 = time.time()
while abs(X - x) > 0.03 or abs(Y - y) > 0.03:
	distance = np.sqrt((X - x) ** 2 + (Y - y) ** 2)
	v = LINEAR_FACTOR * distance
	angle = np.arctan2(Y - y, X - x)
	w = ANGULAR_FACTOR * distance

	w_l, w_r = kinematic.inverse_kinematics(v, w)
	speed = {1: w_l, 2: w_r}
	print("Speed :", speed)
	# dxl_io.set_moving_speed(speed)

	t2 = time.time()
	dt = t1 - t2
	t1 = t2

	x, y, theta = kinematic.tick_odom(x, y, theta, v, w, dt)
	print("x, y, theta :", x, y, theta)

time.sleep(FRAMERATE)
