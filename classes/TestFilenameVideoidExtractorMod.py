#!/usr/bin/env python3
"""
FilenameVideoidExtractorMod.py
"""
import FilenameVideoidExtractorMod as Fvidextr
import sys
import unittest


class TestFixedData:
  
  utube_test_videoid = '0yZNJHae3QM'
  utube_test_title = 'Direito Civil - Obrigações, Contratos e Responsabilidade Civil para o Exame de Ordem'
  utube_test_extension = 'mp4'
  utube_test_filename = None

  def __init__(self):
    self.form_filename()
  
  def form_filename(self):
    self.utube_test_filename = '%s-%s.%s' % (self.utube_test_title, self.utube_test_videoid, self.utube_test_extension)
    

class TestFilenameVideoidExtractor(unittest.TestCase):
  
  def setUp(self):
    self.VIDEOID_CHAR_LEN = 11
    self.fixed_data = TestFixedData()
    self.videoid_extractor = Fvidextr.FilenameVideoidExtractor(self.fixed_data.utube_test_filename)

  def test_1_fixed_videoid_charlength_should_equal_11_etal(self):
    self.assertEqual(self.VIDEOID_CHAR_LEN, len(self.fixed_data.utube_test_videoid))
    test_videoid = 'abc123abc12'
    self.assertTrue(Fvidextr.is_youtube_videoid_good(test_videoid))
    test_videoid = '12345678901'
    self.assertEqual(len(test_videoid), Fvidextr.YOUTUBE_VIDEOID_CHARLENGTH)
    self.assertFalse(Fvidextr.is_youtube_videoid_good(test_videoid))
      
  def test_2_extract_videoid(self):
    """
    This test is to cover the helper 
      generate_nonrepeat_sha1sum() unittest method above,
      this is not a business rule, so to say, unittest
    """
    returned_videoid = self.videoid_extractor.get_videoid()
    self.assertEqual(returned_videoid, self.fixed_data.utube_test_videoid)

  def test_3_compare_filename_extension_and_title(self):
    self.assertEqual(self.videoid_extractor.get_filename(), self.fixed_data.utube_test_filename)
    self.assertEqual(self.videoid_extractor.get_dot_extension(), '.' + self.fixed_data.utube_test_extension)
    self.assertEqual(self.videoid_extractor.get_title_before_videoid(), self.fixed_data.utube_test_title)

  def test_4_get_None_videoid(self):
    test_videoid_extractor = Fvidextr.FilenameVideoidExtractor('blah blah as filename')
    should_be_none = test_videoid_extractor.get_videoid()
    self.assertIsNone(should_be_none)
    
  def test_5_raise_for_invalid_filename_as_None_or_dot(self):
    self.assertRaises(ValueError, Fvidextr.FilenameVideoidExtractor, None)
    self.assertRaises(ValueError, Fvidextr.FilenameVideoidExtractor, '.')

  def test_6_noraise_with_nonvideoid_filename(self):
    test_videoid_extractor = Fvidextr.FilenameVideoidExtractor('None')
    self.assertIsInstance(test_videoid_extractor, Fvidextr.FilenameVideoidExtractor)
    test_videoid_extractor = Fvidextr.FilenameVideoidExtractor('.abc.')
    self.assertIsInstance(test_videoid_extractor, Fvidextr.FilenameVideoidExtractor)
    self.assertIsNone(test_videoid_extractor.get_videoid())
    self.assertEqual(test_videoid_extractor.get_dot_extension(), '.')
    self.assertEqual(test_videoid_extractor.get_extensionless_filename(), '.abc')
    self.assertIsNone(test_videoid_extractor.get_title_before_videoid())

  def test_7_fetch_a_filename_that_is_exactly_a_11char_videoid(self):
    test_videoid = 'abc123abc12'
    test_videoid_extractor = Fvidextr.FilenameVideoidExtractor(test_videoid)
    self.assertIsInstance(test_videoid_extractor, Fvidextr.FilenameVideoidExtractor)
    self.assertIsNone(test_videoid_extractor.get_dot_extension())
    self.assertEqual(test_videoid_extractor.get_extensionless_filename(), test_videoid_extractor.get_filename())
    self.assertEqual(test_videoid_extractor.get_videoid(), test_videoid)

  def test_8_fetch_a_filename_that_a_12char_videoid_but_misses_the_dash(self):
    test_videoid = '+abc123abc12'
    test_videoid_extractor = Fvidextr.FilenameVideoidExtractor(test_videoid)
    self.assertIsInstance(test_videoid_extractor, Fvidextr.FilenameVideoidExtractor)
    self.assertIsNone(test_videoid_extractor.get_dot_extension())
    self.assertEqual(test_videoid_extractor.get_extensionless_filename(), test_videoid_extractor.get_filename())
    self.assertIsNone(test_videoid_extractor.get_videoid())
    
  def test_9_some_filenames_with_extractable_videoid(self):
    test_videoid_filenames = ['  \tasASe3_fd-_.mp4\t\n', '     -badAe3_fd-_.mp4  \t']
    for filename in test_videoid_filenames:
      test_videoid_extractor = Fvidextr.FilenameVideoidExtractor(filename)
      self.assertIsNotNone(test_videoid_extractor.get_videoid())
      self.assertTrue(test_videoid_extractor.get_videoid() in filename)


def unittests():
  unittest.main()


def process():
  """
  """
  test_data = TestFixedData()
  videoid_extractor = Fvidextr.FilenameVideoidExtractor(test_data.utube_test_filename)
  print('-'*40)
  print('Extracting videoid from: ', test_data.utube_test_filename)
  print('Extracted videoid:', videoid_extractor.get_videoid())
  print('-'*40)


if __name__ == '__main__':
  if 'ut' in sys.argv:
    sys.argv.remove('ut')
    unittests()  
  process()
