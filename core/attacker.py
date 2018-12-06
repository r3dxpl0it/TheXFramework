from time import sleep
from multiprocessing import Pool
import  os , sys
import requests
import time
import json
from urllib.request import urlopen
import socket 
from sys import argv, exit
from core.__import__ import *
from core.config import *
from core.netscan import NetworkScanner
from core.lib.dsuc import xploit , r3dxtractor , fuzzable_extract
from core.lib.golismero import golismero_scan
from core.lib.lfi import lfi_scanner
from core.lib.waf_stress import waf_stress_scanner
from core.lib.fuzzpylib import *
from core.lib.ssh_bruteforce import sshbrute 
from core.lib.shellshock import shellshock_scanner 


class Attacker : 
	def __init__(self , output_moderator , target = '' , phases = []) :
		self.target = target
		self.target_tmp = []
		self.available_phases = [x for x in range (1 , 27)]
		self.requested_phases = [ph for ph in phases if ph in self.available_phases]
		self.n_jobs = 16
		self.verbos = False
		self.batch_mode = False
		self.out = output_moderator
		self.debug = False
		self.phase_action = {
		1 : self.Phase1, 
		2 : self.golismero_vuln_scan , #GOLISMERO Scan
		3 : self.waf_detector ,  #Waflulz
		4 : self.alt_vuln_scanner_2 , 
		5 : self.alt_vuln_scanner_3 , 
		6 : self.CmsInvestigator , #Cms Id(cmseek) + Scan supported ( wp/drupal/joomla/silver)
		7 : self.check_sqli_0 , #Small SQLi Scanner (DSSS)
		8 : self.xsspy , 
		9 : self.Fuzzable_Crawler , #massive Sql-injection automated check
		10: self.check_sqli_1 , #Sqliv Injection Test 
		11: self.check_sqli_2 , #Sqlmap Injection Test 
		12: self.sqli_dumper_sqlmap, #Sqlmap Dumper
		13: self.check_tmp_injection , #tplmap Server Side Template Injection scanner 
		14: self.Drupal_Scanner , #droopscan for drupal
		15: self.WP_Scanner_1 , #wpscan for wp 
		16: self.WP_Scanner_2 ,#WPSEKU for wp 
		17: self.Joomla_Scanner_1 , #droopscan for joomla 
		18: self.SS_Scanner , #droopscan for silverstripe
		19: self.xssstrike , 
		20: self.check_xss_0 ,
		21: self.web_application_firewall , 
		22: self.Lfi_scan ,
		23: self.Fuzzable_Crawler_fast , 
		24: self.Fuzzable_Crawler_photon_old , 
		25: self.clickjacking_scanner  , 
		26: self.banner_grabber ,
		27: self.Fuzzable_DeepCrawler_fast , 
		28: self.sshbruter , 
		29: self.shellshock , 
		30: self.extrabanner , 
		31: self.racoon_scan
		}
		self.fuzzable_links = []
		self.xss_mini_vuln_links = []
		self.sqli_mini_vuln_links = []
	#Properties and Functions 

	def set_target(self , target) : 
		self.target = target
		#log
	def set_phases(self , Phases) :
		try : 
			if type (Phases) is str : 
				self.requested_phases = self.phase_formater(Phases)
				if self.debug : 
					self.out	("[DEBUG] Running Tool Number" , self.requested_phases)
			elif  type (Phases) is list :
				if self.debug : 
					self.out	("[DEBUG] Running Tool Number" , Phases)
				self.requested_phases = Phases
			else : 
				self.out	('[DEBUG] Wrong Format! '  , method = 'Error')
		except Exception as e : 
			self.out	 ('[DEBUG] Wrong Format! ' , method = 'Error')
	def phase_formater(self , Phases) :
		buff = Phases.split(',')
		ranger = [foo for foo in buff if '-' in foo]
		buff = [int(foo) for foo in buff if '-' not in foo]
		buff2 = []
		if len(ranger) > 0:
			for i in range(0 , len(ranger) , 1) : 
				temp_buff = ranger[i]
				temp_buff = temp_buff.split('-')
				temp_buff = [int(foo) for foo in temp_buff]
				[buff2.append(foo) for foo in range(temp_buff[0] , temp_buff[1])]
				buff = buff2 + buff
				buff = sorted(buff)
			return (buff)
		elif len(ranger) == 0 : 
			return (buff)
	def runer_managment(self , phase_to_run) : 
		#for ph in phase_to_run : 
		self.phase_action[phase_to_run]()
	def multiprocess_run(self) : 
		p = Pool(processes=self.n_jobs , maxtasksperchild=1)
		p.map(self.runer_managment, self.requested_phases)
	def normalrun(self):
		for ph in self.requested_phases: 
			self.phase_action[ph]()
		#log
	def availabe_phases(self) : 
		return self.available_phases
		#log
	@staticmethod
	def __url_maker__(url , method = 'best'):
		buff = url 
		if method is 'best' : 
			if 'https://' in url : 
				url = url.split('https://')
				url = url[1]
			elif  'http://' in url : 
				url = url.split('http://')
				url = url[1]
			try : 
				furl = requests.get('https://www.' + url)
				furl = 'https://www.' + url
			except : 
				try : 
					furl = requests.get('http://www.' + url) 
					furl = 'http://www.' + url
				except : 
					furl = buff 
			return furl
		if method is 'www' : 
			if 'https://' in url : 
				url = url.split('https://')
				url = url[1]
			elif  'http://' in url : 
				url = url.split('http://')
				url = url[1]
			if 'www' not in url : 
				url = 'www.' + url
			return url 
		if method is 'naked' : 
			if 'https://' in url : 
				url = url.split('https://')
				url = url[1]
			elif  'http://' in url : 
				url = url.split('http://')
				url = url[1]
			if 'www.' in url : 
				url = url.split('www.')
				url = url[1]
			return url 
	def __status__(self): 
		self.status = True 
		if self.target is '' : 
			self.status = False 
		if len(self.phases) < 1 :
			self.status = False
		return self.status 	
	#Attack Mapping
	def sshbruter(self , users = None , passlist = None , target = None) : 
		if target is None : 
			target = self.target
		if users is None : 
			users = ['root']
		if passlist is None : 
			passlist = default_password_list
		sshbrute(sshbrute , users , passlist)
	def extrabanner(self , target = None) : 
		if target is None : 
			target = self.target
		target = Attacker.__url_maker__(target , method = 'best')
		command = 'python' +  " " + waflulz_path + " " + '-u' + " "  + target + " " + '-a' +  " " 
		if self.verbos : 
			command = command +  " " +  '-vv'
		r3dexecute([command] , '[BANNER GRABBER RESULTS]')
	def xssstrike(self , target = None) : 
		if target is None : 
			target = self.target
		target = Attacker.__url_maker__(target , method = 'best')
		command = 'python3' +  " " + xssstrick_path + " " + '-u' + " "  + target + " " 
		if self.verbos : 
			command = command +  " " +  '-v'
		r3dexecute([command] , '[RESULTS][XSSSTRIKE]')
	def Phase1 (self):
		self.out	(COLOR.INF , "Phase One Started : Gather Primary Information" , COLOR.END )
		whatweb_result = PowerExecute(["[WhatWeb] for General Information "
			,"whatweb --colour=never -t 8 -a 3" + " " + self.target, [''], 'all'] ) 
	def golismero_vuln_scan(self): 
		self.out	(COLOR.INF , "[Phase One] Started : Search For Known Vulns" , COLOR.END )
		golismero_scan(self.target)
		pass
	def alt_vuln_scanner_1 (self): 
		pass
		pass
	def alt_vuln_scanner_2 (self): 
		self.out	('phase ') 
		pass
	def alt_vuln_scanner_3 (self): 
		self.out	('phase ') 
		pass
	def racoon_scan(self , target = None) : 
		if target is None : 
			target = self.target
		r3dexecute(['python3'  + " " + raccoon_path  + " " +'-f' + " " + target] , '[INFO][RACOON]' ) 
	def web_application_firewall(self , target = None , fuzzing_file = None) : 
		if target is None : 
			target = self.target 
		target = Attacker.__url_maker__(target , method = 'best')
		waf_stress_scanner(target , fuzzing_file = None  , verbose = self.verbos , mod = self.out , logger = None)		
	def xsspy(self , target = None) : 
		if target is None : 
			target = self.target 
		target = Attacker.__url_maker__(target , method = 'naked')
		command = 'python'  + " " + xsspy_path  + " " +'-u' + " " + target + " " + "-e" + " "
		if self.verbos : 
			command = command +  " " +  '-v'
		self.out(command)
		r3dexecute([command] , '[INFO][RACOON]' ) 
	def CmsInvestigator(self , target = None) : 
		if target is not None :
			self.target.target_tmp.append(self.target) 
			self.target = target
		self.out	(COLOR.INF , "Phase Six Started : Search For CMS/Application" , COLOR.END )
		if 'https://' in self.target : 
			self.target = self.target.split('https://')
			self.target = self.target[1]
		elif  'http://' in self.target : 
			self.target = self.target.split('http://')
			self.target = self.target[1]
		if 'www' not in self.target : 
			self.target = 'www.' + self.target
		#self.out	('DEBUG  : ' , self.target )
		#self.out	(COLOR.INF , "Phase Six Started : Search For CMS/Application" , COLOR.END )
		import os 
		command = '-u' + " "  + self.target 
		cmseek_result = PowerExecute(["[CMSEEK] CMS Identifer"
		,"python3" + "  "  + cmseek_path + " " +  command , [''], 'all'])
		self.out	(COLOR.RES , cmseek_result , COLOR.END)
		if 'Drupal' in cmseek_result : 
			if self.batch_mode : 
				self.Drupal_Scanner(self.target)
			else : 				
				choise = input('Do You Want send the Links to Check With droopescan?[y/n] >>')
				if 'y' in choise.lower() :
					self.Drupal_Scanner(self.target)
		elif 'WordPress' in cmseek_result : 
			if self.batch_mode is False : 
				choise = input('Do You Want send the Links to Check With Both WPSCAN and WPSEKU?[y/n] >>')
				if 'y' in choise.lower() :
					self.WP_Scanner_1(self.target)
					self.WP_Scanner_2(self.target)
				choise = input('Do You Want send the Links to Check With WPSCAN?[y/n] >>')
				if 'y' in choise.lower() :
					self.WP_Scanner_1(self.target)
				choise = input('Do You Want send the Links to Check With WPSEKU?[y/n] >>')
				if 'y' in choise.lower() :
					self.WP_Scanner_2(self.target)
			elif self.batch_mode :
				self.WP_Scanner_1(self.target)
				self.WP_Scanner_2(self.target)
		elif 'Joomla' in cmseek_result : 
			if self.batch_mode : 
				self.Joomla_Scanner_1(self.target)
			else :
				choise = input('Do You Want send the Links to Check With [DROOPESCAN] for joomla?[y/n] >>')
				if 'y' in choise.lower() :
					self.Joomla_Scanner_1(self.target)
		elif 'SilverStripe' in cmseek_result : 
			if self.batch_mode : 
				self.SS_Scanner(self.target)
			else : 
				choise = input('\nDo You Want send the Links to Check With DROOPESCAN] for SilverStripe ?[y/n] >>')
			if 'y' in choise.lower() :
				self.SS_Scanner(self.target)
	def Drupal_Scanner(self , target = None) : 
		if target is None : 
			target = self.target
		target = Attacker.__url_maker__(target , method = 'www')
		command = droopscan_path + ' scan drupal -u' + " " + target
		r3dexecute([command] , '[Droopscan][Drupal]') 
		#self.out	(droopescan_result)
	def WP_Scanner_1(self , target = None) : 
		if target is None : 
			target = self.target
		r3dexecute(['wpscan --no-banner  --force --enumerate vp vt  --ignore-main-redirect --disable-tls-checks --url' 
			+ " " + self.target] ) 
		#self.out	(wpscan_restults)
	def WP_Scanner_2(self , target = None) : 
		if target is None : 
			target = self.target
		r3dexecute(['python3'  + " " + wpseku_path  + " " +'-u' + " " + target] , '[Wpseku][Wordpress]' ) 
	def Joomla_Scanner_1(self , target = None) : 
		if target is None : 
			target = self.target 
		#self.out	(COLOR.INF , "'Joomla' detected : RUNNING MORE TESTS" , COLOR.END)
		r3dexecute([droopscan_path +' scan joomla -u' + " " + self.target] ) 
		#self.out	(droopescan_result)
	def waf_detector(self , target = None) : 
		if target is None : 
			target = self.target 
		target = Attacker.__url_maker__(target , method = 'best')
		#print('python3' + " " + waflulz_path + " " + '-n -u' + " " + target)
		waf = PowerExecute(["[WAF DETECTION]"
				,'python' + " " + waflulz_path + " " + '-a -u -v' + " " + target, [''], 'all'] ) 
		self.out	(waf)
	def SS_Scanner(self , target = None) : 
		if target is None : 
			target = self.target 
		#self.out	(COLOR.INF , "'SilverStripe' detected : RUNNING MORE TESTS" , COLOR.END)
		droopescan_result = PowerExecute(["[DROOPESCAN] for SilverStripe"
					,droopscan_path + ' scan silverstripe -u' + " " + self.target, [''], 'all'] ) 
		#self.out	(droopescan_result)
	def Fuzzable_Crawler_fast(self , target = None) : 
		if target is None : 
			target = self.target
		target = Attacker.__url_maker__(target)
		links =xploit(target)
		if self.verbos: 
			if len(links) > 1 : 
				self.out	('[FASTCRAWLER][RESULT]LINKS :')
				for link in links : 
					self.out	('[RESULT]\t' , link)
			else : 
				self.out	 ('[FASTCRAWLER][RESULT]No Link Found')
		if  len(links) > 1 : 
			if len(fuzzable_extract(links)) > 1 : 
				self.out	('[FASTCRAWLER][RESULT]FUZZABLE LINKS :')
				for link in fuzzable_extract(links) : 
					self.out	('[RESULT][FUZZABLE LINKS]\t' , link)
					self.fuzzable_links.append(link)
			else : 

				self.out('[FASTCRAWLER][RESULT]No Fuzzable Link Found')
		if len(self.fuzzable_links) > 1: 
			self.out	('[XFRAMEWORK ASSISTANCE] :')
			self.out	('Found' , len(self.fuzzable_links) , 'Links In Target')
			self.out	("You Can Either Send this Results for Sql-Injection or Template Injection ")
			if self.batch_mode is False : 
				choise = input('Do You Want send the Fuzzable Links to Check for Both?[y/n] >>')
			else : 
				choise = 'y'
			if 'y' in choise.lower() :
				#self.out	('runned') #debug
				self.check_sqli_1(targets = self.fuzzable_links)
				self.check_tmp_injection(targets = self.fuzzable_links)
				self.xssstrike(self.fuzzable_links)

			else :
				choise = input('Do You Want send the Fuzzable Links to Check for Sql-Injection?[y/n] >>')
				if 'y' in choise.lower() :
					#self.out	('runned') #debug
					self.check_sqli_1(targets = self.fuzzable_links)
					#self.check_tmp_injection(targets = self.fuzzable_links)
				else : 
					choise = input('Do You Want send the Fuzzable Links to Check for Template Injection?[y/n] >>')
					if 'y' in choise.lower() :
						#self.out	('runned') #debug
						#self.check_sqli_1(targets = self.fuzzable_links)
						self.check_tmp_injection(targets = self.fuzzable_links)
		elif len(self.fuzzable_links) is  0 : 
			self.Fuzzable_DeepCrawler_fast(target)
				#self.out	('[FASTCRAWLER][RESULT] Crawier Didnt find Any Fuzzable Links In Target')
	def Fuzzable_DeepCrawler_fast(self , target = None) : 
		if target is None : 
			target = self.target
		target = Attacker.__url_maker__(target)
		links =r3dxtractor(xploit(target) , target)
		if self.verbos: 
			if len(links) > 1 : 
				self.out	('[FASTCRAWLER][RESULT] LINKS :')
				for link in links : 
					self.out	('>\t' , link)
			else : 
				self.out	 ('[FASTCRAWLER][RESULT]No Link Found')
		if  len(links) > 1 : 
			if len(fuzzable_extract(links)) > 1 : 
				self.out	('[FASTCRAWLER][RESULT] FUZZABLE LINKS :')
				for link in fuzzable_extract(links) : 
					self.out	('>\t' , link)
					self.fuzzable_links.append(link)
			else : 
				self.out	 ('[FASTCRAWLER][RESULT] No Fuzzable Link Found')
		if self.batch_mode is False and len(self.fuzzable_links) > 1: 
			self.out	('[XFRAMEWORK  ASSISTANCE] :')
			self.out	('Found' , len(self.fuzzable_links) , 'Links In Target')
			self.out	("You Can Either Send this Results for Sql-Injection or Template Injection ")
			if self.batch_mode is False : 
				choise = input('Do You Want send the Fuzzable Links to Check for Both?[y/n] >>')
			else : 
				choise = 'y'
			if 'y' in choise.lower() :
				#self.out	('runned') #debug
				self.check_sqli_1(targets = self.fuzzable_links)
				self.check_tmp_injection(targets = self.fuzzable_links)
			else :
				choise = input('Do You Want send the Fuzzable Links to Check for Sql-Injection?[y/n] >>')
				if 'y' in choise.lower() :
					#self.out	('runned') #debug
					self.check_sqli_1(targets = self.fuzzable_links)
					#self.check_tmp_injection(targets = self.fuzzable_links)
				else : 
					choise = input('Do You Want send the Fuzzable Links to Check for Template Injection?[y/n] >>')
					if 'y' in choise.lower() :
						#self.out	('runned') #debug
						#self.check_sqli_1(targets = self.fuzzable_links)
						self.check_tmp_injection(targets = self.fuzzable_links)
		elif len(self.fuzzable_links) is  0 : 
				self.out	('Crawler Didnt find Any Fuzzable Links In Target')
	def Fuzzable_Crawler(self , target = None , crawl_level = 5) :
		if target is None : 
			target = self.target
		TARGET = target 
		a = Crawler(TARGET , crawl_level)
		data = a.launch()
		self.out	(data)
	def shellshock(self , target = None ) : 
		if target is None : 
			target = self.target 
		target = Attacker.__url_maker__(target , method = 'best')
		shellshock_scanner(target , verbose = self.verbos , mod = self.out , logger = None)		
	def Fuzzable_Crawler_photon_old(self) : 
		import os
		self.out	(COLOR.INF , "[Phase Nine] Started : Fuzzable CRAWLER" , COLOR.END )
		#import os

		photon_export_adress = os.getcwd()
		command = '-l 1 -t 4 --stdout=fuzzable ' + ' ' +  '-u' + " "  + self.target #+ " " + "-o" + " " + photon_export_adress 
		#debug : 
		#self.out	(command)
		#self.out	(photon_path)
		#self.out	(self.target)
		Photon_false_pos = ['' , 'allactivity?privacy_source=activity_log_top_menu' ] 
		ph_results = PowerExecute(["[Photon] Targeted Crawler"
		,"python" + "  "  + photon_path + " " +  command , [''], 'all'])
		if len(ph_results.replace('/allactivity?privacy_source=activity_log_top_menu' , '')) > 9 +len(self.target):
			self.fuzzable_links = [link for link in ph_results.split('\n') if link  not in Photon_false_pos]
			self.out	(self.fuzzable_links)
			if len(self.fuzzable_links) < 10 : 
				if self.batch_mode is False : 
					choise = input('Do you Want to Dig One Layer More [y/n]? >>> ')
				else :
					choise = 'y'
				if 'y' in choise.lower() :
					command = '-l 2 -t 6 --stdout=fuzzable ' + ' ' +  '-u' + " "  + self.target #+ " " + "-o" + " " + photon_export_adress 
					ph_results = PowerExecute(["[Photon] Targeted Crawler"
					,"python" + "  "  + photon_path + " " +  command , [''], 'all'])
					if len(ph_results.replace('/allactivity?privacy_source=activity_log_top_menu' , '')) > 9 +len(self.target):
						self.fuzzable_links = [link for link in ph_results.split('\n') if link  not in Photon_false_pos]
						self.out	(self.fuzzable_links)

		else : 
			#self.out	(ph_results)
			self.out	(COLOR.RED , '[Photon] Didnt Find Any Fuzzable Link' , COLOR.END)
			self.out	(COLOR.INF , "[Phase Nine][Photon] Try Againg With Depth of 2" , COLOR.END )
			#import os
			photon_export_adress = os.getcwd()
			command = '-l 2 -t 6 --stdout=fuzzable ' + ' ' +  '-u' + " "  + self.target #+ " " + "-o" + " " + photon_export_adress 
			ph_results = PowerExecute(["[Photon] Targeted Crawler"
			,"python" + "  "  + photon_path + " " +  command , [''], 'all'])
			if len(ph_results.replace('/allactivity?privacy_source=activity_log_top_menu' , '')) > 9 +len(self.target):
				self.fuzzable_links = [link for link in ph_results.split('\n') if link  not in Photon_false_pos]
				self.out	(self.fuzzable_links)
			else : 
				#self.out	(ph_results)
				self.out	(COLOR.RED , '[Photon] Didnt Find Any Fuzzable Link' , COLOR.END)
				self.out	(COLOR.INF , "[Phase Nine][Photon] Try Againg With Depth of 3" , COLOR.END )
				import os
				photon_export_adress = os.getcwd()
				command = '-l 3 -t 8 --stdout=fuzzable ' + ' ' +  '-u' + " "  + self.target #+ " " + "-o" + " " + photon_export_adress 
				ph_results = PowerExecute(["[Photon] Targeted Crawler"
				,"python" + "  "  + photon_path + " " +  command , [''], 'all'])
				if len(ph_results.replace('/allactivity?privacy_source=activity_log_top_menu' , '')) > 9 +len(self.target):
						self.fuzzable_links = [link for link in ph_results.split('\n') if link  not in Photon_false_pos]
						self.out	(self.fuzzable_links)

				else : 
					#self.out	(ph_results)
					self.out	(COLOR.RED , '[Photon] No Luck For Fuzzable Links' , COLOR.END)
		if len(self.fuzzable_links) > 0:
			self.out	('Found' , len(self.fuzzable_links) , 'Links In Target')
			self.out	("\nYou Can Either Send this Results for Sql-Injection or Template Injection ")
			if self.batch_mode is False : 
				choise = input('Do You Want send the Fuzzable Links to Check for Both?[y/n] >>')
			else : 
				choise = 'y'
			if 'y' in choise.lower() :
				#self.out	('runned') #debug
				self.check_sqli_1(targets = self.fuzzable_links)
				self.check_tmp_injection(targets = self.fuzzable_links)
			else :
				choise = input('\nDo You Want send the Fuzzable Links to Check for Sql-Injection?[y/n] >>')
				if 'y' in choise.lower() :
					#self.out	('runned') #debug
					self.check_sqli_1(targets = self.fuzzable_links)
					#self.check_tmp_injection(targets = self.fuzzable_links)
				else : 
					choise = input('\nDo You Want send the Fuzzable Links to Check for Template Injection?[y/n] >>')
					if 'y' in choise.lower() :
						#self.out	('runned') #debug
						#self.check_sqli_1(targets = self.fuzzable_links)
						self.check_tmp_injection(targets = self.fuzzable_links)
		elif len(self.fuzzable_links) is  0 : 
				self.out	('Crawier Didnt find Any Fuzzable Links In Target')
	def check_sqli_0(self , targets = None) : 
		if targets is None : 
			targets = self.target
		if type(targets) is list : 
			for target in targets :
				if self.verbos is True : 
					self.out	('[VERBOS]  [Small SQLi Scanner (DSSS)] is Testing' , target)
				command = '-u' + " " + '"' + target + '"'  
				sqli_mini_results = PowerExecute(["[Small SQLi Scanner (DSSS)]"
				,"python" + "  "  + sqli_mini_path + " " +  command , [''], 'all'])
				if len(sqliv_results) > 0 :
					if self.verbos is True :  
						self.out	(sqli_mini_results)
					elif 'no SQL injection vulnerability found' in sqli_mini_results :
						self.out	(COLOR.RED , '[Small SQLi Scanner (DSSS)] Did not Detect Anything ' , COLOR.END)
					if 'possible vulnerabilities found' in sqli_mini_results : 
						self.sqli_mini_vuln_links.append(target)
				else : 
					self.out	(COLOR.RED , '[Small SQLi Scanner (DSSS)]' , COLOR.END)
		elif type (targets) is str : 
			target = targets 
			command = '-u' + " " + '"' + target + '"'  
			sqli_mini_results = PowerExecute(["[Small SQLi Scanner (DSSS)]"
			,"python" + "  "  + sqli_mini_path + " " +  command , [''], 'all'])
			if len(sqli_mini_results) > 0 : 
				self.out	(sqli_mini_results)
			else : 
				self.out	(COLOR.RED , '[Small SQLi Scanner (DSSS)] Did not Detect Anything' , COLOR.END)
			if 'possible vulnerabilities found' in sqli_mini_results : 
				self.sqli_mini_vuln_links.append(target)
		else : 
			self.out	 ('Input Problem') 
			quit()
		if len(self.sqli_mini_vuln_links) > 0 and self.batch_mode is False: 
			self.out	('Added' , len(self.sqli_mini_vuln_links) , 'Potential vulnerable Links')
			choise = input('\nDo You Want send the Potential vulnerable Links to Sqliv for More Enumeration ?[y/n] >>')
			if 'y' in choise.lower() :
				#self.out	('runned') #debug
				self.check_sqli_1(targets = self.sqli_mini_vuln_links)
			else : 
				choise = input('\nDo You Want send the Potential vulnerable Links to Sqlmap for More Enumeration ?[y/n] >>')
				if 'y' in choise.lower() :
						#self.out	('runned') #debug
						self.check_sqli_2(targets = self.sqli_mini_vuln_links)
		if len(self.sqli_mini_vuln_links) is 0 and self.batch_mode is False: 
			choise = input('\nDo You Want send the all Links to Sqliv for More Enumeration ?[y/n] >>')
			if 'y' in choise.lower() :
				#self.out	('runned') #debug
				self.check_sqli_1(targets)
			else :
				choise = input('\nDo You Want send the all Links to Sqlmap for More Enumeration ?[y/n] >>')
				if 'y' in choise.lower() :
					#self.out	('runned') #debug
					self.check_sqli_2(targets)							
	def check_sqli_1(self , targets = None) :
		if targets is None : 
			targets = self.target
		self.sqli_vuln_links = []
		#self.out	(type(targets)) #debug
		if type(targets) is list : 
			for target in targets :
				if self.verbos is True : 
					self.out	('[VERBOS]  [SQLIV] is Testing' , target)
				command = '-t' + " "  + target  
				try : 
					sqliv_results = PowerExecute(["[sqliv]"
					,"python" + "  "  + sqliv_path + " " +  command , [''], 'all'])
					if len(sqliv_results) > 0 :
						if self.verbos is True :  
							self.out	(sqliv_results)
						if 'no SQL injection vulnerability found' in sqliv_results :
							self.out	(COLOR.RED , '[SQLIV] Did not Detect Anything ' , COLOR.END)
						if 'vulnerable' in sqliv_results : 
							self.sqli_vuln_links.append(target)
					else : 
						self.out	(COLOR.RED , '[SQLIV]' , COLOR.END)
				except KeyboardInterrupt :
					self.out	('Passing This test'  , method = 'Error')
		elif type (targets) is str : 
			target = targets 
			if self.verbos is True : 
					self.out	('[VERBOS]  [SQLIV] is Testing' , target)
			command = '-t' + " "  + target  
			try : 
				sqliv_results = PowerExecute(["[sqliv]"
				,"python" + "  "  + sqliv_path + " " +  command , [''], 'all'])
				if len(sqliv_results) > 0 :
					if self.verbos is True :  
						self.out	(sqliv_results)
					if 'no SQL injection vulnerability found' in sqliv_results :
						self.out	(COLOR.RED , '[SQLIV] Did not Detect Anything ' , COLOR.END)
					if 'vulnerable' in sqliv_results : 
						self.sqli_vuln_links.append(target)
				else : 
					self.out	(COLOR.RED , '[SQLIV] Didnt Work Correct' , COLOR.END)
			except KeyboardInterrupt :
				self.out	('Passing This test'  , method = 'Error')
		
		else : 
			self.out	('Input Format Wrong!')
		if len(self.sqli_vuln_links) > 0 : 
			self.out	('Found' , len(self.sqli_vuln_links) , 'vulnerable Links')
			if self.batch_mode is False: 
				choise = input('\n\n\nDo You Want send the vulnerable Links to Sqlmap for More Enumeration ?[y/n] >>')
			else : 
				choise = 'y'
			if 'y' in choise.lower() :
				#self.out	('runned') #debug
				self.check_sqli_2(target = self.fuzzable_links)
			else :
				pass
		else : 
			self.out	(COLOR.RED ,'First Checks Show No Signs of Sql-injection Vulenerablity' , COLOR.END)
			self.out	('In This Stage You Can : ')
			if len(targets) > 1 and type(targets) is list:
				self.out	('\t0)Choose ONE Fuzzable link and Send it To [SQLMAP] for More Enumeration')
				self.out	('\t1)Send all To [SQLMAP]for More Enumeration r (Not Recommended) ')
				self.out	('\t2)Choose ONE Fuzzable link and Send it To [SQLMAP] Dummper')
				self.out	('\t3)Send all To [SQLMAP] Dummper (Not Recommended) ')
				self.out	('\t9)Exit The Process')
				choise = input('Enter The Option >>>')
				if '0' in choise : 
					for i in range(0 , len(targets)) : 
						self.out	(i,')', targets[i])
					choise = input('Enter The Link NUMBER >>> ')
					try : 
						self.check_sqli_2(targets[int(choise)])
					except Exception as e :
						self.out	("Log : " , e) 
						self.out	('Number Out Of List ! Passing !'  , method = 'Error')
				elif '1' in choise : 
					if type(targets) is list : 
						for link in targets : 
							self.check_sqli_2(link)
				elif '2' in choise : 
					for i in range(0 , len(targets)) : 
						self.out	(i+')', targets[i])
					choise = input('Enter The Link NUMBER >>> ')
					try : 
						sqli_dumper_sqlmap(targets[int(choise)])
					except : 
						self.out	('Number Out Of List ! Passing !' , method = 'Error')
				elif '3' in choise : 
					if type(targets) is list : 
						for link in targets : 
							self.sqli_dumper_sqlmap(link)
				elif '9' in choise : 
					self.out	('passing!')
				else : 
					pass
			if (type(targets) is str)  or len(targets) is 1 and type(targets) is list : 
				self.out	('\t1)Send The Link [SQLMAP]for More Enumeration')
				self.out	('\t2)Send all To [SQLMAP] Dummper (Not Recommended)')
				self.out	('\t9)Exit The Process')	
				choise = input('Enter The Link NUMBER >>> ')
				if '1' in choise : 
					if type(targets) is str : 
						self.check_sqli_2(targets)
				elif '2' in choise : 
					if type(targets) is str : 
						self.sqli_dumper_sqlmap(targets)	
				elif '9' in choise : 
					self.out	('passing!')
					pass
				else : 
					pass
	def check_sqli_2(self , target = None) : 
		Sqlinjetable = False 
		self.out	(COLOR.INF , "SQLMAP : For Enumeration Databases" , COLOR.END )
		self.out	(COLOR.INF , "Note : This Test Depend On Databases Can take 2-10 Minutes" , COLOR.END )
		if target is None : 
			target = self.target
		self.sqli_vuln_links = []
		if type(target) is list :
			if len(target) is 1 : 
				pass
			else : 
				self.out	(COLOR.RED , 'Using Sqlmap Enumeration For More Than one Target is Not Recommended ' , COLOR.END)
			if self.verbos : 
				self.out	('[VERBOS] Running' , sqlmap_command)
			for link in target : 
				sqlmap_command = 'sqlmap --risk 3 --level 5 --batch --dbs -u' + " "  + link
				r3dexecute(sqlmap_command)
		if type(target) is str : 
			sqlmap_command = 'sqlmap --risk 3 --level 5 --batch --dbs -u' + " "  + target
			if self.verbos : 
				self.out	('[VERBOS] Running' , sqlmap_command)
			sqlmap_results = r3dexecute([sqlmap_command])
			Negative_Flag = 'all tested parameters do not appear to be injectable.'
			'''
			if Negative_Flag in sqlmap_results : 
				self.out	(COLOR.RED , '[SQLMAP] Did not Detect Anything' , COLOR.END)
				if self.verbos : 
					self.out	(sqlmap_results)
				elif self.batch_mode is False: 
					choise = input('Print All Result?[y/n] >>> ')
					if 'y' in choise : 
						self.out	(sqlmap_results)
				#log
			else :
				Possetive_flag1 = "sqlmap identified the following injection point"
				Possetive_flag2 = 'available databases'
				if Possetive_flag1 in sqlmap_results : 
					self.out	(COLOR.RED , '[SQLMAP] Found Some Injection Points' , COLOR.END)
					Sqlinjetable = True 
				if Possetive_flag2 in sqlmap_results : 
					self.out	(COLOR.RED , '[SQLMAP] Found Some Databases' , COLOR.END)
					Sqlinjetable = True 
				else : 
					self.out	(COLOR.RED , '[SQLMAP] May Found Some Intresting Things' , COLOR.END)
				if self.verbos : 
					if self.batch_mode is False : 
						choise = input('\n\n\nDo You Want See Full Sqlmap Reults ?[y/n] >>')
						if 'y' in choise.lower() :
							self.out	(sqlmap_results)
					else : 
						self.out	(sqlmap_results)						
				if 	Sqlinjetable is True and self.verbos is False: 
					if self.batch_mode is False : 
						choise = input('\nYou Are Not On Verbos Mode But Do You Want See Full Sqlmap Reults ?[y/n] >>')
						if 'y' in choise.lower() :
							self.out	(sqlmap_results)
					if self.batch_mode is True : 
						self.out	(sqlmap_results)
					#log
				else : 
					choise = input('Print All Result?[y/n] >>> ')
					if 'y' in choise : 
						self.out	(sqlmap_results)
				if Sqlinjetable is True : 
					choise = input('Sqlmap Detected That The Link is Injectible , Do You Want to Send the Link to Dump the Database ? [y/n] >>> ')
				if Sqlinjetable is False : 
					choise = input('Do You Want to Send the Link to Dump the Database ? [y/n] >>> ')
				if 'y' in choise : 
						self.sqli_dumper_sqlmap(target)
				else : 
					pass
			'''
	def sqli_dumper_sqlmap(self, targets = None) : 
		if targets is None : 
			targets = self.target
		self.out	(COLOR.INF , "[Phase : Data Base Dummper] Started" , COLOR.END )
		if type(targets) is list and len(targets) > 0: 
			if len(targets) > 1 : 
				self.out	('Last Phase Sent' , len(self.sqli_vuln_links) , 'vulnerable Links')
				for link in targets : self.out	(link)
				self.out	('You Can Dump and Check With Every Each Of them But it is not Recommended')
				if self.verbos is True : 
					self.out	('[VERBOS] Running' , 'sqlmap -a --batch --risk 3 --level 5 ') 
				choise = input('Type "--all-links" for dumping all Links or choose the link you want to check and paste here>>')
				if '--all-links' in choise or self.batch_mode: 
					for link in targets : 
						if self.batch_mode : 
							self.out	('[BATCH MODE IS False] SESSION WILL START AS INTRAVIVE WAY!')	
							sqlmap_command = 'sqlmap -a --batch --risk 3 --level 5 -u' + " " + link
						else :
							if self.verbos : 
								self.out	('[BATCH MODE IS ON] SESSION WILL START AS INTRAVIVE WAY!')	
								sqlmap_command = 'sqlmap -a --risk 3 --level 5 -u' + " " + link
						if self.verbos : 
							self.out	('[VERBOS] running : ' , sqlmap_command)	
						os.system(sqlmap_command)
				else : 
					link = choise
					if self.batch_mode: 
						self.out	('[BATCH MODE IS ON] SESSION WILL START AS INTRAVIVE WAY!')	
						sqlmap_command = 'sqlmap -a --batch --risk 3 --level 5 -u' + " " + link
					else :
						self.out	('[BATCH MODE IS ON] SESSION WILL START AS INTRAVIVE WAY!')	
						sqlmap_command = 'sqlmap -a --risk 3 --level 5 -u' + " " + link
					if self.verbos : 
						self.out	('[VERBOS] running : ' , sqlmap_command)	
					os.system(sqlmap_command)
			elif len(targets) is 1 :
				link = targets[0]
				if self.batch_mode: 
					self.out	('[BATCH MODE IS False] SESSION WILL START AS INTRAVIVE WAY!')	
					sqlmap_command = 'sqlmap -a --batch --risk 3 --level 5 -u' + " " + link
				else :
					if self.verbos : 
						self.out	('[BATCH MODE IS ON] SESSION WILL START AS INTRAVIVE WAY!')	
						sqlmap_command = 'sqlmap -a --risk 3 --level 5 -u' + " " + link
					if self.verbos : 
						self.out	('[VERBOS] running : ' , sqlmap_command)	
				os.system(sqlmap_command)			 
			else : 
				self.out	('Something is Wrong With The Inputed Targets / RTM')	
		elif type(targets) is str : 
			link = targets 
			if self.batch_mode is False: 
				self.out	('[BATCH MODE IS False] SESSION WILL START AS INTRAVIVE WAY!')	
				sqlmap_command = 'sqlmap -a --batch --risk 3 --level 5 -u' + " " + link
			else :
				if self.verbos : 
					self.out	('[BATCH MODE IS ON] SESSION WILL START AS INTRAVIVE WAY!')	
					sqlmap_command = 'sqlmap -a --risk 3 --level 5 -u' + " " + link
			if self.verbos : 
				self.out	('[VERBOS] running : ' , sqlmap_command)	
			os.system(sqlmap_command)

		else : 
			self.out	('Something is Wrong With The Inputed Targets / RTM')	
	def check_tmp_injection(self , targets = None , tplmap_level_command_include = False ) : 
		self.out	(COLOR.INF , "[Server-Side Template Injection Enumeration]" , COLOR.END )
		tplmap_level_command = '--level 5' 
		if self.batch_mode is False : 
			choise = input('\n do you want to increase level to 5 for Better Results? [y/n] >>')
		else :
			self.out	 ('do you want to increase level to 5 for Better Results? [y/n] >> y')
			choise = 'y'
		if 'y' in choise.lower() :
			tplmap_level_command_include = True 
		if targets is None : 
			targets = self.target
		#self.out	(type(targets)) #debug
		if type(targets) is list : 
			for target in targets :
				if self.verbos : 
					self.out	('[VERBOS] [TPLMAP] is Testing' , target)
				command = '-u' + " " + '"'  + target  + '"'
				if tplmap_level_command_include : 
					command = command + " " + tplmap_level_command
				if self.verbos : 
					self.out	('[VERBOS] running' , command)
				try : 
					tplmap_results = PowerExecute(["[TPLMAP]"
					,"python" + "  "  + tplmap_path + " " +  command , [''], 'all'])
					if len(tplmap_results) > 0 :
						if self.verbos:  
							self.out	(tplmap_results)
						if 'Tested parameters appear to be not injectable. Try to increase' in tplmap_results :
							self.out	(COLOR.RED , '[TPLMAP] Did not Detect Anything ' , COLOR.END)
						else : 
							if self.batch_mode is False : 
								choise = input('\nTPLMAP reported some kind of weakness , do you want to see full results? [y/n] >>')
								if 'y' in choise.lower() :
									self.out	(tplmap_results)
								else :
									pass
						if "Try to increase '--level' value to perform more tests" in tplmap_results :
							if self.batch_mode is False:
								choise = input('\nTPLMAP is Influncing to increase the level , do you want to increase level to 5? [y/n] >>')
							else :
								self.out	('\nTPLMAP is Influncing to increase the level , do you want to increase level to 5? [y/n] >> y')
								choise is 'y'
							if 'y' in choise.lower() :
									tplmap_level_command_include = True
					else : 
						self.out	(COLOR.RED , '[TPLMAP] Didnt Return Anything' , COLOR.END)
				except KeyboardInterrupt : 
					self.out	('Passing Test!'  , method = 'Error')
		elif type (targets) is str : 
			target = targets
			command = '-u' + " " + '"'  + target  + '"'
			tplmap_results = PowerExecute(["[TPLMAP]"
			,"python" + "  "  + tplmap_path + " " +  command , [''], 'all'])
			if len(tplmap_results) > 0 :
				if self.verbos:  
					self.out	(tplmap_results)
				if 'Tested parameters appear to be not injectable. Try to increase' in tplmap_results :
					self.out	(COLOR.RED , '[TPLMAP] Did not Detect Anything ' , COLOR.END)
				else : 
					if self.batch_mode is False : 
						choise = input('\nWe Could not Understand if TPLMAP found anythiing or not , do you want to see full results? [y/n] >>')
						if 'y' in choise.lower() :
							self.out	(tplmap_results)
						else :
							pass
			else : 
				self.out	(COLOR.RED , '[TPLMAP] Didnt Return Anything' , COLOR.END)	
	def check_xss_0(self , targets = None) : 
		if targets is None : 
			targets = self.target
		if type(targets) is list : 
			for target in targets :
				if self.verbos is True : 
					self.out	('[VERBOS] [Small Xss Scanner(DSXS)] is Testing' , target)
				command = '-u' + " " + '"' + target + '"'  
				xss_mini_results = PowerExecute(["[Small SQLi Scanner (DSSS)]"
				,"python" + "  "  + xss_mini_path + " " +  command , [''], 'all'])
				if len(sqliv_results) > 0 :
					if self.verbos is True :  
						self.out	(xss_mini_results)
					elif 'no vulnerabilities found' in xss_mini_results :
						self.out	(COLOR.RED , '[Small Xss Scanner(DSXS)] Did not Detect Anything ' , COLOR.END)
					if 'ossible vulnerabilities found' in xss_mini_results : 
						self.xss_mini_vuln_links.append(target)
				else : 
					self.out	(COLOR.RED , '[Small Xss Scanner (DSXS)]]' , COLOR.END)
		elif type (targets) is str : 
			target = targets 
			command = '-u' + " " + '"' + target + '"'  
			xss_mini_results = PowerExecute(["[Small Xss Scanner (DSXS)]"
			,"python" + "  "  + xss_mini_path + " " +  command , [''], 'all'])
			if len(xss_mini_results) > 0 : 
				self.out	(xss_mini_results)
			else : 
				self.out	(COLOR.RED , '[Small Xss Scanner (DSXS)] Did not Detect Anything' , COLOR.END)
			if 'possible vulnerabilities found' in xss_mini_results : 
				self.xss_mini_vuln_links.append(target)
		else : 
			self.out	 ('Input Problem' , method = 'Error') 
			quit()
	def Lfi_scan(self , target = None , fuzzing_file = None) : 
		if target is None : 
			target = self.target
		target = Attacker.__url_maker__(target , method = 'best')
		lfi_scanner(target ,fuzzers = fuzzing_file , verbose = self.verbos , mod = self.out )
	def clickjacking_scanner(self , target = None ) : 
		if target is None : 
			target = self.__url_maker__(self.target)
		data = urlopen(target)
		headers = data.info()
		if not "X-Frame-Options" in headers:  
			self.out	('Possible Click Jacking identified') 
		else:
			self.out	('Not vulnerable to Click ')
	def banner_grabber(self  , target=None) :
		if target is None : 
			target = self.target
		try:
			s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		except Exception as e :
			self.out(e)
		try:
			host=socket.gethostbyname(target)
			s.connect((host,int(80)))
			self.out("[*] connection successfull")
			s.send(b'HEAD / HTTP/1.0\r\n\r\n')
			data=s.recv(1024)
			self.out(str(data))
			s.close()

		except Exception as e :
			self.out("Connection failed")
			self.out(e)

#Handling attacker Class / Phases / Verbose / Simple Communication API 
class Core_Intractor : 
	def __init__ (self , output_moderator) : 
		self.attacker = Attacker(output_moderator = output_moderator)
	def set_target(self , target) :
		self.attacker.set_target(target)
	def set_phases(self , phases) :
		self.attacker.set_phases(phases)
	def set_batch_mode(self) : 
		self.attacker.batch_mode = True
	def set_verbos(self):
		self.attacker.verbos = True
	def set_n_jobs(self , n_jobs) :
		if type(n_jobs) is  int : 
			self.jobs = n_jobs
			self.attacker.n_jobs = int()
		else : 
			pass
	def fast_run(self) : 
		self.attacker.multiprocess_run()
	def normal_run(self) :
		self.attacker.normalrun()
	def stage_run(self , target , phases):
		self.attacker.set_target(target)
		self.attacker.set_phases(phases)
		self.attacker.normalrun()

#usage : 
	#test = Core_Intractor()
	#test.set_target('unito.it')
	#test.set_phases('1-19')
	#test.fast_run()