#!/usr/bin/env python3
"""
FilenameVideoidExtractorMod.py
"""
import os
from string import ascii_letters, digits


ALLOWED_CHARS_IN_YOUTUBEVIDEOID = ascii_letters + digits + '_-'  # ie Encode64
YOUTUBE_VIDEOID_CHARLENGTH = 11


def map_youtubevideoid_having_only_allowed_chars(videoidlist):
  return map(lambda s: s in ALLOWED_CHARS_IN_YOUTUBEVIDEOID, videoidlist)


def map_str_having_only_number_digits(videoidlist):
  return map(lambda s: s in digits, videoidlist)


def is_youtube_videoid_good(videoid):  
  videoidlist = list(videoid)
  boolean_result_list = map_youtubevideoid_having_only_allowed_chars(videoidlist)
  if False in boolean_result_list:
    return False
  # a second test: videoid cannot be only number-digits
  boolean_result_list = map_str_having_only_number_digits(videoidlist)
  if False not in boolean_result_list:
    return False
  return True


class FilenameVideoidExtractor:
  
  def __init__(self, filename):
    self.videoid = 'INIT1234&&&'
    self.filename = None
    self.extensionless_filename = None
    self.dot_extension = None
    self.set_filename(filename)
    
  def set_filename(self, filename):
    if filename is None:
      error_msg = "filename for FilenameVideoidExtractor()'s constructor cannot be None."
      raise ValueError(error_msg)
    # this rule will demand the production of a script that preprocesses to guarantee
    # there are no files with beginning or ending spaces
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
    if videoid is None:
      return None
    if len(self.extensionless_filename) < 13:
      return None
    title = self.extensionless_filename[:-12]  # one extra char is the '-' (dash)
    return title

  def fetch_and_set_videoid_from_extensionless_filename(self):
    try:
      if len(self.extensionless_filename) < 11:
        self.videoid = None
        return
      elif len(self.extensionless_filename) > 11:
        if self.extensionless_filename[-12] != '-':
          # ATTENTION: this Business Rule is IMPORTANT.
          # If extensionless name is more than 11 chars, the 12th last one should be a dash '-'
          self.videoid = None
          return
      # elif len(self.extensionless_filename) == 11:
        # okay, if it's exactly 11, let it not have an obligatory '-' (dash)
      videoid = self.extensionless_filename[-11:]
      self.videoid = FilenameVideoidExtractor.validate_and_return_the_11char_youtube_videoid_or_none(videoid)
    except IndexError:
      self.videoid = None

  @staticmethod
  def validate_and_return_the_11char_youtube_videoid_or_none(videoid):
    if videoid is None:
      return None
    elif len(videoid) != 11:
      return None
    videoid_good = is_youtube_videoid_good(videoid)
    if not videoid_good:
      return None
    return videoid


def adhoc_test1():
  target_path = '/media/friend/CompSci 2T Orig/L CompLang videos/P CompLang videos/' \
                'Y Python videocourses & ytvideos/Web CompSci Py ytvideos/WF Py videos/' \
                'Django Py WF ytvideos/Ecommerce Django ytvideos'
  filename = 'z_ls-R_contents-UpDirTree.txt'
  fpath = os.path.join(target_path, filename)
  lines = open(fpath).readlines()
  for line in lines:
    extr = FilenameVideoidExtractor(filename=line)
    vid = extr.get_videoid()
    title = extr.get_title_before_videoid()
    print(vid, title)


def process():
  adhoc_test1()


if __name__ == '__main__':
  process()
