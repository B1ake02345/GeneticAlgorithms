from rocket import *
from vector import *
import math,pygame

class Population:
	def __init__(self,num,target_pos,mutation_rate):
		self.num = num
		self.target_pos = target_pos
		self.gens = 1

		self.mutation_rate = mutation_rate

		self.pop = [Rocket(Vector(100,100)) for i in range(self.num)]

		self.mating_pool = []

	def run(self,swidth,sheight,obstacle):
		for e in self.pop:
			e.apply_force(swidth,sheight,obstacle)

	def calc_fitness(self):
		for e in self.pop:
			e.calc_fitness(self.target_pos)

	def natural_selection(self):
		self.mating_pool = []

		for e in self.pop:
			n = math.floor(1000*e.dna.fitness)
			for i in range(n):
				self.mating_pool.append(e)

	def generate(self):
		max_fitness = 0
		for e in self.pop:
			if e.dna.fitness > max_fitness:
				max_fitness = e.dna.fitness

		new_pop = []

		for i in range(len(self.pop)):
			parent_a = self.reject_accept(max_fitness)
			parent_b = self.reject_accept(max_fitness)
			child = parent_a.crossover(parent_b,Vector(100,100))
			child.mutate(self.mutation_rate)
			new_pop.append(child)

		self.gens += 1

		self.pop = new_pop


	def reject_accept(self,max_fitness):
		while True:
			parent = random.choice(self.pop)
			r = random.uniform(0,max_fitness)
			if r < parent.dna.fitness:
				return parent



	def draw_pop(self,window):
		for e in self.pop:
			e.draw(window)