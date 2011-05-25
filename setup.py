#!/usr/bin/env python

from setuptools import setup
import memcache

setup(name="mcdict",
      version=mcdict.__version__,
      description="Enhance Python memcached client with a dictionary class",
      long_description=open("README").read(),
      author="Michael Dillon",
      author_email="martine@danga.com",
      maintainer="Michael Dillon",
      maintainer_email="memracom@yahoo.com",
      url="http://www.google.com",
      download_url="ftp://",
      py_modules=["mcdict"],
      classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Python Software Foundation License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ])

