import numpy as np

def main():
	input_nums = np.arange(264793, 803935+1)
	success_counter = 0
	for test_num in input_nums:
		digits_list = np.array([int(d) for d in str(test_num)])
		digits_diff = np.diff(digits_list)
		if (digits_diff==0).any() and (digits_diff>=0).all():
			success_counter += 1
	print("Number of successes=", success_counter)




if __name__ == '__main__':
	main()