#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
FilenameLecturerMod.py
'''
import os, re, string, sys

import __init__
# from SabDirCourseInfoerMod import SabDirCourseInfoer

class SabDirLectureInfoer(object):
  
  def __init__(self, lecture_title=None, lecture_number=None, sabdir_course=None):
    self.lecture_title  = lecture_title
    self.lecture_number = lecture_number
    self.sabdir_course  = sabdir_course

  def get_coursename(self):
    if self.sabdir_course != None:
      return self.sabdir_course.coursename
    return ''

  def get_instructors_str(self):
    if self.sabdir_course != None:
      return self.sabdir_course.get_instructors_str()
    return ''

  def __str__(self):
    outstr = '''Course:      [%(coursename)s]
Instructors: [%(instructors_str)s]
Lecture:     [%(lecture_number)d] [%(lecture_title)s]''' \
    %{
      'coursename'      : self.get_coursename(),
      'instructors_str' : self.get_instructors_str(),
      'lecture_number'  : self.lecture_number,
      'lecture_title'   : self.lecture_title,
      }
    return outstr


import unittest
class TestFilenameVideoidExtractor(unittest.TestCase):
  
  def setUp(self):
    pass

  def test_1_fixed_videoid_charlength_should_equal_11_etal(self):
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
