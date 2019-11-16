
import random
from math import sin, cos, radians, sqrt, atan2, acos
from copy import deepcopy

#this class represents a particle
class Particle():
	#initialize
	def __init__(self, min_distance=None, max_distance=None, vertex_number=None):
		self.x = 0	#x coordinate of the local origin
		self.y = 0	#y coordinate of the local origin
		#minimum distance of vertex from origin
		if not min_distance:
			self.min_distance = 1
		else:
			self.min_distance = min_distance
		#maximum distance of vertex from origin
		if not min_distance:
			self.max_distance = 1.5
		else:
			self.max_distance = max_distance
		#number of vertices in the particle
		if not vertex_number or vertex_number < 4:
			self.vertex_number = self.get_number_of_vertices(30, 30)
		else:
			self.vertex_number = vertex_number
		self.vertices = []	#this list contains all the vertices in the particle
		#calculate vertices and add them to the particle's list of vertices
		for i in range(self.vertex_number):
			angle = self.get_random_angle(i * 360/self.vertex_number, (i + 1) * 360/self.vertex_number)
			distance = self.get_random_distance_from_origin(self.min_distance, self.max_distance)
			vert_x = cos(radians(angle)) * distance
			vert_y = sin(radians(angle)) * distance
			self.vertices.append([vert_x, vert_y])	#a vertex is represented as a list with an x and y coordinate
		#based on the vertices, calculate a new origin
		self.calculate_new_center()
		#normalize the size of the particle to be 1
		self.normalize()

	#get a random number of vertices
	def get_number_of_vertices(self, min=None, max=None):
		max_min_difference = 6
		if not min and not max:
			min = 4
			max = min + max_min_difference
		if not min or min < 4:
			min = 4
		if not max or max < min:
			max = min + max_min_difference
		return self.get_random_vertex_number(min, max)

	#returns an integer between min and max, each value has equal probability
	def get_random_vertex_number(self, min, max):
		val = random.random()
		return int(val * (max - min) + min)

	#returns a float between min and max, each value has equal probability
	def get_random_angle(self, min, max):
		val = random.random()
		return val * (max - min) + min

	#returns a float between min and max using the beta distribution
	def get_random_distance_from_origin(self, min, max):
		alpha = 1
		beta = 1
		val = random.betavariate(alpha, beta)
		return val * (max - min) + min

	#returns a tuple with the position of the particles local origin
	def get_position(self):
		return (self.x, self.y)

	#set a new origin for the particle, and move all vertices accordingly
	def set_position(self, x, y):
		for v in self.vertices:
			v[0] = v[0] + (x - self.x)
			v[1] = v[1] + (y - self.y)
		self.x = x
		self.y = y

	#returns the list of the particle's vertices
	def get_vertices(self):
		return self.vertices

	#calculates and returns the area of the particle
	#method used: https://en.wikipedia.org/wiki/Shoelace_formula
	def get_area(self):
		x_val = 0
		y_val = 0
		for i in range(len(self.vertices) - 1):
			x_val += self.vertices[i][0] * self.vertices[i+1][1]
			y_val += self.vertices[i][1] * self.vertices[i+1][0]
		x_val += self.vertices[len(self.vertices)-1][0] * self.vertices[0][1]
		y_val += self.vertices[len(self.vertices)-1][1] * self.vertices[0][0]
		val = (x_val - y_val) / 2
		return val

	#scales the particle to the given size, this works, since the size of the particle has been normalized to 1
	def scale(self, multiplier):
		for v in self.vertices:
			v[0] = v[0] * multiplier
			v[1] =v[1] * multiplier

	#calculates a new origin from the vertices
	#method used: https://en.wikipedia.org/wiki/Centroid#Of_a_polygon
	def calculate_new_center(self):
		area = self.get_area()
		x, y = 0, 0
		for i in range(len(self.vertices) - 1):
			x += (self.vertices[i][0] + self.vertices[i+1][0]) * (self.vertices[i][0] * self.vertices[i+1][1] - self.vertices[i][1] * self.vertices[i+1][0])
			y += (self.vertices[i][1] + self.vertices[i+1][1]) * (self.vertices[i][0] * self.vertices[i+1][1] - self.vertices[i][1] * self.vertices[i+1][0])
		x += (self.vertices[len(self.vertices)-1][0] + self.vertices[0][0]) * (self.vertices[len(self.vertices)-1][0] * self.vertices[0][1] - self.vertices[len(self.vertices)-1][1] * self.vertices[0][0])
		y += (self.vertices[len(self.vertices)-1][1] + self.vertices[0][1]) * (self.vertices[len(self.vertices)-1][0] * self.vertices[0][1] - self.vertices[len(self.vertices)-1][1] * self.vertices[0][0])
		x = x * 1 / (6 * area)
		y = y * 1 / (6 * area)
		self.set_position(x, y)

	#calculates the longest distance from the origin to a vertex and returns it
	def get_longest_distance(self):
		val = 0
		for v in self.vertices:
			i = (v[0] - self.x)**2 + (v[1] - self.y)**2
			if i > val:
				val = i
		val = sqrt(val)
		return val

	#returns the distance between the center of this particle and the center of the given particle p
	def get_distance_between_origins(self, p):
		x_val = p.get_position()[0] - self.x
		y_val = p.get_position()[1] - self.y
		val = sqrt(x_val**2 + y_val**2)
		return val

	#normalize the size of the particle to facilitate scaling, this methods sets the width to 1
	def normalize(self):
		#for every vertex in the polygon, create a line to each of the other vertices
		#for each line, rotate the polygon along the line, and calculate the width and height of the excribed rectangle
		#then, choose the minimum value as the width of the particle
		temp = deepcopy(self.get_vertices())
		particle_width = None
		for i in range(len(temp)):
			k = i + 1 if i != len(temp) - 1 else 0
			while k != i:
				#calculate the angle between the vertices
				angle = atan2((temp[k][1] - temp[i][1]), (temp[k][0] - temp[i][0]))
				#create a rotated copy of the polygon
				rotated_vertices = self.get_rotated_copy(angle, temp, temp[i])
				#calculate the dimensions of the excribed rectangle
				dimensions = self.get_dimensions(rotated_vertices)
				if particle_width == None:
					particle_width = dimensions[0]
				if particle_width > dimensions[0]:
					particle_width = dimensions[0]
				if particle_width > dimensions[1]:
					particle_width = dimensions[1]
				k = k + 1 if k != len(temp) - 1 else 0
		#scale the particle so that the size of the width is equal to 1
		self.scale(1 / particle_width)

	#rotate the particle, angle is in degrees
	#method used: https://stackoverflow.com/questions/12161277/how-to-rotate-a-vertex-around-a-certain-point
	def rotate(self, angle):
		for v in self.vertices:
			v[0] = self.x + (v[0] - self.x) * cos(radians(angle)) - (v[1] - self.y) * sin(radians(angle))
			v[1] = self.y + (v[0] - self.x) * sin(radians(angle)) + (v[1] - self.y) * cos(radians(angle))

	#similar to rotate(), but takes a list of vertices as argument and returns a list with rotated vertices around the given point
	#angle is in radians
	def get_rotated_copy(self, angle, vertices, point):
		new_vertices = deepcopy(vertices)
		for v in new_vertices:
			v[0] = point[0] + (v[0] - point[0]) * cos(angle) - (v[1] - point[1]) * sin(angle)
			v[1] = point[1] + (v[0] - point[0]) * sin(angle) + (v[1] - point[1]) * cos(angle)
		return new_vertices

	#returns the width and height of the excribed rectangle of the given set of vertices
	def get_dimensions(self, vertices):
		min_x = vertices[0][0]
		for v in vertices:
			if v[0] < min_x:
				min_x = v[0]
		max_x = vertices[0][0]
		for v in vertices:
			if v[0] > max_x:
				max_x = v[0]
		min_y = vertices[0][1]
		for v in vertices:
			if v[1] < min_y:
				min_y = v[1]
		max_y = vertices[0][1]
		for v in vertices:
			if v[1] > max_y:
				max_y = v[1]
		width = max_x - min_x
		height = max_y - min_y
		return (width, height)

	#outputs vertices in a formatted form
	def print_vertices(self):
		for v in self.vertices:
			print(v)
