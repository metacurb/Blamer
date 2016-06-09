import sublime, sublime_plugin
import os
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

	def svn_commit(self):
		self.view.run_command("save")
		current_file_path = self.view.file_name()
		split_file_path = current_file_path.split(os.sep)
		parent_folder = str.join(os.sep, split_file_path[:split_file_path.index("less")])
		script = 'START TortoiseProc.exe /command:commit /path:"' + parent_folder + '"'
		pr = subprocess.Popen(script,
			shell = True,
			stdout = subprocess.PIPE,
			stderr = subprocess.PIPE,
			stdin = subprocess.PIPE)
		(result, error) = pr.communicate()