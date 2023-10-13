import pygame,random,sys
from NeuralNet import *

class Player:
	def __init__(self,swidth,sheight):
		self.swidth = swidth
		self.sheight = sheight

		self.x = 20
		self.y = sheight/2
		self.dimensions = 25
		self.rect = pygame.Rect(self.x,self.y,self.dimensions,self.dimensions)
		self.rect.center = (self.rect.x,self.rect.y)

		self.speed = 12

		self.nn = NeuralNet([128,128,3])
		self.points = 0
		self.pos_points = 0

		self.fitness = 0
		self.penalties = 0
		self.same_pos = 0

		self.prev_y = self.y

		self.dead = False

	def calc_fitness(self):
		self.fitness = self.points**4 + 0.01

	def crossover(self,parent):
		a_weights = parent.nn.get_weights()
		a_biases = parent.nn.get_biases()
		b_weights = self.nn.get_weights()
		b_biases = self.nn.get_biases()

		child_weights = a_weights
		child_biases = a_biases

		for i in range(len(a_weights)):
			for j in range(len(a_weights[i])):
				if random.random() < 0.5:
					child_weights[i][j] = b_weights[i][j]
				if random.random() < 0.5:
					child_biases[i][j] = b_biases[i][j]

		child = Player(self.swidth,self.sheight)
		child.nn.set_weights(child_weights)
		child.nn.set_biases(child_biases)
		return child

	def mutate(self,m_rate):
		for i in range(len(self.nn.get_weights())):
			for j in range(len(self.nn.get_weights()[i])):
				if random.random() < m_rate:
					self.nn.get_weights()[i][j] = random.random()

	def manuel_update(self,obstacles,window):
		keys_pressed = pygame.key.get_pressed()
		if keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_w]:
			self.rect.y -= self.speed

		if keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]:
			self.rect.y += self.speed

		if self.rect.y < 0:
			self.rect.y = 0
		elif self.rect.y > self.sheight-self.dimensions:
			self.rect.y = self.sheight-self.dimensions

		for obs in obstacles:
			if self.rect.colliderect(obs.rect):
				pygame.quit()
				sys.exit()

		pygame.draw.rect(window,(0,0,0),self.rect)


	def update(self,obstacles,window):
		try:
			params = [self.rect.x/self.swidth,self.rect.y/self.sheight,obstacles[0].top_rect.x/self.swidth,obstacles[0].center/self.sheight]
		except:
			params = [self.rect.x/self.swidth,self.rect.y/self.sheight,0.0,0.0]
		"""if len(params) < 5:
			for i in range(5-len(params)):
				params.append(0.0)"""

		self.rect.y += self.nn.choose_direction(params)

		if self.rect.y < 0:
			self.rect.y = 0
		elif self.rect.y > self.sheight-self.dimensions:
			self.rect.y = self.sheight-self.dimensions

		"""if self.rect.y == self.prev_y:
			self.same_pos += 1

		if self.same_pos > 30:
			self.penalties += 1
			self.same_pos = 0

		self.prev_y = self.rect.y"""

		for obs in obstacles:
			if self.rect.colliderect(obs.top_rect) or self.rect.colliderect(obs.bot_rect):
				self.dead = True

		pygame.draw.rect(window,(0,0,0),self.rect)