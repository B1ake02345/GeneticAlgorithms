import pygame,sys,random
from neuralNet import *
from vector import *
from functools import reduce

DIMENSIONS = 20
CELL_SIZE = 25

BLACK = (0,0,0)
GREEN = (0,255,0)
PURPLE = (89,47,196)
RED = (255,0,0)

class Grid:
	def __init__(self):
		self.grid = [[0 for i in range(DIMENSIONS)] for i in range(DIMENSIONS)]

	def change_cell(self,pos,value):
		self.grid[pos[1]][pos[0]] = value

	def draw(self,window,snake):
		for col in range(DIMENSIONS):
			for row in range(DIMENSIONS):
				rect = pygame.Rect(CELL_SIZE*row,CELL_SIZE*col,CELL_SIZE,CELL_SIZE)
				if self.grid[col][row] == 0:
					colour = BLACK
					pygame.draw.rect(window,colour,rect)
				elif self.grid[col][row] == 1:
					if [row,col] == snake.cells[0].pos:
						colour = PURPLE
					else:
						colour = GREEN

					pygame.draw.ellipse(window,colour,rect)
				elif self.grid[col][row] == 2:
					colour = RED
					pygame.draw.rect(window,colour,rect)

	def reset(self):
		self.grid = [[0 for i in range(DIMENSIONS)] for i in range(DIMENSIONS)]

class Fruit:
	def __init__(self,snake):
		self.snake = snake
		self.pos = [random.randint(0,DIMENSIONS-1),random.randint(0,DIMENSIONS-1)]
		while self.snake.grid.grid[self.pos[1]][self.pos[0]] != 0:
			self.pos = [random.randint(0,DIMENSIONS-1),random.randint(0,DIMENSIONS-1)]
		self.snake.grid.grid[self.pos[1]][self.pos[0]] = 2

		self.game_ticks = 0

	def update(self,fruits):
		self.game_ticks += 1

		if self.snake.cells[0].pos == self.pos:
			self.snake.add_cell()
			self.snake.points += 1
			self.snake.steps.append(self.game_ticks)
			fruits.append(Fruit(self.snake))
			fruits.remove(fruits[0])

		if self.game_ticks > 600:
			self.snake.penalties += 1
			self.snake.steps.append(600)
			return self.snake.death(fruits)

class Cell:
	def __init__(self,pos,current_direction,snake):
		self.pos = pos
		self.current_direction = current_direction
		self.snake = snake

	def new_pos(self,direction,fruits):
		self.current_direction = direction
		if self.pos[0]+self.current_direction[0] < 0:
			self.snake.steps.append(600)
			self.snake.deaths_by_wall += 1
			return self.snake.death(fruits)
		elif self.pos[0]+self.current_direction[0] > DIMENSIONS-1:
			self.snake.steps.append(600)
			self.snake.deaths_by_wall += 1
			return self.snake.death(fruits)

		if self.pos[1]+self.current_direction[1] < 0:
			self.snake.steps.append(600)
			self.snake.deaths_by_wall += 1
			return self.snake.death(fruits)
		elif self.pos[1]+self.current_direction[1] > DIMENSIONS-1:
			self.snake.steps.append(600)
			self.snake.deaths_by_wall += 1
			return self.snake.death(fruits)
		self.pos = [self.pos[0]+self.current_direction[0],self.pos[1]+self.current_direction[1]]

class Snake:
	def __init__(self):
		self.directions = [(1,0),(-1,0),(0,1),(0,-1)]
		self.pos = [random.randint(0,DIMENSIONS-1),random.randint(0,DIMENSIONS-1)]
		self.grid = Grid()
		self.current_direction = random.choice(self.directions)
		self.cells = [Cell(self.pos,self.current_direction,self)]
		self.neural_net = NeuralNetwork([132,132,3])
		self.fitness = 0

		self.deaths = 0
		self.deaths_by_wall = 0

		self.steps = []
		self.highscore = 0
		self.points = 0
		self.penalties = 0

	def calc_fitness(self):
		avg_steps = reduce(lambda a,b: a + b,self.steps)
		self.fitness = self.highscore*5000 - 150*avg_steps - 2000*self.penalties - 500*self.deaths_by_wall

	def crossover(self,parent):
		a_weights = parent.neural_net.get_weights()
		a_biases = parent.neural_net.get_biases()
		b_weights = self.neural_net.get_weights()
		b_biases = self.neural_net.get_biases()

		child_weights = a_weights
		child_biases = a_biases

		for i in range(len(a_weights)):
			for j in range(len(a_weights[i])):
				if random.random() < 0.5:
					child_weights[i][j] = b_weights[i][j]

		for i in range(len(a_biases)):
			for j in range(len(a_biases[i])):
				if random.random() < 0.5:
					child_biases[i][j] = b_biases[i][j]

		child = Snake()
		child.neural_net.set_weights(child_weights)
		child.neural_net.set_biases(child_biases)
		return child

	def mutate(self,m_rate):
		for i in range(len(self.neural_net.get_weights())):
			for j in range(len(self.neural_net.get_weights()[i])):
				if random.random() < m_rate:
					self.neural_net.get_weights()[i][j] = random.random()


	def add_cell(self):
		last_cell = self.cells[-1]
		pos = [last_cell.pos[0]-last_cell.current_direction[0],last_cell.pos[1]-last_cell.current_direction[1]]
		self.cells.append(Cell(pos,last_cell.current_direction,self))

	def update(self,fruits):
		params = []

		# above
		top_left_x = self.cells[0].pos[0] - 1
		top_left_y = self.cells[0].pos[0] - 1
		if top_left_x < 0:
			params.append(-1)
		elif top_left_y < 0:
			params.append(-1)
		elif self.grid.grid[top_left_y][top_left_x] == 0:
			params.append(0)
		elif self.grid.grid[top_left_y][top_left_x] == 1:
			params.append(-1)
		elif self.grid.grid[top_left_y][top_left_x] == 2:
			params.append(1)

		top_left_x = self.cells[0].pos[0]
		top_left_y = self.cells[0].pos[0] - 1
		if top_left_y < 0:
			params.append(-1)	
		elif self.grid.grid[top_left_y][top_left_x] == 0:
			params.append(0)
		elif self.grid.grid[top_left_y][top_left_x] == 1:
			params.append(-1)
		elif self.grid.grid[top_left_y][top_left_x] == 2:
			params.append(1)

		top_left_x = self.cells[0].pos[0] + 1
		top_left_y = self.cells[0].pos[0] - 1
		if top_left_x > DIMENSIONS-1:
			params.append(-1)
		elif top_left_y < 0:
			params.append(-1)		
		elif self.grid.grid[top_left_y][top_left_x] == 0:
			params.append(0)
		elif self.grid.grid[top_left_y][top_left_x] == 1:
			params.append(-1)
		elif self.grid.grid[top_left_y][top_left_x] == 2:
			params.append(1)

		# level

		top_left_x = self.cells[0].pos[0] - 1
		top_left_y = self.cells[0].pos[0]
		if top_left_x < 0:
			params.append(-1)	
		elif self.grid.grid[top_left_y][top_left_x] == 0:
			params.append(0)
		elif self.grid.grid[top_left_y][top_left_x] == 1:
			params.append(-1)
		elif self.grid.grid[top_left_y][top_left_x] == 2:
			params.append(1)

		top_left_x = self.cells[0].pos[0] + 1
		top_left_y = self.cells[0].pos[0]
		if top_left_x > DIMENSIONS-1:
			params.append(-1)
		elif self.grid.grid[top_left_y][top_left_x] == 0:
			params.append(0)
		elif self.grid.grid[top_left_y][top_left_x] == 1:
			params.append(-1)
		elif self.grid.grid[top_left_y][top_left_x] == 2:
			params.append(1)

		# below

		top_left_x = self.cells[0].pos[0] - 1
		top_left_y = self.cells[0].pos[0] + 1
		if top_left_x < 0:
			params.append(-1)
		elif top_left_y > DIMENSIONS-1:
			params.append(-1)	
		elif self.grid.grid[top_left_y][top_left_x] == 0:
			params.append(0)
		elif self.grid.grid[top_left_y][top_left_x] == 1:
			params.append(-1)
		elif self.grid.grid[top_left_y][top_left_x] == 2:
			params.append(1)

		top_left_x = self.cells[0].pos[0]
		top_left_y = self.cells[0].pos[0] + 1
		if top_left_y > DIMENSIONS-1:
			params.append(-1)
		elif self.grid.grid[top_left_y][top_left_x] == 0:
			params.append(0)
		elif self.grid.grid[top_left_y][top_left_x] == 1:
			params.append(-1)
		elif self.grid.grid[top_left_y][top_left_x] == 2:
			params.append(1)

		top_left_x = self.cells[0].pos[0] + 1
		top_left_y = self.cells[0].pos[0] + 1
		if top_left_x > DIMENSIONS-1:
			params.append(-1)
		elif top_left_y > DIMENSIONS-1:
			params.append(-1)
		elif self.grid.grid[top_left_y][top_left_x] == 0:
			params.append(0)
		elif self.grid.grid[top_left_y][top_left_x] == 1:
			params.append(-1)
		elif self.grid.grid[top_left_y][top_left_x] == 2:
			params.append(1)

		x_diff = fruits[0].pos[0] - self.cells[0].pos[0]
		try:
			x_diff = x_diff/abs(x_diff)
		except:
			x_diff = 0

		y_diff = fruits[0].pos[0] - self.cells[0].pos[0]
		try:
			y_diff = y_diff/abs(y_diff)
		except:
			y_diff = 0

		if self.current_direction[0] == -x_diff or self.current_direction[1] == -y_diff:
			params.append(-1)
		elif self.current_direction[0] == x_diff or self.current_direction[1] == y_diff:
			params.append(1)
		else:
			params.append(0)
		
		self.current_direction = self.neural_net.choose_direction(params,self.current_direction)

		for cell in self.cells[::-1]:
			try:
				self.grid.grid[cell.pos[1]][cell.pos[0]] = 0
			except:
				pass
			try:
				index = self.cells.index(cell) -1
				if index == -1:
					raise error
				if cell.new_pos(self.cells[index].current_direction,fruits) == "loss":
					return "loss"
			except:
				if cell.new_pos(self.current_direction,fruits) == "loss":
					return "loss"

		for cell in self.cells:
			for ncell in self.cells:
				if ncell.pos == cell.pos and self.cells.index(ncell) != self.cells.index(cell):
					return self.death(fruits)

			self.grid.grid[cell.pos[1]][cell.pos[0]] = 1

	def death(self,fruits):
		if self.deaths < 10:
			self.deaths += 1
			self.grid.reset()
			if self.points > self.highscore:
				self.highscore = self.points

			self.points = 0
			self.pos = [random.randint(0,DIMENSIONS-1),random.randint(0,DIMENSIONS-1)]
			self.cells = [Cell(self.pos,self.current_direction,self)]

			fruits.append(Fruit(self))
			fruits.remove(fruits[0])
		else:
			return "loss"

	def draw(self,window):
		self.grid.draw(window,self)