import numpy as np

# base = [0, 1, 0, -1]
pattern = lambda base, outnum: list(np.array([[x]*outnum for x in base], dtype='int').flatten())
# def pattern(base, outnum):
# 	toret = list(np.array([[x]*outnum for x in base], dtype='int').flatten())
# 	if outnum is not 1:
# 		toret = toret[1:]
# 	return toret


def input_to_sequence(signal):
	seq = [int(x) for x in str(signal)]
	return seq

def ffwtff(signal, base=[0, 1, 0, -1]):
	signal = str(signal)
	len_sig = len(signal)
	out_sig = []
	for i in range(1, len_sig+1):
		pat = pattern(base, i)
		len_pat = len(pat)
		pat = pat * (len_sig // len_pat + 1)
		pat = pat[1:len_sig+1]
		val = sum([int(signal[j])*int(pat[j]) for j in range(len_sig)])

		trimmed_val = int(str(val)[-1])
		out_sig.append(str(trimmed_val))
		# if i == 1:  #DELME
		# 	print("pat = ", pat)  #DELME
		# 	print("signal = ", signal)  #DELME
		# 	print("val = ", val)  #DELME
		# 	print("trimmed_val = ", trimmed_val)  #DELME
		# 	print('-'*30)  #DELME

	return ''.join(out_sig)

def ffwtff_n(signal, base=[0, 1, 0, -1], n=1):
	for i in range(n):
		signal = ffwtff(signal, base)
	return signal

test_input = 12345678
test_signals = [test_input]
for i in range(4):
	in_sig = test_signals[-1]
	out_sig = ffwtff(in_sig)
	print("in_sig = ", in_sig)  #DELME
	print("out_sig = ", out_sig)  #DELME
	test_signals.append(out_sig)

test_input2 = 80871224585914546619083218645595
test_input3 = 19617804207202209144916044189917
test_input4 = 69317163492948606335995924319873

# teststr = "test{}: {} becomes {}"
# print(teststr.format(2, test_input2, ffwtff_n(test_input2, n=100)[:8]))
# print(teststr.format(3, test_input3, ffwtff_n(test_input3, n=100)[:8]))
# print(teststr.format(4, test_input4, ffwtff_n(test_input4, n=100)[:8]))

# with open('input.txt') as f:
# 	input_signal = f.read().strip()
# print(teststr.format('input', input_signal, ffwtff_n(input_signal, n=100)[:8]))