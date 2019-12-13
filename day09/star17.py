from intcode import IntcodeComputer

print('TESTS')
print('='*20)
for fname in ['input_test1.txt', 'input_test2.txt', 'input_test3.txt']:
	ic = IntcodeComputer(fname, allow_pausing=False)
	ic.run()
	print(fname)
	print(ic.output)
	print('-'*10)

print('INPUT')
print('='*20)
ic = IntcodeComputer('input.txt', allow_pausing=False)
ic.run([1])
print(ic.output)