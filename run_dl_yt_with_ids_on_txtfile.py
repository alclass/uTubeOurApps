#!/usr/bin/env python3
"""
"""
import os
import re
import sys
import time
import shellclients.dlYouTubeWithIdsOnTxtFile as dlyt

def adhoc_test():
  youtubeids_folder = '/media/friend/CompSci 2T Orig/L CompLang videos/P CompLang videos/' \
                        'Y Python videocourses & ytvideos/Web CompSci Py ytvideos/WF Py videos/' \
                        'Django Py WF ytvideos/Ecommerce Django ytvideos/' \
                          "CEntrep 11v n' 2020 Oct Django Bootcamp yu CodingEntrepreneurs ytpl"

  txtfilename = 'youtube-ids.txt'
  dlyt.VideoidsGrabberAndDownloader(txtfilename, youtubeids_folder)

if __name__ == '__main__':
  adhoc_test()
