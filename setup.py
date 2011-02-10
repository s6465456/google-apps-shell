#!/usr/bin/python
# usage: python setup.py py2exe
#    or  python setup.py py2app

from setuptools import setup
import sys

MAIN_SCRIPT  = "gasi.py"

if sys.platform in ("win32", "win64"): # does win64 exist?
    import py2exe
    setup(windows=[{ "script":MAIN_SCRIPT}])
elif sys.platform == "darwin":
    import py2app
    setup(app=[MAIN_SCRIPT], setup_requires=["py2app"]) # doesn't include the icon yet
