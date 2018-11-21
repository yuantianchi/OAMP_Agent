#!/usr/bin/env python
# !-*- coding:utf-8 -*-

import sys
import os

class Path(object):
    def __init__(self):
        self.path = sys.path[0]
        # self.projectDirPath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))) + os.sep
        self.projectDirPath = self.path[0:self.path.rindex("bin")]
        self.confDirPath = self.projectDirPath + "conf" + os.sep
        self.logsDirPath = self.projectDirPath + "logs" + os.sep

        if not os.path.exists(self.logsDirPath):
            os.makedirs(self.logsDirPath)


def getInstance():
    return Path()

