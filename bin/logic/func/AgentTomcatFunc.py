#!/usr/bin/env python
# !-*- coding:utf-8 -*-

from bin.base.sys import PR
from bin.init import Init
from bin.logic.func import  Nginxfunc, TomcatFun
from bin.base.tool import Mail
from bin.base.log import PrintLog

T = TomcatFun.getInstance()
M = Mail.getInstance()

N = Nginxfunc.getInstance()
LogObj = PrintLog.getInstance()
_PR = PR.getInstance()
I = Init.getInstance()


class AgentTomcatFunc(object):
    def __init__(self):
        pass
    # 单独重启某个tomcat
    def restartOneTomcat(self, info):
        tomcatName = info["tomcatName"]
        projectName = info["projectName"]
        stopOneTomcatInfo = {"method": "stopOneTomcat", "projectName": projectName, "tomcatName": tomcatName}
        startOneTomcatInfo = {"method": "startOneTomcat", "projectName": projectName, "tomcatName": tomcatName}
        self.stopOneTomcat(stopOneTomcatInfo)
        self.startOneTomcat(startOneTomcatInfo)
        return _PR.setData(info).setCode(PR.Code_OK).setMsg('restart %s success' % (tomcatName))

    # 单独停止某个tomcat
    def stopOneTomcat(self, info):
        tomcatName = info['tomcatName']
        nginxPort = info['nginxPort']

        if not T.stopTomcat(tomcatName, self.maxRestartCount):
            return _PR.setData(info).setCode(PR.Code_OK).setMsg('stop %s failed' % (tomcatName))
        else:
            N.closeNginxUpstream(nginxPort)
            return _PR.setData(info).setCode(PR.Code_OK).setMsg('stop %s success' % (tomcatName))

    # 单独启动某个tomcat
    def startOneTomcat(self, info):
        tomcatName = info['tomcatName']
        nginxPort = info['nginxPort']
        if not T.startTomcat(tomcatName, self.maxRestartCount):
            return _PR.setMsg("start %s failed" % (tomcatName)).setCode(2)
        else:
            N.openNginxUpstream(nginxPort)
            return _PR.setMsg("start %s success" % (tomcatName)).setCode(2)

def getInstance():
    return AgentTomcatFunc()
