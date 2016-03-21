# author: zwei
# email: suifeng20@hotmail.com
# date:  2016/2/29

""" Log in to the specified server from config file"""

import os
import sys
import fcntl
import signal
import struct
import getpass
import termios
import pexpect
import platform

from six import moves
from pexpect import spawn
from pexpect import EOF
from pexpect import TIMEOUT


from loginserver import exception
from loginserver.common import cfg
from loginserver.common import log as logging
from loginserver.exception import ExceptionPexpect

CONF = cfg.CONF


def key_file(key_name="id_rsa"):
    key_file = os.path.expanduser('~/.ssh/') + key_name
    if not os.path.isfile(key_file):
        raise exception.NotFoundPKey(pkey=key_file)
    return key_file


class LoginServer(spawn):
    USERNAME = "root"
    PASSWORD = "toor"
    IS_KEY = False
    PORT = "22"
    KEY_FILE = "id_rsa"
    RECONNECT = 3

    def __init__(self, command=None, timeout=30, maxread=20000):
        super(LoginServer, self).__init__(command, timeout, maxread)
        self.ssh_options = []
        self.name = '<loginserver>'
        self.timeout = int(CONF.timeout) if CONF.timeout else timeout
        self.maxread = int(CONF.maxread) if CONF.maxread else maxread
        self.reconnect = (int(CONF.reconnect)
                          if CONF.reconnect else self.RECONNECT)
        # used to match the command-line prompt
        self.UNIQUE_PROMPT = "\[PEXPECT\][\$\#] "
        self.PROMPT = self.UNIQUE_PROMPT

        # used to set shell command-line prompt to UNIQUE_PROMPT.
        self.PROMPT_SET_SH = "PS1='[PEXPECT]\$ '"
        self.PROMPT_SET_CSH = "set prompt='[PEXPECT]\$ '"
        self._set_ssh_options
        self.connect = 0

    @property
    def _set_ssh_options(self):
        self.port = CONF.port or self.PORT
        quiet = CONF.quiet or True
        check_local_ip = CONF.check_local_ip or False
        force_password = CONF.force_password or False

        if quiet:
            self.ssh_options.append(" -q")
        if not check_local_ip:
            self.ssh_options.append(" -o "
                                    "'NoHostAuthenticationForLocalhost=yes'")
        if not force_password and not CONF.is_key:
            self.ssh_options.append("-o 'RSAAuthentication=no' "
                                    "-o 'PubkeyAuthentication=no'")

    def _set_cmd(self, alias=None):
        if alias is None or alias not in CONF.groups:
            raise exception.NotFoundHost(host=alias)

        self.hostname = CONF[alias].ip or CONF[alias].hostname
        if self.hostname is None:
            raise exception.NotFoundHostIp(alias=alias, ip=self.hostname)

        self.port = CONF[alias].port or self.port
        self.username = CONF[alias].username or CONF.username or self.USERNAME
        self.password = CONF[alias].password or CONF.password or self.PASSWORD

        self.is_key = CONF[alias].is_key or self.IS_KEY

        if self.is_key:
            self.key_name = CONF[alias].key_file or \
                            CONF.key_file or \
                            self.KEY_FILE
            self.key_file = key_file(self.key_name)
            self.ssh_options.append(" -i %s" % self.key_file)

        if self.username:
            self.ssh_options.append(" -l %s" % self.username)

        self.ssh_options.append(" -p %s" % self.port)
        self.ssh_options.append(self.hostname)
        return ' '.join(list(moves.filter(bool, self.ssh_options)))

    @property
    def _set_terminal(self):
        self.terminal_type = 'ansi'
        self.original_prompt = r"[#$]"
        self.login_timeout = self.timeout or 30

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

    @property
    def first_phase(self):
        """ First phase"""
        self._spawn(self.cmd)
        i = self.expect(["(?i)are you sure you want to continue connecting",
                         self.original_prompt,
                         "(?i)(?:password)|(?:passphrase for key)",
                         "(?i)permission denied",
                         "(?i)terminal type",
                         TIMEOUT,
                         "(?i)connection closed by remote host"],
                        timeout=self.login_timeout)
        if i == 0:
            self.sendline('yes')
            i = self.expect(["(?i)are you sure you want to "
                             "continue connecting",
                             self.original_prompt,
                             "(?i)(?:password)|(?:passphrase for key)",
                             "(?i)permission denied",
                             "(?i)terminal type",
                             TIMEOUT])
        elif i == 2:
            self.sendline(self.password)
            i = self.expect(["(?i)are you sure you want to "
                             "continue connecting",
                             self.original_prompt,
                             "(?i)(?:password)|(?:passphrase for key)",
                             "(?i)permission denied",
                             "(?i)terminal type",
                             TIMEOUT])
        elif i == 4:
            self.sendline(self.terminal_type)
            i = self.expect(["(?i)are you sure you want to "
                             "continue connecting",
                             self.original_prompt,
                             "(?i)(?:password)|(?:passphrase for key)",
                             "(?i)permission denied",
                             "(?i)terminal type",
                             TIMEOUT])
        elif i != 1:
            raise ExceptionPexpect("Can't capture the "
                                   "right information ")
        return i

    @property
    def input_passwd(self):
        self.connect += 1
        msg = "Login %(host)s" % dict(host=self.hostname)
        self.password = getpass.getpass("%s, Enter password: " % msg)
        self.second_phase(self.first_phase)

    def second_phase(self, i):
        """Second phase """
        if i == 0:
            self.close()
            raise ExceptionPexpect('Weird error. '
                                   'Got "are you sure" prompt twice.')
        elif i == 1:
            self.setwinsize(*self._resize)
            self.sendline('clear')
            self.interact()
        elif i == 2:
            if self.connect < self.reconnect:
                self.kill(signal.SIGTERM)
                self.close()
                self.pid = None
                self.input_passwd
                # LOG.warn('this password waring')
                return
            self.close()
            raise ExceptionPexpect('password refused')
        elif i == 3:
            self.close()
            raise ExceptionPexpect('permission denied')
        elif i == 4:
            self.close()
            raise ExceptionPexpect('Weird error. '
                                   'Got "are you sure" prompt twice.')
        elif i == 5:
            self.close()
            raise ExceptionPexpect('timeout')
        elif i == 6:
            self.close()
            raise ExceptionPexpect('connection closed')
        else:
            self.close()
        return i

    def login(self, alias):
        self._set_terminal
        self.cmd = "ssh " + "".join(self._set_cmd(alias))
        self.second_phase(self.first_phase)


def main(alias):
    lg = LoginServer()
    lg.login(alias)


if __name__ == '__main__':
    CONF()
    main("test123")
