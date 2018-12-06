import os 
from datetime import datetime
import sys
class io_manage : 
	def __init__(self , file_name='out.txt' , path = os.getcwd()) : 
		self.name = file_name
		self.path = path
		self.cfd = os.path.join(self.path  , self.name)
		if path is not os.getcwd() :
			if not os.path.isdir(self.path):
				os.makedirs(self.path)
	def open(self):
		if not os.path.isfile(self.cfd) :
			self.f = open(self.cfd , "w")
			sys.stderr = self.f
		else : 
			#warn('Out Put File Already Exist')
			self.f = open(self.cfd , 'a+')
			#print('')
			#print(self.cfd)
	def writeline(self , content ): 
		content = content + '\n'
		self.f.write(content )
		self.f.flush()
	def log(self , content, std = '') : 
		if std == '' :
			std = 'UNKNOWN'
		else : 
			formated_content = '[' + str(datetime.now()) +']' + '\t' + '[' + std + ']' + '\t' + content + '\n'
			self.f.write(formated_content)
			self.f.flush()
			
	def close(self):
		self.f.close()
	def docs() : 
		print(
		'''
		#Docs : 
		# workstation_path = os.path.join("work" , 'default')
		# test = workspace.io_manage(file_name = 'results.txt' , path = workstation_path)
		# test.open()
		# test.writeline('helloworld!')
		# test.close()
				'''
		)
