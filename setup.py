#!/usr/bin/env python
from setuptools import setup, find_packages


VERSION = open('VERSION').read().lstrip('version: ').rstrip('\n')


setup(name='django-labjs',
        packages=find_packages(),

        version='0.1.1-dev',
        description='Django labjs templatetags.',
        long_description=open('README.rst').read(),
        author='Ashley Camba Garrido',
        author_email='stuffash@gmail.com',
        url='https://github.com/ashwoods/django-labjs',

        setup_requires = ["setuptools_git >= 0.3",],
        install_requires = [
            'django-appconf >= 0.4',
            'django-compressor >= 0.9.2',
        ],
        include_package_data=True,
        zip_safe=False, # because we're including media that Django needs
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
