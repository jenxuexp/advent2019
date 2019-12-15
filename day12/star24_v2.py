import itertools
import numpy as np


def parse_input(fname, dtype='int64'):
	with open(fname) as f:
		lines = f.readlines()

	xs = np.zeros((4, 1), dtype=dtype)
	ys = np.zeros((4, 1), dtype=dtype)
	zs = np.zeros((4, 1), dtype=dtype)
	for i, line in enumerate(lines):
		moon = [int(x.strip('<>= \nxyz')) for x in line.split(',')]
		xs[i] = moon[0]
		ys[i] = moon[1]
		zs[i] = moon[2]

	return xs, ys, zs

def update_3D(xs, ys, zs, xdots, ydots, zdots):
	# update velocities
	dxdot = np.sign(xs - xs.T).sum(axis=0)
	dxdot.shape = (4, 1)
	xdots += dxdot

	dydot = np.sign(ys - ys.T).sum(axis=0)
	dydot.shape = (4, 1)
	ydots += dydot

	dzdot = np.sign(zs - zs.T).sum(axis=0)
	dzdot.shape = (4, 1)
	zdots += dzdot

	# update positions
	xs += xdots
	ys += ydots
	zs += zdots

def update_1D(xs, xdots):
	# update velocity
	dxdot = np.sign(xs - xs.T).sum(axis=0)
	dxdot.shape = (4, 1)
	xdots += dxdot

	# update positions
	xs += xdots

def run_simulation(fname, t_max=10):
	xs, ys, zs = parse_input(fname)
	xdots = np.zeros((4, 1), dtype='int64')
	ydots = np.zeros((4, 1), dtype='int64')
	zdots = np.zeros((4, 1), dtype='int64')

	t = 0
	while t < t_max:
		update_3D(xs, ys, zs, xdots, ydots, zdots)
		t += 1
	return xs, ys, zs, xdots, ydots, zdots

def check_repeated_1D(xs, xdots, x_inits):
	if not np.all(xdots == 0):
		return False
	return np.all(xs == x_inits)

def find_1D_periods(fname):
	pos_vectors = parse_input(fname)

	periods = []
	i = 0
	for rs in pos_vectors:
		rdots = np.zeros((4, 1), dtype='int64')
		r_inits = rs + 0

		t = 0
		repeated = False
		while not repeated:
			update_1D(rs, rdots)
			t += 1
			repeated = check_repeated_1D(rs, rdots, r_inits)
			if t % 10000 == 0:  #DELME
				print("t = ", t)  #DELME
		print("repeated axis {0} at t = {1}".format(i, t))
		i += 1
		periods.append(t)
	return periods, np.lcm.reduce(periods, dtype='int64')


# run_simulation('input_test1.txt', t_max=1000000)
# run_simulation('input_test2.txt', t_max=100)
# moons = run_simulation('input.txt', t_max=1000)


print(find_1D_periods('input_test1.txt'))
print(find_1D_periods('input_test2.txt'))
print(find_1D_periods('input.txt'))


# xs = np.array([0, 0, 0, 0], dtype='int')





# class Moon:
# 	def __init__(self, position, velocity=[0, 0, 0], dtype='int', name=None):
# 		self.position = np.array(position, dtype=dtype)
# 		self.velocity = np.array(velocity, dtype=dtype)

# 		self.init_position = self.position + 0
# 		self.init_velocity = self.velocity + 0

# 		self.name = name

# 	def __str__(self):
# 		toprint = "pos=<x={0:3}, y={1:3}, z={2:3}>, vel=<x={3:3}, y={4:3}, z={5:3}>"
# 		return toprint.format(*self.position, *self.velocity)

# 	def __repr__(self):
# 		return "<{} (pos={}, vel={})>".format(self.name, self.position, self.velocity)

# 	def total_energy(self):
# 		return np.sum(np.abs(self.position)) * np.sum(np.abs(self.velocity))


# class Moon1D:
# 	def __init__(self, position, velocity=0, dtype='int', name=None):
# 		self.position = int(position)
# 		self.velocity = int(velocity)
# 		self.init_position = int(position)
# 		self.init_velocity = int(velocity)

# 		self.name = name

# 	def __str__(self):
# 		toprint = "pos={0:3}, vel={1:3}"
# 		return toprint.format(self.position, self.velocity)

# 	def __repr__(self):
# 		return "<{} (pos={}, vel={})>".format(self.name, self.position, self.velocity)

# 	# def total_energy(self):
# 	# 	return np.sum(np.abs(self.position)) * np.sum(np.abs(self.velocity))




# def parse_input(fname, dtype='int', make_1D_moons=False):
# 	with open(fname) as f:
# 		lines = f.readlines()

# 	names = ['Io', 'Europa', 'Ganymede', 'Callisto']

# 	moons = []
# 	moons_xs = []
# 	moons_ys = []
# 	moons_zs = []
# 	for i, line in enumerate(lines):
# 		moon = Moon(np.array([int(x.strip('<>= \nxyz')) for x in line.split(',')]), name=names[i])
# 		moons.append(moon)

# 		if make_1D_moons:
# 			moon_x = Moon1D(moon.position[0], name=names[i]+'_x')
# 			moon_y = Moon1D(moon.position[1], name=names[i]+'_y')
# 			moon_z = Moon1D(moon.position[2], name=names[i]+'_z')

# 			moons_xs.append(moon_x)
# 			moons_ys.append(moon_y)
# 			moons_zs.append(moon_z)

# 	if make_1D_moons:
# 		return moons, moons_xs, moons_ys, moons_zs
# 	else:
# 		return moons


# def update(moons, pairs):
# 	update_velocities(pairs)
# 	update_positions(moons)

# def update_velocities(pairs):
# 	for a, b in pairs:
# 		dr = b.position - a.position
# 		dv = np.sign(dr)
# 		a.velocity += dv
# 		b.velocity -= dv

# def update_positions(moons):
# 	for moon in moons:
# 		moon.position += moon.velocity

# def total_energy(moons):
# 	return sum([moon.total_energy() for moon in moons])

# def print_system(moons, t):
# 	print("After {} steps:".format(t))
# 	for moon in moons:
# 		print(moon)
# 	print()

# def run_simulation(fname, t_max=10, verbose_period=None):
# 	moons = parse_input(fname)
# 	pairs = list(itertools.combinations(moons, 2))

# 	t = 0
# 	if verbose_period is not None:
# 		print_system(moons, t)
# 	while t < t_max:
# 		update(moons, pairs)
# 		t += 1
# 		if verbose_period is not None:
# 			if (t % verbose_period) == 0:
# 				print_system(moons, t)
# 	if verbose_period is not None:
# 		print("Total energy = ", total_energy(moons))
# 	return moons

# def check_repeated_1D(moons):
# 	velocities = np.array([moon.velocity for moon in moons], dtype='int')
# 	# print("velocities = ", velocities)  #DELME
# 	if not np.all(velocities == 0):
# 		return False
# 	positions = np.array([moon.position for moon in moons], dtype='int')
# 	init_positions = np.array([moon.init_position for moon in moons], dtype='int')
# 	# print("positions = ", positions)  #DELME
# 	# print("init_positions = ", init_positions)  #DELME
# 	return np.all(positions == init_positions)

# def find_1D_periods(fname):
# 	moons, moons_xs, moons_ys, moons_zs = parse_input(fname, make_1D_moons=True)
# 	pairs_xs = list(itertools.combinations(moons_xs, 2))
# 	pairs_ys = list(itertools.combinations(moons_ys, 2))
# 	pairs_zs = list(itertools.combinations(moons_zs, 2))

# 	axes = ['x', 'y', 'z']
# 	moon_sets = [moons_xs, moons_ys, moons_zs]
# 	pairs = [pairs_xs, pairs_ys, pairs_zs]
# 	periods = []
# 	for i in range(len(axes)):
# 		axis = axes[i]
# 		ms = moon_sets[i]
# 		ps = pairs[i]

# 		t = 0
# 		repeated = False
# 		while not repeated:
# 			update(ms, ps)
# 			t += 1
# 			repeated = check_repeated_1D(ms)
# 			if t % 1000 == 0:  #DELME
# 				print("t = ", t)  #DELME
# 		print("repeated axis {0} at t = {1}".format(axis, t))
# 		periods.append(t)
# 	return np.lcm.reduce(periods)


# # print(find_1D_periods('input_test1.txt'))
# # print(find_1D_periods('input_test2.txt'))
# # print(find_1D_periods('input.txt'))


# # moons = run_simulation('input_test1.txt', t_max=2772, verbose_period=None)
# # moons = run_simulation('input_test2.txt', t_max=10000, verbose_period=None)
# moons = run_simulation('input_test2.txt', t_max=391807628, verbose_period=1000000)

# moons = run_simulation('input.txt', t_max=1000, verbose_period=1000)

