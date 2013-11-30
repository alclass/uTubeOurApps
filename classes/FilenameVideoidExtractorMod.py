#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
FilenameVideoidExtractorMod.py
'''
import os, sys

FORBIDDEN_CHARS_IN_YOUTUBEVIDEOID = '!@#$%&*()+=Çç/:;.,[]{}|\\ \'"'
youtubevideoid_having_some_forbidden_char_lambda = lambda s : s in FORBIDDEN_CHARS_IN_YOUTUBEVIDEOID   


class FilenameVideoidExtractor(object):
  
  def __init__(self, filename):
    self.filename = filename
    self.extensionless_filename, self.extension = os.path.splitext(self.filename)
    # self.extlessname = '.'.join(self.filename.split('.')[:-1])
    # Notice self.videoid can be, later, set as None, that's why it's not None here
    self.videoid = 'INIT1234&&&'
  
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
    videoidlist = list(videoid)
    boolean_result_list = map(youtubevideoid_having_some_forbidden_char_lambda, videoidlist)
    if True in boolean_result_list:
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

  def test_1_fixed_videoid_charlength_should_equal_11(self):
    self.assertEqual(self.VIDEOID_CHAR_LEN, len(self.fixed_data.utube_test_videoid))

  def test_2_extract_videoid(self):
    '''
    This test is to cover the helper 
      generate_nonrepeat_sha1sum() unittest method above,
      this is not a business rule, so to say, unittest
    '''
    returned_videoid = self.videoid_extractor.get_videoid()
    self.assertEqual(returned_videoid, self.fixed_data.utube_test_videoid)

  def test_3_get_None_videoid(self):
    test_videoid_extractor = FilenameVideoidExtractor('blah blah as filename')
    should_be_None = test_videoid_extractor.get_videoid()
    self.assertIsNone(should_be_None)
    
  def test_4_compare_titles(self):
    self.assertEqual(self.videoid_extractor.get_title_before_videoid(), self.fixed_data.utube_test_title)


def unittests():
  unittest.main()

def process():
  '''
  '''
  videoid_extractor = FilenameVideoidExtractor(utube_test_filename)
  print 'Extracting videoid...'
  print '... from: ', utube_test_filename
  print 'videoid:', videoid_extractor.get_videoid()

if __name__ == '__main__':
  if 'ut' in sys.argv:
    sys.argv.remove('ut')
    unittests()  
  process()
