# Installation

### 1. Download the repository

### 2. Install requirements

The code requires you to have Python 3 installed,
which can be downloaded from https://www.python.org/downloads/
<br><br>
Once Python is installed, the following libraries need to be installed:
* numpy (https://numpy.org/)
* matplotlib (https://matplotlib.org/users/installing.html)
* shapely (https://pypi.org/project/Shapely/)
<br>
If Python has been added to the system's path, the libraries can be installed by running the included install_requirements.bat file (on Windows) or by manually running the following commands in the terminal:
* pip install numpy
* pip install matplotlib
* pip install shapely
<br>
Shapely is also included in the /packages folder, and can be installed by running:
* pip install Shapely-1.6.4.post2-cp36-cp36m-win_amd64.whl
<br>
from the terminal.
<br><br>
The required libraries can also be installed using a package manager, included in for example:
* Canopy (https://assets.enthought.com/downloads/)
* Anaconda (https://www.anaconda.com/distribution/)


# How to use

### Running the code

To generate a random particle array, run the generate.py script. The script generates the following files:
* values.txt
	* This file includes data on the individual particles
* statistics.txt
	* This file includes general information on the generated particle array
* particles.png
	* This file visualizes the generated particle array

### Modifying parameters

The following parameters can be edited in the generate.py file to modify the output, the parameters are located under the "USER INPUT" section:
* gradation
	* A list containing information on the gradation to be used. Each element is a list, where the first element should be the size of the sieve (given in millimeters) and the second element should be the passing percentage of mass.
* x1, y1, x2, y2
	* These parameters represent the boundaries of the specimen (given in millimeters). (x1, y1) is the first point in the bounding rectangle, while (x2, y2) is the opposite point, so that the size (width, height) of the rectangle is (x2-x1, y2-y1).
* filled
	* This represents the percentage of the specimen's area that is filled with particles (given as a fraction).
* min_radius, max_radius
	* These are used to control the shape of the generated particles. Each vertex of a particle is created at distance from the particles origin, where the distance is a random value between min_radius and max_radius.
* v_num
	* This specifies the number of vertices in the generated particles. If left as None, a random number between 4 and 10 is chosen.
* write_labels
	* This controls whether labels are written out in the values.txt file.
* write_center
	* This controls whether the centerpoints of the particles are written out in the values.txt file.
* write_vertices
	* This controls whether the vertices of the particles are written out in the values.txt file.
* write_area
	* This controls whether the areas of the particles are written out in the values.txt file.
* write_width
	* This controls whether the widths of the particles are written out in the values.txt file.
* write_longest_distance
	* This controls whether the longest distance from a vertex to the centerpoint of the particle for each particle is written out in the values.txt file.
* show_result
	* This controls whether the result is shown as a plot.
* save_plotted_result
	* This controls whether the result is saved as a plot.
* debug
	* This controls whether information on the generation is displayed while the code is running.
