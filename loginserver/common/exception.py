import sys
import six

class Error(Exception):
    pass

class LoginserverError(Exception):
    msg_fmt = ("An unknown exception occurred.")
    code = 500
    headers = {}
    safe = False
    def __init__(self, message=None, **kwargs):
        self.kwargs = kwargs
        if 'code' not in kwargs:
            try:
                self.kwargs['code'] = self.code
            except AttributeError:
                pass

        if not message:
            try:
               message = self.msg_fmt % kwargs
            except Exception:
                exc_info = sys.exc_info()
                LOG.exception('Exception in string format operation')
                for name, value in six.iteritems(kwargs):
                    LOG.error("%s: %s" % (name, value))
                six.reraise(*exc_info)

        self.message = message
        super(LoginserverError, self).__init__(message)
    
class LogConfigError(Error):
    msg = "unkwon"
    def __init__(self, msg):
        self.msg = msg
        super(LogConfigError, self).__init__(self.msg)
