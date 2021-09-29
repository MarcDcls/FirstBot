import pypot.dynamixel
import itertools
import numpy
import time

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

speed = dict(zip(ids, itertools.repeat(1)))
dxl_io.set_moving_speed(speed)


