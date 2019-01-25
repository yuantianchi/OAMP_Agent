#!/usr/bin/env python
# !-*- coding:utf-8 -*-

import sys
import os

class Path(object):
    def __init__(self):
        self.path = sys.path[0]
        self.projectDirPath = self.path[0:self.path.rindex("bin")]
        self.confDirPath = self.projectDirPath + "conf"
        self.logsDirPath = self.projectDirPath + "logs"
        self.runTimeDirPath=self.projectDirPath+"runTime"
        if not os.path.exists(self.logsDirPath):
            os.makedirs(self.logsDirPath)


def getInstance():
    return Path()

