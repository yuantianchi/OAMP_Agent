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
        LogObj.info("Listening port %s service startup" % ("80" + tomcatId))
        startTime = T.getCurrentTime()
        while True:
            codestatus = self.getHttpStatusCode(checkurl)
            time.sleep(1)
            if (codestatus == 200):
                LogObj.info("端口：%s服务启动成功" % ("80" + str(tomcatId)))
                return True
            else:
                currTime = T.getCurrentTime()
                print("耗时:",T.getReduceTime(startTime, currTime))
                if T.getReduceTime(startTime, currTime) >= maxcheckTime:
                    LogObj.error("端口：%s服务启动失败" % ("80" + str(tomcatId)))
                    return False


def getInstance():
    return Url()
