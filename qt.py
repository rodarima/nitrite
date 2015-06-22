# -*- coding: utf-8 -*-

import numpy as np
import cv2
import os
import time

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import uic
from ConfigParser import SafeConfigParser as Conf

PREPROCESS_CONFIG = "config/preprocess.conf"

class Images:
	def __init__(self, window):
		self.win = window

	def open_images(self):
		dialog = QFileDialog(self.win)
		dialog.setFileMode(QFileDialog.ExistingFiles)
		dialog.setNameFilter("Images (*.png *.jpg *.gif *.bmp)")
		dialog.setViewMode(QFileDialog.Detail)

		if(dialog.exec_()):
			fileNames = dialog.selectedFiles()
			for f in fileNames:
				print(f)
				self.win.list_images.addItem(f)

		if(w.list_images.currentRow() == -1 and 
			w.list_images.count > 0):
			w.list_images.setCurrentRow(0)

	def get_image(self):
		if self.win.list_images.currentRow() != -1:
			i = self.win.list_images.currentRow()
			return str(self.win.list_images.item(i).text())

		return None

class TransformModule:
	def __init__(self, window):
		self.win = window

class ModuleMorph(TransformModule):

	def __init__(self, window):
		super(ModuleMorph, self).__init__(window)

	def 

class Status:
	def __init__(self, window):
		self.win = window

	def set(self, text):
		self.win.label_status.setText(text)

class Preprocess:
	def __init__(self):
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
#		if th < tH:
#			#mask = cv2.inRange(hsv_img, (th, ts, tv), (tH, tS, tV))
#			mask = cv2.adaptativeinRange(hsv_img, (th, ts, tv), (tH, tS, tV))
#			mask = cv2.adaptiveThreshold(h, tH, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,block_size=3)
#		else:
#			mask1 = cv2.inRange(hsv_img, (th, ts, tv), (180, tS, tV))
#			mask2 = cv2.inRange(hsv_img, (0, ts, tv), (tH, tS, tV))
#			mask = cv2.bitwise_or(mask1, mask2)
#		return mask

		if th < tH:
			mask = cv2.inRange(hsv_img, (th, ts, tv), (tH, tS, tV))
		else:
			mask1 = cv2.inRange(hsv_img, (th, ts, tv), (180, tS, tV))
			mask2 = cv2.inRange(hsv_img, (0, ts, tv), (tH, tS, tV))
			mask = cv2.bitwise_or(mask1, mask2)
		return mask

	def equalize_rgb(self, rgb):
		hls = cv2.cvtColor(rgb, cv2.COLOR_RGB2HLS)
#		clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
#		l = hls[:,:,2]
#		hls[:,:,2] = clahe.apply(l)

#		img_ycrcb = cv2.cvtColor(rgb, cv2.COLOR_RGB2HLS)
#		eq = self.equalize_channel(img_ycrcb, 1)
#		return cv2.cvtColor(hls, cv2.COLOR_HLS2RGB)
		return cv2.cvtColor(hls[:,:,2], cv2.COLOR_GRAY2RGB)

	def load_image(self, img_rgb):
		self.img_rgb = img_rgb

	def save_config(self):
		f = open(PREPROCESS_CONFIG, 'w')
		try:
			self.config.write(f)
		finally:
			f.close()

	def get_color(self, col):
		th = self.config.getint(col, 'hue_min')
		tH = self.config.getint(col, 'hue_max')
		ts = self.config.getint(col, 'sat_min')
		tS = self.config.getint(col, 'sat_max')
		tv = self.config.getint(col, 'val_min')
		tV = self.config.getint(col, 'val_max')
		v_min = [th, ts, tv]
		v_max = [tH, tS, tV]
		return [v_min, v_max]

	def set_color(self, col, v):
		th, ts, tv = v[0]
		tH, tS, tV = v[1]
		th = self.config.set(col, 'hue_min', str(th))
		tH = self.config.set(col, 'hue_max', str(tH))
		ts = self.config.set(col, 'sat_min', str(ts))
		tS = self.config.set(col, 'sat_max', str(tS))
		tv = self.config.set(col, 'val_min', str(tv))
		tV = self.config.set(col, 'val_max', str(tV))

	def list_colors(self):
		return self.config.sections()

	def process_color(self, v):
		eq_rgb = self.equalize_rgb(self.img_rgb)
#		img_hsv = cv2.cvtColor(eq_rgb, cv2.COLOR_RGB2HSV)
#		mask = self.threshold_hsv(img_hsv, v)
#		self.img_result = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
		self.img_result = eq_rgb

	def edit_color(self, col):
		v = get_color(col)
		create_trackbars(v, col)
		process_color(v, col)

	def get_img(self):
		return self.img_result

class Sign:
	def __init__(self, path):
		self.load_images(path)

	def load_images(self, path):
		imgs = os.listdir(self.path)
		self.imgs = [os.path.join(self.path,i) for i in imgs]

	def nothing(x): pass

#im = cv2.imread("test/color/1.jpg")
#p = Preprocess(im)
#edit_color('Blue')

class MainWindow(QMainWindow):
	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)

		uic.loadUi('qt/viewer/mainwindow.ui', self)
		self.connect_sliders()
		self.connect_spinners()
		self.preprocess = Preprocess()
		self.images = Images(self)
		self.status = Status(self)

		self.load_preprocess()
		colors = self.preprocess.list_colors()
		self.color_selector.currentIndexChanged.connect(self.on_color_selector_changed)
		for col in colors:
			self.color_selector.addItem(col)
		self.button_reload_color.clicked.connect(self.reload_color)
		self.button_save_color.clicked.connect(self.save_color)
		self.action_open_image.triggered.connect(self.images.open_images)
		self.list_images.itemSelectionChanged.connect(self.reload_preprocess)
		self.combo_output.currentIndexChanged.connect(self.on_output_changed)

		self.status.set("Waiting for images")

	def load_preprocess(self):
		#TODO
		img_name = self.images.get_image()
		if(img_name != None):
			img = cv2.imread(img_name)
			scale_factor = self.spin_resize.value()
			img = cv2.resize(img, (0,0), fx=scale_factor, fy=scale_factor)
			cv2.cvtColor(img, cv2.COLOR_BGR2RGB, img)
			self.result_img = img
			self.preprocess.load_image(img)
			self.status.set("Image loaded")

	def load_image_test(self):
		self.cvImage = cv2.imread(r'test/color/1.jpg')
		height, width, byteValue = self.cvImage.shape
		byteValue = byteValue * width

		cv2.cvtColor(self.cvImage, cv2.COLOR_BGR2RGB, self.cvImage)

		self.mQImage = QImage(self.cvImage, width, height, byteValue,
			QImage.Format_RGB888)

		g = self.graphics_view
		scene = QGraphicsScene()
		scene.addPixmap(QPixmap.fromImage(self.mQImage))
		scene.update()
		g.setScene(scene)

	def load_image(self, img_rgb):
		height, width, byteValue = img_rgb.shape
		byteValue = byteValue * width

		self.mQImage = QImage(img_rgb, width, height, byteValue,
			QImage.Format_RGB888)

		g = self.graphics_view
		scene = QGraphicsScene()
		scene.addPixmap(QPixmap.fromImage(self.mQImage))
		scene.update()
		g.setScene(scene)

	def connect_sliders(self):
		for s in self.hsv_filter.children():
			if type(s) == QSlider:
				s.valueChanged.connect(self.on_slider_changed)

	def connect_spinners(self):
		for s in self.hsv_filter.children():
			if type(s) == QSpinBox:
				s.valueChanged.connect(self.on_spin_changed)
		self.spin_resize.valueChanged.connect(self.on_spin_resize_changed)

	def on_output_changed(self):
		self.update_preprocess()

	def on_slider_changed(self):
		self.threshold_color = self.get_slider_color()
		self.set_spin_color()
		self.update_preprocess()

	def on_spin_changed(self):
		self.threshold_color = self.get_spin_color()
		self.set_slider_color()
		self.update_preprocess()

	def on_spin_resize_changed(self):
		self.reload_preprocess()

	def on_color_selector_changed(self):
		self.reload_color()

	def reload_preprocess(self):
		print("Reloading...")
		self.load_preprocess()
		self.update_preprocess()

	def update_preprocess(self):
		tic = time.time()
		i = self.combo_output.currentIndex()
		result = self.result_img
		if i > 0:
			self.preprocess.process_color(self.threshold_color)
			result = self.preprocess.get_img()
		toc = time.time()
		elap = (toc - tic) * 1000
		self.status.set("Preprocessing done in {:.3f} ms".format(elap))
		self.load_image(result)

	def save_color(self):
		self.preprocess.set_color(self.color_name, self.threshold_color)
		self.preprocess.save_config()

	def reload_color(self):
		slider = self.color_selector
		val = slider.currentText()
		self.color_load(str(val))

	def color_load(self, color):
		v = self.preprocess.get_color(color)
		self.threshold_color = v
		self.color_name = color
		self.set_slider_color()
		self.set_spin_color()

	def set_slider_color(self):
		v = self.threshold_color
		(th, ts, tv) = v[0]
		(tH, tS, tV) = v[1]
		self.th.setValue(th)
		self.tH.setValue(tH)
		self.ts.setValue(ts)
		self.tS.setValue(tS)
		self.tv.setValue(tv)
		self.tV.setValue(tV)

	def get_slider_color(self):
		h = self.th.value()
		H = self.tH.value()
		s = self.ts.value()
		S = self.tS.value()
		v = self.tv.value()
		V = self.tV.value()
		return [[h,s,v],[H,S,V]]

	def set_spin_color(self):
		v = self.threshold_color
		(th, ts, tv) = v[0]
		(tH, tS, tV) = v[1]
		self.spin_hue_min.setValue(th)
		self.spin_hue_max.setValue(tH)
		self.spin_sat_min.setValue(ts)
		self.spin_sat_max.setValue(tS)
		self.spin_val_min.setValue(tv)
		self.spin_val_max.setValue(tV)

	def get_spin_color(self):
		h = self.spin_hue_min.value()
		H = self.spin_hue_max.value()
		s = self.spin_sat_min.value()
		S = self.spin_sat_max.value()
		v = self.spin_val_min.value()
		V = self.spin_val_max.value()
		return [[h,s,v],[H,S,V]]

#	def paintEvent(self, QPaintEvent):
		#painter = QPainter()
		#painter.begin(self)
		#painter.drawImage(0, 0, self.mQImage)
		#painter.end()

#	def keyPressEvent(self, QKeyEvent):
#		super(MainWindow, self).keyPressEvent(QKeyEvent)
#		if 's' == QKeyEvent.text():
#			cv2.imwrite("cat2.png", self.cvImage)
#		elif 'q' == QKeyEvent.text():
#			app.exit(1)


if __name__=="__main__":
	import sys
	app = QApplication(sys.argv)
	w = MainWindow()
	w.show()
	app.exec_()

