#!/usr/bin/env python3
"""
  # -*- coding: utf-8 -*-

"""
import os
import re
import sys

urlBase = 'www.youtube.com/watch?v=%s'
commBase = 'youtube-dl "%s"'


def get_local_html_file_from_sys_arg():
  htmlfilename = sys.argv[1]
  if os.path.isfile(htmlfilename):
    return htmlfilename
  print('file', htmlfilename, 'is not here on local folder.')
  sys.exit(1)


files_on_currentdir = os.listdir('.')


def is_it_on_currentdir(utubeids):
  for eachFile in files_on_currentdir:
    if eachFile.find(utubeids) > -1:
      return True
  return False
  

def youtubedownload():
  html_filename = get_local_html_file_from_sys_arg()
  re_str = r'/watch[?]v[=](\w+)&'
  re_comp = re.compile(re_str)
  iter_obj = re_comp.findall(open(html_filename).read())
  total = len(iter_obj)
  seq = 0
  u_tube_ids_list = []
  for uTubeIds in iter_obj:
    if uTubeIds in u_tube_ids_list:
      total -= 1
      print('Video repeat, moving on to next one', seq+1, 'of', total)
      continue
    if is_it_on_currentdir(uTubeIds):
      total -= 1
      print('There is a video with the same id %s, moving on to next one' % uTubeIds, seq+1, 'of', total)
      continue
    u_tube_ids_list.append(uTubeIds)
    seq += 1
    print(seq, 'of', total, uTubeIds)
    url = urlBase % uTubeIds
    comm = commBase % url
    os.system(comm)


if __name__ == '__main__':
  # copyToUsb()
  youtubedownload()
