import cv2
import numpy as np

def nothing(x):
	print(x)

#im = cv2.imread("test/Trafico/1277381674Image000016.jpg")
im = cv2.imread("test/Trafico/1277381680Image000009.jpg")
#im = cv2.imread("test/Trafico/1277382390Image000004.jpg")
#cv2.startWindowThread()

im = cv2.resize(im, (0,0), fx=0.5, fy=0.5) 
hsv_im = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)

azul = [[156.,145.,103.],[163.,194.,134.]]

azul[0][0] = azul[0][0] * 180. / 256.
azul[1][0] = azul[1][0] * 180. / 256.

azulmin = (109, 145, 103)
azulmax = (114, 194, 134)

cv2.namedWindow('t')
cv2.createTrackbar('low', 't', 0, 255, nothing)
cv2.createTrackbar('upp', 't', 0, 255, nothing)

while 1:
	low = cv2.getTrackbarPos('low','t')
	upp = cv2.getTrackbarPos('upp','t')

	mask = cv2.inRange(hsv_im, np.array(azul[0]), np.array(azul[1]))
#	mask = cv2.inRange(hsv_im, (low, 0, 0), (upp, 255, 255))
#	circles = cv2.HoughCircles(mask, cv2.HOUGH_GRADIENT, 1, 20)
#	hsv_im = cv2.cvtColor(im, cv2.COLOR_2HSV)
#	print(str(circles))
#	print(str(mask))
	cv2.imshow("imagen", mask)
	
	k = cv2.waitKey(100) & 0xFF

	if k == 27:
	        break

#	print('key = '+str(k))

cv2.destroyAllWindows()
