#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
'''
import codecs, os, sys
from FilenameVideoidExtractorMod import FilenameVideoidExtractor
import __init__
import local_settings as ls 

filter_filenames_by_dot_extension_lambda = lambda f, dot_extension : f.endswith(dot_extension)

class VideoIdsOnFolderFilenamesFinder(object):
  '''
  An instance of this class aims to wrap the filenames in a directory, given to the constructor,
  in objects of the FilenameVideoidExtractor class.
  
  That is, every filename that has a YouTube videoid extractable will be kept inside
    the videoids_and_extractors_for_folderfilenames_dict dict.
  
  Client Use of this class
  ========================
  
  The main use of this class is from a tree-dir-walker, that obtains the data
    from this class' instance and saves it to a database of some sort.
    
  The database, in its turn, has at least two uses:
  1) help avoid download a video that has already been downloaded;
  2) facilitate reports (eg. on a webpage) that list title by videoid.
   
  '''

  def __init__(self, videoids_folder_abspath=None):
    '''
    '''
    self.set_videoids_folder_abspath(videoids_folder_abspath)
    self.videoids_and_extractors_for_folderfilenames_dict = None
    self.extract_videoids_from_filenames_on_folder()

  def set_videoids_folder_abspath(self, videoids_folder_abspath=None):
    if videoids_folder_abspath==None or not os.path.isdir(videoids_folder_abspath):
      self.videoids_folder_abspath = os.path.abspath('.')
      return
    self.videoids_folder_abspath = videoids_folder_abspath 
    
  def extract_videoids_from_filenames_on_folder(self, reread=False):
    '''
    Important Semantic Detail:
      the extraction is from the filename, not from the file contents inside itself.
    '''
    if self.videoids_and_extractors_for_folderfilenames_dict != None and not reread:
      return 
    self.videoids_and_extractors_for_folderfilenames_dict = {}
    filenames = os.listdir(self.videoids_folder_abspath)
    for filename in filenames:
      if not os.path.isfile(self.get_abspath_for_filename(filename)):
        continue
      videoid_extractor = FilenameVideoidExtractor(filename)
      youtubeid = videoid_extractor.get_videoid()
      if youtubeid != None:
        self.videoids_and_extractors_for_folderfilenames_dict[youtubeid] = videoid_extractor 

  def get_videoids_and_extractors_for_folderfilenames_dict(self, reread=False):
    if self.videoids_and_extractors_for_folderfilenames_dict != None and not reread:
      return self.videoids_and_extractors_for_folderfilenames_dict
    self.extract_videoids_from_filenames_on_folder(reread)
    return self.videoids_and_extractors_for_folderfilenames_dict
    

  def get_abspath_for_filename(self, filename):
    return os.path.join(self.videoids_folder_abspath, filename)

  def get_all_folder_filenames_with_a_videoid(self):
    filenames = []
    for youtubeid in self.videoids_and_extractors_for_folderfilenames_dict:
      videoid_extractor = self.videoids_and_extractors_for_folderfilenames_dict[videoid]
      filenames.append(videoid_extractor.get_filename())
    return filenames

  def get_folder_filenames_with_a_videoid_by_dot_extension(self, dot_extension=None):
    filenames = self.get_all_folder_filenames_with_a_videoid()
    if None in filenames:
      raise ValueError, 'This is apparently a program or logic error. There is a None inside a list coming from get_all_folder_filenames_with_a_videoid()'
    return filter(filter_filenames_by_dot_extension_lambda, filenames) 

  def get_videoids_from_folder_filenames_listing(self):
    return self.videoids_and_extractors_for_folderfilenames_dict.keys()

  def get_total_videoids_from_folder_filenames_listing(self):
    return len(self.get_videoids_from_folder_filenames_listing())


class VideoIdsOnATextFileFinder(VideoIdsOnFolderFilenamesFinder):
  '''
  '''

  def __init__(self, textfile_abspath=None):
    '''
    '''
    self.videoids_textfile_abspath = None
    self.videoids_folder_abspath   = None
    self.videoids_text_filename    = None
    self.set_textfile_abspath(textfile_abspath)
    super(VideoIdsOnATextFileFinder, self).__init__(self.videoids_folder_abspath)
    self.all_filenames_inside_textfile = None
    self.videoids_and_extractors_for_textfile_dict    = None 
    self.videoids_on_textfile_missing_on_folder_files = None
    self.extract_videoids_from_textfile()

  def set_textfile_abspath(self, textfile_abspath=None):
    if textfile_abspath==None or not os.path.isfile(textfile_abspath):
      self.set_textfile_abspath_with_default_or_raise()
      return
    self.set_videoids_text_folder_and_file_abspath_and_filename(textfile_abspath)
    
  def set_textfile_abspath_with_default_or_raise(self):
    current_folder_abspath = os.path.abspath('.')
    textfile_abspath = os.path.join(current_folder_abspath, ls.VIDEOIDS_FILENAMES_INSIDE_TEXTFILENAME_DEFAULT)
    if not os.path.isfile(textfile_abspath):
      raise OSError, 'Error: The default videoids text file (%s) does not exist.' %textfile_abspath
    self.set_videoids_text_folder_and_file_abspath_and_filename(textfile_abspath)

  def set_videoids_text_folder_and_file_abspath_and_filename(self, textfile_abspath):
    '''
    IMPORTANT/OBS.: This method is PRIVATE!!! It can only be invoked from within this class
    '''
    self.videoids_textfile_abspath = textfile_abspath
    self.videoids_folder_abspath, self.videoids_text_filename = os.path.split(self.videoids_textfile_abspath)

  def read_and_set_all_filenames_from_videoids_textfile(self, reread=False):
    if self.all_filenames_inside_textfile != None and not reread:
      return self.all_filenames_inside_textfile
    f = codecs.open(self.videoids_textfile_abspath, 'r', encoding='utf-8')
    filetext = f.read()
    f.close()
    lines = filetext.split('\n')
    self.all_filenames_inside_textfile = []
    for line in lines:
      filename = line.lstrip(' \t').rstrip(' \t\r\n')
      if len(filename) == 0:
        continue 
      self.all_filenames_inside_textfile.append(filename)

  def get_all_filenames_from_videoids_textfile(self, reread=False):
    self.read_and_set_all_filenames_from_videoids_textfile(reread)
    return self.all_filenames_inside_textfile 

  def get_videoids_filenames_from_textfile(self, reread=False):
    self.extract_videoids_from_textfile(reread)
    filenames = []
    for videoid_extractor in self.videoids_and_extractors_for_textfile_dict.values():
      filenames.append(videoid_extractor.get_filename())
    return filenames 
    
  def extract_videoids_from_textfile(self, reread=False):
    if self.videoids_and_extractors_for_textfile_dict != None and not reread:
      return
    self.videoids_and_extractors_for_textfile_dict = {}    
    for filename in self.get_all_filenames_from_videoids_textfile(reread):
      try:
        videoid_extractor = FilenameVideoidExtractor(filename)
        videoid = videoid_extractor.get_videoid()
        if videoid != None:
          self.videoids_and_extractors_for_textfile_dict[videoid] = videoid_extractor
      except ValueError:
        continue

  def find_videoids_on_textfile_missing_on_folder_files(self, reread=False):
    '''
    '''
    if self.videoids_on_textfile_missing_on_folder_files != None and not reread:
      return
    self.extract_videoids_from_textfile(reread)
    self.extract_videoids_from_filenames_on_folder(reread)
    self.videoids_on_textfile_missing_on_folder_files = []
    for videoid in self.videoids_and_extractors_for_textfile_dict:
      if videoid in self.videoids_and_extractors_for_folderfilenames_dict:
        continue
      self.videoids_on_textfile_missing_on_folder_files.append(videoid)

  def get_videoids_on_textfile_missing_on_folder_files(self, reread=False):
    if self.videoids_on_textfile_missing_on_folder_files != None and not reread:
      return self.videoids_on_textfile_missing_on_folder_files
    self.find_videoids_on_textfile_missing_on_folder_files(reread)
    return self.videoids_on_textfile_missing_on_folder_files

  def get_videoids_and_extractors_from_textfile(self, reread=False):
    if self.videoids_and_extractors_for_textfile_dict == None or reread:
      self.extract_videoids_from_textfile(reread)
    return self.videoids_and_extractors_for_textfile_dict

  def get_videoids_from_textfile(self, reread=False):
    if self.videoids_and_extractors_for_textfile_dict == None or reread:
      self.extract_videoids_from_textfile(reread)
    return self.videoids_and_extractors_for_textfile_dict.keys()

  def get_total_videoids_from_textfile(self):
    return len(self.videoids_and_extractors_for_textfile_dict) 
    
  def download_missing_videos(self):
    '''
    '''
    if self.videoids_on_textfile_missing_on_folder_files == None:
      self.find_videoids_on_textfile_missing_on_folder_files()
    for filename in self.videoids_on_textfile_missing_on_folder_files:
      print filename
    files_download_total = len(self.videoids_on_textfile_missing_on_folder_files)
    print 'Total:', files_download_total 
    print 'Do you want to download the videos above ?'
    ans = raw_input('(Y/n) ? ')
    if ans in ['n', 'N']:
      return
    for i, missing_videoid in enumerate(self.videoids_on_textfile_missing_on_folder_files):
      p_seq = i + 1 
      download_individual_video(missing_videoid, p_seq, files_download_total)

N_OF_FILENAMES_INSIDE_TEST_VIDEOIDS_FILE = 2
def read_test_videoids_file_create_it_if_needed(n_of_retries=0):
  text_to_file = '''
  asASe3_fd-_.mp4    
  -badAe3_fd-_.mp4
  '''
  test_videoids_filename = 'z-test-videoids-filenames.txt'
  videoids_file_abspath = os.path.join(os.path.abspath('.'), test_videoids_filename)
  if os.path.isfile(videoids_file_abspath):
    f = codecs.open(videoids_file_abspath, 'r', encoding='utf-8')
    text_from_file = f.read()
    f.close()
    if text_to_file == text_from_file:
      return text_to_file, videoids_file_abspath
  if n_of_retries > 0:
    raise IOError, 'Could not read videoids file %s from disk.' %videoids_file_abspath
  f = codecs.open(videoids_file_abspath, 'w', encoding='utf-8')
  f.write(text_to_file)
  f.close()
  return read_test_videoids_file_create_it_if_needed(n_of_retries=1)

import unittest
class TestFilenameVideoidExtractor(unittest.TestCase):
  
  def setUp(self):
    self.videoids_on_filenames_finder = VideoIdsOnFolderFilenamesFinder()

  def test_1_raise_ValueError_for_None_filepath(self):
    self.assertIsInstance(self.videoids_on_filenames_finder, VideoIdsOnFolderFilenamesFinder)
    n = self.videoids_on_filenames_finder.get_total_videoids_from_folder_filenames_listing()
    self.assertEqual(type(n), int)
    
  def test_2_raise_ValueError_for_None_filepath(self):
    #self.assertRaises(valueError, VideoIdsOnFolderFilenamesFinder)
    #self.assertRaises(valueError, VideoIdsOnFolderFilenamesFinder, None)
    pass
    #self.assertRaises(ValueError, VideoIdsOnATextFileFinder)
    #self.assertRaises(ValueError, VideoIdsOnATextFileFinder, None)

  def test_3_raise_ValueError_for_None_filepath(self):
    filetext, videoids_file_abspath = read_test_videoids_file_create_it_if_needed()
    videoids_inside_a_file_finder = VideoIdsOnATextFileFinder(videoids_file_abspath)
    self.assertIsInstance(videoids_inside_a_file_finder, VideoIdsOnATextFileFinder)
    n = videoids_inside_a_file_finder.get_total_videoids_from_textfile()
    self.assertEqual(N_OF_FILENAMES_INSIDE_TEST_VIDEOIDS_FILE, 2)
    missing_videoids = videoids_inside_a_file_finder.get_videoids_on_textfile_missing_on_folder_files()
    all_videoids = videoids_inside_a_file_finder.get_videoids_from_textfile()
    self.assertEqual(missing_videoids, all_videoids)
    


def unittests():
  unittest.main()

def process():
  '''
  '''
  filetext, videoids_file_abspath = read_test_videoids_file_create_it_if_needed()
  videoids_inside_a_file_finder = VideoIdsOnATextFileFinder(videoids_file_abspath)
  print 'all filenames with a videoid', videoids_inside_a_file_finder.get_all_filenames_from_videoids_textfile()
  print 'filenames with a videoid', videoids_inside_a_file_finder.get_videoids_filenames_from_textfile()
  print 'get_total_videoids_from_textfile() =', videoids_inside_a_file_finder.get_total_videoids_from_textfile()
  print 'get_videoids_from_textfile() =', videoids_inside_a_file_finder.get_videoids_from_textfile()
  print 'get_videoids_on_textfile_missing_on_folder_files() =', videoids_inside_a_file_finder.get_videoids_on_textfile_missing_on_folder_files()
  pass

if __name__ == '__main__':
  if 'ut' in sys.argv:
    sys.argv.remove('ut')
    unittests()  
  process()
