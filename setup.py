
from setuptools import setup

import sys
import xmlrpclibex


setup(
    name                = xmlrpclibex.__title__,
    version             = xmlrpclibex.__version__,
    description         = xmlrpclibex.__summary__,
    license             = xmlrpclibex.__license__,
    url                 = xmlrpclibex.__url__,
    author              = xmlrpclibex.__author__,
    author_email        = xmlrpclibex.__email__,
    long_description    = open('README.rst').read(),

    packages = ['xmlrpclibex'],

    keywords = 'xmlrpc proxy',

    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: BSD",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        'Topic :: Communications',
    ],

    install_requires = ['PySocks'],
)

