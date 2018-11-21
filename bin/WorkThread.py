#!/usr/bin/env python
# !-*- coding:utf-8 -*-
import threading
from bin import Menu
from util import PrintLog

LogObj = PrintLog.getInstance()


class WorkThread(threading.Thread):
    def __init__(self, msg):
        threading.Thread.__init__(self)
        # super(WorkThread, self).__init__()
        self.msg = msg

    def run(self):
        try:
            print("run 此时线程数：", self.getThreadCount())
            info = eval(self.msg[2].decode("utf-8"))
            methodName = info["method"]
            Me = Menu.getInstance(info)
            if methodName in Me.getMethods():
                getattr(Me, methodName)()
            else:
                LogObj.error("specified method[methodName:\"%s\"] error,no such method" % (methodName))
            # Menu.Menu.sendMail("%s operate complete ！" % (methodName))
        except BaseException as e:
            # Menu.Menu.sendMail("%s 操作失败：%s" % (methodName, str(e)))
            print(str(e))

    @classmethod
    def getThreadCount(cls):
        return threading.active_count()


def getInstance(msg):
    return WorkThread(msg)
