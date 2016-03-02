#coding: utf-8
#author zwei
#email suifeng20@hotmail.com
#data 2016/3/2

import sys
from loginserver import login
from loginserver.common import log as logging
from loginserver.common import cfg

CONF = cfg.CONF
LOG = logging.getLogger(__name__)

def main():
    argv = sys.argv()
    alias = argv[-1]
    LOG = logging.setup(*argv[:-1])
    lg = login.LoginServer()
    lg.login(alias)
