''' This file contains a mapping from the GCode directive 
	to the appropriate method handler '''
	
from method_handlers import *

command_dict = {'G1': execute_g1,
				'G28': execute_g28,
				'M0': execute_m0,
				'M112': execute_m112,
				'M117': execute_m117}

def get_command_dict():
	return command_dict