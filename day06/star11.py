import numpy as np

class SpaceObject:
	def __init__(self, name):
		self.objects_orbiting = []
		self.objects_orbited = []
		self.num_orbiting = 0
		self.num_orbited = 0
		self.name = name

	def __str__(self):
		return self.name

	def __repr__(self):
		return "SpaceObject({0})".format(self.name)

	def add_orbiting_object(self, new_object):
		self.objects_orbiting.append(new_object)
		self.update_orbiting(new_object.num_orbiting + 1)
		new_object.objects_orbited.append(self)
		new_object.num_orbited += 1

	def update_orbiting(self, num_to_add):
		self.num_orbiting += num_to_add
		for obj in self.objects_orbited:
			obj.update_orbiting(num_to_add)

	def find_top(self):
		"""Find the top of the tree"""
		while len(self.objects_orbited) > 0:
			return self.objects_orbited[0].find_top()
		return self

def parse_map(fname):
	"""
	Returns the instructions for construcing the map as a list of 2-element
	lists. First element is the ORBITED object (parent), second element is
	the ORBITING object (child).

	[[parent1, child1],
	 [parent2, child2],
	 ...]
	"""
	with open(fname) as f:
		data = [line.rstrip().split(')') for line in f.readlines()]
	return data

def create_map(data):
	objects = {}
	for parent_name, child_name in data:
		if parent_name not in objects.keys():
			parent_obj = SpaceObject(parent_name)
			objects[parent_name] = parent_obj
		else:
			parent_obj = objects[parent_name]

		if child_name not in objects.keys():
			child_obj = SpaceObject(child_name)
			objects[child_name] = child_obj
		else:
			child_obj = objects[child_name]

		parent_obj.add_orbiting_object(child_obj)

	return objects

def get_number_of_indirect_and_direct_orbits(objects):
	return np.sum([obj.num_orbiting for obj in objects.values()])

data = parse_map('input.txt')
objects = create_map(data)
print(get_number_of_indirect_and_direct_orbits(objects))