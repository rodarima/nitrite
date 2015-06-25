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

import sys
import json
import pprint
import traceback


class Plug:
	def __init__(self, mod, name):
		self.mod = mod
		self.name = name
		self.plugs = []
		self.data = None

	def get_mod(self):
		return self.mod

	def get_name(self):
		return self.name

	def set_mod(self, mod):
		self.mod = mod

	def set_name(self, name):
		self.name = name

	def connections(self):
		return len(self.plugs)

	def show(self):
		plugs = [plug.name for plug in self.plugs]
		print("{} -> {}".format(self.name, plugs))

class PlugIn(Plug):
	def connect(self, plug_out):
		if not isinstance(plug_out, PlugOut): return
		if self.plugs != []: print("PLUG ERROR")
		self.plugs = [plug_out]
		plug_out.plugs += [self]
		self.data = plug_out.data

	def disconnect(self):
		if self.plugs != []:
			while self in self.plugs[0].plugs:
				self.plugs[0].plugs.remove(self)
			self.plugs = []
		else:
			print("PLUG ALREADY DISCONNECTED!")
			#raise Exception()

	def update(self, data):
		print('PlugIn {} updating mod {}'.format(self.name, self.mod.name))
		self.data = data
		self.mod.update()

	def connected(self):
		return self.plugs != []

class PlugOut(Plug):
	def connect(self, plug_in):
		if not isinstance(plug_in, PlugIn): return
		self.plugs += [plug_in]
		plug_in.plugs = [self]

	def disconnect(self, plug_in):
		if not isinstance(plug_in, PlugIn): return
		while plug_in in self.plugs:
			self.plugs.remove(plug_in)
			plug_in.plugs = []

	def update(self, data):
		print('PlugOut {} updating mod {}'.format(self.name, self.mod.name))
		self.data = data
		for plug in self.plugs:
			plug.update(data)

class Mod:
	def __init__(self, name):
		self.inputs = []
		self.outputs = []
		self.plugs = []
		self.name = name

	def get_inputs(self):
		return self.inputs

	def get_outputs(self):
		return self.outputs

	def update_plugs(self, all_inputs, all_outputs):
		'Actualiza las conexiones disponibles'
		self.all_inputs = all_inputs
		self.all_outputs = all_outputs

	def restore(self, config):
		raise NotImplemented()

	def clone(self):
		raise NotImplemented()

class ModSimple(Mod):
	"One input, one output"
	def __init__(self, w, name):
		Mod.__init__(self, name)
		self.w = w
		self.module = QtGui.QGroupBox()
		self.module.setTitle(name)
#		self.module.setFlat(True)
#		self.module.setCheckable(True)
		self.module_layout = QtGui.QFormLayout()
		self.module.setLayout(self.module_layout)

		self.combo_in = QtGui.QComboBox()
		self.combo_in_values = []
		self.text_out = QtGui.QLineEdit()
		self.text_out.setText(name + '_out')

		self.module_layout.addRow("In", self.combo_in)
		self.module_layout.addRow("Out", self.text_out)
		self.on_update = None
		self._enable_signals()

		self.w.scroll_layout.addWidget(self.module)
		self.text_out.selectAll()
		self.text_out.setFocus()

		self.inputs += [PlugIn(self, name + '_in')]
		self.outputs += [PlugOut(self, name + '_out')]

	# -----

	def register_update(self, f): self.on_update = f

	def update(self):
		'No hacer nada, solo reenviar la entrada'
		print("Simple update called")
		if self.inputs[0].connected():
			data = self.inputs[0].data
			self.output[0].update(data)

	def update_plugs(self, all_inputs, all_outputs):
		Mod.update_plugs(self, all_inputs, all_outputs)
		self._update_inputs()

	def restore(self, d):
		self._disable_signals()

		self.text_out.setText(d['text_out'])
		self.combo_in_values = d['combo_in_values']
		combo = self.combo_in
		combo.clear()
		combo.addItems(self.combo_in_values)
		i = d['combo_in_index']
		if i < len(self.combo_in_values) and i >= 0:
			self.combo_in.setCurrentIndex(i)

		self._enable_signals()

	def clone(self):
		d = {}
		d['combo_in_values'] = self.combo_in_values
		d['combo_in_index'] = self.combo_in.currentIndex()
		d['text_out'] = str(self.text_out.text())
		return d

	# -----
	def new_combo(self, name, values, on_update):
		combo = QtGui.QComboBox()
		combo.addItems(values)
		if len(values) > 0: combo.setCurrentIndex(0)
		combo.currentIndexChanged.connect(on_update)
		if name: self.module_layout.addRow(name, combo)
		return combo

	def new_spin(self, name, min_v, max_v, val, on_update):
		spin = QtGui.QSpinBox()
		spin.setMinimum(min_v)
		spin.setMaximum(max_v)
		spin.setValue(val)
		spin.valueChanged.connect(on_update)
		if name: self.module_layout.addRow(name, spin)
		return spin


	def _disable_signals(self):
		self.text_out.editingFinished.disconnect(self._out_updated)
		self.combo_in.currentIndexChanged.disconnect(self._in_updated)

	def _enable_signals(self):
		self.text_out.editingFinished.connect(self._out_updated)
		self.combo_in.currentIndexChanged.connect(self._in_updated)


	def _out_updated(self):
		out_name = str(self.text_out.text())
		self.outputs[0].name = out_name
		if self.on_update: self.on_update(self)

	def _in_updated(self):
		'Al cambiar la elección del combo de entrada'
		selected_name = str(self.combo_in.currentText())
		for plug_out in self.all_outputs:
			if plug_out.name == selected_name:
				#print("connecting "+self.name+' with '+ plug_out.name)
				self.inputs[0].disconnect()
				self.inputs[0].connect(plug_out)
				self.update()
				break

	def _update_inputs(self):
		"Actualiza en el combo las nuevas entradas"
		available_outputs = []
		for plug in self.all_outputs:
			# No añadir la propia salida
			if plug.mod == self: continue
			available_outputs.append(plug)

		self.combo_in_values = [plug.get_name() for plug in available_outputs]

		combo = self.combo_in
		i = combo.currentIndex()

		combo.clear()
		combo.addItems(self.combo_in_values)
		if i < len(self.combo_in_values) and i >= 0:
			combo.setCurrentIndex(i)

class Mod2to1(Mod):
	"Two inputs, one output"
	def __init__(self, w, name):
		Mod.__init__(self, name)
		self.w = w
		self.module = QtGui.QGroupBox()
		self.module.setTitle(name)
#		self.module.setFlat(True)
#		self.module.setCheckable(True)
		self.module_layout = QtGui.QFormLayout()
		self.module.setLayout(self.module_layout)

		self.combo_in = [QtGui.QComboBox(), QtGui.QComboBox()]
		self.combo_in_values = []
		self.text_out = QtGui.QLineEdit()
		self.text_out.setText(name + '_out')

		self.module_layout.addRow("In 1", self.combo_in[0])
		self.module_layout.addRow("In 2", self.combo_in[1])
		self.module_layout.addRow("Out", self.text_out)
		self.on_update = None
		self._enable_signals()

		self.w.scroll_layout.addWidget(self.module)
		self.text_out.selectAll()
		self.text_out.setFocus()

		self.inputs += [PlugIn(self, name + '_in1'), PlugIn(self, name + '_in2')]
		self.outputs += [PlugOut(self, name + '_out')]

	# -----

	def register_update(self, f): self.on_update = f

	def update(self):
		'No hacer nada, solo reenviar la entrada'
		print("Simple update called")
		if self.inputs[0].connected():
			data = self.inputs[0].data
			self.output[0].update(data)

	def update_plugs(self, all_inputs, all_outputs):
		Mod.update_plugs(self, all_inputs, all_outputs)
		self._update_inputs()

	def restore(self, d):
		self._disable_signals()

		self.text_out.setText(d['text_out'])
		self.combo_in_values = d['combo_in_values']
		for combo in self.combo_in:
			combo.clear()
			combo.addItems(self.combo_in_values)
			i = d['combo_in_index']
			if i < len(self.combo_in_values) and i >= 0:
				combo.setCurrentIndex(i)

			self._enable_signals()

	def clone(self):
		d = {}
		d['combo_in_values'] = self.combo_in_values
		d['combo_in_index'] = [combo.currentIndex() for combo in self.combo_in]
		d['text_out'] = str(self.text_out.text())
		return d

	# -----
	def new_combo(self, name, values, on_update):
		combo = QtGui.QComboBox()
		combo.addItems(values)
		if len(values) > 0: combo.setCurrentIndex(0)
		combo.currentIndexChanged.connect(on_update)
		if name: self.module_layout.addRow(name, combo)
		return combo

	def new_spin(self, name, min_v, max_v, val, on_update):
		spin = QtGui.QSpinBox()
		spin.setMinimum(min_v)
		spin.setMaximum(max_v)
		spin.setValue(val)
		spin.valueChanged.connect(on_update)
		if name: self.module_layout.addRow(name, spin)
		return spin


	def _disable_signals(self):
		self.text_out.editingFinished.disconnect(self._out_updated)
		for combo in self.combo_in:
			combo.currentIndexChanged.disconnect(self._in_updated)

	def _enable_signals(self):
		self.text_out.editingFinished.connect(self._out_updated)
		for combo in self.combo_in:
			combo.currentIndexChanged.connect(self._in_updated)


	def _out_updated(self):
		out_name = str(self.text_out.text())
		self.outputs[0].name = out_name
		if self.on_update: self.on_update(self)

	def _in_updated(self):
		'Al cambiar la elección un combo de la entrada'
		for i in range(len(self.combo_in)):
			combo = self.combo_in[i]
			selected_name = str(combo.currentText())
			for plug_out in self.all_outputs:
				if plug_out.name == selected_name:
					#print("connecting "+self.name+' with '+ plug_out.name)
					self.inputs[i].disconnect()
					self.inputs[i].connect(plug_out)
					self.update()
					break

	def _update_inputs(self):
		"Actualiza en el combo las nuevas entradas"
		available_outputs = []
		for plug in self.all_outputs:
			# No añadir la propia salida
			if plug.mod == self: continue
			available_outputs.append(plug)

		self.combo_in_values = [plug.get_name() for plug in available_outputs]

		for combo in self.combo_in:
			i = combo.currentIndex()

			combo.clear()
			combo.addItems(self.combo_in_values)
			if i < len(self.combo_in_values) and i >= 0:
				combo.setCurrentIndex(i)

class ModInput(Mod):
	name = "Image"
	def __init__(self, w):
		Mod.__init__(self, ModInput.name)
		self.outputs += [PlugOut(self, ModInput.name + '_out')]
		self.w = w
		self._enable_signals()
		self.image_files = []

	def _add_images(self):
		dialog = QtGui.QFileDialog()
		dialog.setFileMode(QtGui.QFileDialog.ExistingFiles)
		dialog.setNameFilter("Images (*.png *.jpg *.gif *.bmp)")
		dialog.setViewMode(QtGui.QFileDialog.Detail)

		if(dialog.exec_()):
			fileNames = dialog.selectedFiles()
			self.image_files += [str(f) for f in fileNames]
		self._update_images()

	def _update_images(self):
		imglist = self.w.list_images
		i = imglist.currentRow()

		imglist.clear()
		imglist.addItems(self.image_files)

		if(i >= 0 and i < len(self.image_files)):
			imglist.setCurrentRow(i)
		elif len(self.image_files) > 0:
			imglist.setCurrentRow(0)


	def _get_image(self):
		if self.w.list_images.currentRow() != -1:
			i = self.w.list_images.currentRow()
			return str(self.w.list_images.item(i).text())

		return None

	def _disable_signals(self):
		self.w.list_images.itemSelectionChanged.disconnect(self.update)
		self.w.button_add_images.clicked.disconnect(self._add_images)

	def _enable_signals(self):
		self.w.list_images.itemSelectionChanged.connect(self.update)
		self.w.button_add_images.clicked.connect(self._add_images)

	def update(self):
		img_name = self._get_image()
		if(img_name == None): return

		bgr = cv2.imread(img_name)
		i = ImageBGR(bgr)
		self.outputs[0].update(i)

	def restore(self, d):
		self._disable_signals()
		self.image_files = d['image_files']
		self._update_images()
		i = d['image_index']
		if i >= 0 and i < len(self.image_files):
			self.w.list_images.setCurrentRow(i)
		self._enable_signals()

	def clone(self):
		d = {}
		d['image_files'] = self.image_files
		d['image_index'] = self.w.list_images.currentRow()
		return d

	#No necesita actualizar la salida, pues siempre es la misma


class ModOutput(Mod):
	name = 'Viewer'
	def __init__(self, w):
		Mod.__init__(self, ModOutput.name)
		self._init_gui(w)
		self.inputs += [PlugIn(self, ModOutput.name + '_in')]

	def _init_gui(self, w):
		self.w = w
		self.module = QtGui.QGroupBox()
		self.module_layout = QtGui.QFormLayout()
		self.module.setTitle(ModOutput.name)
		self.module.setLayout(self.module_layout)

		self.combo_in = QtGui.QComboBox()
		self._enable_signals()

		self.module_layout.addRow("In", self.combo_in)
		w.scroll_layout.addWidget(self.module)

	def update(self):
		'Reprocesa los datos a partir de las entradas'
		plug_in = self.inputs[0]
		if plug_in.connections == 0: return
		if plug_in.data == None: return

		print(type(plug_in.data).__name__)
		print(plug_in.data.img.shape)
		print("---- {} CONNECTIONS ----".format(self.name))
		print("Outputs")
		for out_plug in self.outputs:
			out_plug.show()
		print("Inputs")
		for in_plug in self.inputs:
			in_plug.show()
		print("---- END CONNECTIONS ----")
		self._load_image(plug_in.data)

	def _updated(self):
		'Al cambiar la elección del combo'
		#print("Output combo_in changed")

		selected_name = str(self.combo_in.currentText())

		#for plug_out in self.all_outputs:
		#	plug_out.show()
		for plug_out in self.all_outputs:
			if plug_out.name == selected_name:
				self.inputs[0].disconnect()
				self.inputs[0].connect(plug_out)
				self.update()
				break

	def _load_image(self, img):
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

	def _update_inputs(self):
		"Actualiza en el combo las nuevas entradas"
		available_outputs = []
		for plug in self.all_outputs:
			# No añadir la propia salida
			if plug.mod == self: continue
			available_outputs.append(plug)

		self.combo_in_values = [plug.get_name() for plug in available_outputs]

		combo = self.combo_in
		i = combo.currentIndex()

		combo.clear()
		combo.addItems(self.combo_in_values)
		if i < len(self.combo_in_values) and i >= 0:
			combo.setCurrentIndex(i)

	def _disable_signals(self):
		self.combo_in.currentIndexChanged.disconnect(self._updated)

	def _enable_signals(self):
		self.combo_in.currentIndexChanged.connect(self._updated)

	def update_plugs(self, all_inputs, all_outputs):
		Mod.update_plugs(self, all_inputs, all_outputs)
		self._update_inputs()

	def restore(self, d):
		self._disable_signals()

		self.combo_in_values = d['combo_in_values']
		combo = self.combo_in
		combo.clear()
		combo.addItems(self.combo_in_values)
		i = d['combo_in_index']
		if i < len(self.combo_in_values) and i >= 0:
			self.combo_in.setCurrentIndex(i)

		self._enable_signals()

	def clone(self):
		d = {}
		d['combo_in_values'] = self.combo_in_values
		d['combo_in_index'] = self.combo_in.currentIndex()
		return d

class ModScale(ModSimple):
	name = 'Scale'
	def __init__(self, w, name):
		ModSimple.__init__(self, w, name)
		self.scale = QtGui.QDoubleSpinBox()
		self.scale.setMinimum(0.001)
		self.scale.setMaximum(100)
		self.scale.setSingleStep(0.05)
		self.scale.setValue(0.45)

		self.module_layout.addRow("Factor", self.scale)
		self.scale.valueChanged.connect(self.update)

	def update(self):
		if not self.inputs[0].connected(): return
		data = self.inputs[0].data
		if data == None:
			#print("Scale got None")
			return

		rgb = self.inputs[0].data.convert('rgb').img

		s = min(max(self.scale.value(), 0.001), 100)
		rgb = cv2.resize(rgb, (0,0), fx=s, fy=s)
		self.outputs[0].update(ImageRGB(rgb))

	def restore(self, d):
		self.scale.setValue(d['scale'])
		ModSimple.restore(self, d['ModSimple'])

	def clone(self):
		d = {}
		d['scale'] = self.scale.value()
		d['ModSimple'] = ModSimple.clone(self)
		return d

class ModRange(ModSimple):
	name = 'Range'
	def __init__(self, w, name):
		ModSimple.__init__(self, w, name)
		self.minmax = ['Min', 'Max']
		self.models = ImageColor.models
		self.model_names = [c.alias[0] for c in self.models]
		self.model = self.models[0]
		self._add_model_combo()
		#self._add_channel_labels()
		#self._add_bars()
		self.label_layout = None
		self.bar_layouts = []
		self.bars = []
		self.bars_values = []

		self._add_model_range()

	# --- add ---

	def _add_model_range(self):
		self.range_layout = QtGui.QFormLayout()
		self.range_widget = QtGui.QWidget()
		self.range_widget.setLayout(self.range_layout)

		self._add_channel_labels()
		self._add_bars()

		self.module_layout.addRow(self.range_widget)

	def _add_bars(self):
		self.bars = []
		num_channels = len(self.model.channels)
		for label in self.minmax:
			self._add_bars_row(label, num_channels)

	def _add_bars_row(self, label, n):
			row_layout = QtGui.QHBoxLayout()
			bars = []
			for channel in self.model.channels:
				bar = self._add_bar(0, 255)
				bars.append(bar)
				row_layout.addWidget(bar)

			self.range_layout.addRow(label, row_layout)
			self.bar_layouts.append(row_layout)
			self.bars.append(bars)

	def _add_channel_labels(self):
		channel_names = self.model.channels
		label_layout = QtGui.QHBoxLayout()
		for c in channel_names:
			label_layout.addWidget(QtGui.QLabel(c))

		self.range_layout.addRow('', label_layout)

	def _add_model_combo(self):
		self.combo_model = QtGui.QComboBox()
		self.combo_model.addItems(self.model_names)
		self.module_layout.addRow('Model', self.combo_model)
		self.combo_model.currentIndexChanged.connect(self.update_model)

	def _add_bar(self, min_val, max_val):
		bar = QtGui.QSpinBox()
		bar.setMinimum(min_val)
		bar.setMaximum(max_val)
		bar.valueChanged.connect(self.update)
		return bar

	# --- delete ---

	def _delete_model_range(self):
		self.range_widget.deleteLater()
		self.range_widget = None
		self.label_layout = None
		self.bar_layouts = []
		self.bars = []
		self.bars_values = []


	def _get_values(self):
		values = []
		for i in range(len(self.minmax)):
			row = []
			for j in range(len(self.model.channels)):
				row.append(self.bars[i][j].value())
			values.append(row)
		return values

	def _set_values(self, values):
		for i in range(len(values)):
			for j in range(len(values[i])):
				self.bars[i][j].setValue(values[i][j])

	def update_model(self):
		print('TODO: Recalcular modelo')
		self._delete_model_range()
		i = self.combo_model.currentIndex()
		self.model = self.models[i]
		self._add_model_range()
		self.update()

	def _update_bar_values(self):
		self.bars_values = []
		for row in self.bars:
			row_values = []
			for bar in row:
				row_values.append(bar.value())
			self.bars_values.append(row_values)

	def update(self):
		self._update_bar_values()
		print(self.bars_values)
		if not self.inputs[0].connected(): return
		data = self.inputs[0].data
		if data == None: return

		data_model = data.convert(self.model.alias[0])
		data_img = data_model.img
		min_val = np.array(self.bars_values[0])
		max_val = np.array(self.bars_values[1])
		print("range con {} y {}".format(min_val, max_val))

		gray = cv2.inRange(data_img, min_val, max_val)
		print("inRange shape " + str(gray.shape))
		data = ImageGray(gray)

		self.outputs[0].update(data)

	def restore(self, d):
		ModSimple.restore(self, d['ModSimple'])
		self.combo_model.setCurrentIndex(d['model'])
		self._set_values(d['values'])
		return

	def clone(self):
		d = {}
		d['values'] = self._get_values()
		d['model'] = self.combo_model.currentIndex()
		d['ModSimple'] = ModSimple.clone(self)
		return d

class ModMorph(ModSimple):
	name = 'Morphology'

	def __init__(self, w, name):
		ModSimple.__init__(self, w, name)
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

		self._add_widgets()

	def _add_widgets(self):
		self.combo_operation = self.new_combo(
			'Operation', self.operations_name, self.update)
		self.combo_shape = self.new_combo(
			'Shape', self.kernel_shapes_name, self.update)
		self.spin_size = self.new_spin(
			'Size', 1, 200, 5, self.update)

	def update(self):
		if not self.inputs[0].connected(): return
		data = self.inputs[0].data
		if data == None:
			#print("Scale got None")
			return
		print("---- {} CONNECTIONS ----".format(self.name))
		print("Outputs")
		for out_plug in self.outputs:
			out_plug.show()
		print("Inputs")
		for in_plug in self.inputs:
			in_plug.show()
		print("---- END CONNECTIONS ----")

		size = self.spin_size.value()
		operation = self.operations[self.combo_operation.currentIndex()][1]
		shape = self.kernel_shapes[self.combo_shape.currentIndex()][1]

		img = data.img
		kernel = cv2.getStructuringElement(shape, (size, size))
		opening = cv2.morphologyEx(img, operation, kernel)

		data = ImageGray(opening)

		self.outputs[0].update(data)

	def restore(self, d):
		self.combo_operation.setCurrentIndex(d['operation'])
		self.combo_shape.setCurrentIndex(d['shape'])
		self.spin_size.setValue(d['size'])
		ModSimple.restore(self, d['ModSimple'])

	def clone(self):
		d = {}
		d['size'] = self.spin_size.value()
		d['operation'] = self.combo_operation.currentIndex()
		d['shape'] = self.combo_shape.currentIndex()
		d['ModSimple'] = ModSimple.clone(self)
		return d

class ModBitwise(Mod2to1):
	name = 'Bitwise'

	def __init__(self, w, name):
		Mod2to1.__init__(self, w, name)
		self.operations = [
			('AND',	cv2.bitwise_and,	2),
			('OR',	cv2.bitwise_or,		2),
			('XOR',	cv2.bitwise_xor,	2),
			('NOT',	cv2.bitwise_not,	1)
		]
		self.operations_name = [op[0] for op in self.operations]

		self._add_widgets()


	def _add_widgets(self):
		self.combo_operation = self.new_combo(
			'Logic', self.operations_name, self.update)

	def update(self):
		print("  -->  Traceback for Bitwise")
		traceback.print_stack()
		raise Exception
		if not self.inputs[0].connected(): return
		if not self.inputs[0].data: return

		print("---- {} CONNECTIONS ----".format(self.name))
		print("Outputs")
		for out_plug in self.outputs:
			out_plug.show()
		print("Inputs")
		for in_plug in self.inputs:
			in_plug.show()
		print("---- END CONNECTIONS ----")

		operation_tuple = self.operations[self.combo_operation.currentIndex()]
		operation_function = operation_tuple[1]

		data1 = self.inputs[0].data
		img1 = data1.img

		if operation_tuple[2] == 2:
			if not self.inputs[1].connected(): return
			if not self.inputs[1].data: return
			print("Applying {}".format(operation_tuple[0]))
			data2 = self.inputs[1].data
			img2 = data2.img
			dst = operation_function(src1 = img1, src2 = img2)
		elif operation_tuple[2] == 1:
			dst = operation_function(src = img1)

		print("Applyed shape {}".format(dst.shape))

		data = ImageGray(dst)

		self.outputs[0].update(data)

	def restore(self, d):
		self.combo_operation.setCurrentIndex(d['operation'])
		Mod2to1.restore(self, d['Mod2to1'])

	def clone(self):
		d = {}
		d['operation'] = self.combo_operation.currentIndex()
		d['Mod2to1'] = Mod2to1.clone(self)
		return d

class ModCLAHE(ModSimple):
	name = 'CLAHE'
	def __init__(self, w, name):
		ModSimple.__init__(self, w, name)
		self.clip = QtGui.QDoubleSpinBox()
		self.clip.setMinimum(0.0)
		self.clip.setMaximum(100.0)
		self.clip.setSingleStep(0.1)
		self.clip.setValue(2.0)

		self.module_layout.addRow("Clip", self.clip)
		self.clip.valueChanged.connect(self.update)

		self.size = QtGui.QSpinBox()
		self.size.setMinimum(1)
		self.size.setMaximum(100.0)
		self.size.setSingleStep(1)
		self.size.setValue(8)

		self.module_layout.addRow("Size", self.size)
		self.size.valueChanged.connect(self.update)

#	def _add_channels(self, ...)
# TODO: Añadir un selector de canales en el módulo y filtrado

	def update(self):
		if not self.inputs[0].connected(): return
		data = self.inputs[0].data
		if data == None:
			#print("CLAHE got None")
			return

		rgb = self.inputs[0].data.convert('rgb')

		hls = self.equalize(rgb)
		self.outputs[0].update(hls)

	def equalize_channel(self, img, c):
		'Ecualiza el canal indicado en la imagen, sobreescribiéndolo'
		img_channel = img[:,:,c]
		eq = cv2.equalizeHist(img_channel)
		img[:,:,c] = eq
		return img

	def equalize(self, img):
		hls = img.convert('hls')
		clip_val = self.clip.value()
		size_val = self.size.value()
		clahe = cv2.createCLAHE(clipLimit=clip_val, tileGridSize=(size_val,size_val))
		L = hls.img[:,:,1]
		hls.img[:,:,1] = clahe.apply(L)

#		img_ycrcb = cv2.cvtColor(rgb, cv2.COLOR_RGB2HLS)
#		eq = self.equalize_channel(img_ycrcb, 1)
#		return cv2.cvtColor(hls, cv2.COLOR_HLS2RGB)
#		return cv2.cvtColor(hls[:,:,2], cv2.COLOR_GRAY2RGB)

		return hls

	def restore(self, d):
		self.clip.setValue(d['clip'])
		self.size.setValue(d['size'])
		ModSimple.restore(self, d['ModSimple'])

	def clone(self):
		d = {}
		d['clip'] = self.clip.value()
		d['size'] = self.size.value()
		d['ModSimple'] = ModSimple.clone(self)
		return d


class ModManager:
	def __init__(self, w):
		self. w = w
		self.modlist = []

		# Añadir lista de modulos
		self.all_mods = self.get_all_mods()
		self.all_mod_names = self.get_mod_names(self.all_mods)
		self.w.combo_mod.addItems(self.all_mod_names)

		# Boton de añadir modulos
		self.w.button_add_mod.clicked.connect(self.add_mod)

		# Entrada y salida
		self.mod_in = ModInput(w)
		self.mod_out = ModOutput(w)
		self.modlist.append(self.mod_in)
		self.modlist.append(self.mod_out)

		# Actualizar las salidas
		self.update()

	def remove_mod(self, mod):
		#print("Del " + str(mod.name))
		self.modlist.remove(mod)
		self.w.scroll_layout.removeWidget(mod.module)
		mod.module.setParent(None)

	def process(self):
		self.mod_out.get_input()

	def widget_update(self, mod):
		'Los parámetros de un módulo han cambiado de valor'

		# Si la salida está vacía borrar el módulo
		# FIXME ???

		self.update()

	def update(self):
		'Actualizar todas las conexiones disponibles'

		self.plugs_out = []
		self.plugs_in = []
		for m in self.modlist:
			self.plugs_out += m.get_outputs()
			self.plugs_in += m.get_inputs()

		print("---- CONNECTIONS ----")
		for mod in self.modlist:
			print("---- {} ----".format(mod.name))
			print("Outputs")
			for out_plug in mod.outputs:
				out_plug.show()
			print("Inputs")
			for in_plug in mod.inputs:
				in_plug.show()
		print("---- END CONNECTIONS ----")

		for m in self.modlist:
			m.update_plugs(self.plugs_in, self.plugs_out)
		#print(json.dumps(self.clone(), sort_keys=True, indent=4))


	def get_all_mods(self):
		return MODS

	def get_mod_names(self, mods):
		mods_name = [c.name for c in mods]
		return mods_name

	def _new_name(self, mod_name):
		"Crea un nuevo nombre para un módulo"
		i = 1
		new_name = "{}_{:03d}".format(mod_name, i)
		names = [m.name for m in self.modlist]
		while new_name in names:
			i+=1
			new_name = "{}_{:03d}".format(mod_name, i)
		return new_name

	def add_mod(self):
		if self.w.combo_mod.currentIndex() < 0: return

		i = self.w.combo_mod.currentIndex()
		mod_class = self.all_mods[i]
		mod_name = self._new_name(mod_class.name)
		mod = mod_class(self.w, mod_name)
		mod.register_update(self.widget_update)
		self.modlist.append(mod)
		#mod.focus()
		#print("Added " + str(mod.name))

	def _get_mod_conf(self, conf, mod_name):
		for mod_conf in conf:
			if mod_conf['name'] == mod_name: return mod_conf
		return None

	def restore(self, config):
#		modlist_conf = config
#		for conf in modlist_conf:
#			mod_conf, mod_name = conf
#			mod_class = self.all_mods[i]
#
#			modlist_conf.append({mod_name:mod_conf})
#		return modlist_conf
		#TODO: Borrar todos los módulos anteriores
		for mod in self.modlist:
			if isinstance(mod, ModInput): continue
			if isinstance(mod, ModOutput): continue
			self.remove_mod(mod)

		names = [mod.name for mod in self.modlist]

		# Crear los módulos y conexiones
		for mod_conf in config:
			mod_name = mod_conf['name']
			#print(mod_name)

			# Si ya existe (Input y Output)
			if mod_name in names: continue
			# TODO: Crear módulo por nombre de clase en función
			mod_class = globals()[mod_conf['class']]
			mod = mod_class(self.w, mod_name)
			mod.register_update(self.widget_update)
			self.modlist.append(mod)

			self._set_plugs_conf(mod, mod_conf)

		# Conectarlas
		self.plugs_out = []
		self.plugs_in = []
		for m in self.modlist:
			self.plugs_out += m.get_outputs()
			self.plugs_in += m.get_inputs()

		self.plugs_out_name = [plug.name for plug in self.plugs_out]
		self.plugs_in_name = [plug.name for plug in self.plugs_in]

		for mod in self.modlist:
			# Solo conectar las entradas, las salidas se conectarán
			# automáticamente
			mod_conf = self._get_mod_conf(config, mod.name)
			conf_inputs = mod_conf['plugs']['inputs']
			for i in range(len(mod.inputs)):
				mod_input = mod.inputs[i]
				name_input, name_outputs = conf_inputs[i]
				for name in name_outputs:
					j = self.plugs_out_name.index(name)
					plug_out = self.plugs_out[j]
					mod_input.connect(plug_out)

			# Configurar individualmente cada módulo
			mod.restore(mod_conf['Mod'])

		self.update()
		self.mod_in.update()

#		for mod in self.modlist:
#			print("---- {} ----".format(mod.name))
#			print("Outputs")
#			for out_plug in mod.outputs:
#				out_plug.show()
#			print("Inputs")
#			for in_plug in mod.inputs:
#				in_plug.show()



	def _get_plugs_conf(self, mod):
		'Obtiene las conexiones de un módulo'
		conf_inputs = []
		for plug_in in mod.inputs:
			names = [plug.name for plug in plug_in.plugs]
			conf_inputs += [(plug_in.name, names)]
		conf_outputs = []
		for plug_out in mod.outputs:
			names = [plug.name for plug in plug_out.plugs]
			conf_outputs += [(plug_out.name, names)]

		return {'inputs':conf_inputs, 'outputs':conf_outputs}

	def _set_plugs_conf(self, mod, mod_conf):
		'Crea las conexiones de un módulo, sin conectarlas'
		mod.inputs = []
		mod.outputs = []

		plug_conf = mod_conf['plugs']
		conf_inputs = plug_conf['inputs']
		conf_outputs = plug_conf['outputs']

		for conf_input in conf_inputs:
			name, names = conf_input
			mod.inputs.append(PlugIn(mod, name))

		for conf_output in conf_outputs:
			name, names = conf_output
			mod.outputs.append(PlugOut(mod, name))

	def clone(self):
		modlist_conf = []
		for mod in self.modlist:
			mod_conf = {}
			mod_conf['Mod'] = mod.clone()
			mod_conf['plugs'] = self._get_plugs_conf(mod)
			mod_conf['name'] = mod.name
			mod_conf['class'] = mod.__class__.__name__
			modlist_conf.append(mod_conf)

		return modlist_conf


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

		print("Config read:")
		print(json.dumps(config, sort_keys=True, indent=4))
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


class Main(QtGui.QMainWindow):
	def __init__(self, parent = None):
		super(Main, self).__init__(parent)

		uic.loadUi('qt/mod/mainwindow.ui', self)
		self.mm = ModManager(self)
		self.conf = Config(self, self.mm)



MODS = [ModScale, ModCLAHE, ModRange, ModMorph, ModBitwise]
app = QtGui.QApplication(sys.argv)
#app.setStyle("plastique")
myWidget = Main()
myWidget.show()
app.exec_()

