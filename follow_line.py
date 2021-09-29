import cv2 as cv
from image_processing import processing, init_color
import pypot.dynamixel
import sys


line_color = "blue"
nb_args = len(sys.argv)
if nb_args > 1:
    line_color = sys.argv[1]

init_color(line_color)


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

speed = {
    1 : -300,
    2 : 300
}


cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

list_speed = [(-200,200)]*30


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
        mean_speed = {1:np.mean(list_speed,axis=0),2:np.mean(list_speed,axis=1)}
        dxl_io.set_moving_speed(mean_speed)

    else:

        speed = {1 :-300 +0.8* x,2 : 300 +0.8* x}
        del list_speed[0]
        list_speed.append(speed)
        print(speed)

        dxl_io.set_moving_speed(speed)
 
    if cv.waitKey(1) == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
