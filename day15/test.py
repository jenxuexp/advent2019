import numpy as np
from sklearn.feature_extraction import image
from sklearn.utils.graph_shortest_path import graph_shortest_path


mya = np.array([[1, 1, 0, 0],
	            [0, 1, 1, 1],
	            [0, 0, 0, 1],
	            [0, 1, 1, 1],
	            [1, 1, 0, 0]])

# graph = image.img_to_graph(mya, return_as=np.ndarray)
# shortest_paths = graph_shortest_path(graph)

graph2 = image.grid_to_graph(*mya.shape, mask=mya, return_as=np.ndarray)
shortest_paths2 = graph_shortest_path(graph2)

mya.shape

def ij_to_flat(i, j, shape):
	num_rows, num_cols = shape
	return i*num_cols + j

def flat_to_ij(flat, shape):
	num_rows, num_cols = shape
	i = flat // num_cols
	j = flat - i*num_cols
	return i, j

def graph_index_to_flat(img):
	return np.where(img.flatten() == 1)[0]

def graph_index_to_ij(img):
	graph_to_flat = graph_index_to_flat(img)
	return [flat_to_ij(x, img.shape) for x in graph_to_flat]

def ij_to_graph_index(img):
	graph_to_ij = graph_index_to_ij(img)
	toret = {}
	for i, pos in enumerate(graph_to_ij):
		toret[pos] = i
	return toret