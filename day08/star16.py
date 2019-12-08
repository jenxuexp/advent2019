import numpy as np

width = 25
height = 6
n_pixe = width*height

with open('input.txt') as f:
	data = f.read()

data = np.array([int(x) for x in data])
data = data.reshape(-1, height, width)

