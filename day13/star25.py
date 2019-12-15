import numpy as np
from matplotlib.pyplot import *

from intcode import IntcodeComputer

ic = IntcodeComputer()
ic.run()

outputs = np.array(ic.output, dtype='int')
outputs = outputs.reshape((-1, 3))

record = {}

for x, y, t in outputs:
	record[(x, y)] = t

print(np.count_nonzero(np.array(list(record.values())) == 2))

