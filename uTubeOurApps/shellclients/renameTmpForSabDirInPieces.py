#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
'''
import codecs, os, sys


lines ='''Lei Maria da Penha _ Sérgio Ricardo de Souza _Aula 1 Marcos Normativos
Lei Maria da Penha _ Sérgio Ricardo de Souza _Aula 2 Aspectos Polêmicos'''

TOTAL_PARTES = 6

def process():
  line_list = lines.split('\n')
  for line in line_list:
    for n_parte in range(1, TOTAL_PARTES + 1):
      print line + ' _p%d ;' %n_parte

if __name__ == '__main__':
  process()
