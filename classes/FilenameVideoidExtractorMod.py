#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
FilenameVideoidExtractorMod.py
'''
import os, string, sys
ALLOWED_CHARS_IN_YOUTUBEVIDEOID = string.ascii_letters + string.digits + '_-'
youtubevideoid_having_only_allowed_chars_lambda = lambda s : s in ALLOWED_CHARS_IN_YOUTUBEVIDEOID
str_having_only_number_digits_lambda = lambda s : s in string.digits
YOUTUBE_VIDEOID_CHARLENGTH = 11   
# FORBIDDEN_CHARS_IN_YOUTUBEVIDEOID = ' !@#$%&*()+=Çç/:;.,[]{}|\\ \'"'
# youtubevideoid_having_some_forbidden_char_lambda = lambda s : s in FORBIDDEN_CHARS_IN_YOUTUBEVIDEOID   

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

class FilenameVideoidExtractor(object):
  
  def __init__(self, filename):
    self.videoid = 'INIT1234&&&'
    self.set_filename(filename)
    
  def set_filename(self, filename):
    if filename == None:
      error_msg = "filename for FilenameVideoidExtractor()'s constructor cannot be None."
      raise ValueError(error_msg)
    # this rule will demand the production of a script that preprocesses to guarantee there are no files with beginning or ending spaces
    filename = filename.lstrip(' \t').rstrip(' \t\r\n')
    self.filename = filename
    extensionless_filename, dot_extension = os.path.splitext(self.filename)
    if extensionless_filename == '.':
      # this is the directory itself, raise ValueError
      error_msg = "filename for FilenameVideoidExtractor()'s constructor cannot be the dot directory."
      raise ValueError(error_msg)
    self.extensionless_filename = extensionless_filename
    self.dot_extension = None
    if dot_extension != '':
      self.dot_extension = dot_extension
    self.fetch_and_set_videoid_from_extensionless_filename()  

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
  test_data = TestFixedData()
  videoid_extractor = FilenameVideoidExtractor(test_data.utube_test_filename)
  print ('-'*40)
  print ('Extracting videoid from: ', test_data.utube_test_filename)
  print ('Extracted videoid:', videoid_extractor.get_videoid())
  print ('-'*40)

if __name__ == '__main__':
  if 'ut' in sys.argv:
    sys.argv.remove('ut')
    unittests()  
  process()
