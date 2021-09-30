import pypot.dynamixel
import itertools
import time

from kinematic import *

################################ DESTINATION ################################

X = 0
Y = 0
THETA = 0

################################# VARIABLES #################################

FRAMERATE = 1 / 30
MOTOR_SPEED = 200

#
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




initial_theta = np.arctan2(Y, X)
while initial_theta > 0:

	dxl_io.set_moving_speed(speed)
	time.sleep(FRAMERATE)
