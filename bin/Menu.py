#!/usr/bin/env python
# !-*- coding:utf-8 -*-

from bin import ProjectFunc, Nginxfunc, Tomcat,Init
from util import Mail,PrintLog
import json
T = Tomcat.getInstance()
N = Nginxfunc.getInstance()
M = Mail.getInstance()
init = Init.getInstance()
init.getProjectInfo()
LogObj=PrintLog.getInstance()

class Menu:
    def __init__(self, info):
        self.info = info

    def initProjectConf(self):
        projectConfig=self.info
        init.initProjectInfo(projectConfig)
        init.getProjectInfo()

    def updateProject(self):
        ProjectFunc.getInstance(self.info).updateProject()

    def restartProjectTom(self):
        projectName = self.info["projectName"]
        T.restartProjectTom(projectName)

    def restartTomcats(self):
        tomcatList = self.info["tomcatList"]
        for tom in tomcatList:
            self.stopTomcat(tom)
            self.tomcatList(tom)

    def stopTomcat(self):
        tomcatList = json.loads(self.info["tomcatList"])
        for tom in tomcatList:
            tomName = "tomcatA" + str(tom)
            T.stopTomcat(tomName)
            N.closeNginxUpstream(tom)
        LogObj.info("关闭tomcatList:%s完成" % (tomcatList))

    def startTomcat(self):
        tomcatList = json.loads(self.info["tomcatList"])
        for tom in tomcatList:
            tomName = "tomcatA" + str(tom)
            T.startTomcat(tomName)
            N.openNginxUpstream(tom)
        LogObj.info("启动tomcatList:%s完成"%(tomcatList))

    #从本机拿资源更新（已上传更新文件到服务上时使用）
    def localUpdateProject(self):
        ProjectFunc.getInstance(self.info).localUpdateProject()

    def help(self):
        pass

    @staticmethod
    def sendMail(msg_content, receivers=[], receivers_EMail=[], subject=None):
        M.sendMail(msg_content=msg_content, receivers=receivers, receivers_EMail=receivers_EMail,
                   subject=subject)

    def getMethods(self):
        return (list(filter(lambda m: not m.startswith("__") and not m.endswith("__") and callable(getattr(self, m)),
                            dir(self))))


def getInstance(info):
    return Menu(info)
