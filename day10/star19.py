import numpy as np

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
		nv = len(np.unique(np.arctan2(*(meteors - meteor).T)))
		num_visible.append(nv)

	imax = np.argmax(num_visible)
	num_max = num_visible[imax]
	meteor_max = meteors[imax][::-1]

	return imax, meteor_max, num_max

for fname in fnames:
	imax, meteor_max, num_max = find_best_outpost(fname)
	print(fname)
	print("Meteor {0} at {1} is best with {2} meteors visible.".format(imax, meteor_max, num_max))
	print('-'*20)

