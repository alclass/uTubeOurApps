#!/usr/bin/env python
"""
FilenameLecturerMod.py
"""
import sys


class SabDirKnowledgeAreaInfoer(object):

  K_AREA_START_MARKER = '_a '
  K_AREA_FINISH_MARKER = ' (videoaulas SabDir)'
  ROOT_KA = None  # all k_areas are tree-derived from the ROOT knowledge area, search happens thru' children objects
  
  @staticmethod
  def get_kas_by_name_recursive(k_area_name, parent_ka, kas=None):
    if kas is None:
      kas = []
    if k_area_name in parent_ka.children_dict.keys():
      # only 1 may exist per parent, ie k area names are unique with a parent
      kas.append(parent_ka.children_dict[k_area_name])
    for child_ka in parent_ka.children_dict.values():
      kas += SabDirKnowledgeAreaInfoer.get_kas_by_name_recursive(k_area_name, child_ka, [])
    return kas

  @staticmethod
  def get_kas_by_name(k_area_name, kas=None):
    if kas is None:
      kas = []
    root_ka = SabDirKnowledgeAreaInfoer.get_root_knowledge_area()
    if k_area_name == root_ka.k_area_name:
      return [root_ka] # root should have a unique name, so return and look no further
    return SabDirKnowledgeAreaInfoer.get_kas_by_name_recursive(k_area_name, root_ka, kas)

  @staticmethod
  def get_or_create(k_area_name, parent_k_area):
    if parent_k_area is None:
      parent_k_area = SabDirKnowledgeAreaInfoer.get_root_knowledge_area()
    if k_area_name in parent_k_area.children_dict.keys():
      k_area = parent_k_area.children_dict[k_area_name]
      return k_area
    k_area = SabDirKnowledgeAreaInfoer(k_area_name, parent_k_area)
    return k_area

  @staticmethod
  def return_k_area_name_if_marked_or_None(name):
    STA_MARKER = SabDirKnowledgeAreaInfoer.K_AREA_START_MARKER
    FIN_MARKER = SabDirKnowledgeAreaInfoer.K_AREA_FINISH_MARKER
    k_area_name = None
    if name.startswith(STA_MARKER):
      k_area_name = name [ len(STA_MARKER) : ]
      if k_area_name.endswith(FIN_MARKER):
        k_area_name = k_area_name [ : - len(FIN_MARKER) : ]
      k_area_name = k_area_name.lstrip(' ,;\t').rstrip(' ,;\t\r\n')
    return k_area_name 

  @staticmethod
  def filter_in_foldernames_with_k_area_start_marker(relpath):
    STA_MARKER = SabDirKnowledgeAreaInfoer.K_AREA_START_MARKER
    pos_a = relpath.find('_a ')
    if pos_a > -1:
      workpath = relpath [ pos_a : ]
    else:
      return []
    foldernames = workpath.split('/')
    foldernames_with_ka_marker = []
    for foldername in foldernames:
      if foldername.startswith(STA_MARKER):
        foldernames_with_ka_marker.append(foldername)
      else:
        break
    return foldernames_with_ka_marker

  @staticmethod
  def get_knowledge_area_by_relpath(relpath):
    '''
    This method also works with abspathes
    '''
    root_ka = SabDirKnowledgeAreaInfoer.get_root_knowledge_area()
    direito_ka = SabDirKnowledgeAreaInfoer.get_or_create('Direito', root_ka)
    if relpath == None: 
      return root_ka
    foldernames_with_ka_marker = SabDirKnowledgeAreaInfoer.filter_in_foldernames_with_k_area_start_marker(relpath) 
    if len(foldernames_with_ka_marker) == 0:
      return root_ka
    previous_k_area = direito_ka
    current_k_area  = direito_ka
    for foldername in foldernames_with_ka_marker:
      k_area_name = SabDirKnowledgeAreaInfoer.return_k_area_name_if_marked_or_None(foldername)
      if k_area_name != None:
        current_k_area = SabDirKnowledgeAreaInfoer.get_or_create(k_area_name, previous_k_area)
        previous_k_area = current_k_area
    return current_k_area

  @staticmethod
  def get_root_knowledge_area():
    if SabDirKnowledgeAreaInfoer.ROOT_KA == None:
      root_ka = SabDirKnowledgeAreaInfoer(k_area_name = 'ROOT_KA')
      root_ka.children_dict = {}
      SabDirKnowledgeAreaInfoer.ROOT_KA = root_ka 
    return SabDirKnowledgeAreaInfoer.ROOT_KA 

  @staticmethod
  def extract_knowledge_area_from_marked_str(marked_str):
    STA_MARKER = SabDirKnowledgeAreaInfoer.K_AREA_START_MARKER
    FIN_MARKER = SabDirKnowledgeAreaInfoer.K_AREA_FINISH_MARKER
    k_area_str = None
    if marked_str.startswith(STA_MARKER):
      k_area_str = marked_str[ len( STA_MARKER ) : ]
      if k_area_str.endswith(FIN_MARKER):
        k_area_str = k_area_str [ : -len( FIN_MARKER ) ]
      k_area_str = k_area_str.lstrip(' ,;-_\t').rstrip(' ,;-_\t\r\n')
    return k_area_str

  @property
  def root_ka(self):
    return self.get_root_knowledge_area()

  def __init__(self, k_area_name, parent_ka=None):
    self.k_area_name = k_area_name
    self.parent_ka   = parent_ka
    self.children_dict = {}
    if self.parent_ka != None:
      self.add_self_to_parent()

  def add_self_to_parent(self):
    self.parent_ka.children_dict[self.k_area_name] = self
    
  def write_flat(self, vertical_bar=False):
    outstr = ''
    if vertical_bar:
       outstr += ' | '
    outstr += '%s' %self.k_area_name
    if self.parent_ka !=None and self.parent_ka != SabDirKnowledgeAreaInfoer.get_root_knowledge_area():
      outstr += self.parent_ka.write_flat(vertical_bar=True)
    return outstr 

  def __str__(self, n_indents=0):
    outstr = ''; indents = ''
    if n_indents > 0:
      indents = '\t'*n_indents
    outstr += '%s[%s]\n' %(indents, self.k_area_name)
    k_area_names = self.children_dict.keys()
    sorted(k_area_names)
    for k_area_name in k_area_names:
      child_ka = self.children_dict[k_area_name]
      outstr += child_ka.__str__(n_indents + 1)
    return outstr

  @staticmethod
  def print_all_kas():
    root_ka = SabDirKnowledgeAreaInfoer.get_root_knowledge_area()
    return SabDirKnowledgeAreaInfoer.print_recursive(root_ka)

  @staticmethod
  def print_recursive(k_area):
    print(k_area)
    for child_ka in k_area.children_dict.values():
      SabDirKnowledgeAreaInfoer.print_recursive(child_ka)
      
    


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
  area_str = 'Direito'
  base_ka = SabDirKnowledgeAreaInfoer.get_or_create(area_str, SabDirKnowledgeAreaInfoer.get_root_knowledge_area())

  area_str = 'Direito Civil'
  civil = SabDirKnowledgeAreaInfoer.get_or_create(area_str, base_ka)
  area_str = u'Direito de Família'
  family = SabDirKnowledgeAreaInfoer.get_or_create(area_str, civil)
  area_str = u'Direito das Sucessões'
  succession = SabDirKnowledgeAreaInfoer.get_or_create(area_str, civil)
  
  area_str = 'Direito Penal'
  penal = SabDirKnowledgeAreaInfoer.get_or_create(area_str, base_ka)
  SabDirKnowledgeAreaInfoer.print_all_kas()
  
  print(family.write_flat())
  print(succession.write_flat())
  print(penal.write_flat())

  relpath = 'Saber Direito TVJus/_a Direito Civil (videoaulas SabDir)/_a Direito de Família e Sucessório (videoaulas SabDir)/Direito da Criança e do Adolescente _i Enio Vieira Júnior'
  k_area = SabDirKnowledgeAreaInfoer.get_knowledge_area_by_relpath(relpath)
  print(relpath)
  print(k_area.write_flat())

  relpath = 'Saber Direito TVJus/_a Direito Civil (videoaulas SabDir)/_a Direito Contratual (videoaulas SabDir)/Teoria Geral dos Contratos _i Thiago Godoy'
  k_area = SabDirKnowledgeAreaInfoer.get_knowledge_area_by_relpath(relpath)
  print(relpath)
  print(k_area.write_flat())

  kas = SabDirKnowledgeAreaInfoer.get_kas_by_name('Direito Contratual')
  print('len(kas)', len(kas))
  for k_area in kas:
    print(k_area.write_flat())


if __name__ == '__main__':
  if 'ut' in sys.argv:
    sys.argv.remove('ut')
    unittests()  
  process()
