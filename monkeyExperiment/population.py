import random,math,pygame
from DNA import *
from functools import reduce
pygame.font.init()

FONT = pygame.font.SysFont('comicsans',20)
WHITE = (255,255,255)
BLACK = (0,0,0)

class Population:
	def __init__(self,mutation_rate,n,target):
		self.generations = 0
		self.finished = False
		self.target = target
		self.mutation_rate = mutation_rate

		self.pop = [DNA(len(target)) for i in range(n)]

		self.mating_pool = []

	def calc_fitness(self):
		for e in self.pop:
			e.calc_fitness(self.target)

	def natural_selection(self):
		self.mating_pool = []

		for e in self.pop:
			n = math.floor(100*(e.fitness/max_fitness))
			for j in range(n):
				self.mating_pool.append(e)

	def generate(self,window):
		max_fitness = 0
		for e in self.pop:
			if e.fitness > max_fitness:
				max_fitness = e.fitness

		new_pop = []

		for i in range(len(self.pop)):
			parent_a = self.accept_reject(max_fitness)
			parent_b = self.accept_reject(max_fitness)
			child = parent_a.crossover(parent_b)
			child.mutate(self.mutation_rate)
			new_pop.append(child)
			self.evaluate("".join(child.genes),window)
			if self.finished == True:
				break
		self.pop = new_pop

		self.generations += 1

	def accept_reject(self,max_fitness):
		safe = 0
		while True:
			index = math.floor(random.randint(0,len(self.pop)-1))
			r = random.uniform(0,max_fitness)
			parent = self.pop[index]
			if r < parent.fitness:
				return parent

			safe += 1

			if safe > 10000:
				raise RuntimeError

	def evaluate(self,string,window):
		self.draw(string,window)
		if string == self.target:
			self.finished = True

	def print_(self,string):
		print(string)

	def draw(self,string,window):
		window.fill(WHITE)
		text = FONT.render("current element: " + string,1,BLACK)
		window.blit(text,(50,50))
		gen_text = FONT.render("generation: " + str(self.generations),1,BLACK)
		window.blit(gen_text,(50,100))
		mrate_text = FONT.render("mutation rate: " + str(self.mutation_rate),1,BLACK)
		window.blit(mrate_text,(50,125))
		pop_text = FONT.render("population num: " + str(len(self.pop)),1,BLACK)
		window.blit(pop_text,(50,150))
		pygame.display.update()