#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
  dbInsertVideoidsUpTree.py
  This script walks folders down the directory tree, 
    grabbing Saber Direito courses, ie, grabbing the videolecture filenames
    that conform to the markers that lecture filenames carry.
    
  These filename markers are:
  
  + " _i " (required)
    tells there are instructor name(s) after itself and a course title/name before itself.
  
  + " _Aula <N> " (required)
    tells that the instructor string, started by " _i ", has finished and a lecture title follows.

  + " _p <N> ;" (optional)
    tells the lecture encompasses more than 1 videofile (to be a bit further explained below). 

  Notice that the "<N>" in " _Aula <N> " is a 1-digit number, usually from 1 to 5.
  
  How Lecture Titles end
  
  There are 2 hypotheses for their ending, they are:
  1) the dash plus videoid plus dot extension filename ending;
  2) the "part" marker, which is " _p<N> ;" where <N> is also usually a 1-digit number.
  
  Examples of the 2 possible endings after a Lecture Title:
  =========================================================
  
  1) without a part marker: 
  Course X _i Instructor Y _Aula 3 The Third Lecture-99999999999.mp4  


  2) with a part marker: 
  Course X _i Instructor Y _Aula 3 The Third Lecture Part Four _p4 ;-99999999999.mp4

  Obs: 99999999999 represents the 11-character YouTube videoid which consists of
       letters, number, - (dash) and _ (underline).
  
  Notice that spaces must be respected, ie, there is a blank before and after " _i ", 
    so to the " _Aula <N> " marker and the part marker has blanks too and ends with a semicolon ";".  

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

class DownDirTreeSabDirLectureFilenameGrabber(object):
  '''
  The help doc-string above, for this module, explained the whole job that
    the module's script runs.
    
  This class does the down-dir-tree-walking and process folder by folder.
  The videofilenames in each folder are modeled by class:
  
  + SabDirLectureFilenameInfoer(filename)
  
  In this class, a scraping method will extract coursename, instructor(s), 
    lecture number and parts, if any.  The extension and videoid will also be extracted.
  '''

  def __init__(self, basedir_abspath):
    self.lecture_seq = 0
    self.file_count  = 0
    self.basedir_abspath = basedir_abspath

  def get_relpath(self):
    rel_path = self.dirpath
    if self.dirpath.startswith(self.basedir_abspath):
      relpath = self.dirpath[ len(self.basedir_abspath) : ]
    return relpath

  def walkDownDirTree(self):
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


def get_basedir_abspath_from_sysargv_or_default():
  basedir_abspath_DEFAULT = '/run/media/friend/SAMSUNG/Saber Direito TVJus/'
  basedir_abspath = None
  try:
    basedir_abspath = sys.argv[1]
    if not os.path.isdir(basedir_abspath):
      basedir_abspath = basedir_abspath_DEFAULT
  except IndexError:
    pass
  if basedir_abspath == None:
    basedir_abspath = basedir_abspath_DEFAULT
  return basedir_abspath
    
def process():
  basedir_abspath = get_basedir_abspath_from_sysargv_or_default() 
  grabber = DownDirTreeSabDirLectureFilenameGrabber(basedir_abspath)
  grabber.walkDownDirTree()
  for i, sabdir_course in enumerate(SabDirCourseInfoer.get_iterative_sabdir_courses_in_alphabetic_order()):
    seq = i + 1
    print seq, sabdir_course

if __name__ == '__main__':
  if 'ut' in sys.argv:
    sys.argv.remove('ut')
    unittests()  
  process()
