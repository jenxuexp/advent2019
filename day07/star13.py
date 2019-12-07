from itertools import permutations

import numpy as np
from intcode import IntcodeComputer


possibilities = permutations([5, 6, 7, 8, 9])
fname = 'input.txt'

# possibilities = [[9,8,7,6,5]]
# fname = 'input_test1.txt'

# possibilities = [[9,7,8,5,6]]
# fname = 'input_test2.txt'


outputs = []
for phases in possibilities:
	ph_A, ph_B, ph_C, ph_D, ph_E = phases
	amp_A = IntcodeComputer(fname, allow_pausing=True, name='amp_A')
	amp_B = IntcodeComputer(fname, allow_pausing=True, name='amp_B')
	amp_C = IntcodeComputer(fname, allow_pausing=True, name='amp_C')
	amp_D = IntcodeComputer(fname, allow_pausing=True, name='amp_D')
	amp_E = IntcodeComputer(fname, allow_pausing=True, name='amp_E')

	amp_A.run([ph_A, 0])
	amp_B.run([ph_B, amp_A.output[-1]])
	amp_C.run([ph_C, amp_B.output[-1]])
	amp_D.run([ph_D, amp_C.output[-1]])
	amp_E.run([ph_E, amp_D.output[-1]])

	while amp_E.continue_flag:
		amp_A.resume([amp_E.output[-1]])
		amp_B.resume([amp_A.output[-1]])
		amp_C.resume([amp_B.output[-1]])
		amp_D.resume([amp_C.output[-1]])
		amp_E.resume([amp_D.output[-1]])

	outputs.append(amp_E.output[-1])

print(max(outputs))

