#!/usr/bin/env python
# !-*- coding:utf-8 -*-

from bin.base.tool import Time, Url
from bin.base.log import PrintLog
import time
import bin
from bin.logic.func import Nginxfunc
import os
from bin.base.sys import PR

LogObj = PrintLog.getInstance()
T = Time.getIntance()
U = Url.getInstance()
_PR = PR.getInstance()
Nginx = Nginxfunc.getInstance()


class Tomcat(object):
    def __init__(self):
        pass

    # 关闭tomcat
    def stopTomcat(self, tomcatName, maxRestartCount=2):
        stopFailRetriesNum = int(maxRestartCount) - 1
        stopCmd = "service %s stop" % (tomcatName)
        LogObj.info("exec command: " + stopCmd)
        os.system(stopCmd)
        time.sleep(2)
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
        time.sleep(3)
        status = self.checkTomcat(tomcatName)
        num = 0
        while not status:
            if num >= startFailRetriesNum:
                LogObj.error("start service failed, terminate the program")
                return False
            num = num + 1
            LogObj.info("try again start %s, exec: %s" % (tomcatName, startCmd))
            os.system(startCmd)
            time.sleep(3)
            status = self.checkTomcat(tomcatName)
            if status:
                LogObj.info("start %s successful!" % (tomcatName))
                return True
            else:
                LogObj.error("start %s failed" % (tomcatName))
        return True

    # 检查tomcat是否启动成功
    def checkTomcat(self, tomcatName):
        execCmd = "ps -ef|grep %s|grep -v 'grep'|awk '{print $2}'" % tomcatName
        result = os.popen(execCmd)
        pidList = result.read()
        if not str(pidList).strip():
            LogObj.info("%s status is stoped" % (tomcatName))
            return False
        LogObj.info("%s status is running" % (tomcatName))
        return True

    # 获取tomcatPid
    def getTomcatPid(self, tomcatName):
        execCmd = "ps -ef|grep %s|grep -v 'grep'|awk '{print $2}'" % (tomcatName)
        result = os.popen(execCmd)
        pidstr = result.read().strip()
        if pidstr == "":
            return []
        pidList = pidstr.split("\n")
        return pidList

    # 重启项目对应的tomcat
    def restartProjectTom(self, projectName):
        projectInfo = bin.PROJECT_INFO.get(projectName, None)
        tomcatInfo = projectInfo.get("tomcatInfo", None)
        serverIp = bin.CONF_INFO.get("serverIp", None)
        if not projectInfo or not tomcatInfo or not serverIp:
            result = {"confErrorProject": projectName}
            return _PR.setData(result).setCode(PR.Code_ERROR).setMsg("Project configuration file error")
        maxCheckTime = projectInfo.get("serviceMaxCheckTime", None)
        maxRestartCount = projectInfo.get("maxRestartCount", None)
        serviceCheckUrl = projectInfo.get("serviceCheckUrl", None)
        restartSuccessedTomcat = []
        for infoList in tomcatInfo:
            Nginx.closeNginxUpstream(infoList["port"])
            if not self.stopTomcat(infoList["name"], maxRestartCount):
                return _PR.setMsg("关闭%s失败，还未重启的有%s，重启成功的有%s" % (infoList["name"], str(tomcatInfo[tomcatInfo.index(infoList) + 1:]), str(restartSuccessedTomcat))).setCode(PR.Code_ERROR)

            if not self.startTomcat(infoList["name"], maxRestartCount):
                return _PR.setMsg("启动%s失败，还未重启的有%s，重启成功的有%s" % (infoList["name"], str(tomcatInfo[tomcatInfo.index(infoList) + 1:]), str(restartSuccessedTomcat))).setCode(PR.Code_ERROR)

            if serviceCheckUrl:
                # checkurl = "http://" + str(serverIp) + ":" + str(infoList["port"]) + os.sep + str(serviceCheckUrl)
                checkurl = "http://" + str(serverIp) + os.sep + str(serviceCheckUrl)
                if U.checkService(infoList["port"], checkurl, maxCheckTime):
                    Nginx.openNginxUpstream(infoList["port"])
                    LogObj.info("%s corresponding service started success" % (infoList["name"]))
                else:
                    return _PR.setCode(PR.Code_ERROR).setMsg("启动%s项目失败，%s对应服务启动失败超时，还未重启的有%s，服务重启成功的有%s" % (projectName, infoList["name"], str(tomcatInfo[tomcatInfo.index(infoList) + 1:]), str(restartSuccessedTomcat)))
            else:
                Nginx.openNginxUpstream(infoList["port"])
                LogObj.info("%s corresponding service started success" % (infoList["name"]))
            restartSuccessedTomcat.append(infoList["name"])
        result = {"restartSuccessedTomcat": restartSuccessedTomcat}
        LogObj.info("%s项目重启成功" % projectName)
        return _PR.setCode(PR.Code_OK).setMsg("restart project %s success" % (projectName)).setData(result)

    # 将小于两位数的tomcatId前面加0
    def handleTomcatId(self, tag):
        if int(tag) < 10:
            tomcatId = "0" + str(tag)
        else:
            tomcatId = str(tag)
        return tomcatId


def getInstance():
    return Tomcat()
