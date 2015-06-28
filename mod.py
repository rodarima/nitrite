# -*- coding: utf-8 -*-

# This file is part of Nitrite.
#
# Nitrite is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# Nitrite is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Nitrite.  If not, see <http://www.gnu.org/licenses/>.

from PyQt4 import QtGui, QtCore, uic
from image import *
from plug import *

import cv2
import skimage.morphology
import skimage.transform
import skimage.draw
import sys
import json
import pprint
import traceback

START_INDEX = 0 #Para los nombres de los módulos

class Mod:
	def __init__(self, name, plug_manager):
		self.name = name
		self.pm = plug_manager

	def restore(self, config):
		raise NotImplemented()

	def clone(self):
		raise NotImplemented()

class ModInput:
	'Gestiona las entradas del módulo'
	def __init__(self):
		self.inputs = {}
		self.input_filter = {}
		self.input_combo = {}
		self.input_values = {}
		self.input_labels = []	# Importante para mantener el orden

	def add_input(self, label, class_filter=[], optional=False):
		if label in self.inputs.keys():
			raise Exception("Already exists")

		self.input_labels.append(label)
		self.inputs[label] = self.pm.new_input(self, self.name + '.' + label)
		self.input_filter[label] = class_filter
		self.input_combo[label] = self.new_input_combo(label)
	
	def remove_input(self, label):
		if label not in self.inputs.keys():
			raise KeyError('Input not found')

		# Borrar PlugIn
		plug_in = self.inputs.pop(label)
		self.pm.remove_input(plug_in)
		# Borrar el filtro
		self.input_filter.pop(label)
		# Borrar el combo
		self.remove_input_combo(label)
		# Borrar de la lista de etiquetas
		self.input_labels.remove(label)
		
	def remove_input_combo(self, label):
		'Borra el combo y la etiqueta'
		combo = self.input_combo[label]
		label = self.module_layout.labelForField(combo)
		if label: label.deleteLater()
		combo.deleteLater()
		self.input_combo.pop(label)
	
	def new_input_combo(self, label):
		'Crea un combo de entrada y lo añade al módulo'
		# Añadir el combo
		widget_in = QtGui.QComboBox()
		self.module_layout.addRow(label, widget_in)
		self.input_combo[label] = widget_in
		# Comenzar con una lista vacía
		self.input_values[label] = []
		return widget_in

	def enable_inputs(self):
		for combo in self.input_combo.values():
			combo.currentIndexChanged.connect(self.updated_input_combo)

	def disable_inputs(self):
		for combo in self.input_combo.values():
			combo.currentIndexChanged.disconnect(self.updated_input_combo)

	def updated_input_combo(self):
		'Conecta la entrada segun el valor del combo'
		combo = self.w.sender()
		output_name = str(combo.currentText())

		i = self.input_combo.values().index(combo)
		if i < 0: raise RuntimeError()
		label = self.input_combo.keys()[i]
		input_plug = self.inputs[label]
		#print('ModInput.updated_input_combo: connecting {} with {}'.format(input_plug, output_name))

		# Si se ha seleccionado la entrada vacía
		if output_name == '':
			# Desconectar la entrada
			input_plug.disconnect()
		else:
			# Conectar con la entrada correspondiente
			self.pm.connect_input(input_plug, output_name)

		self.update()

	def get_input(self, label):
		plug_in = self.inputs[label]
		if plug_in.connected():
			return plug_in.data

		return None

	def update_io(self):
		'Actualiza la lista de estradas disponibles'
		#print('ModInput {}: update_io()'.format(self.name))
		self.disable_inputs()
		for label in self.inputs.keys():
			self.update_input_combo(label)
		self.enable_inputs()
		#TODO: Gestionar las señales, de forma que no se activen hasta
		# que sea necesario, y se desactiven temporalmente cuando se
		# modifican los valores del combo.

	def update_input_combo(self, label):
		#print('ModInput {}: update_input_combo({})'.format(self.name, label))
		plug_in = self.inputs[label]
		combo = self.input_combo[label]
		input_filter = self.input_filter[label]
		available_outputs = sorted(self.pm.get_outputs(self, input_filter))
		available_outputs.insert(0, '') # Permitir la desconexión
		self.input_values[label] = available_outputs
		#print("Available outputs: {}".format(available_outputs))
		i = self.get_input_index(label)
		self.update_input_combo_values(combo, self.input_values[label], i)

	def get_input_index(self, label):
		plug_in = self.inputs[label]
		i = -1
		if plug_in.connected():
			name = plug_in.plugs[0].name
			i = self.input_values[label].index(name)

		return i
		
	def update_input_combo_values(self, combo, values, index=None):
		"Actualiza en el combo las nuevas entradas"
		if index == None: index = combo.currentIndex()
		combo.clear()
		for item in values:
			combo.addItem(item)
		combo.setCurrentIndex(index)

	def show(self):
		print("ModInput show:")
		print(self.inputs)
		print(self.input_combo)

	def clone(self):
		# Clona la lista de los combos así como sus selecciones
		input_list = []
		for label in self.input_labels:
			input_config = {}
			input_config['values'] = self.input_values[label]
			input_config['index'] = self.input_combo[label].currentIndex()
			input_config['name'] = self.inputs[label].name
			input_config['label'] = label
			input_config['filter'] = [c.__name__ for c in self.input_filter[label]]
			input_list.append(input_config)
		return input_list

	def restore(self, config):
		# Restaura la parte gráfica de las entradas. No debe
		# alterar las conexiones reales del módulo
		if self.enabled: raise RuntimeError()

		for d in config:
			label = d['label']
			combo = self.new_input_combo(label)
			self.update_input_combo_values(combo, d['values'], index=d['index'])
			self.inputs[label] = self.pm.get_input(d['name'])
			self.input_values[label] = d['values']
			self.input_filter[label] = [globals()[c] for c in d['filter']]
			self.input_labels.append(label)

	def destroy(self):
		'Borra las entradas'
		for plug_in in self.inputs.values():
			self.pm.remove_input(plug_in)


class ModOutput:
	'Gestiona las salidas del módulo'
	def __init__(self):
		self.outputs = {} #Indexados por el nombre de la etiqueta
		self.output_line = {}
		self.output_labels = [] # Mantener el orden

	def add_output(self, label, class_type=None):
		if label in self.outputs:
			raise Exception("Already exists")

		self.output_labels.append(label)
		self.outputs[label] = self.pm.new_output(self, self.name + '.' + label, class_type)
		self.output_line[label] = self.new_output_line(label)

	def new_output_line(self, label):
		'Crea un LineEdit de salida y lo añade al módulo'
		# Añadir el combo
		widget_out = QtGui.QLineEdit()
		output_name = self.outputs[label].name
		widget_out.setText(output_name)
		self.module_layout.addRow(label, widget_out)
		self.output_line[label] = widget_out
		return widget_out

	def updated_output_line(self):
		# Obtener el nuevo nombre y comprobar que no este duplicado
		output_line = self.w.sender()
		self.disable_outputs()
		new_name = str(output_line.text())

		i = self.output_line.values().index(output_line)
		if i < 0: raise RuntimeError()
		label = self.output_line.keys()[i]
		output = self.outputs[label]
		output = self.pm.update_output(output, new_name)
		# El nombre ha podido cambiar si ya existía
		if new_name != output.name:
			output_line.setText(output.name)
		self.enable_outputs()

		#TODO

	def set_output(self, label, data):
		self.outputs[label].data = data
		self.outputs[label].update()

	def enable_outputs(self):
		for line in self.output_line.values():
			line.editingFinished.connect(self.updated_output_line)

	def disable_outputs(self):
		for line in self.output_line.values():
			line.editingFinished.disconnect(self.updated_output_line)


	def show(self):
		print("ModOutput show:")
		print(self.outputs)
		print(self.output_line)

	def clone(self):
		config_list = []
		for label in self.output_labels:
			d = {}
			d['name'] = self.outputs[label].name
			d['label'] = label
			config_list.append(d)
		return config_list

	def restore(self, config):
		# Restaura la parte gráfica de las salidas. No debe
		# alterar las conexiones reales del módulo
		if self.enabled: raise RuntimeError()

		for d in config:
			label = d['label']
			self.outputs[label] = self.pm.get_output(d['name'])
			line = self.new_output_line(label)
			line.setText(self.outputs[label].name)
			self.output_line[label] = line
			self.output_labels.append(label)

	def destroy(self):
		'Borra las salidas'
		for plug_out in self.outputs.values():
			self.pm.remove_output(plug_out)

class ModDouble:

	def __init__(self):
		self.gui_double = {}

	def add_double(self, label, min=0.0, max=None, step=0.01, value=0):
		if label in self.gui_double: raise RuntimeError()
		self.gui_double[label] = QtGui.QDoubleSpinBox()
		double = self.gui_double[label]
		double.setMinimum(min)
		if max: double.setMaximum(max)
		double.setSingleStep(step)
		double.setValue(value)

		self.module_layout.addRow(label, double)
		double.valueChanged.connect(self.update)

	def get_double(self, label):
		return self.gui_double[label].value()

	def clone(self):
		'Clona los valores de los QDoubleSpinBox'
		d = {}
		for label in self.gui_double.keys():
			d[label] = self.gui_double[label].value()
		return d

	def restore(self, config):
		'Restaura los valores de los QDoubleSpinBox'
		if self.enabled: raise RuntimeError()

		for label in self.gui_double.keys():
			self.gui_double[label].setValue(config[label])

class ModInt:

	def __init__(self):
		self.gui_int = {}

	def add_int(self, label, min=0, max=1000, step=1, value=0):
		if label in self.gui_int: raise RuntimeError()
		self.gui_int[label] = QtGui.QSpinBox()
		spin = self.gui_int[label]
		spin.setMinimum(min)
		spin.setMaximum(max)
		spin.setSingleStep(step)
		spin.setValue(value)

		self.module_layout.addRow(label, spin)
		spin.valueChanged.connect(self.update)

	def get_int(self, label):
		return self.gui_int[label].value()

	def clone(self):
		'Clona los valores de los QSpinBox'
		d = {}
		for label in self.gui_int.keys():
			d[label] = self.gui_int[label].value()
		return d

	def restore(self, config):
		'Restaura los valores de los QSpinBox'
		if self.enabled: raise RuntimeError()

		for label in self.gui_int.keys():
			self.gui_int[label].setValue(config[label])

class ModCombo:

	def __init__(self):
		self.gui_combo = {}

	def add_combo(self, label, values):
		if label in self.gui_combo: raise RuntimeError()
		self.gui_combo[label] = QtGui.QComboBox()
		combo = self.gui_combo[label]
		combo.addItems(values)

		self.module_layout.addRow(label, combo)
		combo.currentIndexChanged.connect(self.update)

	def get_combo(self, label):
		return str(self.gui_combo[label].currentText())

	def clone(self):
		'Clona los valores de los QComboBox'
		d = {}
		for label in self.gui_combo.keys():
			d[label] = self.gui_combo[label].currentIndex()
		return d

	def restore(self, config):
		'Restaura los valores de los QComboBox'
		if self.enabled: raise RuntimeError()

		for label in self.gui_combo.keys():
			self.gui_combo[label].setCurrentIndex(config[label])

class ModIO(Mod, ModInput, ModOutput):
	def __init__(self, name, plug_manager, window, config=None):
		Mod.__init__(self, name, plug_manager)
		self.gui_add_group(window)
		self.enabled = False
		ModInput.__init__(self)
		ModOutput.__init__(self)

		if config == None:
			self.init_IO()
			self.init_GUI()
			self.enable()

	def gui_add_group(self, window):
		'Añade el widget de grupo donde irán los componentes'
		self.w = window
		self.module = QtGui.QGroupBox()
		self.module.setEnabled(False)
		self.module.setTitle(self.name)
#		self.module.setFlat(True)
#		self.module.setCheckable(True)
		self.module_layout = QtGui.QFormLayout()
		self.module.setLayout(self.module_layout)
#		self.w.scroll_layout.addWidget(self.module)
	
	def enable(self):
		'Activa el módulo gráficamente y las señales'
		self.enabled = True
		self.enable_inputs()
		self.enable_outputs()
		self.module.setEnabled(True)
		self.update_io()

	def show(self):
		self.w.scroll_layout.addWidget(self.module)

	def hide(self):
		self.w.scroll_layout.removeWidget(self.module)
		self.module.setParent(None)

	def clone(self):
		d = {}
		d['ModInput'] = ModInput.clone(self)
		d['ModOutput'] = ModOutput.clone(self)
		return d

	def restore(self, d):
		ModInput.restore(self, d['ModInput'])
		ModOutput.restore(self, d['ModOutput'])

	def destroy(self):
		'Borra el módulo completamente'
		ModInput.destroy(self)
		ModOutput.destroy(self)
		self.w.scroll_layout.removeWidget(self.module)
		self.module.setParent(None)
		self.module.deleteLater()
		
class ModBase(ModIO, ModDouble, ModInt, ModCombo):

	def __init__(self, name, plug_manager, window, config=None):
		ModDouble.__init__(self)
		ModInt.__init__(self)
		ModCombo.__init__(self)
		ModIO.__init__(self, name, plug_manager, window, config)

	def clone(self):
		d = {}
		d['ModIO'] = ModIO.clone(self)
		d['ModDouble'] = ModDouble.clone(self)
		d['ModInt'] = ModInt.clone(self)
		d['ModCombo'] = ModCombo.clone(self)
		return d

	def restore(self, d):
		if self.enabled: raise RuntimeError()

		ModIO.restore(self, d['ModIO'])

		self.init_GUI()
		ModDouble.restore(self, d['ModDouble'])
		ModInt.restore(self, d['ModInt'])
		ModCombo.restore(self, d['ModCombo'])

class ModTestInput(ModIO):
	mod_name = 'Test'

	def init_IO(self):
		self.add_input("Gray", [ImageColor])
		self.add_input("Color")

		self.add_output("Img", ImageColor)
		self.add_output("Mask")
	
	def init_GUI(self):
		pass
	
	def update(self):
		pass


class ModImage(ModIO):
	mod_name = "Image"

	def init_IO(self):
		self.add_output("Img", ImageColor)

	def init_GUI(self):
		self.image_files = []
		self.gui_add_list()

	def gui_add_list(self):
		'Añade una lista y un boton para seleccionar imágenes'
		self.image_list = QtGui.QListWidget()
		self.button_add = QtGui.QPushButton("Add")

		self.module_layout.addWidget(self.image_list)
		self.module_layout.addWidget(self.button_add)

	def add_images(self):
		dialog = QtGui.QFileDialog()
		dialog.setFileMode(QtGui.QFileDialog.ExistingFiles)
		dialog.setNameFilter("Images (*.png *.jpg *.gif *.bmp)")
		dialog.setViewMode(QtGui.QFileDialog.Detail)

		if(dialog.exec_()):
			fileNames = dialog.selectedFiles()
			self.image_files += [str(f) for f in fileNames]
		self.update_images()

	def update_images(self):
		imglist = self.image_list
		i = imglist.currentRow()

		imglist.clear()
		imglist.addItems(self.image_files)

		if(i >= 0 and i < len(self.image_files)):
			imglist.setCurrentRow(i)
		elif len(self.image_files) > 0:
			imglist.setCurrentRow(0)

	def get_image(self):
		i = self.image_list.currentRow()
		#print("Current row {}".format(i))
		if i != -1:
			return str(self.image_list.item(i).text())

		return None

	def enable(self):
		ModIO.enable(self)
		self.image_list.itemSelectionChanged.connect(self.update)
		self.button_add.clicked.connect(self.add_images)

	def update(self):
		img_name = self.get_image()
		if img_name == None:
			return


		bgr = cv2.imread(img_name)
#		print("ModImage: update() name = {}".format(img_name))
		img = ImageBGR(bgr)
#		print("ModImage: set_output({})".format(img))
		self.set_output("Img", img)

	def restore(self, d):
		ModIO.restore(self, d['ModIO'])
		self.init_GUI()
		self.image_files = d['image_files']
		self.update_images()
		i = d['image_index']
		self.image_list.setCurrentRow(i)

	def clone(self):
		d = {}
		d['ModIO'] = ModIO.clone(self)
		d['image_files'] = self.image_files
		d['image_index'] = self.image_list.currentRow()
		return d

class ModViewer(ModIO):
	mod_name = 'Viewer'

	def init_IO(self):
		self.add_input("Img", [Image])

	def init_GUI(self):
		pass

	def update(self):
		'Reprocesa los datos a partir de las entradas'
		img = self.get_input("Img")
#		print("ModViewer update() img={}".format(img))
		if img == None:
			return

		self.load_image(img)

	def load_image(self, img):
		rgb = img.convert('rgb')
		img_rgb = rgb.img
		if type(img_rgb) != np.ndarray: return
		height, width, byteValue = img_rgb.shape
		byteValue = byteValue * width

		self.mQImage = QtGui.QImage(img_rgb, width, height, byteValue,
			QtGui.QImage.Format_RGB888)

		g = self.w.graphics_view
		scene = QtGui.QGraphicsScene()
		scene.addPixmap(QtGui.QPixmap.fromImage(self.mQImage))
		scene.update()
		g.setScene(scene)

class ModScale(ModBase):
	mod_name = 'Scale'

	def init_IO(self):
		self.add_input("In", [Image])
		self.add_output("Out", ImageRGB)

	def init_GUI(self):
		self.add_double("Factor", min=0.001, max=1000, step=0.05, value=0.45)

	def update(self):
		data = self.get_input("In")
		if data == None: return

		rgb = data.convert('rgb').img

		s = self.get_double('Factor')
		s = max(min(s, 1000), 0.001)
		rgb = cv2.resize(rgb, (0,0), fx=s, fy=s)
		self.set_output("Out", ImageRGB(rgb))

class ModRange(ModBase):
	mod_name = 'Range'

	def init_IO(self):
		self.add_input("In", [ImageColor])
		self.add_output("Out", ImageGray)

	def init_GUI(self):
		self.ch_min = ['Ch0 min', 'Ch1 min', 'Ch2 min']
		self.ch_max = ['Ch0 max', 'Ch1 max', 'Ch2 max']
		self.models = [c.alias[0] for c in ImageColor.models]
		self.add_combo('Model', self.models)
		for label in self.ch_min:
			self.add_int(label, min=0, max=255, value=0)
		for label in self.ch_max:
			self.add_int(label, min=0, max=255, value=100)

	def update(self):
		data = self.get_input("In")
		if data == None: return

		model = self.get_combo('Model')
		data = data.convert(model)

		min_val = [self.get_int(label) for label in self.ch_min]
		max_val = [self.get_int(label) for label in self.ch_max]

		min0 = list(min_val)
		min1 = list(min_val)

		max0 = list(max_val)
		max1 = list(max_val)
		flip = False
		for i in range(len(min_val)):
			if min_val[i] > max_val[i]:
				max0[i] = 255
				min1[i] = 0
				flip = True

		gray = cv2.inRange(data.img, np.array(min0), np.array(max0))
		if flip:
			gray1 = cv2.inRange(data.img, np.array(min1), np.array(max1))
			gray = cv2.bitwise_or(gray, gray1)

		self.set_output('Out', ImageGray(gray))

class ModMorph(ModBase):
	mod_name = 'Morphology'

	def init_IO(self):
		self.add_input("In", [ImageGray])
		self.add_output("Out", ImageGray)

	def init_GUI(self):
		self.operations = [
			('Close',		cv2.MORPH_CLOSE),
			('Dilate',		cv2.MORPH_DILATE),
			('Erode',		cv2.MORPH_ERODE),
			('Open',		cv2.MORPH_OPEN),
			('Black Hat',	cv2.MORPH_BLACKHAT),
			('Top Hat',		cv2.MORPH_TOPHAT),
			('Gradient',	cv2.MORPH_GRADIENT)
		]
		self.operations_name = [op[0] for op in self.operations]
		self.kernel_shapes = [
			('Rect',		cv2.MORPH_RECT),
			('Ellipse',		cv2.MORPH_ELLIPSE),
			('Cross',		cv2.MORPH_CROSS)
		]
		self.kernel_shapes_name = [shape[0] for shape in self.kernel_shapes]
		self.add_combo('Operation', self.operations_name)
		self.add_combo('Shape', self.kernel_shapes_name)
		self.add_int('Size', min=1, max=200, step=1, value=5)

	def update(self):
		data = self.get_input('In')
		if data == None: return

		size = self.get_int('Size')
		operation_name = self.get_combo('Operation')
		operation = self.operations[self.operations_name.index(operation_name)][1]
		shape_name = self.get_combo('Shape')
		shape = self.kernel_shapes[self.kernel_shapes_name.index(shape_name)][1]

		img = data.img
		kernel = cv2.getStructuringElement(shape, (size, size))
		gray = cv2.morphologyEx(img, operation, kernel)

		data = ImageGray(gray)

		self.set_output('Out', data)

class ModBitwise(ModBase):
	mod_name = 'Bitwise'

	def init_IO(self):
		self.add_input('In0', [ImageGray])
		self.add_input('In1', [ImageGray])
		self.add_output('Out', ImageGray)

	def init_GUI(self):
		self.operations = [
			('AND',	cv2.bitwise_and,	2),
			('OR',	cv2.bitwise_or,		2),
			('XOR',	cv2.bitwise_xor,	2),
			('NOT',	cv2.bitwise_not,	1)
		]
		self.operations_name = [op[0] for op in self.operations]


		self.add_combo('Logic', self.operations_name)

	def update(self):
		data1 = self.get_input('In0')
		data2 = self.get_input('In1')
		if data1 == None: return

		operation_name = self.get_combo('Logic')
		i = self.operations_name.index(operation_name)
		operation_tuple = self.operations[i]
		operation_function = operation_tuple[1]

		img1 = data1.img

		if operation_tuple[2] == 2:
			if data2 == None: return
			img2 = data2.img
			if img1.shape != img2.shape: return
			dst = operation_function(src1 = img1, src2 = img2)
		elif operation_tuple[2] == 1:
			dst = operation_function(src = img1)

		data = ImageGray(dst)

		self.set_output('Out', data)

class ModHoughCircle(ModBase):
	mod_name = 'HoughCircle'

	def init_IO(self):
		self.add_input('Img', [Image])
		self.add_output('Img', ImageRGB)
		self.add_output('Array')

	def init_GUI(self):
		self.add_int("Inv. Ratio", min=1, value=5)
		self.add_int("Min. Dist.", min=1, value=10)
		self.add_int("Radius min")
		self.add_int("Radius max")
		self.add_int("Canny thr.", min=1)
		self.add_int("Acc. thr.", min=1, value=5)
	
	def update(self):
		data = self.get_input("Img")
		if data == None: return

		rgb = data.copy().convert('RGB')
		gray = data.copy().convert('gray')
		circles = cv2.HoughCircles(
			gray.img,
			method = cv2.cv.CV_HOUGH_GRADIENT,
			dp = self.get_int("Inv. Ratio"),
			minDist = self.get_int("Min. Dist."),
			param1 = self.get_int("Canny thr."),
			param2 = self.get_int("Acc. thr."),
			minRadius = self.get_int("Radius min"),
			maxRadius = self.get_int("Radius max")
		)

		img = rgb.img
		if type(circles) == np.ndarray:
			circles = np.uint16(np.around(circles))
			for i in circles[0,:]:
				# draw the outer circle
				cv2.circle(img,(i[0],i[1]),i[2],(255,255,0),2)
				# draw the center of the circle
				cv2.circle(img,(i[0],i[1]),1,(255,255,0),2)

		self.set_output("Array", circles)
		self.set_output("Img", rgb)

class ModCanny(ModBase):
	mod_name = 'Canny'

	def init_IO(self):
		self.add_input('Img', [Image])
		self.add_output('Edges', ImageGray)

	def init_GUI(self):
		self.add_int("Th1", min = 1)
		self.add_int("Th2", min = 1)
		self.add_int("Size/2", min = 1, max=3)
		self.add_int("L2 grad.", min=0, max=1)
	
	def update(self):
		data = self.get_input("Img")
		if data == None: return

		gray = data.convert('gray')
		zero = ImageGray(np.zeros(gray.img.shape, np.uint8))
		if self.get_int("L2 grad.") == 0: l2 = False
		else: l2 = True

		circles = cv2.Canny(
			image = gray.img,
			edges = zero.img,
			threshold1 = self.get_int("Th1"),
			threshold2 = self.get_int("Th2"),
			apertureSize = self.get_int("Size/2")*2+1,
			L2gradient = l2
		)

		self.set_output("Edges", zero)

class ModBlur(ModBase):
	mod_name = 'Blur'

	def init_IO(self):
		self.add_input('Img', [Image])
		self.add_output('Img', Image)

	def init_GUI(self):
		self.add_int("Size", min = 1)
	
	def update(self):
		data = self.get_input("Img")
		if data == None: return

		data = data.copy()
		size = self.get_int("Size")

		data.img = cv2.blur(
			src = data.img,
			ksize = (size, size)
		)

		self.set_output("Img", data)

class ModSkeleton(ModBase):
	mod_name = 'Skeleton'

	def init_IO(self):
		self.add_input('Img', [ImageGray])
		self.add_output('Img', ImageGray)

	def init_GUI(self): pass
	
	def update(self):
		data = self.get_input("Img")
		if data == None: return

		data = data.copy()
		data.img[data.img > 0] = 1

		data.img = skimage.morphology.skeletonize(
			image = data.img
		)
		data.img = data.img.astype(np.uint8)
		data.img[data.img > 0] = 255

		self.set_output("Img", data)

class ModHoughEllipse(ModBase):
	mod_name = 'HoughEllipse'

	def init_IO(self):
		self.add_input('Img', [ImageGray])
		self.add_output('Draw', ImageRGB)

	def init_GUI(self):
		self.add_int('Threshold', min=0, max=10000, value=250)
		self.add_double('Accuracy', min=0, step=0.5, max=1000, value=20)
		self.add_int('Size min', value=100)
		self.add_int('Size max', value=120)
	
	def update(self):
		data = self.get_input("Img")
		if data == None: return


		result = skimage.transform.hough_ellipse(
			data.img,
			threshold = self.get_int('Threshold'),
			accuracy = self.get_double('Accuracy'),
			min_size = self.get_int('Size min'),
			max_size = self.get_int('Size max')
		)

		data = data.copy().convert('rgb')

		# Draw each ellipse
		for ellipse in result:
			acc, yc, xc, a, b, orientation = ellipse
			cy, cx = skimage.draw.ellipse_perimeter(yc, xc, a, b, orientation)
			data.img[cy, cx] = (255,255,0)


		self.set_output('Draw', data)

class ModFindContours(ModBase):
	mod_name = 'FindContours'

	def init_IO(self):
		self.add_input('Img', [ImageGray])
		self.add_output('Draw', ImageRGB)
		self.add_output('Array')

	def init_GUI(self):
		self.methods = [
			('None',	cv2.cv.CV_CHAIN_APPROX_NONE),
			('Simple',	cv2.cv.CV_CHAIN_APPROX_SIMPLE),
			('L1',		cv2.cv.CV_CHAIN_APPROX_TC89_L1),
			('KCOS',	cv2.cv.CV_CHAIN_APPROX_TC89_KCOS)
		]
		self.method_names = [method[0] for method in self.methods]
		self.add_combo('Method', self.method_names)
	
	def update(self):
		data = self.get_input("Img")
		if data == None: return

		method_name = self.get_combo('Method')
		method_index = self.method_names.index(method_name)
		method = self.methods[method_index][1]

		data = data.copy()
		contours, hierarchy = cv2.findContours(
			image = data.img,
			mode = cv2.cv.CV_RETR_LIST,
			method = method
		)

		data = data.convert('rgb')
		cv2.drawContours(data.img, contours, -1, (255,0,0), 1)

		self.set_output('Draw', data)
		self.set_output('Array', contours)

class ModApproxPoly(ModBase):
	mod_name = 'ApproxPoly'


	def init_IO(self):
		self.add_input('Array', [])
		self.add_input('Draw', [Image])
		self.add_output('Array')
		self.add_output('Draw', ImageRGB)

	def init_GUI(self):
		self.add_double('Epsilon')
		self.add_int('Closed', min=0, max=1, value=1)
	
	def update(self):
		data = self.get_input("Array")
		draw = self.get_input("Draw")
		if data == None or draw == None:
			return

		#print(data)
		#print(type(data))

		closed = True
		if self.get_int('Closed') > 0: closed = True
		approx_contours = []
		for contour in data:
			approx_curve = cv2.approxPolyDP(
				curve = contour,
				epsilon = self.get_double('Epsilon'),
				closed = closed
			)

			#print(approx_curve)
			#print(type(approx_curve))
			approx_contours.append(approx_curve)

		draw = draw.copy().convert('rgb')
		cv2.drawContours(draw.img, approx_contours, -1, (0,255,0), 2)

		self.set_output('Draw', draw)
		self.set_output('Array', approx_contours)

class ModGeometry(ModBase):
	mod_name = 'Geometry'


	def init_IO(self):
		self.add_input('Array', [])
		self.add_input('Draw', [Image])
		self.add_output('Array')
		self.add_output('Draw', ImageRGB)

	def init_GUI(self):
		self.add_int('Vertex min', min=1, value=3)
		self.add_int('Vertex max', min=1, value=3)
		self.add_double('Area min', min=0, value=10)
		self.add_double('Area max', min=0, value=100)
		self.add_int('Perimeter min', min=1, max=100000)
		self.add_int('Perimeter max', min=1, max=100000)
	
	def update(self):
		data = self.get_input("Array")
		draw = self.get_input("Draw")
		if data == None or draw == None:
			return


		vmin = self.get_int('Vertex min')
		vmax = self.get_int('Vertex max')
		pmin = self.get_int('Perimeter min')
		pmax = self.get_int('Perimeter max')
		amin = self.get_int('Area min')
		amax = self.get_int('Area max')

		new_list = []
		for poly in data:
			if len(poly) > vmax or len(poly) < vmin: continue
			perimeter = cv2.arcLength(poly, True)
			if perimeter > pmax or perimeter < pmin: continue
			area = cv2.contourArea(poly)
			if area > amax or area < amin: continue
			#cv2.minEnclosingCircle(points) -> center, radius

			new_list.append(poly)

		draw = draw.copy().convert('rgb')
		cv2.drawContours(draw.img, new_list, -1, (0,255,0), 2)

		self.set_output('Draw', draw)
		self.set_output('Array', new_list)


class ModList:
	'Se encarga de añadir o quitar módulos, así como de mostrarlos'

	def __init__(self):
		self.current_mod = ''

		# Añadir lista de modulos
		self.all_mods = self.get_all_mods()
		self.all_mod_names = self.get_mod_names(self.all_mods)
		self.w.combo_mod.addItems(self.all_mod_names)

		# Boton de añadir modulos
		self.w.button_add_mod.clicked.connect(self.gui_add_mod)
		# Boton de borrar modulos
		self.w.button_del_mod.clicked.connect(self.gui_del_mod)
		self.enable()

	def gui_add_mod(self):
		if self.w.combo_mod.currentIndex() < 0:
			return

		i = self.w.combo_mod.currentIndex()
		mod_class = self.all_mods[i]
		mod = self.add_mod(mod_class)
		self.gui_list_add(mod.name)

	def gui_del_mod(self):
		widget_list = self.w.list_mods
		i = widget_list.currentRow()
		if i < 0:
			return

		name = str(widget_list.item(i).text())
		mod = self.mods[name]
		widget_list.takeItem(i)
		self.remove_mod(mod)

	def gui_list_add(self, name):
		widget_list = self.w.list_mods
		widget_list.addItem(name)

	def gui_clear_list(self):
		self.w.list_mods.clear()

	def enable(self):
		self.w.list_mods.itemSelectionChanged.connect(self.select_mod)

	def hide_mod(self):
		if self.current_mod == '': return
		self.mods[self.current_mod].hide()

	def select_mod(self):
		self.hide_mod()
		self.current_mod = ''
		item = self.w.list_mods.currentItem()
		if item == None:
			return
		name = str(item.text())
		self.current_mod = name

		self.mods[name].show()

class ModManager(ModList):
	'Gestiona la lista interna de módulos'

	def __init__(self, window):
		self.w = window
		self.mods = {}
		self.mod_names = []

		# ModList para la lista de módulos
		ModList.__init__(self)

		# Actualizar las salidas
		#self.update_io()

	def set_plug_manager(self, pm):
		self.pm = pm

	def update_io(self):
		'Actualizar las conexiones disponibles de todos los módulos'

		for mod in self.mods.values():
			mod.update_io()


	def get_all_mods(self):
		return MODS

	def get_mod_names(self, mods):
		mods_name = [c.mod_name for c in mods]
		return mods_name

	def get_mod(self, name):
		return self.mods[name]

	def new_name(self, mod_name):
		"Crea un nuevo nombre para un módulo"
		i = START_INDEX
		new_name = "{}{}".format(mod_name, i)
		while new_name in self.mods.keys():
			i+=1
			new_name = "{}{}".format(mod_name, i)
		return new_name

	def add_mod(self, mod_class):
		'Crea un módulo de la clase especificada'
		name = self.new_name(mod_class.mod_name)
		mod = mod_class(name, self.pm, self.w)
		self.mods[name] = mod
		self.mod_names.append(name)
		return mod

	def destroy_all(self):
		'Borra todos los módulos y conexiones'
		self.gui_clear_list()
		for mod in self.mods.values():
			self.remove_mod(mod)

	def remove_mod(self, mod):
		#print("Del " + str(mod.name))
		self.mods.pop(mod.name)
		self.mod_names.remove(mod.name)
		mod.destroy()

	def clone(self):
		config = {}
		modlist_conf = []
		for name in self.mod_names:
			mod = self.mods[name]
			d = {}
			d['Mod'] = mod.clone()
			d['name'] = mod.name
			d['class'] = mod.__class__.__name__
			modlist_conf.append(d)

		config['ModManager'] = modlist_conf
		config['PlugManager'] = self.pm.clone()

		return config

	def restore(self, config):
		self.destroy_all()

		modlist_conf = config['ModManager']

		# Crear los módulos sin iniciar
		for mod_conf in modlist_conf:
			name = mod_conf['name']
			mod_clone = mod_conf['Mod']
			mod_class = globals()[mod_conf['class']]
			mod = mod_class(name, self.pm, self.w, config=mod_clone)
			self.gui_list_add(name)
			
			self.mod_names.append(name)
			self.mods[name] = mod

		# Crea las conexiones y las conecta
		self.pm.restore(config['PlugManager'])

		# Restaurar configuración de cada módulo
		for mod_conf in modlist_conf:
			name = mod_conf['name']
			mod = self.mods[name]
			mod.restore(mod_conf['Mod'])

		# Activar los módulos
		for mod_conf in modlist_conf:
			name = mod_conf['name']
			mod = self.mods[name]
			mod.enable()
			
		# Actualizar las entradas
		for name in self.mods:
			mod = self.mods[name]
			if isinstance(mod, ModImage):
				mod.update()
			

class Config:
	def __init__(self, w, mm):
		self.w = w
		self.mm = mm
		w.action_open_config.activated.connect(self.open_config)
#		w.action_save_config.connect(self.save_config)
		w.action_save_as.activated.connect(self.save_config_as)

		self.config_file = None
		w.action_save_config.setEnabled(False)

	def open_config(self):
		dialog = QtGui.QFileDialog()
		dialog.setFileMode(QtGui.QFileDialog.ExistingFile)
		dialog.setNameFilter("Json config (*.json)")
		dialog.setViewMode(QtGui.QFileDialog.Detail)

		if not dialog.exec_(): return

		self.config_file = str(dialog.selectedFiles()[0])

		with open(self.config_file) as fd:
			config = json.load(fd)

		#print("Config read:")
		#print(json.dumps(config, sort_keys=True, indent=4))
		self.mm.restore(config)

	def save_config_as(self):
		dialog = QtGui.QFileDialog()
		dialog.setFileMode(QtGui.QFileDialog.AnyFile)
		dialog.setNameFilter("Json config (*.json)")
		dialog.setViewMode(QtGui.QFileDialog.Detail)

		if not dialog.exec_(): return

		self.config_file = str(dialog.selectedFiles()[0])
		config = self.mm.clone()

		with open(self.config_file, 'w') as fd:
			json.dump(config, fd)

		print("Config write:")
		print(json.dumps(config, sort_keys=True, indent=4))


class Main(QtGui.QMainWindow):
	def __init__(self, parent = None):
		super(Main, self).__init__(parent)

		uic.loadUi('qt/mod/mainwindow.ui', self)
		self.mm = ModManager(self)
		self.pm = PlugManager(self.mm)
		self.mm.set_plug_manager(self.pm)
		self.conf = Config(self, self.mm)



#MODS = [ModScale, ModCLAHE, ModRange, ModMorph, ModBitwise, ModHist2D]
MODS = [ModImage, ModViewer, ModScale, ModRange, ModMorph,
		ModBitwise, ModHoughCircle, ModCanny, ModBlur, ModSkeleton, ModHoughEllipse,
		ModFindContours, ModApproxPoly, ModGeometry]
app = QtGui.QApplication(sys.argv)
#app.setStyle("plastique")
myWidget = Main()
myWidget.show()
app.exec_()

