#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
'''

class VideoIdsComparer(object):

  def __init__(self, local_filename = 'z-filenames.txt'):
    self.local_filename = local_filename
    self.all_filevideoids = None
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
        if youtubeid != None:
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
    if self.all_filevideoids == None:
      self.store_all_filevideoids_on_local_dir()
    return self.all_filevideoids

  def compareLocalIdsWithFileDB(self):
    self.missing_videoids = []; n_missing = 0
    videoidsObj = VideoIdsOnFile(self.local_filename)
    for videoid in videoidsObj.get_videoids_on_file():
      if videoid not in self.all_filevideoids:
        n_missing += 1
        # print n_missing, 'VideoId', videoid, 'in file not on local dir.'
        self.missing_videoids.append(videoid)

  def download_missing_videos(self):
    self.compareLocalIdsWithFileDB()
    print 'Do you want to download the videos below ?'
    print self.missing_videoids
    print 'Total:', len(self.missing_videoids)
    ans = raw_input('(Y/n) ? ')
    if ans in ['n', 'N']:
      return
    total_to_go = len(self.missing_videoids)
    for i, missing_videoid in enumerate(self.missing_videoids):
      p_seq = i + 1 
      download_individual_video(missing_videoid, p_seq, total_to_go)

def download_missing_videoids():
  video_comparer = VideoIdsComparer(local_filename = 'z-filenames.txt')
  video_comparer.download_missing_videos()

def process():
  if len(sys.argv) < 2: # ie, sys.argv[0] contains the script's name and no parameter is present
    download_missing_videoids()
  elif sys.argv[1] == '--checkids':
    checkEveryFileHas11CharId()
  
if __name__ == '__main__':
  process()
