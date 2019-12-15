import time

import numpy as np
import matplotlib.pyplot as plt

from intcode import IntcodeComputer

canvas = np.zeros((39, 20), dtype='int')
fig, ax = plt.subplots(num=0)
im = ax.imshow(canvas.T, vmin=0, vmax=4)

paddle_position = 19
target_paddle_position = 19
ball_position = 17
ball_old_position = 17
ball_direction = 1
score = 0
next_input = 0

ic = IntcodeComputer(allow_pausing=True)
ic.code[0] = 2
ic.run(0)
ic.resume(0)
ic.resume(0)
while ic.continue_flag:
	ic.resume(next_input)
	ic.resume(next_input)
	ic.resume(next_input)
	x, y, t = ic.output[-3:]
	if x == -1:
		score = t
		print("score = ", score)
		ax.imshow(canvas.T)
		fig.canvas.draw()	
		plt.pause(.01)

		continue

	canvas[x, y] = t

	if t == 3:
		# ax.imshow(canvas.T)
		# fig.canvas.draw()	
		# plt.pause(.01)

		paddle_position = x
		next_input = np.sign(target_paddle_position - paddle_position)
	elif t == 4:
		# ax.imshow(canvas.T)
		# fig.canvas.draw()	
		# plt.pause(.01)

		ball_old_position = ball_position + 0
		ball_position = x
		ball_direction = np.sign(ball_position - ball_old_position)
		target_paddle_position = ball_position #+ ball_direction
		next_input = np.sign(target_paddle_position - paddle_position)

