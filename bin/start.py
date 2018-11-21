# !/usr/bin/env python
# !-*- coding:utf-8 -*-
import sys

sys.path.append(sys.path[0].replace("/bin", ""))

from util import Time
from util import RedisFunc, PrintLog
from bin import WorkThread

T = Time.getIntance()
R = RedisFunc.getInstance()
LogObj = PrintLog.getInstance()


if __name__ == '__main__':
    while True:
        LogObj.info("Listen on channel...")
        LogObj.info(T.getCurrentTime())
        # msg = r.subscribe().parse_response(block=False, timeout=60)  ##非阻塞如果收不到消息，60秒收不到消息就会返回None。这俩参数可以不加，变成阻塞的
        msg = R.subscribe().parse_response()
        workThred = WorkThread.getInstance(msg)
        workThred.start()



