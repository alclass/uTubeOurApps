#!/usr/bin/env python3
"""

"""
import os
import sys
import unittest
from FilenameVideoidExtractorMod import FilenameVideoidExtractor


class FilepathVideoidExtractor(FilenameVideoidExtractor):
  
  def __init__(self, file_abspath, simulate=False):
    if not simulate:
      if not os.path.isfile(file_abspath):
        error_msg = 'File %s does not exist.' % file_abspath
        raise OSError(error_msg)
    folder_abspath, filename = os.path.split(file_abspath)
    if not folder_abspath or folder_abspath == '':
      error_msg = 'Folder %s does not exist for file %s.' % (folder_abspath, file_abspath)
      raise OSError(error_msg)
    if not filename or filename == '':
      error_msg = 'Filename %s does not exist for file %s.' % (filename, file_abspath)
      raise OSError(error_msg)
    self.folder_abspath = folder_abspath
    self.file_abspath = file_abspath
    super(FilepathVideoidExtractor, self).__init__(filename)
  
  def get_file_abspath(self):
    return self.file_abspath 
    
  def get_folder_abspath(self):
    return self.folder_abspath 


class TestFilepathVideoidExtractor(unittest.TestCase):

  def test_1(self):
    folder_abspath = '/abc/def'
    videoid = '12345678901'
    filename = 'file -%s.txt' % videoid
    file_abspath = os.path.join(folder_abspath, filename)
    filepathobj = FilepathVideoidExtractor(file_abspath, simulate=True)
    self.assertEqual(folder_abspath, filepathobj.get_folder_abspath())
    self.assertEqual(file_abspath, filepathobj.get_file_abspath())
    self.assertEqual(filename, filepathobj.get_filename())
    self.assertEqual(videoid, filepathobj.get_videoid())
    

def unittests():
  unittest.main()


def process():
  """
  test_data = TestFixedData()
  videoid_extractor = FilenameVideoidExtractor(test_data.utube_test_filename)
  print '-'*40
  print 'Extracting videoid from: ', test_data.utube_test_filename
  print 'Extracted videoid:', videoid_extractor.get_videoid()
  print '-'*40
  """
  pass


if __name__ == '__main__':
  if 'ut' in sys.argv:
    sys.argv.remove('ut')
    unittests()  
  process()
