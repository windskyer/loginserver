#coding: utf-8
#author zwei
#email suifeng20@hotmail.com
#data 2016/3/2

import sys
from loginserver import login
from loginserver.common import cfg
from loginserver.common import log as logging

CONF = cfg.CONF
LOG = logging.getLogger(__name__)

def main():
    argv = sys.argv
    CONF()
    alias = argv[-1]
    #LOG = logging.setup(*argv[:-1])
    login.main(alias)

if __name__ == '__main__':
    main()
