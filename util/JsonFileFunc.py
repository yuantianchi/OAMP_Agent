#!/usr/bin/env python
# !-*- coding:utf-8 -*-
import json
import codecs

from util import PrintLog

L = PrintLog.getInstance()

class JsonFileFunc(object):
    def __init__(self):
        pass

    # read json file
    def readFile(self, filePath):
        data = None
        try:
            with open(filePath, "r", encoding="utf-8") as f:
              data = json.load(f)
        except Exception as e:
            L.error("read [  %s ] not exists, %s", str(filePath), str(e))
            pass

        return data


    # create json file
    def writeFile(self, filePath, data):
        try:
            with codecs.open(filePath, 'w', encoding='utf-8') as tmpFile:
                tmpFile.write(json.dumps(data, ensure_ascii=False, indent=4))
        except Exception as e:
            L.error('create %s fail , %s', str(filePath), str(e))
            pass

def getInstance():
    return JsonFileFunc()