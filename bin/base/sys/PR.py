#!/usr/bin/env python
# !-*- coding:utf-8 -*-

import json

'''
        @author:windStreet
        @time:2017年8月7日15:32:42
        @version:V0.1.0
        @func:"PR CODE defined"
        @notice:
            Code_ERROR = "0"  # 错误
            Code_OK = "1"  # 成功
            Code_EXCEPTION = "2"  # 异常（exception 异常信息）
            Code_PARERROR = "000"  # 参数错误（传递参数为空或者无法取值）
            Code_DATAERROR = "001"  # 数据错误（数据解析过程错误）
            Code_METHODERROR = "002"  # 方法错误 （传递方法名称不存在）
        @return:
'''
Code_ERROR = "0"  # 错误
Code_PARERROR = "000"  # 参数错误
Code_DATAERROR = "001"  # 数据错误
Code_METHODERROR = "002"  # 方法错误
Code_OK = "1"  # 成功
Code_EXCEPTION = "2"  # 异常 [出现未知情况]
Code_WARNING = "3"  # 警告 [出现一些不应该发生的事情，但未造成重大影响]
Code_NORETURN = "003"  # 无返回错误 ,无返回结果情况
Code_REQUESTSTATEERROR = "004"  # 请求状态错误


class PR(object):
    def __init__(self):
        self.code = Code_OK
        self.msg = "ok"
        self.result = None
        self.pageCount = 1
        self.pageNum = 0
        self.pageSize = 0

    def json(self):
        """JSON format data."""
        json = {
            'code': self.code,
            'msg': self.msg,
            'result': self.result,
        }
        return json

    def setCode(self, code=1):
        self.code = code
        return self

    def setMsg(self, msg="ok"):
        self.msg = msg
        return self

    def setResult(self, result):
        self.result = result
        try:
            if hasattr(result, 'count'):
                self.pageCount = result.count()
        except Exception as e:
            self.pageCount = 0
        if hasattr(result, 'to_json'):
            self.result = {
                'data': json.loads(result.to_json()) if (self.pageCount > 0) else None,
                'pageCount': self.pageCount,
                'pageNum': self.pageNum,
                'pageSize': self.pageSize
            }
        return self

    def setData(self, data):
        if self.result is None:
            self.result = {}
        self.result['data'] = data
        return self

    def getCode(self):
        return self.code

    def getMsg(self):
        return self.msg

    def getResult(self):
        return self.result

    def getData(self):
        return self.result.get('data')

    def getPR(self):
        return self

    def getPageCount(self):
        return self.pageCount

    def setpageCount(self, pageCount):
        self.pageCount = pageCount
        return self

    def getPageNum(self):
        return self.pageNum

    def setPageNum(self, pageNum):
        self.pageNum = pageNum
        return self

    def getPageSize(self):
        return self.pageSize

    def setPageSize(self, pageSize):
        self.pageSize = pageSize
        return self

    def is_result_not_none(self):
        return self is not None and self.getCode() == Code_OK and self.result is not None

    def is_results_not_none(self):
        return self is not None and self.getCode() == Code_OK and self.getData() is not None and len(self.getData()) > 0


def getInstance():
    return PR()


# 数据必须是json格式
def getPRBytes(data):
    return bytes(json.dumps(data, sort_keys=True, indent=4), encoding='utf-8')
