#!/usr/bin/env python
"""
FilenameLecturerMod.py
"""
import sys
import unittest


class SabDirCourseInfoer(object):

  # static dict to keep all courses scraped in memory during runtime
  courses_dict = {}
  
  @staticmethod
  def get_sabdir_course_by_name_or_create_it(coursename):
    if coursename in SabDirCourseInfoer.courses_dict.keys():
      return SabDirCourseInfoer.courses_dict[coursename]
    sabdir_course = SabDirCourseInfoer(coursename)
    SabDirCourseInfoer.courses_dict[coursename] = sabdir_course
    return sabdir_course

  @staticmethod
  def get_all_sabdir_coursenames_in_alphabetic_order():
    coursenames = SabDirCourseInfoer.courses_dict.keys()
    sorted(coursenames)
    return coursenames
  
  @staticmethod
  def get_iterative_sabdir_courses_in_alphabetic_order():
    for coursename in SabDirCourseInfoer.get_all_sabdir_coursenames_in_alphabetic_order():
      sabdir_course = SabDirCourseInfoer.courses_dict[coursename]
      yield sabdir_course 

  def __init__(self, coursename=None, instructors=None):
    self.coursename = coursename
    self.instructors = instructors
    self.lectures_dict = {}  # key is lecture_number
    self.knowledge_area = None
    
  def add_lecture(self, sabdir_lecture):
    self.lectures_dict[sabdir_lecture.lecture_number] = sabdir_lecture

  def get_instructors_str(self):
    outstr = ''
    if self.instructors is None:
      return ''
    for instructor in self.instructors:
      outstr += '%s & ' % instructor
    outstr = outstr[: -3]
    return outstr 

  def get_knowledge_area_flat_str(self):
    k_area_str = ''
    if self.knowledge_area is not None:
      k_area_str = self.knowledge_area.write_flat() 
    return k_area_str
    
  def __str__(self):
    outstr = 'Course        : [%s]\n' % self.coursename
    outstr += 'Instructor(s) : [%s]\n' % self.get_instructors_str()
    outstr += 'Knowledge Area: [%s]\n' % self.get_knowledge_area_flat_str()
    lecture_numbers = self.lectures_dict.keys()
    sorted(lecture_numbers)
    if len(lecture_numbers) == 0:
      outstr += ' * No lectures have been found for this courses.\n'
      return outstr
    outstr += '  * This courses has the following %d lectures:\n' % len(lecture_numbers)
    for lecture_number in lecture_numbers:
      lecture = self.lectures_dict[lecture_number]
      outstr += '  [%d] %s\n' % (lecture_number, lecture.lecture_title)
    return outstr


class TestFilenameVideoidExtractor(unittest.TestCase):
  
  def setUp(self):
    pass

  def test_1_fixed_videoid_charlength_should_equal_11_etal(self):
    pass      


def unittests():
  unittest.main()


def process():
  """
  """
  coursename = 'Direito das Sucessões'
  instructor = 'Anamaria Prates'
  instructors = [instructor]
  sabdir_course = SabDirCourseInfoer(coursename, instructors)
  exec('from SabDirLectureInfoerMod import SabDirLectureInfoer')

  sabdir_lecture = eval('SabDirLectureInfoer()')
  sabdir_lecture.lecture_title = 'Sucessores'
  sabdir_lecture.lecture_number = 1
  sabdir_lecture.sabdir_course = sabdir_course
  sabdir_course.add_lecture(sabdir_lecture)

  sabdir_lecture = eval('SabDirLectureInfoer()')
  sabdir_lecture.lecture_title = 'Herança'
  sabdir_lecture.lecture_number = 2
  sabdir_lecture.sabdir_course = sabdir_course
  sabdir_course.add_lecture(sabdir_lecture)

  print(sabdir_course)
  print('&')
  print(sabdir_lecture)


if __name__ == '__main__':
  if 'ut' in sys.argv:
    sys.argv.remove('ut')
    unittests()  
  process()
