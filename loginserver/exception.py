# author: zwei
# email: suifeng20@hotmail.com
# data: 2016/3/2

from loginserver.common.exception import LoginserverError as Error


class NotFoundPKey(Error):
    msg_fmt = ("Not Found PRIVATE KEY file in %(pkey)s")


class NotFoundHost(Error):
    msg_fmt = ("Not Found ssh server hostname %(host)s from config")


class ExceptionPexpect(Error):
    msg_fmt = ("Pexpct runing Error")


class NotFoundHostIp(Error):
    msg_fmt = ("Not Found ssh server alias: %(alias)s and "
               "ip or hostname : %(ip)s")
