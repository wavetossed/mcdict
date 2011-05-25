#!/usr/bin/env python

from setuptools import setup
import memcache
import mcdict

setup(name="mcdict",
      version=mcdict.__version__,
      description="Enhance Python memcached client with a dictionary class",
      long_description=open("README.md").read(),
      author="Michael Dillon",
      author_email="wavetossed@gmail.com",
      maintainer="Michael Dillon",
      maintainer_email="wavetossed@gmail.com",
      url="https://github.com/wavetossed/mcdict",
      download_url="https://github.com/wavetossed/mcdict/tarball/master",
      py_modules=["mcdict"],
      classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Topic :: Database :: Front-Ends",
        "Topic :: System :: Distributed Computing",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ])

