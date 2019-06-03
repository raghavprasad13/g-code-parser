''' This file contains the method handlers for the respective
	GCode directives. In this, I have just assumed, for the sake
	of simulation, that each command takes 1 second to execute'''

import time

def execute_g1(params, machine):
	if len(params) == 0:
		return 'Error. Insufficient parameters for G1'
	X = machine.current_position[0]
	Y = machine.current_position[1]
	Z = machine.current_position[2]

	message = ''

	for param in params:
		if param[0] is 'X':
			X += float(param[1:])
			message = message + 'Move ' + param[1:] + machine.selected_units[0] + ' X. '
		elif param[0] is 'Y':
			Y += float(param[1:])
			message = message + 'Move ' + param[1:] + machine.selected_units[0] + ' Y. '
		elif param[0] is 'Z':
			Z += float(param[1:])
			message = message + 'Move ' + param[1:] + machine.selected_units[0] + ' Z. '
		elif param[0] is 'E':
			message = message + 'Extrude '+param[1:]+' of filament. '
		elif param[0] is 'F':
			machine.set_feed_rate(float(param[1:]))
			message = message + 'Set feed rate to ' + param[1:] + machine.selected_units[0] + '/minute. '

	machine.move((X,Y,Z))
	time.sleep(1)
	print(message)


def execute_g28(params, machine):
	X = machine.current_position[0]
	Y = machine.current_position[1]
	Z = machine.current_position[2]

	message = 'Move to origin '

	if len(params) == 0:
		machine.move(machine.origin)
		return message

	for param in params:
		if param[0] is 'X':		# if X is among the included parameters
			X = machine.origin[0]	# shift X to X-coordinate of origin
			message = message + 'along X '	# update message

		elif param[0] is 'Y':	# if Y is among the included parameters
			Y = machine.origin[1]	# shift Y to Y-coordinate of origin
			message = message + 'along Y '	# update message

		elif param[0] is 'Z':	# if Z is among the included parameters
			Z = machine.origin[2]	# shift Z to Z-coordinate of origin
			message = message + 'along Z '	# update message

	machine.move((X,Y,Z))
	time.sleep(1)
	print(message)
	return message
			

def execute_m0(params, machine):
	machine.instruction_queue.close()		# do not accept any more instructions
	machine.instruction_queue.put('ustop')
	time.sleep(1)

def execute_m112(params, machine):
	while not machine.instruction_queue.empty():	# clear the instruction queue
		machine.instruction_queue.get()
	machine.instruction_queue.put('estop')
	time.sleep(1)

def execute_m117(params, machine):
	print('Displaying message')
	time.sleep(1)