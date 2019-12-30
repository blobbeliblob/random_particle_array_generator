#Author: Camilo Hernandez

import random
import time
from particle import Particle
from plot import Plot
from shapely.geometry import Polygon

#this class handles the generation of particles
class Generator():
	#initialize the class
	#boundaries = (x1, y1, x2, y2)
	#filled = amount of specimen area that is filled with particles, given as fraction
	#particle_constraints = (minimum_radius, maximum_radius, number_of_vertices)
	#debug = display the progress when the program is running
	def __init__(self, gradation, boundaries, filled, particle_constraints, allowed_amount_of_fails, debug=False):
		#######################
		#	MAIN PROGRAM
		#######################
		#normalize the gradation to make the sum of sieve percentages add up to 100 %
		diff = 1.00 - gradation[len(gradation)-1][1]
		for fraction in gradation:
			fraction[1] = fraction[1] / diff
		#convert the gradation to be a list of percentage retained
		temp_var_a = 0
		for i in range(len(gradation)):
			gradation[i][1] = 1.00 - gradation[i][1] - temp_var_a
			temp_var_a += gradation[i][1]
		gradation = gradation[::-1]	#reverse the list
		self.gradation = gradation	#set the gradation
		#specimen boundaries, given as millimeters
		self.x1, self.y1 = boundaries[0], boundaries[1]
		self.x2, self.y2 = boundaries[2], boundaries[3]
		#area of the specimen and area filled with particles
		self.filled = filled
		self.total_area = (self.x2 - self.x1) * (self.y2 - self.y1)
		self.filled_area = self.filled * self.total_area
		#minimum and maximum radius when generating vertices for the particles using polar coordinates
		self.min_radius = particle_constraints[0]
		self.max_radius = particle_constraints[1]
		#number of vertices in the generated particles, leave as None for randomized
		self.v_num = particle_constraints[2]
		#display the progress when the program is running
		self.debug = debug
		#list of particles to be generated and placed
		self.particles = []
		#number of permitted tries to find a placement for a new particle before deeming the generation unsuccessful
		self.allowed_amount_of_fails = allowed_amount_of_fails
		#######################
		#	STATISTICS
		#######################
		#list of the amount to be filled for each sieve size, used in statistics
		self.to_be_filled = []
		#list of the amount left unfilled for each sieve size, used in statistics
		self.left_unfilled = []
		#list of number of particles generated for each sieve size, used in statistics
		self.number_of_particles = []
		#number of particles that are of the wrong size, used in statistics
		self.wrong_size = 0
		#time to execute generation
		self.exec_time = 0
		#######################
		#	OUTPUT
		#######################
		#what contents should be written to the readable file
		self.write_labels = True
		self.write_center = True
		self.write_vertices = True
		self.write_area = True
		self.write_width = True
		self.write_longest_distance = True

	#returns true if a new particle p can be placed at coordinates (x, y)
	def check_insert_point(self, p):
		#check if the new particle is fully inside the specimen
		for v in p.get_vertices():
			if v[0] < self.x1 or v[0] > self.x2 or v[1] < self.y1 or v[1] > self.y2:
				return False
		#for each existing particle, check if the new particle is in its close vicinity,
		#if it is, check if any of the new particles vertices are inside the other particle
		for particle in self.particles:
			if particle.get_longest_distance() + p.get_longest_distance() > p.get_distance_between_origins(particle):
				vertices = particle.get_vertices()
				pv = p.get_vertices()
				for ind in range(len(pv)):
					v = pv[ind]
					c = False
					i = 0
					j = len(vertices) - 1
					while i < len(vertices):
						if ((vertices[i][1] > v[1]) != (vertices[j][1] > v[1])) and (v[0] < (vertices[j][0] - vertices[i][0]) * (v[1] - vertices[i][1]) / (vertices[j][1] - vertices[i][1]) + vertices[i][0]):
							c = not c
						j = i
						i = i + 1
					if c:
						return False
		#check polygon intersection using the shapely library
		polygon_1 = Polygon(p.get_vertices())
		for particle in self.particles:
			polygon_2 = Polygon(particle.get_vertices())
			if polygon_1.intersects(polygon_2):
				return False
		return True

	#generates a random aggregate microstructure within the given boundaries of the specimen
	#returns True if successful, else False
	def generate(self):
		#initialize timer
		init_time = time.time()
		#reset lists
		self.particles = []
		self.to_be_filled = []
		self.left_unfilled = []
		self.number_of_particles = []
		self.wrong_size = 0
		#generate
		for i in range(len(self.gradation) - 2, -1, -1):	#for each sieve size
			area_to_be_filled = self.gradation[i][1] * self.filled_area	#the area that should be filled by particles of the current sieve size
			self.to_be_filled.append([self.gradation[i][0], self.gradation[i][1] * self.filled_area])	#used in statistics
			self.left_unfilled.append([self.gradation[i][0], self.gradation[i][1] * self.filled_area])	#used in statistics
			self.number_of_particles.append([self.gradation[i][0], 0])	#used in statistics
			particle_size = random.random() * (self.gradation[i+1][0] - self.gradation[i][0]) + self.gradation[i][0]	#get a random particle size for the current sieve size
			particle = Particle(self.min_radius, self.max_radius, self.v_num)	#create a new particle (polygon)
			particle.scale(particle_size)	#scale the particle to the correct size
			area = particle.get_area()	#get the area of the new particle
			while area < area_to_be_filled:
				#keep generating (x, y) coordinates until they are valid for insertion,
				#then insert the particle into the list of placed particles
				x = random.random() * (self.x2 - self.x1) + self.x1
				y = random.random() * (self.y2 - self.y1) + self.y1
				particle.set_position(x, y)
				failed_tries = 0
				while not self.check_insert_point(particle):
					failed_tries += 1
					if failed_tries > self.allowed_amount_of_fails:
						return False
					x = random.random() * (self.x2 - self.x1) + self.x1
					y = random.random() * (self.y2 - self.y1) + self.y1
					particle.set_position(x, y)
				self.particles.append(particle)
				area_to_be_filled -= area	#subtract the area of the placed particle from the area that needs to be filled
				if self.debug:
					print('Size: ' + str(self.gradation[i][0]) + ' mm\tProgress:' + "{:0.2f}".format(int(self.to_be_filled[len(self.gradation)-2-i][1]-self.left_unfilled[len(self.gradation)-2-i][1]) / int(self.to_be_filled[len(self.gradation)-2-i][1]) * 100) + " %" + '\tParticles: ' + str(self.number_of_particles[len(self.gradation)-2-i][1]), end='\r')
				#used in statistics
				self.left_unfilled[len(self.gradation)-2-i][1] -= area
				self.number_of_particles[len(self.gradation)-2-i][1] += 1
				if particle.get_width() < self.gradation[i][0] or particle.get_width() > self.gradation[i+1][0]:
					self.wrong_size += 1
				#generate the following particle
				particle_size = random.random() * (self.gradation[i+1][0] - self.gradation[i][0]) + self.gradation[i][0]
				particle = Particle(self.min_radius, self.max_radius, self.v_num)
				particle.scale(particle_size)
				area = particle.get_area()
			if self.debug:
				print('Size: ' + str(self.gradation[i][0]) + ' mm\tProgress:' + "{:0.2f}".format(int(self.to_be_filled[len(self.gradation)-2-i][1]-self.left_unfilled[len(self.gradation)-2-i][1]) / int(self.to_be_filled[len(self.gradation)-2-i][1]) * 100) + " %" + '\tParticles: ' + str(self.number_of_particles[len(self.gradation)-2-i][1]))
		#time it took to execute the generation of the particles
		self.exec_time = time.time() - init_time
		if self.debug:
			print("\nGenerating the particles took " + "{:0.2f}".format(self.exec_time) + " seconds\n")
		return True

	#return the generated particles
	def get_particles(self):
		return self.particles

	#write statistics to the give file
	def write_statistics_to_file(self, file):
		p_str = "Time to execute:\t" + str(self.exec_time) + " seconds\n\n"
		file.write(p_str)
		p_str = "Particles generated:\n"
		p_sum = 0
		for p in self.number_of_particles:
			p_sum += p[1]
		for p in self.number_of_particles:
			p_str += "\tSize:\t" + str(p[0]) + " mm\tNumber:\t" + str(p[1]) + "\tPercentage:\t" + str(p[1]/p_sum*100) + "\n"
		p_str += "\nTotal number of particles:\t" + str(p_sum) + "\n\n"
		file.write(p_str)
		p_str = "Filled area:\n"
		p_tot_unfilled = 0
		for i in range(len(self.left_unfilled)):
			p_tot_unfilled += self.left_unfilled[i][1]
			p_str += "\tSize:\t" + str(self.left_unfilled[i][0]) + " mm\tTo be filled:\t" + str(self.to_be_filled[i][1]) + "\tFilled:\t" + str(self.to_be_filled[i][1] - self.left_unfilled[i][1]) + "\tLeft unfilled:\t" + str(self.left_unfilled[i][1]) + "\n"
		p_str += "\nTotal area left unfilled:\t" + str(p_tot_unfilled) + "\n\n"
		file.write(p_str)
		p_str = "Target fraction of area filled:\t" + str(self.filled) + "\n"
		p_str += "Output fraction of area filled:\t" + str((self.filled_area-p_tot_unfilled)/self.total_area) + "\n\n"
		file.write(p_str)
		p_str = "Output gradation:\n"
		for i in range(len(self.left_unfilled)):
			p_str += "\tSize:\t" + str(self.left_unfilled[i][0]) + " mm\tPercentage:\t" + str((self.to_be_filled[i][1] - self.left_unfilled[i][1])/(self.filled_area-p_tot_unfilled)) + "\n"
		file.write(p_str)
		p_str = "\nParticles not within the right sieve size:\t" + str(self.wrong_size) + "\n\n"
		file.write(p_str)

	#write particles to readable file
	def write_particles_to_file(self, file):
		for p in self.particles:
			p_str = ""
			if self.write_labels:
				p_str += "*** Particle ***\n"
			if self.write_center:
				if self.write_labels:
					p_str += "\t*** Center ***\n\t"
				p_str += str(p.get_position()[0]) + ", " + str(p.get_position()[1]) + "\n"
			if self.write_vertices:
				if self.write_labels:
					p_str += "\t*** Vertices ***\n"
				for v in p.get_vertices():
					p_str += "\t" + str(v[0]) + ", " + str(v[1]) + "\n"
			if self.write_area:
				if self.write_labels:
					p_str += "\t*** Area ***\n"
				p_str += "\t" + str(p.get_area()) + "\n"
			if self.write_width:
				if self.write_labels:
					p_str += "\t*** Width ***\n"
				p_str += "\t" + str(p.get_width()) + "\n"
			if self.write_longest_distance:
				if self.write_labels:
					p_str += "\t*** Longest distance from center to vertex ***\n"
				p_str += "\t" + str(p.get_longest_distance()) + "\n"
			file.write(p_str)

	#write particle centers to file
	def write_centers_to_file(self, file):
		for i in range(len(self.particles)):
			p_str = str(self.particles[i].get_position()[0]) + "," + str(self.particles[i].get_position()[1]) + "\n"
			file.write(p_str)

	#write particle vertices to file
	def write_vertices_to_file(self, file):
		for i in range(len(self.particles)):
			p_str = ""
			for j in range(len(self.particles[i].get_vertices())):
				p_str += str(self.particles[i].get_vertices()[j][0]) + "," + str(self.particles[i].get_vertices()[j][1]) + "\n"
			p_str += "\n"
			file.write(p_str)
