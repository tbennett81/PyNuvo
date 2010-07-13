from distutils.core import setup
from glob import glob
import py2exe

data_files = [("Microsoft.VC90.CRT", glob(r'c:\dev\ms-vc-runtime\*.*'))]

setup(data_files = data_files, console=['WinService.py'])