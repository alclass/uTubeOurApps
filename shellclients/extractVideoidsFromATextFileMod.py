#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
'''
import codecs, os, sys
import __init__
from classes.FilenameVideoidExtractorMod import FilenameVideoidExtractor
from classes.VideoIdsOnATextFileFinderMod import VideoIdsOnATextFileFinder
#import local_settings as ls 

class SelectedVideoIdPagesComparer(object):

  def __init__(self):
    pass

  def extractVideoidsFromATextFile(self):
    filename = sys.argv[1]
    current_dir = os.path.abspath('.')
    file_abspath = os.path.join(current_dir, filename)
    finder = VideoIdsOnATextFileFinder(file_abspath)
    videoids_and_extractors_for_textfile_dict = finder.get_videoids_and_extractors_for_textfile_dict()
  

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
  pass

if __name__ == '__main__':
  if 'ut' in sys.argv:
    sys.argv.remove('ut')
    unittests()  
  process()
