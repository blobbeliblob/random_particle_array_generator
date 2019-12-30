#Author: Camilo Hernandez

class Filereader():
	def __init__(self):
		return

	# reads the given file and returns a list representing the gradation
	def read_gradation(self, file):
		gradation = []
		lines = file.readlines()
		lines = [line.strip() for line in lines]
		for i in range(len(lines)):
			if lines[i] == "":	# empty row
				pass
			elif lines[i][0] == "#":	# comment
				pass
			else:
				lines[i] = lines[i].replace(" ", "")	# remove whitespace
				lines[i] = lines[i].replace("\t", "")	# remove tabs
				data = lines[i].split(",")
				sieve_size = float(data[0])
				passing_percentage = float(data[1])
				gradation.append([sieve_size, passing_percentage])
		if gradation[0][1] == 100:
			for x in gradation:
				x[1] = x[1] / 100
		return gradation

	def read_settings(self, file):
		settings = {}
		lines = file.readlines()
		lines = [line.strip() for line in lines]
		for i in range(len(lines)):
			if lines[i] == "":	# empty row
				pass
			elif lines[i][0] == "#":	# comment
				pass
			else:
				lines[i] = lines[i].replace(" ", "")	# remove whitespace
				lines[i] = lines[i].replace("\t", "")	# remove tabs
				data = lines[i].split("=")
				parameter = data[0]
				value = data[1]
				if parameter in ["x1", "y1", "x2", "y2", "min_radius", "max_radius", "allowed_amount_of_fails"]:
					value = float(value)
				elif parameter == "aggregate_fraction":
					value = float(value) / 100
				elif parameter == "v_num":
					if value == "None":
						value = None
					else:
						value = float(value)
				elif parameter in ["retry", "show_result", "save_plotted_result"]:
					if value == "1":
						value = True
					else:
						value = False
				elif parameter == "resolution":
					value = int(value)
				settings[parameter] = value
		return settings
