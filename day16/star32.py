import itertools
import operator

import numpy as np
import matplotlib.pyplot as plt

base = [0, 1, 0, -1]
pattern = lambda base, outnum: list(np.array([[x]*outnum for x in base], dtype='int').flatten())
def pattern2(base, outnum):
	rep = lambda x: itertools.repeat(x, outnum)
	return itertools.cycle(itertools.chain(*map(rep, base)))

def pattern_array(base, outnum, len_sig):
	pat = pattern2(base, outnum)
	next(pat)
	return np.fromiter(pat, dtype='int8', count=len_sig)

def pattern_matrix(base, len_sig, dtype='int16'):
	return np.array([pattern_array(base, i+1, len_sig) for i in range(len_sig)], dtype=dtype)

def fast_dot(vec1, vec2, num=None):
	if num is None:
		return sum(map(operator.mul, vec1, vec2))
	else:
		return sum(map(operator.mul, itertools.islice(vec1, num), itertools.islice(vec2, num)))

def input_to_sequence(signal):
	seq = [int(x) for x in str(signal)]
	return itertools.cycle(seq)

def ffwtff(signal, base=[0, 1, 0, -1], repeat=1, dtype='int64'):
	len_sig = len(str(signal))*repeat
	# print("len_sig = ", len_sig)  #DELME
	signal = input_to_sequence(signal)
	sig_array = np.fromiter(signal, dtype=dtype, count=len_sig)
	# print("sig_array = ", sig_array)  #DELME
	# print("sig_array.shape = ", sig_array.shape)  #DELME
	out_sig = []
	for i in range(len_sig):
		pat = pattern2(base, i+1)
		next(pat)
		pat_array = np.fromiter(pat, dtype=dtype, count=len_sig)

		val = np.dot(sig_array, pat_array)

		trimmed_val = int(str(val)[-1])
		out_sig.append(str(trimmed_val))

	return ''.join(out_sig)

def _ffwtff(sig_array, base=[0, 1, 0, -1], dtype='int64'):
	print("sig_array = ", sig_array)  #DELME
	print("sig_array.shape = ", sig_array.shape)  #DELME
	out_sig = []
	len_sig = len(sig_array)
	for i in range(len_sig):
		pat = pattern2(base, i+1)
		next(pat)
		pat_array = np.fromiter(pat, dtype=dtype, count=len_sig)

		val = np.dot(sig_array, pat_array)

		trimmed_val = int(str(val)[-1])
		out_sig.append(str(trimmed_val))

	return ''.join(out_sig)


def ffwtff_n(signal, base=[0, 1, 0, -1], n=1, repeat=1, dtype='int64'):
	len_sig = len(str(signal))*repeat
	signal = input_to_sequence(signal)
	sig_array = np.fromiter(signal, dtype=dtype, count=len_sig)
	for i in range(n):
		signal = _ffwtff(sig_array, base, repeat, dtype=dtype)
	return signal

def _ffwtff_n(sig_array, base=[0, 1, 0, -1], n=1, dtype='int64'):
	for i in range(n):
		signal = _ffwtff(sig_array, base, dtype=dtype)
	return signal


def decode(signal, repeat=10000, n=100, dtype='int64'):
	len_sig = len(str(signal))*repeat
	signal = input_to_sequence(signal)
	sig_array = np.fromiter(signal, dtype=dtype, count=len_sig)
	output = _ffwtff_n(sig_array, n=n, dtype=dtype)
	offset = int(output[:7])
	decoded = output[offset:offset+8]
	return decoded

test_input = 12345678
# test_signals = [test_input]
# for i in range(4):
# 	in_sig = test_signals[-1]
# 	out_sig = ffwtff(in_sig)
# 	print("in_sig = ", in_sig)  #DELME
# 	print("out_sig = ", out_sig)  #DELME
# 	test_signals.append(out_sig)

test_input2 = 80871224585914546619083218645595
test_input22 = 8087122458591454661908321864559580871224585914546619083218645595
test_input3 = 19617804207202209144916044189917
test_input4 = 69317163492948606335995924319873

# teststr = "test{}: {} becomes {}"
# print(teststr.format(2, test_input2, ffwtff_n(test_input2, n=100)[:8]))
# print(teststr.format(3, test_input3, ffwtff_n(test_input3, n=100)[:8]))
# print(teststr.format(4, test_input4, ffwtff_n(test_input4, n=100)[:8]))

with open('input.txt') as f:
	input_signal = f.read().strip()
# print(teststr.format('input', input_signal, ffwtff_n(input_signal, n=100)[:8]))

decode(test_input22, repeat=1, n=2)
# print('='*50)
decode(test_input2, repeat=2, n=2)