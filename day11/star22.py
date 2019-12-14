import numpy as np
from matplotlib.pyplot import *

from intcode import IntcodeComputer

class Crawler:
	def __init__(self, ic, init_color=1):
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
		self.init_color = init_color

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
		self.ic.run(self.init_color)
		self.ic.resume(self.init_color)
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

pixels = np.array(list(crawler.record.keys()))

xmin = np.min(pixels[:, 0])
xmax = np.max(pixels[:, 0])
dx = xmax - xmin + 1

ymin = np.min(pixels[:, 1])
ymax = np.max(pixels[:, 1])
dy = ymax - ymin + 1
print("x: {} -> {}".format(xmin, xmax))
print("y: {} -> {}".format(ymin, ymax))

canvas = np.zeros([dx, dy])
canvas[0 - xmin, 0 - ymin] = 1

for key, value in crawler.record.items():
	x, y = key
	x = x - xmin
	y = y - ymin
	canvas[x, y] = value

figure()
canvas = canvas[:, ::-1]
imshow(canvas.T)


show()