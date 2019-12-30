#Author: Camilo Hernandez

from filereader import Filereader
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

	# display the progress when the program is running
	debug = True

	# set initial parameters
	print("\nINITIALIZING...\n")

	try:
		fr = Filereader()

		file = open("gradation.txt", "r")
		gradation = fr.read_gradation(file)
		file.close()

		file = open("settings.txt", "r")
		settings = fr.read_settings(file)
		file.close()

		# specimen boundaries
		x1, y1 = settings["x1"], settings["y1"]
		x2, y2 = settings["x2"], settings["y2"]

		boundaries = (x1, y1, x2, y2)

		# amount of specimen area that is filled with particles
		aggregate_fraction = settings["aggregate_fraction"]

		# minimum and maximum radius when generating vertices for the particles using polar coordinates
		min_radius = settings["min_radius"]
		max_radius = settings["max_radius"]

		# number of vertices in the generated particles
		v_num = settings["v_num"]

		constraints = (min_radius, max_radius, v_num)

		# if the generation of a specimen is unsuccessful, shall the program keep trying
		retry = settings["retry"]

		# number of permitted tries to find a placement for a new particle before deeming the generation unsuccessful
		allowed_amount_of_fails = settings["allowed_amount_of_fails"]

		# should the result be displayed and saved as a plot
		show_result = settings["show_result"]
		save_plotted_result = settings["save_plotted_result"]

		# resolution of the plotted result
		resolution = settings["resolution"]

		# print settings to terminal
		if debug:
			print("Starting generation with the current settings:\n")
			print("\tGradation\n\t------------------------\n\tSize\t|\tPass. %\n\t------------------------")
			for size in gradation:
				print("\t" + str(size[0]) + "\t|\t" + "{:0.2f}".format(size[1] * 100))
			print("\n\tAggregate fraction\n\t" + "{:0.2f}".format(aggregate_fraction * 100) + " %\n")
			print("\tSpecimen boundaries\n\t(x1, y1, x2, y2)\n\t" + str(boundaries) + "\n")
			print("\tMinimum radius\n\t" + str(min_radius) + "\n")
			print("\tMaximum radius\n\t" + str(max_radius) + "\n")
			if not v_num:
				print("\tNumber of vertices\n\t" + "Random" + "\n")
			else:
				print("\tNumber of vertices\n\t" + str(v_num) + "\n")
			print("\tRetries:\n\t" + str(retry) + "\n")
			print("\tAllowed amount of failed attempts:\n\t" + str(allowed_amount_of_fails) + "\n")
			print("\tShow results:\n\t" + str(show_result) + "\n")
			print("\tSave plotted results as image:\n\t" + str(save_plotted_result) + "\n")
			print("\tResolution of plotted result:\n\t" + str(resolution) + "\n")
	except Exception as e:
		print("Could not set intial parameters!\n")
		if debug:
			print("Error:\t" + str(e) + "\n")

	#######################
	#	PARTICLE GENERATION
	#######################

	# generate particles
	print("GENERATING PARTICLES...\n")

	try:
		init_time = time.time()
		# create the generator
		gen = Generator(gradation, boundaries, aggregate_fraction, constraints, allowed_amount_of_fails, debug)
		# generate
		res = gen.generate()
		if retry:
			while not res:
				print("\nFailed! Restarting generation...\n")
				res = gen.generate()
			exec_time = time.time() - init_time
			if debug:
				print("Total time for generation was " + "{:0.2f}".format(exec_time) + " seconds\n")
			particles = gen.get_particles()
		else:
			if not res:
				print("\nFailed! Terminating program...\n")
	except Exception as e:
		print("Could not generate particles!\n")
		if debug:
			print("Error:\t" + str(e) + "\n")
		res = False

	#######################
	#	SAVE RESULTS
	#######################

	if not os.path.exists("results"):
		os.makedirs("results")

	if res:
		# save results
		print("WRITING TO FILE...\n")

		# write particles to readable file
		try:
			file = open("results/values.txt", "w")
			gen.write_particles_to_file(file)
			file.close()
		except Exception as e:
			print("Could not save results to values.txt!\n")
			if debug:
				print("Error:\t" + str(e) + "\n")

		# write particle centers to file
		try:
			file = open("results/centers.txt", "w")
			gen.write_centers_to_file(file)
			file.close()
		except Exception as e:
			print("Could not save results to centers.txt!\n")
			if debug:
				print("Error:\t" + str(e) + "\n")

		# write particle vertices to file
		try:
			file = open("results/vertices.txt", "w")
			gen.write_vertices_to_file(file)
			file.close()
		except Exception as e:
			print("Could not save results to vertices.txt!\n")
			if debug:
				print("Error:\t" + str(e) + "\n")

		# write statistics to file
		try:
			file = open("results/statistics.txt", "w")
			gen.write_statistics_to_file(file)
			file.close()
		except Exception as e:
			print("Could not save results to statistics.txt!\n")
			if debug:
				print("Error:\t" + str(e) + "\n")

		if debug:
			try:
				pathname = os.path.dirname(sys.argv[0])
				print("Results saved to:\n" + os.path.abspath(pathname) + "\\results" + "\n")
			except Exception as e:
				print("Could not print path of saved results!\n")
				if debug:
					print("Error:\t" + str(e) + "\n")

	#######################
	#	PLOT RESULTS
	#######################

	if res:
		# plot results
		print("PLOTTING RESULTS...\n")

		if show_result or save_plotted_result:
			try:
				Plot(particles, show_result, save_plotted_result, (x1, y1, x2, y2), resolution)
			except Exception as e:
				print("Could not plot results!\n")
				if debug:
					print("Error:\t" + str(e) + "\n")

	#######################
	#	END OF PROGRAM
	#######################

	# if this is printed it means everything probably went well
	print("END OF PROGRAM\n")
