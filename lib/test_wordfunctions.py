#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
This lib script contains functions with word utilities.

'''

import unittest
import wordfunctions as wf

class TestCase(unittest.TestCase):

  def test_is_there_at_least_one_lowercase_letter(self):
    word = 'AAA'
    self.assertFalse(wf.is_there_at_least_one_lowercase_letter(word))
    word = 'AaA'
    self.assertTrue(wf.is_there_at_least_one_lowercase_letter(word))
    word = 'aaa'
    self.assertTrue(wf.is_there_at_least_one_lowercase_letter(word))
    word = 'aaaA'
    self.assertTrue(wf.is_there_at_least_one_lowercase_letter(word))

  def test_is_there_at_least_one_uppercase_letter(self):
    word = 'AAA'
    self.assertTrue(wf.is_there_at_least_one_uppercase_letter(word))
    word = 'AaA'
    self.assertTrue(wf.is_there_at_least_one_uppercase_letter(word))
    word = 'aaa'
    self.assertFalse(wf.is_there_at_least_one_uppercase_letter(word))
    word = 'aaaA'
    self.assertTrue(wf.is_there_at_least_one_uppercase_letter(word))

  def test_is_word_a_base64(self):
    word = '-_AAA12'
    self.assertTrue(wf.is_word_a_base64(word))
    word = 'AAA'
    self.assertTrue(wf.is_word_a_base64(word))
    word = '_-'
    self.assertTrue(wf.is_word_a_base64(word))
    word = 'aaaç'
    self.assertFalse(wf.is_word_a_base64(word))

  def test_is_word_a_restricted_base64(self):
    word = '-_AaA12'
    self.assertTrue(wf.is_word_a_restricted_base64(word))
    word = 'AaA'
    self.assertTrue(wf.is_word_a_restricted_base64(word))
    word = 'aaaç'
    self.assertFalse(wf.is_word_a_restricted_base64(word))
    word = 'aaaA54%&'
    self.assertFalse(wf.is_word_a_restricted_base64(word))

  def test_is_word_an_11char_restricted_base64(self):
    words = [
      'XVi9-ZAOaaY',
      'eiLuySR4ItI',
      'vUBCdnM1B1w',
      '1exkgrsJ5DA',
      'w0I1t1gXM7s',
      'C4nS9W_LzZY',
      '3NryZ-d65Gs',
    ]
    for word in words:
      self.assertTrue(wf.is_word_an_11char_restricted_base64(word))

    words = [
      'XVi9-ZAOaaYaaa',
      'eiLuyItI',
      'vUBCdnM1B1&',
      '"exkgrsJ5DA',
      '3413413w0I1t1gXM7s',
      'C4nS9WLzZY',
      '3NryZ+d65Gs',
    ]
    for word in words:
      self.assertFalse(wf.is_word_an_11char_restricted_base64(word))

  def test_cleanup_lines_in_text_from_border_blanks(self):
    text = ''
    self.assertEqual('', wf.cleanup_lines_in_text_from_border_blanks(text))
    text = None
    self.assertEqual('', wf.cleanup_lines_in_text_from_border_blanks(text))
    text = 123
    self.assertEqual('', wf.cleanup_lines_in_text_from_border_blanks(text))
    text = '''
          blah \t blah
    blahnew newblah
    \t okay kay\r
    '''
    expected_text = '''blah \t blah
blahnew newblah
okay kay'''
    self.assertEqual(expected_text, wf.cleanup_lines_in_text_from_border_blanks(text))
    expected_text = '''
blah \t blah
blahnew newblah
okay kay
'''
    self.assertNotEquals(expected_text, wf.cleanup_lines_in_text_from_border_blanks(text))


if __name__ == '__main__':
  pass
