#!/usr/bin/env python
# !-*- coding:utf-8 -*-

from bin import ProjectFunc, Nginxfunc, Tomcat, Init
from util import Mail, PrintLog

T = Tomcat.getInstance()
N = Nginxfunc.getInstance()
M = Mail.getInstance()
init = Init.getInstance()
init.getProjectInfo()
LogObj = PrintLog.getInstance()


class Menu:
    def __init__(self, info):
        self.info = info

    def initProjectConf(self):
        projectConfig = self.info
        init.initProjectInfo(projectConfig)
        init.getProjectInfo()

    def updateProject(self):
        ProjectFunc.getInstance(self.info).updateProject()
    #重启项目对应的所有tomcat
    def restartProjectTom(self):
        projectName = self.info["projectName"]
        T.restartProjectTom(projectName)

    #单独重启某个tomcat
    def restartOneTomcat(self):
        tomcatId = T.handleTomcatId(self.info["tomcatId"])
        self.stopOneTomcat(tomcatId)
        self.startOneTomcat(tomcatId)

    #单独停止某个tomcat
    def stopOneTomcat(self,tomcatId=None):
        if tomcatId is None:
            tomcatId = T.handleTomcatId(self.info["tomcatId"])
        tomcatName = "tomcatA" + tomcatId
        T.stopTomcat(tomcatName)
        N.closeNginxUpstream(tomcatId)

    #单独启动某个tomcat
    def startOneTomcat(self,tomcatId=None):
        if tomcatId is None:
            tomcatId = T.handleTomcatId(self.info["tomcatId"])
        tomcatName = "tomcatA" + tomcatId
        T.startTomcat(tomcatName)
        N.openNginxUpstream(tomcatId)

    # 从本机拿资源更新（已上传更新文件到服务上时使用）
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
