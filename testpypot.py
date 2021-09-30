import pypot.dynamixel
import time

ports = pypot.dynamixel.get_available_ports()
port = ports[0]
dxl_io = pypot.dynamixel.DxlIO(port)

dxl_io.disable_torque([1,2])

speed = {
    1 : -100,
    2 : 100
}
for i in range 50:100 
    dxl_io.set_moving_speed(speed)

    print(dxl_io.get_present_position([1,2]))
    print(dxl_io.get_moving_speed([1,2]))

    time.sleep(0.5)
