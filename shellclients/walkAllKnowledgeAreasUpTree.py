#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
'''
import codecs, os, sys
import __init__
from classes.SabDirKnowledgeAreaInfoerMod import SabDirKnowledgeAreaInfoer


class UpTreeKnowledgeAreaGrabber(object):

  def __init__(self, basedir_abspath):
    self.dirpath_count  = 0
    self.basedir_abspath = basedir_abspath

  def doUpTreeWalk(self):
    for self.dirpath, _, _ in os.walk(self.basedir_abspath): # dirnames
      # SabDirKnowledgeAreaInfoer.register_knowledges_via_its_foldernames(dirnames, self.dirpath)
      self.extract_knowledge_areas()
  
  def extract_knowledge_areas(self):
      self.dirpath_count += 1
      print self.dirpath_count, 'Processing', self.dirpath,
      k_area = SabDirKnowledgeAreaInfoer.get_knowledge_area_by_relpath(self.dirpath)
      print k_area

import unittest
class TestFilenameVideoidExtractor(unittest.TestCase):
  
  def setUp(self):
    pass

  def test_1_raise_ValueError_for_None_filepath(self):
    pass


def unittests():
  unittest.main()

def process():
  '''
  '''
def process():
  # basedir_abspath = sys.argv[1] 
  #SourceAndTargetBaseDirsKeeper.set_source_basepath(source_basedir_abspath)

  basedir_abspath = '/run/media/friend/SAMSUNG/'
  grabber = UpTreeKnowledgeAreaGrabber(basedir_abspath)
  grabber.doUpTreeWalk()
  print SabDirKnowledgeAreaInfoer.root_ka

if __name__ == '__main__':
  if 'ut' in sys.argv:
    sys.argv.remove('ut')
    unittests()  
  process()
