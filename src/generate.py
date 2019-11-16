#this is a test

import random
import time
from particle import Particle
from plot import Plot
from shapely.geometry import Polygon

#initialize timer
init_time = time.time()

#######################
#	USER INPUT
#######################

#list of tuples representing gradation,
#elements take the shape: (sieve size, mass % that that is caught by the sieve),
#last element should be the maximum sieve size (meaning no particles caught in that sieve)
#size given in millimeters
#mass % given as fraction
#gradation = [(1, 0.45), (5, 0.35), (10, 0.20), (20, 0)]
#gradation = [(10, 1), (20, 0)]
#gradation = [(0.074, 0.05), (0.177, 0.10), (0.42, 0.225), (2.00, 0.19), (4.76, 0.265), (9.52, 0.10), (12.7, 0.00)]
#gradation = [(2.0, 0.06), (3.15, 0.044), (4.0, 0.045), (5.0, 0.068), (6.3, 0.139), (8.0, 0.133), (10.0, 0.047), (12.5, 0.013), (14.0, 0)]
gradation = [(5, 0.20), (10, 0.30), (30, 0.50), (50, 0.00)]
#gradation = [(10, 1.0), (10.1, 0.00)]

#specimen boundaries
#given as millimeters
x1, y1 = 0, 0
x2, y2 = 100, 100

#amount of specimen area that is filled with particles, given as fraction
filled = 0.50

#minimum and maximum radius when generating vertices for the particles using polar coordinates
min_radius = 1
max_radius = 1

#what contents should be written to the file
write_labels = True
write_center = True
write_vertices = True
write_area = True
#should the result be displayed and saved as a plot
show_result = True
save_plotted_result = False

#######################
#	MAIN PROGRAM
#######################

#area of the specimen and area filled with particles
total_area = (x2 - x1) * (y2 - y1)
filled_area = filled * total_area

#list of particles to be generated and placed
particles = []

#returns true if a new particle p can be placed at coordinates (x, y)
#point in polygon algorithm found at:
#https://wrf.ecse.rpi.edu//Research/Short_Notes/pnpoly.html
#http://erich.realtimerendering.com/ptinpoly/
#shapely found at:
#https://github.com/Toblerity/Shapely
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
	for i in range(len(gradation) - 1):	#for each sieve size
		area_to_be_filled = gradation[i][1] * filled_area
		particle_size = random.random() * (gradation[i+1][0] - gradation[i][0]) + gradation[i][0]	#get a random particle size for the appropriate sieve size
		particle = Particle(min_radius, max_radius)	#create a new particle (polygon)
		particle.scale(particle_size)	#scale the particle to the correct size
		area = particle.get_area()	#get the area of the new particle
		too_many_attempts = False
		while area < area_to_be_filled:
			#keep generating (x, y) coordinates until they are valid for insertion,
			#then insert the particle into the list of placed particles
			#failed_attempts = 0
			x = random.random() * (x2 - x1) + x1
			y = random.random() * (y2 - y1) + y1
			particle.set_position(x, y)
			while not check_insert_point(particle):
			#	failed_attempts += 1
			#	if failed_attempts >= 100000:
			#		print("too many attempts\n")
			#		too_many_attempts = True
			#		break
				x = random.random() * (x2 - x1) + x1
				y = random.random() * (y2 - y1) + y1
				particle.set_position(x, y)
			#if too_many_attempts:
			#	break
			particles.append(particle)
			area_to_be_filled -= area	#subtract the area of the placed particle from the area that needs to be filled
			#generate the following particle
			particle_size = random.random() * (gradation[i+1][0] - gradation[i][0]) + gradation[i][0]
			particle = Particle(min_radius, max_radius)
			particle.scale(particle_size)
			area = particle.get_area()

	#time it took to execute the generation of the particles
	exec_time = time.time() - init_time
	print("Generating the particles took " + str(exec_time) + " seconds\n")

	#write particles to file
	print("WRITING TO FILE...\n")
	file = open("values.txt", "w")
	for p in particles:
		p_str = ""
		if write_labels:
			p_str += "*** Particle ***\n"
		if write_center:
			if write_labels:
				p_str += "\t*** Center ***\n\t"
			p_str += str(p.get_position()) + "\n"
		if write_vertices:
			if write_labels:
				p_str += "\t*** Vertices ***\n"
			for v in p.get_vertices():
				p_str += "\t" + str(v) + "\n"
		if write_area:
			if write_labels:
				p_str += "\t*** Area ***\n"
			p_str += "\t" + str(p.get_area()) + "\n"
		file.write(p_str)
	file.close()

	#plot results
	print("PLOTTING RESULTS...\n")
	if show_result or save_plotted_result:
		Plot(particles, show_result, save_plotted_result, (x1, y1, x2, y2))

#time it took to execute the complete script
#exec_time = time.time() - init_time
#print("The program took " + str(exec_time) + " seconds to execute")

#if this is printed it means everything probably went well
print("END OF PROGRAM\n")
