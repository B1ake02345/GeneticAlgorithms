import random
from vector import *
from snake import *

class Population:
	def __init__(self,m_rate,pop_size):
		self.pop = [Snake(Vector(400,400)) for i in range(pop_size)]
		self.m_rate = m_rate
		self.current_snake = -1
		self.generation = 1

	def calc_fitness(self):
		for snake in self.pop:
			snake.calc_fitness()

	def calc_prob(self):
		self.snakes = [{"snake":snake,"fitness":snake.fitness} for snake in self.pop]

		total = 0
		for i in range(len(self.snakes)):
			total += self.snakes[i]["fitness"]

		for i in range(len(self.snakes)):
			self.snakes[i]["prob"] = self.snakes[i]["fitness"]/total

	def pick_one(self):
		index = 0
		r = random.random()
		while r > 0:
			r = r - self.snakes[index]["prob"]
			index += 1
		return self.snakes[index-1]

	def repopulate(self):
		new_pop = []

		for i in range(len(self.pop)):
			parent_a = self.pick_one()["snake"]
			parent_b = self.pick_one()["snake"]
			child = parent_a.crossover(parent_b)
			child.mutate(self.m_rate)
			new_pop.append(child)

		self.pop = new_pop

	def simulate(self):
		self.current_snake += 1
		if self.current_snake >= len(self.pop):
			self.calc_fitness()
			self.calc_prob()
			self.repopulate()
			self.current_snake = 0
			self.generation += 1
		return self.pop[self.current_snake]
