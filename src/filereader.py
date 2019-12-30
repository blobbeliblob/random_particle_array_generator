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
				data = lines[i].split(",")
				sieve_size = float(data[0])
				passing_percentage = float(data[1])
				gradation.append([sieve_size, passing_percentage])
		if gradation[0][1] == 100:
			for x in gradation:
				x[1] = x[1] / 100
		return gradation
