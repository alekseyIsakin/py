import logging as lg

def initLogger(lvl=lg.INFO):
  lg.basicConfig(format='[%(asctime)s][%(filename)s][%(levelname)s] %(message)s', level=lvl)