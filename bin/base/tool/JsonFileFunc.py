#!/usr/bin/env python
# !-*- coding:utf-8 -*-
import json
import codecs

from bin.base.log import PrintLog

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
        return data


    # create json file
    def writeFile(self, filePath, data):
        try:
            with codecs.open(filePath, 'w', encoding='utf-8') as tmpFile:
                tmpFile.write(json.dumps(data, ensure_ascii=False, indent=4))
                return True
        except Exception as e:
            L.error('create %s fail , %s', str(filePath), str(e))
            return False

    # json 格式转换为字符串
    def json_to_str(self,json_data):
        if isinstance(json_data, str):
            return json_data
        if json_data is None:
            return ''
        return json.dumps(json_data)


def getInstance():
    return JsonFileFunc()