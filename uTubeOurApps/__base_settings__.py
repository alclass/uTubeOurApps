'''
  This is the __init__.py script for the uTubeOurApps (basedir for itself) package
  
  "cli", here, stands for Command Line Interface
  
  The purpose of this module is, beyond marking a Python package,
    to insert (dynamically) the parent directory into the PYTHON PATH 
'''

import os, sys

def add_pythonpath(dir_abspath):
  if dir_abspath not in sys.path: 
    sys.path.insert(0, dir_abspath)

def _set_django_settings_dir_to_python_path():
  this_file_path = os.path.abspath(__file__)
  THIS_DIR_PATH, _ = os.path.split(this_file_path)
  DJANGO_BASEDIRNAME ='uTubeIdsDjango'
  DJANGO_BASEDIR = os.path.join(THIS_DIR_PATH, DJANGO_BASEDIRNAME)
  add_pythonpath(DJANGO_BASEDIR)
  