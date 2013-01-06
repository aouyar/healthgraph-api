#!/usr/bin/env python
"""healthgraph-api Setup Script

"""

import os
from setuptools import setup, find_packages
import healthgraph

def read_file(filename):
    """Read a file into a string"""
    path = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(path, filename)
    try:
        return open(filepath).read()
    except IOError:
        return ''


setup(
    name='healthgraph',
    description=u'Python Client for HealthGraph API from RunKeeper.com.',
    long_description=read_file('README.markdown'),
    keywords=['Health', 'Graph', 'API', 'RunKeeper'],
    version=healthgraph.__version__,
    author=healthgraph.__author__,
    author_email=healthgraph.__email__,
    mantainer=healthgraph.__author__,
    mantainer_email=healthgraph.__email__,
    include_package_data=True,
    url='http://aouyar.github.com/healthgraph-api',
    license=healthgraph.__license__,
    classifiers=[
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python',
        'Development Status :: 3 - Alpha',
        'Operating System :: OS Independent',
    ],
    packages=find_packages(),
    install_requires=["requests",],
)
