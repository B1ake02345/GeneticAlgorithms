from vector import*
from rocket import*
import random

def random_vector():
	return Vector(random.uniform(-1,1),random.uniform(-1,1))

class DNA:
	def __init__(self):
		self.fitness = 0
		self.genes = [random_vector() for i in range(100)]
		self.current_movement = 0

	def mutate(self,mutation_rate):
		for i in range(len(self.genes)):
			if random.random() < mutation_rate:
				self.genes[i] = random_vector()

	def get_vel(self):
		if self.current_movement + 1 > len(self.genes)-1:
			self.current_movement = 0
		else:
			self.current_movement += 1
		return self.genes[self.current_movement]