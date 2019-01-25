#!/usr/bin/env python
# !-*- coding:utf-8 -*-

import bin
from bin.base.sys import PR
from bin.init import Init
from bin.logic.func import Nginxfunc, TomcatFun
from bin.base.tool import Mail
from bin.base.log import PrintLog
from bin.logic.func import AgentProjectFunc
from bin.logic.func import AgentTomcatFunc

T = TomcatFun.getInstance()
M = Mail.getInstance()

N = Nginxfunc.getInstance()
LogObj = PrintLog.getInstance()
_PR = PR.getInstance()
I = Init.getInstance()


class Service_logic():
    def __init__(self):
        pass

    # 以增量形式初始化项目配置信息
    def initProjectConf(self, info):
        return AgentProjectFunc.getInstance().initProjectConf(info=info)

    # 更新LEAP项目资源
    def replaceResource(self, info):
        return AgentProjectFunc.getInstance().replaceResource(info=info)

    # 重启项目对应的所有tomcat
    def restartProject(self, info):
        return AgentProjectFunc.getInstance().restartProject(info=info)

    # 更新项目
    def updateProject(self, info):
        return AgentProjectFunc.getInstance().updateProject(info=info)

    #获取项目运行状态
    def getProjectStatus(self,info):
        return AgentProjectFunc.getInstance().getProjectStatus(info=info)

    # 单独重启某个tomcat
    def restartOneTomcat(self, info):
        return AgentTomcatFunc.getInstance().restartOneTomcat(info=info)

    # 单独停止某个tomcat
    def stopOneTomcat(self, info):
        return AgentTomcatFunc.getInstance().stopOneTomcat(info=info)

    # 单独启动某个tomcat
    def startOneTomcat(self, info):
        return AgentTomcatFunc.getInstance().startOneTomcat(info=info)



    # # -------------------------------
    # # 服务器上直接使用
    # def localUpdateProject(self, info):
    #     ProjectFunc.getInstance(info).localUpdateProject()
    #
    # def help(self):
    #     pass
    #
    # # 通过redis订阅更新项目
    # def updateProject_reids(self, info):
    #     ProjectFunc.getInstance(info).updateProject_redis()
    #
    # @staticmethod
    # def sendMail(msg_content, receivers=[], receivers_EMail=[], subject=None):
    #     M.sendMail(msg_content=msg_content, receivers=receivers, receivers_EMail=receivers_EMail,
    #                subject=subject)
    #
    # def getMethods(self):
    #     return (list(filter(lambda m: not m.startswith("__") and not m.endswith("__") and callable(getattr(self, m)),
    #                         dir(self))))
    #
    # # -------------------------------
def getInstance():
    return Service_logic()
