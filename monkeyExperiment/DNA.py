import random,string

def newChar():
	return random.choice(random.choice([string.ascii_letters,string.punctuation,string.digits]))


class DNA:
	def __init__(self,length):
		self.length = length

		self.genes = []
		self.fitness = 0
		for i in range(self.length):
			self.genes.append(newChar())

	def calc_fitness(self,target):
		score = 0
		for i in range(len(self.genes)):
			if self.genes[i] == target[i]:
				score += 1

		self.fitness = score/len(target)
		(2**self.fitness) + 0.01

	def crossover(self,parent):
		child = DNA(len(self.genes))

		midpoint = random.randint(0,len(self.genes)-1)

		for i in range(len(self.genes)):
			if i > midpoint:
				child.genes[i] = self.genes[i]
			else:
				child.genes[i] = parent.genes[i]

		return child

	def mutate(self,mutation_rate):
		for i in range(len(self.genes)):
			if random.random() < mutation_rate:
				self.genes[i] = newChar()