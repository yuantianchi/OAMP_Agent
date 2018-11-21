#!/usr/bin/env python
# !-*- coding:utf-8 -*-

from util import JsonFileFunc
from util import Path
import bin

jff = JsonFileFunc.getInstance()
p = Path.getInstance()

class Init:
    def __init__(self):
        self.confPath = p.confDirPath + "conf.json"
        self.ProjectConfigPath = p.confDirPath + "projectInfo.json"


    def getProjectInfo(self):
        confData = jff.readFile(self.confPath)
        projectData = jff.readFile(self.ProjectConfigPath)
        bin.PROJECT_INFO = projectData
        bin.CONF_INFO = confData


    def initProjectInfo(self, projectConfig):
        jff.writeFile(self.ProjectConfigPath, projectConfig)
        pass



def getInstance():
    return Init()
