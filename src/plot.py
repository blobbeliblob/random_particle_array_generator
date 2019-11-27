
#this plots the particle objects

import matplotlib.pyplot as plt
import numpy as np

#particles = list of Particle objects
#show_plot = boolean
#save_plot = boolean
#boundaries = defines the boundaries of the plotting area as a rectangle, (x1, y1, x2, y2)
def Plot(particles, show_plot, save_plot, boundaries=None):
	fig, ax = plt.subplots()
	if boundaries:
		x1, y1, x2, y2 = boundaries
		ax.plot([x1, x2], [y1, y1], color='b')
		ax.plot([x1, x2], [y2, y2], color='b')
		ax.plot([x1, x1], [y1, y2], color='b')
		ax.plot([x2, x2], [y1, y2], color='b')
	for p in particles:
		#x, y = p.get_position()
		#center = plt.Circle((x, y), .05, color='r')
		#plt.gcf().gca().add_artist(center)
		for i in range(len(p.vertices) - 1):
			line_x = [p.vertices[i][0], p.vertices[i+1][0]]
			line_y = [p.vertices[i][1], p.vertices[i+1][1]]
			ax.plot(line_x, line_y, color='r', linewidth=0.5)
		line_x = [p.vertices[len(p.vertices)-1][0], p.vertices[0][0]]
		line_y = [p.vertices[len(p.vertices)-1][1], p.vertices[0][1]]
		ax.plot(line_x, line_y, color='r', linewidth=0.5)
	if save_plot:
		plt.savefig("particles.png")
	if show_plot:
		plt.show()
