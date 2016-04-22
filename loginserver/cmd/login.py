# coding: utf-8
# author zwei
# email suifeng20@hotmail.com
# data 2016/3/2

from __future__ import print_function

import os
import sys
from loginserver import login
from loginserver.login import Login
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
    # LOG = logging.setup(*argv[:-1])


def help_info():
    print("\n" + " " * 15 + "Print available aliase")
    for alias in Login.all_alias():
        print("alias %-8s " % alias, end='')
        print("-" * 10 + ">   ", end='')
        print("hostname or ip %2s" % Login.get_hostname(alias))
    sys.exit(1)


def not_in_alias(alias=None):
    if alias not in Login.all_alias():
        help_info()
    return alias


def main():
    argv = sys.argv
    set_env()
    if len(argv) < 2:
        help_info()
    alias = argv[-1]
    login.main(not_in_alias(alias))

if __name__ == '__main__':
    main()
