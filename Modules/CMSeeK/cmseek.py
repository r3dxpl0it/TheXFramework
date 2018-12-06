import cmseekdb.basic as cmseek # All the basic functions
import cmseekdb.core as core
import argparse


parser = argparse.ArgumentParser(prog='cmseek.py')
parser.add_argument('-u', '--url' , dest = 'url')
parser.add_argument('-v', '--verbose', action="store_true")
args = parser.parse_args()

def cmseekapi(target , cua = None) : 
	target = cmseek.process_url(target)
	if cua == None:
		cua = cmseek.randomua()
	core.main_proc(target,cua)

#	cmseek.handle_quit()
	
if args.verbose:
    cmseek.verbose = True
#cmseek.clear_log()
if args.url : 
	cmseekapi(args.url)