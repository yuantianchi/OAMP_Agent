#!/usr/bin/env python
# !-*- coding:utf-8 -*-

import requests
import time
from bin.base.tool import Time
from bin.base.log import PrintLog

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
    def checkService(self, nginxPort, checkurl, maxcheckTime=300):
        LogObj.info("Listening port %s service startup..." % (str(nginxPort)))
        startTime = T.getCurrentTime()
        while True:
            codestatus = self.getHttpStatusCode(checkurl)
            consumeTime = T.getReduceTime(startTime, T.getCurrentTime())
            LogObj.info("check url: %s, status code: %s, check time is %ss" % (checkurl, str(codestatus), str(consumeTime)))
            if (codestatus == 200):
                LogObj.info(
                    "port %s Service started successfully, time consuming: %ss" % (nginxPort, consumeTime))
                return True
            else:
                if consumeTime >= maxcheckTime:
                    LogObj.error("port %s service failed to start, time consuming: %ss" % (nginxPort, consumeTime))
                    return False
            time.sleep(3)


def getInstance():
    return Url()
