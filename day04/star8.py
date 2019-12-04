import numpy as np

def main():
	input_nums = np.arange(264793, 803935+1)
	success_counter = 0
	for test_num in input_nums:
		digits_list = np.array([int(d) for d in str(test_num)])
		digits_diff = np.diff(digits_list)
		adjacent_bools = digits_diff==0
		adjacent_bools = np.insert(adjacent_bools, 0, 0)
		adjacent_bools = np.append(adjacent_bools, 0)
		searchval = [0,1,0]
		possibles = np.where(adjacent_bools==searchval[0])[0]
		if (digits_diff>=0).all():
			# print("test_num = ", test_num)  #DELME
			# print("digits_dff = ", digits_diff)  #DELME
			# print("adjacent_bools = ", adjacent_bools)  #DELME
			# print("possibles = ", possibles)  #DELME
			for p in possibles:
				check = adjacent_bools[p:p+3]
				# print("check = ", check)  #DELME
				if np.all(check==searchval):
					success_counter += 1
					break
	print("Number of successes=", success_counter)




if __name__ == '__main__':
	main()