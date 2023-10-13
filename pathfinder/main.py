from population import *
from obstacle import*
import pygame,sys
pygame.font.init()

game_ticks = 0

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
FONT = pygame.font.SysFont("arial",20)

WIDTH,HEIGHT = 600,600
WINDOW = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

def draw(current_population,target):
	WINDOW.fill(WHITE)
	target.draw(WINDOW)
	gen_text = FONT.render("Generation: " + str(current_population.gens),1,BLACK)
	WINDOW.blit(gen_text,(450,50))
	current_population.draw_pop(WINDOW)

	closest_dist = 1000000000000000
	closest_rocket = None 

	for i in current_population.pop:
		if i.pos.distance(target.pos) < closest_dist:
			closest_dist = i.pos.distance(target.pos)
			closest_rocket = i

	pygame.draw.line(WINDOW,RED,[target.pos.x,target.pos.y],[closest_rocket.pos.x,closest_rocket.pos.y])

	pygame.display.update()

def simulate(current_population,obstacle):
	global game_ticks
	if game_ticks <= 1500:
		current_population.run(WIDTH,HEIGHT,obstacle)
	else:
		current_population.calc_fitness()
		#current_population.natural_selection()
		current_population.generate()
		game_ticks = 0

def main():
	global game_ticks

	target = Obstacle([550,300])
	mutation_rate = 0.01
	population_num = 100
	target_pos = [target.pos.x,target.pos.y]
	population = Population(population_num,target_pos,mutation_rate)

	while True:
		clock.tick(500)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

		simulate(population,target)
		draw(population,target)

		game_ticks += 1

if __name__ == "__main__":
	main()