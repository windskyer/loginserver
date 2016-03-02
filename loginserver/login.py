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
from loginserver import excption
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

    def _set_cmd(self, alias=None):
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

        if self.username:
            self.ssh_options.append(" -l %s" % self.username)

        self.ssh_options.append(" -p %s" % self.port)
        self.ssh_options.append(self.hostname)
        return ' '.join(self.ssh_options)

    def _set_terminal(self):


        pass
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
        return (rows, cols)

    def first_phase(self,cmd):
        # First phase
        i = self.expect(["(?i)are you sure you want to continue connecting", self.original_prompt, "(?i)(?:password)|(?:passphrase for key)", "(?i)permission denied", "(?i)terminal type", TIMEOUT, "(?i)connection closed by remote host"], timeout=self.login_timeout)
        if i==0:
            self.sendline('yes')
            i = self.expect(["(?i)are you sure you want to continue connecting", self.original_prompt, "(?i)(?:password)|(?:passphrase for key)", "(?i)permission denied", "(?i)terminal type", TIMEOUT])
        elif i==2:
            self.sendline(self.password)
            i = self.expect(["(?i)are you sure you want to continue connecting", self.original_prompt, "(?i)(?:password)|(?:passphrase for key)", "(?i)permission denied", "(?i)terminal type", TIMEOUT])
        elif i==4:
            self.sendline(self.terminal_type)
            i = self.expect(["(?i)are you sure you want to continue connecting", self.original_prompt, "(?i)(?:password)|(?:passphrase for key)", "(?i)permission denied", "(?i)terminal type", TIMEOUT])
        else:
            raise 
        return i

    def second_phase(self, i):
          # Second phase 
        if i==0:
            self.close()
            raise ExceptionPexpect ('Weird error. Got "are you sure" prompt twice.')
        elif i==1:
            self.setwinsize(*self._resize)
            self.sendline('clear')
            self.interact()
        elif i==2:
            self.close()
            raise ExceptionPexpect ('password refused')
        elif i==3:
            self.close()
            raise ExceptionPexpect ('permission denied')
        elif i==4:
            self.close()
            raise ExceptionPexpect ('Weird error. Got "are you sure" prompt twice.')
        elif i==5:
            self.close()
            raise ExceptionPexpect ('timeout')
        elif i==6:
            self.close()
            raise ExceptionPexpect ('connection closed')
        else:
            self.close()

        return i

    def login(self, alias):
        cmd = self._open(alias)
        self._spawn(cmd)

