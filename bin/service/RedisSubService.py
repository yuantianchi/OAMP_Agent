#!/usr/bin/env python
# !-*- coding:utf-8 -*-
from bin.base.log import PrintLog
import os
import time
from bin.base.tool import File, FileTransfer
import bin
from bin.logic.func import TomcatFun

logObj = PrintLog.getInstance()
Tom = TomcatFun.getInstance()
F = File.getInstance()


class ProjectFunc:

    def __init__(self, updateInfo):
        # self.sftpInfo = bin.CONF_INFO["proxySftp"]
        self.allProjectInfo = bin.PROJECT_INFO
        self.updateInfo = updateInfo
        self.projectName = self.updateInfo["projectName"]
        self.projectVersion = self.updateInfo["projectVersion"]

        self.projectInfo = self.allProjectInfo[self.projectName]
        self.projectType = self.projectInfo["projectType"]
        self.projectHome = self.projectInfo["projectHome"]
        self.tomcatInfo = dict(self.projectInfo["tomcatInfo"])

        self.proxyVersionPath = self.sftpInfo["proxyPath"] + os.sep + self.projectName + os.sep + str(self.projectVersion)
        self.localVersionPath = self.projectInfo["backupFilePath"] + os.sep + str(self.projectVersion)
        self.proxyCMPFilePath = self.proxyVersionPath + ".tar.gz"
        self.localCMPFilePath = self.localVersionPath + ".tar.gz"

        self.sftpIp = self.sftpInfo["serverIP"]
        self.sftpPort = self.sftpInfo["port"]
        self.sftpUser = self.sftpInfo["username"]
        self.sftpPassWord = self.sftpInfo["password"]

        # 若本地不存在更新文件存放目录着自动创建
        F.makedir(self.projectInfo["backupFilePath"])

    # 从本机拿资源更新（已上传更新文件到服务上时使用）
    def localUpdateProject(self):
        self.judgeProject()

    def judgeProject(self):
        # 判断项目类型
        if (self.projectType == "leap"):
            self.replaceLEAPResource()
        elif (self.projectType == "jersey"):
            self.replaceJersyResource()
        else:
            exit("%s the project type is unknown, please check the configuration file" % (self.projectName))
        Tom.restartProjectTom(self.projectName)

    # 创建ssh连接
    def getconnetion(self):
        try:
            fileTransfer = FileTransfer.getInstance(hostname=self.sftpIp, username=self.sftpUser,
                                                    password=self.sftpPassWord, port=self.sftpPort)
        except Exception as e:
            exit("create a connection to the proxy server ssh failed：%s" % (str(e)))
        return fileTransfer

    # 更新项目
    def updateProject(self):
        self.handleResource()
        self.judgeProject()

    # 更新项目
    def updateProject_redis(self):
        fileTransfer = self.getconnetion()
        self.copyProxyFile(fileTransfer)
        while not self.compareLocalProxyMD5(fileTransfer):
            self.copyProxyFile(fileTransfer)
        fileTransfer.close()  # 关闭文件传输线程
        self.handleResource()
        self.judgeProject()

    # 拷贝代理服务的更新资源到本地，并解压
    def copyProxyFile(self, fileTransfer):
        if self.projectName is not None:
            F.makedir(self.localVersionPath)
            logObj.info("get the files needed for the update from the proxy server...")
            try:
                fileTransfer.getFile(self.proxyCMPFilePath, self.localCMPFilePath)
            except Exception as e:
                logObj.error("sftp transfer file exception: %s" % (str(e)))
                fileTransfer.close()
                exit("Copy file exception from proxy server: %s" % (str(e)))

    # 校验代理服务器与本地文件的md5值
    def compareLocalProxyMD5(self, fileTransfer):
        try:
            proxyCMPFileMD5 = fileTransfer.exec_command(
                "md5sum %s | awk '{print $1}'" % (self.proxyCMPFilePath)).read().decode()
            localCMPFileMD5 = os.popen("md5sum %s | awk '{print $1}'" % (self.localCMPFilePath)).readline()
            if (proxyCMPFileMD5 == localCMPFileMD5):
                return True
            else:
                logObj.info(
                    "verify that the local file is inconsistent with the remote file, try to continue the transfer")
        except Exception as e:
            logObj.error(e)
            return False

    # 解压文件夹并赋予权限
    def handleResource(self):
        tarCmd = "tar -xzf %s -C %s" % (self.localCMPFilePath, F.getFileParentPath(self.localCMPFilePath))
        logObj.info("unzip file, exec: tar -xzf %s -C %s" % (self.localCMPFilePath, F.getFileParentPath(self.localCMPFilePath)))
        os.system(tarCmd)
        logObj.info("modify file permissions, exec: %s" %(self.localVersionPath))
        os.system("chmod -R 755 %s" % (self.localVersionPath))

    # 更新jersy项目 替换配置文件、war包
    def replaceJersyResource(self):
        backupConfPath = self.projectInfo["backupConfPath"]
        warUzipPath = self.localVersionPath + os.sep + self.projectName
        warFile = warUzipPath + ".war"
        F.makedir(warUzipPath)
        unzipCmd = "unzip -o " + warFile + " -d " + warUzipPath
        logObj.info("unzip file, exec: %s" % (unzipCmd))
        os.system(unzipCmd)
        cpConfCmd = "\cp -rf %s/* %s/" % (backupConfPath,
                                          warUzipPath + os.sep + "WEB-INF" + os.sep + "classes")
        logObj.info("replacement profile, exec: %s" % (cpConfCmd))
        os.system(cpConfCmd)
        for tomcatName in self.tomcatInfo.keys():
            webappsPath = self.projectHome + os.sep + "tomcatA" + tomcatName + os.sep + "webapps"
            projectpath = webappsPath + os.sep + self.projectName
            cpWarCmd = "\cp -rf %s/*.war %s/" % (self.localVersionPath, webappsPath)
            logObj.info("replace the war package, exec: %s" % (cpWarCmd))
            os.system(cpWarCmd)

            # 等待war包解压
            time.sleep(2)
            cpCmd = "\cp -rf %s/* %s/" % (warUzipPath, projectpath)
            logObj.info("update project file, exec: %s" % (cpCmd))
            os.system(cpCmd)
            chownCmd = "chown -R tomcat:tomcat %s" % (projectpath)
            logObj.info("modify file permission, exec：%s" % (chownCmd))
            os.system(chownCmd)

    # 更新LEAP项目资源
    def replaceLEAPResource(self):
        webInfPath = self.projectHome + os.sep + self.projectName + os.sep + "WEB-INF"
        projectlibPath = webInfPath + os.sep + "lib"
        projectResourceLib = webInfPath + os.sep + "ResourceLib"
        projectStaticPath = webInfPath + os.sep + "ResourceLib.TMP" + os.sep + self.projectName + os.sep + "LEAP" + os.sep
        updatelibPath = self.localVersionPath + os.sep + "lib"
        updateResourceLib = self.localVersionPath + os.sep + "ResourceLib"
        updatestatic = self.localVersionPath + os.sep + "static"

        if (F.isExitsPath(updatelibPath)):
            cpLibCmd = "\cp -rf %s/* %s" % (updatelibPath, projectlibPath)
            logObj.info("copy Lib package, exec: " + cpLibCmd)
            os.system(cpLibCmd)
        if (F.isExitsPath(updateResourceLib)):
            cpResourceLibCmd = "\cp -rf %s/* %s" % (updateResourceLib, projectResourceLib)
            logObj.info("copy ResourceLib package, exec: " + cpResourceLibCmd)
            os.system(cpResourceLibCmd)
        if (F.isExitsPath(updatestatic)):
            cpStaticPathCmd = "\cp -rf %s/* %s" % (updatestatic, projectStaticPath)
            logObj.info("copy static package,exec: " + cpStaticPathCmd)
            os.system(cpStaticPathCmd)

def getInstance(info):
    return ProjectFunc(info)
