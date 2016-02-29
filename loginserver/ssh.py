#!/usr/bin/env python 

import sys
import json
import tty
import termios

import paramiko
from paramiko import PasswordRequiredException
from paramiko.dsskey import DSSKey
from paramiko.rsakey import RSAKey
from paramiko.ssh_exception import SSHException

import eventlet
from eventlet import event 
from eventlet import greenpool
from eventlet import greenthread

class LoginServer(object):
    def __init__(self):
        self._ssh = paramiko.SSHClient()
        self._ssh.set_missing_host_key_policy(
                        paramiko.AutoAddPolicy())

        self.pool = eventlet.GreenPool()
        self.done = event.Event()
        self._task = []

    def open(self,
             hostname=None, 
             port=22,
             username='root',
             password='toor'):
        self._connect = self._ssh.connect(hostname,
                                          port,
                                          username,
                                          password)
    def close(self):
        """ Terminate a bridge session """
        #gevent.killall(self._tasks, block=True)
        self._tasks = []
        self._ssh.close()

    def output(self, data):
        sys.stdout.writelines(data)
        sys.stdout.flush()

    def outbound(self, channel):
        try:
            while True:
                #wait_read(channel.fileno())
                data = channel.recv(10240)
                #if not len(data) or str(data).startswith('\n'):
                if not len(data):
                    return
                #self._websocket.send(json.dumps({'data': data}))
                self.output(data)
                greenthread.sleep(0.1)

        finally:
            self.close()

    def input(self, buffer=None):
        if buffer is None:
            buffer = 1024
        data = sys.stdin.readline(buffer)
        return {'data' : data}

    def inbound(self, channel):
        new = termios.tcgetattr(self.fd)
        new[3] = new[3] & ~termios.ECHO 
        termios.tcsetattr(self.fd, termios.TCSADRAIN, new)
        try:
            while True:
                #wait_write(channel.fileno())
                #data = self._websocket.receive()
                data = self.input()
                print data
                if not data:
                    return 
                #data = json.loads(str(data))
                if 'resize' in data:
                    channel.resize_pty(
                        data['resize'].get('width', 132),
                        data['resize'].get('height', 43))
                if 'data' in data:
                    channel.send(data['data'])
                greenthread.sleep(0.1)
        finally:
            self.close()

    def execute(self):
        pass

    def _pty_size(self, raws, cows):
        pass
    def _shell(self, channel):
        channel.setblocking(1)
        channel.settimeout(1.0)
        self.fd = sys.stdin.fileno()
        old = termios.tcgetattr(self.fd)
        #print new
        #tty.setraw(sys.stdin.fileno())
        #tty.setcbreak(sys.stdin.fileno())

        self._task = [
            self.pool.spawn(self.outbound, channel),
            self.pool.spawn(self.inbound, channel),
        ]
        self.pool.waitall()
        termios.tcsetattr(self.fd, termios.TCSADRAIN, old)

    def shell(self, term='xterm'):
        channel = self._ssh.invoke_shell(term)
        self._shell(channel)
        channel.close()

if __name__ == '__main__':
    login = LoginServer()
    login.open('192.168.122.1', username='love',  password='flf1007828039@')
    login.shell()
