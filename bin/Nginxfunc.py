#!/usr/bin/env python
# !-*- coding:utf-8 -*-
from util import PrintLog
import bin
import os
LogObj = PrintLog.getInstance()

class NginxFunc:
    # 关闭nginx upstream流
    def closeNginxUpstream(self, tomcatId):
        LogObj.info("close nginx upstream to 80%s port" % (tomcatId))
        # cmd = "sed -i \"s/^.*server.*80%s/#&/g\" %s" % (tomcatId, bin.CONF_INFO["nginxUpstreamPath"])
        cmd = "sed -i \"/^.*server.*80%s/s/;/ down&/g\" %s" % (tomcatId, bin.CONF_INFO["nginxUpstreamPath"])
        os.system(cmd)
        self.reloadNginx()

    # 开启nginx upstream 流
    def openNginxUpstream(self, tomcatId):
        LogObj.info("open nginx upstream to 80%s port" % (tomcatId))
        # cmd = "sed -i \"/^#.*server.*80%s/s/^#\+//\" %s" % (tomcatId, bin.CONF_INFO["nginxUpstreamPath"])
        cmd = "sed -i \"/^.*server.*80%s.*down/s/ down//g\" %s" % (tomcatId, bin.CONF_INFO["nginxUpstreamPath"])
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