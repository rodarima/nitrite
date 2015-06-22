#coding=utf-8

import cv2
import numpy as np
import os
from ConfigParser import SafeConfigParser as Conf

PREPROCESS_CONFIG = "config/preprocess.conf"

class Preprocess:
	def __init__(self, img):
		self.img = img
		self.config = Conf()
		self.config.read(PREPROCESS_CONFIG)

	def equalize_channel(self, img, c):
		'Ecualiza el canal indicado en la imagen, sobreescribiéndolo'
		img_channel = img[:,:,c]
		eq = cv2.equalizeHist(img_channel)
		img[:,:,c] = eq
		return img

	def threshold_hsv(self, hsv_img, v):
		(th, ts, tv) = v[0]
		(tH, tS, tV) = v[1]

		if th < tH:
			mask = cv2.inRange(hsv_img, (th, ts, tv), (tH, tS, tV))
		else:
			mask1 = cv2.inRange(hsv_img, (th, ts, tv), (180, tS, tV))
			mask2 = cv2.inRange(hsv_img, (0, ts, tv), (tH, tS, tV))
			mask = cv2.bitwise_or(mask1, mask2)
		return mask

	def create_trackbars(self, v, name):
		(th, ts, tv) = v[0]
		(tH, tS, tV) = v[1]
		cv2.namedWindow(name)
		cv2.createTrackbar('th', name, th, 180, nothing)
		cv2.createTrackbar('tH', name, tH, 180, nothing)
		cv2.createTrackbar('ts', name, ts, 256, nothing)
		cv2.createTrackbar('tS', name, tS, 256, nothing)
		cv2.createTrackbar('tv', name, tv, 256, nothing)
		cv2.createTrackbar('tV', name, tV, 256, nothing)

	def save_conf(self):
		f = open(PREPROCESS_CONFIG, 'w')
		try:
			self.config.write(f)
		finally:
			f.close()

	def get_color(self, col):
		sec = self.config[col]
		v_min = [sec['th'], sec['ts'], sec['tv']]
		v_max = [sec['tH'], sec['tS'], sec['tV']]
		return [v_min, v_max]

	def process_color(self, v, col):
		v = get_color(col)
		

	def edit_color(self, col):
		v = get_color(col)
		create_trackbars(v, col)
		process_color(v, col)

class Sign:
	def __init__(self, path):
		self.load_images(path)

	def load_images(self, path):
		imgs = os.listdir(self.path)
		self.imgs = [os.path.join(self.path,i) for i in imgs]

	def nothing(x): pass

im = cv2.imread("test/color/1.jpg")
p = Preprocess(im)
edit_color('Blue')

#	#im = cv2.imread("test/Trafico/1277381674Image000016.jpg")
#	#im = cv2.imread("test/Trafico/1277381680Image000009.jpg")
#	#im = cv2.imread("test/Trafico/1277382390Image000004.jpg")
#	#im = cv2.imread("test/Trafico/1277381967Image000014.jpg")
#	im = cv2.imread("test/color/1.jpg")
#	#cv2.startWindowThread()
#
#	im = cv2.resize(im, (0,0), fx=0.5, fy=0.5)
#	hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV) #BGR?
#	ycrcb = cv2.cvtColor(im, cv2.COLOR_BGR2YCR_CB)
#
#	hsv_eq = equalize_channel(hsv, 2)
#	ycrcb_eq = equalize_channel(ycrcb, 2)
#
#	#azul = [[156.,145.,103.],[163.,194.,134.]]
#	azul = [[156,0,0],[163,0,0]]
#
#	azul[0][0] = azul[0][0] * 180. / 256.
#	azul[1][0] = azul[1][0] * 180. / 256.
#
#	#azulmin = (109, 145, 103)
#	#azulmax = (114, 194, 134)
#
#	th = 13
#	tH = 31
#	ts = 79
#	tS = 189
#	tv = 31
#	tV = 145
#
#	hc1 = 2
#	hc2 = 20
#	hp1 = 50
#	hp2 = 30
#	hcM = 0
#	hcm = 0
#	blur = 1
#
#	cv2.namedWindow('t')
#	cv2.createTrackbar('th', 't', th, 180, nothing)
#	cv2.createTrackbar('tH', 't', tH, 180, nothing)
#	cv2.createTrackbar('ts', 't', ts, 256, nothing)
#	cv2.createTrackbar('tS', 't', tS, 256, nothing)
#	cv2.createTrackbar('tv', 't', tv, 256, nothing)
#	cv2.createTrackbar('tV', 't', tV, 256, nothing)
#
#	cv2.namedWindow('c')
#	cv2.createTrackbar('hc1', 'c', hc1, 200, nothing)
#	cv2.createTrackbar('hc2', 'c', hc2, 200, nothing)
#	cv2.createTrackbar('hp1', 'c', hp1, 200, nothing)
#	cv2.createTrackbar('hp2', 'c', hp2, 200, nothing)
#	cv2.createTrackbar('hcM', 'c', hcM, 200, nothing)
#	cv2.createTrackbar('hcm', 'c', hcm, 200, nothing)
#	cv2.createTrackbar('blur', 'c', blur, 200, nothing)
#
#	while 1:
#	#	low = cv2.getTrackbarPos('low','t')
#	#	upp = cv2.getTrackbarPos('upp','t')
#		th = cv2.getTrackbarPos('th','t')
#		ts = cv2.getTrackbarPos('ts','t')
#		tv = cv2.getTrackbarPos('tv','t')
#		tH = cv2.getTrackbarPos('tH','t')
#		tS = cv2.getTrackbarPos('tS','t')
#		tV = cv2.getTrackbarPos('tV','t')
#		hc1 = max(1, cv2.getTrackbarPos('hc1','c'))
#		hc2 = max(1, cv2.getTrackbarPos('hc2','c'))
#		hp1 = max(1, cv2.getTrackbarPos('hp1','c'))
#		hp2 = max(1, cv2.getTrackbarPos('hp2','c'))
#		hcM = cv2.getTrackbarPos('hcM','c')
#		hcm = cv2.getTrackbarPos('hcm','c')
#		blur = cv2.getTrackbarPos('blur','c')
#
#		print("H={}..{}, S={}..{}, V={}..{}".format(th,ts,tv,tH,tS,tV))
#		print("hc1={}, hc2={}".format(hc1, hc2))
#
#	#	mask = cv2.inRange(hsv_eq, np.array(azul[0]), np.array(azul[1]))
#	#	mask = cv2.inRange(hsv_eq, (low, 0, 0), (upp, 255, 255))
#		if th<tH:
#			mask = cv2.inRange(hsv_eq, (th, ts, tv), (tH, tS, tV))
#		else:
#			mask1 = cv2.inRange(hsv_eq, (th, ts, tv), (180, tS, tV))
#			mask2 = cv2.inRange(hsv_eq, (0, ts, tv), (tH, tS, tV))
#			mask = cv2.bitwise_or(mask1, mask2)
#
#		mask = cv2.medianBlur(mask, blur*2+1)
#		circles = cv2.HoughCircles(mask, cv2.cv.CV_HOUGH_GRADIENT, hc1, hc2,
#			param1=hp1,param2=hp2,minRadius=hcm,maxRadius=hcM)
#
#		cimg = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
#		if circles != None:
#			circles = np.uint16(np.around(circles))
#			#rgb_eq = cv2.cvtColor(ycrcb_eq, cv2.COLOR_YCR_CB2BGR)
#			for i in circles[0,:]:
#				# draw the outer circle
#				cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
#				# draw the center of the circle
#				cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)
#
#		cv2.imshow("circle", cimg)
#		cv2.imshow("original", im)
#
#
#	#	hsv_im = cv2.cvtColor(im, cv2.COLOR_2HSV)
#	#	print(str(circles))
#	#	print(str(mask))
#	#	cv2.imshow("imagen", mask)
#		#cv2.imshow("rgb", rgb)
#		#cv2.imshow("rgb_eq", rgb_eq)
#	#	cv2.imshow("mask", mask)
#
#		k = cv2.waitKey(100) & 0xFF
#
#		if k == 27:
#				break
#
#	#	print('key = '+str(k))
#
#	cv2.destroyAllWindows()
