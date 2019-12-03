import numpy as np


fname = 'input1.txt'
# import data and split into 2 paths
# paths_list = np.loadtxt('input1.txt', delimiter=',', dtype='str')

with open(fname) as f:
	paths_list = f.readlines()
# paths_list = np.loadtxt('test_input1.txt', delimiter=',', dtype='str')
path1_instruction_list = paths_list[0].rstrip().split(',')
path2_instruction_list = paths_list[1].rstrip().split(',')

# count the number of steps in each wire and figure out the largest step size
num_steps = max(len(path1_instruction_list), len(path2_instruction_list))
# paths_list2 = np.char.lstrip(paths_list, 'RLUD')
paths1_step_sizes = [int(val.lstrip('RLUD')) for val in path1_instruction_list]
paths2_step_sizes = [int(val.lstrip('RLUD')) for val in path2_instruction_list]
paths_step_sizes = paths1_step_sizes + paths2_step_sizes
max_step = np.max(paths_step_sizes)
# max_step = paths_list2.astype('int').max()

# num_steps * largest_step is the furthest we could get out
max_extent = num_steps*max_step

# encode steps as x*base + y, where base is 3 orders of magnitude larger than max_extent
base = int(10**(np.ceil(np.log10(max_extent)) + 3))

def encoded_to_pair(value, base=base):
	x = round(value/base)
	y = value - x*base
	return x, y

def L1_norm(pair):
	return np.abs(pair[0]) + np.abs(pair[1])

def operate_L(step_size, start, start_length):
	encoded_to_extend = range(start, start - (step_size+1)*base, -base)[1:]
	length_to_extend = range(start_length, start_length + step_size+1)[1:]
	return encoded_to_extend, length_to_extend

def operate_R(step_size, start, start_length):
	encoded_to_extend = range(start, start + (step_size+1)*base, base)[1:]
	length_to_extend = range(start_length, start_length + step_size+1)[1:]
	return encoded_to_extend, length_to_extend

def operate_U(step_size, start, start_length):
	encoded_to_extend = range(start, start + step_size + 1, 1)[1:]
	length_to_extend = range(start_length, start_length + step_size+1)[1:]
	return encoded_to_extend, length_to_extend

def operate_D(step_size, start, start_length):
	encoded_to_extend = range(start, start - step_size - 1, -1)[1:]
	length_to_extend = range(start_length, start_length + step_size+1)[1:]
	return encoded_to_extend, length_to_extend

op_dict = {'L': operate_L,
           'R': operate_R,
           'U': operate_U,
           'D': operate_D}

def path_list_to_wire_values(instruction_list):
	wire = [0]
	wire_length = [0]
	for instruction in instruction_list:
		op = instruction[0]
		step_size = int(instruction.lstrip('RLUD'))
		op_func = op_dict[op]
		to_extend, to_extend_length = op_func(step_size, wire[-1], wire_length[-1])
		print("current end = ", encoded_to_pair(wire[-1]))  #DELME
		print("current length = ", wire_length[-1])  #DELME
		print ("op = ", op, step_size)  #DELME
		wire.extend(to_extend)
		wire_length.extend(to_extend_length)
		print(to_extend_length)  #DELME
		print("new end = ", encoded_to_pair(wire[-1]))  #DELME
		print("new length = ", wire_length[-1])  #DELME

	wire = wire[1:]  # remove the origin, since it messes with the intersection finder
	wire_length = wire_length[1:]
	return wire, wire_length


wire1, wire_length1 = path_list_to_wire_values(path1_instruction_list)
wire2, wire_length2 = path_list_to_wire_values(path2_instruction_list)

# WAAAAAAY too slow
# print("leni = ", len(wire1))  #DELME
# print("lenj = ", len(wire2))  #DELME
# intersections = []
# for i, val1 in enumerate(wire1):
# 	print("i = ", i)  #DELME
# 	for j, val2 in enumerate(wire2):
# 		if val1 == val2:
# 			intersections.append((i, j))


wire1_unique = set(wire1)
wire2_unique = set(wire2)

wire_intersections = list(wire1_unique.intersection(wire2_unique))

wire_nd1 = np.array(wire1, dtype='int64')
wire_nd2 = np.array(wire2, dtype='int64')

wire_intersections_lengths = []
for wi in wire_intersections:
	wi_ind1s = np.where(wire_nd1 == wi)[0]
	wi_ind2s = np.where(wire_nd2 == wi)[0]

	wlen1 = min([wire_length1[x] for x in wi_ind1s])
	wlen2 = min([wire_length2[x] for x in wi_ind2s])
	wire_intersections_lengths.append(wlen1 + wlen2)



# wire_intersections_mask1 = np.isin(wire1, wire2)
# wire_intersections_mask2 = np.isin(wire2, wire1)

# wire_intersections = [encoded_to_pair(val) for val in wire_intersections]

# L1s = [L1_norm(pair) for pair in wire_intersections]

nearest = np.min(wire_intersections_lengths)

print(nearest)