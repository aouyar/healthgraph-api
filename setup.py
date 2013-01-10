#!/usr/bin/env python
"""healthgraph-api Setup Script

"""

import os
from setuptools import setup

__author__ = "Ali Onur Uyar"
__copyright__ = "Copyright 2012, Ali Onur Uyar"
__credits__ = []
__license__ = "GPL"
__version__ = "0.2.1"
__email__ = "aouyar at gmail.com"
__status__ = "Development"


def read_file(filename):
    """Read a file into a string"""
    path = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(path, filename)
    try:
        return open(filepath).read()
    except IOError:
        return ''


setup(
    name='healthgraph-api',
    description=u'Python Client for HealthGraph API from RunKeeper.com.',
    keywords=['Health', 'Graph', 'API', 'RunKeeper'],
    version=__version__,
    author=__author__,
    author_email=__email__,
    maintainer=__author__,
    maintainer_email=__email__,
    include_package_data=True,
    url='http://aouyar.github.com/healthgraph-api',
    license=__license__,
    classifiers=[
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python',
        'Development Status :: 3 - Alpha',
        'Operating System :: OS Independent',
    ],
    packages=['healthgraph',],
    long_description=read_file('README.md'),
    install_requires=["requests",],
)
