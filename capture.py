import cv2 as cv
from process import processing

cap = cv.VideoCapture(2)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?).")
        continue

    #cv.imwrite('img.jpg', frame)
    processing(frame)
    
    cv.imshow('frame', frame)
    if cv.waitKey(1) == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()