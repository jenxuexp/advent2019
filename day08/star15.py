import numpy as np

width = 25
height = 6
n_pixe = width*height

with open('input.txt') as f:
	data = f.read()

# data = '123456789012'  #DELME
# width = 3  #DELME
# height = 2  #DELME
data = np.array([int(x) for x in data])
data = data.reshape(-1, height, width)

imin = np.argmin((data == 0).sum(1).sum(1))

layer_min = data[imin, :, :]

print((layer_min == 1).sum() * (layer_min == 2).sum())