from sublime import HIDDEN, PERSISTENT

class Line:

	def __init__(self, view, region, file_id, file_cacher, line_number):
		self.view     = view
		self.region   = region
		self.file_id  = file_id
		self.text     = self.view.substr(self.region)
		self.file_cacher = file_cacher
		self.line_number = line_number

	def color(self):
		return self.file_cacher.get_image_for_line(self.line_number)

	def relative_icon_path(self):
		"""The relative location of the color icon"""
		return "Cache/Blamer/%s" % (self.color())

	def add_region(self):
		"""Add the icon to the gutter"""
		self.view.add_regions(
			"Blamer_%s" % self.region.a,
			[self.region],
			"Blamer",
			self.relative_icon_path(),
			HIDDEN | PERSISTENT
		)

	def erase_region(self):
		"""Remove icon from the gutter"""
		self.view.erase_regions("Blamer_%s" % self.region.a)