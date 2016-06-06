import re
import subprocess

class Subversion:

	def __init__(self, view):
		self.view 		= view
	
	def svn_blame(self): 	
		revision_dictionary = {}

		script = 'svn blame "' + self.view.file_name() + '"'
		pr = subprocess.Popen(script,
			shell = True,
			stdout = subprocess.PIPE,
			stderr = subprocess.PIPE,
			stdin = subprocess.PIPE)
		(result, error) = pr.communicate()
		lines = result.splitlines()

		for idx, line in enumerate(lines):
			index = re.search("\d", line.decode("utf-8")).start()
			line_number_string = line.split(b' ')[index]
			revision_dictionary[idx] = int(line_number_string.decode('utf-8'))

		return revision_dictionary
