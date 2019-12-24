import numpy as np

# class Component:
# 	def __init__(self, children):
# 		self.children = children

# key = output product, values are (# output, [# input, input product], ...) 
# recipes = {}

def construct_recipe_list(fname):
	with open(fname) as f:
		lines = f.readlines()

	recipes = {}
	for line in lines:
		in_products, out_product = line.strip().split('=>')
		num_out, type_out = out_product.strip().split(' ')
		num_out = int(num_out)

		in_products = in_products.strip().split(',')
		in_products = [in_product.strip().split(' ') for in_product in in_products]
		in_products = [(int(num_in), type_in.strip()) for num_in, type_in in in_products]

		recipes[type_out] = [num_out, in_products]

	return recipes

def compute_ingredients(target, recipes, stockpile=None, num_target=1):
	# print('-'*10)
	# print("need {0} of {1}".format(num_target, target))  #DELME
	# Initialize stockpile to 0 of everything
	if stockpile is None:
		stockpile = {}
		for key in recipes.keys():
			stockpile[key] = 0

	# print("stockpile = ", stockpile)  #DELME
	num_per_reaction, ingredients = recipes[target]
	num_to_make = num_target - stockpile[target]
	if num_to_make < 0:
		stockpile[target] = -num_to_make + 0
		num_to_make = 0
	else:
		stockpile[target] = 0
	num_reactions = int(np.ceil(num_to_make/num_per_reaction))
	num_made = num_reactions*num_per_reaction
	excess_made = num_made - num_to_make
	# print("making {0} ({1} excess) of {2}".format(num_made, excess_made, target))  #DELME
	stockpile[target] += excess_made
	if ingredients[0][1] == 'ORE':
		num_ore = num_reactions*ingredients[0][0]
		# print("consuming {0} ORE".format(num_ore))  #DELME
		return num_ore, stockpile
	else:
		tosum = []
		for num, prod in ingredients:
			num_needed = num_reactions*num
			num_ore, stockpile = compute_ingredients(prod, recipes, stockpile, num_target=num_needed)
			tosum.append(num_ore)
		return int(np.sum(tosum)), stockpile

trillion = 1000000000000

for fname in ['input_test3.txt', 'input_test4.txt', 'input_test5.txt', 'input.txt']:
	print(fname)
	recipes = construct_recipe_list(fname)
	compute_fuel = lambda num_fuel: compute_ingredients('FUEL', recipes, num_target=num_fuel)[0]
	num_fuel = 1
	total_ore = compute_fuel(num_fuel)
	print("Total ORE consumed for 1 fuel = ", total_ore)

	start_fuel = trillion // total_ore  # always undershoots
	fuel = start_fuel + 0
	total_ore = compute_fuel(fuel)
	while total_ore < trillion:
		fuel = 2*fuel
		total_ore = compute_fuel(fuel)
	max_fuel = fuel
	min_fuel = fuel//2

	new_fuel = (max_fuel + min_fuel) // 2
	dfuel = int(np.abs(max_fuel - min_fuel))

	while dfuel != 1:
		total_ore = compute_fuel(new_fuel)
		if total_ore < trillion:
			min_fuel = new_fuel
		else:
			max_fuel = new_fuel
		new_fuel = (max_fuel + min_fuel)//2
		dfuel = int(np.abs(max_fuel - min_fuel))


	print("min fuel = ", min_fuel, compute_fuel(min_fuel))
	print("max fuel = ", max_fuel, compute_fuel(max_fuel))
	print('-'*20)

	fuel = min_fuel - 1000
	total_ore, stockpile = compute_ingredients('FUEL', recipes, num_target=fuel)
	while total_ore < trillion:
		fuel += 1
		total_ore, stockpile = compute_ingredients('FUEL', recipes, stockpile, num_target=fuel)
	fuel -= 1
	print("fuel with stockpiling 1000 = ", fuel)
	print('='*30)



	# stockpile = None
	# for _ in range(1000):
	# 	total_ore, stockpile = compute_ingredients('FUEL', recipes, stockpile, num_target=1)
	# stockpile

	# while total_ore < 1000000000000:
	# 	num_fuel += 1
	# 	total_ore = compute_ingredients('FUEL', recipes, num_target=num_fuel)[0]

	# num_fuel -= 1
	# total_ore = compute_ingredients('FUEL', recipes, num_target=num_fuel)[0]

	# print("Total ORE consumed for {0} fuel = {1}".format(num_fuel, total_ore))
	# print('='*40)

