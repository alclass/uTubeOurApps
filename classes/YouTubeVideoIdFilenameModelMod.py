#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
YouTubeVideoIdFilenameModelMod.py
'''
import os, string, sys

from sqlalchemy import create_engine
engine = create_engine('sqlite:///:memory:', echo=True)

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class YouTubeVideoIdFilenameModel(Base):
  '''
  '''

  __tablename__ = 'YouTubeVideoIdFilenames'
  id        = Column(Integer, primary_key=True)
  title     = Column(String(150))
  videoid   = Column(String(11))
  extension = Column(String(12))
  filesize  = Column(Integer)
  sha1hex   = Column(Integer)
  

  def __repr__(self):
    return "<Video(vid='%s', title='%s', ext='%s')>" % (self.videoid, self.title, self.extension)

class Recorder(object):
  
  def __init__(self, videoids_and_extractors_for_folderfilenames_dict):
    self.videoids_and_extractors_for_folderfilenames_dict = videoids_and_extractors_for_folderfilenames_dict
  
  def process(self):
    for extractor in self.videoids_and_extractors_for_folderfilenames_dict.values():
      Session = sessionmaker(bind=engine)
      session = Session()
      vidFilenameObj = YouTubeVideoIdFilenameModel(
        videoid   = extractor.get_videoid(),
        title     = extractor.get_title(),
        extension = extractor.get_extension(),
      )
      session.add(vidFilenameObj)
    
    

import unittest
class TestFilenameVideoidExtractor(unittest.TestCase):
  
  def setUp(self):
    pass

  def test_1_fixed_videoid_charlength_should_equal_11_etal(self):
    pass

def unittests():
  unittest.main()

def process():
  '''
  '''
  pass

if __name__ == '__main__':
  if 'ut' in sys.argv:
    sys.argv.remove('ut')
    unittests()  
  process()
