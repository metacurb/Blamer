import sublime
import sublime_plugin
import subprocess
import math
from .subversion import Subversion
from .Blamer import file_cacher_dict

def is_coord_on_gutter(view, x, y):
	"""Determine if x and y coordinates are over the gutter.

	Because this is inapplicable for empty lines,
	returns `None` to let the caller decide on what do to.
	"""
	original_pt = view.window_to_text((x, y))
	if view.rowcol(original_pt)[1] != 0:
		return False

	# If the line is empty,
	# we will always get the same textpos
	# regardless of x coordinate.
	# Return `None` in this case and let the caller decide.
	if view.line(original_pt).empty():
		return False

	# ST will put the caret behind the first character
	# if we click on the second half of the char.
	# Use view.em_width() / 2 to emulate this.
	adjusted_pt = view.window_to_text((x + view.em_width() / 2, y))
	if adjusted_pt != original_pt:
		return False

	return True

class GutterListener(sublime_plugin.EventListener):

	def on_text_command(self, view, cmd, args):
		
		if cmd == 'drag_select' and 'event' in args:
			event = args['event']
			pt = view.window_to_text((event['x'], event['y']))
			line_pt = view.window_to_layout((event['x'], event['y']))
			line_number = math.ceil(line_pt[1] / view.line_height())
			on_gutter = is_coord_on_gutter(view, event['x'], event['y'])

			if on_gutter is not False and event['button'] == 1:
				print("Line " + str(line_number))
				file_cacher = file_cacher_dict.get(view.file_name())
				print(file_cacher)
				revision_number = file_cacher.RevDictionary.get(line_number)
				print(revision_number)
				Subversion.svn_log(self, str(revision_number))
				def async_popup():
					view.show_popup('<style>html,body{margin: 0; padding: 5px; background-color: #fafafa;} span{display: block;} a {display: block; padding: 5px 0;} </style><span><b>#13274 - beau.august@gforces.co.uk</b><span><a target="_blank" href="https://jira.netdirector.co.uk/browse/AFUFM-1">AFUFM-1</a> The code will pick up URLs and wrap them. If you write any text, it will sit underneath.</span>', on_navigate=self.navigate, location=pt)
				sublime.set_timeout_async(async_popup)

	def navigate(self, href):
		script = 'start ' + href
		pr = subprocess.Popen(script,
			shell = True,
			stdout = subprocess.PIPE,
			stderr = subprocess.PIPE,
			stdin = subprocess.PIPE)
		(result, error) = pr.communicate()