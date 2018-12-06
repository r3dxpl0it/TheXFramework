import requests

def waf_stress_scanner(target , verbose = False ,  fuzzing_file = None , mod = print , logger = None ) : 
		if fuzzing_file is None : 
			try : 
				fuzz_file = open("/usr/share/wfuzz/wordlist/Injections/All_attack.txt" , "r")
			except Exception as e : 
				mod	('Default Fuzz File Adding Error' , method = 'Error')
				choise = input("Fuzzing Dictionary File Adress >>>")
				try : 	
					fuzz_file = open(choise , "r")
				except Exception as e : 
					mod	('File Adding Error' , method = 'Error')
		else : 
			try : 
				fuzz_file = open(fuzzing_file,"r") 
			except Exception as e : 
				mod	('File Adding Error' , method = 'Error')
		try : 
			PASS = list()
			request_count	= success_count = failed_count = allowed_count = blocked_count = error_count = 0
			if target[:-1] is not "/" :
				target = target + '/'
			for fuzz in fuzz_file:
				request_count += 1
				try:
					req = requests.get(target, params=fuzz)
					if verbose : 
						mod	("[VERBOSE] [STATUS:"+str(req.status_code)+"]"  ,target + fuzz.strip())
					success_count += 1
					if req.status_code == 200:
						allowed_count += 1
						PASS.append(fuzz)
					elif req.status_code == 403:
						mod	("[VERBOSE] [STATUS:"+str(req.status_code)+"]"  ,target + fuzz.strip())
						blocked_count += 1
					else:
						mod('** Failed: status_code={}, Payload: {}'.format(req.status_code, fuzz))
				except KeyboardInterrupt : 
					break
				except Exception as e:
					failed_count += 1
					mod(e)
			mod	('\n','-'*10)
			mod	('WAF Testing results for : ' , target)
			mod	('Number of Fuzzes available', len(fuzz_file.read().split("\n")))
			mod	('Total requests ' , request_count)
			mod	('Success requests: ' , success_count)
			mod	('Failed requests: ' , failed_count)
			mod	('Allowed requests: ' , allowed_count)
			mod	('Blocked requests: ' , blocked_count)		

		except Exception as e : 
			mod	(e , method = 'Error')