from .randomise import Randomise

class FileCacher:

	def __init__(self, RevDictionary):
		self.RevDictionary = RevDictionary
		self.image_dictionary = {}

	def iterate_lines(self):
		if self.RevDictionary == None:
			return None

		randomise = Randomise()
		for line, revision in self.RevDictionary.items():
			
			if revision not in self.image_dictionary:
				file = randomise.getRandomFile()

				while file in self.image_dictionary.values():
					file = randomise.getRandomFile()

				self.image_dictionary[revision] = file

	def get_image_for_line(self, line_number):
		if line_number in self.RevDictionary:
			return self.image_dictionary[self.RevDictionary[line_number]]