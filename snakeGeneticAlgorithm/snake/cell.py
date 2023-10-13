import pygame

GREEN = (0,255,0)

class Cell:
	def __init__(self,pos):
		cell_size = 10
		self.pos = pos
		self.rect = pygame.Rect(self.pos.x,self.pos.y,cell_size,cell_size)
		self.rect.center = (self.pos.x,self.pos.y)

	def move(self,direction,speed):
		self.rect.move_ip(direction.x*speed,direction.y*speed)

	def draw(self,window):
		pygame.draw.rect(window,GREEN,self.rect)