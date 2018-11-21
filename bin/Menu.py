#!/usr/bin/env python
# !-*- coding:utf-8 -*-

from bin import ProjectFunc, Nginxfunc, Tomcat,Init
from util import Mail

T = Tomcat.getInstance()
N = Nginxfunc.getInstance()
M = Mail.getInstance()
init = Init.getInstance()
init.getProjectInfo()

class Menu:
    def __init__(self, info):
        self.info = info
        self.P = ProjectFunc.getInstance(info)
        print("info:", self.info)


    def initProjectConf(self):
        projectConfig=self.info
        init.initProjectInfo(projectConfig)
        init.getProjectInfo()

    def updateProject(self):
        self.P.updateProject()

    def restartProjectTom(self):
        projectName = self.info["projectName"]
        T.restartProjectTom(projectName)

    def restartTomcats(self):
        tomcatList = self.info["tomcatList"]
        for tom in tomcatList:
            self.stopTomcat(tom)
            self.tomcatList(tom)

    def stopTomcat(self):
        tomcatList = self.info["tomcatList"]
        for tom in tomcatList:
            tomName = "tomcatA" + tom
            T.stopTomcat(tomName)
            N.closeNginxUpstream(tom)

    def startTomcat(self):
        tomcatList = self.info["tomcatList"]
        for tom in tomcatList:
            tomName = "tomcatA" + tom
            T.startTomcat(tomName)
            N.openNginxUpstream(tom)

    #从本机拿资源更新（已上传更新文件到服务上时使用）
    def localUpdateProject(self):
        self.P.localUpdateProject()

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
