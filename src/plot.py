#Author: Camilo Hernandez

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import numpy as np

#define the dpi / detail level of the plot
resolution = 1000

#particles = list of Particle objects
#show_plot = boolean
#save_plot = boolean
#boundaries = defines the boundaries of the plotting area as a rectangle, (x1, y1, x2, y2)
def Plot(particles, show_plot, save_plot, boundaries=None):
	fig, ax = plt.subplots()
	shapes = []
	if boundaries:
		x1, y1, x2, y2 = boundaries
		ax.plot([x1, x2], [y1, y1], color='k')
		ax.plot([x1, x2], [y2, y2], color='k')
		ax.plot([x1, x1], [y1, y2], color='k')
		ax.plot([x2, x2], [y1, y2], color='k')
	for p in particles:
		v = np.array(p.get_vertices())
		polygon = Polygon(v, True)
		shapes.append(polygon)
	p_col = PatchCollection(shapes)
	p_col.set_color([0.3, 0.3, 0.3])	#color of the particles
	ax.set_facecolor([1, 1, 1])	#color of the figure
	fig.patch.set_facecolor([1, 1, 1])	#color around the figure
	ax.add_collection(p_col)
	ax.set_aspect('equal')
	if save_plot:
		plt.savefig("particles.png", dpi=resolution)
	if show_plot:
		plt.show()
