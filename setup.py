#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from setuptools import setup, find_packages


VERSION = open('VERSION').read().lstrip('version: ').rstrip('\n')


setup(
    name='django-labjs',
    packages=find_packages(),
    version=VERSION,
    description='Django labjs templatetags.',
    long_description=open('README.rst').read(),
    author='Ashley Camba Garrido',
    author_email='stuffash@gmail.com',
    maintainer='Luke Pomfrey',
    maintainer_email='lpomfrey@gmail.com',
    url='https://github.com/lpomfrey/django-labjs',
    setup_requires=['setuptools_git >= 0.3'],
    install_requires=[
        'django-appconf>=0.4',
        'django-compressor>=0.9.2',
    ],
    test_suite='runtests.runtests',
    include_package_data=True,
    zip_safe=False,  # because we're including media that Django needs
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
