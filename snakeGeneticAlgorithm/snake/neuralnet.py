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
	def __init__(self,node_num,weights):
		if weights == None:
			self.nodes = [Node() for i in range(node_num)]
		else:
			self.nodes = [Node(weights[i]) for i in range(node_num)]
		self.weights = weights

	def forward_pass(self,inputs):
		self.outputs = []
		for node in range(len(self.nodes)):
			self.outputs.append(self.nodes[node].forward_pass(inputs))

		return self.outputs

	def get_weights(self):
		weights = []
		for node in self.nodes:
			weights.append(node.weights)

		return weights

	def get_weights_biases(self):
		weights_biases = []
		for node in self.nodes:
			weights_biases.append([node.weights,node.bias])
		return weights_biases

class NeuralNetwork:
	def __init__(self,model,weights=None):
		self.directions = [Vector(1,0),Vector(-1,0),Vector(0,1),Vector(0,-1)]
		self.layers = []
		self.weights = weights

		for node_num in range(len(model)):
			if self.weights != None:
				self.layers.append(Layer(model[node_num],self.weights[node_num]))
			else:
				self.layers.append(Layer(model[node_num],self.weights))


	def forward_pass(self,inputs):
		for layer in self.layers:
			output = layer.forward_pass(inputs)

		return output

	def choose_direction(self,inputs,current_direction):
		output = self.forward_pass(inputs)
		direction = self.directions[output.index(max(output))]
		if (direction.x == -current_direction.x and direction.y == current_direction.y) or (direction.x == current_direction.x and direction.y == -current_direction.y) :
			return current_direction
		else:
			return direction

	def get_model(self):
		model = []
		for layer in self.layers:
			model.append(layer.get_weights())

		return model

	def save_model(self):
		full_model = []
		for layer in self.layers:
			full_model.append(layer.get_weights_biases())
		f = open("models.txt","a")
		f.write("\n\n")
		f.write(str(full_model))
		f.close()