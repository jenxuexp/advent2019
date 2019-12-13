import itertools
import numpy as np
from numpy.linalg import norm

fnames = ['input_test1.txt', 'input_test2.txt', 'input_test3.txt', 'input_test4.txt', 'input.txt']

def find_best_outpost(fname):
	with open(fname) as f:
		data = [[(char == '#') for char in line.strip()] for line in f.readlines()]
	with open(fname) as f:
		data2 = [[char for char in line.strip()] for line in f.readlines()]


	data = np.array(data, dtype='bool')

	meteors = np.array(list(zip(*np.where(data))))

	num_visible = []
	for meteor in meteors:
		angles = np.arctan2(*(meteors - meteor).T)
		nv = len(np.unique(angles))
		num_visible.append(nv)

	imax = np.argmax(num_visible)
	num_max = num_visible[imax]
	meteor_max = meteors[imax]

	return meteors, imax, meteor_max, num_max

for fname in fnames:
	meteors, imax, meteor_max, num_max = find_best_outpost(fname)

	diffs = meteors - meteor_max
	angles = np.pi/2 + np.arctan2(*(diffs).T)
	angles2 = np.mod(angles, 2*np.pi)
	distances = norm(meteors - meteor_max, axis=1)
	unique_angles = np.unique(angles2)

	dtype = [('index', 'uint'), ('angle', 'float'), ('distance', 'float'), ('location', 'int', (2,))] 
	sarray = np.array(list(zip(range(len(angles2)), angles2, distances, meteors)), dtype=dtype)
	sarray = sarray[sarray['distance'] != 0]

	grouped = []
	for ua in unique_angles:
		group = sarray[sarray['angle'] == ua]
		group.sort(order='distance')
		grouped.append(group)

	ordered = list(itertools.zip_longest(*grouped)) 
	ordered = [[item for item in row if item is not None] for row in ordered]
	flat_ordered = np.array(list(itertools.chain(*ordered)), dtype=dtype)
	try:
		fo199 = flat_ordered[199]
	except:
		fo199 = flat_ordered[-1]

	print(fname)
	print("Meteor {0} at {1} is best with {2} meteors visible.".format(imax, meteor_max[::-1], num_max))
	print("200th (or last if <200) asteroid vaporized is asteroid {} at {}".format(fo199[0], fo199[-1][::-1]))
	print("result = ", fo199[-1][0] + fo199[-1][1]*100)
	print('-'*20)




