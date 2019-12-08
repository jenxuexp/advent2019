import numpy as np
from matplotlib.pyplot import *

width = 25
height = 6
n_pixe = width*height

with open('input.txt') as f:
	data = f.read()

data = np.array([int(x) for x in data])
data = data.reshape(-1, height, width)

image = np.zeros([height, width])
for i in range(data.shape[1]):
	for j in range(data.shape[2]):
		stack = data[:, i, j]
		imin = np.where(stack != 2)[0][0]
		val = stack[imin]
		image[i, j] = val

imshow(image)
show()