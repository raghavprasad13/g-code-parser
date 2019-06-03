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
	time.sleep(2)
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
		if param[0] is 'X':
			X = machine.origin[0]
			message = message + 'along X '
		elif param[0] is 'Y':
			Y = machine.origin[1]
			message = message + 'along Y '
		elif param[0] is 'Z':
			Z = machine.origin[2]
			message = message + 'along Z '

	machine.move((X,Y,Z))
	time.sleep(2)
	return message
			

def execute_m0(params, machine):
	machine.instruction_queue.close()
	machine.instruction_queue.put('ustop')

def execute_m112(params, machine):
	while not machine.instruction_queue.empty():
		machine.instruction_queue.get()
	machine.instruction_queue.put('estop')

def execute_m117(params, machine):
	print('Displaying message')