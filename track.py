import cv2
import numpy as np

def nothing(x):
    print(x)

img = np.zeros((300,512,3), np.uint8)

cv2.namedWindow('t', flags=cv2.WINDOW_AUTOSIZE)

cv2.createTrackbar('R', 't', 0, 255, nothing)
cv2.createTrackbar('G', 't', 0, 255, nothing)
cv2.createTrackbar('B', 't', 0, 255, nothing)

while(1):
	cv2.imshow('t', img)

	k = cv2.waitKey(1) & 0xFF
	
	if k == 27:
		break
	
	r = cv2.getTrackbarPos('R','t')
	g = cv2.getTrackbarPos('G','t')
	b = cv2.getTrackbarPos('B','t')

	img[:] = [b,g,r]
