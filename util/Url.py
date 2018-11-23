#!/usr/bin/env python
# !-*- coding:utf-8 -*-

import requests
import time
from util import PrintLog, Time

T = Time.getIntance()

LogObj = PrintLog.getInstance()


class Url:
    def __init__(self):
        pass

    def getHttpStatusCode(self, url):
        try:
            request = requests.get(url, timeout=3)
            httpStatusCode = request.status_code
            return httpStatusCode
        except:
            return "777"

    # 服务检测
    def checkService(self, tomcatId, checkurl, maxcheckTime=300):
        LogObj.info("Listening port %s service startup..." % ("80" + tomcatId))
        startTime = T.getCurrentTime()
        while True:
            codestatus = self.getHttpStatusCode(checkurl)
            time.sleep(1)
            consumeTime = T.getReduceTime(startTime, T.getCurrentTime())
            if (codestatus == 200):
                LogObj.info(
                    "port %s Service started successfully, time consuming: %ss" % ("80" + str(tomcatId), consumeTime))
                return True
            else:
                if consumeTime >= maxcheckTime:
                    LogObj.error("port %s service failed to start, time consuming: %ss" % ("80" + str(tomcatId)),
                                 consumeTime)
                    return False


def getInstance():
    return Url()
