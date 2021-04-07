#!/usr/bin/env python3
"""
This script forms file youtube-ids.txt which is input for a second script
that reuses youtube-dl and download the youtube videos by their id's, one at a time
"""
import os
# import sys


class CommBase:
  @staticmethod
  def get_commbase_to_postinterpol_seq(filename_with_increment_interpolation):
    commbase = 'weblinksExtractor.py "%(filename_with_increment_interpolation)s"' \
           % {'filename_with_increment_interpolation': filename_with_increment_interpolation} + \
           ' | grep watch > %(seq)d.txt'
    return commbase


def roll_the_htmlfiles(filename_with_increment_interpolation, n_total_pages):
  commbase = CommBase.get_commbase_to_postinterpol_seq(filename_with_increment_interpolation)
  for seq in range(1, n_total_pages + 1):
    comm = commbase % {'seq': seq}
    os.system(comm)


def concatenate_n_cleanup():
  concatenate_n_cleanup()
  comm = 'cat ?.txt > youtube-ids.txt'
  os.system(comm)

  text = open('youtube-ids.txt').read()
  text = text.replace('/watch?v=', '')
  f_output = open('youtube-ids.txt', 'w')
  f_output.write(text)
  f_output.close()


def get_args():
  filename_with_increment_interpolation = ''
  n_total_pages = 10
  return filename_with_increment_interpolation, n_total_pages


def process():
  filename_with_increment_interpolation, n_total_pages = get_args()
  roll_the_htmlfiles(filename_with_increment_interpolation, n_total_pages)
  concatenate_n_cleanup()


if __name__ == '__main__':
  process()
