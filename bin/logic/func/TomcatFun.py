#!/usr/bin/env python
# !-*- coding:utf-8 -*-

from bin.base.tool import Time, Url
from bin.base.log import PrintLog
import time
import bin
import math
from bin.logic.func import Nginxfunc
import os
from bin.base.sys import PR
from bin.logic.bo import RestartInfo
from concurrent.futures import ThreadPoolExecutor, as_completed

LogObj = PrintLog.getInstance()
T = Time.getIntance()
U = Url.getInstance()

Nginx = Nginxfunc.getInstance()

TOMCAT_SLEEP_TIME = 2


class Tomcat(object):
    def __init__(self):
        pass

    # 关闭tomcat
    def stopTomcat(self, tomcatName, maxRestartCount=2):
        stopFailRetriesNum = int(maxRestartCount) - 1
        stopCmd = "service %s stop" % (tomcatName)
        LogObj.info("exec command: " + stopCmd)
        os.system(stopCmd)
        time.sleep(TOMCAT_SLEEP_TIME)
        status = self.checkTomcat(tomcatName)
        num = 0
        while status:
            # 判读尝试次数是到了最大尝试次数
            if num >= stopFailRetriesNum:
                LogObj.error("stop service failed, terminate the program")
                return False
            num = num + 1
            pid = " ".join(self.getTomcatPid(tomcatName))
            killcmd = "kill -9 %s" % (pid)
            # 获取tomcat pid
            if pid:
                LogObj.info("try again stop %s, exec: %s" % (tomcatName, killcmd))
                os.system(killcmd)
            else:
                LogObj.info("%s has stopped" % (tomcatName))
                return True
            time.sleep(2)
            status = self.checkTomcat(tomcatName)
            if status:
                LogObj.error("stop %s failed" % (tomcatName))
            else:
                LogObj.info("stop %s successful!" % (tomcatName))
                return True
        return True

    # 启动tomcat
    def startTomcat(self, tomcatName, maxRestartCount=2):
        startFailRetriesNum = int(maxRestartCount) - 1
        startCmd = "service %s start" % tomcatName
        LogObj.info("exec: " + startCmd)
        os.system(startCmd)
        time.sleep(TOMCAT_SLEEP_TIME)
        status = self.checkTomcat(tomcatName)
        num = 0
        while not status:
            if num >= startFailRetriesNum:
                LogObj.error("start service failed, terminate the program")
                return False
            num = num + 1
            LogObj.info("try again start %s, exec: %s" % (tomcatName, startCmd))
            os.system(startCmd)
            time.sleep(TOMCAT_SLEEP_TIME)
            status = self.checkTomcat(tomcatName)
            if status:
                LogObj.info("start %s successful!" % (tomcatName))
                return True
            else:
                LogObj.error("start %s failed" % (tomcatName))
        return True

    # 重启tomcat --- 不屏蔽nginx端口
    def restartOneTomcat(self, tomcatName):
        if self.stopTomcat(tomcatName) and self.startTomcat(tomcatName):
            return True
        else:
            return False

    # 检查tomcat是否启动成功
    def checkTomcat(self, tomcatName):
        execCmd = "ps -ef|grep %s|grep -v 'grep'|awk '{print $2}'" % tomcatName
        r_execCmd = os.popen(execCmd)
        result = r_execCmd.read()
        r_execCmd.close()
        if not str(result).strip():
            LogObj.info("%s status is stoped" % (tomcatName))
            return False
        LogObj.info("%s status is running" % (tomcatName))
        return True

    # 获取tomcatPid
    def getTomcatPid(self, tomcatName):
        execCmd = "ps -ef|grep %s|grep -v 'grep'|awk '{print $2}'" % (tomcatName)
        r_execCmd = os.popen(execCmd)
        pidstr = r_execCmd.read().strip()
        r_execCmd.close()
        if pidstr == "":
            return []
        return pidstr.split("\n")

    def restartProjectOneTomcat(self, projectName, tomcatInfo):
        _RestartInfo = RestartInfo.getInstance()
        projectInfo = bin.PROJECT_INFO.get(projectName, None)
        serverIp = bin.CONF_INFO.get("serverIp", None)
        maxCheckTime = projectInfo.get("serviceMaxCheckTime", None)
        maxRestartCount = projectInfo.get("maxRestartCount", None)
        serviceCheckUrl = projectInfo.get("serviceCheckUrl", None)
        Nginx.closeNginxUpstream(tomcatInfo["port"])
        if not self.stopTomcat(tomcatInfo["name"], maxRestartCount):
            return _RestartInfo.setMsg("关闭%s失败").setCode(PR.Code_ERROR).setfailList(tomcatInfo)
        if not self.startTomcat(tomcatInfo["name"], maxRestartCount):
            return _RestartInfo.setMsg("启动%s失败").setCode(PR.Code_ERROR).setfailList(tomcatInfo)
        if serviceCheckUrl:
            checkurl = "http://" + str(serverIp) + ":" + str(tomcatInfo["port"]) + os.sep + str(serviceCheckUrl)
            if U.checkService(tomcatInfo["port"], checkurl, maxCheckTime):
                Nginx.openNginxUpstream(tomcatInfo["port"])
                LogObj.info("%s corresponding service started success" % (tomcatInfo["name"]))
            else:
                return _RestartInfo.setCode(PR.Code_ERROR).setfailList(tomcatInfo).setMsg("启动%s项目失败，%s对应服务启动失败超时" % (projectName, tomcatInfo["name"]))
        else:
            Nginx.openNginxUpstream(tomcatInfo["port"])
            LogObj.info("%s corresponding service started success" % (tomcatInfo["name"]))
        return _RestartInfo.setCode(PR.Code_OK).setMsg("restart %s corresponding service success" % (tomcatInfo["name"]))

    def restartProjectTom(self, projectName, restartMode="one_half"):
        _PR = PR.getInstance()
        projectInfo = bin.PROJECT_INFO.get(projectName, None)
        tomcatInfo = projectInfo.get("tomcatInfo", None)
        serverIp = bin.CONF_INFO.get("serverIp", None)
        if not projectInfo or not tomcatInfo or not serverIp:
            result = {"confErrorProject": projectName}
            return _PR.setData(result).setCode(PR.Code_ERROR).setMsg("Project configuration file error")
        okRestartTomcat = []
        yetRestartTomcat = []
        failRestartTomcat = []
        willRestartTomcat = []
        lastRestartTomcat = tomcatInfo

        if restartMode == "one_half":
            firstRestartCount = len(tomcatInfo) // 2
            if (firstRestartCount < len(tomcatInfo) / 2):
                firstRestartCount = int(firstRestartCount) + 1
            willRestartTomcat = lastRestartTomcat[:firstRestartCount]
        elif restartMode == "whole":
            willRestartTomcat = lastRestartTomcat
        else:
            willRestartTomcat = lastRestartTomcat[:-len(lastRestartTomcat) + 1]

        while len(willRestartTomcat) > 0:

            LogObj.info("进行%s项目重启，即将重启%s，还未重启的有%s，服务重启成功的有%s" % (projectName, willRestartTomcat, str(lastRestartTomcat), str(okRestartTomcat)))
            executor = ThreadPoolExecutor(max_workers=len(willRestartTomcat))
            task = [executor.submit(self.restartProjectOneTomcat, projectName, t) for t in willRestartTomcat]
            isSuccess = True
            for future in as_completed(task):
                data = future.result()
                if data.getCode() == RestartInfo.Code_ERROR:
                    failRestartTomcat.append(data.getFailList())
                    isSuccess = False
            if not isSuccess:
                LogObj.error("重启项目失败，重启成功的tomcat有：%s 失败的tomcat有：%s，还未有重启的tomcat有：%s" % (str(okRestartTomcat), str(failRestartTomcat), str(yetRestartTomcat)))
                return _PR.setCode(PR.Code_ERROR).setMsg("重启项目失败，重启成功的tomcat有：%s 失败的tomcat有：%s，还未有重启的tomcat有：%s" % (str(okRestartTomcat), str(failRestartTomcat), str(yetRestartTomcat)))

            if restartMode == "one_half":
                okRestartTomcat.extend(willRestartTomcat)
                lastRestartTomcat = lastRestartTomcat[len(willRestartTomcat):]
                willRestartTomcat = lastRestartTomcat
            elif restartMode == "whole":
                okRestartTomcat = tomcatInfo
                lastRestartTomcat = []
                willRestartTomcat = []
            else:
                okRestartTomcat.extend(willRestartTomcat)
                lastRestartTomcat = lastRestartTomcat[1:]
                willRestartTomcat = lastRestartTomcat[:-len(lastRestartTomcat) + 1]

        LogObj.info("%s项目重启成功" % projectName)
        return _PR.setCode(PR.Code_OK).setMsg("%s项目重启成功" % (projectName))

    # 重启项目对应的tomcat
    # def restartProjectTom(self, projectName):
    #     _PR = PR.getInstance()
    #     projectInfo = bin.PROJECT_INFO.get(projectName, None)
    #     tomcatInfo = projectInfo.get("tomcatInfo", None)
    #     serverIp = bin.CONF_INFO.get("serverIp", None)
    #     if not projectInfo or not tomcatInfo or not serverIp:
    #         result = {"confErrorProject": projectName}
    #         return _PR.setData(result).setCode(PR.Code_ERROR).setMsg("Project configuration file error")
    #     maxCheckTime = projectInfo.get("serviceMaxCheckTime", None)
    #     maxRestartCount = projectInfo.get("maxRestartCount", None)
    #     serviceCheckUrl = projectInfo.get("serviceCheckUrl", None)
    #     restartSuccessedTomcat = []
    #     for infoList in tomcatInfo:
    #         LogObj.info("进行%s项目重启，正在重启%s，还未重启的有%s，服务重启成功的有%s" % (projectName, infoList["name"], str(tomcatInfo[tomcatInfo.index(infoList) + 1:]), str(restartSuccessedTomcat)))
    #         Nginx.closeNginxUpstream(infoList["port"])
    #         if not self.stopTomcat(infoList["name"], maxRestartCount):
    #             return _PR.setMsg("关闭%s失败，还未重启的有%s，重启成功的有%s" % (infoList["name"], str(tomcatInfo[tomcatInfo.index(infoList) + 1:]), str(restartSuccessedTomcat))).setCode(PR.Code_ERROR)
    #         if not self.startTomcat(infoList["name"], maxRestartCount):
    #             return _PR.setMsg("启动%s失败，还未重启的有%s，重启成功的有%s" % (infoList["name"], str(tomcatInfo[tomcatInfo.index(infoList) + 1:]), str(restartSuccessedTomcat))).setCode(PR.Code_ERROR)
    #
    #         if serviceCheckUrl:
    #             checkurl = "http://" + str(serverIp) + ":" + str(infoList["port"]) + os.sep + str(serviceCheckUrl)
    #             if U.checkService(infoList["port"], checkurl, maxCheckTime):
    #                 Nginx.openNginxUpstream(infoList["port"])
    #                 LogObj.info("%s corresponding service started success" % (infoList["name"]))
    #             else:
    #                 return _PR.setCode(PR.Code_ERROR).setMsg("启动%s项目失败，%s对应服务启动失败超时，还未重启的有%s，服务重启成功的有%s" % (projectName, infoList["name"], str(tomcatInfo[tomcatInfo.index(infoList) + 1:]), str(restartSuccessedTomcat)))
    #         else:
    #             Nginx.openNginxUpstream(infoList["port"])
    #             LogObj.info("%s corresponding service started success" % (infoList["name"]))
    #         restartSuccessedTomcat.append(infoList["name"])
    #
    #     result = {"restartSuccessedTomcat": restartSuccessedTomcat}
    #     LogObj.info("%s项目重启成功" % projectName)
    #     return _PR.setCode(PR.Code_OK).setMsg("restart project %s success" % (projectName)).setData(result)

    # 将小于两位数的tomcatId前面加0
    def handleTomcatId(self, tag):
        if int(tag) < 10:
            tomcatId = "0" + str(tag)
        else:
            tomcatId = str(tag)
        return tomcatId


def getInstance():
    return Tomcat()
