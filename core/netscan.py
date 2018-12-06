import shlex , sys , os
from time import sleep
from nmap import PortScanner
from core.__import__ import *
'''
try : 
	from core.exec import PowerExecute
	from core.Graphics import COLOR
except : 
	from exec import PowerExecute
	from Graphics import COLOR
'''
class NetworkScanner(PortScanner): 
	def __init__(self) : 
		self.ports = []
		self.network_speed = '4'
		self.nmap_args = '-sV' 
		self.ports_name = []	
		self.port_of_intrest = []
		self.protocols = []
		self.products = []
		self.flags = []
		self.results = []
		self.service_detected = []
		self.service_identified = []  
		self.unknown_ports = list()
		self.time_frame = '25'
		self.Web_Port = False 
		self.nm = PortScanner()
	def set_target(self , target) : 
		self.target = target
		self.verbos = False
	def run_networkscanner(self):
		print(COLOR.INF ,  "NMAP Port/Service/Version Scan Started" , COLOR.END)
		#spinner.start()
		args = '-T'+ self.network_speed + " " + self.nmap_args
		self.nm.scan(self.target , arguments=args)
		for host in self.nm.all_hosts():
			self.hosts =  self.nm[host].hostname()
			for Protocol in self.nm[host].all_protocols() : 
				self.protocols.append(Protocol)
				for Port in self.nm[host][Protocol].keys(): 
					#print(Port , "is Open")
					self.ports.append(Port)
					self.ports_name.append(str(self.nm[host][Protocol][Port]['name'].lower()))		
					self.products.append(self.nm[host][Protocol][Port]['product'])
					self.results.append([Port , self.nm[host][Protocol][Port]['name'] , self.nm[host][Protocol][Port]['product'] , self.nm[host][Protocol][Port]['version']])
					if (self.nm[host][Protocol][Port]['product'] != '') :
						if (self.nm[host][Protocol][Port]['version'] != ''): 
							self.service_identified.append([self.nm[host][Protocol][Port]['product'] , self.nm[host][Protocol][Port]['version']])
						else : 
							self.service_detected.append([self.nm[host][Protocol][Port]['product']])
		#spinner.stop()
		if len(self.service_detected) > 0 : 
			print(COLOR.GRE , "FOLLOWING SERVICE DETECTED WITHOUT VERSION" , COLOR.END)
			print(COLOR.RED , self.service_detected, COLOR.END)
		if len(self.service_identified) > 0 : 
			print(COLOR.GRE , "FOLLOWING SERVICE DETECTED WITH VERSION :D" , COLOR.END)
			print(COLOR.RED ,self.service_identified, COLOR.END)
		if self.verbos is True : 
			print('[VERBOS] [PROTOCOLS]' , self.protocols)
			print('[VERBOS] [PORT NAMES / PORT NUMBER] ' , (self.ports_name , self.ports))
			print('[VERBOS] [PRODUCTS]' , self.products)
			print('[VERBOS] [ALL RESULTS]' ,self.results)

	def run_portvulnscanner(self , Target = None ,ports = None ):
		if ports is None : 
			try :
				ports = self.ports
			except :
				pass 
		for Port in ports: 
			if   Port in [21]:
				print(COLOR.YEL , "[NMAP] Port Idetified As" , Port , COLOR.END)
			elif Port in [22]:
				print(COLOR.INF , "Port Idetified As" , Port , COLOR.END)
				self.Port_ssh(Port , Target)
			elif Port in [23]:
				print(COLOR.INF , "Port Idetified As" , Port , COLOR.END)
			elif Port in [25] :
				print(COLOR.INF , "Port Idetified As" , Port , COLOR.END)
			elif Port in [53] :
				print(COLOR.INF , "Port Idetified As" , Port , COLOR.END)
			elif Port in [143]:
				print(COLOR.INF , "Port Idetified As" , Port , COLOR.END)
			elif Port in [443]:
				print(COLOR.YEL , "[NMAP] Port Idetified As" , Port , COLOR.END)
				self.Port_ssl(Port , Target)
				self.WebPort = True
			elif Port in [135  , 137 , 139 , 445]:
				print(COLOR.YEL , "[NMAP] Port Idetified As" , Port , COLOR.END)
				Port_smb(Port , Target)
			else :
				if Port in [80 , 8080 , 8081 , 8081]:
					print(COLOR.YEL , "[NMAP] Port Idetified As" , Port , COLOR.END)
					self.WebPort = True 
					self.Port_web(Port)
				else : 
					self.unknown_ports.append(Port)
					print(COLOR.RED , "[NMAP] Port Idetified As" , Port , COLOR.END)
	def Port_ssh(self , Port) : 
		pass	
	def Port_web(self , port , target = None) : 
		port_arg = '-p' + str(port)
		if target is None : 
			target = self.target
		PowerExecute(["Nmap Script Apache Axis2"
		,'nmap ' + port_arg + ' --script http-axis2-dir-traversal -Pn' + " " + target,
		['credentials found'] , 'in'])
		PowerExecute(["Nmap Script File Upload Exploiter"
		,'nnmap ' + port_arg +' --script http-fileupload-exploiter.nse -Pn' + " " + target,
		['Successfully'] , 'in'])	
	def Port_ssl(self , port , target = None) :
		port_arg = '-p' + str(port)
		if target is None : 
			target = self.target			
		' + " " + self.time_frame + " " + '
		PowerExecute(["Nmap Script Heartbleed"
		,'nmap -v' + " " + port_arg + " " + '--script ssl-heartbleed --script-timeout ' + " " + self.time_frame + " " + '-Pn' + " " + target, ['VULNERABLE'], 'in'] ) 
		
		PowerExecute(["Nmap Script Poodle"
		, 'nmap -v' + " " + port_arg + " " + '--script ssl-poodle --script-timeout ' + " " + self.time_frame + " " + '-Pn'  + " " + target, ['VULNERABLE'], 'in'] )
		
		PowerExecute(["Nmap Script ciphers"
		, 'nmap -v' + " " + port_arg + " " + '--script ssl-poodle --script ssl-enum-ciphers ' + " " + self.time_frame + " " + '-Pn'  + " " + target , ['VULNERABLE'], 'in'] )

		PowerExecute(["Nmap Script ccs-injection"
		, 'nmap -v' + " " + port_arg + " " + '--script ssl-ccs-injection --script-timeout ' + " " + self.time_frame + " " + '-Pn' + ' ' + target , ['VULNERABLE'], 'in'] )

		PowerExecute(["map Script Diffie-Hellman parameter detection"
		, 'nmap -v' + " " + port_arg + " " + '--script ssl-dh-params --script-timeout ' + " " + self.time_frame + " " + '-Pn' + ' ' + target , ['VULNERABLE'] , 'in'])
	def Port_smb(self , port , target = None) : 
		port_arg = '-p' + str(port)
		PowerExecute(["Nmap Script http-asp.net-debug"
		,'nmap ' + " " + port_arg + " " + ' --script http-aspnet-debug --script-timeout ' + " " + self.time_frame + " " + ' -T4 -Pn' + " " + target,
		['enabled'] , 'in'])

		PowerExecute(["Nmap Script stuxnet-detect"
		,'nmap ' + " " + port_arg + " " + ' --script stuxnet-detect --script-timeout ' + " " + self.time_frame + " " + ' -Pn' + " " + target,
		['INFECTED'] , 'in'] )

