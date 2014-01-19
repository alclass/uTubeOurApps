'''
  This is the __init__.py script for the uTubeIdsDjango.uTubeIdsDjango package
  
  The purpose of this module is, beyond marking a Python package,
    to insert (dynamically) the parent directory into the PYTHON PATH 
'''

import os, sys

def add_pythonpath(dir_abspath):
  if dir_abspath not in sys.path: 
    sys.path.insert(0, dir_abspath)
  
def recurse_searching_for_downtree_pypackageinitfile(THIS_DIR_PATH):
  try:
    PARENT_DIR_PATH = '/'.join(THIS_DIR_PATH.split('/')[:-1])
    if os.path.isdir(PARENT_DIR_PATH):
      contents = os.listdir(PARENT_DIR_PATH)
      if '__init__.py' in contents:
        add_pythonpath(PARENT_DIR_PATH)
        return recurse_searching_for_downtree_pypackageinitfile(PARENT_DIR_PATH)
  except IndexError:
    pass
  return

def _insert_parent_dir_to_path_if_needed():
  try:
    this_file_path = os.path.abspath(__file__)
    THIS_DIR_PATH, _ = os.path.split(this_file_path)
    if os.path.isdir(THIS_DIR_PATH):
      add_pythonpath(THIS_DIR_PATH)
    recurse_searching_for_downtree_pypackageinitfile(THIS_DIR_PATH)
  except OSError:
    pass

_insert_parent_dir_to_path_if_needed()
