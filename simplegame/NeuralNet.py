import random

class NeuralNet:
	def __init__(self,model):
		self.layers = [Layer(node_num) for node_num in model]

	def forward_pass(self,inputs):
		for layer in self.layers:
			output = layer.forward_pass(inputs)
		return output

	def choose_direction(self,inputs):
		output = self.forward_pass(inputs)
		directions = [5,0,-5]
		return directions[output.index(max(output))]

	def set_weights(self,weights):
		for i in range(len(weights)):
			self.layers[i].set_weights(weights[i])

	def set_biases(self,biases):
		for i in range(len(biases)):
			self.layers[i].set_biases(biases[i])

	def get_weights(self):
		return [layer.get_weights() for layer in self.layers]

	def get_biases(self):
		return [layer.get_biases() for layer in self.layers]

class Layer:
	def __init__(self,node_num):
		self.nodes = [Node() for i in range(node_num)]

	def forward_pass(self,inputs):
		outputs = []
		for node in range(len(self.nodes)):
			outputs.append(self.nodes[node].forward_pass(inputs))

		return outputs

	def set_weights(self,weights):
		for i in range(len(weights)):
			self.nodes[i].weights = weights[i]

	def set_biases(self,biases):
		for i in range(len(biases)):
			self.nodes[i].bias = biases[i]

	def get_weights(self):
		return [node.weights for node in self.nodes]

	def get_biases(self):
		return [node.bias for node in self.nodes]

class Node:
	def __init__(self):
		self.bias = random.random()
		self.weights = []

	def sigmoid(self,value):
		e = 2.71828
		return 1/(1 + (1/e**value))

	def forward_pass(self,inputs):
		if len(self.weights) == 0:
			self.weights = [random.random() for i in range(len(inputs))]

		output = 0.0
		for i in range(len(inputs)):
			output += inputs[i]*self.weights[i]

		output += self.bias
		return self.sigmoid(output)