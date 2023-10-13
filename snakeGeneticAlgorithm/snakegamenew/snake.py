import pygame,sys,random
from neuralNet import *
from vector import *
from functools import reduce
from population import *
from objects import *

pygame.font.init()

FONT = pygame.font.SysFont("arial",10)

DIMENSIONS = 20
CELL_SIZE = 25

BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)
WHITE = (255,255,255)
swidth,sheight = DIMENSIONS*CELL_SIZE + 100,DIMENSIONS*CELL_SIZE
window = pygame.display.set_mode((swidth,sheight))
clock = pygame.time.Clock()

population = Population(0.01,100)
snake = population.simulate()
fruits = [Fruit(snake)]

def draw():
	global snake
	global population
	global fruits
	window.fill(BLACK)
	if snake.update(fruits) == "loss":
		snake = population.simulate()
		fruits.append(Fruit(snake))
		fruits.remove(fruits[0])
	snake.draw(window)
	for fruit in fruits:
		if fruit.update(fruits) == "loss":
			snake = population.simulate()
			fruits.append(Fruit(snake))
			fruits.remove(fruits[0])

	current_snake_text = FONT.render("Snake: " + str(population.current_snake),1,WHITE)
	window.blit(current_snake_text,(swidth-75,100))
	gen_text = FONT.render("Generation: " + str(population.gens),1,WHITE)
	window.blit(gen_text,(swidth-75,50))
	death_text = FONT.render("Deaths: " + str(snake.deaths),1,WHITE)
	window.blit(death_text,(swidth-75,150))
	pygame.display.update()

def main():
	fps = 500
	while True:
		clock.tick(fps)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				population.save_model()
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if fps == 500:
					fps = 120
				elif fps == 120:
					fps = 60
				elif fps == 60:
					fps = 45
				elif fps == 45:
					fps = 30
				elif fps == 30:
					fps = 10
				else:
					fps = 500

		draw()

if __name__ == "__main__":
	main()