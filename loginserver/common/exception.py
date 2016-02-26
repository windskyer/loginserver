class Error(Exception):
    pass

class LoginserverError(Exception):
    message = ("An unknown exception occurred.")
    code = 500
    headers = {}
    safe = False
    def __init__(self):
        super(LoginserverError, self).__init__()

class LogConfigError(Error):
    msg = "unkwon"
    def __init__(self, msg):
        self.msg = msg
        super(LogConfigError, self).__init__(self.msg)
