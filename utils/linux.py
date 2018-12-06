import os , time 
class linux_commands : 
	def __init__(self , moderator): 
		self.mod = moderator
	def Monitor_Mode(self):
		try : 
			buff = os.system("ifconfig -s")
			self.mod.out(buff)
			interface = self.mod.get_buff("Choose the interface for changing to MONITOR mode : >>>")
			os.system("ifconfig" + " " + interface + " " + "down")
			time.sleep(3)	
			os.system("iwconfig" + " " + interface + " " + " mode monitor ")
			os.system("ifconfig" + " " + interface + " " + "up")
		except Exception as e: 
			self.mod.out(e , method = 'ERROR')
			pass		
	def Macchanger(self):
		try : 
			buff = os.system("ifconfig -s")
			self.mod.out(buff)
			interface = self.mod.get_buff("Choose the interface for changing the MAC adress : >>>")
			os.system("macchanger -r" + " " + interface)
		except Exception as e: 
			self.mod.out(e , method = 'ERROR')
			pass		 
	
