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

	def connections(self):
		return len(self.plugs)

	def connected(self, plug=None):
		if plug: return plug in self.plugs
		else: return self.plugs != []

	def _check_plug_out(self, plug_out):
		if not isinstance(plug_out, PlugOut):
			raise TypeError("PlugOut expected")

	def _check_plug_in(self, plug_in):
		if not isinstance(plug_in, PlugIn):
			raise TypeError("PlugIn expected")


class PlugIn(Plug):
	def __init__(self, mod, name):
		Plug.__init__(self, mod, name)
		self.updating = False

	def connect(self, plug_out):
		self._check_plug_out(plug_out)

		if self.connected(): self.disconnect()
		plug_out._connect(self)
		self._connect(plug_out)

	def _connect(self, plug_out):
		if self.connected(): raise RuntimeError()
		self.plugs = [plug_out]
		self.data = plug_out.data

	def disconnect(self):
		if not self.connected(): return

		self.plugs[0]._disconnect(self)
		self._disconnect()

	def _disconnect(self):
		if not self.connected(): raise RuntimeError()
		self.plugs = []

	def update(self):
#		print('PlugIn {} updating mod {}'.format(self.name, self.mod.name))
		if self.connected():
			self.data = self.plugs[0].data
		if self.updating: return
		self.updating = True
		self.mod.update()
		self.updating = False

	def show(self):
		if self.connected():
			print("{} -> {}".format(self.plugs[0].name, self.name))
		else:
			print("None -> {}".format(self.name))

	def destroy(self):
		if self.connected(): self.disconnect()

class PlugOut(Plug):
	def __init__(self, mod, name, plug_type=None):
		Plug.__init__(self, mod, name)
		self.plug_type = plug_type

	def connect(self, plug_in):
		self._check_plug_in(plug_in)
		if self.connected(plug_in): return

		plug_in._connect(self)
		self._connect(plug_in)

	def _connect(self, plug_in):
		if self.connected(plug_in): raise RuntimeError()
		self.plugs.append(plug_in)

	def disconnect(self, plug_in):
		self._check_plug_in(plug_in)
		if not self.connected(plug_in): return

		plug_in._disconnect()
		self._disconnect(plug_in)

	def _disconnect(self, plug_in):
		if not self.connected(plug_in): raise RuntimeError()
		self.plugs.remove(plug_in)

	def update(self):
#		print('PlugOut {} updating mod {}'.format(self.name, self.mod.name))
		for plug in self.plugs:
			plug.update()

	def show(self):
		plugs = [plug.name for plug in self.plugs]
		print("{} -> {}".format(self.name, plugs))

	def destroy(self):
		if self.connected():
			for plug in plugs:
				self.disconnect(plug)

class GPlugIn(PlugIn):
	pass

class GPlugOut(PlugOut):
	pass

class PlugManager(object):

	def __init__(self, mod_manager):
		self.mod_manager = mod_manager
		self.inputs = {}
		self.outputs = {}

	def new_input(self, mod, name):
		'Crea una conexión de entrada con un nombre nuevo'
		if name in self.inputs:
			raise RuntimeError('Nombre de entrada duplicado')

		plug_in = GPlugIn(mod, name)
		self.inputs[name] = plug_in
		#print('PlugManager: new input "{}" at {}'.format(name, plug_in))

		self.mod_manager.update_io()
		return plug_in

	def new_output(self, mod, name, plug_type):
		'Crea una conexión de salida con un nombre nuevo'
		if name in self.outputs:
			raise RuntimeError('Nombre de salida duplicado')

		plug_out = GPlugOut(mod, name, plug_type)
		self.outputs[name] = plug_out

		self.mod_manager.update_io()
		return plug_out

	def new_name(self, name, names):
		"Crea un nuevo nombre que no exista"
		i = 0
		name = "{}{}".format(name, i)
		while name in names:
			i += 1
			name = "{}{}".format(name, i)
		return name

	def remove_input(self, plug_in):
		'Quita una conexión de entrada'
		name = plug_in.name
		self.inputs.pop(name)
		plug_in.destroy()

		self.mod_manager.update_io()

	def remove_output(self, plug_out):
		'Quita una conexión de salida'
		name = plug_out.name
		self.outputs.pop(name)
		plug_out.destroy()

		self.mod_manager.update_io()

	def connect_name(self, plug, name):
		'Conecta una conexión con otra a traves del nombre'
		if isinstance(plug, PlugIn):
			plug_out = self.outputs[name]
			plug.connect(plug_out)

		elif isinstance(plug, PlugOut):
			plug_in = self.inputs[name]
			plug.connect(plug_in)

		else: raise RuntimeError()

	def filter_self(self, mod, plugs):
		return [plug.name for plug in self.plugs if plug.mod != mod]
	
	def get_outputs(self, mod, filter_list):
		'Obtiene una lista de las salidas del tipo filtrado'
		# Si no hay filtro, devolver todas
		if filter_list == []:
			return self.filter_self(self.outputs.values())
		# Si no, fltrar por el tipo
		input_list = []
		for name in self.outputs:
			plug_type = self.outputs[name].plug_type
			if plug_type == None: continue
			if self.outputs[name].mod == mod: continue
			for class_filter in filter_list:
				if issubclass(plug_type, class_filter):
					input_list.append(name)
					break

		return input_list

	def get_input(self, name):
		return self.inputs[name]

	def get_output(self, name):
		return self.outputs[name]

	def show(self):
		print("")
		print("---PlugManager: Inputs")
		for name in self.inputs:
			plug_in = self.inputs[name]
			print(name)
			plug_in.show()

		print("---PlugManager: Outputs")
		for name in self.outputs:
			plug_out = self.outputs[name]
			print(name)
			plug_out.show()
		print("")
	
	def update_output(self, output, new_name):
		'''Se encarga de llevar a cabo una actualización en
		el nombre de una salida'''

		self.outputs.pop(output.name)

		if new_name in self.outputs.keys():
			old_name = new_name
			new_name = self.new_name(new_name, self.outputs.keys())
#			print("ModManager: update_output nuevo nombre {} -> {}".format(old_name, new_name))

		output.name = new_name
		self.outputs[new_name] = output

		self.mod_manager.update_io()
		return output

	def connect_input(self, input_plug, output_name):
		'''Conecta una entrada con la correspondiente salida, tras haber
		cambiado la selección del combo'''

		output = self.outputs[output_name]
		# Automáticamente se desconecta
		input_plug.connect(output)


	def clone(self):
		# Clona el estado de las conexiones
		config = {}
		conf_inputs = {} # Las conexiones no necesitan orden
		for plug_in in self.inputs.values():
			d = {}
			d['mod'] = plug_in.mod.name
			d['plugs'] = [plug.name for plug in plug_in.plugs]
			conf_inputs[plug_in.name] = d

		config['inputs'] = conf_inputs

		conf_outputs = {}
		for plug_out in self.outputs.values():
			d = {}
			d['mod'] = plug_out.mod.name
			if plug_out.plug_type != None:
				d['type'] = plug_out.plug_type.__name__
			else:
				d['type'] = None
			d['plugs'] = [plug.name for plug in plug_out.plugs]
			conf_outputs[plug_out.name] = d

		config['outputs'] = conf_outputs

		return config

	def restore(self, config):
		# Restaura el estado de las conexiones SIN asignar
		# los módulos
		
		# Borrar todas las conexiones si existen
		self.inputs = {}
		self.outputs = {}


		# Crear conexiones sin conectar aún
		conf_inputs = config['inputs']
		for name in conf_inputs.keys():
			d = conf_inputs[name]
			mod = self.mod_manager.get_mod(d['mod'])
			self.inputs[name] = GPlugIn(mod, name)

		conf_outputs = config['outputs']
		for name in conf_outputs.keys():
			d = conf_outputs[name]
			mod = self.mod_manager.get_mod(d['mod'])
			plug_type = None
			if d['type'] != None: plug_type = globals()[d['type']]
			self.outputs[name] = GPlugOut(mod, name, plug_type)

		# Conecta SOLO las conexiones de entrada, de forma
		# que las de salida se autoconectan

		conf_inputs = config['inputs']
		for name in conf_inputs.keys():
			plugs = conf_inputs[name]['plugs']
			for plug_name in plugs:
				self.inputs[name].connect(self.outputs[plug_name])



