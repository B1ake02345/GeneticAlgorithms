from DNA import *
from vector import *
import pygame

GREEN = (0,255,0)

class Rocket:
	def __init__(self,starting_pos):
		self.starting_pos = starting_pos
		self.pos = starting_pos

		self.velocity = Vector(0,0)

		self.dna = DNA()

		self.width = 10
		self.height = 10

		self.rect = pygame.Rect(self.pos.x,self.pos.y,self.width,self.height)
		self.rect.center = (self.pos.x,self.pos.y)

	def calc_fitness(self,target_pos):
		distance = self.pos.distance(Vector(target_pos[0],target_pos[1]))
		self.dna.fitness = 1/distance

	def crossover(self,parent,starting_pos):
		midpoint = random.randint(0,len(self.dna.genes)-1)
		child = Rocket(starting_pos)
		for i in range(len(self.dna.genes)):
			if i > midpoint:
				child.dna.genes[i] = parent.dna.genes[i]
			else:
				child.dna.genes[i] = self.dna.genes[i]

		return child

	def mutate(self,mutation_rate):
		self.dna.mutate(mutation_rate)

	def apply_force(self,swidth,sheight,obstacle):
		if self.rect.colliderect(obstacle.rect):
			self.dna.fitness * 100
		else:
			self.velocity = self.dna.get_vel()
			self.pos.add(self.velocity)

		if self.pos.x >= swidth - self.width/2:
			self.pos.x = swidth - self.width/2
		elif self.pos.x <= self.width/2:
			self.pos.x = self.width/2

		if self.pos.y >= sheight - self.height/2:
			self.pos.y = sheight - self.height/2
		elif self.pos.y <= self.height/2:
			self.pos.y = self.height/2

	def draw(self,window):
		self.rect = pygame.Rect(self.pos.x,self.pos.y,self.width,self.height)
		self.rect.center = (self.pos.x,self.pos.y)
		pygame.draw.ellipse(window,GREEN,self.rect)