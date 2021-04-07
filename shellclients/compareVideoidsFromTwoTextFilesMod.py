#!/usr/bin/env python3
"""
"""
import datetime
import sys
# from classes.FilenameVideoidExtractorMod import FilenameVideoidExtractor
# from classes.VideoIdsOnATextFileFinderMod import VideoIdsOnATextFileFinder
from extractVideoidsFromFilenamesInAFilename import FileReader
# import local_settings as ls
import unittest


def fetch_videoids(filepath):
  file_reader = FileReader(filepath)
  file_reader.read()
  videoids = file_reader.videoids
  videoids_dict_repeats = file_reader.videoids_dict_repeats
  return videoids, videoids_dict_repeats


class Comparer:

  def __init__(self, filepath1, filepath2):
    self.videoids1, self.videoids_dict_repeats1 = fetch_videoids(filepath1)
    self.videoids2, self.videoids_dict_repeats2 = fetch_videoids(filepath2)
    self.in_1_missing_in_2 = []
    self.in_2_missing_in_1 = []
    self.compare()

  def compare(self):
    for videoid in self.videoids1:
      if videoid not in self.videoids2:
        self.in_1_missing_in_2.append(videoid)
    for videoid in self.videoids2:
      if videoid not in self.videoids1:
        self.in_2_missing_in_1.append(videoid)
   
  def report(self):
    """
    print 'in_1_missing_in_2'
    print self.in_1_missing_in_2
    print 'in_2_missing_in_1'
    print self.in_2_missing_in_1
    """
    print('total 1', len(self.videoids1))
    print('total 2', len(self.videoids2))
    print('total of repeats in_1', len(self.videoids_dict_repeats1))
    print('total of repeats in_2', len(self.videoids_dict_repeats2))
    print('total in_1_missing_in_2', len(self.in_1_missing_in_2))
    print('total in_2_missing_in_1', len(self.in_2_missing_in_1))


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
  filepath1 = sys.argv[1]
  filepath2 = sys.argv[2]
  print(datetime.datetime.now())
  print('Running Comparer, please wait.')
  extractor = Comparer(filepath1, filepath2)
  extractor.report()
  print(datetime.datetime.now())


if __name__ == '__main__':
  if 'ut' in sys.argv:
    sys.argv.remove('ut')
    unittests()  
  process()
