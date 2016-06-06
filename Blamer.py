import sublime, sublime_plugin
from .line import Line
from .subversion import Subversion
from .filecacher import FileCacher

class blame_setCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		subversion = Subversion(self.view)
		filecacher = FileCacher(subversion.svn_blame())
		filecacher.iterate_lines()

		regions = self.view.lines(Region(0, self.view.size()))
		for idx, region in enumerate(regions):
			line = Line(self.view, region, self.view.buffer_id(), filecacher, idx)
			line.add_region()

class blame_removeCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		subversion = Subversion(self.view)
		filecacher = FileCacher(subversion.svn_blame())
		filecacher.iterate_lines()

		regions = self.view.lines(Region(0, self.view.size()))
		for idx, region in enumerate(regions):
			line = Line(self.view, region, self.view.buffer_id(), filecacher, idx)
			line.erase_region()
