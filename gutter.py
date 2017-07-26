import sublime
import sublime_plugin
import subprocess
import math
import re
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
				svn = Subversion(view)
				file_cacher = file_cacher_dict.get(view.file_name())
				revision_number = file_cacher.RevDictionary.get(line_number - 1)
				commit_info = svn.svn_log(str(revision_number))
				def async_popup():
					commit_message = " <br>".join(commit_info.commit_message)
					clean_commit_message = commit_message
					urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', commit_message)
					if urls:
						urls = list(set(urls)) # Identifies and removes duplicates
						for url in urls:
							print(url)
							url_text = url.rsplit('/', 1)[1]
							a_tag = "<a href=" + url + ">" + url_text + "</a>"
							clean_commit_message = clean_commit_message.replace(url, a_tag)
							print(clean_commit_message)
					else: 
						urls = '""'
						url_text = ''
					popup = """
						<style>html,body{{margin: 0; padding: 5px;}} span{{display: block;}} a {{display: block; padding: 5px 0;}} </style>
						<span><b>#{} - {}</b></span><span><b>{}</b></span><br><span>{}</span>""".format(commit_info.revision, commit_info.committer, commit_info.commit_date, clean_commit_message)
					view.show_popup(popup, on_navigate=self.navigate, location=pt)
				sublime.set_timeout_async(async_popup)
	def navigate(self, href):
		script = 'start ' + href
		pr = subprocess.Popen(script,
			shell = True,
			stdout = subprocess.PIPE,
			stderr = subprocess.PIPE,
			stdin = subprocess.PIPE)
		(result, error) = pr.communicate()