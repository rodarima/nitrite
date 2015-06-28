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




#class ModTest(ModIO):
#
#	def init_IO(self):
#		self.add_input("In", [ImageColor])
#		self.add_output("Out")
#	
#	def init_GUI(self):
#		self.values = ['RGB', 'HSV', 'HLS']
#		self.add_combo("Color space", values)
#	
#	def update(self):
#		data = self.get_input("In")
#		color_space = self.get_combo("Color space")
#		out = data.convert(color_space)
#		self.set_output("Out", out)
#
#class ModCircles(ModIO):
#
#	def init_IO(self):
#		self.add_input("In", [ImageColor])
#		self.add_output("Draw")
#		self.add_output("Array")
#	
#	def init_GUI(self):
#		self.add_int("Inv. Ratio")
#		self.add_int("Min. Distance")
#		self.add_group("Radius")
#		self.add_int("Min", group="Radius", optional=True)
#		self.add_int("Max", group="Radius", optional=True)
#		self.add_int("Canny thr.", optional=True)
#		self.add_int("Accumulator thr.", optional=True)
#	
#	def update(self):
#		data = self.get_input("In")
#		color_space = self.get_combo("Color space")
#		img = data.img
#		circles = cv2.HoughCircles(
#			img,
#			method = cv2.CV_HOUGH_GRADIENT,
#			dp = self.get_int("Inv. Ratio"),
#			minDist = self.get_int("Min. Distance")
#			param1 = self.get_int("Canny thr.")
#			param2 = self.get_int("Accumulator thr.")
#			minRadius = self.get_int("Min", group="Radius")
#			maxRadius = self.get_int("Max", group="Radius")
#		)
#		self.set_output("Array", circles)

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

#class ModSpin:
#	def add_int(self, label, min=0, max=None, step=1, group=None):

class ModDouble:

	def __init__(self):
		self.gui_double = {}

	def add_double(self, label, min=0.0, max=None, step=0.01, value=0):
		if label in self.gui_double: raise RuntimeError()
		self.gui_double[label] = QtGui.QDoubleSpinBox()
		double = self.gui_double[label]
		double.setMinimum(min)
		double.setMaximum(max)
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


#class ModSimple(Mod):
#	"One input, one output"
#	def __init__(self, w, name):
#		Mod.__init__(self, name)
#		self.w = w
#		self.module = QtGui.QGroupBox()
#		self.module.setTitle(name)
##		self.module.setFlat(True)
##		self.module.setCheckable(True)
#		self.module_layout = QtGui.QFormLayout()
#		self.module.setLayout(self.module_layout)
#
#		self.combo_in = QtGui.QComboBox()
#		self.combo_in_values = []
#		self.text_out = QtGui.QLineEdit()
#		self.text_out.setText(name + '_out')
#
#		self.module_layout.addRow("In", self.combo_in)
#		self.module_layout.addRow("Out", self.text_out)
#		self.on_update = None
#		self._enable_signals()
#
#		self.w.scroll_layout.addWidget(self.module)
#		self.text_out.selectAll()
#		self.text_out.setFocus()
#
#		self.inputs += [PlugIn(self, name + '_in')]
#		self.outputs += [PlugOut(self, name + '_out')]
#
#	# -----
#
#	def register_update(self, f): self.on_update = f
#
#	def update(self):
#		'No hacer nada, solo reenviar la entrada'
#		print("Simple update called")
#		if self.inputs[0].connected():
#			data = self.inputs[0].data
#			self.output[0].update(data)
#
#	def update_plugs(self, all_inputs, all_outputs):
#		Mod.update_plugs(self, all_inputs, all_outputs)
#		self._update_inputs()
#
#	def restore(self, d):
#		self._disable_signals()
#
#		self.text_out.setText(d['text_out'])
#		self.combo_in_values = d['combo_in_values']
#		combo = self.combo_in
#		combo.clear()
#		combo.addItems(self.combo_in_values)
#		i = d['combo_in_index']
#		if i < len(self.combo_in_values) and i >= 0:
#			self.combo_in.setCurrentIndex(i)
#
#		self._enable_signals()
#
#	def clone(self):
#		d = {}
#		d['combo_in_values'] = self.combo_in_values
#		d['combo_in_index'] = self.combo_in.currentIndex()
#		d['text_out'] = str(self.text_out.text())
#		return d
#
#	# -----
#	def new_combo(self, name, values, on_update):
#		combo = QtGui.QComboBox()
#		combo.addItems(values)
#		if len(values) > 0: combo.setCurrentIndex(0)
#		combo.currentIndexChanged.connect(on_update)
#		if name: self.module_layout.addRow(name, combo)
#		return combo
#
#	def new_spin(self, name, min_v, max_v, val, on_update):
#		spin = QtGui.QSpinBox()
#		spin.setMinimum(min_v)
#		spin.setMaximum(max_v)
#		spin.setValue(val)
#		spin.valueChanged.connect(on_update)
#		if name: self.module_layout.addRow(name, spin)
#		return spin
#
#
#	def _disable_signals(self):
#		self.text_out.editingFinished.disconnect(self._out_updated)
#		self.combo_in.currentIndexChanged.disconnect(self._in_updated)
#
#	def _enable_signals(self):
#		self.text_out.editingFinished.connect(self._out_updated)
#		self.combo_in.currentIndexChanged.connect(self._in_updated)
#
#
#	def _out_updated(self):
#		out_name = str(self.text_out.text())
#		self.outputs[0].name = out_name
#		if self.on_update: self.on_update(self)
#
#	def _in_updated(self):
#		'Al cambiar la elección del combo de entrada'
#		selected_name = str(self.combo_in.currentText())
#		for plug_out in self.all_outputs:
#			if plug_out.name == selected_name:
#				#print("connecting "+self.name+' with '+ plug_out.name)
#				self.inputs[0].disconnect()
#				self.inputs[0].connect(plug_out)
#				self.update()
#				break
#
#	def _update_inputs(self):
#		"Actualiza en el combo las nuevas entradas"
#		available_outputs = []
#		for plug in self.all_outputs:
#			# No añadir la propia salida
#			if plug.mod == self: continue
#			available_outputs.append(plug)
#
#		self.combo_in_values = [plug.get_name() for plug in available_outputs]
#
#		combo = self.combo_in
#		i = combo.currentIndex()
#
#		combo.clear()
#		combo.addItems(self.combo_in_values)
#		if i < len(self.combo_in_values) and i >= 0:
#			combo.setCurrentIndex(i)

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

		rgb = data.convert('RGB')
		gray = data.convert('gray')
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
				cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),2)
				# draw the center of the circle
				cv2.circle(img,(i[0],i[1]),2,(0,0,255),3)

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

class ModList:

	def __init__(self):
		self.current_index = -1
		self.enable()

	def gui_add_mod(self, mod):
		widget_list = self.w.list_mods
		widget_list.addItem(mod.name)

	def gui_clear_list(self):
		self.w.list_mods.clear()

	def enable(self):
		self.w.list_mods.itemSelectionChanged.connect(self.select_mod)

	def hide_mod(self):
		if self.current_index == -1: return
		name = self.mod_names[self.current_index]
		self.mods[name].hide()

	def select_mod(self):
		self.hide_mod()
		i = self.w.list_mods.currentRow()
		self.current_index = i
		if i == -1: return

		name = self.mod_names[i]
		self.mods[name].show()

class ModManager(ModList):
	def __init__(self, window):
		self.w = window
		self.mods = {}
		self.mod_names = []

		# Añadir lista de modulos
		self.all_mods = self.get_all_mods()
		self.all_mod_names = self.get_mod_names(self.all_mods)
		self.w.combo_mod.addItems(self.all_mod_names)

		# Boton de añadir modulos
		self.w.button_add_mod.clicked.connect(self.add_mod)

		# ModList para la lista de módulos
		ModList.__init__(self)

		# Actualizar las salidas
		#self.update_io()

	def set_plug_manager(self, pm):
		self.pm = pm

	def process(self):
		self.mod_out.get_input()

	def widget_update(self, mod):
		'Los parámetros de un módulo han cambiado de valor'

		# Si la salida está vacía borrar el módulo
		# FIXME ???

		self.update()

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

	def add_mod(self):
		if self.w.combo_mod.currentIndex() < 0: return

		i = self.w.combo_mod.currentIndex()
		mod_class = self.all_mods[i]
		name = self.new_name(mod_class.mod_name)
		mod = mod_class(name, self.pm, self.w)
		self.mods[name] = mod
		self.mod_names.append(name)
		self.gui_add_mod(mod)
		#print("Added " + str(mod.name))
		#self.pm.show()
		#mod.show()

#	def _get_mod_conf(self, conf, mod_name):
#		for mod_conf in conf:
#			if mod_conf['name'] == mod_name: return mod_conf
#		return None
#

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
			self.gui_add_mod(mod)
			
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
			
#		# Conectarlas
#		self.plugs_out = []
#		self.plugs_in = []
#		for m in self.modlist:
#			self.plugs_out += m.get_outputs()
#			self.plugs_in += m.get_inputs()
#
#		self.plugs_out_name = [plug.name for plug in self.plugs_out]
#		self.plugs_in_name = [plug.name for plug in self.plugs_in]
#
#		for mod in self.modlist:
#			# Solo conectar las entradas, las salidas se conectarán
#			# automáticamente
#			mod_conf = self._get_mod_conf(config, mod.name)
#			conf_inputs = mod_conf['plugs']['inputs']
#			for i in range(len(mod.inputs)):
#				mod_input = mod.inputs[i]
#				name_input, name_outputs = conf_inputs[i]
#				for name in name_outputs:
#					j = self.plugs_out_name.index(name)
#					plug_out = self.plugs_out[j]
#					mod_input.connect(plug_out)
#
#			# Configurar individualmente cada módulo
#			mod.restore(mod_conf['Mod'])
#
#		self.update()
#		self.mod_in.update()

#		for mod in self.modlist:
#			print("---- {} ----".format(mod.name))
#			print("Outputs")
#			for out_plug in mod.outputs:
#				out_plug.show()
#			print("Inputs")
#			for in_plug in mod.inputs:
#				in_plug.show()


#
#	def _get_plugs_conf(self, mod):
#		'Obtiene las conexiones de un módulo'
#		conf_inputs = []
#		for plug_in in mod.inputs:
#			names = [plug.name for plug in plug_in.plugs]
#			conf_inputs += [(plug_in.name, names)]
#		conf_outputs = []
#		for plug_out in mod.outputs:
#			names = [plug.name for plug in plug_out.plugs]
#			conf_outputs += [(plug_out.name, names)]
#
#		return {'inputs':conf_inputs, 'outputs':conf_outputs}
#
#	def _set_plugs_conf(self, mod, mod_conf):
#		'Crea las conexiones de un módulo, sin conectarlas'
#		mod.inputs = []
#		mod.outputs = []
#
#		plug_conf = mod_conf['plugs']
#		conf_inputs = plug_conf['inputs']
#		conf_outputs = plug_conf['outputs']
#
#		for conf_input in conf_inputs:
#			name, names = conf_input
#			mod.inputs.append(PlugIn(mod, name))
#
#		for conf_output in conf_outputs:
#			name, names = conf_output
#			mod.outputs.append(PlugOut(mod, name))
#

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
MODS = [ModTestInput, ModImage, ModViewer, ModScale, ModRange, ModMorph,
		ModBitwise, ModHoughCircle, ModCanny]
app = QtGui.QApplication(sys.argv)
#app.setStyle("plastique")
myWidget = Main()
myWidget.show()
app.exec_()

