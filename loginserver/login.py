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

def key_file(key_name="id_rsa"):
    pass

class LoginServer(spawn):
    USERNAME = "root"
    PASSWORD = "toor"
    IS_KEY = False
    PORT = "22" 

    def __init__(self, timeout=30, maxread=20000):
        self.ssh_options = []
        self.timeout = CONF.timeout or timeout
        self.maxread = CONF.maxread or maxread
        self._set_ssh_options

    @property
    def _set_ssh_options(self)
        self.port = CONF.port or self.PORT
        quiet = CONF.quiet or True
        check_local_ip = CONF.check_local_ip or False
        force_password = CONF.force_password or False

        if quiet:
            self.ssh_options.append(" -q")
        if not check_local_ip:
            self.ssh_options.append(" -o 'NoHostAuthenticationForLocalhost=yes'")
        if not force_password:
            self.ssh_options.append("-o 'RSAAuthentication=no' -o 'PubkeyAuthentication=no'")

    def _open(self, alias=None):
        if alias is None or alias not in CONF.groups:
            raise exception.NotFoundHost(host=hostname)

        self.port = CONF[alias].port or self.port
        self.hostname = CONF[alias].hostname

        self.username = CONF[alias].username or self.USERNAME
        self.password = CONF[alias].password or self.PASSWORD

        self.is_key = CONF[alias].IS_KEY or self.IS_KEY

        self.key_name = CONF.[alias].key_name or CONF.key_name

        self.key_file = key_file(self.key_name)

        if self.is_key:
            self.ssh_options.append(" -i %s" % self.key_file)

        self.ssh_options.append(" -p %s" % self.port)
                        
        if self.hostname:
            self.ssh_options.append(" -i %s" % self.key_file)

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

    @property
    def _resize(self):
        rows, cols = self._pty_size()
        return {'resize': {'width': cols, 'height': rows}}

    def login(self):
        pass
