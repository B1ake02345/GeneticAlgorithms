import random,pygame
from player import *

class Population:
	def __init__(self,m_rate,pop_size,swidth,sheight):
		self.pop = [Player(swidth,sheight) for i in range(pop_size)]
		self.m_rate = m_rate

		self.gens = 1

	def calc_fitness(self):
		for player in self.pop:
			player.calc_fitness()

	def calc_prob(self):
		self.calc_fitness()

		self.players = [{"player":player,"fitness":player.fitness} for player in self.pop]

		total = 0
		for i in range(len(self.players)):
			total += self.players[i]["fitness"]

		for i in range(len(self.players)):
			self.players[i]["prob"] = self.players[i]["fitness"]/total

	def pick_one(self):
		index = 0
		r = random.random()
		while r > 0:
			r = r - self.players[index]["prob"]
			index += 1
		return self.players[index-1]

	def repopulate(self):
		new_pop = []

		for i in range(len(self.pop)):
			parent_a = self.pick_one()["player"]
			parent_b = self.pick_one()["player"]
			child = parent_a.crossover(parent_b)
			child.mutate(self.m_rate)
			new_pop.append(child)

		self.pop = new_pop

	def save_model(self):
		with open("models.txt","w") as f:
			for player in self.pop:
				f.write(f"weights: {player.nn.get_weights()}\n\nbiases: {player.nn.get_biases()}\n\n")

			f.close()

	def simulate(self):
		self.calc_prob()
		self.repopulate()
		self.gens += 1