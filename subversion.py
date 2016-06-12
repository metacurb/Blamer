import sublime, sublime_plugin
import os
import re
import subprocess
from .filecacher import FileCacher

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
			line = line.decode("utf-8")
			search = re.search("\d", line)
			if line.find("-") != 5:
				index = search.start()
				line_number_string = line.split(' ')[index]
				revision_dictionary[idx] = int(line_number_string)

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

	def svn_log(self, revision):
		script = 'svn log -r' + revision + ' "' + self.view.file_name() + '"'
		pr = subprocess.Popen(script,
			shell = True,
			stdout = subprocess.PIPE,
			stderr = subprocess.PIPE,
			stdin = subprocess.PIPE)
		(result, error) = pr.communicate()
		full_log = (result).decode("utf-8").split("\n")
		committer = full_log[1].split(" | ")[1]
		commit_message = [commit_message.strip("\r") for commit_message in full_log[3:-2]]
		return SvnCommit(revision, committer, commit_message)

class SvnCommit:

	def __init__(self, revision, committer, commit_message):
		self.revision 		= revision
		self.committer		= committer
		self.commit_message = commit_message