#!/usr/bin/env python 
#coding: utf-8

#author zwei
#email zwei@hotmail.com
#date 20150331

import os, sys
import subprocess

## configure
from ConfigParser import ConfigParser
from ConfigParser import re

## ssh 
import paramiko
from paramiko import PasswordRequiredException
from paramiko.dsskey import DSSKey
from paramiko.rsakey import RSAKey
from paramiko.ssh_exception import SSHException


FILE_DIR = os.getcwd()
FILE_DIR = os.path.dirname(sys.argv[:1][0])
FILE_NAME = "loginfile.sh "
FILE = os.path.join(FILE_DIR , FILE_NAME)
CONF_FILE = "%s/.ssh/auth_login" % os.environ.get('HOME')

if os.path.isfile(CONF_FILE):
    print CONF_FILE


## return dict type
## read ssh config file
def read_conf(conf=None,name=None):
    returndict = {}
    servernamelist = []
    cf = ConfigParser()
    if conf is None:
        print "Not Found ~/.ssh/auth_login file"
        sys.exit(2)

    cf.read(conf)

    if cf.has_section('ssh_server'):
        if cf.has_option('ssh_server','ssh_server_alias'):
            servernames = cf.get('ssh_server', 'ssh_server_alias')
        else:
            print "Not Found ~/.ssh/auth_login in ssh_server_alias option  file"
            sys.exit(2)
    else:
        print "Not Found ~/.ssh/auth_login in ssh_server section file"
        sys.exit(2)

    servernamelist = re.split("\,|\#|\?|\|", servernames)

    if name is not None:
        if name in servernamelist:
            if cf.has_section(name):
                vmlist = cf.items(name)
                vmdict = {}
                for vm in vmlist:
                    vmdict[vm[0]] = vm[1]

                returndict[name] = vmdict 
            else:
                print "Not Found ~/.ssh/auth_login in %s section  file" % name
                sys.exit(3)
        else:
            for k in servernamelist:
                print "\tplease input\t'%s'" % k
            print "Not Found ~/.ssh/auth_login in %s section  file" % name
            sys.exit(3)
    else:
        print "please input ssh server name eg:"
        for k in servernamelist:
            print "\tplease input\t'%s'" % k
        sys.exit(3)
    
    return returndict
                

def login_server(servername,serverdict,loginfile):

    if os.path.isfile(loginfile) == "False":
        print "this is %s is Not Found !" % loginfile
        return 0
    if servername is None:
        print "this is %s is None !" % servername 
        return 0

    #获取ip 通过 server name
    #vips = SERVERS.get(servername)
    values = serverdict.get(servername)
    
    vip = values.get('ip')
    passwd = values.get('user_passwd')
    user = values.get('user_name')
    is_key = values.get('is_key')
    port = values.get('port')

    #for vip in vips:
    try:
        print "login server %s  host ip %s" % (servername,vip)

        ret = subprocess.call("expect " + FILE + " " + vip  + " " + user + " " + passwd + " " + port, shell=True, stdout=sys.stderr, stderr=sys.stderr) 
        if ret == 0:
            subprocess.call("clear " , shell=True, stdout=sys.stderr, stderr=sys.stderr) 
            print "logout server %s  host" % vip
            print "您已经退出服务器 %s " % servername
            subprocess.call("exit 0" , shell=True, stdout=sys.stderr, stderr=sys.stderr) 
        else :
            ret = subprocess.call("ssh-keygen -R %s " % vip, shell=True ,stdout=sys.stderr, stderr=sys.stderr)
            if ret == 0:
                ret = subprocess.call("expect " + FILE + " " + vip  + " " + user + " " + passwd + " " + port, shell=True, stdout=sys.stderr, stderr=sys.stderr) 
            else:
                print "%s ip is not useage" % vip

    except subprocess.CalledProcessError.message as e:
        print "Execution failed:", e

        if ret == 0:
            subprocess.call("clear " , shell=True, stdout=sys.stderr, stderr=sys.stderr) 
            print "logout server %s  host" % vip
            print "您已经退出服务器 %s " % servername
            subprocess.call("exit 0 " , shell=True, stdout=sys.stderr, stderr=sys.stderr) 
        else :
            ret = subprocess.call("ssh-keygen -R %s " % vip, shell=True, stdout=sys.stderr, stderr=sys.stderr )
            print "%s ip is not useage" % vip


## check vmname host
def check_vmnames(vmname=None):
    if vmname not in SERVERS.keys() or vmname is None:
        for vmname , values in SERVERS.items():
            print "please input\t%s\t------->\tlogin info\t%s " % (vmname,values)
        sys.exit(1)

    return True 

## get vmname host
def get_vmnames(vmnames="all"):
    if vmnames == "all":
        vmnames = SERVERS.keys()

    for vmname in vmnames:
        if check_vmnames(vmname):
            login_server(vmname, FILE)

## main function 
if __name__ == "__main__":
    vmnames = sys.argv[1:]
    #get_vmnames(vmnames)
    if len(vmnames) > 0:
        serverdict =  read_conf(CONF_FILE, vmnames[0])
        login_server(vmnames[0], serverdict,FILE)
    else:
        print "please input ssh server name eg: vm200"


