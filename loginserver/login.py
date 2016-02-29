#author: zwei
#email: suifeng20@hotmail.com
#date:  2016/2/29

""" Log in to the specified server from config file"""

import fcntl
import struct
import platform
import pexpect
from pexpect import spawn

from loginserver.common import cfg
from loginserver.common import excption
CONF = cfg.CONF

class LoginServer(spawn):
    USERNAME = "root"
    PASSWORD = "toor"
    IS_KEY = False

    def __init__(self):
        pass
    def _open(self, hostname=None):
        if hostname is None or hostname not in CONF.groups:
            raise exception.NotFoundHost(host=hostname)

        self.hostname = CONF[hostname].hostname
        self.username = CONF[hostname].username or self.USERNAME
        self.password = CONF[hostname].password or self.PASSWORD
        self.is_key = CONF[self.hostname].IS_KEY or self.IS_KEY

    def _pty_size(self, rows=24, cols=80):
        # Can't do much for Windows
        if platform.system() == 'Windows':
            return rows, cols
        fmt = 'HH'
        buffer = struct.pack(fmt, 0, 0)
        result = fcntl.ioctl(sys.stdout.fileno(), 
                             termios.TIOCGWINSZ,
                             buffer)
        rows, cols = struct.unpack(fmt, result)
        return rows, cols

    def _resize(self):
        rows, cols = self._pty_size()
        return {'resize': {'width': cols, 'height': rows}}

