import numpy as np

def calculate_fuel(mass):
	fuel = mass//3 - 2
	fuel = 0 if fuel <= 0 else fuel
	return fuel
calculate_fuel = np.vectorize(calculate_fuel)

data = np.loadtxt('input.txt')
fuel = calculate_fuel(data)
total_fuel = 0
fuel_sum = fuel.sum(0)
while fuel_sum > 0:
	total_fuel += fuel_sum
	fuel = calculate_fuel(fuel)
	fuel_sum = fuel.sum()

print(total_fuel)