#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
'''
import codecs, os, sys
import __init__
from classes.FilenameVideoidExtractorMod import FilenameVideoidExtractor
from classes.VideoIdsOnATextFileFinderMod import VideoIdsOnATextFileFinder
#import local_settings as ls 

# uTubeOurApps.
#from uTubeIdsDjango.uTubeIdsDjApp.models import VideoFile, RelativeDir

'''
class VideoFile(models.Model):
  videoid  = models.CharField(max_length=11, primary_key=True)
  filename = models.TextField()
  rel_dir  = models.ForeignKey(RelativeDir, null=True, blank=True)
  abs_base_dir = models.TextField(null=True, blank=True)
  sha1hex = models.CharField(max_length=40, null=True, blank=True)
  #reporter = models.ForeignKey(Reporter)
  pub_date = models.DateField(null=True, blank=True)
  k_area = models.ForeignKey(KnowledgeArea, null=True, blank=True)
'''

class UpTreeVideoIdFileGrabber(object):

  def __init__(self, basedir_abspath):
    self.basedir_abspath = basedir_abspath

  def get_rel_path(self, dirpath):
    rel_path = dirpath
    if dirpath.startswith(self.basedir_abspath):
      rel_path = dirpath[ len(self.basedir_abspath) : ]
    return rel_path

  def doUpTreeWalk(self):
    for dirpath, dirnames, filenames in os.walk(self.basedir_abspath):
      rel_path = self.get_rel_path(dirpath)
      self.process_folder(filenames, rel_path)
  
  def process_folder(self, filenames, rel_path):
    for filename in filenames:
      print filename, rel_path

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
  basedir = '/run/media/friend/SAMSUNG/'
  grabber = UpTreeVideoIdFileGrabber(basedir)
  
  grabber.doUpTreeWalk()  

if __name__ == '__main__':
  if 'ut' in sys.argv:
    sys.argv.remove('ut')
    unittests()  
  process()
