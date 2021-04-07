import os

tlist = [
  'ab_bar.doc',
  'cd-bla.txt',
  'ef-foo.xls',
]


filter_filename_by_dot_extension_lambda = lambda f, dot_extension : f.endswith(dot_extension)
def filter_filenames_by_dot_extension_lambda(files, dot_extension):
  filtered_file_list = filter(filter_filename_by_dot_extension_lambda, files, dot_extension)
  return filtered_file_list


def filter_test(tlist, extgiven='doc'):
  exts = list(map(os.path.splitext, tlist))
  print(exts)
  newlist = list(filter(lambda f: f.endswith(extgiven), tlist))
  print(newlist)
  return newlist

def test():
  """:cvar
  newlist = filter_test(tlist)
  print(newlist)
  """
  newlist = filter_filenames_by_dot_extension_lambda(tlist, 'doc')
  print(newlist)

test()


