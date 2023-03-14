import cppyy

from os import listdir
from os.path import join

class Connector:

	def __init__(self):
		for file in (listdir('cxx')):
			if file.endswith('.cxx'):
				cppyy.include(join('cxx', file))

	def __getattr__(self, name:str):
		return getattr(cppyy.gbl, name)