#!/usr/bin/env python
# !-*- coding:utf-8 -*-

import tornado.web
from tornado import gen
from bin.base.sys import PR
from bin.base.log import PrintLog
from bin.logic import Service_loigc
from bin.base.tool import Time
from bin.base.tool import Mail
import json
import traceback

SL = Service_loigc.getInstance()
_PR = PR.getInstance()
L = PrintLog.getInstance()
T = Time.getIntance()

from concurrent.futures import ThreadPoolExecutor
from tornado.concurrent import run_on_executor


class Service(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(20)

    @gen.coroutine
    def post(self):
        result = yield self.done()
        self.write(result)

    @run_on_executor
    def done(self, *args, **kwargs):
        method = 'default_method'
        try:
            starTime = T.getCurrentTime()
            request_body = str(self.request.body, encoding="utf-8")
            if request_body is None or request_body == "":
                _PR.setCode(PR.Code_PARERROR)
                _PR.setMsg("not set the request data")
                return self.write(PR.getPRBytes(_PR.json()))
            info = json.loads(request_body)
            data = info.get('data', None)

            method = data.get('method', '__error__')
            if method == "__error__":
                _PR.setCode(PR.Code_METHODERROR)
                _PR.setMsg("method ERROR, not give the method or get the method is __error__")
                return _PR.json()
            L.info("接受到客户端请求执行%s操作，完整请求：%s" % (method, str(data)))
            r = getattr(SL, method)(data)
            if r.getCode() == PR.Code_OK:
                L.info("msg:" + str(r.getMsg()) + ",data:" + str(r.getData()))
            elif r.getCode() == PR.Code_ERROR:
                L.error("msg:" + str(r.getMsg()))
            else:
                L.exception("msg:" + str(r.getMsg()))
            return r.json()
        except BaseException as e:
            exceptMessage = "run %s method exception: %s" % (method, str(e))
            L.error(exceptMessage)
            L.error(traceback.format_exc())
            Mail.getInstance().sendMail(str(exceptMessage) + str(traceback.format_exc()))
            return _PR.setCode(PR.Code_EXCEPTION).setMsg(exceptMessage).json()

    @gen.coroutine
    def get(self):
        self.post()
