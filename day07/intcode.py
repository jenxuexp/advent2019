import numpy as np


class IntcodeComputer:
	"""
	Initialize computer from __init__ or one of the init methods.

	    ic = IntcodeComputer()

	Then run the program with the run method, which takes the input as an argument.

	    ic.run(1)
	"""
	def __init__(self, fname='input.txt', delimiter=',', dtype='int', allow_pausing=False,
	             name=None, **kwargs):
		if name is not None:
			self.name = name
		if isinstance(fname, list):
			self.initialize_code(fname)
		else:
			self.initialize_code_from_file(fname, delimiter=delimiter, dtype=dtype,
				                           **kwargs)
		self.opcode_dict = {1: self.add,
		                    2: self.multiply,
		                    3: self.input,
		                    4: self.output,
		                    5: self.jump_if_true,
		                    6: self.jump_if_false,
		                    7: self.less_than,
		                    8: self.equals,
		                    99: self.halt}
		self.output = []
		self.allow_pausing = allow_pausing
		self.unpaused_flag = True

	def __str__(self):
		try:
			return "<IC({})>".format(self.name)
		except:
			return "<No Name>"

	# INIT FUNCTIONS
	def initialize_code_from_file(self, fname, delimiter=',', dtype='int', **kwargs):
		"""Initialize the computer with code in file `fname`"""
		self.init_code = np.loadtxt(fname, delimiter=delimiter, dtype=dtype, **kwargs)
		self.code = self.init_code + 0
		self.pointer = 0
		self.continue_flag = True

	def initialize_code(self, code):
		"""Initialize the computer with code in a list `code`"""
		self.init_code = np.array(code, dtype='int')
		self.code = self.init_code + 0
		self.pointer = 0
		self.continue_flag = True

	# MAIN RUN FUNCTION
	def run(self, input_value=None):
		"""Run program with input value `input_value`"""
		self.input = input_value if isinstance(input_value, list) else [input_value]
		while self.continue_flag and self.unpaused_flag:
			full_opcode = self.code[self.pointer]
			toadd = self.operate(full_opcode)  # Do NOT combine with next line -- operate may change pointer
			self.pointer += toadd

	def resume(self, input_value=None):
		"""Resume after a pause."""
		self.unpaused_flag = True
		self.run(input_value)

	# INTERNAL MACHINERY
	def operate(self, full_opcode):
		parameters, opcode = self.parse_full_opcode(full_opcode)
		opfunc = self.opcode_dict[opcode]
		return opfunc(parameters)

	def parse_full_opcode(self, full_opcode):
		parameters = [int(x) for x in str(full_opcode)[:-2][::-1]]
		opcode = int(str(full_opcode)[-2:])
		return parameters, opcode

	def check_modes_length(self, modes, num_args):
		if len(modes) < num_args:
			modes += [0]*(num_args - len(modes))
		return modes

	def follow_pointers(self, modes, num_args, allow_last_to_follow=False):
		modes = self.check_modes_length(modes, num_args)
		if not allow_last_to_follow:
			modes[-1] = 1  # Don't let the last argument follow pointers
		args = self.code[self.pointer+1:self.pointer+1+num_args]
		args = [self.code[args[i]] if (modes[i] == 0) else args[i] for i in range(len(args))]
		return args

	# OPCODE FUNCTIONS
	def add(self, modes=[]):
		args = self.follow_pointers(modes, 3)
		arg1, arg2, output_index = args

		self.code[output_index] = arg1 + arg2
		return 4

	def multiply(self, modes=[]):
		args = self.follow_pointers(modes, 3)
		arg1, arg2, output_index = args

		self.code[output_index] = arg1 * arg2
		return 4

	def input(self, modes=[]):
		arg1 = self.code[self.pointer+1] 

		self.code[arg1] = self.input.pop(0)
		return 2

	def output(self, modes=[]):
		args = self.follow_pointers(modes, 1, True)
		arg1 = args[0]

		self.output.append(arg1)
		if self.allow_pausing:
			self.unpaused_flag = False
		return 2

	def jump_if_true(self, modes=[]):
		args = self.follow_pointers(modes, 2, True)
		arg1, arg2 = args

		if arg1:
			self.pointer = arg2
			return 0
		else:
			return 3

	def jump_if_false(self, modes=[]):
		args = self.follow_pointers(modes, 2, True)
		arg1, arg2 = args

		if not arg1:
			self.pointer = arg2
			return 0
		else:
			return 3

	def less_than(self, modes=[]):
		args = self.follow_pointers(modes, 3)
		arg1, arg2, arg3 = args

		self.code[arg3] = 1 if (arg1 < arg2) else 0
		return 4

	def equals(self, modes=[]):
		args = self.follow_pointers(modes, 3)
		arg1, arg2, arg3 = args

		self.code[arg3] = 1 if (arg1 == arg2) else 0
		return 4

	def halt(self, parameters=[]):
		self.continue_flag = False
		return 1
