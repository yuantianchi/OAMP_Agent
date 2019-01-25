#!/usr/bin/env python
# !-*- coding:utf-8 -*-
import sys

sys.path.append(sys.path[0].replace("/bin/service", ""))

import getopt
from bin.base.tool import Time
from bin.base.log import PrintLog
from bin.logic.func import ShellFunc
from bin.base.sys import PR
import traceback

method = None
projectName = None
projectVersion = None

L = PrintLog.getInstance()
SF = ShellFunc.getInstance()
T = Time.getIntance()
_PR = PR.getInstance()
from bin.init import Init

Init.getInstance().rebuild_memory_val()
if __name__ == '__main__':

    options, args = getopt.getopt(sys.argv[1:], "hm:p:v:", ["help", "method=", "project=", "version="])
    if (len(options) <= 0):
        method = "help"
        print(SF.help().getMsg())
        sys.exit(1)
    else:
        for name, value in options:
            if name in ['-h', '--help']:
                if method is not None:
                    L.error("请使用正确的方法")
                    sys.exit(1)

            elif name in ['-m', '--method']:
                if value is None or str(value).startswith("-"):
                    L.info("-m:--method 需要参数method名")
                    sys.exit(1)
                method = value

            elif name in ['-p', '--project']:
                if value is None or str(value).startswith("-"):
                    L.info("-m:--project 需要参数projectname")
                    sys.exit(1)
                projectName = value

            elif name in ['-v', '--version']:
                if value is None or str(value).startswith("-"):
                    L.info("-v:--version 需要参数version")
                    sys.exit(1)
                projectVersion = value
            else:
                method = "help"
                print(SF.help().getMsg())
                sys.exit(1)
    info = {"method": method, "projectName": projectName, "projectVersion": projectVersion}
    startTime = T.getCurrentTime()
    try:
        r = getattr(SF, method)(info)
        if r.getCode() == PR.Code_OK:
            L.info("msg:" + str(r.getMsg()) + ", data:" + str(r.getData()))
        elif r.getCode() == PR.Code_ERROR:
            L.error("msg:" + str(r.getMsg()))
        else:
            L.exception("msg:" + str(r.getMsg()))
    except BaseException as e:
        exceptMessage = "run %s method exception: %s" % (method, str(e))
        L.error(exceptMessage)
        L.error(traceback.format_exc())
