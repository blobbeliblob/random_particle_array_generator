# Installation

### 1. Download the repository

The code can be found under [releases](https://github.com/blobbeliblob/random_particle_array_generator/releases). These instructions assume you download Version 2 of the code.

### 2. Install requirements

##### 2.1 Download Python

The code requires you to have Python 3 installed,
which can be downloaded from https://www.python.org/downloads/.
<br>
_Note! The Shapely library appears to only work with Python 3.6, so make sure to download this version._

##### 2.2 Download libraries

Once Python is installed, the following libraries need to be installed:

* numpy (https://numpy.org/)
* matplotlib (https://matplotlib.org/users/installing.html)
* shapely (https://pypi.org/project/Shapely/)

If Python has been added to the system's path, the libraries can be installed by running the included _install_requirements.bat_ file (on Windows) or by manually running the following commands in the terminal:

`pip install numpy`

`pip install matplotlib`

`pip install shapely`

Shapely is also included in the /packages folder, and can be installed by running:

`pip install Shapely-1.6.4.post2-cp36-cp36m-win_amd64.whl`

from the terminal.
<br><br>

For more information on how to install and add Python to the system's path, see the Python [documentation](https://docs.python.org/3/using/windows.html).
<br><br>

The required libraries can also be installed using a package manager, included in for example:

* Canopy (https://assets.enthought.com/downloads/)
* Anaconda (https://www.anaconda.com/distribution/)


# How to use

### Running the code

To generate a random particle array, run the _main.py_ script. The script generates the following files in the _/results_ folder:
* _values.txt_
	* This file includes data on the individual particles in an easy to read format
* _centers.txt_
	* This file includes data on the center points of the particles
* _vertices.txt_
	* This file includes data on the vertices of the particles
* _statistics.txt_
	* This file includes general information on the generated particle array
* _particles.png_
	* This file visualizes the generated particle array

### Modifying parameters

The parameters used when generating the particle arrays can be modified by changing the values in the files _gradation.txt_ and _settings.txt_.
These files contain further information on how to set the parameter values.
