from Plugins.plugins import Plugins
import os 
from Plugins.__import__ import *

class XPlugins(): 
	def __init__(self, config_file = Plugins , Target = None ,Debug = True) : 
		self.config = config_file
		self.target = Target
		self.debug = Debug
		self.plugin_list = []
		for plug in self.config : 
			self.plugin_list.append(plug)
	def List(self) : 
		print('Plugin List : ')
		for plug in self.config.keys() : 
			print('\t>',plug )
		#if self.debug : 
			#print(self.config[plug]['name'])
			#print(self.config[plug]['plugin_type'])
			#print(self.config[plug]['parrentfolder'])
			#print(self.config[plug]['subfolder'])
			#print(self.config[plug]['filename'])
			#print(self.config[plug]['pre-fix'])
			#print(self.config[plug]['mandatories'])
			#print(self.config[plug]['command'])
	def __list__(self) : 
		allplugins = [plug for plug in self.config.keys()]
		return allplugins
	def __help__ (self) : 
		for plug in self.config.keys() : 
			print(">",plug )
			print(">"*5,self.config[plug]['plugin_type'],":",self.config[plug]['name'])
	def __obj__(self) : 
			return self.config
	def build(self , plugin_name , *args) : 
		try : 
			if self.config[plugin_name]['pre-fix'] is 'path' : 
				command = os.path.join(self.config[plugin_name]['parrentfolder'] , self.config[plugin_name]['subfolder'] , self.config[plugin_name]['filename'])
			elif self.config[plugin_name]['pre-fix'] is './' : 
				command = os.path.join(self.config[plugin_name]['parrentfolder'] , self.config[plugin_name]['subfolder'] , self.config[plugin_name]['filename'])
			else : 
				command = self.config[plugin_name]['pre-fix']
				command += ' '
				command += os.path.join(self.config[plugin_name]['parrentfolder'] , self.config[plugin_name]['subfolder'] , self.config[plugin_name]['filename'])
			for arg in self.config[plugin_name]['mandatories'] :
				choise = input ('set ' + arg + '>>>')
				ccommand = self.config[plugin_name]['command']
				ccommand = ccommand.replace(arg , choise)
			return (command + ' ' + ccommand)
		except KeyError : 
			return None
	def load(self) : 
		tmp  = test.build(choise)
		if tmp is not None : 
			return test.build(choise)
		else : 
			print('Tmp Not Found!')
	def run(self , plg) : 
		plg = plg.split(' ')
		for item in plg : 
			if item in self.__list__() : 
				tmp = self.build(item)
				if tmp is not None : 
					os.system(tmp) 
			else : 
				print(item ,' Not Found')
	def pluger(self):
		self.List()
		choise = input('Enter Plug Name >')
		#os.system(self.build(choise))
		PowerExecute(["PLUGIN" + ' ' +  choise  + " " , self.build(choise) , [''], 'all']) 
	def run(self, plugin) : 
		try : 
			r3dexecute([str(self.build(plugin))] , [self.config[plugin]['name']])
		except KeyboardInterrupt : 
			print("Exiting")



'''

test = XPlugins(config_file )
#test.List()
choise = input('Enter Plug Name >')
test.build(choise)
'''