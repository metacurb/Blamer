from os.path import join, dirname, realpath, isfile
from sublime import HIDDEN, PERSISTENT, load_settings, cache_path
import subprocess, os, glob, re, platform
import random
from .randomise import Randomise

def current_directory(full=False):
  """Return the name of the directory containing this plugin"""
  from os.path import dirname, realpath, split
  if full:
    return dirname(realpath(__file__))
  else:
    return split(dirname(realpath(__file__)))[1]

class Line:

  # A digit is one-three numbers, with an optional floating point part,
  # and maybe a % sign, and maybe surrounded by whitespace.
  DIGIT = '\s*\d{1,3}(\.\d*)?%?\s*'

  # Three digits is three digits, with commas between.
  THREE_DIGITS = DIGIT + ',' + DIGIT + ',' + DIGIT

  # Four digits is three digits (which we save for later),
  # and then a comma and then the fourth digit.
  FOUR_DIGITS = '(' + THREE_DIGITS + '),' + DIGIT

  def __init__(self, view, region, file_id, file_cacher, line_number):
    self.view     = view
    self.region   = region
    self.file_id  = file_id
    self.settings = load_settings("Blamer.sublime-settings")
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