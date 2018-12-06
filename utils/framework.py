import os 
import time
import socket 
from warnings import warn
from time import sleep
from shutil import rmtree
import platform 
import sys
import json
import datetime 
from Plugins.Engine import  XPlugins
from core.attacker import Core_Intractor 
from core.netscan import NetworkScanner
from core.__import__ import *
from utils.help import HELP
from utils.workspace import Workspace

	
try:
	from urllib2 import urlopen, URLError
	from urlparse import urlparse
except ImportError or ModuleNotFoundError:
	from urllib.parse import urlparse
	from urllib.request import urlopen, URLError
try : 
	import readline
except ModuleNotFoundError or ImportError : 
	from pyreadline import readline
else :
	pass
	#print("Module readline not available.")
	#print("Module readline Is for Auto-Completing Your Command And now its Disabled")
	#print("Try : 'pip install readline pyreadline'")			



class XFramework(Core_Intractor , NetworkScanner):
	def __init__(self) : 
		self.target = None
		self.buff_input = None
		self.buff_split_list = []
		self.master_commands = {}
		self.activator_commands = {}
		self.manual_commands = {}
		self.list_of_commands = [] 
		self.tool_name = 'X-Framework'
		self.version = '0.1'
		self.version_name = 'Dark'
		self.version_edition = 'Community Edition'
		self.version_language = 'Python'
		self.licence = 'GNU'
		self.n_jobs = 2
		self.cint = Core_Intractor(self.out)
		self.netscan = NetworkScanner()
		self.verbose = False 
		self.quiet = False 
	def __out__(self) : 
			return self.out 
	def packageinfo(self): 
		self.out(self.tool_name + ' ' + self.version + ' [' + self.version_name + ' '  + self.version_edition +  ']')
		self.out('Type "help" , "Ctrl+D" back ,"creadits" for more info.')
	def __listit__ (self) : 
		self.buff_split_list = self.buff_input.split(' ')
		self.buff_split_list = [arg.lower() for arg in self.buff_split_list if len(arg) > 0]
	def workspacer_start(self) : 
		self.currentworkspace = Workspace()
		#self.currentworkspace.create()
		self.currentworkspace.open_out_pipe()
	def workspacer_new(self):
		newworkpsace = self.get_buff('NEW WORKSPACE')
		self.currentworkspace.create (newworkpsace , 'WorkSpace')
	def workspacer_show(self):
		self.out('current workspace name : ' , self.currentworkspace.name)
		self.out('workspace folder name: ' , self.currentworkspace.wsname)
		self.out('workspace folder path : ' , self.currentworkspace.path)
		self.out('complete path : ' , self.currentworkspace.cws)
	def add_master_commands(self , command , action = None): 
		self.master_commands[command] = action
	def add_activator_commands(self , master , slave , action = None): 
		self.activator_commands[(master , slave)] = action
	def add_manual_commands(self , master , action = None): 
		self.manual_commands[master] = action	
	def all_commands(self):
		self.out(self.master_commands.keys() , self.activator_commands.keys() , self.manual_commands.keys())
	def __all_attacker_commands__(self) :
		return ([(x[1]) for x in self.activator_commands.keys() if 'run' in x] )
	def do(self) :
		#try : 
			if len(self.buff_split_list) == 1 : 
				if self.buff_split_list[0] in self.master_commands :
					self.master_commands[self.buff_split_list[0]]()
				elif self.buff_split_list[0] in self.manual_commands : 
					self.out(self.buff_split_list[0] , 'take an argument')
				else : 
					self.out("Command Not Found !")
			elif len(self.buff_split_list) == 2 : 
				if (self.buff_split_list[0] , self.buff_split_list[1]) in self.activator_commands :
					self.activator_commands[(self.buff_split_list[0] , self.buff_split_list[1])]()
				elif self.buff_split_list[0] in self.manual_commands : 
					self.manual_commands[self.buff_split_list[0]](self.buff_split_list[1])
				else :
					for wrongcommand in self.buff_split_list : 
						if wrongcommand in self.master_commands : 
							self.out('Wrong Usage of ' , wrongcommand)
						else : 
							self.out(wrongcommand , "Not Found !")



			elif len(self.buff_split_list) > 2 :
				if (self.buff_split_list[0] , self.buff_split_list[1]) in self.activator_commands :
					self.out('Wrong Usage of ' , self.buff_split_list[0] + self.buff_split_list[1])
					#self.activator_commands[(self.buff_split_list[0] , self.buff_split_list[1])]()
				else : 
					for wrongcommand in self.buff_split_list : 
						if wrongcommand in self.master_commands : 
							self.out('Wrong Usage of ' , wrongcommand)
		#except Exception as e : 
			#self.out(str(e) , method = 'ERROR')
	def get_buff(self , arg = None):
		if arg is not None : 
			return input(arg + '>>>')
		else : 	
			return input('>>>')
	def cli_completer_setup(self , commandlist): 
		self.commandline_options = commandlist
		self.commandline_current_candidates = []
	def cli_completer_search(self , text, state): 
		response = None
		if state == 0:
			original = readline.get_line_buffer()
			begin = readline.get_begidx()
			end = readline.get_endidx()
			being_completed = original[begin:end]
			words = original.split()
			if not words:
				self.commandline_current_candidates = sorted(self.commandline_options.keys())
			else:
				try:
					if begin == 0:
						# first word
						candidates = self.commandline_options.keys()
					else:
						# later word
						first = words[0]
						candidates = self.commandline_options[first]
					
					if being_completed:
						# match options with portion of input
						# being completed
						self.commandline_current_candidates = [ w for w in candidates
													if w.startswith(being_completed) ]
					else:
						# matching empty string so use all candidates
						self.commandline_current_candidates = candidates
					
				except KeyError or IndexError as err:
					self.commandline_current_candidates = []
		try:
			response = self.commandline_current_candidates[state]
		except IndexError as e:
			response = None
		return response
	def cli_loop(self) :
		while True : 
			try :
				readline.set_completer(self.cli_completer_search)
				readline.parse_and_bind("tab: complete")
				self.buff_input = self.get_buff('XFI') 
				self.currentworkspace.logit(self.buff_input , 'in')
				self.__listit__()
				self.do()
			except KeyboardInterrupt : 
				self.Exit()	
			except EOFError : 
				self.out('ctrl-d : back or exiting Sub-Program')
	def set_target_wizard(self) :
		self.target = self.get_buff('TARGET')
	def show_target(self) : 
		try : 
			if self.target is None : 
				self.out('TARGET : Has Not Been Set ! ')
			else : 	
				self.out('TARGET : ' , self.target)
		except : 
			self.out('The Target Has Not Been Set ! ')
	def set_n_jobs(self , jobs) : 
		self.n_jobs = int(jobs)
	def set_target(self , target) :
		if len(target) < 2  : 
			self.target = None 
		else : 
			self.target = target
	def netstatus(self): 
		try:
			response=urlopen('https://google.com',timeout=1)
			self.connected = True
		except Exception as e: 
			#self.out("DEBUG : " , e)
			self.connected =  False
	def setup_initials(self) :

		self.platform = platform.system()
		self.python_version = platform.python_version()[:1]
		self.host_name = socket.gethostbyaddr(socket.gethostbyname(socket.gethostname()))[0]
		self.host_ip =  socket.gethostbyaddr(socket.gethostbyname(socket.gethostname()))[2]
		self.netstatus()
	def show_all(self) :
		self.out('Version : ' , self.version)
		self.out('Version Name : ' , self.version_name)
		self.out('Version Edition : ' , self.version_edition)
		self.out('Written in : ' , self.version_language)
		self.out('Current Platform : ' , self.platform)
		self.out('Current Python Version : ' , self.python_version)
		self.out('Current Host Name : ' , self.host_name)
		self.out('Current Ip Address : ' , self.host_ip)
		self.show_target()
		self.out('Internet Status : ' , self.connected)
		self.out('Current Threads : ' + str(self.n_jobs))
		self.out('Current workspace name : ' , self.currentworkspace.name)
		self.out('Current Workspace Parrent folder name: ' , self.currentworkspace.wsname)
		self.out('Current Workspace folder path : ' , self.currentworkspace.path)
		self.out('Current Workspace Complete path : ' , self.currentworkspace.cws)
	def clearPage (self):
		try : 
			if self.platform == 'Linux' : 
				os.system("clear")
			elif self.platform == 'Windows' :
				os.system("cls")
		except:
			for i in range(50):
				print("\n")
	def syscommandline(self) : 
		try : 
			self.out('Exit : "back" , "Ctrl+d" ')
			BASH_CM = self.get_buff('SYSTEM COMMAND PROMPT')
			while BASH_CM not in ['back' , 'bash' , 'exit'] :
				PowerExecute.Os(BASH_CM)
				BASH_CM = self.get_buff('SYSTEM COMMAND PROMPT')
		except KeyboardInterrupt: 
			self.out('\n')
			pass
	def pythoncommand(self):
		try : 
			PowerExecute.Os('python')
		except KeyboardInterrupt: 
			self.out('\n')
			pass		
	def Launcher(self):
		self.clearPage()
		self.setup_initials()
		self.workspacer_start()
		self.packageinfo()
		self.cli_loop()
	def out(self , arg1 , arg2 = None , arg3 = None , arg4 = None , arg5 = None , method = 'OUT'):
		#Temp , In future : it will be replaced with *args ! 
		if arg5 is not None : 
			self.currentworkspace.logit(str(arg1) + str(arg2) + str(arg3) +  str(arg4) + str(arg5) , method)
			datetimestr = str(datetime.datetime.strftime(datetime.datetime.now(), '%H:%M:%S'))
			print("[" + datetimestr + "] " + str(arg1) , str(arg2) , str(arg3) , str(arg4) , str(arg5))
		elif arg4 is not None : 
			self.currentworkspace.logit(str(arg1) + str(arg2) + str(arg3) +  str(arg4) , method)		
			datetimestr = str(datetime.datetime.strftime(datetime.datetime.now(), '%H:%M:%S'))
			print("[" + datetimestr + "] " + str(arg1) , str(arg2) , str(arg3) , str(arg4))
		elif arg3 is not None : 
			self.currentworkspace.logit(str(arg1) + str(arg2) + str(arg3), method)
			datetimestr = str(datetime.datetime.strftime(datetime.datetime.now(), '%H:%M:%S'))
			print("[" + datetimestr + "] " + str(arg1) , str(arg2) , str(arg3))
		elif arg2 is not None  : 
			self.currentworkspace.logit(str(arg1) + str(arg2) , method)
			datetimestr = str(datetime.datetime.strftime(datetime.datetime.now(), '%H:%M:%S'))
			print("[" + datetimestr + "] " + str(arg1) , str(arg2))
		else : 
			self.currentworkspace.logit(str(arg1), method)
			datetimestr = str(datetime.datetime.strftime(datetime.datetime.now(), '%H:%M:%S'))
			print("[" + datetimestr + "] " + str(arg1))	

	def core_attacker(self , phases= None ) :
			if self.target is None : 
				self.set_target_wizard()
			else :
				self.cint.set_target(self.target)
			impt = input("phases >>")
			self.cint.set_phases(impt)
			if self.verbose : 
				self.cint.set_verbos()
			if self.quiet : 
				self.cint.set_batch_mode()
			self.cint.fast_run()		
	def net_attacker(self) :
			if self.target is None : 
				self.set_target_wizard()
			else :
				self.cint.set_target(self.target)
			impt = input("phases >>")
			self.netscan.set_target(self.target)
			self.netscan.run_networkscanner()
			choise = self.get_buff("Do You Like to Run Standard Tests on Open Ports ? [y/n] ?") 
			if 'y' in choise.lower() : 
 				self.netscan.run_portvulnscanner()
	def stage_run(self , Phase) :
 		if self.target is None :
 			self.set_target_wizard()
 			self.cint.stage_run(self.target , Phase)
 		else : 
  			self.cint.stage_run(self.target , Phase)			
	def Swich_Verbose (self) : 
		if self.verbose is True : 
			self.out('Verbose Mode is' , self.verbose)
			choise = self.get_buff('Do You Wish To Turn It Off ? [y/n]' )
			if 'y' in choise.lower() :
				self.verbose = False 
		elif self.verbose is False : 
			self.out('Verbose Mode is' , self.verbose)
			choise = self.get_buff('Do You Wish To Turn It On ? [y/n]' )
			if 'y' in choise.lower() :
				self.verbose = True 
	def Swich_Quiet(self) : 
		if self.quiet is True : 
			self.out('Quiet Mode is' , self.quiet)
			choise = self.get_buff('Do You Wish To Turn It Off ? [y/n]' )
			if 'y' in choise.lower() :
				self.quiet = False 
				self.cint.verbose = True
				self.cint.set_batch_mode = False
		elif self.quiet is False : 
			self.out('Quiet Mode is' , self.quiet)
			choise = self.get_buff('Do You Wish To Turn It On ? [y/n]' )
			if 'y' in choise.lower() :
				self.quiet = True 
				self.cint.verbose = False
				self.cint.set_batch_mode = True
	def Exit(self):
		self.out('Exiting')
		if os.path.isdir("__pycache__") == True:
			try : 
				rmtree(path = "__pycache__" , ignore_errors=True)
				rmtree(path = os.path.join('core',"__pycache__") , ignore_errors=True)
				rmtree(path = os.path.join('utils',"__pycache__") , ignore_errors=True)
				rmtree(path = os.path.join('Plugins',"__pycache__") , ignore_errors=True)
			except Exception as e : 
				self.out(e , method = 'ERROR')
		self.currentworkspace.close_out_pip()
		quit()
	def Restart(self):
		if 'Linux' in self.platform : 
			os.execv(sys.executable, ['python3'] + sys.argv)
		else : 
			os.execv(sys.executable, ['python'] + sys.argv)


class Core_Intractor_handler(Core_Intractor):
	def __init__ (self , output_moderator) : 
		self.handle = Core_Intractor(output_moderator)
	def Process(self , Phase , Verbose = True) :
		tar = input('TARGET >>')
		self.handle.set_target(tar)
		if Verbose : 
			self.handle.set_verbos()
		self.handle.set_phases(Phase)
		self.handle.normal_run()
	def NONE(self): 
		self.Process('1')	
	def GOLISMERO(self): 
		self.Process('2')	
	def NONE(self): 
		self.Process('3')	
	def NONE(self): 
		self.Process('4')	
	def NONE(self): 
		self.Process('5')	
	def NONE(self): 
		self.Process('6')	
	def SQLI_SCAN_MINI(self): 
		self.Process('7')	
	def CMSSCAN(self): 
		self.Process('8')
	def FUZZABLE_CRAWLER_PHOTON_NEW(self): 
		self.Process('9')
	def SQLIV(self): 
		self.Process('10')	
	def SQLMAP_ENUM(self): 
		self.Process('11')
	def SQLMAP_DUMPER(self): 
		self.Process('12')
	def TEMPLATE_INJECTION(self) :
		self.Process('13')
	def DROOP_DRUP(self) :				
		self.Process('14')
	def WPSCAN(self) :				
		self.Process('15')
	def WPSEKU(self) :				
		self.Process('16')
	def DROOP_JOOMLA(self) :				
		self.Process('17')
	def DROOP_SILVER(self) :				
		self.Process('18')
	def NONE(self) :				
		self.Process('19')
	def XSS_SCAN_MINI(self) :				
		self.Process('20')
	def WAF(self) :				
		self.Process('21')
	def LFI(self) :				
		self.Process('22')
	def DFUC(self) :				
		self.Process('23')
	def CRAWLER_PHOTON_CORE_MODIFIED(self) :				
		self.Process('24')
	def CLICK_JACK(self) :				
		self.Process('25')
	def BANNER_GRABBER(self) :				
		self.Process('26')
	def FAST_DEEPCRAWL(self) :				
		self.Process('27')
#	def WAF(self) :				
#		self.Process('14')
#	def WAF(self) :				
#		self.Process('14')