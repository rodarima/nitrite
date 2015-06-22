# -*- coding: utf-8 -*-

import numpy as np
import cv2

class Image:

	def __init__(self, img):
		self.img = img

	def convert(self, to):
		raise NotImplemented()


class ImageGray(Image):

	def convert(self, to):
		to = to.lower()
		if to == 'gray':
			return self
		else:
			rgb = ImageRGB(cv2.cvtColor(self.img, cv2.COLOR_GRAY2RGB))
			return rgb.convert(to)

	def show(self):
		cv2.imshow('img', self.img)



class ImageColor(Image):

	def show(self):
		bgr = self.convert('bgr')
		cv2.imshow('img', bgr.img)


class ImageRGB(ImageColor):
	def channel(self, c):
		c = c.lower()
		if c == 'r': return self.img[:,:,0]
		elif c == 'g': return self.img[:,:,1]
		elif c == 'b': return self.img[:,:,2]
		else:
			raise ValueError('Unknown channel "' + c + '"')

	def convert(self, to):
		to = to.lower()
		if to == 'rgb':
			return self
		elif to == 'gray':
			return ImageGray(cv2.cvtColor(self.img, cv2.COLOR_RGB2GRAY))
		elif to == 'bgr':
			return ImageBGR(cv2.cvtColor(self.img, cv2.COLOR_RGB2BGR))
		elif to == 'hsl' or to == 'hls':
			return ImageHSL(cv2.cvtColor(self.img, cv2.COLOR_RGB2HLS))
		elif to == 'hsv':
			return ImageHSV(cv2.cvtColor(self.img, cv2.COLOR_RGB2HSV))
		elif to == 'ycrcb' or to == 'ycc' or to == 'ycr_cb':
			return ImageYCRCB(cv2.cvtColor(self.img, cv2.COLOR_RGB2YCR_CB))
		else:
			raise ValueError('Unknown space color "' + to + '"')

class ImageBGR(ImageColor):
	def convert(self, to):
		to = to.lower()
		if to == 'bgr':
			return self
		else:
			rgb = ImageRGB(cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB))
			return rgb.convert(to)

class ImageHSL(ImageColor):
	def channel(self, c):
		c = c.lower()
		if c == 'h': return self.img[:,:,0]
		elif c == 's': return self.img[:,:,1]
		elif c == 'l': return self.img[:,:,2]
		else:
			raise ValueError('Unknown channel "' + c + '"')
	def convert(self, to):
		to = to.lower()
		if to == 'hsl' or to == 'hls':
			return self
		else:
			rgb = ImageRGB(cv2.cvtColor(self.img, cv2.COLOR_HLS2RGB))
			return rgb.convert(to)

class ImageHSV(ImageColor):
	def convert(self, to):
		to = to.lower()
		if to == 'hsv':
			return self
		else:
			rgb = ImageRGB(cv2.cvtColor(self.img, cv2.COLOR_HSV2RGB))
			return rgb.convert(to)

class ImageYCRCB(ImageColor):
	def convert(self, to):
		to = to.lower()
		if to == 'ycrcb' or to == 'ycc' or to == 'ycr_cb':
			return self
		else:
			rgb = ImageRGB(cv2.cvtColor(self.img, cv2.COLOR_YCR_CB2RGB))
			return rgb.convert(to)

def wait_key():
	while 1:
		k = cv2.waitKey(100) & 0xFF
		if k == 27:
			break
	cv2.destroyAllWindows()

if __name__=="__main__":
	img = cv2.imread("test/rojo.png")
	bgr = ImageBGR(img)
	bgr.convert('rgb').show()
	wait_key()

	bgr.convert('hls').show()
	wait_key()

	bgr.convert('hls').show()
	wait_key()

	bgr.convert('hsv').show()
	wait_key()

	bgr.convert('bgr').show()
	wait_key()

	bgr.convert('ycrcb').show()
	wait_key()

	bgr.convert('gray').show()
	wait_key()

