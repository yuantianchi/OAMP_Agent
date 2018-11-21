#!/usr/bin/env python
# !-*- coding:utf-8 -*-

from util import PrintLog, Time, Url
import time
import bin
from bin import Nginxfunc
import os
from bin import WorkThread

LogObj = PrintLog.getInstance()
T = Time.getIntance()
U = Url.getInstance()
Nginx = Nginxfunc.getInstance()


class Tomcat(object):
    def __init__(self):
        self.stopFailRetriesNum = 1
        self.StartFailRetriesNum = 1


    # 关闭tomcat
    def stopTomcat(self, tomcatName):
        stopCmd = "service %s stop" % tomcatName
        LogObj.info("exec command:" + stopCmd)
        os.system(stopCmd)
        time.sleep(2)
        status = self.checkTomcat(tomcatName)
        num = 0
        while status:
            num = num + 1
            pid = self.getTomcatPid(tomcatName)
            if len(pid):
                pid = pid[0]
            else:
                LogObj.info("%s has been closed" % (tomcatName))
                break
            killcmd = "kill -9 %s" %(pid)
            LogObj.info("try again stop %s ,exec: %s" % (tomcatName, killcmd))
            os.system(killcmd)
            time.sleep(2)
            status = self.checkTomcat(tomcatName)
            if status:
                LogObj.error("stop %s failed" % (tomcatName))
            else:
                LogObj.info("stop %s successful!" % (tomcatName))
                break
            if num > self.stopFailRetriesNum:
                LogObj.error("end try stop %s" % (tomcatName))
                exit("stop %s failed" % (tomcatName))

    # 启动tomcat
    def startTomcat(self, tomcatName):
        startCmd = "service %s start" % tomcatName
        LogObj.info("exec command:" + startCmd)
        os.system(startCmd)
        time.sleep(5)
        status = self.checkTomcat(tomcatName)
        num = 0
        while not status:
            num = num + 1
            LogObj.info("try again start %s ,exec: %s" % (tomcatName, startCmd))
            os.system(startCmd)
            time.sleep(5)
            status = self.checkTomcat(tomcatName)
            if status:
                LogObj.info("start %s successful!" % (tomcatName))
                break
            else:
                LogObj.error("start %s failed" % (tomcatName))
            if num >= self.stopFailRetriesNum:
                LogObj.error("end try start %s" % (tomcatName))
                # break
                print("当前线程数量:", WorkThread.WorkThread.getThreadCount())
                LogObj.error("start service failed, terminate the program")
                exit("start %s failed"%(tomcatName))

    # 检查tomcat是否启动成功
    def checkTomcat(self, tomcatName):
        execCmd = "ps -ef|grep %s|grep -v 'grep'|awk '{print $2}'" % tomcatName
        result = os.popen(execCmd)
        pidList = result.read()
        if not str(pidList).strip():
            LogObj.info("%s status is stop" % (tomcatName))
            return False
        LogObj.info("%s status is running" % (tomcatName))
        return True

    # 获取tomcatPid
    def getTomcatPid(self,tomcatName):
        execCmd = "ps -ef|grep %s|grep -v 'grep'|awk '{print $2}'" % (tomcatName)
        result = os.popen(execCmd)
        pidstr = result.read().strip()
        if pidstr=="":
            return []
        pidList = pidstr.split("\n")
        return pidList

    # 重启项目对应的tomcat
    def restartProjectTom(self, projectName):
        projectInfo = bin.PROJECT_INFO[projectName]
        tomcatList = projectInfo["tomcats"]
        serverIp = bin.CONF_INFO["serverIp"]
        serviceCheckUrl = projectInfo["serviceCheckUrl"]
        maxCheckTime=projectInfo["serviceMaxCheckTime"]

        if tomcatList is None:
            LogObj.error("the restart tomcat tag not given")
            return False
        LogObj.info("will be restarted tomcat tag is :" + str(tomcatList))
        for tomcatId in tomcatList:
            tomcatName = "tomcatA" + tomcatId
            Nginx.closeNginxUpstream(tomcatId)
            self.stopTomcat(tomcatName)
            self.startTomcat(tomcatName)
            if serviceCheckUrl.strip():
                checkurl = "http://" + str(serverIp) + ":" + "80" + tomcatId + "/" + projectName + str(
                    serviceCheckUrl)
                if U.checkService(tomcatId, checkurl, maxCheckTime):
                    Nginx.openNginxUpstream(tomcatId)
                    LogObj.info("%s Restart success !" % (tomcatName))
                else:
                    LogObj.error("%s restart failed, update operation stopped" % (tomcatName))
                    return "false"
            LogObj.info(" project %s update completed" % (tomcatName))
        return True

    # def getTomcatName(self, tag):
    #     if int(tag) >= 10:
    #         tomcatName = "tomcatA" + str(tag)
    #     else:
    #         tomcatName = "tomcatA0" + str(tag)
    #     return tomcatName


def getInstance():
    return Tomcat()
