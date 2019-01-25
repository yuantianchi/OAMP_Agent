#!/usr/bin/env python
# !-*- coding:utf-8 -*-

import bin
from bin.base.sys import PR
from bin.base.log import PrintLog
from bin.base.tool import File
from bin.base.tool import JsonFileFunc
from bin.base.tool import Path
from bin.logic.func import TomcatFun
from bin.logic.func import ProjectFunc
import os

LogObj = PrintLog.getInstance()
jff = JsonFileFunc.getInstance()
p = Path.getInstance()
F = File.getInstance()
T = TomcatFun.getInstance()


class AgentProjectFunc(object):
    def __init__(self):
        pass

    # 重启项目对应的所有tomcat
    def restartProject(self, info):
        _PR = PR.getInstance()
        projectName = info.get("projectName")
        if not projectName:
            return _PR.setCode(PR.Code_ERROR).setMsg('更新项目失败，项目名或项目版本为空').setData(projectName)
        if projectName not in bin.PROJECT_INFO:
            return _PR.setCode(PR.Code_ERROR).setMsg('更新项目失败，angent中还未配置%s项目信息' % projectName).setData(projectName)
        return TomcatFun.getInstance().restartProjectTom(projectName)

    # 更新项目
    def updateProject(self, info):
        _PR = PR.getInstance()
        projectName = info.get("projectName", None)
        projectVersion = info.get("projectVersion", None)
        backupFilePath = bin.PROJECT_INFO.get(projectName)["backupFilePath"]
        # updateFilePath = backupFilePath + os.sep + projectVersion + ".tar.gz"
        updateFilePath = backupFilePath + os.sep + projectVersion
        if not projectName or not projectVersion:
            return _PR.setCode(PR.Code_ERROR).setMsg('更新项目失败，项目名或项目版本为空').setData(projectName)
        if projectName not in bin.PROJECT_INFO:
            return _PR.setCode(PR.Code_ERROR).setMsg('更新项目失败，agent中还未配置%s项目信息' % projectName).setData(projectName)
        if not F.isExitsFile(updateFilePath):
            return _PR.setCode(PR.Code_ERROR).setMsg("%s项目的%s版本的更新资源不存在" % (projectName, projectVersion))
        PF = ProjectFunc.getInstance(projectName)
        _PR = PR.getInstance()
        replaceProjectResourcePR = PF.replaceProjectResource(projectVersion)
        if replaceProjectResourcePR.getCode() != PR.Code_OK:
            return replaceProjectResourcePR
        restartProjectTomPR = T.restartProjectTom(projectName)
        if restartProjectTomPR != PR.Code_OK:
            return restartProjectTomPR
        result = {"projectName": "projectName", "projectVersion": projectVersion}
        return _PR.setCode(PR.Code_OK).setMsg("更新项目成功").setData(result)

    def help(self):
        methods = list(filter(lambda m: not m.startswith("__") and not m.endswith("__") and callable(getattr(self, m)), dir(self)))
        _PR = PR.getInstance()
        return _PR.setCode(PR.Code_OK).setMsg("Please use the following methods：" + str(methods))


def getInstance():
    return AgentProjectFunc()
