#coding: utf-8
#author zwei
#email suifeng20@hotmail.com

import os
import sys
import inspect

from loginserver.common import exception

def _get_binary_name():
    return os.path.basename(inspect.stack()[-1][1])

def _fixpath(p):
    """Apply tilde expansion and absolutization to a path."""
    return os.path.abspath(os.path.expanduser(p))

def _get_config_dirs(project=None):
    """ ~/.foo.conf
        ~/.foo/foo.conf
        /etc/foo.conf
        /etc/foo/foo.conf
    """
    cfg_dirs = [
        _fixpath(os.path.join('~', '.' + project)) if project else None,
        _fixpath('~'),
        os.path.join('/etc', project) if project else None,
        '/etc'
    ]
    return cfg_dirs


def _find_default_config(project=None, exten='.conf'):
    """ ~/.foo.conf
        ~/.foo/foo.conf
        /etc/foo.conf
        /etc/foo/foo.conf
    """
    if project is None:
        project = _get_binary_name() 
    default_dirs = _get_config_dirs(project)
    for pdir in default_dirs:
        tempfile = os.path.join(pdir, project + exten)
        if os.path.exists(tempfile):
            return tempfile


def find_config_file(pdir=None, pfile=None, exten='.conf'):
    confdir = os.path.expanduser('~/.ssh') 
    binfile = _get_binary_name() + exten 
    pdir = pdir or confdir
    if not os.path.exists(pdir):
        os.mkdir(pdir, 0755)
    if pfile is None:
        pfile = os.path.join(confdir, binfile)
    if os.path.exists(pfile):
        return pfile
    else:
        pfile = _find_default_config()
    if pfile is None:
        raise exception.LogConfigError(msg="Not Found %s Configfile" % pfile)



class Config(object):
    pass


if __name__ == '__main__':
    print _get_binary_name()
    find_config_file()
    _find_default_config()
