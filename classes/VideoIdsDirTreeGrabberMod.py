#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
'''
import os, sys

from VideoIdsOnATextFileFinderMod import VideoIdsOnFolderFilenamesFinder

class VideoIdsDirTreeGrabber(object):

  def __init__(self, basepath=None):
    self.basepath = None
    self.videoids_and_extractors_for_folderfilenames_dict = None 
    # self.videoids_and_titles_tuple_list = None
    self.set_basepath(basepath)
    self.walk_uptree()

  def set_basepath(self, basepath):
    if basepath == None or not os.path.isdir(basepath):
      # default it to the current folder
      self.basepath = os.path.abspath('.')
    else:
      self.basepath = basepath
    print 'basepath', self.basepath
    
  def walk_uptree(self):
    self.videoids_and_extractors_for_folderfilenames_dict = {}
    # self.videoids_and_titles_tuple_list = []
    for dirpath, dirnames, filenames in os.walk(self.basepath):
      print dirpath
      videoids_on_folder_finder = VideoIdsOnFolderFilenamesFinder(dirpath)
      print 'get_total_videoids_from_folder_filenames_listing', videoids_on_folder_finder.get_total_videoids_from_folder_filenames_listing()
      extractors_dict = videoids_on_folder_finder.get_videoids_and_extractors_for_folderfilenames_dict()
      self.update_videoids_and_extractors_for_folderfilenames_dict(extractors_dict)

  def update_videoids_and_extractors_for_folderfilenames_dict(self, extractors_dict):
    videoids_to_remove = []
    for videoid in extractors_dict:
      if videoid in self.videoids_and_extractors_for_folderfilenames_dict:
        print 'Repeated', videoid, extractors_dict[videoid].get_filename()
        videoids_to_remove.append(videoid)
        continue
    for videoid in videoids_to_remove:
      del extractors_dict[videoid] 
    self.videoids_and_extractors_for_folderfilenames_dict.update(extractors_dict)
      # self.videoids_and_titles_tuple_list.append((videoid, extractor.get_title_before_videoid()))

  def print_videoids_and_titles(self):
    seq = 0
    for videoid in self.videoids_and_extractors_for_folderfilenames_dict:
      extractor = self.videoids_and_extractors_for_folderfilenames_dict[videoid]
      seq += 1
      print seq, videoid, extractor.get_title_before_videoid()

  def insert_videoids_into_localhost_db(self):
    seq = 0
    for videoid_and_title in self.videoids_and_titles_tuple_list:
      videoid, title = videoid_and_title
      seq += 1
      print seq, videoid, title


import unittest
class TestCase(unittest.TestCase):
  
  def setUp(self):
    pass

  def test_1_raise_ValueError_for_None_filepath(self):
    pass


def unittests():
  unittest.main()

def process():
  '''
  '''
  grabber = VideoIdsDirTreeGrabber(sys.argv[1])
  grabber.print_videoids_and_titles()
  pass

if __name__ == '__main__':
  if 'ut' in sys.argv:
    sys.argv.remove('ut')
    unittests()  
  process()
