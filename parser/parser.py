'''
version: 1.0.1
Currently supports commands G1, G28, M0, M112 and M117
'''

from normalize import normalizer
from queue import Queue
import multiprocessing as mp
from method_handlers import *
import commands
import sys
import os

ERROR_FREE_CODE = True

if len(sys.argv) != 2:
	print("Usage: python3 parser.py </path/to/GCode_file>")
	sys.exit(1)

normalizer(sys.argv[1])

class Machine(object):

	ROOM_TEMP = 27

	def __init__(self, instruction_queue, message_queue, current_position = (0,0,0), origin = (0,0,0), feed_rate=0, extrusion_rate=0, fan_on=False, bed_temp=ROOM_TEMP, extruder_temp=ROOM_TEMP, is_waiting=False, selected_units=('mm', 's', 'C'), absolute_coordinates=True, message=None):
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
		self.message_queue = message_queue

	def move(self, position):
		self.current_position = position

	def set_feed_rate(self, rate):
		self.feed_rate = rate


def get_commands(lines, machine):
	for line in lines:
		machine.instruction_queue.put(line)


def parse_commands(machine):
	global ERROR_FREE_CODE

	while not machine.instruction_queue.empty():
		command = machine.instruction_queue.get()

		command_directive, params = get_command_directive(command)

		command_directive = command_directive.strip()

		command_return_message = commands.get_command()[command_directive](params, machine)

		if command_return_message.startswith("Error"):
			print(command_return_message)
			ERROR_FREE_CODE = False
			break

		if command_return_message == '==> Emergency stop':
			machine.message_queue.put(command_return_message)
			break

		if command_return_message == '==> Unconditional stop':
			machine.message_queue.put(command_return_message)
			break

		machine.message_queue.put(command_return_message)


def get_command_directive(command):
	command = command.split(' ')
	directive = command[0]
	params = command[1:]

	return [directive, params]

def print_command_messages(machine):
	while not machine.message_queue.empty():
		print(machine.message_queue.get())


def main():
	# manager = mp.Manager()
	instr_queue = Queue()
	message_queue = Queue()
	# directive_queue = manager.Queue()

	machine = Machine(instruction_queue=instr_queue, 
						message_queue=message_queue)

	input_file_handle = open('./tmp.txt', 'r')
	
	lines = input_file_handle.readlines()

	input_file_handle.close()
	os.remove('./tmp.txt')

	get_commands(lines, machine)

	parse_commands(machine)

	if ERROR_FREE_CODE:
		print_command_messages(machine)

	# pool = mp.Pool(mp.cpu_count() + 2)

	# jobs = []
	# job1 = pool.apply_async(get_commands, (lines, machine))
	# job2 = pool.apply_async(parse_commands, (machine, ))

	# jobs = [job1, job2]

	# for job in jobs:
	# 	job.get()

	# pool.close()

if __name__ == '__main__':
	main()


