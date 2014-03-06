#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
'''
import codecs, os, sys
import __init__
#from classes.FilenameVideoidExtractorMod import FilenameVideoidExtractor
#from classes.VideoIdsOnATextFileFinderMod import VideoIdsOnATextFileFinder
from classes.SabDirLectureFilenameInfoerMod import NotAFilenameSabDirLectureError
from classes.SabDirLectureFilenameInfoerMod import SabDirLectureFilenameInfoer
from classes.SabDirKnowledgeAreaInfoerMod import SabDirKnowledgeAreaInfoer
from classes.SabDirCourseInfoerMod import SabDirCourseInfoer

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
    self.file_count  = 0
    self.basedir_abspath = basedir_abspath

  def get_relpath(self):
    rel_path = self.dirpath
    if self.dirpath.startswith(self.basedir_abspath):
      relpath = self.dirpath[ len(self.basedir_abspath) : ]
    return relpath

  def doUpTreeWalk(self):
    for self.dirpath, dirnames, self.filenames in os.walk(self.basedir_abspath): # dirnames
      # SabDirKnowledgeAreaInfoer.register_knowledges_via_its_foldernames(dirnames, self.dirpath)
      self.k_area = SabDirKnowledgeAreaInfoer.get_knowledge_area_by_relpath(self.dirpath)
      self.process_folder()
  
  def process_folder(self):
    for filename in self.filenames:
      if not filename.endswith('.mp4'):
        continue
      self.file_count += 1
      try:
        filename_lecture = SabDirLectureFilenameInfoer(filename)
        filename_lecture.relpath = self.get_relpath()
        #filename_lecture.set_knowledge_area_to_course_via_relpath()
        filename_lecture.sabdir_course.knowledge_area = self.k_area
        print self.file_count, 'Processing', filename, '(Previous Lecture n. %d)' %self.lecture_seq
        print filename_lecture.relpath
        if  filename_lecture.sabdir_course.knowledge_area != None:
          print filename_lecture.sabdir_course.knowledge_area.write_flat()
        else:
          print '[KA NOT FOUND]'
        self.lecture_seq += 1
      except NotAFilenameSabDirLectureError:
        continue
      # print 'Saving to DB' 
      # dj_course = filename_lecture.save_dj_sabdir_filename()

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
  for i, sabdir_course in enumerate(SabDirCourseInfoer.get_iterative_sabdir_courses_in_alphabetic_order()):
    seq = i + 1
    print seq, sabdir_course

if __name__ == '__main__':
  if 'ut' in sys.argv:
    sys.argv.remove('ut')
    unittests()  
  process()
