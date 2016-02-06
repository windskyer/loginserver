class Error(Exception):
    pass

class LoginserverError(Exception):
    message = _("An unknown exception occurred.")
    code = 500
    headers = {}
    safe = False
    super.__init__(LoginserverError, self)

class LogConfigError(base_excption):
    message = "Not Found %(pfile)s"
    super.__init__(LogConfigError, self)
