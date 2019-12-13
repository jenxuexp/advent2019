from intcode import IntcodeComputer

print('INPUT')
print('='*20)
ic = IntcodeComputer('input.txt', allow_pausing=False)
ic.run([2])
print(ic.output)