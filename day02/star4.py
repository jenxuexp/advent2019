import sys
import numpy as np

def intcode(code):
	ind_list = np.arange(0, len(code), 4)
	for ind in ind_list:
		opcode = code[ind]
		if opcode == 1:
			code[code[ind+3]] = code[code[ind+1]] + code[code[ind+2]]
		elif opcode == 2:
			code[code[ind+3]] = code[code[ind+1]]*code[code[ind+2]]
		else:
			return code
	return code

def main():
	init_code = np.loadtxt('input.txt', delimiter=',', dtype='int')
	init_code = np.array(init_code)
	for noun in range(100):
		for verb in range(100):
			code = init_code + 0
			code[1] = noun
			code[2] = verb
			code = intcode(code)
			if code[0] == 19690720:
				print(100*noun + verb)
				# sys.exit(0)

if __name__ == '__main__':
	main()