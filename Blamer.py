import sublime, sublime_plugin
from sublime import Region
from .line import Line
from .subversion import Subversion
from .filecacher import FileCacher
from .config import file_cacher_dict
import time 

class blame_setCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		if self.view.file_name() == None:
			sublime.status_message('SVN Gutter - File is not a working copy')
			return

		file_cacher = None
		subversion = Subversion(self.view)
		file_cacher = FileCacher(subversion.svn_blame())
		
		file_cacher_dict[self.view.file_name()] = file_cacher
		file_cacher.iterate_lines()

		regions = self.view.lines(Region(0, self.view.size()))

		for idx, region in enumerate(regions):
			line = Line(self.view, region, self.view.buffer_id(), file_cacher, idx)
			line.erase_region()
			line.add_region()

class blame_removeCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		regions = self.view.lines(Region(0, self.view.size()))

		for idx, region in enumerate(regions):
			line = Line(self.view, region, self.view.buffer_id(), None, idx)
			line.erase_region()
			
		del file_cacher_dict[self.view.file_name()]