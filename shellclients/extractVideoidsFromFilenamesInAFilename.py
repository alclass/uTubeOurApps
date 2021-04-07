#!/usr/bin/env python3
"""
  # -*- coding: utf-8 -*-

"""
import os
import sys
import unittest
from classes.FilenameVideoidExtractorMod import FilenameVideoidExtractor


class Dict2(dict):
  
  def add(self, key):
    if key in self.keys():
      self[key] += 1
      return
    self[key] = 1
      
  
class FileReader(object):
  """
  This class aims to extract, line by line, videoids from a list of videoid-enclosing filenames
  """
  
  def __init__(self, names_filename_abspath):
    self.names_filename_abspath = None
    self.set_names_filename_abspath(names_filename_abspath)
    self.videoids = []
    self.videoids_dict_repeats = Dict2()

  def set_names_filename_abspath(self, names_filename_abspath):
    if os.path.isfile(names_filename_abspath):
      self.names_filename_abspath = names_filename_abspath
    else:
      error_msg = 'names_filename_abspath (%s) does not exist.' % names_filename_abspath
      raise OSError(error_msg)
  
  def read(self):
    f = open(self.names_filename_abspath, 'r', encoding='utf-8')
    lines = f.readlines()
    for line in lines:
      line = line.lstrip(' \t').rstrip(' \t\r\n')
      if len(line) < 11:
        continue
      extractor = FilenameVideoidExtractor(line)
      videoid = extractor.get_videoid()
      if videoid not in self.videoids: 
        self.videoids.append(videoid)
      else:
        self.videoids_dict_repeats.add(videoid)

  def print_out(self):
    print('# There are %d videoids.' % len(self.videoids))
    for videoid in self.videoids:
      print(videoid)


class TestFilenameVideoidExtractor(unittest.TestCase):
  
  def setUp(self):
    pass

  def test_1_raise_ValueError_for_None_filepath(self):
    pass


def unittests():
  unittest.main()


def process():
  """
  """
  names_filename_abspath = sys.argv[1]
  freader = FileReader(names_filename_abspath)
  freader.read()
  freader.print_out()


if __name__ == '__main__':
  if 'ut' in sys.argv:
    sys.argv.remove('ut')
    unittests()  
  process()
