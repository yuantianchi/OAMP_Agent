#!/usr/bin/env python
# !-*- coding:utf-8 -*-
from bin.base.log import PrintLog
import bin
import os
LogObj = PrintLog.getInstance()

class NginxFunc:
    def __init__(self):
        pass

    # 关闭nginx upstream流
    def closeNginxUpstream(self, nginxPort):
        nginxUpstreamPath = bin.CONF_INFO.get("nginxUpstreamPath", None)
        if not nginxUpstreamPath:
            exit("Nginx path is not specified")
        LogObj.info("close nginx upstream to %s port" % str(nginxPort))
        # cmd = "sed -i \"s/^.*server.*80%s/#&/g\" %s" % (tomcatId, bin.CONF_INFO["nginxUpstreamPath"])
        cmd = "sed -i \"/^.*server.*%s/s/;/ down&/g\" %s" % (nginxPort, nginxUpstreamPath)
        os.system(cmd)
        self.reloadNginx()

    # 开启nginx upstream 流
    def openNginxUpstream(self, nginxPort):
        nginxUpstreamPath = bin.CONF_INFO.get("nginxUpstreamPath", None)
        if not nginxUpstreamPath:
            exit("Nginx path is not specified")
        LogObj.info("open nginx upstream to %s port" % str(nginxPort))
        # cmd = "sed -i \"/^#.*server.*80%s/s/^#\+//\" %s" % (tomcatId, bin.CONF_INFO["nginxUpstreamPath"])
        cmd = "sed -i \"/^.*server.*%s.*down/s/ down//g\" %s" % (nginxPort, nginxUpstreamPath)
        os.system(cmd)
        self.reloadNginx()


    # 重启加载nginx配置
    def reloadNginx(self):
        LogObj.info("reload nginx")
        cmd = "ps -ef |grep nginx |grep -v \"grep\" |grep -E \"master.*process\" | awk '{print $2}'"
        masterPid = os.popen(cmd).readline().strip()
        if masterPid:
            cmd = "kill -HUP %s" % (masterPid)
            os.system(cmd)
        else:
            LogObj.error("nginx main process not found")

def getInstance():
    return NginxFunc()