'''
  This is the __init__.py script for the uTubeOurApps.uTubeIdsDjango.uTubeIdsDjApp package
  
  "cli", here, stands for Command Line Interface
  
  The purpose of this module is, beyond marking a Python package,
    to insert (dynamically) the all application's parent directories into the PYTHON PATH 
'''

import os, sys

def add_pythonpath(dir_abspath):
  if dir_abspath not in sys.path: 
    sys.path.insert(0, dir_abspath)

def _recursively_search_base_settings_for_pythonpath(current_path):
  if os.path.isdir(current_path):
    folder_contents = os.listdir(current_path)
    if '__base_settings__.py' in folder_contents:
      add_pythonpath(folder_contents)
      import __base_settings__
      __base_settings__._set_django_settings_dir_to_python_path()
  try:
    PARENT_DIR_PATH = '/'.join(current_path.split('/')[:-1])
    if os.path.isdir(PARENT_DIR_PATH):
      return _recursively_search_base_settings_for_pythonpath(PARENT_DIR_PATH)
  except IndexError:
    pass
  return

def _search_base_settings_for_pythonpath():
  this_file_path = os.path.abspath(__file__)
  THIS_DIR_PATH, _ = os.path.split(this_file_path)
  return _recursively_search_base_settings_for_pythonpath(THIS_DIR_PATH)

_search_base_settings_for_pythonpath()
