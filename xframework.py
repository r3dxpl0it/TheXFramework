#!/usr/bin/python3
import argparse
import platform 
if not int(platform.python_version()[0]) >= 3 : 
	print("Version not Satisfiable ! Try With Python > 3  ")
	raise SystemExit
def pre_launch() : 
	from utils.framework import XFramework , HELP , Core_Intractor_handler
	from Plugins.Engine import  XPlugins
	from Plugins.plugins import  Plugins
	from utils.linux import  linux_commands

	xf_handler = XFramework()
	helper = HELP(xf_handler)
	plugin_handler = XPlugins(Target = xf_handler.target,  config_file = Plugins)
	linux_handler = linux_commands(xf_handler)
	Sr = Core_Intractor_handler(xf_handler.__out__())

	#Master Commands : 
	xf_handler.add_master_commands('tar' , xf_handler.set_target_wizard)
	xf_handler.add_master_commands('target' , xf_handler.set_target_wizard)
	xf_handler.add_master_commands('clear' , xf_handler.clearPage)
	xf_handler.add_master_commands('cls' , xf_handler.clearPage)
	xf_handler.add_master_commands('clc' , xf_handler.clearPage)
	xf_handler.add_master_commands('exit' , xf_handler.Exit)
	xf_handler.add_master_commands('restart' , xf_handler.Restart)
	xf_handler.add_master_commands('show' , helper.show)
	xf_handler.add_master_commands('system' , helper.linux)
	xf_handler.add_master_commands('help' , helper.help)
	xf_handler.add_master_commands('plugins' , plugin_handler.__help__)
	xf_handler.add_master_commands('-v' , xf_handler.Swich_Verbose)
	xf_handler.add_master_commands('-u' , xf_handler.set_target_wizard)
	#Activator Commands : 
	xf_handler.add_activator_commands('plugins' , 'list' , plugin_handler.List)
	xf_handler.add_activator_commands('plugins' , 'loader' , plugin_handler.pluger)
	xf_handler.add_activator_commands('load' , 'netscan' , xf_handler.net_attacker)
	xf_handler.add_activator_commands('load' , 'attacker' , xf_handler.core_attacker)
	xf_handler.add_activator_commands('set' , 'target' , xf_handler.set_target_wizard)
	#Run Commands
	xf_handler.add_activator_commands('run' , 'golismero' , Sr.GOLISMERO)
	xf_handler.add_activator_commands('run' , 'sqlimini' , Sr.SQLI_SCAN_MINI)
	xf_handler.add_activator_commands('run' , 'cmscan' , Sr.CMSSCAN)
	xf_handler.add_activator_commands('run' , 'crawlerph0' , Sr.FUZZABLE_CRAWLER_PHOTON_NEW)
	xf_handler.add_activator_commands('run' , 'sqliv' , Sr.SQLIV)
	xf_handler.add_activator_commands('run' , 'smapenum' , Sr.SQLMAP_ENUM)
	xf_handler.add_activator_commands('run' , 'smapdump' , Sr.SQLMAP_DUMPER)
	xf_handler.add_activator_commands('run' , 'dsdroopal' , Sr.DROOP_DRUP)
	xf_handler.add_activator_commands('run' , 'wpscan' , Sr.WPSCAN)
	xf_handler.add_activator_commands('run' , 'wpseku' , Sr.WPSEKU)
	xf_handler.add_activator_commands('run' , 'dsjoomla' , Sr.DROOP_JOOMLA)
	xf_handler.add_activator_commands('run' , 'dssilver' , Sr.DROOP_SILVER)
	xf_handler.add_activator_commands('run' , 'xssmini' , Sr.XSS_SCAN_MINI)
	xf_handler.add_activator_commands('run' , 'waf' , Sr.WAF)
	xf_handler.add_activator_commands('run' , 'lfi' , Sr.LFI)
	xf_handler.add_activator_commands('run' , 'crawlerph0' , Sr.FUZZABLE_CRAWLER_PHOTON_NEW)
	xf_handler.add_activator_commands('run' , 'crawlerph1' , Sr.CRAWLER_PHOTON_CORE_MODIFIED)
	xf_handler.add_activator_commands('run' , 'crawler' , Sr.DFUC)
	xf_handler.add_activator_commands('run' , 'deapcrawl' , Sr.FAST_DEEPCRAWL)
	xf_handler.add_activator_commands('run' , 'bannergrabber' , Sr.BANNER_GRABBER)
	#Info Commands
	xf_handler.add_activator_commands('show' , 'target' , xf_handler.show_target)
	xf_handler.add_activator_commands('show' , 'workspace' , xf_handler.workspacer_show)
	xf_handler.add_activator_commands('show' , 'info' , xf_handler.show_all)
	xf_handler.add_activator_commands('show' , 'commands' , xf_handler.all_commands)
	#Workspace Commands 
	xf_handler.add_activator_commands('workspace' , 'show' , xf_handler.workspacer_show)
	xf_handler.add_activator_commands('workspace' , 'new' , xf_handler.workspacer_new)
	#System Commands 
	xf_handler.add_activator_commands('system' , 'term' , xf_handler.syscommandline)
	xf_handler.add_activator_commands('system' , 'python' , xf_handler.pythoncommand)
	xf_handler.add_activator_commands('system' , 'monitor-mode' , linux_handler.Monitor_Mode)
	xf_handler.add_activator_commands('system' , 'macchanger' , linux_handler.Macchanger)
	xf_handler.add_activator_commands('system' , 'verbose' , xf_handler.Swich_Verbose)
	xf_handler.add_activator_commands('system' , 'quiet' , xf_handler.Swich_Quiet)
	#Manual Commands  : 
	xf_handler.add_manual_commands('tar' , xf_handler.set_target)
	xf_handler.add_manual_commands('load' , plugin_handler.run)
	xf_handler.add_manual_commands('jobs' , xf_handler.set_n_jobs)
	xf_handler.add_manual_commands('target' , xf_handler.set_target)
	xf_handler.add_manual_commands('-u' , xf_handler.set_target)
	#xf_handler.add_manual_commands('use' , plugin_handler.run)

	LIST_OF_COMMANDS = {'show':['target' , 'workspace', 'info' , 'commands'],
		 'system':['term', 'python' , 'monitor-mode' , 'macchanger' , 'verbose' , 'quiet'],
		 'plugins':['list', 'loader'],
		 'workspace':['new', 'show'],
		
		 'load' : [x for x in plugin_handler.__list__() ] , 
		 'run' : [x for x in xf_handler.__all_attacker_commands__()] , 
		 'exit':[], 'clear':[], 'restart':[], 'target':[], 'help':[]
		 #'load':['netscan' , 'attacker'],
		}
	xf_handler.cli_completer_setup(LIST_OF_COMMANDS)
	xf_handler.Launcher()
#Run This Shit 
if __name__ == "__main__":
	import sys

	parser = argparse.ArgumentParser('./xframework.py' , usage = './xframework.py -u <Target> [Options/Scans]')
	'''Commands Groups'''
	req_commands = parser.add_argument_group('Required Options')
	options_commands = parser.add_argument_group('Options')
	group_phases = parser.add_argument_group('Auto Scans')
	group_modules = parser.add_argument_group('Advanced Scans')
	crawler_ccli = parser.add_argument_group('Crawler Engine')
	group_plugins = parser.add_argument_group('-'*30 + '''\nNote :\n\t*Plugins Would not accept any Options\n\t*Each Plugin Will Ask You Specific Input\n\nPlugins [Scripts and Exploits]''')

	"""Required Commands Lists"""
	req_commands.add_argument('-u', '--url', help='root url', dest='url')

	''''''
	options_commands.add_argument('-i', '--interprator', help='Load interprator', dest='interprator', default = False,  action='store_true')
	options_commands.add_argument('-v', '--verbose', help='Verbose Mode', dest='Verbose', default = False,  action='store_true')
	options_commands.add_argument('-b' , '--batch', help='batch Mode', dest='batch', default = False,  action='store_true')
	options_commands.add_argument('-f',  help='A File For Fuzzing (Only For Scans That Uses Fuzzing)', dest='fuzzfile')
	options_commands.add_argument('-F', '--fast', help='Run Very Fast Without Logging/Saving/History [Soon]', default = False , action='store_true', dest='fastmode')


	#Scans
	group_phases.add_argument("-n" , "--netscan" , action='store_true' ,dest='netscan' , default = False, help='Auto Network Port Scanner')
	group_phases.add_argument("-w" , '--webscan' , action='store_true' , dest='webscan' , default = False,help='Auto web Application Scanner')
	group_phases.add_argument("-t", type = int  , dest='threads' , default = 8, help='Number of Threads')
	#Crawler Options
	crawler_ccli.add_argument('--crawler' , action='store_true' ,dest='crawler' , default = False, help='Run Crawler')
	#crawler_ccli.add_argument('--fuzz' , action='store_true' ,dest='fuzz' , default = False, help='Collecting Fuzzable Addresses')
	#crawler_ccli.add_argument('--internal' , action='store_true' ,dest='internal' , default = False, help='Collecting Internal Addresses')
	#crawler_ccli.add_argument('--external' , action='store_true' ,dest='external' , default = False, help='Collecting External Addresses')	
	crawler_ccli.add_argument('--deep' ,action='store_true' ,dest='deep' , default = False, help='Run Crawler With Deep Depth')
	crawler_ccli.add_argument('--photon' ,action='store_true' ,dest='photon' , default = False, help='Run Crawler With Minimized Photon Engine')
	crawler_ccli.add_argument('--photonold' ,action='store_true' ,dest='photonold' , default = False, help='Run Crawler With Photon Engine')

	#Advance Options 
	group_modules.add_argument("--banner" , action='store_true' , dest='banner' , help='Grab Target Banner')
	group_modules.add_argument("--wafbanner" , action='store_true' , dest='extrabanner' , help='Agressive Banner Grabbing with Limited WAF detection')
	group_modules.add_argument("--wafstress" , action='store_true' , dest='waf' , help='Web Application Firewall Stress(Optional : Fuzzfile)')
	group_modules.add_argument("--waf" , action='store_true' , dest='waf_detect' , help='Web ApplicationFirewall and Server Service Detection')
	group_modules.add_argument("--cms" , action='store_true' , dest='cms' , help='CMS Identifier')
	group_modules.add_argument("--lfi" , action='store_true' , dest='lfi' , help='Local File Inclution Attack (Optional : Fuzzfile)' )
	group_modules.add_argument("--clickjack" , action='store_true' , dest='clickjack' , help='clickjack Vuln Scan' )
	group_modules.add_argument("--tempi" , action='store_true' , dest='tempi' , help='Template Injection Attack')
	group_modules.add_argument("--sqlimini" , action='store_true' , dest='sqlimini' , help='Pre-Enumeration Simple Sqli Attacks')
	group_modules.add_argument("--sqliv" , action='store_true' , dest='sqliv' , help='Enumeration Simple Sqli Attacks')
	group_modules.add_argument("--sqlmap" , action='store_true' , dest='sqlmapdbs' , help='Identify Databases with Sqlmap')
	group_modules.add_argument("--sqlmapdump" , action='store_true' , dest='sqlmapdump' , help='Identify Databases with Sqlmap')
	group_modules.add_argument("--xssmini" , action='store_true' , dest='xssmini' , help='Pre-Enumeration Simple Cross Siting Scripting')
	group_modules.add_argument("--xsspy" , action='store_true' , dest='xsspy' , help='Pre-Enumeration Simple Cross Siting Scripting')
	group_modules.add_argument("--drupal" , action='store_true' , dest='drupalscandroop' , help='Droopal Full Enumeration')
	group_modules.add_argument("--wordpress" , action='store_true' , dest='wpscan' , help='Wordpress Full Enumeration with wpscan')
	group_modules.add_argument("--wordpress2" , action='store_true' , dest='wpseku' , help='Wordpress Full Enumeration with wpseku')
	group_modules.add_argument("--joomla" , action='store_true' , dest='joomla' , help='Joomla Full Enumeration with wpseku')
	#group_modules.add_argument("--Nmap" , action='store_true' , dest='Nmap' , help='Target Full Enumeration with Nmap')
	group_modules.add_argument("--golismero" , action='store_true' , dest='golismero' , help='Target Full Enumeration with golismero')
	group_modules.add_argument("--raccoon" , action='store_true' , dest='raccoon' , help='Raccoon Framework Full Scan')
	group_modules.add_argument("--shellshock" , action='store_true' , dest='shellshock' , help='Scan For shellshock')
	group_modules.add_argument("--xssstrick" , action='store_true' , dest='xssstrick' , help='Scan a URL For XSS injection with XSS-Strick')

	#Modules
	from utils.framework import XFramework , HELP , Core_Intractor_handler
	from Plugins.Engine import  XPlugins
	from Plugins.plugins import  Plugins
	import sys
	def test(arg , item) :
		#item = item.__name__ 
		if arg.item is True : 
			return True 
		else :
			return False 
	xf_handler = XFramework()

	helper = HELP(xf_handler)
	plugin_handler = XPlugins(Target = xf_handler.target,  config_file = Plugins)
	#Plugins
	plugins = list()
	for item in plugin_handler.__obj__().keys(): 
		group_plugins.add_argument("--"+item , action='store_true' , dest=item , default  = False ,  help = plugin_handler.__obj__()[item]['name'])
		plugins.append(item)
	if len(sys.argv) < 2:
		parser.print_help()
		sys.exit(1)

	args = parser.parse_args()
	if args.interprator:
		pre_launch()
	if args.fastmode : 
		xf_handler.workspacer_start()
	else : 
		import traceback , sys
		try :
			from core.attacker import Core_Intractor
			if  args.fastmode : 
				cint = Core_Intractor(xf_handler.out)
			else :
				cint = Core_Intractor(print)
			cint.attacker.n_jobs = args.threads

			if args.url is not None : 
				cint.set_target(args.url)
				if args.Verbose : 
					cint.set_verbos()
				if args.webscan is True or args.netscan is True: 
				#if args.scan : 
					cint.set_batch_mode()
					if args.webscan : 
						cint.set_verbos()
						cint.set_batch_mode()
						cint.set_phases([23 , 25])
						cint.mod = print 
						cint.fast_run()
				else :
					if args.golismero : 
						cint.set_phases([2])
						cint.normal_run()
					if args.waf_detect : 
						cint.set_phases([3])
						cint.normal_run()	
					if args.cms : 
						cint.set_phases([6])
						cint.normal_run()
					if args.sqlimini : 
						cint.set_phases([7])
						cint.normal_run()	
					if args.xsspy : 
						cint.set_phases([8])
						cint.normal_run()	
					if args.photon : 
						cint.set_phases([9])
						cint.normal_run()	
					if args.sqliv : 
						cint.set_phases([10])
						cint.normal_run()	
					if args.sqlmapdbs : 
						cint.set_phases([11])
						cint.normal_run()	
					if args.sqlmapdump : 
						cint.set_phases([12])
						cint.normal_run()	
					if args.tempi : 
						cint.set_phases([13])
						cint.normal_run()	
					if args.drupalscandroop : 
						cint.set_phases([14])
						cint.normal_run()	
					if args.wpscan : 
						cint.set_phases([15])
						cint.normal_run()	
					if args.wpseku : 
						cint.set_phases([16])
						cint.normal_run()	
					if args.joomla : 
						cint.set_phases([17])
						cint.normal_run()	
					if args.xssstrick : 
						cint.set_phases([19])
						cint.normal_run()	
					if args.xssmini : 
						cint.set_phases([20])
						cint.normal_run()	
					if args.waf : 
						cint.set_phases([21])
						cint.normal_run()	
					if args.lfi : 
						cint.set_phases([22])
						cint.normal_run()	
					if args.crawler : 
						cint.set_phases([23])
						cint.normal_run()	
					if args.photonold : 
						cint.set_phases([24])
						cint.normal_run()
					if args.clickjack : 
						cint.set_phases([25])
						cint.normal_run()

					if args.banner : 
						cint.set_phases([26])
						cint.normal_run()
					if args.deep : 
						cint.set_phases([27])
						cint.normal_run()
					#if args.sshbrute : 
					#	cint.set_phases([28])
					#	cint.normal_run()
					if args.shellshock : 
						cint.set_phases([29])
						cint.normal_run()
					if args.extrabanner : 
						cint.set_phases([30])
						cint.normal_run()
					if args.raccoon : 
						cint.set_phases([31])
						cint.normal_run()
			else : 
				if len(sys.argv) > 1 :  
					for _item_ in sys.argv :  
						if '--' in _item_ : 
							_item_ = _item_[2:]
							if _item_  in Plugins : 
								plugin_handler.run(_item_)	
				else :
					print("Target Undifined, Use '-u TARGET'")

		except Exception as e: 
			print(e)
			print(traceback.format_exc())


	

