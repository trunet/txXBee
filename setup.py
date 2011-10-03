#!/usr/bin/env python
"""
txXBee installation script
"""
from setuptools import setup
import os
import sys
import subprocess
import txXBee

setup(
    name = "txXBee",
    version = txXBee.__version__,
    author = "Wagner Sartori Junior",
    author_email = "wsartori@gmail.com",
    url = "http://github.com/trunet/txxbee",
    description = "XBee Protocol for Twisted",
    scripts = [],
    license="COPYING",
    packages = ["txXBee"],
    install_requires = ['XBee'],
    long_description = """XBee os an easy-to-implement embedded short- and long-range wireless modules leveraging industry standard and cutting-edge designs for global flexibility from http://www.digi.com/.

This library implements txXBee for the Twisted Python framework.
  """,
    classifiers = [
        "Framework :: Twisted",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        "Topic :: Communications",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities"
        ]
    )

