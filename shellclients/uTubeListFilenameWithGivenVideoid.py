#!/usr/bin/env python3
"""
This script picks up all YouTube video ids on the local directory and downwards from it.
The video ids that can be found are those that end a filename before its extension.

Created on 05/jul/2013
Upgraded on 19/mar/2021
  #-*-coding:utf-8-*-

@author: friend
"""
import glob
import os
import sys
from dlYouTubeMissingVideoIdsOnLocalDir import get_videoid_from_filename        


def verify_local_folder(p_videoid):
  # current_folder_abspath = os.path.abspath('.')
  folder_contents = glob.glob('*')
  # allfiles = []
  for content in folder_contents:
    if not os.path.isfile(content):
      continue
    videoid = get_videoid_from_filename(content)
    if videoid is not None and videoid.startswith(p_videoid):
      print('Filename on folder:', content)
      return
  print('Nothing found.')


def process():
  p_videoid = sys.argv[1]
  print('Verifying videoid', p_videoid, 'existence on local folder')
  verify_local_folder(p_videoid)


if __name__ == '__main__':
  process()
