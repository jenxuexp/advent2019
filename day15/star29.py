from random import randint

import numpy as np
import matplotlib.pyplot as plt

from intcode import IntcodeComputer


class Crawler:
	def __init__(self, fname='input.txt'):
		self.ic = IntcodeComputer(fname, allow_pausing=True)

		self.history = {(0, 0): 1}
		self.dir_tried = {(0, 0): [0, 0, 0, 0]}  # N, E, S, W

		self.output = -1
		self.itercount = 0
		self.direction = 'N'
		self.position = np.array([0, 0])
		self.dir_dict = {'N': 1,
		                 'S': 2,
		                 'W': 3,
		                 'E': 4}
		self.rev_dir_dict = {1: 'N',
		                     2: 'S',
		                     3: 'W',
		                     4: 'E'}
		self.try_dir_dict = {'N': 0,
		                     'E': 1,
		                     'S': 2,
		                     'W': 3}
		self.rev_try_dir_dict = {0: 'N',
		                         1: 'E',
		                         2: 'S',
		                         3: 'W'}
		self.add_dict = {'N': np.array([0, 1]),
		                 'S': np.array([0, -1]),
		                 'W': np.array([-1, 0]),
		                 'E': np.array([1, 0])}


	def run(self):
		while self.output is not 2:
			# print("iteration", self.itercount)  #DELME
			# Run next step
			print('-'*20)  #DELME
			next_input = self.strategy()
			if self.itercount == 0:
				self.ic.run(next_input)
			else:
				self.ic.resume(next_input)
			self.output = self.ic.output[-1]
			print("new_output = ", self.output)  #DELME


			next_pos = self.position + self.add_dict[self.direction]
			print("next_pos = ", next_pos)  #DELME
			self.history[tuple(next_pos)] = self.output
			self.update_dir_tried()

			if self.output == 1 or self.output == 2:
				self.position = next_pos
			print("new position = ", self.position)  #DELME
			self.itercount += 1
			if self.itercount % 100 == 0:
				plot_maze(self.history)  #DELME
			if self.itercount == 20000:  #DELME
				self.output = 2   #DELME


	def update_dir_tried(self):
		reverse_direction = {0: 2,
		                     1: 3,
		                     2: 0,
		                     3: 1}
		next_pos = self.position + self.add_dict[self.direction]
		dir_index = self.try_dir_dict[self.direction]
		self.dir_tried[tuple(self.position)][dir_index] = 1
		if self.output == 1 or self.output == 2:
			if tuple(next_pos) not in self.dir_tried:
				self.dir_tried[tuple(next_pos)] = [0, 0, 0, 0]
			reverse_index = reverse_direction[dir_index]
			self.dir_tried[tuple(next_pos)][reverse_index] = 1



	def strategy(self):
		tried_list = self.dir_tried[tuple(self.position)]
		try:
			next_dir = tried_list.index(0)
		except ValueError:
			next_dir = randint(0, 3)
		self.direction = self.rev_try_dir_dict[next_dir]
		next_input = self.dir_dict[self.direction]

		print("Iteration:", self.itercount)  #DELME
		print("Position:", self.position)  #DELME
		print("tried_list = ", tried_list)  #DELME
		print("next_input = {0} ({1})".format(next_input, self.direction))  #DELME
		print("old_output = ", self.output)  #DELME
		return next_input

		# transition = {'N': 'E',
		#               'E': 'S',
		#               'S': 'W',
		#               'W': 'N'}
		# if self.output == 0:
		# 	self.direction = transition[self.direction]
		# next_input = self.dir_dict[self.direction]
		# tried_list = self.dir_tried[tuple(self.position)]
		# if tried_list[next_input]:
		# 	try:
		# 		tried_list.index

		# return 

crawler = Crawler()

def make_array_from_record(history):
	xs, ys = np.array(list(history.keys()), dtype='int').T
	xmin = xs.min()
	xmax = xs.max()
	ymin = ys.min()
	ymax = ys.max()
	dx = xmax - xmin + 1
	dy = ymax - ymin + 1

	maze = np.zeros((dx, dy)) - 1

	for (x, y), t in history.items():
		maze[x - xmin, y - ymin] = t
	return maze

def plot_maze(history):
	maze = make_array_from_record(history)
	plt.imshow(maze.T)
	plt.pause(.05)

# ic = IntcodeComputer(allow_pausing=True)
# ic.code[0] = 2
# ic.run(0)
# ic.resume(0)
# ic.resume(0)
# while ic.continue_flag:
# 	ic.resume(next_input)
# 	ic.resume(next_input)
# 	ic.resume(next_input)
# 	x, y, t = ic.output[-3:]
# 	if x == -1:
# 		score = t
# 		print("score = ", score)
# 		ax.imshow(canvas.T)
# 		fig.canvas.draw()	
# 		plt.pause(.01)
