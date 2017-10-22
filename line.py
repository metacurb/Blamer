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
		return "Packages/Blamer/icons/%s" % (self.color())

	def add_region(self):
		"""Add the icon to the gutter"""
		if self.file_cacher.RevDictionary == None:
			return
		if self.line_number in self.file_cacher.RevDictionary:
			self.view.add_regions(
				"Blamer_%s" % self.line_number,
				[self.region],
				"Blamer",
				self.relative_icon_path(),
				HIDDEN | PERSISTENT
			)

	def erase_region(self):
		"""Remove icon from the gutter"""
		self.view.erase_regions("Blamer_%s" % self.line_number)