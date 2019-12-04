import numpy as np

def main():
	input_nums = np.arange(264793, 803935+1)
	success_counter = 0
	for test_num in input_nums:
		digits_list = np.array([int(d) for d in str(test_num)])
		digits_diff = np.diff(digits_list)
		adjacent_bools = digits_diff==0
		np.insert(adjacent_bools, 0, 0)
		np.append(adjacent_bools, 0)
		searchval = [0,1,0]
		possibles = np.where(adjacent_bools==searchval[0])[0]
		if (digits_diff>=0).all():
			for p in possibles:
				check = adjacent_bools[p:p+3]
				if (check==searchval).all():
					success_counter += 1
					continue
	print("Number of successes=", success_counter)




if __name__ == '__main__':
	main()