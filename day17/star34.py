import numpy as np
from scipy.signal import convolve2d
from matplotlib.pyplot import *

from intcode import IntcodeComputer

ic = IntcodeComputer()
ic.run()

view = [chr(x) for x in ic.output]

print(''.join(view))
print('='*60)
# Part 2
# ========
# main = "A,A,B,C\n"
# a = "R,6,L,12,R,6\n"
# b = "L,12,R,6,L,6\n"
# c = "R,6,R,12,L,12\n"
# continuous_feed = "n\n"

main = "A,B,A,B,C,B,C\n"
a = "R,6,L,6\n"
b = "6,R,6\n"
c = "L,6\n"
continuous_feed = "n\n"


program = [ord(x) for x in main + a + b + c + continuous_feed]
ic2 = IntcodeComputer()
ic2.code[0] = 2
ic2.run(program)

view2 = [chr(x) for x in ic2.output]

print(''.join(view2))

# view_list = ''.join(view).split('\n')

# view_arr = np.array([[(1 if (x == '#') else 0) for x in v] for v in view_list if v],
# 	                dtype='int')

