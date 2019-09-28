#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
This script forms file youtube-ids.txt which is input for a second script that reuses youtube-dl and download the youtube videos by their id's, one at a time
'''
import os, sys
sys.path.insert(0, '..')
import lib.wordfunctions as wf

def extract_ytids_from_filenames(filenames_filename):
  '''

  '''
  lines = open(filenames_filename).readlines()
  ytids = []
  for filename in lines:
    name, _ = os.path.splitext(filename)
    try:
      ytid = name[ -11 : ]
      if not wf.is_word_an_11char_restricted_base64(ytid):
        continue
      ytids.append(ytid)
      # print(ytid, name)
    except IndexError:
      pass
  return ytids

def get_args():
  '''

  # for the time  being, there's only one argument (filename)

  :return:
  '''
  filename = 'z-filenames.txt'
  for arg in sys.argv:
    if arg.startswith('-'):
      continue
    else:
      filename = arg
  if not os.path.isfile(filename):
    print ('Filename (%s) is missing on directory.' %filename)
    sys.exit(1)
  # for the time  being, there's only one argument (filename)
  return filename

def process():
  '''

  :return:
  '''
  filenames_filename = get_args()
  ytids = extract_ytids_from_filenames(filenames_filename)
  for ytid in ytids:
    print (ytids)

if __name__ == '__main__':
  process()
