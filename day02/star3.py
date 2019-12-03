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
	code = np.loadtxt('input.txt', delimiter=',', dtype='int')
	code = np.array(code)
	code[1] = 12
	code[2] = 2
	code = intcode(code)
	print(code[0])

if __name__ == '__main__':
	main()