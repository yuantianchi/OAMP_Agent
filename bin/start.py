# !/usr/bin/env python
# !-*- coding:utf-8 -*-
import sys
sys.path.append(sys.path[0].replace("/bin", ""))

from bin.init import Init
import tornado.web
from tornado.options import define, options
from bin.service import Service
from bin.base.tool import Time
from bin.base.log import PrintLog
from bin.logic.func import RedisFunc

T = Time.getIntance()
R = RedisFunc.getInstance()
L = PrintLog.getInstance()

if __name__ == '__main__':
    # 1、启动redis进程，等待执行相关接口任务
    Init.getInstance().rebuild_memory_val()
    Init.getInstance().init_redis_func_receiver()
    port = 3099
    context = 'OAMP_agent'
    define("port", default=port, help="run on the given port", type=int)
    handlers = [(r"/" + context + "/service", Service.Service), ]
    # 应用设置
    app = tornado.web.Application(
        handlers=handlers,
    )

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    L.info("############################################################################")
    L.info("server started , port is : %s , context is : %s ", port, context)
    # 检测主控服务问题 fixed @me 2018年1月23日22:47:12
    tornado.ioloop.IOLoop.instance().start()
