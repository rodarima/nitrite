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



#class ModIO(ModGroup):
#	'Añade las entradas y salidas, y gestiona las actualizaciones'
#	def __init__(self, w, name=None, puts=(1,1), config=None):
#		if config: name = config['name']
#		ModGroup.__init__(self, w, name)
#
#		self.ready = False
#
#		if config:
#			config_inputs = config['plugs']['inputs']
#			config_outputs = config['plugs']['outputs']
#			puts = (len(config_inputs), len(config_outputs))
#			self.gui_add_io(puts)
#		else:
#			self.gui_add_io(puts)
#			self.add_io()
#			self.gui_activate()
#
#	def gui_add_io(self, io=(1,1), config=None):
#		'Añade los selectores de entradas y salidas al widget'
#		self.io_gui = {} # widgets de entrada/salida
#		self.add_gui_inputs(io[0])
#		self.add_gui_outputs(io[1])
#
#	def gui_add_inputs(self, n):
#		'Añade n entradas tipo combo al módulo'
#		self.io_gui['in'] = []
#		for i in range(n):
#			# Añadir el combo
#			widget_in = QtGui.QComboBox()
#			self.module_layout.addRow("In" + str(i), widget_in)
#			self.io_gui['in'].append(widget_in)
#
#	def gui_add_outputs(self, n):
#		'Añade n salidas tipo lineEdit al módulo'
#		self.io_gui['out'] = []
#		for i in range(n):
#			widget_out = QtGui.QLineEdit()
#			self.module_layout.addRow("Out" + str(i), widget_out)
#			self.io_gui['out'].append(wigdet_out)
#
#	def gui_update_inputs(self):
#		'Actualiza la lista de selección de los combos de entrada'
#		plugs = [plug.name for plug in self.all_outputs]
#		for i in len(self.io_gui['in']):
#			widget = self.io_gui['in'][i]
#			j = widget.currentIndex()
#			widget.clear()
#			widget.addItems(plugs)
#			widget.setCurrentIndex(j)
#
#	def gui_activate(self):
#		'''Pone el módulo activo y listo para ser usado, activando
#		las señales de las entradas y salidas, así como la función de
#		actualización'''
#		# Activar señales de entrada
#		for widget in self.io_gui['in']:
#			widget.currentIndexChanged.connect(self.gui_in_updated)
#		# Activar señales de salida
#		for widget in self.io_gui['out']:
#			widget.editingFinished.disconnect(self.gui_out_updated)
#		#TODO...
#
#	def gui_in_updated(self):
#		'Al cambiar la elección del combo de entrada, cambiar PlugIn'
#		for i in len(self.io_gui['in']):
#			widget = self.io_gui['in'][i]
#			j = widget.currentIndex()
#			plug_in = self.inputs[i]
#			plug_in.disconnect()
#			plug_in.connect(self.all_outputs[j])
#
#		self.update()
#
#	def gui_out_updated(self):
#		'Al modificar el nombre de la salida, avisar a ModManager'
#		for i in len(self.io_gui['out']):
#			widget = self.io_gui['out'][i]
#			plug_out = self.outputs[i]
#			plug_out.name = str(widget.currentText())
#
#		self.out_updated(self)
#
#	def set_out_updated(self, fun): self.out_updated = fun
#
#	def update_plugs(self, all_inputs, all_outputs):
#		'''Cuando ModManager avise de que hay nuevas entradas, actualizar
#		la información de los combos de entrada'''
#		Mod.update_plugs(self, all_inputs, all_outputs)
#		self.gui_update_inputs()
#
#	def update(self): raise NotImplemented()
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
#		d['combo_in_index'] = [c.currentIndex() for c in self.io_gui['in']]
#		d['text_out'] = str(self.text_out.text())
#		return d

#class ModTest(ModBase):
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
#class ModCircles(ModBase):
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

	def add_input(self, label, class_filter=[], optional=False):
		if label in self.inputs:
			raise Exception("Already exists")

		self.inputs[label] = self.pm.new_input(self, self.name + '_' + label)
		self.input_filter[label] = class_filter
		self.input_combo[label] = self.new_input_combo(label)
	
	def remove_input(self, label):
		if label not in self.inputs:
			raise KeyError('Input not found')

		# Borrar PlugIn
		plug_in = self.inputs.pop(label)
		self.pm.remove_input(plug_in)
		# Borrar el filtro
		self.input_filter.pop(label)
		# Borrar el combo
		self.remove_input_combo(label)
		
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
		return widget_in

	def enable_inputs(self):
		for combo in self.input_combo.values():
			combo.currentIndexChanged.connect(self.updated_input_combo)

	def updated_input_combo(self):
		'Conecta la entrada segun el valor del combo'
		combo = self.w.sender()
		output_name = str(combo.currentText())

		i = self.input_combo.values().index(combo)
		if i < 0: raise RuntimeError()
		label = self.input_line.keys()[i]
		input_plug = self.inputs[label]

		self.pm.connect_input(input_plug, output_name)
		self.update()

	def get_input(self, label): return self.inputs[label]

	def update_io(self):
		'Actualiza la lista de estradas disponibles'
		#print('ModInput {}: update_io()'.format(self.name))
		for label in self.inputs.keys():
			self.update_input_combo(label)

	def update_input_combo(self, label):
		#print('ModInput {}: update_input_combo({})'.format(self.name, label))
		plug_in = self.inputs[label]
		combo = self.input_combo[label]
		input_filter = self.input_filter[label]
		list_values = self.pm.get_outputs(input_filter)
		self.update_input_combo_values(combo, list_values)
		
	def update_input_combo_values(self, combo, values):
		"Actualiza en el combo las nuevas entradas"
		combo.currentIndexChanged.disconnect(self.update)
		i = combo.currentIndex()
		combo.clear()
		combo.addItems(values)
		combo.setCurrentIndex(i)
		combo.currentIndexChanged.connect(self.update)

	def show(self):
		print("ModInput show:")
		print(self.inputs)
		print(self.input_combo)

class ModOutput:
	'Gestiona las salidas del módulo'
	def __init__(self):
		self.outputs = {} #Indexados por el nombre de la etiqueta
		self.output_line = {}

	def add_output(self, label, class_type=None):
		if label in self.outputs:
			raise Exception("Already exists")

		self.outputs[label] = self.pm.new_output(self, self.name + '_' + label, class_type)
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
		new_name = output_line.text()

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
		
#	def gui_out_updated(self):
#		'Al modificar el nombre de la salida, avisar a ModManager'
#		for i in len(self.io_gui['out']):
#			widget = self.io_gui['out'][i]
#			plug_out = self.outputs[i]
#			plug_out.name = str(widget.currentText())
#
#		self.out_updated(self)
#

class ModBase(Mod, ModInput, ModOutput):
	def __init__(self, name, plug_manager, window):
		Mod.__init__(self, name, plug_manager)
		self.gui_add_group(window)
		ModInput.__init__(self)
		ModOutput.__init__(self)

		self.init_IO()
		self.gui_enable()

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
		self.w.scroll_layout.addWidget(self.module)
	
	def gui_enable(self):
		self.enable_inputs()
		self.enable_outputs()
		self.module.setEnabled(True)
		self.update_io()

	def show(self):
		ModInput.show(self)
		ModOutput.show(self)
		

class ModTestInput(ModBase):
	mod_name = 'Test Input'

	def init_IO(self):
		self.add_input("In0", [ImageColor])
		self.add_input("In1")

		self.add_output("Out0", ImageColor)
		self.add_output("Out1")
	
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


class ModManager:
	def __init__(self, window):
		self. w = window
		self.mods = {}

		# Añadir lista de modulos
		self.all_mods = self.get_all_mods()
		self.all_mod_names = self.get_mod_names(self.all_mods)
		self.w.combo_mod.addItems(self.all_mod_names)

		# Boton de añadir modulos
		self.w.button_add_mod.clicked.connect(self.add_mod)

		# Actualizar las salidas
		self.update_io()

	def set_plug_manager(self, pm):
		self.pm = pm

	def remove_mod(self, mod):
		#print("Del " + str(mod.name))
		self.mods.pop(mod.name)
		self.w.scroll_layout.removeWidget(mod.module)
		mod.module.setParent(None)

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

	def new_name(self, mod_name):
		"Crea un nuevo nombre para un módulo"
		i = START_INDEX
		new_name = "{}{}".format(mod_name, i)
		while new_name in self.mods:
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
		#print("Added " + str(mod.name))
		#self.pm.show()
		#mod.show()

#	def _get_mod_conf(self, conf, mod_name):
#		for mod_conf in conf:
#			if mod_conf['name'] == mod_name: return mod_conf
#		return None
#
#	def restore(self, config):
##		modlist_conf = config
##		for conf in modlist_conf:
##			mod_conf, mod_name = conf
##			mod_class = self.all_mods[i]
##
##			modlist_conf.append({mod_name:mod_conf})
##		return modlist_conf
#		#TODO: Borrar todos los módulos anteriores
#		for mod in self.modlist:
#			if isinstance(mod, ModInput): continue
#			if isinstance(mod, ModOutput): continue
#			self.remove_mod(mod)
#
#		names = [mod.name for mod in self.modlist]
#
#		# Crear los módulos y conexiones
#		for mod_conf in config:
#			mod_name = mod_conf['name']
#			#print(mod_name)
#
#			# Si ya existe (Input y Output)
#			if mod_name in names: continue
#			# TODO: Crear módulo por nombre de clase en función
#			mod_class = globals()[mod_conf['class']]
#			mod = mod_class(self.w, mod_name)
#			mod.register_update(self.widget_update)
#			self.modlist.append(mod)
#
#			self._set_plugs_conf(mod, mod_conf)
#
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
#
##		for mod in self.modlist:
##			print("---- {} ----".format(mod.name))
##			print("Outputs")
##			for out_plug in mod.outputs:
##				out_plug.show()
##			print("Inputs")
##			for in_plug in mod.inputs:
##				in_plug.show()
#
#
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
#	def clone(self):
#		modlist_conf = []
#		for mod in self.modlist:
#			mod_conf = {}
#			mod_conf['Mod'] = mod.clone()
#			mod_conf['plugs'] = self._get_plugs_conf(mod)
#			mod_conf['name'] = mod.name
#			mod_conf['class'] = mod.__class__.__name__
#			modlist_conf.append(mod_conf)
#
#		return modlist_conf


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
		self.pm = PlugManager(self.mm)
		self.mm.set_plug_manager(self.pm)
#		self.conf = Config(self, self.mm)



#MODS = [ModScale, ModCLAHE, ModRange, ModMorph, ModBitwise, ModHist2D]
MODS = [ModTestInput]
app = QtGui.QApplication(sys.argv)
#app.setStyle("plastique")
myWidget = Main()
myWidget.show()
app.exec_()

