import os 
from utils.io import io_manage

class Workspace :
	def __init__(self , ws_name = 'WorkSpace' , name = 'default' , path = os.getcwd()) : 
		self.name = name
		self.wsname = ws_name
		self.path = path 
		self.cws = os.path.join(self.path,self.wsname,self.name)
		if not os.path.isdir(self.path):
			os.makedirs(self.path)
		if not os.path.isdir(self.cws) :
			os.makedirs(self.cws)
	def create(self , wsname , wsfoldername  , path = os.getcwd()):
		wsfoldername = self.wsname
		self.name = wsname
		self.wsname = wsfoldername
		self.path = path
		self.cws = os.path.join(self.path,self.wsname,self.name)
		#print(self.cws)
		if not os.path.isdir(self.path):
			os.makedirs(self.path)
			print (self.path , 'CREATED !')
		#else : 
		#	print (self.path , 'Already Exist !')
		if not os.path.isdir(self.cws) :
			print (self.cws , 'CREATED !')
			os.makedirs(self.cws)
		else : 
			print (self.cws , 'Already Exist !')
	def open_out_pipe(self) :
		self.results = io_manage(file_name = 'result.txt' ,  path = self.cws)
		self.log = io_manage(file_name = 'history.txt' ,  path = self.cws)
		self.results.open()
		self.log.open()
	def close_out_pip(self) : 
		self.results.close()
		self.log.close()
	def outit(self , text) : 
		self.resutls.writeline(text)
	def logit(self, text , pipe = None):
		self.log.log(text , pipe)
	def outitandlogit (self , text , pipe = None) : 
		self.resutls.writeline(text)
		self.log.writeline(text , pipe)
	def docs():
		print ('''
		test = workspace()
		test.create('helloworld!')
		test.outconfig()
		''')

