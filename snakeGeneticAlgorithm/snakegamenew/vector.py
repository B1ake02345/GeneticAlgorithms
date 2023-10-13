class Vector:
	def __init__(self,x,y):
		self.x = x
		self.y = y

	def multi(self,val):
		self.x*=val
		self.y*=val

	def div(self,val):
		self.x/=val
		self.x/=val

	def add(self,vector):
		self.x+=vector.x
		self.y+=vector.y

	def sub(self,vector):
		self.x-=vector.x
		self.y-=vector.y

	def set(self,x,y):
		self.x = x
		self.y = y

	def reverse_vector(self):
		self.x = -self.x
		self.y = -self.y

	def normalise(self):
		mag = self.get_magnitude()
		self.x,self.y = self.x/mag,self.y/mag

	def distance(self,vector):
		return ((self.x-vector.x)**2 + (self.y-vector.y)**2)**0.5

	def get_magnitude(self):
		return ((self.x)**2 + (self.y)**2)**0.5