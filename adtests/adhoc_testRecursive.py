

class R:
  
  ROOT = None
  
  @staticmethod
  def get_kas_by_name_recursive(p_name, parent, p_kas=None):
    if p_kas is None:
      p_kas = []
    if p_name in parent.childrendict.keys():
      p_kas.append(parent.childrendict[p_name])
    for child in parent.childrendict.values():
      p_kas += R.get_kas_by_name_recursive(p_name, child, [])
    return p_kas

  @staticmethod
  def get_kas_by_name(p_name, parent=None, p_kas=None):
    if p_kas is None:
      p_kas = []
    if parent is None:
      parent = R.get_root()
    if p_name == parent.name:
      return [parent]  # ROOT should have a unique name, so look no further
    return R.get_kas_by_name_recursive(p_name, parent, p_kas)

  @staticmethod
  def get_root():
    if R.ROOT is None:
      R.ROOT = R('ROOT', None)
    return R.ROOT

  def __init__(self, name, parent):
    self.name = name
    self.childrendict = {}
    self.parent = parent
    if self.parent is not None:
      self.parent.add_child(self)
    
  def add_child(self, child):
    self.childrendict[child.name] = child
    
  def __str__(self):
    outstr = '|'
    outstr += '%s' % self.name
    if self.parent is not None and self.parent != R.get_root():
      outstr += str(self.parent)
    return outstr 


a1 = R('A1', R.get_root())
a11 = R('A11', a1)
a111 = R('A111', a11)
a2 = R('A2', R.get_root())
a21 = R('A21', a2)
az = R('A111', a21)
print('a111 =', a111)
print('a21 =', a21)
print('az =', az)
kas = R.get_kas_by_name('A111')
print('len(kas)', len(kas))
for ka in kas:
  print(ka)
