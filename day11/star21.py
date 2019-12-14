import numpy as np

from intcode import IntcodeComputer

class Crawler:
	def __init__(self, ic):
		self.ic = ic
		self.dir_dict = {'U': np.array([0, 1], dtype='int'),
					     'D': np.array([0, -1], dtype='int'),
					     'L': np.array([-1, 0], dtype='int'),
					     'R': np.array([1, 0], dtype='int')}
		self.dir_transition = {'U': ('L', 'R'),
		                       'D': ('R', 'L'),
		                       'L': ('D', 'U'),
		                       'R': ('U', 'D')}
		self.direction = 'U'
		self.position = np.array([0, 0], dtype='int')
		self.num_steps = 0
		self.num_unique_painted = 0
		self.record = {}

	def turn(self, mode):
		self.direction = self.dir_transition[self.direction][mode]

	def step(self, input_pair):
		color, mode = input_pair
		if tuple(self.position) not in crawler.record:
			self.num_unique_painted += 1

		self.record[tuple(self.position)] = color
		self.turn(mode)
		self.position += self.dir_dict[self.direction]
		self.num_steps += 1

	def run(self):
		self.ic.run(0)
		self.ic.resume(0)
		pair = self.ic.output[-2:]
		self.step(pair)
		while self.ic.continue_flag:
			try:
				color = self.record[tuple(self.position)]
			except KeyError:
				color = 0
			self.ic.resume(color)
			if not self.ic.continue_flag:
				break
			self.ic.resume(color)
			pair = self.ic.output[-2:]
			self.step(pair)


ic = IntcodeComputer('input.txt', allow_pausing=True)
crawler = Crawler(ic)

crawler.run()

print(crawler.num_unique_painted)