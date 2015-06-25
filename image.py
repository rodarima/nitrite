# -*- coding: utf-8 -*-

import numpy as np
import cv2

class Image(object):
#	models = ['Gray', 'RGB', 'BGR', 'HSL', 'HSV', 'YCRCB']

	def __init__(self, img):
		self.img = img

	def convert(self, to):
		to = to.upper()
		if to in map(str.upper, self.alias):
			return self
		else:
			rgb = ImageRGB(cv2.cvtColor(self.img, self.toRGB))
			return rgb.convert(to)

	def get_model(self):
		if len(self.alias) > 0: return self.alias[0]
		else: return None
			


class ImageGray(Image):
	channels = ['Gray']
	alias = ['Gray', 'GrayScale']
	toRGB = cv2.COLOR_GRAY2RGB
	fromRGB = cv2.COLOR_RGB2GRAY

	def show(self):
		cv2.imshow('img', self.img)

	def __getitem__(self, channel):
		if not isinstance(channel, int):
			channel = map(str.upper, self.channels).index(channel.upper())
		if channel != 0: raise ValueError("Channel unknown")
			
		return self.img

#	def __iter__(self):
#		return self.c.itervalues()

	def __setitem__(self, channel, value):
		if not isinstance(channel, int):
			channel = map(str.upper, self.channels).index(channel.upper())
		if channel != 0: raise ValueError("Channel unknown")
		self.img[:,:] = value

class ImageColor(Image):

	def show(self):
		bgr = self.convert('bgr')
		cv2.imshow('img', bgr.img)

	def __getitem__(self, channel):
		if not isinstance(channel, int):
			channel = map(str.upper, self.channels).index(channel.upper())
			
		return self.img[:,:,channel]

#	def __iter__(self):
#		return self.c.itervalues()

	def __setitem__(self, channel, value):
		if not isinstance(channel, int):
			channel = map(str.upper, self.channels).index(channel.upper())
		self.img[:,:,channel] = value


class ImageRGB(ImageColor):
	channels = ['R', 'G', 'B']
	alias = ['RGB']

	def convert(self, to):
		to = to.upper()
		if to in map(str.upper, self.alias):
			return self
		else:
			for img_class in self.models:
				if to in map(str.upper, img_class.alias):
					return img_class(cv2.cvtColor(self.img, img_class.fromRGB))

			raise ValueError('Unknown space color "' + to + '"')

class ImageBGR(ImageColor):
	channels = ['B', 'G', 'R']
	alias = ['BGR']
	toRGB = cv2.COLOR_BGR2RGB
	fromRGB = cv2.COLOR_RGB2BGR

class ImageHLS(ImageColor):
	channels = ['H', 'L', 'S']
	alias = ['HLS', 'HSL']
	toRGB = cv2.COLOR_HLS2RGB
	fromRGB = cv2.COLOR_RGB2HLS

class ImageHSV(ImageColor):
	channels = ['H', 'S', 'V']
	alias = ['HSV']
	toRGB = cv2.COLOR_HSV2RGB
	fromRGB = cv2.COLOR_RGB2HSV

class ImageYCRCB(ImageColor):
	channels = ['Y', 'Cr', 'Cb']
	alias = ['YCrCb', 'YCC', 'YCR_CB']
	toRGB = cv2.COLOR_YCR_CB2RGB
	fromRGB = cv2.COLOR_RGB2YCR_CB

Image.models = [ImageGray] + ImageColor.__subclasses__()
ImageColor.models = ImageColor.__subclasses__()

def wait_key():
	while 1:
		k = cv2.waitKey(100) & 0xFF
		if k == 27:
			break
	cv2.destroyAllWindows()

if __name__=="__main__":
	img = cv2.imread('test/Trafico/1277381674Image000016.jpg')#"test/rojo.png")
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

