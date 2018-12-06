#Sample Plugin Listing
#Supported Commands for Usage : 
#For non intravtive tool too add as plugin
#note for mandatories :
	# if you use TARGET it will alwayas ask you for your target befor running but if if you use %TARGEt% the target which you give ti framework will replace it !
	#Supported Framwork Auto-Replace COmmands : %TARGET% (NOT IMPLEMENTED YET!)

plugin_folder = 'Plugins'
space = ' '





Plugins =  {

#Open SSH

'openssh77' : { # Plugin Name for calling
'name'  : 'OpenSSH 7.7 - Username Enumeration' , #Plugin Full Name   
'plugin_type' : 'Exploit' , #Plugin Type : 1) Add-On 
'parrentfolder' : plugin_folder , #
'subfolder' : 'scripts' , #
'filename' : 'OpenSSH_77.py' , 
'pre-fix' : 'python' , #For Scripts like python Use 'python' or 'python3' | For bash scripts use './' | for tools that are already in path use 'path'
'mandatories' : ['TARGET'] , 
'command' : space + 'TARGET' + space + '--userList Data/users.txt ' , 
'output_method' : 'live'
}

#PYBUSTER 

,
'pybuster' : { # Plugin Name for calling
'name'  : 'pybuster : Directory Bruteforce' , #Plugin Full Name   
'plugin_type' : 'add-on' , 
'parrentfolder' : plugin_folder , #
'subfolder' : 'scripts' , #
'filename' : 'Minidirb.py' , 
'pre-fix' : 'python' , #For Scripts like python Use 'python' or 'python3' | For bash scripts use './' | for tools that are already in path use 'path'
'mandatories' : ['TARGET'] , 
'command' : space + 'TARGET' +  space + str(1) + space + '/usr/share/wordlists/dirb/common.txt' + space + '-vv'  , 
'output_method' : 'live'
}

}
