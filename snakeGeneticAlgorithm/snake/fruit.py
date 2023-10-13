import pygame,random
from vector import *

RED = (255,0,0)
cell_size = 10

class Fruit:
	def __init__(self,swidth,sheight,snake_pos):
		rand_x = random.randint(25,swidth-25)
		rand_y = random.randint(25,sheight-25)
		valid = False
		while not valid:
			if rand_x < snake_pos[0]+20 and rand_x > snake_pos[0]-20 or rand_y < snake_pos[1]+20 and rand_y > snake_pos[1]-20:
				rand_x = random.randint(25,swidth-25)
				rand_y = random.randint(25,sheight-25)
			else:
				valid = True
		self.pos = Vector(rand_y,rand_x)
		self.colour = RED
		self.rect = pygame.Rect(self.pos.x,self.pos.y,cell_size,cell_size)
		self.rect.center = (self.pos.x,self.pos.y)
		self.game_ticks = 0

	def update(self,snake,fruits,swidth,sheight,snake_pos):
		self.game_ticks += 1 
		to_remove = []
		for cell in snake.cells:
			if self.rect.colliderect(cell.rect):
				if self not in to_remove:
					to_remove.append(self)
				fruits.append(Fruit(swidth,sheight,snake_pos))
				snake.add_cell()
				break

		for i in to_remove:
			fruits.remove(i)
		to_remove.clear()

		if self.game_ticks > 500:
			snake.penalties += 1
			return snake.stop_code(swidth,sheight)

	def next_fruit(self,fruits,swidth,sheight,snake_pos):
		fruits.remove(fruits[0])
		fruits.append(Fruit(swidth,sheight,snake_pos))

	def draw(self,window):
		pygame.draw.rect(window,self.colour,self.rect)