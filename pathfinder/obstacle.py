from vector import *
import pygame

RED = (255,0,0)

class Obstacle:
	def __init__(self,pos):
		self.pos = Vector(pos[0],pos[1])
		self.width = 25
		self.height = 25
		self.rect = pygame.Rect(self.pos.x,self.pos.y,self.width,self.height)
		self.rect.center = (self.pos.x,self.pos.y)

	def draw(self,window):
		pygame.draw.rect(window,RED,self.rect)