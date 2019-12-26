import numpy as np
from scipy.signal import convolve2d
from matplotlib.pyplot import *

from intcode import IntcodeComputer

ic = IntcodeComputer()
ic.run()

view = [chr(x) for x in ic.output]
view_list = ''.join(view).split('\n')
view_arr = np.array([[(1 if (x == '#') else 0) for x in v] for v in view_list if v],
	                dtype='int')
print(''.join(view))
print('='*60)
# Part 2
# ========
# main = "A,A,B,C\n"
# a = "R,6,L,12,R,6\n"
# b = "L,12,R,6,L,6\n"
# c = "R,6,R,12,L,12\n"
# continuous_feed = "n\n"

# R,6,L,6,6,R,6,R,6,L,6,6,R,6,L,6,6
main = "A,B,A,B,C\n"
a = "R\n" # 6,6,R,6,L,6,6
b = "6,L,12,R,6\n"
c = "L,6\n"
continuous_feed = "n\n"


program = [ord(x) for x in main + a + b + c + continuous_feed]
ic2 = IntcodeComputer()
ic2.code[0] = 2
ic2.run(program)

view2 = [chr(x) for x in ic2.output]

print(''.join(view2))

class ScaffoldCrawler:
	def __init__(self, map, init_pos=(16, 0), init_dir = 'U'):
		self.map = map
		self.position = init_pos
		self.direction = init_dir
		self.visited = []
		self.dir_dict = {'L': {'U': 'L',
		                       'R': 'U',
		                       'D': 'R',
		                       'L': 'D'},
		                 'R': {'U': 'R',
		                       'R': 'D',
		                       'D': 'L',
		                       'L': 'U'}}
		self.move_dict = {'U': np.array([-1, 0]),
		                  'R': np.array([0, 1]),
		                  'D': np.array([1, 0]),
		                  'L': np.array([0, -1])}
		self.empty_val = 0
		self.scaffold_val = 1
		self.visited_val = 2
		self.marker_dict = {self.empty_val: '.',  # empty
		                    self.scaffold_val: '#',
		                    self.empty_val + self.visited_val: 'X',
		                    self.scaffold_val + self.visited_val: 'O',
		                    'U': '^',
		                    'R': '>',
		                    'L': '<',
		                    'D': 'v'}

	def process_command(self, cmd):
		if cmd in ('L', 'R'):
			self.direction = self.dir_dict[cmd][self.direction]
		else:
			for i in range(int(cmd)):
				self.position += self.move_dict[self.direction]
				if self.map[tuple(self.position)] < self.visited_val:
					self.map[tuple(self.position)] += self.visited_val

	def process_sequence(self, seq):
		if isinstance(seq, str):
			seq = seq.split(',')
		print("seq = ", seq)
		for cmd in seq:
			self.process_command(cmd)

	def print_map(self):
		pmap = [[self.marker_dict[x] for x in row] for row in self.map]
		dir_marker = self.marker_dict[self.direction]
		x, y = self.position
		pmap[x][y] = dir_marker
		pmap = '\n'.join([''.join(row) for row in pmap]) + '\n'

		print(pmap)
 
sc = ScaffoldCrawler(view_arr)
# sc.process_sequence(['R', '6', 'L', '12', 'R'])
sc.process_sequence('R,6,L,6,6,R,6,R,6,L,6,6,R,6,L,6,6,R,6,L,6,R,6,R,6,6,L,10,L,10,L,6,6,R,6,L,8')
sc.print_map()


# view_list = ''.join(view).split('\n')

# view_arr = np.array([[(1 if (x == '#') else 0) for x in v] for v in view_list if v],
# 	                dtype='int')

