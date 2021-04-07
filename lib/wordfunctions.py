#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
This lib script contains functions with word utilities.
*** ALL functions have corresponding unit tests ***
'''

import string
BASE64CHAR = '_' + '-' + string.ascii_lowercase + string.ascii_uppercase + string.digits

lambdastripblanksinline = lambda line : line.strip(' \t\r')
def cleanup_lines_in_text_from_border_blanks(text):
  '''
  The functions receives a text and returns a filtered text,
    which filter acts line by line.

  Each line is stripped of the following characters:
  (The border blanks are:)
     1) the space character
     2) the tab character
     3) the \r (carriage return) character used in Windows
  :param text:
  :return:
  '''
  if text is None or text == '' or type(text) != str:
    return ''
  lines = text.split('\n')
  lines = list(map(lambdastripblanksinline, lines))
  newtext = '\n'.join(lines)
  newtext = newtext.strip('\n')
  return newtext

lambdaatleastonelower = lambda c : c in string.ascii_lowercase
def is_there_at_least_one_lowercase_letter(word):
  '''
  Returns False if at least one lowercase letter is missing in input word.
  :param word:
  :return:
  '''
  bool_list = list(map(lambdaatleastonelower, word))
  if True in bool_list:
    return True
  return False

lambdaatleastoneupper = lambda c : c in string.ascii_uppercase
def is_there_at_least_one_uppercase_letter(word):
  '''
  Returns False if at least one uppercase letter is missing in input word.
  :param word:
  :return:
  '''
  bool_list = list(map(lambdaatleastoneupper, word))
  if True in bool_list:
    return True
  return False

lambdatrueforallbase64chars = lambda c : c in BASE64CHAR
def is_word_a_base64(word):
  '''
  Returns True if all characters in input string word are BASE64.
  :param word:
  :return:
  '''
  bool_list = list(map(lambdatrueforallbase64chars, word))
  if False in bool_list:
    return False
  return True

def is_word_a_restricted_base64(word):
  '''
  A restricted base64 word has the following characteristics:
  1) it's a base64 word
  2) it has at least one lowercase letter
  3) it has at least one uppercase letter

  :param word:
  :return:
  '''
  if not is_word_a_base64(word):
    return False
  if not is_there_at_least_one_lowercase_letter(word):
    return False
  if not is_there_at_least_one_uppercase_letter(word):
    return False
  return True

def is_word_an_11char_restricted_base64(word):
  '''
  This functions verifies whether or not its input is an
    11-character restricted base64 word.

  Its main usage
  ==============

  Its main usage is to verify a youtube-id.
  A youtude-id is, in principle, a BASE64 11-character string.
  (See above how a BASE64 is formed in the concatenation for BASE64CHAR.)

  We have just added two statistical restrictions:
    1) it must have at least one lowercase letter
    2) it must have at least one uppercase letter

  :param word:
  :return:
  '''
  if len(word) != 11:
    return False
  return is_word_a_restricted_base64(word)


if __name__ == '__main__':
  pass
