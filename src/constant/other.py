from numpy import dtype, int32
from collections import namedtuple



def _get_line_dtype() -> dtype:
  return dtype([('index', int32),('top', int32),('down', int32)])

def _get_fragment_dir_tuple() -> tuple:
  return namedtuple('couple', ['fr', 'to'])

def _get_dir_dictionary() -> dict:
  return {'left': 0, 'down':1, 'top': 2, 'right':3, 'scum':4, 'none':5}