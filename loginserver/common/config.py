#coding: utf-8
#author zwei
#email suifeng20@hotmail.com

import os
import sys

def find_config_file(pdir=None, pfile=None):
    confdir = os.path.expanduser('~')    
    binfile = sys. 
    pdir = pdir or confdir
    if os.path.exits(pdir):
        os.mkdir(pdir, mode=0755)
    if pfile is None:
        pfile = os.path.join(confdir, binfile)
