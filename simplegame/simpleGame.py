import pygame,sys,random
from player import *
from obstacle import *
from population import *
pygame.font.init()

WIDTH,HEIGHT = 600,250
WINDOW = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

FONT = pygame.font.SysFont("comicsans",15)

population = Population(0.05,75,WIDTH,HEIGHT)
best_score = 0

def draw(obstacles):
	global population
	global best_score

	WINDOW.fill((50, 156, 201))

	count = 0
	alive = []
	for player in population.pop:
		if not player.dead:
			player.update(obstacles,WINDOW)
			alive.append(player)
		else:
			count += 1
		if player.points > best_score:
			best_score = player.points

	if count >= len(population.pop):
		population.simulate()
		obstacles.clear()

	points_txt = FONT.render("highest: " + str(best_score),1,(255,255,255))
	WINDOW.blit(points_txt,(500,25))

	gen_txt = FONT.render("gen: " + str(population.gens),1,(255,255,255))
	WINDOW.blit(gen_txt,(20,25))

	for obs in obstacles:
		obs.update(obstacles,alive,WINDOW)

	pygame.display.update()

def main():
	fps = 30
	game_ticks = 0
	obstacles = [Obstacle(WIDTH,HEIGHT)]
	spawn_rate = 60
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
					fps = 30
				else:
					fps = 500

		draw(obstacles)

		game_ticks += 1
		if game_ticks%spawn_rate == 0:
			obstacles.append(Obstacle(WIDTH,HEIGHT))

if __name__ == "__main__":
	main()