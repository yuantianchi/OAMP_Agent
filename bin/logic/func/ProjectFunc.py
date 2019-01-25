#!/usr/bin/env python
# !-*- coding:utf-8 -*-
from bin.base.log import PrintLog
import os
import time
from bin.base.tool import File
import bin
from bin.logic.func import TomcatFun
from bin.base.sys import PR

logObj = PrintLog.getInstance()
Tom = TomcatFun.getInstance()
F = File.getInstance()


class ProjectFunc:

    def __init__(self, projectName):
        self.projectName = projectName
        self.projectInfo = bin.PROJECT_INFO.get(projectName, None)
        self.projectType = self.projectInfo["projectType"]
        self.projectHome = self.projectInfo["projectHome"]
        self.tomcatInfo = dict(self.projectInfo["tomcatInfo"])
        self.backupFilePath = self.projectInfo["backupFilePath"]
        self.webInfPath = self.projectHome + os.sep + "WEB-INF"
        self.projectlibPath = self.webInfPath + os.sep + "lib"
        self.projectResourceLib = self.webInfPath + os.sep + "ResourceLib"
        self.projectStaticPath = self.webInfPath + os.sep + "ResourceLib.TMP" + os.sep + self.projectName + os.sep + "LEAP" + os.sep

    # 替换项目资源
    def replaceProjectResource(self, projectVersion):
        _PR = PR.getInstance()
        # 判断项目类型
        if (self.projectType == "LEAP"):
            return self.replaceLEAPResource(projectVersion)
        elif (self.projectType == "JERSYSE"):
            return self.replaceJersyResource(projectVersion)
        else:
            return _PR.setCode(PR.Code_ERROR).setMsg("%s项目类型未知，请检查配置文件" % (self.projectName))

    # 更新项目
    def updateProject(self, projectVersion):
        _PR = PR.getInstance()
        handleResourcePR = self.handleResource(projectVersion)
        if handleResourcePR.getCode() != PR.Code_OK:
            return handleResourcePR
        replaceProjectResourcePR = self.replaceProjectResource(projectVersion)
        if replaceProjectResourcePR.getCode() != PR.Code_OK:
            return replaceProjectResourcePR
        restartProjectTomPR = Tom.restartProjectTom(self.projectName)
        if restartProjectTomPR != PR.Code_OK:
            return restartProjectTomPR
        logObj.info("%s项目更新成功!" % self.projectName)
        return _PR.setCode(PR.Code_OK).setMsg("更新项目成功")

    # 解压文件夹并赋予权限
    def handleResource(self, projectVersion):
        _PR = PR.getInstance()
        tarFileStatus, modifyAccess = 0, 0
        backTARFilePath = self.backupFilePath + os.sep + projectVersion + ".tar.gz"
        tarCmd = "tar -xzf %s -C %s" % (backTARFilePath, F.getFileParentPath(backTARFilePath))
        logObj.info("unzip file, exec: tar -xzf %s -C %s" % (backTARFilePath, F.getFileParentPath(backTARFilePath)))

        tarFileStatus = os.system(tarCmd)
        if int(tarFileStatus):
            return _PR.setCode(PR.Code_ERROR).setMsg("解压更新资源异常失败")
        logObj.info("modify file permissions, exec: chmod -R 755 %s" % (backTARFilePath))
        os.system("chmod -R 755 %s" % (backTARFilePath))
        if int(modifyAccess):
            return _PR.setCode(PR.Code_ERROR).setMsg("修改更新资源权限异常失败")
        return _PR.setCode(PR.Code_OK).setMsg("解压更新资源并赋予权限成功")

    # 更新jersy项目 替换配置文件、war包
    def replaceJersyResource(self, projectVersion):
        _PR = PR.getInstance()
        unzipFileStatus, cpConfStatus, updateWarStatus, updateResourceStatus, modifyAccessStatus = 0, 0, 0, 0, 0
        updateFilePath = self.backupFilePath + os.sep + projectVersion
        warUzipPath = updateFilePath + os.sep + self.projectName
        warFile = warUzipPath + ".war"
        F.makedir(warUzipPath)
        unzipCmd = "unzip -o " + warFile + " -d " + warUzipPath
        logObj.info("unzip file, exec: %s" % (unzipCmd))
        unzipFileStatus = os.system(unzipCmd)
        if int(unzipFileStatus):
            return _PR.setCode(PR.Code_ERROR).setMsg('解压war包异常失败')
        cpConfCmd = "\cp -rf %s/* %s/" % (self.backupConfPath,
                                          warUzipPath + os.sep + "WEB-INF" + os.sep + "classes")
        logObj.info("replacement profile, exec: %s" % (cpConfCmd))
        cpConfStatus = os.system(cpConfCmd)
        if int(cpConfStatus):
            return _PR.setCode(PR.Code_ERROR).setMsg('替换配置文件到war解压文件失败')
        for tomcatName in self.tomcatInfo.keys():
            webappsPath = self.projectHome + os.sep + "tomcatA" + tomcatName + os.sep + "webapps"
            projectpath = webappsPath + os.sep + self.projectName
            cpWarCmd = "\cp -rf %s %s/" % (warFile, webappsPath)
            logObj.info("replace the war package, exec: %s" % (cpWarCmd))
            updateWarStatus = os.system(cpWarCmd)
            if int(updateWarStatus):
                return _PR.setCode(PR.Code_ERROR).setMsg('替换war包失败')
            # 等待war包解压
            time.sleep(2)
            cpCmd = "\cp -rf %s/* %s/" % (warUzipPath, projectpath)
            logObj.info("update project file, exec: %s" % (cpCmd))
            updateResourceStatus = os.system(cpCmd)
            if int(updateResourceStatus):
                return _PR.setCode(PR.Code_ERROR).setMsg('替换war包解压资源失败')
            chownCmd = "chown -R tomcat:tomcat %s" % (projectpath)
            logObj.info("modify file permission, exec：%s" % (chownCmd))
            modifyAccessStatus = os.system(chownCmd)
            if int(modifyAccessStatus):
                return _PR.setCode(PR.Code_ERROR).setMsg('修改项目文件权限失败')
        return _PR.setCode(PR.Code_OK).setMsg('更新资源成功')

    # 更新LEAP项目资源
    def replaceLEAPResource(self, projectVersion):
        updateFilePath = self.backupFilePath + os.sep + projectVersion
        updatelibPath = updateFilePath + os.sep + "lib"
        updateResourceLib = updateFilePath + os.sep + "ResourceLib"
        updateStatic = updateFilePath + os.sep + "static"
        _PR = PR.getInstance()
        updateLibStatus, updateResourceLibStatus, updateStaticStatus = 0, 0, 0
        if F.isExitsPath(updatelibPath):
            cpLibCmd = "\cp -rf %s/* %s" % (updatelibPath, self.projectlibPath)
            logObj.info("copy lib package, exec: " + cpLibCmd)
            updateLibStatus = os.system(cpLibCmd)
            if int(updateLibStatus):
                return _PR.setCode(PR.Code_ERROR).setMsg("替换lib资源异常失败")

            modifylibAccCmd = "chown -R tomcat:tomcat %s" % updatelibPath
            logObj.info("Modify project lib package permissions, exec: " + modifylibAccCmd)
            os.system(modifylibAccCmd)

        if F.isExitsPath(updateResourceLib):
            cpResourceLibCmd = "\cp -rf %s/* %s" % (updateResourceLib, self.projectResourceLib)
            logObj.info("copy ResourceLib package, exec: " + cpResourceLibCmd)
            updateResourceLibStatus = os.system(cpResourceLibCmd)
            if int(updateResourceLibStatus):
                return _PR.setCode(PR.Code_ERROR).setMsg("替换ResourceLib资源异常失败")
            modifyResourceLibAccCmd = "chown -R tomcat:tomcat %s" % (updateResourceLib)
            logObj.info("Modify project ResourceLib package permissions, exec: " + modifyResourceLibAccCmd)
            os.system(modifyResourceLibAccCmd)

        if F.isExitsPath(updateStatic):
            cpStaticPathCmd = "\cp -rf %s/* %s" % (updateStatic, self.projectStaticPath)
            logObj.info("copy static package,exec: " + cpStaticPathCmd)
            updateStaticStatus = os.system(cpStaticPathCmd)
            if int(updateStaticStatus):
                return _PR.setCode(PR.Code_ERROR).setMsg("替换static资源异常失败")
            modifyStaticAccCmd = "chown -R tomcat:tomcat %s" % (updateStatic)
            logObj.info("Modify project static package permissions, exec: " + modifyStaticAccCmd)
            os.system(modifyStaticAccCmd)
        return _PR.setCode(PR.Code_OK).setMsg("替换版本资源包成功")


def getInstance(projectName):
    return ProjectFunc(projectName)
