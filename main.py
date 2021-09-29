import cv2 as cv
from process import processing
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
cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
    
speed = {1 :-200 ,2 : 200 }

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?).")
        continue

    #cv.imwrite('img.jpg', frame)
    x, y = processing(frame)

    if x==None:
       #speed={1:0,2:0}
       dxl_io.set_moving_speed(speed)
       exit()
    
    speed = {1 :-200 + 0.5*x,2 : 200 + 0.5*x}
    print(speed)

    dxl_io.set_moving_speed(speed)
 
    if cv.waitKey(1) == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
