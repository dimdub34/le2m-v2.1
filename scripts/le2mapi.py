#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Delete the content of the apidoc directory and create the new documentation
The command only works on linux
"""
import os

scriptdir = os.path.realpath(os.path.dirname(__file__))
appdir = os.path.realpath(os.path.dirname(scriptdir))

os.system("rm {}/*".format(os.path.join(appdir, "apidoc")))
os.system("epydoc {} --html -o {}".format(
    os.path.join(appdir, "le2m"), os.path.join(appdir, "apidoc")))