import pygame,sys,random
from vector import *
from snake import *
from fruit import *
from population import *

pygame.font.init()

FONT = pygame.font.SysFont("comicsans",15)

GREEN = (0,255,0)
BLACK = (0,0,0)
RED = (255,0,0)
WHITE = (255,255,255)

swidth,sheight = 500,500
window = pygame.display.set_mode((swidth,sheight))
clock = pygame.time.Clock()
cell_size = 10

pop = Population(0.02,150)
snake = pop.simulate() 


def draw(fruits):
	global snake
	global pop
	window.fill(BLACK)
	update = snake.update(window,swidth,sheight,fruits)
	if update == "next":
		snake = pop.simulate()
		fruits[0].next_fruit(fruits,swidth,sheight,(snake.cells[0].rect.x,snake.cells[0].rect.y))
	elif update == "try":
		fruits[0].next_fruit(fruits,swidth,sheight,(snake.cells[0].rect.x,snake.cells[0].rect.y))
	snake.draw(window)
	for fruit in fruits:
		fruit_update = fruit.update(snake,fruits,swidth,sheight,(snake.cells[0].rect.x,snake.cells[0].rect.y))
		if fruit_update == "next":
			snake = pop.simulate()
			fruits[0].next_fruit(fruits,swidth,sheight,(snake.cells[0].rect.x,snake.cells[0].rect.y))
		elif fruit_update == "try":
			fruits[0].next_fruit(fruits,swidth,sheight,(snake.cells[0].rect.x,snake.cells[0].rect.y))
		fruit.draw(window)

	gen_text = FONT.render("generation: " + str(pop.generation),1,WHITE)
	window.blit(gen_text,(20,40))
	snake_num_text = FONT.render("snake: " + str(pop.pop.index(snake)),1,WHITE)
	window.blit(snake_num_text,(150,40))
	pygame.display.update()

def main():
	global game_ticks
	global snake
	global pop
	fps = 500
	fruits = [Fruit(swidth,sheight,(snake.cells[0].rect.x,snake.cells[0].rect.y))]
	playing = False
	while not playing:
		clock.tick(fps)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				for e in pop.pop:
					e.neural_network.save_model()
				pygame.quit()
				sys.exit()

			if event.type == pygame.KEYDOWN:
				if fps == 500:
					fps = 60
				else:
					fps = 500

		draw(fruits)


if __name__ == "__main__":
	main()