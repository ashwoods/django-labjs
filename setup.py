#!/usr/bin/env python
from setuptools import setup, find_packages

VERSION = open('VERSION').read().lstrip('version: ').rstrip('\n')


setup(name='django-labjs',
      version = VERSION,
      packages=find_packages(),
      exclude_package_data={'labjs': ['bin/*.pyc']},
      setup_requires = ["setuptools_git >= 0.3",],
      install_requires = [
        'django-appconf >= 0.4',
        'django-compressor >= 0.9.2',
        ],

      )
