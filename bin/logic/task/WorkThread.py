#!/usr/bin/env python
# !-*- coding:utf-8 -*-
import threading
from bin.base.log import PrintLog
from bin.base.tool import Time
from bak import DataFunc

T= Time.getIntance()
LogObj = PrintLog.getInstance()


class WorkThread(threading.Thread):
    def __init__(self, info):
        threading.Thread.__init__(self)
        # super(WorkThread, self).__init__()
        self.info = info

    def run(self):
        LogObj.info("run 此时线程数：%s"%(self.getThreadCount()))
        DataFunc.getInstance(self.info,self.obj).handlerMethod()




    @classmethod
    def getThreadCount(cls):
        return threading.active_count()


def getInstance(msg,obj):
    return WorkThread(msg)
