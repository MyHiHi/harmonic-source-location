import sys,os
from sys import path
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)
path.append(BASE_DIR);
from util import *;
p=util.Util();