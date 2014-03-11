#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
'''
import codecs, os, sys
import __init__
from classes.FilenameVideoidExtractorMod import FilenameVideoidExtractor


class FileReader(object):
  '''
  This class aims to extract, line by line, videoids from a list of videoid-enclosing filenames
  '''
  
  def __init__(self, names_filename_abspath):
    self.names_filename_abspath = None
    self.set_names_filename_abspath(names_filename_abspath)
    self.videoids = []

  def set_names_filename_abspath(self, names_filename_abspath):
    if os.path.isfile(names_filename_abspath):
      self.names_filename_abspath = names_filename_abspath
    else:
      raise OSError, 'names_filename_abspath (%s) does not exist.' %names_filename_abspath
  
  def read(self):
    f = codecs.open(self.names_filename_abspath, 'r', encoding='utf-8')
    lines = f.readlines()
    for line in lines:
      line = line.lstrip(' \t').rstrip(' \t\r\n')
      if len(line) < 11:
        continue
      extractor = FilenameVideoidExtractor(line)
      videoid = extractor.get_videoid()
      self.videoids.append(videoid)

  def print_out(self):
    print '# There are %d videoids.' %len(self.videoids)
    for videoid in self.videoids:
      print videoid


import unittest
class TestFilenameVideoidExtractor(unittest.TestCase):
  
  def setUp(self):
    pass

  def test_1_raise_ValueError_for_None_filepath(self):
    pass


def unittests():
  unittest.main()

def process():
  '''
  '''
  names_filename_abspath = sys.argv[1]
  freader = FileReader(names_filename_abspath)
  freader.read()
  freader.print_out()

if __name__ == '__main__':
  if 'ut' in sys.argv:
    sys.argv.remove('ut')
    unittests()  
  process()
