import time
import pypot.dynamixel

from robot import *

################################ DESTINATION ################################

X = 0
Y = 1
THETA = 0

################################# VARIABLES #################################

FRAMERATE = 1 / 30
MOTOR_SPEED = 200

LINEAR_FACTOR = 0.02
ANGULAR_FACTOR = 2

ports = pypot.dynamixel.get_available_ports()
if not ports:
	exit('No port')

port = ports[0]
print('Using the first on the list', port)

dxl_io = pypot.dynamixel.DxlIO(port)
print('Connected!')

found_ids = dxl_io.scan([1,2])
print('Found ids:', found_ids)

ids = found_ids[:2]

dxl_io.enable_torque(ids)


robot = Robot()

current_time = time.time()
while abs(X - x) > 0.03 or abs(Y - y) > 0.03:
	distance = np.sqrt((X - x) ** 2 + (Y - y) ** 2)
	v = LINEAR_FACTOR * distance

	angle = np.arctan2(Y - y, X - x) - np.pi / 2
	w = ANGULAR_FACTOR * angle
	# print("angle :", angle)
	# print("v, w :", v, w)

	w_l, w_r = inverse_kinematics(v, w)
	speed = {1: w_l, 2: w_r}
	# print("Speed :", speed)
	dxl_io.set_moving_speed(speed)

	dt = time.time() - current_time
	current_time += dt

	robot.odom(v, w, dt)
	# print("x, y, theta :", x, y, theta)
	time.sleep(FRAMERATE)


