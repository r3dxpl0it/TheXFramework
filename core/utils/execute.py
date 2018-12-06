import subprocess 
import os 
from core.utils.Graphics import COLOR

def vulnscheck(command , flag , Mode = 'in' , decode_type = "utf-8" , SHELL = True):
	if Mode == 'in' : 
		p = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=SHELL)
		output, err = p.communicate()
		result = output.lower() + err.lower()
		red_flag = [flg for flg in flag if flg in str(result)]
		if len(red_flag) > 0 :
			#print("DEBUG : " , found_flags , str(flag))
			return(output.decode(decode_type))
		else :
			return None
	elif Mode == 'nin' : 
		p = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=SHELL)
		output, err = p.communicate()
		result = output.lower() + err.lower()
		red_flag = output.lower() + err.lower()
		red_flag = [flg for flg in flag if flg not in str(result)]
		if len(red_flag) > 0 :
			#print("DEBUG : " , found_flags , str(flag))
			return(output.decode(decode_type))
		else :
			return None
	elif Mode is 'all' : 
		p = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=SHELL)
		#sleep(3)
		output, err = p.communicate()
		return(output.decode(decode_type))
	elif Mode is 'print' :
		process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		
		while True:
			output = process.stdout.readline()
			if output == '' and process.poll() is not None:
				break
			if output:
				#print('koohyar')
				print (output.strip())
		rc = process.poll()

def PowerExecute(action):
	title = action[0]
	print(COLOR.INF ,title + "Scan Start" , COLOR.END)
	command = action[1]
	#print( '\033[42m',"Running:" , command , COLOR.END)
	flag = [flg.lower() for flg in action[2]]
	result = vulnscheck(command , flag , Mode = action[3])
	if action[3] in ['in' , 'nin'] : 
		if result != None :
			print( COLOR.RED , title , 'Reported Vulenerablity' ,COLOR.END)
			#print("Log")
			#print(result)
		else :
			print( COLOR.GRE , title , "Didn't Detect Anything" , COLOR.END)	
	elif action[3] is 'all' : 
		print( COLOR.GRE , title , 'SCAN RESULTS :' ,COLOR.END) 	
		return (result)
		#print("Log")
	elif action[3] is 'print' : 
		if result is not None : 
			print ('[' + title + ']\t' +result)
		#print("Log")

class PowerExecute2 : 
	def Os(Command) : 
		try : 		
			return os.system(Command)
		except Exception as e:
			print("DEBUG : " , e)
			print("Execute Error !")
			pass 	

def executeBackEnd(cmd):
	try : 
	    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True , shell = True)
	    for stdout_line in iter(popen.stdout.readline, ""):
	        yield stdout_line 
	    popen.stdout.close()
	    return_code = popen.wait()
	    if return_code:
	        return (subprocess.CalledProcessError(return_code , cmd))
	except : 
		return ('Operation Failed')
def r3dexecute(cmd , info = '[Info]', moderator = print) : 
    for out in executeBackEnd(cmd):
        moderator(info , out, end="")


#r3dexecute(['python'])