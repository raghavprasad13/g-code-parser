import multiprocessing as mp

class File(object):
	def __init__(self, name, mode):
		self.name = name
		self.mode = mode

	def open(self):
		file = open(self.name, self.mode)
		return file


def remove_semi_colon_comments(lines, output_queue):
	''' This function takes in the raw G Code lines
		and remove the comments that begin with a ; 
		Also, this capitalizes every character for
		the sake of uniformity '''

	for line in lines:
		line = line.upper()
		index = line.find(';')
		if index == 0:
			continue
		if index is not -1:
			line = line[0:index]
		output_queue.put(line)


def remove_parenthesis_comments(input_queue, output_queue):
	''' This function takes the G Code without the 
		; comments and removes the comments enclosed in ().
		Additionally, all extraneous whitespaces are removed'''

	while not input_queue.empty():
		line = input_queue.get()
		line = remove_comments(line)
		line = " ".join(line.split())	# This is done in order to remove extra whitespaces
		output_queue.put(line)

		
def remove_comments(line):
	while True:
		index = line.find('(')
		if index is -1:
			break
		start = index
		end = line.find(')', start)
		if end == -1:
			return 'unclosed comment error'
		line = line[0:start]+line[end+1:]
	return line


def print_normalized_output(output_file, input_queue):
	''' method handler to write the normalized GCode to the temporary file '''
	out_file = output_file.open()
	while True:
		line = input_queue.get()
		if line == 'done':
			break
		if line == 'unclosed comment error':
			print(line+' encountered. Parsing aborted')
			break
		out_file.write(line+'\n')
		out_file.flush()
	out_file.close()


def normalizer(input_file_name):
	input_file = File(input_file_name, 'r')
	output_file = File('./tmp.txt', 'a+')	
	''' A temporary file (tmp.txt) is created to 
		store the normalized GCode '''

	input_file_handle = input_file.open()

	lines = input_file_handle.readlines()

	manager = mp.Manager()
	queue1 = manager.Queue()
	queue2 = manager.Queue()

	pool = mp.Pool(mp.cpu_count() + 2)

	printer_job = pool.apply_async(print_normalized_output, (output_file, queue2))

	job1 = pool.apply_async(remove_semi_colon_comments, (lines, queue1))
	job2 = pool.apply_async(remove_parenthesis_comments, (queue1, queue2))

	jobs = [job1, job2]

	for job in jobs:
		job.get()

	queue2.put('done')
	pool.close()