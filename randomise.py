import os, random
from sublime import cache_path

class Randomise:

	def getRandomFile(path):
		"""
		Returns a random filename, chosen among the files of the given path.
		"""
		files = os.listdir(cache_path() + "\\Blamer\\")
		index = random.randrange(0, len(files))
		return files[index]