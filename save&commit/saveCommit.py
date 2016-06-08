import sublime, sublime_plugin
import subprocess
import os

class save_commitCommand(sublime_plugin.TextCommand):

	def __init__(self, view):
		self.view 		= view

	def run(self, edit): 	
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