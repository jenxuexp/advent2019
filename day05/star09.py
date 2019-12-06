import numpy as np


class IntcodeComputer:
	def __init__(self, fname='input.txt', delimiter=',', dtype='int', **kwargs):
		if isinstance(fname, list):
			self.initialize_code(fname)
		else:
			self.initialize_code_from_file(fname, delimiter=delimiter, dtype=dtype,
				                           **kwargs)
		self.opcode_dict = {1: self.add,
		                    2: self.multiply,
		                    3: self.input,
		                    4: self.output,
		                    99: self.halt}
		self.output = []

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

	def run(self, input_value=None):
		"""Run program with input value `input_value`"""
		self.input = input_value
		while self.continue_flag:
			full_opcode = self.code[self.pointer]
			self.pointer += self.operate(full_opcode)

	def operate(self, full_opcode):
		parameters, opcode = self.parse_full_opcode(full_opcode)
		opfunc = self.opcode_dict[opcode]
		return opfunc(parameters)

	def parse_full_opcode(self, full_opcode):
		parameters = [int(x) for x in str(full_opcode)[:-2][::-1]]
		opcode = int(str(full_opcode)[-2:])
		return parameters, opcode

	def add(self, modes=[], pointer=None):
		if pointer is None:
			pointer = self.pointer
		num_args = 3
		if len(modes) < num_args:
			modes += [0]*(num_args - len(modes))

		arg1, arg2, output_index = self.code[pointer+1:pointer+1+num_args] 
		if modes[0] == 0:
			arg1 = self.code[arg1]
		if modes[1] == 0:
			arg2 = self.code[arg2]

		print("ADD: args = ", [arg1, arg2, output_index])  #DELME


		self.code[output_index] = arg1 + arg2
		return num_args + 1

	def multiply(self, modes=[], pointer=None):
		if pointer is None:
			pointer = self.pointer
		num_args = 3
		if len(modes) < num_args:
			modes += [0]*(num_args - len(modes))

		arg1, arg2, output_index = self.code[pointer+1:pointer+1+num_args] 
		if modes[0] == 0:
			arg1 = self.code[arg1]
		if modes[1] == 0:
			arg2 = self.code[arg2]
		print("MULTIPLY: args = ", [arg1, arg2, output_index])  #DELME

		self.code[output_index] = arg1 * arg2
		return num_args + 1

	def input(self, modes=[], pointer=None):
		if pointer is None:
			pointer = self.pointer

		arg1 = self.code[pointer+1] 

		self.code[arg1] = self.input
		return 2

	def output(self, modes=[], pointer=None):
		if pointer is None:
			pointer = self.pointer
		num_args = 1
		if len(modes) < num_args:
			modes += [0]*(num_args - len(modes))

		arg1, = self.code[pointer+1:pointer+1+num_args] 
		if modes[0] == 0:
			arg1 = self.code[arg1]

		self.output.append(arg1)
		return num_args + 1

	def halt(self, parameters=[]):
		self.continue_flag = False
		return 1


if __name__ == '__main__':
	ic = IntcodeComputer('input_day02.txt')
	ic.run(1)
	print(ic.output[-1])