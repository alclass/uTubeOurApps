#!/usr/bin/env python3
"""
dlYouTubeMissingVideoIdsOnLocalDir.py
  # -*- coding: utf-8 -*-

Explanation: 
  This script reads a .txt file, which has a hardcoded name z-filenames.txt
  that has YouTube filenames as given by youtube-dl
  (this filename is the video title, a '-' (dash), its videoid, then the dot extension)
  It can also read filenames that have starts with '-' (dash) before the videoid, ie,
  filenames that do not have the title part.
  

  Limitations:
  
    A safe rule to check whether an id is a valid videoid or not, that has not been implemented.
    For the time being, videoids have the following checking (in function return_videoid_if_good_or_none(videoid)):
    + it must contain 11 characters;
    + it must not have the following characters: ' ' (blank), '%' nor '.';
    + it must have at least one lowercase letter and one UPPERCASE letter.

***
Though the following is not parameterized, here follows an example with --list-formats:

youtube-dl --list-formats http://www.youtube.com/watch?v=pNDtN4XM8KA
[youtube] Setting language
[youtube] pNDtN4XM8KA: Downloading video webpage
[youtube] pNDtN4XM8KA: Downloading video info webpage
[youtube] pNDtN4XM8KA: Extracting video information
Available formats:
37  :  mp4  [1080x1920]
45  :  webm  [720x1280]
22  :  mp4  [720x1280]
44  :  webm  [480x854]
35  :  flv  [480x854]
43  :  webm  [360x640]
34  :  flv  [360x640]
18  :  mp4  [360x640]
5  :  flv  [240x400]

"""
import glob
import logging
import os
import sys
import time
import string


def print_and_log(line_msg):
  print(line_msg)
  logging.info(line_msg)


BASE_COMMAND_INDIVUAL_VIDEO = 'youtube-dl -w -f 18 http://www.youtube.com/watch?v=%(videoid)s'
TWO_MIN_IN_SECS = 2 * 60


def download_individual_video(videoid, p_seq=1, total_to_go=1):
  ret_val = -1
  loop_seq = 0
  while ret_val != 0:
    loop_seq += 1
    line_msg = '[%s] Downloading with p_seq = %d of %d' % (time.ctime(), p_seq, total_to_go)
    print_and_log(line_msg)
    comm = BASE_COMMAND_INDIVUAL_VIDEO % {'videoid': videoid}
    line_msg = 'loop_seq = %d :: %s' % (loop_seq, comm)
    print_and_log(line_msg)
    ret_val = os.system(comm)
    line_msg = 'retVal = %d' % ret_val
    print_and_log(line_msg)
    if loop_seq > 2:  # ie, it tries 3 times!
      # give up
      return 
    if ret_val != 0:
      print('Pausing for 2 minutes until next issuing of youtube-dl.')
      time.sleep(TWO_MIN_IN_SECS)


def get_videoid_from_extless_filename(extlessname):
  try:
    videoid = extlessname[-11:]
    videoid = return_videoid_if_good_or_none(videoid)
    if videoid is not None:
      return videoid
  except IndexError:
    pass
  return None


def get_videoid_from_filename(filename):
  try:
    extlessname = '.'.join(filename.split('.')[:-1])
    return get_videoid_from_extless_filename(extlessname)
  except IndexError:
    pass
  return None
  

FORBIDDEN_CHARS_IN_YOUTUBEVIDEOID = '!@#$%&*()+=Çç/:;.,[]{}|\\ \'"'
ENC64CHARS = string.digits + string.ascii_uppercase + string.ascii_lowercase + '_-'


def filter_youtubevideoids_are_encode64(ytids):
  return filter(lambda s: s in ENC64CHARS, ytids)


def is_youtubevideoidword_encode64(ytidword):
  if False in filter_youtubevideoids_are_encode64(ytidword):
    return False
  return True


def return_videoid_if_good_or_none(videoid):
  if videoid is None:
    return None
  elif len(videoid) != 11:
    return None
  if not is_youtubevideoidword_encode64(videoid):
    return None
  return videoid


class VideoIdsOnFile(object):

  def __init__(self, local_filename):
    self.local_filename = local_filename
    self.videoids_on_file = []
    self.find_videoids_on_file()

  def find_videoids_on_file(self):
    self.videoids_on_file = []
    lines = open(self.local_filename, encoding='utf8').readlines()
    for line in lines:
      if line.endswith('\n'):
        line = line.rstrip('\n')
      if line.find('.') < 0:
        continue
      # strip extension and recompose filename without extension
      try:
        videoid = get_videoid_from_filename(line)
        videoid = return_videoid_if_good_or_none(videoid)
        if videoid is None:
          continue
        if videoid not in self.videoids_on_file:
          self.videoids_on_file.append(videoid)
      except IndexError:
        continue

  def get_videoids_on_file(self):
    return self.videoids_on_file


def check_every_file_has_11charid():
  mp4s = glob.glob('*.mp4')
  seq = 0
  for mp4 in mp4s:
    try:
      extlessname = os.path.splitext(mp4)[0]
      prefixed_id = extlessname[-12:]
    except IndexError:
      continue
    if prefixed_id.startswith('-'):
      seq += 1
    print(seq, prefixed_id)
  # mp4's total 
  n_of_mp4s = len(mp4s)
  print('nOfMp4s', n_of_mp4s)


class VideoIdsComparer(object):

  def __init__(self, local_filename='z-filenames.txt'):
    self.local_filename = local_filename
    self.all_filevideoids = None
    self.missing_videoids = []
    self.store_all_filevideoids_on_local_dir()

  def store_all_filevideoids_on_local_dir(self):
    self.all_filevideoids = []
    files = os.listdir('.')
    for filename in files:
      if not os.path.isfile(filename):
        continue
      try:
        extlessname = filename
        if filename.find('.') > -1:
          extlessname = os.path.splitext(filename)[0]
        youtubeid = get_videoid_from_extless_filename(extlessname)
        if youtubeid is not None:
          self.all_filevideoids.append(youtubeid)
      except IndexError:
        continue

  def get_all_mp4_videoids_on_local_dir(self):
    mp4s = []
    for filevideoid in self.all_filevideoids:
      if filevideoid.endswith('.mp4'):
        mp4s.append(filevideoid)
    return mp4s

  def get_all_filevideoids_on_local_dir(self):
    if self.all_filevideoids is None:
      self.store_all_filevideoids_on_local_dir()
    return self.all_filevideoids

  def compare_local_ids_with_filedb(self):
    self.missing_videoids = []
    n_missing = 0
    videoids_obj = VideoIdsOnFile(self.local_filename)
    for videoid in videoids_obj.get_videoids_on_file():
      if videoid not in self.all_filevideoids:
        n_missing += 1
        # print n_missing, 'VideoId', videoid, 'in file not on local dir.'
        self.missing_videoids.append(videoid)

  def download_missing_videos(self):
    self.compare_local_ids_with_filedb()
    print('Do you want to download the videos below ?')
    print(self.missing_videoids)
    print('Total:', len(self.missing_videoids))
    ans = input('(Y/n) ? ')
    if ans in ['n', 'N']:
      return
    total_to_go = len(self.missing_videoids)
    for i, missing_videoid in enumerate(self.missing_videoids):
      p_seq = i + 1 
      download_individual_video(missing_videoid, p_seq, total_to_go)


def download_missing_videoids():
  video_comparer = VideoIdsComparer(local_filename='z-filenames.txt')
  video_comparer.download_missing_videos()


def process():
  if len(sys.argv) < 2:  # ie, sys.argv[0] contains the script's name and no parameter is present
    download_missing_videoids()
  elif sys.argv[1] == '--checkids':
    check_every_file_has_11charid()


if __name__ == '__main__':
  process()
