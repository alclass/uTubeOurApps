#!/usr/bin/env python3
"""
  # -*- coding: utf-8 -*-

"""
import os
import sys
# from classes.FilenameVideoidExtractorMod import FilenameVideoidExtractor
from classes.VideoIdsOnATextFileFinderMod import VideoIdsOnATextFileFinder
import unittest

# import local_settings as ls


class SelectedVideoIdPagesComparer(object):

  def __init__(self, filename):
    self.filename = filename
    self.videoids = [] 
    self.extract_videoids_from_textfile()

  def extract_videoids_from_textfile(self):
    current_dir = os.path.abspath('.')
    file_abspath = os.path.join(current_dir, self.filename)
    finder = VideoIdsOnATextFileFinder(file_abspath)
    videoids_and_extractors_for_textfile_dict = finder.get_videoids_and_extractors_for_textfile_dict()
    for videoid in videoids_and_extractors_for_textfile_dict:
      self.videoids.append(videoid)
  
  def printextractedvideoids(self):
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
  filename = sys.argv[1]
  extractor = SelectedVideoIdPagesComparer(filename)
  extractor.printextractedvideoids()


if __name__ == '__main__':
  if 'ut' in sys.argv:
    sys.argv.remove('ut')
    unittests()  
  process()
