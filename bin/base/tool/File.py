#!/usr/bin/env python
# !-*- coding:utf-8 -*-
import os
from bin.base.log import PrintLog


class File(object):
    def __init__(self):
        self.LogObj = PrintLog.getInstance()

    #若文件夹不存在则创建
    def makedir(self,dir):
        if not os.path.exists(dir):
            self.LogObj.info("mkdir %s"%(dir))
            os.makedirs(dir)
    #判断文件是否存在
    def isExitsFile(self,path):
        if os.path.exists(path):
            return True
        return  False

    #判断文件夹是否存在
    def isExitsPath(self,path):
        if os.path.exists(path) and os.path.isdir(path):
            return True
        return False

    #去掉文件名，返回目录
    def getFileParentPath(self, filePath):
        parentPath=os.path.dirname(filePath)
        return parentPath

def getInstance():
    return File()
