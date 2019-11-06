""" exe_demo1.py"""
from distutils.core import setup
import py2exe
import sys

#this allows to run it with a simple double click.
sys.argv.append('py2exe')

options = {
    "py2exe": {
        "compressed": 1,
        "optimize": 2,
        "bundle_files": 1
    }
}

setup(
    version = "1.0.0",
    description = "Compute sum(100)",
    name = "py2exe demo",
    options = options,
    zipfile = None,
    console=["main.py"]
)