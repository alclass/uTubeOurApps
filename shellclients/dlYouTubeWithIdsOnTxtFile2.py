#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, re, sys, time
'''

This script outputs YouTube videoids that are yet to be downloaded
  comparing TWO text files. (...)

'''

DEFAULT_YOUTUBE_FILENAMES_ALREADY_DOWNLOADED_TXT_FILENAME = 'z-files-with-youtubevideoids-already-downloaded.txt'

#from dlYouTubeMissingVideoIdsOnLocalDir import VideoIdsComparer # a class

class CouldNotExtractNameFromFilename(ValueError):
  pass

def extract_name_from_extension_if_any(filename):
  try:
    pp = filename.split('.')
    if len(pp) == 1:
      return filename
    name = '.'.join(pp[:-1])
    return name
  except IndexError:
    pass
  raise CouldNotExtractNameFromFilename, 'CouldNotExtractNameFromFilename %s' %filename 

FORBIDDEN_CHARS_IN_YOUTUBE_VIDEOID = ' @/\\,?;:><!#$%&*()=\'ç'
lambda_char_in_forbidden_set = lambda c : c in FORBIDDEN_CHARS_IN_YOUTUBE_VIDEOID  
def is_videoid_good(videoid):
  videoidchars = list(videoid)
  true_false_list_result = map(lambda_char_in_forbidden_set, videoidchars)
  if True in true_false_list_result:
    return False
  return True

class VideoidsGrabberAndDownloader(object):
  '''
  This class models the processing of a find, confirm and download YouTube video ids.
  '''
  
  DEFAULT_TXT_FILE = 'youtube-ids.txt'
  MAX_N_TRIES = 3
  
  def __init__(self, youtubeids_filename=None):
    self.set_youtubeids_filename(youtubeids_filename)
    #self.process()

  def set_youtubeids_filename(self, youtubeids_filename=None):
    if youtubeids_filename == None or not os.path.isfile(youtubeids_filename):
      self.youtubeids_filename = self.DEFAULT_TXT_FILE
      return
    self.youtubeids_filename = youtubeids_filename
    
  def process(self):
    self.read_ids_from_txt_file()
    self.compare_ids_with_mp4s_already_on_localdir()
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
        if not is_videoid_good(vid):
          continue
        if vid not in self.videoids_to_download: 
          self.videoids_to_download.append(vid)
      except IndexError: # if line[0] above raises it in case line is empty
        pass

  def read_ids_from_compare_filename_txt_file(self, youtubeids_already_downloaded_filename = None):
    '''
    Take the YouTube video ids from a txt file, line by line and ids starting the 11 first characters.
    '''
    self.videoids_already_downloaded = []
    if youtubeids_already_downloaded_filename == None:
      youtubeids_already_downloaded_filename = DEFAULT_YOUTUBE_FILENAMES_ALREADY_DOWNLOADED_TXT_FILENAME
    lines=open(youtubeids_already_downloaded_filename).readlines()
    vids_total = 0
    n_downloaded = 0
    for line in lines:
      try:
        if line[0]=='#':
          continue
        line = line.rstrip(' \t\r\n')
        name = extract_name_from_extension_if_any(line)
        if len(name) < 11:
          continue
        videoid = name[-11:]
        if is_videoid_good(videoid):
          self.videoids_already_downloaded.append(videoid)
      except IndexError:
        continue

  def set_ids_yet_to_download(self):
    self.videoids_already_to_download = []
    for videoid in self.videoids_to_download:
      if videoid not in self.videoids_already_downloaded:
        self.videoids_already_to_download.append(videoid)
        
  def print_videoids_already_to_download(self):
    print '-'*40
    print 'Video IDs yet to download if any'
    print '-'*40
    for videoid in self.videoids_already_to_download:
      print videoid        
  
  def compare_ids_with_mp4s_already_on_localdir(self):
    video_comparer = VideoIdsComparer()
    mp4_ids_on_localdir = video_comparer.get_all_mp4_videoids_on_local_dir()
    new_video_ids = []
    for vid in self.videoids_to_download:
      if vid not in mp4_ids_on_localdir:
        new_video_ids.append(vid)
    self.videoids_to_download = new_video_ids

  def please_confirm_download(self):
    '''
    To ask the user to confirm or not the download of all taken ids
    '''
    print self.videoids_to_download
    print 'vids_total', len(self.videoids_to_download)
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
  grabber = VideoidsGrabberAndDownloader(youtubeids_filename)
  grabber.read_ids_from_txt_file()
  grabber.read_ids_from_compare_filename_txt_file()
  grabber.set_ids_yet_to_download()
  grabber.print_videoids_already_to_download()
   

if __name__ == '__main__':
  process()
