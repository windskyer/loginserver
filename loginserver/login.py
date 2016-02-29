#author: zwei
#email: suifeng20@hotmail.com
#date:  2016/2/29

""" Log in to the specified server from config file"""

from loginserver.common import cfg
CONF = cfg.CONF

class LoginServer(object):
    USERNAME = "root"
    PASSWORD = "toor"
    IS_KEY = False

