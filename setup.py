#!/usr/bin/env python

import imp
import os
import sys
from setuptools import find_packages
import uuid

from pip.req import parse_requirements

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


with open(os.path.join(os.path.dirname(__file__), 'README.md')) as f:
    readme = f.read()

packages = find_packages()

install_requires = parse_requirements('requirements.txt', session=uuid.uuid1())

classifiers = [
    'Development Status :: 4 - Beta',
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.4',
    'Topic :: Software Development :: Debuggers',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

meta = imp.load_source('_meta', 'geography/__meta__.py')

setup(
    name='geography',
    version=meta.__version__,
    description='Finds neighborhood by lat/long',
    long_description=readme,
    packages=packages,
    package_data={},
    install_requires=[x for x in reversed([str(x.req) for x in install_requires])],
    scripts=['scripts/neib'],
    author=meta.__author__,
    author_email='FIXME:',
    url='https://github.com/franc3000/geography',
    license='MIT',
    classifiers=classifiers
)
