#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
  moveOutMp3splitFiles.py
  
  This script searches for mp3split foldernames down a given the directory tree 
    and copies the whole directory tree with these foldernames to a target base directory.
    
  From the command line, these script should be used as:
  
  moveOutMp3splitFiles.py ["<source_base_abspath>"] [-t="<target_base_abspath>"]
  
  if source and target base abspaths are not entered, they default to:
  
  source : /run/media/friend/SAMSUNG/Saber Direito TVJus/
  target : /run/media/friend/TOSHIBA EXT/Saber Direito TVJus Mp3split/
'''
import codecs, os, shutil, sys
import __init__
from classes.SabDirLectureFilenameInfoerMod import SabDirLectureFilenameInfoer

#import local_settings as ls 

class DownDirTreeSabDirMp3splitFolderFinder(object):
  '''
  The help doc-string above, for this module, explained the whole job that
    the module's script runs.
    
  '''

  def __init__(self, basedir_abspath):
    self.mp3split_abspaths = []
    self.basedir_abspath   = basedir_abspath

  def walkDownDirTree(self):
    print 'Walking down tree', self.basedir_abspath
    print 'Please, wait a few seconds.'
    found_count = 0
    for dirpath, dirnames, _ in os.walk(self.basedir_abspath):
      mp3folderfound = None
      if 'mp3split' in dirnames:
        mp3folderfound = 'mp3split'
      if 'mp3split-from-wmv' in dirnames:
        if mp3folderfound != None:
          error_msg  = 'There are 2 mp3split* folders...\n'
          error_msg += '...on %s\n' %dirpath
          error_msg += ' *** Please, look into it.'
          raise OSError, error_msg
        mp3folderfound = 'mp3split-from-wmv'
      if mp3folderfound != None:
        try:
          on_folder = dirpath.split('/')[-1]
          if on_folder.find(SabDirLectureFilenameInfoer.MARKER_FOR_INSTRUCTORS) < 0:
            continue
          mp3split_abspath = os.path.join(dirpath, mp3folderfound)
          found_count += 1
          # print found_count, 'Found', mp3folderfound, 'on ...', dirpath[-55:]
          self.mp3split_abspaths.append(mp3split_abspath)
        except AttributeError: # usually when, in var.split(), var is None, having no attribute (it will probably never happen here, for dirpath comes from os.walk())  
          continue

  def print_all_collected_folders(self):
    for i, mp3split_abspath in enumerate(self.mp3split_abspaths):
      seq = i+1
      print seq, mp3split_abspath

  def get_relpath(self, dirpath):
    relpath = dirpath [ len( self.basedir_abspath ) : ]
    if relpath.startswith('/'):
      relpath = relpath.lstrip('/')
    return relpath

  def copy_all_collected_folders_to_target(self, target_base_abspath):
    for i, mp3split_abspath in enumerate(self.mp3split_abspaths):
      seq = i+1
      print seq, mp3split_abspath
      folder_above_abspath = '/'.join(mp3split_abspath.split('/')[:-1])
      relpath = self.get_relpath(folder_above_abspath)
      target_abspath = os.path.join(target_base_abspath, relpath)
      if not os.path.isdir(target_abspath):
        print 'mkdir', target_abspath
        os.makedirs(target_abspath)
      for filename in os.listdir(mp3split_abspath):
        target_file_abspath = os.path.join(target_abspath, filename)
        if os.path.isfile(target_file_abspath) or os.path.isdir(target_file_abspath):
          print 'Cannot copy %s' %target_file_abspath
          print 'File exists on target.'
          continue
        source_file_abspath = os.path.join(mp3split_abspath, filename)
        print 'Copying:'
        print 'From:', source_file_abspath
        print 'To:', target_abspath
        shutil.copy2(source_file_abspath, target_abspath)

  def remove_all_collected_folders(self):
    self.print_all_collected_folders()
    ans = raw_input('Are you sure you want to erase all %d folders above? (y/N*) ' %len(self.mp3split_abspaths))
    if ans.lower() != 'y':
      print 'No folders erased.'
      return
    for i, mp3split_abspath in enumerate(self.mp3split_abspaths):
      seq = i+1
      print seq, 'Removing', mp3split_abspath
      comm = 'rm -rf "%s"' %mp3split_abspath
      os.system(comm)
      print 'No exceptions raised. The %d folders were erased.' %len(self.mp3split_abspaths)

import unittest
class TestFilenameVideoidExtractor(unittest.TestCase):
  
  def setUp(self):
    pass

  def test_1_raise_ValueError_for_None_filepath(self):
    pass


def unittests():
  unittest.main()


def get_target_basedir_abspath_from_sysargv_or_default():
  target_base_abspath_DEFAULT = '/run/media/friend/TOSHIBA EXT/Saber Direito TVJus Mp3split/'
  target_base_abspath = None
  for arg in sys.argv:
    if arg.startswith('-h') or arg.startswith('--help'):
      print __doc__
      return
    if arg.startswith('-t='):
      target_base_abspath = arg[ len('-t=') : ]
      if not os.path.isdir(target_base_abspath):
        raise OSError, 'Folder %s does not exist.' %target_base_abspath
  if target_base_abspath == None:
    target_base_abspath = target_base_abspath_DEFAULT
  return target_base_abspath

from dbInsertVideoidsDownDirTree import get_basedir_abspath_from_sysargv_or_default    
def process():
  
  # 1st part: Find all mp3split and mp3split-from-wmv folders
  basedir_abspath = get_basedir_abspath_from_sysargv_or_default() 
  grabber = DownDirTreeSabDirMp3splitFolderFinder(basedir_abspath)
  grabber.walkDownDirTree()

  # 2nd part: Get target_base_abspath and call method on grabber to copy everything into target
  target_base_abspath = get_target_basedir_abspath_from_sysargv_or_default()
  # grabber.copy_all_collected_folders_to_target(target_base_abspath)
  grabber.remove_all_collected_folders()

if __name__ == '__main__':
  if 'ut' in sys.argv:
    sys.argv.remove('ut')
    unittests()  
  process()
