#!/usr/bin/env python
# coding: utf-8
version = (0, 2, 1, 'dev1')

import os
import sys
from glob import glob
from distutils.command.sdist import sdist
from setuptools import setup, Extension

try:
    from Cython.Distutils import build_ext
    import Cython.Compiler.Main as cython_compiler
    have_cython = True
except ImportError:
    from distutils.command.build_ext import build_ext
    have_cython = False

# make msgpack/__verison__.py
f = open('msgpack/__version__.py', 'w')
f.write("version = %r\n" % (version,))
f.close()
del f

version_str = '.'.join(str(x) for x in version[:3])
if len(version) > 3 and version[3] != 'final':
    version_str += version[3]

# take care of extension modules.
if have_cython:
    sources = ['msgpack/_msgpack.pyx']

    class Sdist(sdist):
        def __init__(self, *args, **kwargs):
            for src in glob('msgpack/*.pyx'):
                cython_compiler.compile(glob('msgpack/*.pyx'),
                                        cython_compiler.default_options)
            sdist.__init__(self, *args, **kwargs)
else:
    sources = ['msgpack/_msgpack.cpp']

    for f in sources:
        if not os.path.exists(f):
            raise ImportError("Building msgpack from VCS needs Cython. Install Cython or use sdist package.")

    Sdist = sdist

libraries = []
if sys.platform == 'win32':
    libraries.append('ws2_32')

msgpack_mod = Extension('msgpack._msgpack',
                        sources=sources,
                        libraries=libraries,
                        include_dirs=['.'],
                        language='c++',
                        )
del sources, libraries


desc = 'MessagePack (de)serializer.'
f = open('README.rst')
long_desc = f.read()
f.close()
del f

setup(name='msgpack-python',
      author='INADA Naoki',
      author_email='songofacandy@gmail.com',
      version=version_str,
      cmdclass={'build_ext': build_ext, 'sdist': Sdist},
      ext_modules=[msgpack_mod],
      packages=['msgpack'],
      description=desc,
      long_description=long_desc,
      url='http://msgpack.org/',
      download_url='http://pypi.python.org/pypi/msgpack/',
      classifiers=[
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Apache Software License',
          ]
      )
