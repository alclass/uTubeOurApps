#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, re, sys, time
'''

This script downloads videoid inside a text file that are
  not (yet) present on the local folder, and, by extension, on a database of videoids.

The 3 steps below further explain the functionality of this script:
  
  1) This script reads a list of YouTube Video Ids from a text file (default name is 'youtube-ids.txt')
       This file must have the 11-character video id starting each line. 
       (A "#" at the beginning of a line ignores that line.)
  
  2) The video ids collected from 'youtube-ids.txt' (or some other file chosen) are compared with the
       mp4s that have videoids ending the filename before the extension.
       The 11-char-id before extension is a "business rule" convention.
         Without it, this system DOES NOT work!)

       If this videoid is already present, it is discarded.
       If not present, it queues it up to be downloaded.
       
    It's important to notice that not only the program looks up the current dir for id's,
      it also looks up the whole database that stores all videoids that have been
      previously recorded on the database.
    This database search must be configured in local_settings.py, because
      it can either be done by reading a z_ls-R_contents* file or a SQL database.
  
  3) A confirmation yes/no for the queued-up download list is asked on the shell-terminal,
     ie, download will only begin if the user doesn't say 'no' (n or N).

'''


from dlYouTubeMissingVideoIdsOnLocalDir import VideoIdsComparer # a class
import __init__
from classes.VideoIdsOnATextFileFinderMod import VideoIdsOnATextFileFinder
import local_settings as ls 

class VideoidsGrabberAndDownloader(object):
  '''
  This class models the processing of a "find", asks confirmation for downloading
    videoids collected, and, if confirmed, downloads the YouTube videoids listed.
    
  The videoids listed are those that exist on youtube-ids.txt (or other file)
    and were not found on 3 kinds of places (the 3 levels of searching for collected videos "here")
    
  The "here" videos are simply videos that have already been downloaded
    and should not be downloaded again
  '''
  
  DEFAULT_TXT_FILE = 'youtube-ids.txt'
  PREFIX_TO_LS_R_CONTENTS_TEXT_FILE = ls.PREFIX_TO_LS_R_CONTENTS_TEXT_FILE
  # PREFIX_TO_LS_R_CONTENTS_TEXT_FILE = 'z_ls-R_contents'
  MAX_N_TRIES = 3
  
  def __init__(self, youtubeids_filename=None):
    self.set_youtubeids_filename(youtubeids_filename)
    self.all_videoids_here = [] 
    self.process()

  def set_youtubeids_filename(self, youtubeids_filename=None):
    if youtubeids_filename == None or not os.path.isfile(youtubeids_filename):
      self.youtubeids_filename = self.DEFAULT_TXT_FILE
      return
    self.youtubeids_filename = youtubeids_filename
    
  def process(self):
    self.read_ids_from_txt_file()
    self.grab_videoids_here()
    self.compare_videoids_with_all_collected_videos_here()
    self.please_confirm_download()
    self.download_videos_by_their_ids()

  def find_alternative(self):
    '''
    Not yet fully implemented
    '''
    files = os.listdir('.')
    print files
    idstr = 'id[=](.+)[.]'
    idstr_re = re.compile(idstr)
    vids = []
    for eachfile in files:
      matchObj = idstr_re.search(eachfile)
      if matchObj:
        vid = matchObj.group(1)
        if vid not in vids:
          print 'Found vid', vid
          vids.append(vid)

  def read_ids_from_txt_file(self):
    '''
    Take the YouTube video ids from a txt file, line by line and ids starting the 11 first characters.
    '''
    self.videoids_to_download = []
    lines=open(self.youtubeids_filename).readlines()
    vids_total = 0
    n_downloaded = 0
    for line in lines:
      try:
        if line[0]=='#':
          continue
        vid = line.rstrip('\n')
        if len(vid) < 11:
          continue
        if len(vid) > 11:
          vid = vid[:11]
        if vid not in self.videoids_to_download: 
          self.videoids_to_download.append(vid)
      except IndexError: # if line[0] above raises it in case line is empty
        pass

  def compare_videoids_with_all_collected_videos_here(self):
    new_video_ids = []
    for vid in self.videoids_to_download:
      if vid not in self.all_videoids_here:
        new_video_ids.append(vid)
    self.videoids_to_download = new_video_ids

  def add_videoids_from_contents_text_file(self, dir_content, current_abspath):
    contents_text_file_abspath = os.path.join(current_abspath, dir_content)
    if os.path.isfile(contents_text_file_abspath):
      videoid_on_textfile_finder = VideoIdsOnATextFileFinder(contents_text_file_abspath)
      videoids = videoid_on_textfile_finder.get_videoids_from_textfile()
      self.all_videoids_here += videoids 

  def grab_videoids_here(self):
    '''
    grab_videoids_here() means videos that have already been download 
      and should not be downloaded again
      
    There are 3 levels of grabbing videoids-here:
    1st level) the videoids that exist on filenames on localdir
    2nd level) the videoids that exist inside every file prefixed "z_ls-R_contents" every path down to / (root), excepting root itself
    3rd level) the videoids that exist on a database (the database connection and config must be available on local_settings.py
    '''
    self.grab_videoids_on_files_on_localdir()
    self.grab_videoids_on_root_textfiles()
    self.grab_videoids_on_database()

  def grab_videoids_on_files_on_localdir(self):
    video_comparer = VideoIdsComparer()
    all_filevideoids_on_localdir = video_comparer.get_all_filevideoids_on_local_dir()
    for videoid in all_filevideoids_on_localdir:
      if videoid not in self.all_videoids_here:
        self.all_videoids_here.append(videoid)

  def grab_videoids_on_root_textfiles(self):
    current_abspath = os.path.abspath('.')
    n_of_split_index_errors = 0
    while current_abspath not in ['/', '', ' ']:
      try:
        pp = current_abspath.split('/')
        current_abspath = '/'.join(pp[:-1])
        # current_abspath is now parent_dir
        if os.path.isdir(current_abspath):
          dir_contents = os.listdir(current_abspath)
          for dir_content in dir_contents:
            if dir_content.startswith(self.PREFIX_TO_LS_R_CONTENTS_TEXT_FILE):
              self.add_videoids_from_contents_text_file(dir_content, current_abspath)
        else:
          # parent_dir does not exist, break from while
          break  
      except IndexError:
        n_of_split_index_errors += 1
        if n_of_split_index_errors > 2:
          break
  
  def grab_videoids_on_database(self):
    '''
    Not yet implemented
    '''
    pass

  def please_confirm_download(self):
    '''
    To ask the user to confirm or not the download of all taken ids
    '''
    if len(self.videoids_to_download) > 0:
      print 'Videoids to download:'
      print self.videoids_to_download
    print 'Total videoids to download:', len(self.videoids_to_download)
    if len(self.videoids_to_download) > 0:
      ans = raw_input(' Y*/n ')
      if ans in ['n', 'N']:
        sys.exit(0)
  
  def download_videos_by_their_ids(self):
    '''
    Loop all video ids, issuing download one by one
    '''
    self.n_downloaded = 0
    for i, vid in enumerate(self.videoids_to_download):
      n_seq = i + 1
      self.issue_download(n_seq, vid)
        
  def issue_download(self, n_seq, vid):
    '''
    Proceed download of passed-on video id
    '''
    n_tries = 1
    while n_tries <= self.MAX_N_TRIES:
      print  n_seq, 'n.of dl. so far', self.n_downloaded, 'of', len(self.videoids_to_download), 'video', vid, 'n_tries', n_tries, '[%s]' %time.ctime()
      comm = 'youtube-dl -f 18 "http://www.youtube.com/?v=%s"' %vid
      print comm
      ret_val = os.system(comm)
      if ret_val == 0:
        self.n_downloaded += 1
        return
      print 'Problem with the download: waiting 3 min.'
      time.sleep(3*60)
      n_tries += 1
    print 'After', self.MAX_N_TRIES, 'tries, given up downloading', vid


def process():
  youtubeids_filename = None
  try:
    youtubeids_filename = sys.argv[1]
  except IndexError:
    pass
  VideoidsGrabberAndDownloader(youtubeids_filename)  

if __name__ == '__main__':
  process()
