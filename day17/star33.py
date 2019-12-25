import numpy as np
from scipy.signal import convolve2d
from matplotlib.pyplot import *

from intcode import IntcodeComputer

ic = IntcodeComputer()
ic.run()

view = [chr(x) for x in ic.output]

print(''.join(view))

view_list = ''.join(view).split('\n')

view_arr = np.array([[(1 if (x == '#') else 0) for x in v] for v in view_list if v],
	                dtype='int')

kernel = np.array([[0, 1, 0],
	               [1, 1, 1],
	               [0, 1, 0]])

w = convolve2d(view_arr, kernel, mode='same')

print(np.dot(*np.where(w == 5)))
