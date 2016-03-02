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

class ParseError(Exception):
    def __init__(self, message, lineno, line):
        self.msg = message
        self.line = line
        self.lineno = lineno

    def __str__(self):
        return 'at line %d, %s: %r' % (self.lineno, self.msg, self.line)

class BaseParser(object):
    lineno = 0
    parse_exc = ParseError

    def _assignment(self, key, value):
        self.assignment(key, value)
        return None, []

    def _get_section(self, line):
        if not line.endswith(']'):
            return self.error_no_section_end_bracket(line)
        if len(line) <= 2:
            return self.error_no_section_name(line)

        return line[1:-1]
    
    def _split_key_value(self, line):
        colon = line.find(':')
        equal = line.find('=')
        if colon < 0 and equal < 0:
            return self.error_invalid_assignment(line)

        if colon < 0 or (equal >= 0 and equal < colon):
            key, value = line[:equal], line[equal + 1:]
        else:
            key, value = line[:colon], line[colon + 1:]

        value = value.strip()
        if value and value[0] == value[-1] and value.startswith(("\"", "'")):
            value = value[1:-1]
        return key.strip(), [value]

    def parse(self, lineiter):
        key = None
        value = []

        for line in lineiter:
            self.lineno += 1

            line = line.rstrip()
            if not line:
                # Blank line, ends multi-line values
                if key:
                    key, value = self._assignment(key, value)
                continue
            elif line.startswith((' ', '\t')):
                # Continuation of previous assignment
                if key is None:
                    self.error_unexpected_continuation(line)
                else:
                    value.append(line.lstrip())
                continue

            if key:
                # Flush previous assignment, if any
                key, value = self._assignment(key, value)

            if line.startswith('['):
                # Section start
                section = self._get_section(line)
                if section:
                    self.new_section(section)
            elif line.startswith(('#', ';')):
                self.comment(line[1:].lstrip())
            else:
                key, value = self._split_key_value(line)
                if not key:
                    return self.error_empty_key(line)
        if key:
            # Flush previous assignment, if any
            self._assignment(key, value)

    def assignment(self, key, value):
        """Called when a full assignment is parsed."""
        raise NotImplementedError()

    def new_section(self, section):
        """Called when a new section is started."""
        raise NotImplementedError()

    def comment(self, comment):
        """Called when a comment is parsed."""
        pass

    def error_empty_key(self, line):
        raise self.parse_exc('Key cannot be empty', self.lineno, line)

    def error_no_section_end_bracket(self, line):
        raise self.parse_exc('Invalid section (must end with ])',
                             self.lineno, line)

    def error_unexpected_continuation(self, line):
        raise self.parse_exc('Unexpected continuation line',
                             self.lineno, line)

    def error_no_section_name(self, line):
        raise self.parse_exc('Empty section name', self.lineno, line)

class Config(object):
    def read_conf(conf=None, name=None):
        returndict = {}
        servernamelist = []
    pass


if __name__ == '__main__':
    print _get_binary_name()
    find_config_file()
    _find_default_config()
