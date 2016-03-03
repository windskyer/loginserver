#coding: utf-8
#author zwei
#email suifeng20@hotmail.com
#data 2016/3/2

import os
import sys
from loginserver import login
from loginserver.common import cfg
from loginserver.common import log as logging

CONF = cfg.CONF
LOG = logging.getLogger(__name__)

def set_env():
    possible_topdir = os.path.normpath(os.path.join(os.path.abspath(__file__),
                                                os.pardir,
                                                os.pardir,
                                                os.pardir))
    if os.path.exists(os.path.join(possible_topdir,
                               "loginserver",
                               "__init__.py")):
        sys.path.insert(0, possible_topdir)

    dev_conf = os.path.join(possible_topdir,
                            'etc',
                            'loginserver.conf')
    if os.path.exists(dev_conf):
        CONF(dev_conf)
    else:
        CONF()
    #LOG = logging.setup(*argv[:-1])

def main():
    argv = sys.argv
    if len(argv) < 2:
        sys.exit(1)
    alias = argv[-1]
    set_env()
    login.main(alias)

if __name__ == '__main__':
    main()
