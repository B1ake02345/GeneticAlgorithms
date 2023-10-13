from population import *
import pygame,sys
pygame.font.init()

WIDTH,HEIGHT = 750,500
WINDOW = pygame.display.set_mode((WIDTH,HEIGHT))


def setup():
	target = "To-be-or-not-to-be."
	population_num = 200
	mutation_rate = 0.01
	population = Population(mutation_rate,population_num,target)
	return population

def main():
	population = setup()

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
		if not population.finished:
			population.calc_fitness()
			#population.natural_selection()
			population.generate(WINDOW)
		else:
			population.draw(population.target,WINDOW)


if __name__ == "__main__":
	main()