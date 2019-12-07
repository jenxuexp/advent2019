from itertools import permutations

import numpy as np
from intcode import IntcodeComputer


possibilities = permutations([0, 1, 2, 3, 4])

outputs = []
for phases in possibilities:
	ph_A, ph_B, ph_C, ph_D, ph_E = phases
	amp_A = IntcodeComputer('input.txt')
	amp_B = IntcodeComputer('input.txt')
	amp_C = IntcodeComputer('input.txt')
	amp_D = IntcodeComputer('input.txt')
	amp_E = IntcodeComputer('input.txt')

	amp_A.run([ph_A, 0])
	amp_B.run([ph_B, amp_A.output[0]])
	amp_C.run([ph_C, amp_B.output[0]])
	amp_D.run([ph_D, amp_C.output[0]])
	amp_E.run([ph_E, amp_D.output[0]])

	outputs.append(amp_E.output[0])

print(max(outputs))