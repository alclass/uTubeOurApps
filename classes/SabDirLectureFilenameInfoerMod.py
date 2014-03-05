#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
FilenameLecturerMod.py
'''
import os, re, string, sys

import __init__
from uTubeIdsDjango.uTubeIdsDjApp.models import SabDirInstructorDj
from uTubeIdsDjango.uTubeIdsDjApp.models import SabDirCourseDj
from uTubeIdsDjango.uTubeIdsDjApp.models import SabDirLectureDj
from uTubeIdsDjango.uTubeIdsDjApp.models import SabDirVideoFilenameDj


ALLOWED_CHARS_IN_YOUTUBEVIDEOID = string.ascii_letters + string.digits + '_-'
youtubevideoid_having_only_allowed_chars_lambda = lambda s : s in ALLOWED_CHARS_IN_YOUTUBEVIDEOID
str_having_only_number_digits_lambda = lambda s : s in string.digits
YOUTUBE_VIDEOID_CHARLENGTH = 11   
# FORBIDDEN_CHARS_IN_YOUTUBEVIDEOID = ' !@#$%&*()+=Çç/:;.,[]{}|\\ \'"'
# youtubevideoid_having_some_forbidden_char_lambda = lambda s : s in FORBIDDEN_CHARS_IN_YOUTUBEVIDEOID   

re_for_lecture_number = ' _Aula (\d+) '
re_for_lecture_number_comp = re.compile(re_for_lecture_number)

re_for_lecture_parts_str = ' _p(\d+) ;'
re_for_lecture_parts_comp = re.compile(re_for_lecture_parts_str)

re_valid_youtube_videoid_str = '[A-Za-z0-9_\-]{11}'
re_valid_youtube_videoid_comp = re.compile(re_valid_youtube_videoid_str)
def is_videoid_well_formed(videoid):
  if re_valid_youtube_videoid_comp.match(videoid):
    return True
  return False

def is_youtube_videoid_good(videoid):  
  videoidlist = list(videoid)
  boolean_result_list = map(youtubevideoid_having_only_allowed_chars_lambda, videoidlist)
  if False in boolean_result_list:
    return False
  # a second test: videoid cannot be only number-digits
  boolean_result_list = map(str_having_only_number_digits_lambda, videoidlist)
  if False not in boolean_result_list:
    return False
  return True

class NotAFilenameSabDirLectureError(ValueError):
  pass

courses_dict = {}

class SabDirLectureInfoer(object):
  
  def __init__(self, coursename=None, instructors=None, lecture_title=None, lecture_number=None):
    self.coursename     = coursename
    self.instructors    = instructors
    self.lecture_title  = lecture_title
    self.lecture_number = lecture_number

  def get_instructors_str(self):
    outstr = ''
    if self.instructors == None:
      return ''
    for instructor in self.instructors:
      outstr += '%s & ' %instructor
    outstr = outstr[ : -3 ]
    return outstr 
    
  def __str__(self):
    outstr = '''Course: [%(coursename)s]
    Instructors: [%(instructors_str)s]
    Lecture:     [%(lecture_number)d]
    Title:       [%(lecture_title)s]''' %{'coursename':self.coursename, 'instructors_str':self.get_instructors_str(),'lecture_title':self.lecture_title,'lecture_number':self.lecture_number,'lecture_part':self.lecture_part}
    return outstr

class SabDirLectureFilenameInfoer(SabDirLectureInfoer):
  
  def __init__(self, filename):
    super(SabDirLectureFilenameInfoer, self).__init__() # set attribs after decomposing them from filename
    self.extension    = None
    self.lecture_part = 0
    #self.videoid   = None
    self.videoid = '99999999999'
    self.rel_dir = None
    self.set_filename(filename)
    self.decompose_filename_into_lecture_attribs()

  #=============================================================================
  # def is_it_a_filename_sabdir_lecture(self):
  #   if self.lecture_number == None:
  #     return False
  #   if self.lecture_title == None:
  #     return False
  #   if len(self.instructors) == 0:
  #     return False
  #   if self.coursename == None:
  #     return False
  #   return True
  #=============================================================================

  def decompose_filename_into_lecture_attribs(self):
    pos_i =  self.filename.find(' _i ')
    if pos_i > -1:
      self.coursename = self.filename[ : pos_i ]
    else:
      # return
      raise NotAFilenameSabDirLectureError, 'filename %s NotAFilenameSabDirLecture (str/marker _i is missing)' %self.filename 
    pos_aula = self.filename.find(' _Aula ')
    self.instructors = []
    if pos_aula > -1:
      instructors_str = self.filename[ pos_i + len(' _i ') : pos_aula ]
      if instructors_str.find('&'):
        self.instructors = instructors_str.split('&')
      else:
        self.instructors = [instructors_str]
    else:
      # return
      raise NotAFilenameSabDirLectureError, 'filename %s NotAFilenameSabDirLecture (str/marker _Aula is missing)' %self.filename 
    for instructor in self.instructors:
      instructor = instructor.lstrip(' ').rstrip(' ')
    courses_dict[self.coursename] = self.instructors    
    # test there is a videoid at the end
    extensionless_fn, self.extension = os.path.splitext(self.filename)
    videoid_exists = False
    if len(extensionless_fn) > 11:
      videoid_chunk = extensionless_fn[ -12 : ]
      if videoid_chunk.startswith('-'):
        videoid_chunk = videoid_chunk[1:]
        if is_videoid_well_formed(videoid_chunk):
          videoid_exists = True
    self.lecture_title = extensionless_fn[ pos_aula + len(' _Aula N ') : ]
    if videoid_exists:
      self.lecture_title = self.lecture_title[ : -12 ]
      self.videoid       = self.lecture_title[ -11 : ]
    # verify lecture_title has ' _p<n> ;'
    parts_re_find = re_for_lecture_parts_comp.search(self.filename)
    if parts_re_find:
      pos_pp = self.lecture_title.find(' _p')
      self.lecture_title = self.lecture_title[ : pos_pp ]
      part_as_str = parts_re_find.group(1)
      self.lecture_part = int(part_as_str)
    number_re_find = re_for_lecture_number_comp.search(self.filename)
    if number_re_find:
      number_as_str = number_re_find.group(1)
      self.lecture_number = int(number_as_str) # because \d+ is used in RegExp, it's guaranteed not to raise ValueError against int() 
    else:
      raise NotAFilenameSabDirLectureError, 'filename %s NotAFilenameSabDirLecture (Lecture Number after marker _Aula is missing)' %self.filename 
      
  def set_filename(self, filename):
    if filename == None:
      raise ValueError, "filename for FilenameVideoidExtractor()'s constructor cannot be None."
    # this rule will demand the production of a script that preprocesses to guarantee there are no files with beginning or ending spaces
    filename = filename.lstrip(' \t').rstrip(' \t\r\n')
    self.filename = filename
    extensionless_filename, dot_extension = os.path.splitext(self.filename)
    if extensionless_filename == '.':
      # this is the directory itself, raise ValueError
      raise ValueError, "filename for FilenameVideoidExtractor()'s constructor cannot be the dot directory."
    self.extensionless_filename = extensionless_filename
    self.dot_extension = None
    if dot_extension != '':
      self.dot_extension = dot_extension
  
  def get_filename(self):
    return self.filename

  def get_dot_extension(self):
    return self.dot_extension

  def get_extensionless_filename(self):
    return self.extensionless_filename

  def get_videoid(self, refetch=False):
    if self.videoid != 'INIT1234&&&' and not refetch:
      return self.videoid
    # Notice self.videoid can be set as None
    self.fetch_and_set_videoid_from_extensionless_filename()
    return self.videoid

  def get_title_before_videoid(self):
    videoid = self.get_videoid()
    if videoid == None:
      return None
    if len(self.extensionless_filename) < 13:
      return None
    title = self.extensionless_filename[:-12] # one extra char is the '-' (dash)
    return title

  def fetch_and_set_videoid_from_extensionless_filename(self):
    try:
      if len(self.extensionless_filename) < 11:
        self.videoid = None
        return
      elif len(self.extensionless_filename) > 11:
        if self.extensionless_filename[-12] != '-':
          # ATTENTION: this Business Rule is IMPORTANT. If extensionless name is than 11 chars, the 12th last one should be a dash '-'
          self.videoid = None
          return
      # elif len(self.extensionless_filename) == 11:
        # okay, if it's exactly 11, let it not have an obligatory '-' (dash)
      videoid = self.extensionless_filename[-11:]
      self.videoid = FilenameVideoidExtractor.validate_and_return_the_11char_youtube_videoid_or_None(videoid)
    except IndexError:
      self.videoid = None

  def save_dj_sabdir_filename(self):
    '''
    This method transfers the object's attributes to its equivalent
      Django model object, so that it may be persisted onto a database
    '''
    instructor_str = self.get_instructors_str()
    try:
      dj_instructor = SabDirInstructorDj.objects.get(tarjaname=instructor_str)
    except SabDirInstructorDj.DoesNotExist:
      dj_instructor = SabDirInstructorDj()
      dj_instructor.tarjaname = instructor_str 
      #dj_instructor.flush()
      dj_instructor.commit()
    try:
      dj_course = SabDirCourseDj.objects.get(coursename=self.coursename)
    except SabDirCourseDj.DoesNotExist:
      dj_course = SabDirCourseDj()
      dj_course.coursename = self.coursename 
      dj_course.instructor = dj_instructor 
      dj_course.commit() 
    try:
      dj_lecture = SabDirLectureDj.objects.get(course=dj_course, seq_order=self.lecture_number)
    except SabDirLectureDj.DoesNotExist:
      dj_lecture           = SabDirLectureDj()
      dj_lecture.course    = dj_course  
      dj_lecture.title     = self.lecture_title  
      dj_lecture.seq_order = self.lecture_number  
      dj_lecture.commit()
    try: 
      dj_videofilename = SabDirVideoFilenameDj.objects.get(lecture=dj_lecture, part=self.lecture_part)
    except SabDirVideoFilenameDj.DoesNotExist:
      dj_videofilename = SabDirVideoFilenameDj()
      dj_videofilename.lecture = dj_lecture
      dj_videofilename.part = self.lecture_part
      dj_videofilename.videoid = self.videoid
      dj_videofilename.extension = self.extension
      if self.rel_dir != None:
        dj_videofilename.rel_dir = self.rel_dir
        dj_videofilename.commit() 
      dj_videofilename.commit()

  #@ooverride
  def __str__(self):
    outstr = super(SabDirLectureFilenameInfoer, self).__str__()
    outstr += '\nFilename  = [%s]' %self.filename
    outstr += '\nLecture Part = [%d]' %self.lecture_part
    outstr += '\nExtension = [%s]' %self.extension
    outstr += '\nVideoid   = [%s]' %self.videoid
    return outstr


  @staticmethod
  def validate_and_return_the_11char_youtube_videoid_or_None(videoid):
    if videoid == None:
      return None
    elif len(videoid) != 11:
      return None
    videoid_good = is_youtube_videoid_good(videoid)
    if not videoid_good:
      return None
    return videoid  
  
    
class TestFixedData:
  
  utube_test_videoid   = '0yZNJHae3QM'
  utube_test_title     = 'Direito Civil - Obrigações, Contratos e Responsabilidade Civil para o Exame de Ordem'
  utube_test_extension = 'mp4'
  utube_test_filename  = None

  def __init__(self):
    self.form_filename()
  
  def form_filename(self):
    self.utube_test_filename = '%s-%s.%s' %(self.utube_test_title, self.utube_test_videoid, self.utube_test_extension)
    

import unittest
class TestFilenameVideoidExtractor(unittest.TestCase):
  
  def setUp(self):
    self.VIDEOID_CHAR_LEN = 11
    self.fixed_data = TestFixedData()
    self.videoid_extractor = FilenameVideoidExtractor(self.fixed_data.utube_test_filename)

  def test_1_fixed_videoid_charlength_should_equal_11_etal(self):
    self.assertEqual(self.VIDEOID_CHAR_LEN, len(self.fixed_data.utube_test_videoid))
    test_videoid = 'abc123abc12'
    self.assertTrue(is_youtube_videoid_good(test_videoid))
    test_videoid = '12345678901'
    self.assertEqual(len(test_videoid), YOUTUBE_VIDEOID_CHARLENGTH)
    self.assertFalse(is_youtube_videoid_good(test_videoid))
      
  def test_2_extract_videoid(self):
    '''
    This test is to cover the helper 
      generate_nonrepeat_sha1sum() unittest method above,
      this is not a business rule, so to say, unittest
    '''
    returned_videoid = self.videoid_extractor.get_videoid()
    self.assertEqual(returned_videoid, self.fixed_data.utube_test_videoid)

  def test_3_compare_filename_extension_and_title(self):
    self.assertEqual(self.videoid_extractor.get_filename(),             self.fixed_data.utube_test_filename)
    self.assertEqual(self.videoid_extractor.get_dot_extension(), '.'  + self.fixed_data.utube_test_extension)
    self.assertEqual(self.videoid_extractor.get_title_before_videoid(), self.fixed_data.utube_test_title)

  def test_4_get_None_videoid(self):
    test_videoid_extractor = FilenameVideoidExtractor('blah blah as filename')
    should_be_None = test_videoid_extractor.get_videoid()
    self.assertIsNone(should_be_None)
    
  def test_5_raise_for_invalid_filename_as_None_or_dot(self):
    self.assertRaises(ValueError, FilenameVideoidExtractor, None)
    self.assertRaises(ValueError, FilenameVideoidExtractor, '.')

  def test_6_noraise_with_nonvideoid_filename(self):
    test_videoid_extractor = FilenameVideoidExtractor('None')
    self.assertIsInstance(test_videoid_extractor, FilenameVideoidExtractor)
    test_videoid_extractor = FilenameVideoidExtractor('.abc.')
    self.assertIsInstance(test_videoid_extractor, FilenameVideoidExtractor)
    self.assertIsNone(test_videoid_extractor.get_videoid())
    self.assertEqual(test_videoid_extractor.get_dot_extension(), '.')
    self.assertEqual(test_videoid_extractor.get_extensionless_filename(), '.abc')
    self.assertIsNone(test_videoid_extractor.get_title_before_videoid())

  def test_7_fetch_a_filename_that_is_exactly_a_11char_videoid(self):
    test_videoid = 'abc123abc12'
    test_videoid_extractor = FilenameVideoidExtractor(test_videoid)
    self.assertIsInstance(test_videoid_extractor, FilenameVideoidExtractor)
    self.assertIsNone(test_videoid_extractor.get_dot_extension())
    self.assertEqual(test_videoid_extractor.get_extensionless_filename(), test_videoid_extractor.get_filename())
    self.assertEqual(test_videoid_extractor.get_videoid(), test_videoid)

  def test_8_fetch_a_filename_that_a_12char_videoid_but_misses_the_dash(self):
    test_videoid = '+abc123abc12'
    test_videoid_extractor = FilenameVideoidExtractor(test_videoid)
    self.assertIsInstance(test_videoid_extractor, FilenameVideoidExtractor)
    self.assertIsNone(test_videoid_extractor.get_dot_extension())
    self.assertEqual(test_videoid_extractor.get_extensionless_filename(), test_videoid_extractor.get_filename())
    self.assertIsNone(test_videoid_extractor.get_videoid())
    
  def test_9_some_filenames_with_extractable_videoid(self):
    test_videoid_filenames = ['  \tasASe3_fd-_.mp4\t\n','     -badAe3_fd-_.mp4  \t']
    for filename in test_videoid_filenames:
      test_videoid_extractor = FilenameVideoidExtractor(filename)
      self.assertIsNotNone(test_videoid_extractor.get_videoid())
      self.assertTrue(test_videoid_extractor.get_videoid() in filename)


def unittests():
  unittest.main()

def process():
  '''
  '''
  filenames = []
  filename = 'Direito Internacional Humanitário _i Maurício Fariña _Aula 1 Direito Humanitário - Conceitos e Distinções-U9QYgLb4kDo.mp4'
  filenames.append(filename)
  filename = 'Direito Internacional Humanitário _i Maurício Fariña _Aula 5 O Brasil nas Operações de Paz-AXO9p0naktA.mp4'
  filenames.append(filename)
  for filename in filenames:
    lecture = FilenameLecturer(filename)
    print lecture

if __name__ == '__main__':
  if 'ut' in sys.argv:
    sys.argv.remove('ut')
    unittests()  
  process()
