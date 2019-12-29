#Author: Camilo Hernandez

import random
import time
from particle import Particle
from plot import Plot
from shapely.geometry import Polygon
import sys
import os

#initialize timer
init_time = time.time()

#overrides the normal print
#used for printing to the terminal
'''
def print(str, end='\n'):
	sys.stdout.write(str + end)
	sys.stdout.flush()
'''

#######################
#	USER INPUT
#######################

#list of tuples representing gradation,
#elements take the shape: [sieve size, passing %],
#sieve size given in millimeters
#passing % given as fraction

#gradation used for testing
#gradation = [[50, 1.00], [30, 0.50], [10, 0.20], [5, 0.00]]

#full real gradation
#gradation = [[19, 1.00], [12.5, 0.987], [9.5, 0.865], [4.75, 0.718], [2.36, 0.514], [1.18, 0.361], [0.6, 0.255], [0.3, 0.147], [0.15, 0.077], [0.075, 0.054]]

#simpler real gradation
gradation = [[19, 1.00], [12.5, 0.987], [9.5, 0.865], [4.75, 0.718], [2.36, 0.514]]

#specimen boundaries
#given as millimeters
x1, y1 = 0, 0
x2, y2 = 300, 300

#amount of specimen area that is filled with particles, given as fraction
filled = 0.50

#minimum and maximum radius when generating vertices for the particles using polar coordinates
min_radius = 1
max_radius = 1.25

#number of vertices in the generated particles, leave as None for randomized
v_num = None

#what contents should be written to the file
write_labels = True
write_center = True
write_vertices = True
write_area = True
write_width = True
write_longest_distance = True
#should the result be displayed and saved as a plot
show_result = True
save_plotted_result = True

#display the progress when the program is running
debug = True

#######################
#	MAIN PROGRAM
#######################

#convert the gradation to be a list of percentage retained
temp_var_a = 0
for i in range(len(gradation)):
	gradation[i][1] = 1.00 - gradation[i][1] - temp_var_a
	temp_var_a += gradation[i][1]
gradation = gradation[::-1]	#reverse the list

#area of the specimen and area filled with particles
total_area = (x2 - x1) * (y2 - y1)
filled_area = filled * total_area

#list of particles to be generated and placed
particles = []

#list of the amount to be filled for each sieve size, used in statistics
to_be_filled = []
#list of the amount left unfilled for each sieve size, used in statistics
left_unfilled = []
#list of number of particles generated for each sieve size, used in statistics
number_of_particles = []
#number of particles that are of the wrong size, used in statistics
wrong_size = 0

#returns true if a new particle p can be placed at coordinates (x, y)
def check_insert_point(p):
	#check if the new particle is fully inside the specimen
	for v in p.get_vertices():
		if v[0] < x1 or v[0] > x2 or v[1] < y1 or v[1] > y2:
			return False
	#for each existing particle, check if the new particle is in its close vicinity,
	#if it is, check if any of the new particles vertices are inside the other particle
	for particle in particles:
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
	#check intersection polygon intersection using the shapely library
	polygon_1 = Polygon(p.get_vertices())
	for particle in particles:
		polygon_2 = Polygon(particle.get_vertices())
		if polygon_1.intersects(polygon_2):
			return False
	return True

#main program
if __name__=='__main__':

	#generate the particles
	print("\nGENERATING PARTICLES...\n")
	for i in range(len(gradation) - 2, -1, -1):	#for each sieve size
		area_to_be_filled = gradation[i][1] * filled_area	#the area that should be filled by particles of the current sieve size
		to_be_filled.append([gradation[i][0], gradation[i][1] * filled_area])	#used in statistics
		left_unfilled.append([gradation[i][0], gradation[i][1] * filled_area])	#used in statistics
		number_of_particles.append([gradation[i][0], 0])	#used in statistics
		particle_size = random.random() * (gradation[i+1][0] - gradation[i][0]) + gradation[i][0]	#get a random particle size for the current sieve size
		particle = Particle(min_radius, max_radius, v_num)	#create a new particle (polygon)
		particle.scale(particle_size)	#scale the particle to the correct size
		area = particle.get_area()	#get the area of the new particle
		while area < area_to_be_filled:
			#keep generating (x, y) coordinates until they are valid for insertion,
			#then insert the particle into the list of placed particles
			x = random.random() * (x2 - x1) + x1
			y = random.random() * (y2 - y1) + y1
			particle.set_position(x, y)
			while not check_insert_point(particle):
				x = random.random() * (x2 - x1) + x1
				y = random.random() * (y2 - y1) + y1
				particle.set_position(x, y)
			particles.append(particle)
			area_to_be_filled -= area	#subtract the area of the placed particle from the area that needs to be filled
			if debug:
				print('Size: ' + str(gradation[i][0]) + 'mm\tProgress:' + "{:0.2f}".format(int(to_be_filled[len(gradation)-2-i][1]-left_unfilled[len(gradation)-2-i][1]) / int(to_be_filled[len(gradation)-2-i][1]) * 100) + " %" + '\tParticles: ' + str(number_of_particles[len(gradation)-2-i][1]), end='\r')
			#used in statistics
			left_unfilled[len(gradation)-2-i][1] -= area
			number_of_particles[len(gradation)-2-i][1] += 1
			if particle.get_width() < gradation[i][0] or particle.get_width() > gradation[i+1][0]:
				wrong_size += 1
			#generate the following particle
			particle_size = random.random() * (gradation[i+1][0] - gradation[i][0]) + gradation[i][0]
			particle = Particle(min_radius, max_radius, v_num)
			particle.scale(particle_size)
			area = particle.get_area()
		if debug:
			print('Size: ' + str(gradation[i][0]) + 'mm\tProgress:' + "{:0.2f}".format(int(to_be_filled[len(gradation)-2-i][1]-left_unfilled[len(gradation)-2-i][1]) / int(to_be_filled[len(gradation)-2-i][1]) * 100) + " %" + '\tParticles: ' + str(number_of_particles[len(gradation)-2-i][1]))

	#time it took to execute the generation of the particles
	exec_time = time.time() - init_time
	if debug:
		print("\nGenerating the particles took " + str(exec_time) + " seconds\n")

	#write particles to readable file
	print("WRITING TO FILE...\n")
	file = open("values.txt", "w")
	for p in particles:
		p_str = ""
		if write_labels:
			p_str += "*** Particle ***\n"
		if write_center:
			if write_labels:
				p_str += "\t*** Center ***\n\t"
			p_str += str(p.get_position()[0]) + ", " + str(p.get_position()[1]) + "\n"
		if write_vertices:
			if write_labels:
				p_str += "\t*** Vertices ***\n"
			for v in p.get_vertices():
				p_str += "\t" + str(v[0]) + ", " + str(v[1]) + "\n"
		if write_area:
			if write_labels:
				p_str += "\t*** Area ***\n"
			p_str += "\t" + str(p.get_area()) + "\n"
		if write_width:
			if write_labels:
				p_str += "\t*** Width ***\n"
			p_str += "\t" + str(p.get_width()) + "\n"
		if write_longest_distance:
			if write_labels:
				p_str += "\t*** Longest distance from center to vertex ***\n"
			p_str += "\t" + str(p.get_longest_distance()) + "\n"
		file.write(p_str)
	file.close()

	#write particle centers to file
	file = open("centers.txt", "w")
	for i in range(len(particles)):
		p_str = str(particles[i].get_position()[0]) + "," + str(particles[i].get_position()[1]) + "\n"
		file.write(p_str)
	file.close()

	#write particle vertices to file
	file = open("vertices.txt", "w")
	for i in range(len(particles)):
		p_str = ""
		for j in range(len(particles[i].get_vertices())):
			p_str += str(particles[i].get_vertices()[j][0]) + "," + str(particles[i].get_vertices()[j][1]) + "\n"
		p_str += "\n"
		file.write(p_str)
	file.close()

	#write statistics to file
	file = open("statistics.txt", "w")
	p_str = "Time to execute:\t" + str(exec_time) + " seconds\n\n"
	file.write(p_str)
	p_str = "Particles generated:\n"
	p_sum = 0
	for p in number_of_particles:
		p_sum += p[1]
	for p in number_of_particles:
		p_str += "\tSize:\t" + str(p[0]) + " mm\tNumber:\t" + str(p[1]) + "\tPercentage:\t" + str(p[1]/p_sum*100) + "\n"
	p_str += "\nTotal number of particles:\t" + str(p_sum) + "\n\n"
	file.write(p_str)
	p_str = "Filled area:\n"
	p_tot_unfilled = 0
	for i in range(len(left_unfilled)):
		p_tot_unfilled += left_unfilled[i][1]
		p_str += "\tSize:\t" + str(left_unfilled[i][0]) + " mm\tTo be filled:\t" + str(to_be_filled[i][1]) + "\tFilled:\t" + str(to_be_filled[i][1] - left_unfilled[i][1]) + "\tLeft unfilled:\t" + str(left_unfilled[i][1]) + "\n"
	p_str += "\nTotal area left unfilled:\t" + str(p_tot_unfilled) + "\n\n"
	file.write(p_str)
	p_str = "Target fraction of area filled:\t" + str(filled) + "\n"
	p_str += "Output fraction of area filled:\t" + str((filled_area-p_tot_unfilled)/total_area) + "\n\n"
	file.write(p_str)
	p_str = "Output gradation:\n"
	for i in range(len(left_unfilled)):
		p_str += "\tSize:\t" + str(left_unfilled[i][0]) + " mm\tPercentage:\t" + str((to_be_filled[i][1] - left_unfilled[i][1])/(filled_area-p_tot_unfilled)) + "\n"
	file.write(p_str)
	p_str = "\nParticles not within the right sieve size:\t" + str(wrong_size) + "\n\n"
	file.write(p_str)
	file.close()

	if debug:
		pathname = os.path.dirname(sys.argv[0])
		print("Results saved to:\n" + os.path.abspath(pathname) + "\n")

	#plot results
	print("PLOTTING RESULTS...\n")
	if show_result or save_plotted_result:
		Plot(particles, show_result, save_plotted_result, (x1, y1, x2, y2))

#time it took to execute the complete script, don't use if plotting results, as the program won't terminate before the image is closed
#exec_time = time.time() - init_time
#print("The program took " + str(exec_time) + " seconds to execute")

#if this is printed it means everything probably went well
print("END OF PROGRAM\n")
