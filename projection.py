import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('img3.jpg')

cv2.circle(img, (349, 0), 5, (0, 0, 255), -1) # top left
cv2.circle(img, (462, 0), 5, (0, 0, 255), -1) # top right
cv2.circle(img, (345,476), 5, (0, 0, 255), -1) # bottom left
cv2.circle(img, (504, 478), 5, (0, 0, 255), -1) # bottom right

#cv2.imshow("Image", img)
#cv2.waitKey(0)

pts1 = np.float32(
        [[349,0], # top left
         [462,0], # top right
         [345,476], # bottom left
         [504,478]] # bottom right
)

pts2 = np.float32(
        [[0,0], # top left
         [639,0], # top right
         [0,479], # bottom left
         [639,479]] # bottom right
)

matrix = cv2.getPerspectiveTransform(pts1,pts2)
result = cv2.warpPerspective(img, matrix, (639,479)) # set size image based on pts2 (w = 500 h = 600)


plt.subplot(1,2,1),
plt.imshow(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))
plt.title('Original Image')

plt.subplot(1,2,2),
plt.imshow(cv2.cvtColor(result,cv2.COLOR_BGR2RGB))
plt.title('Result')

plt.show()
cv2.waitKey(0)

