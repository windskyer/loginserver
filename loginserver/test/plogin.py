#!/usr/bin/env python
#coding: utf-8
#author leidong


import pexpect
import os
import getpass
from pexpect import spawn
from pexpect import ExceptionPexpect 
from pexpect import EOF
from pexpect import TIMEOUT

class ConnSsh(spawn):
    """Connection  ssh service"""
    
    def __init__ (self, timeout=30, maxread=200000, searchwindowsize=None, logfile=None, cwd=None, env=None):
        super(ConnSsh, self).__init__(None, timeout=timeout, maxread=maxread, searchwindowsize=searchwindowsize, logfile=logfile, cwd=cwd, env=env)

        self.name = '<connssh>'

         # used to match the command-line prompt
        self.UNIQUE_PROMPT = "\[PEXPECT\][\$\#] "
        self.PROMPT = self.UNIQUE_PROMPT

        # used to set shell command-line prompt to UNIQUE_PROMPT.
        self.PROMPT_SET_SH = "PS1='[PEXPECT]\$ '"
        self.PROMPT_SET_CSH = "set prompt='[PEXPECT]\$ '"
        self.SSH_OPTS = ("-o'RSAAuthentication=no'"
                + " -o 'PubkeyAuthentication=no'")

        self.force_password = False
        self.auto_prompt_reset = True
        self.login_timeout = timeout


    def _login(self, cmd):
        # set windows size 
        self._spawn(cmd)
        
        # First phase
        i = self.expect(["(?i)are you sure you want to continue connecting", self.original_prompt, "(?i)(?:password)|(?:passphrase for key)", "(?i)permission denied", "(?i)terminal type", TIMEOUT, "(?i)connection closed by remote host"], timeout=self.login_timeout)
        if i==0:
            self.sendline('yes')
            i = self.expect(["(?i)are you sure you want to continue connecting", self.original_prompt, "(?i)(?:password)|(?:passphrase for key)", "(?i)permission denied", "(?i)terminal type", TIMEOUT])
        if i==2:
            self.sendline(self.password)
            i = self.expect(["(?i)are you sure you want to continue connecting", self.original_prompt, "(?i)(?:password)|(?:passphrase for key)", "(?i)permission denied", "(?i)terminal type", TIMEOUT])
        if i==4:
            self.sendline(self.terminal_type)
            i = self.expect(["(?i)are you sure you want to continue connecting", self.original_prompt, "(?i)(?:password)|(?:passphrase for key)", "(?i)permission denied", "(?i)terminal type", TIMEOUT])
 
        # Second phase 
        if i==0:
            self.close()
            raise ExceptionPexpect ('Weird error. Got "are you sure" prompt twice.')
        elif i==1:
            #print str(self.getwinsize())
            self.setwinsize(200,132)
            #print str(self.getwinsize())
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

    def login (self,server,username=None,password=None,terminal_type='ansi',original_prompt=r"[#$]",login_timeout=10,port=None,auto_prompt_reset=True,ssh_key=None,quiet=True,sync_multiplier=1,check_local_ip=True):

        ssh_options  = ''
        if quiet:
            ssh_options = ssh_options + '-q'

        if not check_local_ip:
            ssh_options = ssh_options + " -o'NoHostAuthenticationForLocalhost=yes'"

        if self.force_password:
            ssh_options = ssh_options + ' ' + self.SSH_OPTS
        if port is not None:
            ssh_options = ssh_options + ' -p %s'%(str(port))
        if ssh_key is not None:
            try:
                os.path.isfile(ssh_key)
            except:
                raise ExceptionPexpect ('private ssh key does not exist')
            ssh_options = ssh_options + ' -i %s' % (ssh_key)

        if server is None:
            raise ExceptionPexpect ('Not Found ssh Server')

        if username is None:
            username = 'root'
        if password is None:
            password = getpass.getpass()
        cmd = "ssh %s -l %s %s" % (ssh_options, username, server)
        self.original_prompt = original_prompt
        self.login_timeout = login_timeout
        self.password = password
        self.terminal_type = terminal_type
        print str(cmd)
        return self._login(cmd)


if __name__ == '__main__':
    cs = ConnSsh() 
    cs.login('192.168.122.182','root','toor')
