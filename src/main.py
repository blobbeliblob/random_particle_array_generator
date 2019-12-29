#Author: Camilo Hernandez

from generator import Generator
from particle import Particle
from plot import Plot
import sys
import os
import time

#main program
if __name__=='__main__':

	#######################
	#	USER INPUT
	#######################

	# list of tuples representing gradation,
	# elements take the shape: [sieve size, passing %],
	# sieve size given in millimeters
	# passing % given as fraction
	gradation = [[50, 1.00], [30, 0.50], [10, 0.20], [5, 0.00]]

	# specimen boundaries
	# given as millimeters
	x1, y1 = 0, 0
	x2, y2 = 300, 300

	boundaries = (x1, y1, x2, y2)

	# amount of specimen area that is filled with particles, given as fraction
	aggregate_fraction = 0.65

	# minimum and maximum radius when generating vertices for the particles using polar coordinates
	min_radius = 1
	max_radius = 1.25

	# number of vertices in the generated particles, leave as None for randomized
	v_num = None

	# particle constraints
	constraints = (min_radius, max_radius, v_num)

	# if the generation of a specimen is unsuccessful, shall the program keep trying
	retry = True

	# number of permitted tries to find a placement for a new particle before deeming the generation unsuccessful
	allowed_amount_of_fails = 1000

	# should the result be displayed and saved as a plot
	show_result = False
	save_plotted_result = True

	# display the progress when the program is running
	debug = True

	#######################
	#	PARTICLE GENERATION
	#######################

	# create the generator
	gen = Generator(gradation, boundaries, aggregate_fraction, constraints, allowed_amount_of_fails, debug)

	# generate particles
	print("\nGENERATING PARTICLES...\n")

	try:
		init_time = time.time()
		res = gen.generate()
		if retry:
			while not res:
				print("\nFailed! Restarting generation...\n")
				res = gen.generate()
			exec_time = time.time() - init_time
			if debug:
				print("Total time for generation was " + "{:0.2f}".format(exec_time) + " seconds\n")
		else:
			if not res:
				print("\nFailed! Terminating program...\n")
	except Exception as e:
		print("Could not generate particles!\n")

	particles = gen.get_particles()

	#######################
	#	SAVE RESULTS
	#######################

	if res:
		# save results
		print("WRITING TO FILE...\n")

		# write particles to readable file
		try:
			file = open("values.txt", "w")
			gen.write_particles_to_file(file)
			file.close()
		except Exception as e:
			print("Could not save results to values.txt!\n")

		# write particle centers to file
		try:
			file = open("centers.txt", "w")
			gen.write_centers_to_file(file)
			file.close()
		except Exception as e:
			print("Could not save results to centers.txt!\n")

		# write particle vertices to file
		try:
			file = open("vertices.txt", "w")
			gen.write_vertices_to_file(file)
			file.close()
		except Exception as e:
			print("Could not save results to vertices.txt!\n")

		# write statistics to file
		try:
			file = open("statistics.txt", "w")
			gen.write_statistics_to_file(file)
			file.close()
		except Exception as e:
			print("Could not save results to statistics.txt!\n")

		if debug:
			try:
				pathname = os.path.dirname(sys.argv[0])
				print("Results saved to:\n" + os.path.abspath(pathname) + "\n")
			except Exception as e:
				print("Could not print path of saved results!\n")

	#######################
	#	PLOT RESULTS
	#######################

	if res:
		# plot results
		print("PLOTTING RESULTS...\n")

		if show_result or save_plotted_result:
			try:
				Plot(particles, show_result, save_plotted_result, (x1, y1, x2, y2))
			except Exception as e:
				print("Could not plot results!\n")

	#######################
	#	END OF PROGRAM
	#######################

	# if this is printed it means everything probably went well
	print("END OF PROGRAM\n")
