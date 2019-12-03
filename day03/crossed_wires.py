import numpy as np

def path_instruction_to_inds(path_instruction, cur_ind):
	if path_instruction.split('R')[0]:
		move_distance = path_instruction.split('R')[1]
		x_inds = np.arange(move_distance) + 1 + cur_ind[0]
		y_inds = np.ones_like(move_inds)*cur_ind[1]
	elif path_instruction.split('L')[0]:
		move_distance = path_instruction.split('L')[1]
		x_inds = cur_ind[0] - np.arange(move_distance) - 1
		y_inds = np.ones_like(move_inds)*cur_ind[1]
	elif path_instruction.split('U')[0]:
		move_distance = path_instruction.split('U')[1]
		y_inds = np.arange(move_distance) + 1 + cur_ind[1]
		x_inds = np.ones_like(move_inds)*cur_ind[0]
	elif path_instruction.split('D')[0]:
		move_distance = path_instruction.split('D')[1]
		y_inds = cur_ind[1] - np.arange(move_distance) - 1
		x_inds = np.ones_like(move_inds)*cur_ind[0]
	out_inds = np.transpose(np.vstack((x_inds, y_inds)))
	return out_inds

def intersection_finder(path1_list, path2_list):
	path1_ind_init = np.array([0, 0])
	path2_ind_init = np.array([0, 0])
	path1_list = path1_ind_init
	path2_list = path2_ind_init
	for path1_instruction in path1_list:
		move_inds = path_instruction_to_inds(path1_instruction, path1_ind_init)
		path1_list = np.vstack((path1_list, move_inds))
		path1_ind_init = path1_list[-1, :]
	for path2_instruction in path2_list:
		move_inds = path_instruction_to_inds(path2_instruction, path2_ind_init)
		path2_list = np.vstack((path2_list, move_inds))
		path2_ind_init = path2_list[-1, :]
	return path1_list, path2_list

def main():
	paths_list = np.loadtxt('input1.txt', delimiter=',', dtype='str')
	path1_instruction_list = paths_list[0]
	path2_instruction_list = paths_list[1]
	path1_inds, path2_inds = intersection_finder(path1_instruction_list, path2_instruction_list)



if __name__ == '__main__':
	main()