# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore, uic
import sys

class ModTransform(QtGui.QGroupBox):
	name = 'Tranform'
	def __init__(self, w):
		super(ModTransform, self).__init__()
		self.module_layout = QtGui.QFormLayout()
		self.setTitle("Lolelali")
		self.setLayout(self.module_layout)

		self.combo_in = QtGui.QComboBox()
		self.combo_out = QtGui.QLineEdit()
		self.combo_out.editingFinished.connect(self.out_changed)

		self.combo_in.addItem('in 111111')
		self.combo_in.addItem('in 222222')

		self.module_layout.addRow("In", self.combo_in)
		self.module_layout.addRow("Out", self.combo_out)
		self.on_out_changed = None


	def process(self, img):
		pass

	def register_out(self, f):
		self.on_out_changed = f

	def out_changed(self):
		if self.on_out_changed:
			self.on_out_changed()

	def set_inputs(self, l):
		combo = self.combo_in
		i = combo.currentIndex()
		combo.clear()
		combo.addItems(l)
		if i < len(l):
			combo.setCurrentIndex(i)

	def get_output(self):
		return self.combo_out.text()

class ModInput:
	def __init__(self, w):
		self.w = w
		self.w.button_add_images.clicked.connect(self.add_images)

	def get_output(self):
		return "Input"

	def add_images(self):
		dialog = QtGui.QFileDialog()
		dialog.setFileMode(QtGui.QFileDialog.ExistingFiles)
		dialog.setNameFilter("Images (*.png *.jpg *.gif *.bmp)")
		dialog.setViewMode(QtGui.QFileDialog.Detail)

		if(dialog.exec_()):
			fileNames = dialog.selectedFiles()
			for f in fileNames:
				self.w.list_images.addItem(f)

		if(self.w.list_images.currentRow() == -1 and 
			self.w.list_images.count > 0):
			self.w.list_images.setCurrentRow(0)

	def get_image(self):
		if self.w.list_images.currentRow() != -1:
			i = self.w.list_images.currentRow()
			return str(self.w.list_images.item(i).text())

		return None

	def process(self, data):
		img_name = self.get_image()
		if(img_name == None): return None

		img = cv2.imread(img_name)
		cv2.cvtColor(img, cv2.COLOR_BGR2RGB, img)
		return img

class ModOutput:
	name = 'View image'
	def __init__(self, w):
		self.w = w

	def process(self, data):
		if data == None: return

		self.load_image(data)

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


class ModuleMorph(ModTransform):

	def __init__(self, window):
		super(ModuleMorph, self).__init__(window)


class ModManager:
	def __init__(self, w):
		self. w = w
		self.modlist = []

		self.all_mods = self.get_all_mods()
		self.all_mod_names = self.get_mod_names(self.all_mods)

		self.w.combo_mod.addItems(self.all_mod_names)

		self.w.button_add_mod.clicked.connect(self.add_mod)

	def add(self, mod):
		self.modlist.append(mod)

	def update_out(self):
		outs = []
		for m in self.modlist:
			outs.append(m.get_output())

		for m in self.modlist:
			m.set_inputs(outs)

	def get_all_mods(self):
		return [ModTransform, ModOutput]

	def get_mod_names(self, mods):
		mods_name = [c.name for c in mods]
		return mods_name

	def add_mod(self):
		if self.w.combo_mod.currentIndex() < 0: return

		i = self.w.combo_mod.currentIndex()
		mod_class = self.all_mods[i]
		mod = mod_class(self.w)
		mod.register_out(self.update_out)
		self.w.scroll_layout.addWidget(mod)
		self.add(mod)



class Main(QtGui.QMainWindow):
	def __init__(self, parent = None):
		super(Main, self).__init__(parent)

		uic.loadUi('qt/mod/mainwindow.ui', self)
		self.tm = ModManager(self)

		# Input image
		self.mod_input = ModInput(self)

	def add_widget(self):
		mod = ModTransform()
		mod.register_out(self.tm.update_out)
		self.scroll_layout.addWidget(mod)
		self.tm.add(mod)


#class Main(QtGui.QMainWindow):
#	def __init__(self, parent = None):
#		super(Main, self).__init__(parent)
#
#		# main button
#		self.addButton = QtGui.QPushButton('button to add other widgets')
#		self.addButton.clicked.connect(self.addWidget)
#
#		# scroll area widget contents - layout
#		self.scrollLayout = QtGui.QFormLayout()
#
#		# scroll area widget contents
#		self.scrollWidget = QtGui.QWidget()
#		self.scrollWidget.setLayout(self.scrollLayout)
#
#		# scroll area
#		self.scrollArea = QtGui.QScrollArea()
#		self.scrollArea.setWidgetResizable(True)
#		self.scrollArea.setWidget(self.scrollWidget)
#
#		# main layout
#		self.mainLayout = QtGui.QVBoxLayout()
#
#		self.inputlist = ModInput()
#
#		# add all main to the main vLayout
#		self.mainLayout.addWidget(self.addButton)
#		self.mainLayout.addWidget(self.scrollArea)
#		self.scrollLayout.addWidget(self.inputlist)
#
#		# central widget
#		self.centralWidget = QtGui.QWidget()
#		self.centralWidget.setLayout(self.mainLayout)
#
#		# set central widget
#		self.setCentralWidget(self.centralWidget)
#		self.tm = TransformManager()
#
#	def addWidget(self):
##		self.scrollLayout.addRow(Test())
#
#		mod = ModTransform()
#		mod.register_out(self.tm.update_out)
#		self.scrollLayout.addWidget(mod)
#		self.tm.add(mod)
#
#
#class Test(QtGui.QWidget):
#	def __init__(self, parent=None):
#		super(Test, self).__init__(parent)
#
#		self.pushButton = QtGui.QPushButton('I am in Test widget')
#
#		layout = QtGui.QHBoxLayout()
#		layout.addWidget(self.pushButton)
#		self.setLayout(layout)



app = QtGui.QApplication(sys.argv)
myWidget = Main()
myWidget.show()
app.exec_()

