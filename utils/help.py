class HELP:
	def __init__(self , moderator) : 
		self.mod = moderator
	def show(self) : 
		doc = '''
		show commands : Showing All Available Commands
		show target : Show Target
		show info : Show All Info and Settings
		show help : Show Manual 
		'''
		self.mod.out(doc)
	def linux(self) : 
		doc = '''
		macchanger
		monitor mode 
		'''
		self.mod.out(doc)
	def help(self) : 
		doc = '''

              COMMAND                              Description                
 ---------------------------------- ----------------------------------------- 
  target <TARGET>                    set target                               
  run                                List of all Modules/Phases/Implements    
  run <Module-Name>                  Run Specific Module or Phase             
  jobs <Number of Threads>           Number of Threads to Use for Attacking   
  show <target/info/workspace>       Show Session Information                 
  plugins <list/loader>              Show Available Plugins or Load a plugin  
  system <term/python>               Load Shell/Python Interpreter            
  system <verbose/quite>             Make Xframework Very Load or Too Shy     
  system <monitor-mode/macchanger>   Linux System Assist                      
  workspace <show/new>               Change The Logging/History Place         
  clear                              Clear the Page                           
  CTRL+D                             back                                     
  exit/CTRL+C                        Exit the system                          

	'''
		self.mod.out(doc)
