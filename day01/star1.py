import numpy as np

def calculate_fuel(mass):
	fuel = mass//3 - 2
	return fuel

data = np.loadtxt('input.txt')
fuel = calculate_fuel(data)
print(fuel.sum())