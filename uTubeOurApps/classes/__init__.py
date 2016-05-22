'''
  This is the __init__.py script for the uTubeOurApps.classes package
  
  "cli", here, stands for Command Line Interface
  
  The purpose of this module is, beyond marking a Python package,
    to insert (dynamically) the all application's parent directories into the PYTHON PATH 
'''

import os, sys

def _recursively_insert_dir_to_pythonpath_if_needed(THIS_DIR_PATH):
  if not os.path.isdir(THIS_DIR_PATH):
    return # a point of ending recursion
  folder_contents = os.listdir(THIS_DIR_PATH)
  if '__init__.py' not in folder_contents:
    return # a point of ending recursion
  if THIS_DIR_PATH not in sys.path: 
    sys.path.insert(0, THIS_DIR_PATH)
  try:
    PARENT_DIR_PATH = '/'.join(THIS_DIR_PATH.split('/')[:-1])
    return _recursively_insert_dir_to_pythonpath_if_needed(PARENT_DIR_PATH)
  except IndexError:
    pass
  return # a point of ending recursion
    

def _insert_folder_and_parents_to_pythonpath_if_needed():
  this_file_path = os.path.abspath(__file__)
  THIS_DIR_PATH, _ = os.path.split(this_file_path)
  return _recursively_insert_dir_to_pythonpath_if_needed(THIS_DIR_PATH)

_insert_folder_and_parents_to_pythonpath_if_needed()
