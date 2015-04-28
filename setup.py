#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
    
setup(name='md2web',
      version='0.1',
      description='Simple website generator',
      author='Eric Thrift',
      author_email='ericdthrift@mcdrc.org',
      url='http://mcdrc.org/code/md2web/',
      scripts=['md2web'],
      install_requires=['docopt']
     )
