import pygame,sys,random
from vector import *
from cell import *
from neuralnet import *

class Snake:
	def __init__(self,pos,weights=None):
		self.cell_size = 10
		self.pos = pos
		self.directions = [Vector(1,0),Vector(-1,0),Vector(0,1),Vector(0,-1)]
		self.cells = [Cell(Vector(self.pos.x+(i*self.cell_size),self.pos.y)) for i in range(5)]
		self.current_direction = self.directions[1]
		self.points = 0
		self.speed = 5

		self.neural_network = NeuralNetwork([120,120,4],weights)
		self.fitness = 0
		self.game_ticks = 0

		self.close_encounters = 0
		self.closest_encounter = 100000000
		self.current_fruit = None

		self.deaths = 0
		self.highscore = 0
		self.penalties = 0

	def calc_fitness(self):
		self.fitness = (self.highscore**2)*5000 + 0.01
		self.fitness -= self.deaths*150
		self.fitness -= self.penalties*1000

	def crossover(self,parent):
		a_weights = self.neural_network.get_model()
		b_weights = self.neural_network.get_model()
		child_weights = a_weights
		count = 1
		for i in range(len(a_weights)):
			for j in range(len(a_weights[i])):
				if random.random() < 0.5:
					child_weights[i][j] = b_weights[i][j]

		return Snake(Vector(400,400),child_weights)

	def mutate(self,m_rate):
		model = self.neural_network.get_model()
		for layer in model:
			for node in layer:
				for weight in node:
					if random.random() < m_rate:
						weight = random.random()


	def normalise(self,pos,swidth,sheight):
		new_x = pos[0]/swidth
		new_y = pos[1]/sheight
		return new_x,new_y

	def update(self,window,swidth,sheight,fruits):

		direction = []

		for i in range(4):
			if self.current_direction == self.directions[i]:
				direction.append(1)
			else:
				direction.append(0)


		danger_left,danger_right = self.normalise([self.cells[0].rect.x,swidth-self.cells[0].rect.x],swidth,sheight)
		danger_up,danger_down = self.normalise([self.cells[0].rect.y,sheight-self.cells[0].rect.y],swidth,sheight)
		fruit_left,fruit_right = self.normalise([fruits[0].pos.x-self.cells[0].rect.x,fruits[0].pos.x-self.cells[0].rect.x],swidth,sheight)
		fruit_up,fruit_down = self.normalise([fruits[0].pos.y-self.cells[0].rect.y,fruits[0].pos.y-self.cells[0].rect.y],swidth,sheight)
		right,left,down,up = direction[0],direction[1],direction[2],direction[3]
		params = [danger_left,danger_right,danger_down,danger_up,fruit_left,fruit_right,fruit_up,fruit_down,right,left,down,up]
		self.current_direction = self.neural_network.choose_direction(params,self.current_direction)

		if self.cells[0].rect.x > swidth - self.cell_size/2 or self.cells[0].rect.x < self.cell_size/2 or self.cells[0].rect.y > sheight - self.cell_size/2 or self.cells[0].rect.y < self.cell_size/2:
			return self.stop_code(swidth,sheight)


		self.cells[0].move(self.current_direction,self.speed)
		for i in range(len(self.cells)-1):
			cell = self.cells[(len(self.cells)-i-1)]
			cell.rect.clamp_ip(self.cells[self.cells.index(cell)-1])
			cell.draw(window)

		for cell in self.cells[5::]:
			if self.cells[0].rect.collidepoint(cell.rect.center):
				return self.stop_code(swidth,sheight)

	def stop_code(self,swidth,sheight):
		if self.points > self.highscore:
			self.highscore = self.points
		self.points = 0
		if self.deaths < 10:
			self.deaths += 1
			self.cells[0].rect.update(random.randint(25,swidth-25),random.randint(25,sheight-25),10,10)
			return "try"
		else:
			return "next"

	def add_cell(self):
		self.cells.append(Cell(Vector(self.cells[len(self.cells)-1].pos.x,self.cells[len(self.cells)-1].pos.y)))
		self.points += 1

	def draw(self,window):
		for cell in self.cells:
			cell.draw(window)