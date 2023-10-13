import math,random,os
from vector import *

class Node:
	def __init__(self,weights=None):
		self.bias = random.random()
		self.weights = weights

	def sigmoid(self,value):
		e = 2.71828
		return 1/(1 + (1/e**value))

	def forward_pass(self,inputs):
		self.inputs = inputs
		if self.weights == None:
			self.weights = [random.random() for i in range(len(self.inputs))]
			self.bias = random.random()

		self.output = 0.0

		for i in range(len(self.inputs)):
			self.output += self.inputs[i]*self.weights[i]

		self.output += self.bias

		return self.sigmoid(self.output)

class Layer:
	def __init__(self,node_num):
		self.nodes = [Node() for i in range(node_num)]

	def forward_pass(self,inputs):
		self.outputs = []
		for node in range(len(self.nodes)):
			self.outputs.append(self.nodes[node].forward_pass(inputs))

		return self.outputs

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

class NeuralNetwork:
	def __init__(self,model):
		self.directions = [(1,0),(-1,0),(0,1),(0,-1)]
		self.layers = []

		for node_num in range(len(model)):
			self.layers.append(Layer(model[node_num]))


	def forward_pass(self,inputs):
		for layer in self.layers:
			output = layer.forward_pass(inputs)

		return output

	def choose_direction(self,inputs,current_direction):
		output = self.forward_pass(inputs)
		directions = [(1,0),(-1,0),(0,1),(0,-1)]
		if current_direction == (1,0) or current_direction == (-1,0):
			directions = [(0,1),(0,-1),(1,0),(-1,0)]
		directions.remove((-current_direction[0],-current_direction[1]))
		direction = directions[output.index(max(output))]
		return direction

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