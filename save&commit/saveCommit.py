import sublime, sublime_plugin
import subprocess

class save_commitCommand(sublime_plugin.TextCommand):

	def __init__(self, view):
		self.view 		= view

	def run(self, edit): 	
		self.view.run_command("save")
		script = 'START TortoiseProc.exe /command:commit /path:"' + self.view.file_name() + '"'
		pr = subprocess.Popen(script,
			shell = True,
			stdout = subprocess.PIPE,
			stderr = subprocess.PIPE,
			stdin = subprocess.PIPE)
		(result, error) = pr.communicate()