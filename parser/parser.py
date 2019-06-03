from normalize import normalizer
import multiprocessing as mp
from method_handlers import *
import commands
import sys
import os

if len(sys.argv) != 2:
	print("Usage: python3 parser.py </path/to/input_file>")
	sys.exit(1)

normalizer(sys.argv[1])

class Machine(object):

	ROOM_TEMP = 27

	def __init__(self, instruction_queue, current_position = (0,0,0), origin = (0,0,0), feed_rate=0, extrusion_rate=0, fan_on=False, bed_temp=ROOM_TEMP, extruder_temp=ROOM_TEMP, is_waiting=False, selected_units=('mm', 's', 'C'), absolute_coordinates=True, message=None):
		self.instruction_queue = instruction_queue
		self.current_position = current_position
		self.origin = origin
		# self.speed = speed
		self.feed_rate = feed_rate
		self.extrusion_rate = extrusion_rate
		self.fan_on = fan_on
		self.bed_temp = bed_temp
		self.extruder_temp = extruder_temp
		self.is_waiting = is_waiting
		self.selected_units = selected_units
		self.absolute_coordinates = absolute_coordinates

	def move(self, position):
		self.current_position = position

	def set_feed_rate(self, rate):
		self.feed_rate = rate


def get_commands(lines, machine):
	for line in lines:
		machine.instruction_queue.put(line)


def parse_commands(machine):
	while True:
		command = machine.instruction_queue.get()

		if command == 'estop':
			print('Emergency stop!')
			break
		if command == 'ustop':
			print('Unconditional stop!')
			break

		handler, params = get_command_directive(command)

		p = mp.Process(target = handler, args = (params, machine))
		p.start()
		# if directive == 'G1':
			
		# 	if message.split('.') == 'Error':
		# 		break
		# 	print(message)
		# if directive == 'G28':
		# 	message = execute_g28(params, machine)
		# elif directive == 'G2':
		# 	pass

		# if command == 'estop':
		# 	print('Emergency stop!')
		# 	break
		# if command == 'ustop':
		# 	print('Unconditional stop!')
		# 	break
		# p = mp.Process(command[0], command[1])
		

# def execute_commands(directive_queue, machine):
# 	while True:
# 		if command == 'estop':
# 			print('Emergency stop!')
# 			break
# 		if command == 'ustop':
# 			print('Unconditional stop!')
# 			break
# 		proc = mp.Process(directive_queue.get())


def get_command_directive(command):
	command = command.split(' ')
	directive = command[0]
	params = command[1:]

	return [commands.get_command_dict().get(directive), params]


def main():
	manager = mp.Manager()
	instr_queue = manager.Queue()
	directive_queue = manager.Queue()

	# machine = Machine(instr_queue, (0,0,0), (0,0,0), 0, 0, False, Machine.ROOM_TEMP, Machine.ROOM_TEMP, False, ('mm', 's', 'C'), True)
	machine = Machine(instruction_queue = instr_queue)
	# machine.instruction_queue.put('Hello')
	# print(machine.instruction_queue.get())
	input_file_handle = open('./tmp.txt', 'r')
	
	lines = input_file_handle.readlines()

	input_file_handle.close()
	os.remove('./tmp.txt')

	pool = mp.Pool(mp.cpu_count() + 2)

	jobs = []
	job1 = pool.apply_async(get_commands, (lines, machine))
	job2 = pool.apply_async(parse_commands, (machine, ))
	# job3 = pool.apply_async()

	jobs = [job1, job2]

	for job in jobs:
		job.get()

	pool.close()

if __name__ == '__main__':
	main()


