import pygame,random
from functools import reduce

class Obstacle:
	def __init__(self,swidth,sheight):
		self.swidth = swidth
		self.sheight = sheight

		self.width = 25
		self.gap_height = 50

		self.x = 800
		self.y_top = random.randint(0,sheight-100)
		self.y_bottom = self.y_top + self.gap_height

		self.height_bot = sheight - self.y_bottom

		self.top_rect = pygame.Rect(self.x,0,self.width,self.y_top)
		self.bot_rect = pygame.Rect(self.x,self.y_bottom,self.width,self.height_bot)

		self.center = self.y_top + self.gap_height/2

		self.speed = 20

	def update(self,obstacles,players,window):
		self.top_rect.x -= 5
		self.bot_rect.x -= 5
		if self.top_rect.x < 0:
			for player in players:
				player.points += 1
			obstacles.remove(self)

		pygame.draw.rect(window,(255,0,0),self.top_rect)
		pygame.draw.rect(window,(255,0,0),self.bot_rect)