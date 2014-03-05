#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
'''
import codecs, os, sys
import __init__
from classes.FilenameVideoidExtractorMod import FilenameVideoidExtractor
from classes.VideoIdsOnATextFileFinderMod import VideoIdsOnATextFileFinder
from SabDirLectureFilenameInfoerMod import SabDirLectureFilenameInfoer
from SabDirLectureFilenameInfoerMod import NotAFilenameSabDirLectureError
from SabDirLectureFilenameInfoerMod import courses_dict

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
    self.lecture_seq = 0
    self.basedir_abspath = basedir_abspath

  def get_rel_path(self, dirpath):
    rel_path = dirpath
    if dirpath.startswith(self.basedir_abspath):
      rel_path = dirpath[ len(self.basedir_abspath) : ]
    return rel_path

  def doUpTreeWalk(self):
    for dirpath, _, filenames in os.walk(self.basedir_abspath): # dirnames
      rel_path = self.get_rel_path(dirpath)
      self.process_folder(filenames, rel_path)
  
  def process_folder(self, filenames, rel_path):
    self.lecture_seq += 1
    for filename in filenames:
      try:
        lecture = SabDirLectureFilenameInfoer(filename)
      except NotAFilenameSabDirLectureError:
        continue
      print lecture 
      print '>>>', self.lecture_seq, '<<<', ' *** rel_path ***', rel_path
      print 'Saving to DB' 
      dj_course = lecture.save_dj_sabdir_filename()

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
def process():
  # basedir_abspath = sys.argv[1] 
  #SourceAndTargetBaseDirsKeeper.set_source_basepath(source_basedir_abspath)

  basedir_abspath = '/run/media/friend/SAMSUNG/'
  grabber = UpTreeVideoIdFileGrabber(basedir_abspath)
  grabber.doUpTreeWalk()
  courses = courses_dict.keys()
  courses.sort()
  for i, coursename in enumerate(courses):
    instructors = courses_dict[coursename]
    seq = i + 1
    print seq, coursename, '(',
    for instructor in instructors:
      print instructor,
    print ')'

if __name__ == '__main__':
  if 'ut' in sys.argv:
    sys.argv.remove('ut')
    unittests()  
  process()
