#!/usr/bin/env python
# !-*- coding:utf-8 -*-

import json

Code_ERROR = "0"  # 错误
Code_OK = "1"  # 成功


class ResartInfo(object):
    def __init__(self):
        self.code = Code_OK
        self.msg = "ok"
        self.failList = []

    def json(self):
        """JSON format data."""
        json = {
            'code': self.code,
            'msg': self.msg,
            'failList': self.failList,
        }
        return json

    def setCode(self, code=1):
        self.code = code
        return self

    def setMsg(self, msg="ok"):
        self.msg = msg
        return self

    def setfailList(self, list=[]):
        self.failList = list
        return self
    def getCode(self):
        return self.code

    def getMsg(self):
        return self.msg
    def getFailList(self):
        return self.failList
    def getResartInfo(self):
        return self

def getInstance():
    return ResartInfo()
