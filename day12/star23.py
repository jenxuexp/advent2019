import itertools
import numpy as np

class Moon:
	def __init__(self, position, velocity=[0, 0, 0], dtype='int', name=None):
		self.position = np.array(position, dtype=dtype)
		self.velocity = np.array(velocity, dtype=dtype)

		self.name = name

	def __str__(self):
		toprint = "pos=<x={0:3}, y={1:3}, z={2:3}>, vel=<x={3:3}, y={4:3}, z={5:3}>"
		return toprint.format(*self.position, *self.velocity)

	def __repr__(self):
		return "<{} (pos={}, vel={})>".format(self.name, self.position, self.velocity)

	def total_energy(self):
		return np.sum(np.abs(self.position)) * np.sum(np.abs(self.velocity))



def parse_input(fname, dtype='int'):
	with open(fname) as f:
		lines = f.readlines()

	names = ['Io', 'Europa', 'Ganymede', 'Callisto']

	moons = []
	for i, line in enumerate(lines):
		moon = Moon(np.array([int(x.strip('<>= \nxyz')) for x in line.split(',')]), name=names[i])
		moons.append(moon)

	return moons


def update(moons, pairs):
	update_velocities(pairs)
	update_positions(moons)

def update_velocities(pairs):
	for a, b in pairs:
		dr = b.position - a.position
		dv = np.sign(dr)
		a.velocity += dv
		b.velocity -= dv

def update_positions(moons):
	for moon in moons:
		moon.position += moon.velocity

def total_energy(moons):
	return sum([moon.total_energy() for moon in moons])

def print_system(moons, t):
	print("After {} steps:".format(t))
	for moon in moons:
		print(moon)
	print()

def run_simulation(fname, t_max=10, verbose_period=None):
	moons = parse_input(fname)
	pairs = list(itertools.combinations(moons, 2))

	t = 0
	if verbose_period is not None:
		print_system(moons, t)
	while t < t_max:
		update(moons, pairs)
		t += 1
		if verbose_period is not None:
			if (t % verbose_period) == 0:
				print_system(moons, t)
	if verbose_period is not None:
		print("Total energy = ", total_energy(moons))
	return moons



run_simulation('input_test1.txt', t_max=10, verbose_period=1)
run_simulation('input_test2.txt', t_max=100, verbose_period=10)
moons = run_simulation('input.txt', t_max=1000, verbose_period=1000)

